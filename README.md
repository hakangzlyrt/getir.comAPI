# Getir Market Fiyat Analizi

Bu proje, Getir marketteki ürünlerin fiyatlarını analiz eden bir Python uygulamasıdır.

## Özellikler

- Getir marketteki ürünlerin fiyatlarını CSV formatında kaydetme
- Ürün kategorilerine göre en düşük fiyatları hesaplama
- Sonuçları CSV dosyasına kaydetme

## Kurulum

1. Repository'yi klonlayın:
```bash
git clone [repository-url]
```

2. Gerekli Python paketlerini yükleyin:
```bash
pip install -r requirements.txt
```

## Kullanım

1. Ürün fiyatlarını analiz etmek için:
```bash
python hesapla.py
```

## Dosya Yapısı

- `getircvs/` - CSV dosyalarının bulunduğu klasör
  - `getir_tum_urunler.csv` - Tüm ürünlerin listesi
  - `ortalama_fiyatlar.csv` - Analiz sonuçları

## Gereksinimler

- Python 3.x
- pandas 