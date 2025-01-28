import json
import glob
from datetime import datetime

def process_getir_data():
    # Tüm JSON dosyalarını bul
    json_files = glob.glob('getir_products_*_*.json')
    
    all_products = []
    
    for file_path in json_files:
        try:
            print(f"\nDosya işleniyor: {file_path}")
            
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                print("JSON yapısı:", json.dumps(data, indent=2)[:500] + "...")  # İlk 500 karakteri göster
            
            # Veri yapısını kontrol et ve ürünleri çıkar
            products = []
            if isinstance(data, dict):
                if 'data' in data and 'products' in data['data']:
                    products = data['data']['products']
                elif 'products' in data:
                    products = data['products']
            elif isinstance(data, list):
                products = data
                
            category = file_path.split('_')[2] if len(file_path.split('_')) > 2 else 'unknown'
            
            for product in products:
                try:
                    # Ürün verilerini kontrol et ve çıkar
                    processed_product = {
                        "id": str(product.get('id', '')),
                        "name": str(product.get('name', '')),
                        "price": float(product.get('price', 0)),
                        "category": category,
                        "image": str(product.get('image', {}).get('url', '')) if isinstance(product.get('image'), dict) else str(product.get('image', '')),
                        "description": str(product.get('description', '')),
                        "unit": str(product.get('unit', '')),
                        "quantity": float(product.get('quantity', 0))
                    }
                    all_products.append(processed_product)
                    print(f"Ürün eklendi: {processed_product['name']}")
                    
                except Exception as e:
                    print(f"Ürün işleme hatası: {e}")
            
            print(f"{len(products)} ürün işlendi.")
            
        except Exception as e:
            print(f"Dosya işleme hatası ({file_path}): {e}")
    
    # İşlenmiş verileri kaydet
    if all_products:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = f'processed_getir_data_{timestamp}.json'
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(all_products, f, ensure_ascii=False, indent=4)
        
        print(f"\nToplam {len(all_products)} ürün işlendi ve {output_file} dosyasına kaydedildi.")
        
        # Örnek ürünleri göster
        print("\nÖrnek ürünler:")
        for product in all_products[:5]:
            print(f"- {product['name']}: {product['price']} TL ({product['category']})")
    else:
        print("\nHiç ürün bulunamadı!")

if __name__ == "__main__":
    process_getir_data() 