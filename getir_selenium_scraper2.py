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
    # chrome_options.add_argument("--headless")  # Tarayıcıyı arka planda çalıştır
    
    # Chrome driver'ı başlat
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.maximize_window()  # Pencereyi tam ekran yap
    
    try:
        # Getir ana sayfasına git
        driver.get("https://getir.com/kategori/temel-gida")
        
        # Sayfanın yüklenmesini bekle
        wait = WebDriverWait(driver, 20)
        
        # Konum seçim modalını bekle ve kapat (varsa)
        try:
            location_modal = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='location-modal']")))
            close_button = location_modal.find_element(By.CSS_SELECTOR, "button")
            close_button.click()
            time.sleep(2)
        except:
            print("Konum modalı bulunamadı, devam ediliyor...")
        
        # Ürün kartlarının yüklenmesini bekle
        product_cards = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "[data-testid='product-card']")))
        
        # Sayfayı aşağı kaydır ve tüm ürünlerin yüklenmesini bekle
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
        
        # Tüm ürün kartlarını topla
        product_cards = driver.find_elements(By.CSS_SELECTOR, "[data-testid='product-card']")
        products = []
        
        for card in product_cards:
            try:
                name = card.find_element(By.CSS_SELECTOR, "[data-testid='product-name']").text
                price = card.find_element(By.CSS_SELECTOR, "[data-testid='product-price']").text
                image = card.find_element(By.CSS_SELECTOR, "img").get_attribute("src")
                
                products.append({
                    "name": name,
                    "price": price.replace("₺", "").strip(),
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
            
        print(f"\nVeriler başarıyla {filename} dosyasına kaydedildi.")
        print(f"Toplam {len(products)} ürün bulundu.")
        
    except Exception as e:
        print(f"Hata oluştu: {e}")
    
    finally:
        driver.quit()

if __name__ == "__main__":
    scrape_getir() 