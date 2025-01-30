import pandas as pd

def urun_ara(arama_kelimesi):
    # Excel dosyasını oku
    df = pd.read_excel('tum_urunler_fiyatlar.xlsx')
    
    # Büyük-küçük harf duyarlılığını kaldır
    arama_kelimesi = arama_kelimesi.lower()
    
    # Ürün adında arama yap
    sonuclar = df[df['urun_adi'].str.lower().str.contains(arama_kelimesi, na=False)]
    
    if len(sonuclar) == 0:
        print(f"\n'{arama_kelimesi}' ile ilgili ürün bulunamadı.")
        return
    
    # Sonuçları göster
    print(f"\n'{arama_kelimesi}' araması için {len(sonuclar)} ürün bulundu:\n")
    for _, urun in sonuclar.iterrows():
        print(f"Ürün: {urun['urun_adi']}")
        print(f"Fiyat: {urun['fiyat']} TL")
        if pd.notna(urun.get('gram')):
            print(f"Gram: {urun['gram']}")
        if pd.notna(urun.get('kg_price')):
            print(f"Kg Fiyatı: {urun['kg_price']} TL")
        print("-" * 50)

if __name__ == "__main__":
    while True:
        arama = input("\nAramak istediğiniz ürünü yazın (çıkmak için 'q'): ")
        if arama.lower() == 'q':
            break
        urun_ara(arama) 