from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import json
from datetime import datetime
import time

def scrape_getir():
    # Chrome ayarlarını yapılandır
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Tarayıcıyı arka planda çalıştır
    
    # Chrome driver'ı başlat
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    try:
        # Getir ana sayfasına git
        driver.get("https://getir.com/kategori/temel-gida")
        
        # Sayfanın yüklenmesini bekle
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='product-card']")))
        
        # Ürünleri topla
        products = []
        product_cards = driver.find_elements(By.CSS_SELECTOR, "[data-testid='product-card']")
        
        for card in product_cards:
            try:
                name = card.find_element(By.CSS_SELECTOR, "[data-testid='product-name']").text
                price = card.find_element(By.CSS_SELECTOR, "[data-testid='product-price']").text
                image = card.find_element(By.CSS_SELECTOR, "img").get_attribute("src")
                
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
        
    except Exception as e:
        print(f"Hata oluştu: {e}")
    
    finally:
        driver.quit()

if __name__ == "__main__":
    scrape_getir() 