import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

def parse_getir():
    # Getir URL
    url = "https://getir.com/kategori/temel-gida"
    
    # Tarayıcıdan aldığımız headers
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7",
        "cache-control": "max-age=0",
        "sec-ch-ua": "\"Not A(Brand\";v=\"8\", \"Chromium\";v=\"132\", \"Google Chrome\";v=\"132\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36"
    }
    
    try:
        # İsteği yap
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        # HTML'i parse et
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Ürünleri bul
        products = []
        product_cards = soup.select('[data-testid="product-card"]')
        
        for card in product_cards:
            try:
                name = card.select_one('[data-testid="product-name"]').text.strip()
                price = card.select_one('[data-testid="product-price"]').text.strip()
                image = card.select_one('img')['src']
                
                products.append({
                    "name": name,
                    "price": price,
                    "image": image
                })
                print(f"Ürün eklendi: {name} - {price}")
            except Exception as e:
                print(f"Ürün bilgisi alınamadı: {e}")
        
        # Sonuçları kaydet
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'getir_products_{timestamp}.json'
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(products, f, ensure_ascii=False, indent=4)
            
        print(f"Veriler başarıyla {filename} dosyasına kaydedildi.")
        print(f"Toplam {len(products)} ürün bulundu.")
        
    except requests.exceptions.RequestException as e:
        print(f"Hata oluştu: {e}")
    except Exception as e:
        print(f"Beklenmeyen hata: {e}")

if __name__ == "__main__":
    parse_getir() 