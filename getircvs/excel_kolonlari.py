import pandas as pd

# Excel dosyasını oku
df = pd.read_excel('tum_urunler_fiyatlar.xlsx')

# Kolonları yazdır
print("Excel dosyasındaki kolonlar:")
for col in df.columns:
    print(f"- {col}")

# İlk birkaç satırı göster
print("\nİlk 3 satır:")
print(df.head(3)) 