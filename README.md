🎮 Unicode Game Lab

Unicode Game V0.1.1 Beta

Python ve JSON ile geliştirilmiş, Unicode karakterler üzerinden çalışan modüler bir terminal oyun motoru.

✨ Genel Bakış

Unicode Game Lab;
karakterleri (Unicode / ASCII) oyun nesnesi olarak kullanan, tamamen özelleştirilebilir, hafif ve öğrenmesi kolay bir oyun motorudur.

Terminal tabanlıdır

JSON ile genişletilebilir

Katmanlı ve modüler yapıya uygundur

🚀 Özellikler

✅ Unicode & ASCII karakter tabanlı oyun sistemi

✅ JSON tabanlı karakter tanımları

✅ İtilebilir nesneler (yönlü / yönsüz)

✅ Diken, blok, su, hedef gibi çevresel öğeler

✅ Çoklu örnek harita sistemi

✅ Kolayca genişletilebilir mimari

✅ Cross-platform (Windows / Linux / macOS)

🧩 Oyun Mekanikleri

Oyuncu (P) harita üzerinde hareket eder

İtilebilir nesneler yol açmak için kullanılır

Dikenler ve bloklar engeldir

Hedefe (O) ulaşınca bölüm tamamlanır

Tüm davranışlar JSON üzerinden kontrol edilir

⌨️ Kontroller
Tuş	İşlev
W / ↑	Yukarı
S / ↓	Aşağı
A / ←	Sol
D / →	Sağ
Q	Oyundan çık
📦 Kurulum
Gereksinimler

Python 3.7+

Çalıştırma
cd "Unicode Game Lab"
python oyun_baslat.py


Windows kullanıcıları için .exe çıktısı mevcuttur.

📁 Proje Yapısı
Unicode Game Lab/
├── karakter_anlamlari.json   # Karakter ve davranış tanımları
├── game_lab.py               # Karakter analiz sistemi
├── ornek_haritalar.py        # Python tabanlı haritalar
├── ornek_haritalar.json      # JSON tabanlı haritalar
├── oyun_motoru.py            # Ana oyun motoru
├── oyun_baslat.py            # Başlatıcı
└── README.md

🗺️ Örnek Haritalar

Basit Başlangıç

Labirent

Tuzaklı Alan

Yönlü İtilebilir Nesneler

Anahtar & Kapı Mekaniği

Karmaşık Seviye

🧠 Karakter Sistemi
Geçilebilir

→ Boş alan

~ → Su

O → Hedef

Geçilemez

# → Duvar / Blok

▲ △ ▷ ▼ ◁ → Dikenler

Özel

P → Oyuncu

🟥 🟧 🟨 🟩 🟦 → İtilebilir nesneler

⬆️ ➡️ ⬇️ ⬅️ → Yönlü itilebilir nesneler

K → Anahtar

D → Kapı

⚡ 💎 → Enerji / Özel nesneler

👉 Tüm tanımlar: karakter_anlamlari.json

🛠️ Kendi Haritanı Oluştur
from oyun_motoru import OyunMotoru

harita = [
    ["#", "#", "#", "#", "#"],
    ["#", "P", " ", " ", "#"],
    ["#", " ", "🟥", " ", "#"],
    ["#", " ", " ", "O", "#"],
    ["#", "#", "#", "#", "#"]
]

motor = OyunMotoru(harita)
motor.oyunu_baslat()

🎨 Özelleştirme

Yeni karakter ekle

Var olanların davranışını değiştir

Renk / Unicode / çarpışma kurallarını ayarla

👉 Hepsi JSON üzerinden.

🧪 Sürüm Bilgisi

Unicode Game V0.1.1 Beta

Stabil çekirdek

Genişletilebilir yapı

Sprite destekli V2 planlanıyor

📜 Lisans

Bu proje eğitim ve deneysel amaçlıdır.
Serbestçe kullanılabilir, geliştirilebilir.

🤝 Katkı

Harita ekle

Yeni mekanik öner

Unicode karakter setini genişlet

İyi oyunlar ve iyi kodlamalar! 🎮🚀