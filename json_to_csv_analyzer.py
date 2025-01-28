import json
import csv
import glob
import statistics

def process_category_json(json_file):
    products = []
    
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        if 'data' in data and 'category' in data['data']:
            category_data = data['data']['category']
            category_name = category_data.get('name', '')
            
            # Alt kategorileri işle
            for subcategory in category_data.get('subCategories', []):
                subcategory_name = subcategory.get('name', '')
                
                # Alt kategorideki ürünleri işle
                for product in subcategory.get('products', []):
                    products.append({
                        'kategori': category_name,
                        'alt_kategori': subcategory_name,
                        'urun_adi': product.get('name', ''),
                        'fiyat': float(product.get('price', 0)),
                        'birim': product.get('unit', ''),
                        'miktar': product.get('quantity', '')
                    })
    
    except Exception as e:
        print(f"Hata: {json_file} dosyası işlenirken hata oluştu - {e}")
    
    return products

def analyze_prices(products):
    # Kategori bazında fiyat analizi
    category_prices = {}
    subcategory_prices = {}
    
    for product in products:
        category = product['kategori']
        subcategory = product['alt_kategori']
        price = product['fiyat']
        
        # Kategori fiyatlarını topla
        if category not in category_prices:
            category_prices[category] = []
        category_prices[category].append(price)
        
        # Alt kategori fiyatlarını topla
        key = f"{category} - {subcategory}"
        if key not in subcategory_prices:
            subcategory_prices[key] = []
        subcategory_prices[key].append(price)
    
    # Sonuçları yazdır
    print("\nKategori Bazında Ortalama Fiyatlar:")
    print("-" * 50)
    for category, prices in category_prices.items():
        avg_price = statistics.mean(prices)
        min_price = min(prices)
        max_price = max(prices)
        print(f"\n{category}:")
        print(f"Ortalama Fiyat: {avg_price:.2f} TL")
        print(f"En Düşük Fiyat: {min_price:.2f} TL")
        print(f"En Yüksek Fiyat: {max_price:.2f} TL")
        print(f"Ürün Sayısı: {len(prices)}")
    
    print("\n\nAlt Kategori Bazında Ortalama Fiyatlar:")
    print("-" * 50)
    for key, prices in subcategory_prices.items():
        avg_price = statistics.mean(prices)
        min_price = min(prices)
        max_price = max(prices)
        print(f"\n{key}:")
        print(f"Ortalama Fiyat: {avg_price:.2f} TL")
        print(f"En Düşük Fiyat: {min_price:.2f} TL")
        print(f"En Yüksek Fiyat: {max_price:.2f} TL")
        print(f"Ürün Sayısı: {len(prices)}")

def save_to_csv(products, output_file):
    if products:
        # CSV dosyasına yaz
        with open(output_file, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=products[0].keys())
            writer.writeheader()
            writer.writerows(products)
        print(f"\nVeriler {output_file} dosyasına kaydedildi.")

def main():
    # Tüm JSON dosyalarını bul
    json_files = glob.glob('getir_*.json')
    
    all_products = []
    
    # Her JSON dosyasını işle
    for json_file in json_files:
        products = process_category_json(json_file)
        all_products.extend(products)
    
    # CSV'ye kaydet
    save_to_csv(all_products, 'getir_tum_urunler.csv')
    
    # Fiyat analizi yap
    analyze_prices(all_products)

if __name__ == "__main__":
    main() 