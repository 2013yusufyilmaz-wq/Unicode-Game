#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unicode Game Lab - Oyun Başlatıcı
Hızlı oyun başlatma scripti
"""

import sys
from ornek_haritalar import (
    ornek_harita_1, ornek_harita_2, ornek_harita_3,
    ornek_harita_4, ornek_harita_5, ornek_harita_6
)
from oyun_motoru import OyunMotoru

def harita_sec():
    """Kullanıcıdan harita seçimi al"""
    print("🎮 UNICODE GAME LAB - OYUN BAŞLAT")
    print("=" * 60)
    print("\nLütfen bir harita seçin:\n")
    print("1. Basit Örnek (10x10) - Başlangıç için ideal")
    print("2. Labirent (15x15) - Karmaşık yapı")
    print("3. Tuzaklar ve Zorluklar (12x12) - Dikenler ve su")
    print("4. Yönlü İtilebilir Nesneler (11x11)")
    print("5. Anahtar ve Kapı (13x9)")
    print("6. Karmaşık (14x14) - Enerji + Tuzaklar")
    print("0. Çıkış")
    print("\n" + "=" * 60)
    
    try:
        secim = input("\nSeçiminiz (1-6, 0=Çıkış): ").strip()
        return secim
    except (EOFError, KeyboardInterrupt):
        return "0"

def main():
    """Ana fonksiyon"""
    # Windows UTF-8 desteği
    if sys.platform == 'win32':
        try:
            sys.stdout.reconfigure(encoding='utf-8')
            sys.stderr.reconfigure(encoding='utf-8')
        except:
            pass
    
    haritalar = {
        "1": ("Basit Örnek", ornek_harita_1),
        "2": ("Labirent", ornek_harita_2),
        "3": ("Tuzaklar ve Zorluklar", ornek_harita_3),
        "4": ("Yönlü İtilebilir Nesneler", ornek_harita_4),
        "5": ("Anahtar ve Kapı", ornek_harita_5),
        "6": ("Karmaşık", ornek_harita_6),
    }
    
    while True:
        secim = harita_sec()
        
        if secim == "0":
            print("\n👋 Görüşmek üzere!")
            break
        
        if secim in haritalar:
            isim, harita = haritalar[secim]
            
            print(f"\n📋 Seçilen harita: {isim}")
            print("\nKontroller:")
            print("  W / ↑ : Yukarı")
            print("  S / ↓ : Aşağı")
            print("  A / ← : Sol")
            print("  D / → : Sağ")
            print("  Q     : Oyundan çık")
            
            input("\n🎮 Oyunu başlatmak için Enter'a basın...")
            
            # Oyun motorunu başlat
            motor = OyunMotoru(harita)
            motor.oyunu_baslat()
            
            # Oyun bittikten sonra tekrar oynamak ister misiniz?
            print("\n" + "=" * 60)
            try:
                devam = input("Başka bir harita oynamak ister misiniz? (E/H): ").strip().upper()
                if devam != "E":
                    print("\n👋 Görüşmek üzere!")
                    break
            except (EOFError, KeyboardInterrupt):
                break
        else:
            print("\n❌ Geçersiz seçim! Lütfen 1-6 arası bir sayı girin.\n")
            input("Devam etmek için Enter'a basın...")

if __name__ == "__main__":
    main()
