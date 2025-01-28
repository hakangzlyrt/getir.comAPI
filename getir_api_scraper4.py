import requests
import json
import time

def scrape_category(category_slug, category_name):
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
        print(f"\nKategori çekiliyor: {category_name}")
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        
        # JSON verisini al
        data = response.json()
        
        # Sonuçları kaydet
        filename = f'getir_{category_name}.json'
        
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

def scrape_all_categories():
    # Kategori slug'ları ve isimleri
    categories = [
        ("su-icecek-ewknEvzsJc", "suicecek"),
        ("atistirmalik-BaaxwkyV1y", "atistirmalik"),
        ("meyve-sebze-VN2A9ap5Fm", "meyvesebze"),
        ("sut-urunleri-JGtfnNALTJ", "suturunleri"),
        ("firindan-q357eEdgBs", "firindan"),
        ("dondurma-Aw6YFhRWBI", "dondurma"),
        ("temel-gida-IQH9bir3bX", "temelgida"),
        ("kahvalti-iat0l1yrkf", "kahvalti"),
        ("yiyecek-0VLJmBhnI3", "yiyecek"),
        ("et-tavuk-balik-P1593VdPBd", "ettavukbalik"),
        ("fit-form-A9ciT987qU", "fitform"),
        ("kisisel-bakim-A21PNmddpt", "kisiselbakim"),
        ("ev-bakim-JXy6KcrPKW", "evbakim"),
        ("ev-yasam-jdRnndEpyl", "evyasam"),
        ("evcil-hayvan-T27vt8aM7c", "evcilhayvan"),
        ("bebek-T71m4N3D3K", "bebek"),
        ("cinsel-saglik-viPc8mv9zd", "cinselsaglik")
    ]
    
    for category_slug, category_name in categories:
        scrape_category(category_slug, category_name)

if __name__ == "__main__":
    scrape_all_categories() 