import pandas as pd

def analyze_average_prices():
    # CSV dosyasını oku
    df = pd.read_csv('getircvs/getir_tum_urunler.csv')
    
    # Ürün adına göre grupla ve ortalama fiyatları hesapla
    product_averages = {}
    
    # Özel ürünleri belirle ve ortalamalarını hesapla
    keywords = {
        # Tahıllar ve Bakliyat
        'bulgur': 'Bulgur',
        'pirinç': 'Pirinç',
        'makarna': 'Makarna',
        'nohut': 'Nohut',
        'mercimek': 'Mercimek',
        'fasulye': 'Fasulye',
        'börülce': 'Börülce',
        'barbunya': 'Barbunya',
        'mısır': 'Mısır',
        'kinoa': 'Kinoa',
        'yulaf': 'Yulaf',
        
        # Süt Ürünleri
        'süt': 'Süt',
        'yoğurt': 'Yoğurt',
        'peynir': 'Peynir',
        'ayran': 'Ayran',
        'kefir': 'Kefir',
        'kaymak': 'Kaymak',
        'tereyağ': 'Tereyağ',
        'lor': 'Lor Peyniri',
        
        # Ekmek ve Unlu Mamüller
        'ekmek': 'Ekmek',
        'un': 'Un',
        'galeta': 'Galeta',
        'kraker': 'Kraker',
        
        # Protein Kaynakları
        'yumurta': 'Yumurta',
        'tavuk': 'Tavuk',
        'et': 'Et',
        'balık': 'Balık',
        'hindi': 'Hindi',
        'somon': 'Somon',
        'ton': 'Ton Balığı',
        
        # Meyveler
        'elma': 'Elma',
        'armut': 'Armut',
        'muz': 'Muz',
        'portakal': 'Portakal',
        'mandalina': 'Mandalina',
        'kivi': 'Kivi',
        'çilek': 'Çilek',
        'üzüm': 'Üzüm',
        'şeftali': 'Şeftali',
        'kayısı': 'Kayısı',
        'kiraz': 'Kiraz',
        'erik': 'Erik',
        'incir': 'İncir',
        'nar': 'Nar',
        'kavun': 'Kavun',
        'karpuz': 'Karpuz',
        'avokado': 'Avokado',
        'hurma': 'Hurma',
        'limon': 'Limon',
        'greyfurt': 'Greyfurt',
        
        # Sebzeler
        'domates': 'Domates',
        'salatalık': 'Salatalık',
        'biber': 'Biber',
        'patlıcan': 'Patlıcan',
        'kabak': 'Kabak',
        'patates': 'Patates',
        'soğan': 'Soğan',
        'sarımsak': 'Sarımsak',
        'havuç': 'Havuç',
        'brokoli': 'Brokoli',
        'karnabahar': 'Karnabahar',
        'ıspanak': 'Ispanak',
        'marul': 'Marul',
        'lahana': 'Lahana',
        'pırasa': 'Pırasa',
        'kereviz': 'Kereviz',
        'turp': 'Turp',
        'enginar': 'Enginar',
        'bezelye': 'Bezelye',
        'bamya': 'Bamya',
        'semizotu': 'Semizotu',
        
        # Kuruyemişler
        'fındık': 'Fındık',
        'ceviz': 'Ceviz',
        'badem': 'Badem',
        'fıstık': 'Fıstık',
        'kaju': 'Kaju',
        'leblebi': 'Leblebi',
        'kestane': 'Kestane',
        
        # İçecekler
        'çay': 'Çay',
        'kahve': 'Kahve',
        'meyvesuyu': 'Meyve Suyu',
        'gazlı': 'Gazlı İçecek',
        'ayran': 'Ayran',
        'kola': 'Kola',
        'soda': 'Soda',
        'maden': 'Maden Suyu',
        
        # Temel Gıda
        'şeker': 'Şeker',
        'tuz': 'Tuz',
        'baharat': 'Baharat',
        'salça': 'Salça',
        'zeytin': 'Zeytin',
        'zeytinyağ': 'Zeytinyağı',
        'sıvıyağ': 'Sıvı Yağ',
        'sirke': 'Sirke',
        'sos': 'Sos',
        'konserve': 'Konserve',
        'reçel': 'Reçel',
        'bal': 'Bal',
        'pekmez': 'Pekmez',
        'tahin': 'Tahin',
        'helva': 'Helva'
    }
    
    print("\nÜrün Ortalama Fiyatları (TL/kg veya TL/L):")
    print("-" * 50)
    print(f"{'Ürün':<20} {'Ortalama Fiyat':<15} {'Ürün Sayısı':<10}")
    print("-" * 50)
    
    for keyword, display_name in keywords.items():
        # İlgili ürünleri filtrele
        mask = df['urun_adi'].str.lower().str.contains(keyword, na=False)
        filtered_products = df[mask]
        
        if not filtered_products.empty:
            avg_price = filtered_products['fiyat'].mean()
            count = len(filtered_products)
            print(f"{display_name:<20} {avg_price:>15.2f} {count:>10}")
            product_averages[display_name] = {'average': avg_price, 'count': count}

if __name__ == "__main__":
    analyze_average_prices() 