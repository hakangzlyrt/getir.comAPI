import requests
import json
from datetime import datetime

def get_getir_data():
    # Getir API endpoint'i
    url = "https://api.getir.com/v2/catalog/categories"
    
    # Tarayıcı gibi görünmek için headers
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'application/json',
        'Accept-Language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7',
        'Origin': 'https://getir.com',
        'Referer': 'https://getir.com/'
    }
    
    try:
        # API'ye istek at
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        # JSON verisini al
        data = response.json()
        
        # Sonuçları kaydet
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'getir_data_{timestamp}.json'
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
            
        print(f"Veriler başarıyla {filename} dosyasına kaydedildi.")
        
    except requests.exceptions.RequestException as e:
        print(f"Hata oluştu: {e}")
    except json.JSONDecodeError as e:
        print(f"JSON parse hatası: {e}")
    except Exception as e:
        print(f"Beklenmeyen hata: {e}")

if __name__ == "__main__":
    get_getir_data() 