import requests
import json
from datetime import datetime

def scrape_getir():
    # Getir URL
    url = "https://getir.com/kategori/"
    
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
        response.raise_for_status()  # Hata kontrolü
        
        print(f"Durum Kodu: {response.status_code}")
        print("Headers:", response.headers)
        
        # HTML içeriğini kaydet
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        html_filename = f'getir_page_{timestamp}.html'
        
        with open(html_filename, 'w', encoding='utf-8') as f:
            f.write(response.text)
            
        print(f"HTML içeriği {html_filename} dosyasına kaydedildi.")
        
        # JSON verisi varsa onu da kaydet
        try:
            json_data = response.json()
            json_filename = f'getir_data_{timestamp}.json'
            
            with open(json_filename, 'w', encoding='utf-8') as f:
                json.dump(json_data, f, ensure_ascii=False, indent=4)
                
            print(f"JSON verisi {json_filename} dosyasına kaydedildi.")
        except:
            print("JSON verisi bulunamadı.")
            
    except requests.exceptions.RequestException as e:
        print(f"Hata oluştu: {e}")
    except Exception as e:
        print(f"Beklenmeyen hata: {e}")

if __name__ == "__main__":
    scrape_getir() 