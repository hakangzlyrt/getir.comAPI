import pandas as pd
import json
import os
import re

def temizle_birim_fiyat(fiyat_str):
    if pd.isna(fiyat_str):
        return None
    # Sayı ve birim kısmını ayır (örn: "₺12,80/kg" -> 12.80)
    sayi = re.search(r'₺?([\d.,]+)', fiyat_str)
    if sayi:
        # Noktaları kaldır ve virgülü noktaya çevir
        return float(sayi.group(1).replace('.', '').replace(',', '.'))
    return None

def temizle_miktar(miktar_str):
    if pd.isna(miktar_str):
        return None
    # Sayı kısmını al (örn: "500 g" -> 500)
    sayi = re.search(r'([\d.,]+)', str(miktar_str))
    if sayi:
        # Noktaları kaldır ve virgülü noktaya çevir
        return float(sayi.group(1).replace('.', '').replace(',', '.'))
    return None

def temizle_fiyat(fiyat):
    if isinstance(fiyat, (int, float)):
        return float(fiyat)
    if isinstance(fiyat, str):
        # Noktaları kaldır ve virgülü noktaya çevir
        return float(fiyat.replace('.', '').replace(',', '.'))
    return 0.0

def json_to_excel():
    # Tüm ürünleri saklayacak liste
    tum_urunler = []
    
    # JSON dosyalarının bulunduğu dizin
    json_dir = '../getircategory'
    
    print("JSON dosyaları okunuyor...")
    # Tüm JSON dosyalarını oku
    for json_file in os.listdir(json_dir):
        if json_file.endswith('.json'):
            print(f"\nDosya okunuyor: {json_file}")
            with open(os.path.join(json_dir, json_file), 'r', encoding='utf-8') as f:
                try:
                    data = json.load(f)
                    
                    # Alt kategorilerdeki ürünleri al
                    if 'data' in data and 'category' in data['data']:
                        category = data['data']['category']
                        if 'subCategories' in category:
                            for sub_category in category['subCategories']:
                                if 'products' in sub_category:
                                    print(f"- {sub_category['name']} kategorisinde {len(sub_category['products'])} ürün bulundu")
                                    
                                    # Her üründen gerekli bilgileri al
                                    for product in sub_category['products']:
                                        birim_fiyat = product.get('unitPriceText', '').replace('(', '').replace(')', '')
                                        miktar = product.get('shortDescription', '')
                                        
                                        urun = {
                                            'Ürün Adı': product.get('name', ''),
                                            'Fiyat (TL)': temizle_fiyat(product.get('price', 0)),
                                            'Miktar (Metin)': miktar,
                                            'Miktar (Sayı)': temizle_miktar(miktar),
                                            'Birim Fiyat (Metin)': birim_fiyat,
                                            'Birim Fiyat (Sayı)': temizle_birim_fiyat(birim_fiyat),
                                            'Kategori': category.get('name', ''),
                                            'Alt Kategori': sub_category.get('name', '')
                                        }
                                        tum_urunler.append(urun)
                except Exception as e:
                    print(f"Hata: {json_file} dosyası okunurken hata oluştu - {str(e)}")
    
    if not tum_urunler:
        print("\nHiç ürün bulunamadı!")
        return
    
    print(f"\nToplam {len(tum_urunler)} ürün bulundu.")
    
    # DataFrame oluştur
    df = pd.DataFrame(tum_urunler)
    
    # Excel dosyasını oluştur
    output_file = 'getir_tum_urunler_yeni.xlsx'
    
    # Excel yazıcı oluştur
    writer = pd.ExcelWriter(output_file, engine='xlsxwriter')
    
    # DataFrame'i Excel'e yaz
    df.to_excel(writer, sheet_name='Ürünler', index=False)
    
    # Excel çalışma kitabını al
    workbook = writer.book
    worksheet = writer.sheets['Ürünler']
    
    # Başlık formatı
    header_format = workbook.add_format({
        'bold': True,
        'text_wrap': True,
        'valign': 'top',
        'bg_color': '#D9D9D9',
        'border': 1
    })
    
    # Sayı formatı
    number_format = workbook.add_format({'num_format': '#,##0.00'})
    
    # Kolon genişliklerini ve formatları ayarla
    worksheet.set_column('A:A', 40)  # Ürün Adı
    worksheet.set_column('B:B', 12, number_format)  # Fiyat
    worksheet.set_column('C:C', 15)  # Miktar (Metin)
    worksheet.set_column('D:D', 12, number_format)  # Miktar (Sayı)
    worksheet.set_column('E:E', 20)  # Birim Fiyat (Metin)
    worksheet.set_column('F:F', 12, number_format)  # Birim Fiyat (Sayı)
    worksheet.set_column('G:G', 20)  # Kategori
    worksheet.set_column('H:H', 20)  # Alt Kategori
    
    # Başlıkları formatla
    for col_num, value in enumerate(df.columns.values):
        worksheet.write(0, col_num, value, header_format)
    
    # Otomatik filtre ekle
    if len(df) > 0:
        worksheet.autofilter(0, 0, len(df), len(df.columns) - 1)
    
    # İlk satırı dondur
    worksheet.freeze_panes(1, 0)
    
    # Excel dosyasını kaydet
    writer.close()
    
    print(f"\nExcel dosyası oluşturuldu: {output_file}")
    print("""
Excel'de filtreleme ve sıralama yapmak için:
1. Herhangi bir kolonun yanındaki filtre butonuna (▼) tıklayın
2. İstediğiniz filtreleme seçeneğini kullanın:
   - Metin filtreleri için: İçerir, Eşittir, İle Başlar, vb.
   - Sayı filtreleri için: Büyüktür, Küçüktür, İki Değer Arası, vb.
3. Sayısal kolonları (Fiyat, Miktar, Birim Fiyat) büyükten küçüğe veya küçükten büyüğe sıralayabilirsiniz
4. Filtreyi kaldırmak için 'Tümü' seçeneğini seçin
""")

if __name__ == "__main__":
    json_to_excel() 