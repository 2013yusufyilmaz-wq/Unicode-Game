#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unicode Game Lab - Karakter Anlam Sistemi
Python ve JSON kullanarak karakter tabanlı oyun öğelerini yönetir
"""

import json
import os
import sys
from typing import Dict, List, Optional, Tuple

# Windows konsolunda UTF-8 desteği için
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except:
        pass  # Eski Python versiyonları için


class KarakterAnlamSistemi:
    """Karakter anlamlarını JSON'dan okuyup yöneten sınıf"""
    
    def __init__(self, json_dosya: str = "karakter_anlamlari.json"):
        """JSON dosyasından karakter anlamlarını yükle"""
        self.json_dosya = json_dosya
        self.karakter_veritabani = {}
        self.kategori_veritabani = {}
        self._json_yukle()
    
    def _json_yukle(self):
        """JSON dosyasını yükle ve veritabanlarını oluştur"""
        # JSON dosyasının tam yolunu bul
        if not os.path.isabs(self.json_dosya):
            # Göreceli yol ise, script'in bulunduğu dizinde ara
            script_dir = os.path.dirname(os.path.abspath(__file__))
            json_path = os.path.join(script_dir, self.json_dosya)
        else:
            json_path = self.json_dosya
        
        if not os.path.exists(json_path):
            print(f"⚠️  Uyarı: {json_path} dosyası bulunamadı!")
            return
        
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Her kategori için işlem yap
            for kategori, bilgi in data.items():
                self.kategori_veritabani[kategori] = bilgi
                
                # Karakter listesi var mı?
                if "karakterler" in bilgi:
                    # Liste mi dict mi?
                    if isinstance(bilgi["karakterler"], list):
                        # Normal liste
                        for karakter in bilgi["karakterler"]:
                            self.karakter_veritabani[karakter] = {
                                "kategori": kategori,
                                "ozellik": bilgi.get("ozellik", ""),
                                "aciklama": bilgi.get("aciklama", ""),
                                **{k: v for k, v in bilgi.items() if k not in ["karakterler", "ozellik", "aciklama"]}
                            }
                    elif isinstance(bilgi["karakterler"], dict):
                        # Özel dict (yönlü itilebilir gibi)
                        for karakter, yon in bilgi["karakterler"].items():
                            self.karakter_veritabani[karakter] = {
                                "kategori": kategori,
                                "ozellik": bilgi.get("ozellik", ""),
                                "aciklama": bilgi.get("aciklama", ""),
                                "yon": yon,
                                **{k: v for k, v in bilgi.items() if k not in ["karakterler", "ozellik", "aciklama"]}
                            }
            
            print(f"✅ {len(self.karakter_veritabani)} karakter yüklendi!")
            
        except json.JSONDecodeError as e:
            print(f"❌ JSON hatası: {e}")
        except Exception as e:
            print(f"❌ Hata: {e}")
    
    def karakter_bul(self, karakter: str) -> Optional[Dict]:
        """Bir karakterin özelliklerini döndür"""
        return self.karakter_veritabani.get(karakter)
    
    def karakter_ozellik(self, karakter: str) -> str:
        """Karakterin özelliğini döndür (örn: 'Blok', 'Oyuncu')"""
        bilgi = self.karakter_bul(karakter)
        return bilgi.get("ozellik", "Bilinmiyor") if bilgi else "Bilinmiyor"
    
    def karakter_aciklama(self, karakter: str) -> str:
        """Karakterin açıklamasını döndür"""
        bilgi = self.karakter_bul(karakter)
        return bilgi.get("aciklama", "") if bilgi else ""
    
    def kategori_listesi(self) -> List[str]:
        """Tüm kategorilerin listesini döndür"""
        return list(self.kategori_veritabani.keys())
    
    def kategorideki_karakterler(self, kategori: str) -> List[str]:
        """Belirli bir kategorideki tüm karakterleri döndür"""
        kategori_bilgi = self.kategori_veritabani.get(kategori, {})
        if "karakterler" in kategori_bilgi:
            if isinstance(kategori_bilgi["karakterler"], list):
                return kategori_bilgi["karakterler"]
            elif isinstance(kategori_bilgi["karakterler"], dict):
                return list(kategori_bilgi["karakterler"].keys())
        return []
    
    def karakter_ekle(self, karakter: str, kategori: str, ozellik: str, 
                     aciklama: str = "", **ekstra):
        """Yeni bir karakter ekle (sadece runtime için, JSON'ı güncellemez)"""
        self.karakter_veritabani[karakter] = {
            "kategori": kategori,
            "ozellik": ozellik,
            "aciklama": aciklama,
            **ekstra
        }
    
    def harita_analiz_et(self, harita: List[List[str]]) -> Dict:
        """Bir harita üzerindeki tüm karakterleri analiz et"""
        analiz = {
            "toplam_karakter": 0,
            "karakter_tipleri": {},
            "oyuncu_konum": None,
            "ozellikler": {}
        }
        
        for y, satir in enumerate(harita):
            for x, karakter in enumerate(satir):
                if karakter in self.karakter_veritabani:
                    analiz["toplam_karakter"] += 1
                    bilgi = self.karakter_bul(karakter)
                    kategori = bilgi["kategori"]
                    ozellik = bilgi["ozellik"]
                    
                    # Karakter tipi sayısı
                    if ozellik not in analiz["karakter_tipleri"]:
                        analiz["karakter_tipleri"][ozellik] = 0
                    analiz["karakter_tipleri"][ozellik] += 1
                    
                    # Oyuncu konumu
                    if ozellik == "Oyuncu":
                        analiz["oyuncu_konum"] = (x, y)
        
        return analiz
    
    def tum_karakterleri_listele(self) -> Dict[str, Dict]:
        """Tüm yüklenen karakterleri ve özelliklerini döndür"""
        return self.karakter_veritabani.copy()
    
    def ozellik_ile_ara(self, ozellik: str) -> List[str]:
        """Belirli bir özelliğe sahip tüm karakterleri bul"""
        sonuc = []
        for karakter, bilgi in self.karakter_veritabani.items():
            if bilgi.get("ozellik") == ozellik:
                sonuc.append(karakter)
        return sonuc
    
    def rapor_yazdir(self):
        """Yüklenen tüm karakterleri güzel bir şekilde yazdır"""
        print("\n" + "="*60)
        print("📋 KARAKTER RAPORU")
        print("="*60)
        
        for kategori, bilgi in sorted(self.kategori_veritabani.items()):
            print(f"\n🏷️  {kategori.upper()}")
            print(f"   Özellik: {bilgi.get('ozellik', 'N/A')}")
            print(f"   Açıklama: {bilgi.get('aciklama', 'N/A')}")
            
            if "karakterler" in bilgi:
                if isinstance(bilgi["karakterler"], list):
                    karakterler_str = " ".join(bilgi["karakterler"][:10])
                    if len(bilgi["karakterler"]) > 10:
                        karakterler_str += f" ... (+{len(bilgi['karakterler'])-10} daha)"
                    print(f"   Karakterler: {karakterler_str}")
                elif isinstance(bilgi["karakterler"], dict):
                    print(f"   Karakterler:")
                    for kar, yon in bilgi["karakterler"].items():
                        print(f"     {kar} → {yon}")
        
        print("\n" + "="*60)
        print(f"📊 Toplam {len(self.karakter_veritabani)} benzersiz karakter")
        print("="*60 + "\n")


def main():
    """Test ve örnek kullanım"""
    print("🎮 Unicode Game Lab - Karakter Anlam Sistemi\n")
    
    # Sistemi başlat
    lab = KarakterAnlamSistemi("karakter_anlamlari.json")
    
    # Rapor yazdır
    lab.rapor_yazdir()
    
    # Örnek kullanımlar
    print("\n🔍 ÖRNEK KULLANIMLAR:")
    print("-" * 40)
    
    # Karakter sorgulama
    test_karakterler = ["P", "#", "~", "🟥", "⬆️", "△"]
    for karakter in test_karakterler:
        bilgi = lab.karakter_bul(karakter)
        if bilgi:
            print(f"\nKarakter: {karakter}")
            print(f"  Özellik: {bilgi['ozellik']}")
            print(f"  Açıklama: {bilgi.get('aciklama', 'N/A')}")
            if 'yon' in bilgi:
                print(f"  Yön: {bilgi['yon']}")
        else:
            print(f"\nKarakter: {karakter} → Bulunamadı!")
    
    # Özellik ile arama
    print("\n\n🔎 'İtilebilir' özelliğine sahip karakterler:")
    itilebilirler = lab.ozellik_ile_ara("İtilebilir")
    print(f"   {', '.join(itilebilirler[:15])}")
    if len(itilebilirler) > 15:
        print(f"   ... ve {len(itilebilirler)-15} tane daha")
    
    # Harita analizi örneği
    print("\n\n🗺️  ÖRNEK HARİTA ANALİZİ:")
    ornek_harita = [
        ["#", "#", "#", "#", "#"],
        ["#", "P", " ", "🟥", "#"],
        ["#", " ", "~", " ", "#"],
        ["#", "⬆️", "O", " ", "#"],
        ["#", "#", "#", "#", "#"]
    ]
    analiz = lab.harita_analiz_et(ornek_harita)
    print(f"   Toplam karakter: {analiz['toplam_karakter']}")
    print(f"   Karakter tipleri: {analiz['karakter_tipleri']}")
    if analiz['oyuncu_konum']:
        print(f"   Oyuncu konumu: {analiz['oyuncu_konum']}")


if __name__ == "__main__":
    main()
