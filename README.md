# 🎮 Unicode Game Lab

Karakter tabanlı terminal oyun motoru - Python ve JSON ile geliştirildi.

## 📋 Özellikler

- ✅ Çeşitli karakter anlamları (Blok, Diken, İtilebilir, Oyuncu, vb.)
- ✅ JSON tabanlı karakter yönetimi
- ✅ Terminal tabanlı oynanabilir oyun motoru
- ✅ İtilebilir nesneler ile oynanış
- ✅ 6 farklı örnek harita
- ✅ Cross-platform (Windows, macOS, Linux)

## 🚀 Kurulum

Python 3.7 veya üzeri gereklidir.

```bash
# Klasöre git
cd "Unicode Game lab"

# Oyunu başlat
python oyun_baslat.py
```

## 🎯 Nasıl Oynanır?

### Kontroller:
- **W** veya **↑** : Yukarı hareket
- **S** veya **↓** : Aşağı hareket
- **A** veya **←** : Sol hareket
- **D** veya **→** : Sağ hareket
- **Q** : Oyundan çık

### Amaç:
- Oyuncu (**P**) karakteri ile hareket edin
- Hedefe (**O**) ulaşın
- Kutuları (**🟥**, **🟧**, **🟨**, vb.) iterek yol açın
- Su (**~**) üzerinden geçebilirsiniz
- Dikenler (**▲**, **△**, **▷**, vb.) ve bloklar (**#**) geçilemez

## 📁 Dosya Yapısı

```
Unicode Game lab/
├── karakter_anlamlari.json   # Karakter anlamları veritabanı
├── game_lab.py               # Karakter anlam sistemi
├── ornek_haritalar.py        # Örnek haritalar (Python)
├── ornek_haritalar.json      # Örnek haritalar (JSON)
├── oyun_motoru.py            # Oyun motoru
├── oyun_baslat.py            # Oyun başlatıcı
└── README.md                 # Bu dosya
```

## 🎲 Örnek Haritalar

1. **Basit Örnek** - Başlangıç için ideal
2. **Labirent** - Karmaşık labirent yapısı
3. **Tuzaklar ve Zorluklar** - Dikenler ve su içeren zorlu harita
4. **Yönlü İtilebilir Nesneler** - Yönlü hareket eden nesneler
5. **Anahtar ve Kapı** - Anahtar toplama ve kapı açma
6. **Karmaşık** - Enerji nesneleri ve tuzaklarla dolu

## 🔧 Kendi Haritanızı Oluşturma

```python
from oyun_motoru import OyunMotoru

# Harita oluştur
benim_haritam = [
    ["#", "#", "#", "#", "#"],
    ["#", "P", " ", " ", "#"],
    ["#", " ", "🟥", " ", "#"],
    ["#", " ", " ", "O", "#"],
    ["#", "#", "#", "#", "#"]
]

# Oyunu başlat
motor = OyunMotoru(benim_haritam)
motor.oyunu_baslat()
```

## 📚 Karakter Anlamları

### Geçilebilir:
- ` ` (Boşluk) - Boş alan
- `~` - Su (geçilebilir ama yavaş)
- `O` - Hedef

### Geçilemez:
- `#` - Blok/Duvar
- `▲`, `△`, `▷`, `▼`, `◁` - Dikenler

### Özel:
- `P` - Oyuncu
- `🟥`, `🟧`, `🟨`, `🟩`, `🟦` - İtilebilir nesneler
- `⬆️`, `➡️`, `⬇️`, `⬅️` - Yönlü itilebilir nesneler
- `K` - Anahtar
- `D` - Kapı
- `⚡`, `💎` - Enerji nesneleri

Tam liste için `karakter_anlamlari.json` dosyasına bakın.

## 🎨 Özelleştirme

`karakter_anlamlari.json` dosyasını düzenleyerek yeni karakterler ve özellikler ekleyebilirsiniz.

## 📝 Lisans

Bu proje örnek amaçlıdır. İstediğiniz gibi kullanabilir ve değiştirebilirsiniz.

## 🤝 Katkıda Bulunma

Kendi haritalarınızı oluşturup paylaşabilirsiniz!

---

**İyi oyunlar! 🎮**
