# GreenStay - Tatil Kiralama Platformu

Python 3.12 ve SQLite ile yapılmış hafif bir tatil kiralama platformu. Özellikler ara, rezervasyon yap, yorum bırak ve ev sahibi ile iletişime geç.

**GreenStay**, Airbnb benzeri bir platform olup tam stack web geliştirmeyi öğrenmek için idealdir. Tamamen SQLite ile yapılmıştır - veritabanı sunucusu kurulumuna gerek yoktur.

## Canlı Demo

[http://localhost:5000](http://localhost:5000)

## Özellikler

- Token tabanlı kullanıcı kimlik doğrulaması
- Detaylı emlak listeleme ve arama
- Rezervasyon yapma ve yönetme
- Özellik puanlaması ve yorum sistemi
- Misafir ve ev sahibi arasında mesajlaşma
- Host ve Misafir rol yönetimi
- Modern arayüzle duyarlı tasarım
- Yerleşik SQLite veritabanı - hiç kurulum gerektirmez

## Gereksinimler

- Python 3.12+ (Python 3.13 SQLAlchemy uyumsuzluğu var)
- pip (Python paket yöneticisi)
- SQLite3 (Python ile birlikte gelir)

**ÖNEMLİ**: Bu proje Python 3.12 ile yapılmıştır. SQLAlchemy 2.0.23 Python 3.13 ile uyumsuzluk yaşıyor. Python 3.12 veya daha eski sürüm kullanın.

## Hızlı Başlama (5 dakika)

### 1. Repository'yi İndir
```bash
git clone https://github.com/fatih1963/greenstay.git
cd greenstay
```

### 2. Sanal Ortam Oluştur
```bash
python3.12 -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### 3. Bağımlılıkları Yükle
```bash
pip install -r requirements.txt
```

### 4. Ortam Değişkenlerini Ayarla
```bash
cp .env.example .env
```

### 5. Backend Sunucusunu Başlat
```bash
cd backend
python main.py
```

### 6. Tarayıcıda Aç
```
http://localhost:5000
```

## Proje Yapısı

```
greenstay/
├── backend/
│   ├── main.py              # Flask uygulamasının giriş noktası
│   ├── models/              # SQLAlchemy ORM modelleri
│   │   ├── user.py          # Kullanıcı modeli
│   │   ├── property.py      # Emlak ilanları
│   │   ├── booking.py       # Rezervasyonlar
│   │   ├── review.py        # Puanlamalar ve yorumlar
│   │   └── message.py       # Mesajlaşma
│   ├── routes/              # API endpoint'leri
│   │   ├── auth.py          # Kimlik doğrulama
│   │   ├── property.py      # Emlak işlemleri
│   │   ├── booking.py       # Rezervasyon yönetimi
│   │   ├── review.py        # Yorum sistemi
│   │   └── message.py       # Mesajlaşma
│   └── static/              # Frontend HTML, CSS, JS
├── database/
│   └── airbnb.db           # Otomatik oluşturulan SQLite DB
├── frontend/                # Orijinal frontend kaynak dosyaları
│   ├── html/
│   ├── css/
│   └── js/
├── requirements.txt
├── .env.example
└── README.md
```

## API Dokümantasyonu

### Kimlik Doğrulama Endpoint'leri
```
POST   /api/auth/register      # Yeni hesap oluştur
POST   /api/auth/login         # Giriş yap ve token al
GET    /api/auth/profile       # Profili al (token gerekli)
PUT    /api/auth/profile       # Profili güncelle (token gerekli)
POST   /api/auth/logout        # Çıkış yap (token gerekli)
```

### Emlak Endpoint'leri
```
GET    /api/properties              # Tüm emlakları listele
GET    /api/properties/<id>         # Emlak detaylarını al
POST   /api/properties              # Yeni emlak oluştur (host için)
PUT    /api/properties/<id>         # Emlağı düzenle (host için)
DELETE /api/properties/<id>         # Emlağı sil (host için)
```

### Rezervasyon Endpoint'leri
```
GET    /api/bookings                # Kullanıcı rezervasyonlarını listele (token gerekli)
GET    /api/bookings/<id>           # Rezervasyon detaylarını al (token gerekli)
POST   /api/bookings                # Rezervasyon yap (token gerekli)
DELETE /api/bookings/<id>           # Rezervasyonu iptal et (token gerekli)
```

### Yorum Endpoint'leri
```
GET    /api/reviews/property/<id>   # Emlak yorumlarını al
POST   /api/reviews                 # Yorum yaz (token gerekli)
DELETE /api/reviews/<id>            # Yorumu sil (token gerekli)
```

### Mesajlaşma Endpoint'leri
```
GET    /api/messages                # Konuşmaları al (token gerekli)
POST   /api/messages                # Mesaj gönder (token gerekli)
PUT    /api/messages/<id>/read      # Okundu olarak işaretle (token gerekli)
```

### Kullanıcı Endpoint'leri
```
GET    /api/users                   # Tüm kullanıcıları listele
GET    /api/users/<id>              # Kullanıcı profilini al
```

## Veritabanı

SQLite veritabanı ilk çalıştırmada otomatik olarak `database/airbnb.db`'de oluşturulur.

### Veritabanını Sıfırla
```bash
rm database/airbnb.db
# Backend'i yeniden başlat - yeni veritabanı otomatik oluşturulur
```

## API'yi Test Etme

### Kullanıcı Kaydı
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "gezgin",
    "email": "gezgin@example.com",
    "password": "guvenliSifre123",
    "first_name": "Ahmet",
    "last_name": "Yilmaz"
  }'
```

### Giriş Yap
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "gezgin@example.com",
    "password": "guvenliSifre123"
  }'
```

### Profili Al (token gerekli)
```bash
curl -X GET http://localhost:5000/api/auth/profile \
  -H "Authorization: Bearer TOKEN_BURAYA_YAPISTIR"
```

### Emlakları Gözat
```bash
curl http://localhost:5000/api/properties
```

## Sorun Giderme

### Python 3.13 Uyumsuzluk Hatası
`AssertionError: Class directly inherits TypingOnly` hatası alırsan, Python 3.13 kullanıyorsun.

**Çözüm**: Python 3.12'ye downgrade et
```bash
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Port 5000 Zaten Kullanımda
`backend/main.py` dosyasını düzenle ve portu değiştir:
```python
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
```

### Modül İthal Hatası
Sanal ortamın aktif olduğundan emin ol:
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Veritabanı Sorunları
Veritabanını sıfırla:
```bash
rm database/airbnb.db
python main.py  # Veritabanı yeniden oluşturulacak
```

## Kullanılan Teknolojiler

- **Backend Framework**: Flask 3.0.0
- **ORM**: SQLAlchemy 2.0.23
- **Veritabanı**: SQLite3
- **Frontend**: HTML5, CSS3, JavaScript ES6
- **Kimlik Doğrulama**: Token tabanlı (base64 kodlamalı)
- **API**: CORS destekli RESTful endpoint'ler

## Dosya Boyutları

- Hafif kod tabanı: ~50KB Python kodu
- SQLite veritabanı: ~1MB'den başlar
- Harici servis gerektirmez

## Geliştirme

### Yeni Python Paketi Ekle
```bash
pip install paket_adi
pip freeze > requirements.txt
```

### Frontend'i Backend'e Deploy Et
```bash
mkdir -p backend/static/css backend/static/js
cp frontend/html/* backend/static/
cp -r frontend/css backend/static/
cp -r frontend/js backend/static/
```

### Gunicorn ile Çalıştır (Production)
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 main:app
```

## Katkıda Bulunma

Katkılar hoşlanır! Şunları yapabilirsin:
- Bug raporla
- Özellik öner
- Pull request gönder
- Dokümantasyonu geliştir

## Lisans

MIT Lisansı - Detaylar için LICENSE dosyasına bakın

## Yazar

**Fatih Kaya**
- GitHub: [@fatih1963](https://github.com/fatih1963)
- Proje: [GreenStay](https://github.com/fatih1963/greenstay)

## Yol Haritası

- [ ] Emlaklar için resim yükleme
- [ ] Ödeme entegrasyonu (Stripe/PayPal)
- [ ] Gelişmiş arama filtreleri
- [ ] Leaflet.js ile harita görünümü
- [ ] Fotoğraf ile yorum sistemi
- [ ] E-mail bildirimleri
- [ ] Admin paneli
- [ ] Mobil uygulama (Flutter/React Native)

## Öğrenme Kaynakları

Bu proje şunları gösterir:
- Flask web framework'ü
- SQLAlchemy ORM
- RESTful API tasarımı
- Token tabanlı kimlik doğrulama
- SQLite ile veritabanı tasarımı
- Frontend-backend iletişimi
- HTML/CSS/JavaScript

Şunları öğrenenler için ideal:
- Full-stack web geliştirme
- Python backend geliştirme
- REST API oluşturma
- Veritabanı yönetimi
- Web kimlik doğrulaması

## Destek

Hata buldum? Yardım gerek?
- GitHub'da issue aç
- Mevcut issues'lara bak
- Sorun giderme bölümünü kontrol et

## İlgili Projeler

Benzer öğrenme projeleri:
- Django Blog Platformu
- FastAPI Todo Uygulaması
- Node.js E-ticaret Sitesi

---

**GreenStay** - Python 3.12 + SQLite ile yapılmıştır. Veritabanı sunucusu gerekmez. Full-stack geliştirmeyi öğrenmek için idealdir.

İyi kodlamalar!
