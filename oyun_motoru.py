#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unicode Game Lab - Oyun Motoru
Oynanabilir terminal tabanlı oyun motoru
"""

import os
import sys
from typing import List, Tuple, Optional
from game_lab import KarakterAnlamSistemi

# Windows konsolunda UTF-8 desteği için
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except:
        pass


class OyunMotoru:
    """Terminal tabanlı oyun motoru"""
    
    def __init__(self, harita: List[List[str]], karakter_sistemi: Optional[KarakterAnlamSistemi] = None):
        """Oyun motorunu başlat"""
        self.harita = [satir[:] for satir in harita]  # Kopyala
        self.karakter_sistemi = karakter_sistemi or KarakterAnlamSistemi()
        self.oyuncu_x, self.oyuncu_y = self._oyuncu_konum_bul()
        self.hareket_sayisi = 0
        self.oyun_devam = True
        
    def _oyuncu_konum_bul(self) -> Tuple[int, int]:
        """Oyuncunun konumunu bul"""
        for y, satir in enumerate(self.harita):
            for x, karakter in enumerate(satir):
                bilgi = self.karakter_sistemi.karakter_bul(karakter)
                if bilgi and bilgi.get("ozellik") == "Oyuncu":
                    return x, y
        return 1, 1  # Varsayılan
    
    def _ekran_temizle(self):
        """Ekranı temizle (cross-platform)"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def _harita_goster(self):
        """Haritayı ekrana yazdır"""
        print("=" * 60)
        print("🎮 UNICODE GAME LAB")
        print("=" * 60)
        print(f"Hareket: {self.hareket_sayisi} | WASD veya ↑↓←→ ile hareket edin")
        print("=" * 60)
        print()
        
        for satir in self.harita:
            print(" ".join(satir))
        
        print()
        print("=" * 60)
    
    def _karakter_kontrol(self, x: int, y: int) -> bool:
        """Belirli bir konumda oyuncu geçebilir mi?"""
        if y < 0 or y >= len(self.harita) or x < 0 or x >= len(self.harita[y]):
            return False
        
        karakter = self.harita[y][x]
        bilgi = self.karakter_sistemi.karakter_bul(karakter)
        
        if not bilgi:
            return True  # Bilinmeyen karakter = boş
        
        ozellik = bilgi.get("ozellik", "")
        
        # Geçilebilir karakterler
        if ozellik in ["Boş", "Su", "Hedef", "Anahtar", "Enerji"]:
            return True
        
        # Geçilemez karakterler
        if ozellik in ["Blok", "Duvar", "Diken", "Tuzak", "Kapı"]:
            return False
        
        # İtilebilir nesneler için kontrol
        if ozellik in ["İtilebilir", "Yönlü İtilebilir"]:
            return False  # İtilebilir, geçilemez ama itilebilir
        
        return True
    
    def _itilebilir_mi(self, x: int, y: int) -> Tuple[bool, Optional[str]]:
        """Belirli bir konumdaki nesne itilebilir mi?"""
        if y < 0 or y >= len(self.harita) or x < 0 or x >= len(self.harita[y]):
            return False, None
        
        karakter = self.harita[y][x]
        bilgi = self.karakter_sistemi.karakter_bul(karakter)
        
        if not bilgi:
            return False, None
        
        ozellik = bilgi.get("ozellik", "")
        
        if ozellik == "İtilebilir":
            return True, karakter
        
        if ozellik == "Yönlü İtilebilir":
            # Yön kontrolü gerekirse buraya eklenebilir
            return True, karakter
        
        return False, None
    
    def _hedef_var_mi(self) -> bool:
        """Haritada hedef var mı?"""
        for satir in self.harita:
            for karakter in satir:
                bilgi = self.karakter_sistemi.karakter_bul(karakter)
                if bilgi and bilgi.get("ozellik") == "Hedef":
                    return True
        return False
    
    def _hedefe_ulasildi_mi(self) -> bool:
        """Oyuncu hedefe ulaştı mı?"""
        # Oyuncu konumunda P var, ama hedef O'nun üzerinde miyiz kontrol et
        # Eğer haritada O kalmadıysa, oyuncu O'nun üzerinde demektir
        o_var_mi = False
        for satir in self.harita:
            for karakter in satir:
                bilgi = self.karakter_sistemi.karakter_bul(karakter)
                if bilgi and bilgi.get("ozellik") == "Hedef" and karakter == "O":
                    o_var_mi = True
                    break
            if o_var_mi:
                break
        return not o_var_mi  # O yoksa hedefe ulaşılmış demektir
    
    def _hareket_et(self, dx: int, dy: int) -> bool:
        """Oyuncuyu hareket ettir"""
        yeni_x = self.oyuncu_x + dx
        yeni_y = self.oyuncu_y + dy
        
        # Sınır kontrolü
        if yeni_y < 0 or yeni_y >= len(self.harita) or \
           yeni_x < 0 or yeni_x >= len(self.harita[yeni_y]):
            return False
        
        hedef_karakter = self.harita[yeni_y][yeni_x]
        hedef_bilgi = self.karakter_sistemi.karakter_bul(hedef_karakter)
        
        # Boş alana hareket
        if hedef_bilgi and hedef_bilgi.get("ozellik") in ["Boş", "Su", "Hedef", "Anahtar", "Enerji"]:
            # Eski konumu boş yap
            self.harita[self.oyuncu_y][self.oyuncu_x] = " "
            
            # Yeni konuma taşı
            self.oyuncu_x = yeni_x
            self.oyuncu_y = yeni_y
            # Hedefe ulaşmadıysa P koy, ulaştıysa O üzerinde P olsun
            if hedef_bilgi.get("ozellik") != "Hedef":
                self.harita[self.oyuncu_y][self.oyuncu_x] = "P"
            else:
                self.harita[self.oyuncu_y][self.oyuncu_x] = "P"  # Hedefe ulaşınca da P göster
            self.hareket_sayisi += 1
            return True
        
        # İtilebilir nesne kontrolü
        itilebilir_mi, nesne_karakter = self._itilebilir_mi(yeni_x, yeni_y)
        
        if itilebilir_mi:
            # İtilecek nesnenin arkasındaki konum
            itme_x = yeni_x + dx
            itme_y = yeni_y + dy
            
            # İtme konumu geçerli mi ve boş mu?
            if 0 <= itme_y < len(self.harita) and 0 <= itme_x < len(self.harita[itme_y]):
                itme_karakter = self.harita[itme_y][itme_x]
                itme_bilgi = self.karakter_sistemi.karakter_bul(itme_karakter)
                
                # İtme konumu boş veya geçilebilir mi?
                if itme_bilgi and itme_bilgi.get("ozellik") in ["Boş", "Su", "Hedef"]:
                    # Nesneyi it
                    self.harita[itme_y][itme_x] = nesne_karakter
                    # Oyuncuyu hareket ettir
                    self.harita[self.oyuncu_y][self.oyuncu_x] = " "
                    self.oyuncu_x = yeni_x
                    self.oyuncu_y = yeni_y
                    self.harita[self.oyuncu_y][self.oyuncu_x] = "P"
                    self.hareket_sayisi += 1
                    return True
        
        return False  # Hareket edilemedi
    
    def _komut_al(self) -> str:
        """Kullanıcıdan komut al"""
        try:
            komut = input("\nHareket (W/A/S/D veya ↑↓←→, Q=Çıkış): ").strip().upper()
            return komut
        except (EOFError, KeyboardInterrupt):
            return "Q"
    
    def _komut_islem(self, komut: str) -> bool:
        """Komutu işle ve hareket et"""
        hareket_haritasi = {
            "W": (0, -1),  # Yukarı
            "S": (0, 1),   # Aşağı
            "A": (-1, 0),  # Sol
            "D": (1, 0),   # Sağ
            "↑": (0, -1),
            "↓": (0, 1),
            "←": (-1, 0),
            "→": (1, 0),
            "8": (0, -1),  # Numpad
            "2": (0, 1),
            "4": (-1, 0),
            "6": (1, 0),
        }
        
        if komut == "Q":
            return False  # Çıkış
        
        if komut in hareket_haritasi:
            dx, dy = hareket_haritasi[komut]
            self._hareket_et(dx, dy)
            return True
        
        return True  # Geçersiz komut ama oyun devam eder
    
    def oyunu_baslat(self):
        """Oyunu başlat ve döngüyü çalıştır"""
        if not self._hedef_var_mi():
            print("⚠️  Uyarı: Haritada hedef (O) bulunamadı!")
            return
        
        while self.oyun_devam:
            self._ekran_temizle()
            self._harita_goster()
            
            if self._hedefe_ulasildi_mi():
                print("\n🎉 TEBRİKLER! Hedefe ulaştınız!")
                print(f"📊 Toplam hareket: {self.hareket_sayisi}")
                break
            
            komut = self._komut_al()
            
            if komut == "Q":
                print("\n👋 Oyundan çıkılıyor...")
                break
            
            if not self._komut_islem(komut):
                break
        
        print("\n✅ Oyun bitti!")


def main():
    """Ana fonksiyon - Örnek harita ile oyun başlat"""
    from ornek_haritalar import ornek_harita_1
    
    print("🎮 Unicode Game Lab - Oyun Motoru")
    print("=" * 60)
    print("\nKontroller:")
    print("  W / ↑ : Yukarı")
    print("  S / ↓ : Aşağı")
    print("  A / ← : Sol")
    print("  D / → : Sağ")
    print("  Q     : Çıkış")
    print("\n" + "=" * 60)
    input("\nDevam etmek için Enter'a basın...")
    
    # Oyun motorunu başlat
    motor = OyunMotoru(ornek_harita_1)
    motor.oyunu_baslat()


if __name__ == "__main__":
    main()
