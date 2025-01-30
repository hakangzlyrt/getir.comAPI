import pandas as pd
import re
import json
import os

def extract_gram_from_description(text):
    if pd.isna(text):
        return None
    text = str(text).lower()
    match = re.search(r'(\d+)\s*(gr|g|gram|kg|ml|lt|l)', text)
    if match:
        amount = float(match.group(1))
        unit = match.group(2)
        # Birimi grama çevir
        if unit in ['kg', 'lt', 'l']:
            amount *= 1000
        return amount
    return None

# JSON dosyalarından ürün bilgilerini al
product_grams = {}
json_dir = '../getircategory'
for json_file in os.listdir(json_dir):
    if json_file.endswith('.json'):
        with open(os.path.join(json_dir, json_file), 'r', encoding='utf-8') as f:
            data = json.load(f)
            if 'data' in data and 'category' in data['data'] and 'subCategories' in data['data']['category']:
                for subcat in data['data']['category']['subCategories']:
                    if 'products' in subcat:
                        for product in subcat['products']:
                            if 'name' in product and 'shortDescription' in product:
                                gram = extract_gram_from_description(product['shortDescription'])
                                if gram:
                                    product_grams[product['name']] = gram

def extract_gram(text, miktar, birim):
    # Önce JSON'dan kontrol et
    if text in product_grams:
        return product_grams[text]
    
    # Sonra miktar sütunundan kontrol et
    if not pd.isna(miktar):
        try:
            miktar = float(miktar)
            # Birim 'kg' ise 1000 ile çarp
            if not pd.isna(birim) and 'kg' in str(birim).lower():
                miktar *= 1000
            return miktar
        except:
            pass
    
    # Son olarak ürün adından kontrol et
    if not pd.isna(text):
        text = str(text).lower()
        match = re.search(r'(\d+)\s*(gr|g|gram|kg|ml|lt|l)', text)
        if match:
            amount = float(match.group(1))
            unit = match.group(2)
            # Birimi grama çevir
            if unit in ['kg', 'lt', 'l']:
                amount *= 1000
            return amount
    
    return None

# CSV dosyasını oku
df = pd.read_csv('getir_tum_urunler.csv')

# Gram bilgisini ekle
df['gram'] = df.apply(lambda x: extract_gram(x['urun_adi'], x['miktar'], x['birim']), axis=1)

# KG fiyatını hesapla
df['kg_price'] = None
mask_with_gram = df['gram'].notna()
df.loc[mask_with_gram, 'kg_price'] = df.loc[mask_with_gram, 'fiyat'] * 1000 / df.loc[mask_with_gram, 'gram']

# Tüm ürünleri Excel'e kaydet (her kategori ayrı sheet olacak)
with pd.ExcelWriter('tum_urunler_fiyatlar.xlsx', engine='openpyxl') as writer:
    # Ana sayfa - tüm ürünler fiyata göre sıralı
    df_sorted = df.sort_values('fiyat')
    df_sorted = df_sorted[['kategori', 'alt_kategori', 'urun_adi', 'fiyat', 'gram', 'kg_price', 'birim', 'miktar']]
    df_sorted.to_excel(writer, sheet_name='Tüm Ürünler', index=False)
    
    # Her kategori için ayrı sayfa
    for kategori in df['kategori'].unique():
        df_kategori = df[df['kategori'] == kategori].copy()
        df_kategori = df_kategori.sort_values('fiyat')
        df_kategori = df_kategori[['kategori', 'alt_kategori', 'urun_adi', 'fiyat', 'gram', 'kg_price', 'birim', 'miktar']]
        sheet_name = kategori[:31].replace('/', '_')  # Excel sheet adı max 31 karakter olabilir ve / içeremez
        df_kategori.to_excel(writer, sheet_name=sheet_name, index=False)

print("Tüm ürünler ve fiyatları 'tum_urunler_fiyatlar.xlsx' dosyasına kaydedildi.") 