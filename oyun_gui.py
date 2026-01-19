#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unicode Game Lab - Grafik Arayüz (GUI)
Tkinter ile görsel oyun arayüzü
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sys
from typing import List, Tuple, Optional
from game_lab import KarakterAnlamSistemi
from oyun_motoru import OyunMotoru


class OyunGUI:
    """Grafik arayüzlü oyun motoru"""
    
    def __init__(self, root: tk.Tk, harita: List[List[str]], harita_adi: str = "Harita"):
        self.root = root
        self.root.title(f"🎮 Unicode Game Lab - {harita_adi}")
        self.root.geometry("800x700")
        self.root.configure(bg="#020617")
        
        # Harita ve motor
        self.harita = [satir[:] for satir in harita]
        self.karakter_sistemi = KarakterAnlamSistemi()
        self.motor = OyunMotoru(self.harita, self.karakter_sistemi)
        
        # Renk şeması (neon mavi tema)
        self.colors = {
            "bg": "#020617",
            "bg_light": "#0a1440",
            "text": "#1ec8ff",
            "text_soft": "#6be7ff",
            "border": "#1ec8ff",
            "block": "#1a1a2e",
            "player": "#00ff00",
            "target": "#ffff00",
            "water": "#0080ff",
            "box": "#ff6b00",
            "wall": "#333333"
        }
        
        # Hücre boyutu
        self.cell_size = 40
        self.padding = 10
        
        # Arayüz oluştur
        self._arayuz_olustur()
        self._haritayi_ciz()
        
        # Klavye bağlantısı
        self.root.bind("<KeyPress>", self._klavye_hareket)
        self.root.focus_set()
    
    def _arayuz_olustur(self):
        """Arayüz elemanlarını oluştur"""
        # Üst bilgi paneli
        info_frame = tk.Frame(self.root, bg=self.colors["bg_light"], relief=tk.RAISED, bd=2)
        info_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Başlık
        title_label = tk.Label(
            info_frame,
            text="🎮 Unicode Game Lab",
            font=("Orbitron", 16, "bold"),
            fg=self.colors["text"],
            bg=self.colors["bg_light"]
        )
        title_label.pack(side=tk.LEFT, padx=10, pady=5)
        
        # Bilgi etiketleri
        info_text = tk.Label(
            info_frame,
            text="W/A/S/D veya ↑↓←→ ile hareket | Q: Çıkış",
            font=("Arial", 10),
            fg=self.colors["text_soft"],
            bg=self.colors["bg_light"]
        )
        info_text.pack(side=tk.RIGHT, padx=10, pady=5)
        
        # Canvas (harita için)
        canvas_frame = tk.Frame(self.root, bg=self.colors["bg"])
        canvas_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=5)
        
        # Scrollbar
        scrollbar_y = tk.Scrollbar(canvas_frame, orient=tk.VERTICAL)
        scrollbar_x = tk.Scrollbar(canvas_frame, orient=tk.HORIZONTAL)
        
        self.canvas = tk.Canvas(
            canvas_frame,
            bg=self.colors["bg"],
            highlightthickness=0,
            yscrollcommand=scrollbar_y.set,
            xscrollcommand=scrollbar_x.set
        )
        
        scrollbar_y.config(command=self.canvas.yview)
        scrollbar_x.config(command=self.canvas.xview)
        
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.canvas.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        
        # Alt bilgi paneli
        status_frame = tk.Frame(self.root, bg=self.colors["bg_light"], relief=tk.RAISED, bd=2)
        status_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.status_label = tk.Label(
            status_frame,
            text="Hareket: 0",
            font=("Arial", 12),
            fg=self.colors["text"],
            bg=self.colors["bg_light"]
        )
        self.status_label.pack(padx=10, pady=5)
        
        # Butonlar
        button_frame = tk.Frame(self.root, bg=self.colors["bg"])
        button_frame.pack(fill=tk.X, padx=5, pady=5)
        
        restart_btn = tk.Button(
            button_frame,
            text="🔄 Yeniden Başlat",
            command=self._yeniden_baslat,
            font=("Arial", 10),
            bg="#1a1a2e",
            fg=self.colors["text"],
            activebackground="#2a2a3e",
            activeforeground=self.colors["text_soft"],
            relief=tk.RAISED,
            bd=2,
            cursor="hand2"
        )
        restart_btn.pack(side=tk.LEFT, padx=5)
        
        # Anasayfaya Dön butonu
        home_btn = tk.Button(
            button_frame,
            text="🏠 Anasayfaya Dön",
            command=self._anasayfaya_don,
            font=("Arial", 10),
            bg="#1a1a2e",
            fg=self.colors["text"],
            activebackground="#2a2a3e",
            activeforeground=self.colors["text_soft"],
            relief=tk.RAISED,
            bd=2,
            cursor="hand2"
        )
        home_btn.pack(side=tk.LEFT, padx=5)
        
        exit_btn = tk.Button(
            button_frame,
            text="❌ Çıkış",
            command=self.root.quit,
            font=("Arial", 10),
            bg="#1a1a2e",
            fg=self.colors["text"],
            activebackground="#2a2a3e",
            activeforeground=self.colors["text_soft"],
            relief=tk.RAISED,
            bd=2,
            cursor="hand2"
        )
        exit_btn.pack(side=tk.RIGHT, padx=5)
    
    def _karakter_rengi(self, karakter: str) -> str:
        """Karaktere göre renk döndür"""
        bilgi = self.karakter_sistemi.karakter_bul(karakter)
        if not bilgi:
            return "#ffffff"
        
        ozellik = bilgi.get("ozellik", "")
        
        renk_haritasi = {
            "Oyuncu": self.colors["player"],
            "Hedef": self.colors["target"],
            "Blok": self.colors["block"],
            "Duvar": self.colors["wall"],
            "Su": self.colors["water"],
            "Lav": "#ff0000",
            "Asit": "#00ff00",
            "İtilebilir": self.colors["box"],
            "Yönlü İtilebilir": "#ff9900",
            "Diken": "#ff3333",
            "Anahtar": "#ffff00",
            "Kapı": "#8b4513",
            "Enerji": "#00ffff",
            "Boş": self.colors["bg"]
        }
        
        return renk_haritasi.get(ozellik, "#ffffff")
    
    def _haritayi_ciz(self):
        """Haritayı canvas üzerine çiz"""
        self.canvas.delete("all")
        
        if not self.motor.harita:
            return
        
        rows = len(self.motor.harita)
        cols = len(self.motor.harita[0]) if rows > 0 else 0
        
        # Canvas boyutunu ayarla
        canvas_width = cols * self.cell_size + 2 * self.padding
        canvas_height = rows * self.cell_size + 2 * self.padding
        
        self.canvas.config(scrollregion=(0, 0, canvas_width, canvas_height))
        
        # Her hücreyi çiz
        for y, satir in enumerate(self.motor.harita):
            for x, karakter in enumerate(satir):
                x1 = x * self.cell_size + self.padding
                y1 = y * self.cell_size + self.padding
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                
                # Arka plan
                renk = self._karakter_rengi(karakter)
                self.canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill=renk,
                    outline=self.colors["border"],
                    width=1,
                    tags=f"cell_{x}_{y}"
                )
                
                # Karakteri göster (emoji veya metin)
                if karakter and karakter != " ":
                    # Karakterden emoji'ye dönüşüm haritası
                    emoji_haritasi = {
                        "P": "🧑",  # Oyuncu
                        "p": "🧑",  # Oyuncu (küçük harf)
                        "O": "⭐",  # Hedef
                        "o": "⭐",  # Hedef (küçük harf)
                        "#": "⬛",  # Blok
                        "■": "⬛",  # Blok
                        "□": "⬜",  # Blok (açık)
                        "~": "💧",  # Su
                        "K": "🔑",  # Anahtar
                        "k": "🔑",  # Anahtar (küçük harf)
                        "D": "🚪",  # Kapı
                        "d": "🚪",  # Kapı (küçük harf)
                        "X": "💀",  # Tuzak
                        "x": "💀",  # Tuzak (küçük harf)
                        "<": "▶️",  # Diken
                        ">": "◀️",  # Diken
                        "▲": "⬆️",  # Diken yukarı
                        "△": "⬆️",  # Diken yukarı
                        "▷": "➡️",  # Diken sağ
                        "▼": "⬇️",  # Diken aşağı
                        "◁": "⬅️",  # Diken sol
                        "|": "▮",   # Duvar dikey
                        "-": "▬",   # Duvar yatay
                        "=": "▬",   # Duvar kalın
                    }
                    
                    # Emoji haritasında varsa kullan, yoksa orijinal karakter
                    text = emoji_haritasi.get(karakter, karakter)
                    
                    # Text renk (emoji'ler için uygun renkler)
                    if karakter in ["P", "p"]:
                        text_color = "#ffffff"  # Oyuncu emoji için beyaz
                    elif karakter in ["O", "o"]:
                        text_color = "#ffff00"  # Hedef emoji için sarı
                    elif karakter == "~":
                        text_color = "#00bfff"  # Su emoji için mavi
                    elif self.karakter_sistemi.karakter_bul(karakter) and \
                         self.karakter_sistemi.karakter_bul(karakter).get("ozellik") in ["İtilebilir", "Yönlü İtilebilir"]:
                        text_color = "#ffffff"  # İtilebilir nesneler için beyaz
                    elif karakter in emoji_haritasi and karakter not in ["P", "p", "O", "o", "~"]:
                        text_color = "#ffffff"  # Diğer emoji'ler için beyaz
                    else:
                        text_color = self.colors["text"] if renk == self.colors["bg"] else "#ffffff"
                    
                    # Emoji'ler için daha büyük font, normal karakterler için standart
                    font_boyutu = 24 if text in emoji_haritasi.values() else 16
                    font_adi = ("Segoe UI Emoji", font_boyutu) if text in emoji_haritasi.values() else ("Arial", font_boyutu, "bold")
                    
                    self.canvas.create_text(
                        (x1 + x2) / 2,
                        (y1 + y2) / 2,
                        text=text,
                        font=font_adi,
                        fill=text_color,
                        tags=f"text_{x}_{y}"
                    )
        
        # Canvas'ı ortala ve scroll ayarla
        self.canvas.update()
        canvas_frame_width = self.canvas.winfo_width()
        canvas_frame_height = self.canvas.winfo_height()
        
        if canvas_width < canvas_frame_width:
            scroll_x = (canvas_frame_width - canvas_width) / 2
            self.canvas.xview_moveto(0)
        else:
            scroll_x = 0
        
        if canvas_height < canvas_frame_height:
            scroll_y = (canvas_frame_height - canvas_height) / 2
            self.canvas.yview_moveto(0)
        else:
            scroll_y = 0
        
        # Durum güncelle
        self._durum_guncelle()
    
    def _durum_guncelle(self):
        """Durum bilgisini güncelle"""
        hareket = self.motor.hareket_sayisi
        self.status_label.config(text=f"Hareket: {hareket}")
        
        # Hedefe ulaşıldı mı kontrol
        if self.motor._hedefe_ulasildi_mi():
            messagebox.showinfo(
                "🎉 Tebrikler!",
                f"Hedefe ulaştınız!\nToplam hareket: {hareket}"
            )
            # Yeniden başlatmayı sor
            if messagebox.askyesno("Yeniden Oyna", "Yeniden oynamak ister misiniz?"):
                self._yeniden_baslat()
            else:
                self.root.quit()
    
    def _klavye_hareket(self, event):
        """Klavye hareketini işle"""
        komut_haritasi = {
            "w": "W",
            "a": "A",
            "s": "S",
            "d": "D",
            "q": "Q",
            "Up": "W",
            "Down": "S",
            "Left": "A",
            "Right": "D"
        }
        
        komut = komut_haritasi.get(event.keysym, "")
        
        if komut == "Q":
            if messagebox.askyesno("Çıkış", "Oyundan çıkmak istediğinize emin misiniz?"):
                self.root.quit()
            return
        
        if komut:
            self.motor._komut_islem(komut)
            self._haritayi_ciz()
    
    def _yeniden_baslat(self):
        """Oyunu yeniden başlat"""
        from copy import deepcopy
        # Orijinal haritayı yeniden yükle
        orijinal_harita = [[karakter for karakter in satir] for satir in self.harita]
        self.motor = OyunMotoru(orijinal_harita, self.karakter_sistemi)
        self._haritayi_ciz()
    
    def _anasayfaya_don(self):
        """Anasayfaya (menüye) dön"""
        if messagebox.askyesno("Anasayfaya Dön", "Anasayfaya dönmek istediğinize emin misiniz?\n(Oyun ilerlemeniz kaydedilmeyecek)"):
            self.root.destroy()
            # Ana menüyü tekrar başlat
            main()


def main():
    """Ana fonksiyon - GUI ile oyun başlat"""
    from ornek_haritalar import (
        ornek_harita_1, ornek_harita_2, ornek_harita_3,
        ornek_harita_4, ornek_harita_5, ornek_harita_6
    )
    
    # Windows UTF-8 desteği
    if sys.platform == 'win32':
        try:
            sys.stdout.reconfigure(encoding='utf-8')
            sys.stderr.reconfigure(encoding='utf-8')
        except:
            pass
    
    # Ana pencere
    root = tk.Tk()
    
    # Harita seçimi için basit menü
    def harita_sec_menu():
        menu_window = tk.Toplevel(root)
        menu_window.title("Harita Seç")
        menu_window.geometry("400x500")
        menu_window.configure(bg="#020617")
        menu_window.grab_set()  # Modal yap
        
        tk.Label(
            menu_window,
            text="🎮 Harita Seçin",
            font=("Arial", 16, "bold"),
            fg="#1ec8ff",
            bg="#020617"
        ).pack(pady=20)
        
        haritalar = [
            ("Basit Örnek", ornek_harita_1),
            ("Labirent", ornek_harita_2),
            ("Tuzaklar ve Zorluklar", ornek_harita_3),
            ("Yönlü İtilebilir Nesneler", ornek_harita_4),
            ("Anahtar ve Kapı", ornek_harita_5),
            ("Karmaşık", ornek_harita_6),
        ]
        
        def harita_baslat(isim, harita):
            menu_window.destroy()
            root.destroy()  # Menü penceresini kapat
            
            # Yeni pencere ile oyunu başlat
            game_root = tk.Tk()
            app = OyunGUI(game_root, harita, isim)
            game_root.mainloop()
        
        for isim, harita in haritalar:
            btn = tk.Button(
                menu_window,
                text=isim,
                command=lambda i=isim, h=harita: harita_baslat(i, h),
                font=("Arial", 11),
                bg="#1a1a2e",
                fg="#1ec8ff",
                activebackground="#2a2a3e",
                activeforeground="#6be7ff",
                relief=tk.RAISED,
                bd=2,
                cursor="hand2",
                width=30,
                height=2
            )
            btn.pack(pady=5)
        
        tk.Button(
            menu_window,
            text="❌ İptal",
            command=lambda: (menu_window.destroy(), root.destroy()),
            font=("Arial", 10),
            bg="#1a1a2e",
            fg="#ff3333",
            relief=tk.RAISED,
            bd=2
        ).pack(pady=20)
    
    # Menüyü göster
    harita_sec_menu()
    root.mainloop()  # Ana döngüyü başlat


if __name__ == "__main__":
    main()
