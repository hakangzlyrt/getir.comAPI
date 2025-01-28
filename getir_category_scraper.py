import requests
import json
from datetime import datetime
import time

def scrape_category(category_slug):
    # API URL
    url = f"https://getir.com/_next/data/getir-web-mainnet/tr/kategori/{category_slug}.json"
    
    # Headers
    headers = {
        "accept": "*/*",
        "accept-language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7",
        "cache-control": "no-cache",
        "pragma": "no-cache",
        "sec-ch-ua": "\"Not A(Brand\";v=\"8\", \"Chromium\";v=\"132\", \"Google Chrome\";v=\"132\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36"
    }
    
    try:
        # API'ye istek at
        print(f"\nKategori çekiliyor: {category_slug}")
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        # JSON verisini al
        data = response.json()
        
        # Sonuçları kaydet
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'getir_category_{category_slug}_{timestamp}.json'
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
            
        print(f"Veriler başarıyla {filename} dosyasına kaydedildi.")
        
        # Ürün sayısını göster
        if 'pageProps' in data and 'category' in data['pageProps']:
            category_data = data['pageProps']['category']
            product_count = category_data.get('productCount', 0)
            print(f"Kategori: {category_data.get('name', '')} - Toplam {product_count} ürün")
            
            # Alt kategorileri göster
            subcategories = category_data.get('subCategories', [])
            if subcategories:
                print("\nAlt kategoriler:")
                for sub in subcategories:
                    print(f"- {sub.get('name', '')}: {sub.get('productCount', 0)} ürün")
        
    except requests.exceptions.RequestException as e:
        print(f"API isteği hatası: {e}")
    except json.JSONDecodeError as e:
        print(f"JSON parse hatası: {e}")
    except Exception as e:
        print(f"Beklenmeyen hata: {e}")
    
    # Bir sonraki istek için bekle
    time.sleep(2)

def scrape_all_categories():
    categories = [
        "su-icecek-ewknEvzsJc",
        "temel-gida-IQH9bir3bX",
        "meyve-sebze-H3dt5DZqIp",
        "atistirmalik-r8tu6sxrYX",
        "dondurma-0KD7KsPVX3",
        "sut-kahvaltilik-1m3K6kqHGG",
        "fit-form-3dP6KUuGBw",
        "kisisel-bakim-2bqH8TOggL",
        "ev-bakim-gk3dp3UBIe",
        "ev-yasam-gBj11yFY8n",
        "teknoloji-jvvR3u4LjG",
        "bebek-3Lt1XTXP4F",
        "cinsel-saglik-2ZJKbVXy4y",
        "evcil-hayvan-QWMtjGKUHe"
    ]
    
    for category in categories:
        scrape_category(category)

if __name__ == "__main__":
    scrape_all_categories() 