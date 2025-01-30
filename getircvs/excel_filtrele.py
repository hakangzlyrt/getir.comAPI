import pandas as pd
import openpyxl
from openpyxl.worksheet.filters import FilterColumn, CustomFilter, CustomFilters

def excel_filtre_olustur():
    # Orijinal Excel'i oku
    df = pd.read_excel('tum_urunler_fiyatlar.xlsx')
    
    # Yeni bir Excel dosyası oluştur
    output_file = 'filtrelenebilir_urunler.xlsx'
    df.to_excel(output_file, index=False)
    
    # Excel dosyasını openpyxl ile aç
    wb = openpyxl.load_workbook(output_file)
    ws = wb.active
    
    # Başlık satırını dondur ve filtreleri ekle
    ws.freeze_panes = 'A2'
    ws.auto_filter.ref = ws.dimensions
    
    # Dosyayı kaydet
    wb.save(output_file)
    
    print(f"""
Filtrelenebilir Excel dosyası oluşturuldu: {output_file}

Excel'de filtreleme yapmak için:
1. Oluşturulan '{output_file}' dosyasını açın
2. 'urun_adi' kolonunun yanındaki filtre butonuna tıklayın
3. Arama kutusuna istediğiniz ürünü yazın (örn: 'bulgur')
4. Sonuçları görmek için Tamam'a tıklayın

Not: Excel'de filtreleme yaparken büyük-küçük harf duyarlılığı yoktur.
    """)

if __name__ == "__main__":
    excel_filtre_olustur() 