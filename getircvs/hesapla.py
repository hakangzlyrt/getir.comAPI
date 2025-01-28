import pandas as pd

# CSV dosyasını oku
df = pd.read_csv('getir_tum_urunler.csv')

# Ürün adına göre grupla ve en düşük fiyatları hesapla
results = []

# Ürünleri tanımla
keywords = {
    # Tahıllar ve Bakliyat
    'bulgur': 'Bulgur',
    'pirinç': 'Pirinç',
    'makarna': 'Makarna',
    'nohut': 'Nohut',
    'kırmızı mercimek': 'Kırmızı Mercimek',
    'yeşil mercimek': 'Yeşil Mercimek',
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

# Her ürün için en düşük fiyat hesapla
for keyword, display_name in keywords.items():
    # İlgili ürünleri filtrele
    mask = df['urun_adi'].str.lower().str.contains(keyword, na=False)
    filtered_products = df[mask]
    
    if not filtered_products.empty:
        min_price = filtered_products['fiyat'].min()
        min_price_product = filtered_products.loc[filtered_products['fiyat'] == min_price, 'urun_adi'].iloc[0]
        
        # Sonuçları listeye ekle
        results.append({
            'Ürün': display_name,
            'En Düşük Fiyat': round(min_price, 2),
            'Ürün Adı': min_price_product
        })

# Sonuçları DataFrame'e çevir ve fiyata göre sırala
results_df = pd.DataFrame(results)
results_df = results_df.sort_values('En Düşük Fiyat')

# CSV dosyasına kaydet
results_df.to_csv('ortalama_fiyatlar.csv', index=False, encoding='utf-8')
print("En düşük fiyatlar 'ortalama_fiyatlar.csv' dosyasına kaydedildi.") 