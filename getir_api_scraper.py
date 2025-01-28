import requests
import json
from datetime import datetime
import uuid

def scrape_getir_category(category_slug):
    # API URL
    url = f"https://getirx-client-api-gateway.getirapi.com/category/products"
    
    # Query parametreleri
    params = {
        "countryCode": "TR",
        "categorySlug": category_slug,
        "deviceUUID": str(uuid.uuid4()),
        "sessionId": str(uuid.uuid4())
    }
    
    # Headers
    headers = {
        "accept": "*/*",
        "accept-language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7",
        "content-type": "application/json",
        "sec-ch-ua": "\"Not A(Brand\";v=\"8\", \"Chromium\";v=\"132\", \"Google Chrome\";v=\"132\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "cross-site",
        "x-language": "tr",
        "x-merchant": "GETIR",
        "x-platform": "web",
        "x-device-id": str(uuid.uuid4()),
        "x-correlation-id": str(uuid.uuid4()),
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
        "Origin": "https://getir.com",
        "Referer": "https://getir.com/"
    }
    
    try:
        # API'ye istek at
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        
        # JSON verisini al
        data = response.json()
        
        # Response'u kontrol et
        print(f"API Response: {json.dumps(data, indent=2)[:500]}...")
        
        # Sonuçları kaydet
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'getir_products_{category_slug}_{timestamp}.json'
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
            
        print(f"Veriler başarıyla {filename} dosyasına kaydedildi.")
        
        # Ürün sayısını göster
        if 'data' in data and 'products' in data['data']:
            products = data['data']['products']
            print(f"Toplam {len(products)} ürün bulundu.")
            
            # İlk birkaç ürünü göster
            for product in products[:5]:
                name = product.get('name', 'İsimsiz')
                price = product.get('price', 0)
                print(f"Ürün: {name} - Fiyat: {price} TL")
        
    except requests.exceptions.RequestException as e:
        print(f"API isteği hatası: {e}")
        if hasattr(e.response, 'text'):
            print(f"API Response: {e.response.text}")
    except json.JSONDecodeError as e:
        print(f"JSON parse hatası: {e}")
    except Exception as e:
        print(f"Beklenmeyen hata: {e}")

def scrape_all_categories():
    categories = [
        "su-icecek-ewknEvzsJc",
        "temel-gida-IQH9bir3bX",
        "meyve-sebze-H3dt5DZqIp",
        "atistirmalik-r8tu6sxrYX",
        "dondurma-0KD7KsPVX3"
    ]
    
    for category in categories:
        print(f"\nKategori: {category} taranıyor...")
        scrape_getir_category(category)

if __name__ == "__main__":
    scrape_all_categories() 