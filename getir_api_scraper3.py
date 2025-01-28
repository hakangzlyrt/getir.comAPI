import requests
import json
from datetime import datetime
import time

def scrape_category(category_slug):
    # API URL
    url = f"https://getirx-client-api-gateway.getirapi.com/category/products"
    
    # Query parametreleri
    params = {
        "countryCode": "TR",
        "categorySlug": category_slug
    }
    
    # Headers
    headers = {
        "accept": "*/*",
        "accept-language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7",
        "content-type": "application/json",
        "priority": "u=1, i",
        "sec-ch-ua": "\"Not A(Brand\";v=\"8\", \"Chromium\";v=\"132\", \"Google Chrome\";v=\"132\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "cross-site",
        "x-language": "tr",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
        "Origin": "https://getir.com",
        "Referer": "https://getir.com/"
    }
    
    try:
        # API'ye istek at
        print(f"\nKategori çekiliyor: {category_slug}")
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        
        # JSON verisini al
        data = response.json()
        
        # Sonuçları kaydet
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'getir_products_{category_slug}_{timestamp}.json'
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
            
        print(f"Veriler başarıyla {filename} dosyasına kaydedildi.")
        
        # Kategori bilgilerini göster
        if 'data' in data and 'category' in data['data']:
            category_data = data['data']['category']
            name = category_data.get('name', '')
            product_count = category_data.get('productCount', 0)
            print(f"Kategori: {name} - Toplam {product_count} ürün")
            
            # Alt kategorileri göster
            subcategories = category_data.get('subCategories', [])
            if subcategories:
                print("\nAlt kategoriler:")
                for sub in subcategories:
                    sub_name = sub.get('name', '')
                    sub_count = sub.get('productCount', 0)
                    print(f"- {sub_name}: {sub_count} ürün")
                    
                    # Alt kategori ürünlerini göster
                    products = sub.get('products', [])
                    for product in products[:3]:  # İlk 3 ürünü göster
                        product_name = product.get('name', '')
                        product_price = product.get('price', 0)
                        print(f"  * {product_name}: {product_price} TL")
        
    except requests.exceptions.RequestException as e:
        print(f"API isteği hatası: {e}")
        if hasattr(e.response, 'text'):
            print(f"API Response: {e.response.text}")
    except json.JSONDecodeError as e:
        print(f"JSON parse hatası: {e}")
    except Exception as e:
        print(f"Beklenmeyen hata: {e}")
    
    # Bir sonraki istek için bekle
    time.sleep(2)

def scrape_selected_categories():
    # Güncel kategori slug'ları
    categories = [
        "su-icecek-ewknEvzsJc",
        "atistirmalik-BaaxwkyV1y",
        "meyve-sebze-VN2A9ap5Fm",
        "sut-urunleri-JGtfnNALTJ",
        "firindan-q357eEdgBs",
        "dondurma-Aw6YFhRWBI",
        "temel-gida-IQH9bir3bX",
        "kahvalti-iat0l1yrkf",
        "yiyecek-0VLJmBhnI3",
        "et-tavuk-balik-P1593VdPBd",
        "fit-form-A9ciT987qU",
        "kisisel-bakim-A21PNmddpt",
        "ev-bakim-JXy6KcrPKW",
        "ev-yasam-jdRnndEpyl",
        "evcil-hayvan-T27vt8aM7c",
        "bebek-T71m4N3D3K",
        "cinsel-saglik-viPc8mv9zd"
    ]
    
    for category in categories:
        scrape_category(category)

if __name__ == "__main__":
    scrape_selected_categories() 
