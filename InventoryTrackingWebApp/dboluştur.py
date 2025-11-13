import sqlite3

conn = sqlite3.connect("stok_takip.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS urunler (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    urun_adi TEXT NOT NULL,
    kategori TEXT NOT NULL,
    miktar INTEGER NOT NULL,
    fiyat REAL NOT NULL,
    ekleme_tarihi TEXT NOT NULL
)
""")

conn.commit()
conn.close()
print("Veritabanı ve tablo oluşturuldu!")
