import pandas as pd
import json
import os
from difflib import get_close_matches

# Getir kategori ID'leri ve isimleri
CATEGORY_NAMES = {
    "551430043427d5010a3a5c5e": "Fırından",
    "551430043427d5010a3a5c5d": "Et & Tavuk & Balık",
    "551430043427d5010a3a5c5c": "Süt & Kahvaltı",
    "551430043427d5010a3a5c5b": "Meyve & Sebze",
    "55449fdf02632e11003c2da8": "Ev Bakım & Temizlik",
    "566eeb85f9facb0f00b1cb16": "Atıştırmalık",
    "623d6d7b046e00290ff7f861": "İçecek",
    "641170494299463fa9f5e562": "Temel Gıda",
    "6220aade4b7e8f42a3100532": "Kişisel Bakım",
    "654a33f6697c2c3099cd34df": "Bebek",
    "6555c3d2ffdcd3491c581aef": "Ev & Yaşam",
    "67092adedc6a804471d91a8a": "Teknoloji",
    "678134182edbe1bcf90375c0": "Evcil Hayvan"
}

def find_closest_match(product_name, product_list):
    # Büyük-küçük harf duyarlılığını kaldır
    product_name = product_name.lower()
    product_list_lower = [p.lower() for p in product_list]
    
    # En yakın eşleşmeyi bul
    matches = get_close_matches(product_name, product_list_lower, n=1, cutoff=0.6)
    if matches:
        # Orijinal büyük-küçük harfli versiyonu bul
        index = product_list_lower.index(matches[0])
        return product_list[index]
    return None

def load_category_data():
    category_mapping = {}
    product_names = []  # Tüm ürün isimlerini sakla
    product_categories = {}  # Ürün ismi -> kategori ID eşleştirmesi
    category_dir = '../getircategory'
    
    print("Kategori dosyaları okunuyor...")
    # Tüm kategori JSON dosyalarını oku
    for file in os.listdir(category_dir):
        if file.endswith('.json'):
            print(f"Dosya okunuyor: {file}")
            with open(os.path.join(category_dir, file), 'r', encoding='utf-8') as f:
                data = json.load(f)
                items = data.get('data', {}).get('items', [])
                print(f"- {len(items)} ürün bulundu")
                # Her ürün için kategori bilgilerini topla
                for item in items:
                    if 'categoryIds' in item:
                        product_name = item.get('name', '')
                        categories = item.get('categoryIds', [])
                        if product_name and categories:
                            product_names.append(product_name)
                            product_categories[product_name] = categories[0]
    
    print(f"\nToplam {len(product_names)} referans ürün bulundu")
    
    def find_category(name):
        closest = find_closest_match(name, product_names)
        if closest:
            return product_categories[closest]
        return None
    
    return find_category

def categorize_products():
    # Excel dosyasını oku
    print("\nExcel dosyası okunuyor...")
    df = pd.read_excel('tum_urunler_fiyatlar.xlsx')
    print(f"Excel'de {len(df)} ürün bulundu")
    
    # İlk birkaç ürünü göster
    print("\nİlk 5 ürün:")
    for _, row in df.head().iterrows():
        print(f"- {row['urun_adi']}")
    
    # Kategori eşleştirme fonksiyonunu al
    category_finder = load_category_data()
    
    print("\nKategoriler eşleştiriliyor...")
    # Yeni kategori kolonu ekle
    df['getir_kategori_id'] = df['urun_adi'].apply(category_finder)
    
    # Kategori isimlerini ekle
    df['getir_kategori'] = df['getir_kategori_id'].map(CATEGORY_NAMES)
    
    # Sonuçları yeni bir Excel dosyasına kaydet
    output_file = 'urunler_kategorili_yeni.xlsx'
    df.to_excel(output_file, index=False)
    print(f"\nKategorileme tamamlandı. Sonuçlar '{output_file}' dosyasına kaydedildi.")
    
    # Kategori bazında ürün sayılarını göster
    print("\nKategori bazında ürün sayıları:")
    category_counts = df['getir_kategori'].value_counts()
    for category, count in category_counts.items():
        if pd.notna(category):  # NaN değerleri gösterme
            print(f"{category}: {count} ürün")
    
    # Kategorize edilemeyen ürün sayısı
    uncategorized = df['getir_kategori'].isna().sum()
    if uncategorized > 0:
        print(f"\nKategorize edilemeyen ürün sayısı: {uncategorized}")
        print("\nKategorize edilemeyen ilk 5 ürün örneği:")
        uncategorized_examples = df[df['getir_kategori'].isna()]['urun_adi'].head()
        for product in uncategorized_examples:
            print(f"- {product}")

if __name__ == "__main__":
    categorize_products() 
import pandas as pd
import json
import os
from difflib import get_close_matches

# Getir kategori ID'leri ve isimleri
CATEGORY_NAMES = {
    "551430043427d5010a3a5c5e": "Fırından",
    "551430043427d5010a3a5c5d": "Et & Tavuk & Balık",
    "551430043427d5010a3a5c5c": "Süt & Kahvaltı",
    "551430043427d5010a3a5c5b": "Meyve & Sebze",
    "55449fdf02632e11003c2da8": "Ev Bakım & Temizlik",
    "566eeb85f9facb0f00b1cb16": "Atıştırmalık",
    "623d6d7b046e00290ff7f861": "İçecek",
    "641170494299463fa9f5e562": "Temel Gıda",
    "6220aade4b7e8f42a3100532": "Kişisel Bakım",
    "654a33f6697c2c3099cd34df": "Bebek",
    "6555c3d2ffdcd3491c581aef": "Ev & Yaşam",
    "67092adedc6a804471d91a8a": "Teknoloji",
    "678134182edbe1bcf90375c0": "Evcil Hayvan"
}

def find_closest_match(product_name, product_list):
    # Büyük-küçük harf duyarlılığını kaldır
    product_name = product_name.lower()
    product_list_lower = [p.lower() for p in product_list]
    
    # En yakın eşleşmeyi bul
    matches = get_close_matches(product_name, product_list_lower, n=1, cutoff=0.6)
    if matches:
        # Orijinal büyük-küçük harfli versiyonu bul
        index = product_list_lower.index(matches[0])
        return product_list[index]
    return None

def load_category_data():
    category_mapping = {}
    product_names = []  # Tüm ürün isimlerini sakla
    product_categories = {}  # Ürün ismi -> kategori ID eşleştirmesi
    category_dir = '../getircategory'
    
    # Tüm kategori JSON dosyalarını oku
    for file in os.listdir(category_dir):
        if file.endswith('.json'):
            with open(os.path.join(category_dir, file), 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Her ürün için kategori bilgilerini topla
                for item in data.get('data', {}).get('items', []):
                    if 'categoryIds' in item:
                        product_name = item.get('name', '')
                        categories = item.get('categoryIds', [])
                        if product_name and categories:
                            product_names.append(product_name)
                            product_categories[product_name] = categories[0]
    
    def find_category(name):
        closest = find_closest_match(name, product_names)
        if closest:
            return product_categories[closest]
        return None
    
    return find_category

def categorize_products():
    # Excel dosyasını oku
    df = pd.read_excel('tum_urunler_fiyatlar.xlsx')
    
    # Kategori eşleştirme fonksiyonunu al
    category_finder = load_category_data()
    
    # Yeni kategori kolonu ekle
    df['getir_kategori_id'] = df['urun_adi'].apply(category_finder)
    
    # Kategori isimlerini ekle
    df['getir_kategori'] = df['getir_kategori_id'].map(CATEGORY_NAMES)
    
    # Sonuçları yeni bir Excel dosyasına kaydet
    output_file = 'urunler_kategorili_yeni.xlsx'
    df.to_excel(output_file, index=False)
    print(f"Kategorileme tamamlandı. Sonuçlar '{output_file}' dosyasına kaydedildi.")
    
    # Kategori bazında ürün sayılarını göster
    print("\nKategori bazında ürün sayıları:")
    category_counts = df['getir_kategori'].value_counts()
    for category, count in category_counts.items():
        if pd.notna(category):  # NaN değerleri gösterme
            print(f"{category}: {count} ürün")
    
    # Kategorize edilemeyen ürün sayısı
    uncategorized = df['getir_kategori'].isna().sum()
    if uncategorized > 0:
        print(f"\nKategorize edilemeyen ürün sayısı: {uncategorized}")

if __name__ == "__main__":
    categorize_products() 