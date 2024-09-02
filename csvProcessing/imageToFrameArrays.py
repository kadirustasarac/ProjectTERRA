import rasterio
import numpy as np
import psycopg2

# PostgreSQL veritabanı bilgileri
db_params = {
    'dbname': 'your_database',
    'user': 'your_username',
    'password': 'your_password',
    'host': 'localhost',  # Veritabanı sunucusu
    'port': '5432'        # PostgreSQL portu
}

# Her bir bandı temsil eden TIFF dosyalarının yolları
red_band_file = r'images/RED.TIF'
nir_band_file = r'images/NIR.TIF'  # Near-Infrared (NIR) band
green_band_file = r'images/GREEN.TIF'
reg_band_file = r'images/REG.TIF'  # Red Edge band

# NDVI hesaplama fonksiyonu
def calculate_ndvi(red_band, nir_band):
    ndvi = (nir_band.astype(float) - red_band.astype(float)) / ((nir_band + red_band) + 1e-10)
    ndvi = np.clip(ndvi, -1, 1)
    return ndvi

# PostgreSQL'e bağlantı kurma
def create_connection():
    try:
        conn = psycopg2.connect(**db_params)
        print("PostgreSQL bağlantısı başarılı")
        return conn
    except psycopg2.Error as e:
        print(f"Veritabanı bağlantı hatası: {e}")
        return None

# Tablo oluşturma fonksiyonu
def create_table(conn):
    try:
        cursor = conn.cursor()
        create_table_query = '''CREATE TABLE IF NOT EXISTS indices_results (
                                    id SERIAL PRIMARY KEY,
                                    file_name TEXT NOT NULL,
                                    mean_ndvi REAL,
                                    mean_vari REAL,
                                    mean_cwsi REAL
                                );'''
        cursor.execute(create_table_query)
        conn.commit()
        cursor.close()
    except psycopg2.Error as e:
        print(f"Tablo oluşturma hatası: {e}")

# Sonuçları veritabanına ekleme fonksiyonu
def insert_indices_result(conn, file_name, mean_ndvi):
    try:
        cursor = conn.cursor()
        insert_query = '''INSERT INTO indices_results (file_name, mean_ndvi)
                          VALUES (%s, %s);'''
        cursor.execute(insert_query, (file_name, mean_ndvi))
        conn.commit()
        cursor.close()
    except psycopg2.Error as e:
        print(f"Veritabanına ekleme hatası: {e}")

# Ana fonksiyon
def main():
    # PostgreSQL bağlantısı
    conn = create_connection()
    
    # Tablo oluştur
    if conn is not None:
        create_table(conn)
    
    # Her bandı ayrı dosyalardan oku
    with rasterio.open(red_band_file) as red_src, \
         rasterio.open(nir_band_file) as nir_src, \
         rasterio.open(green_band_file) as green_src, \
         rasterio.open(reg_band_file) as reg_src:
        
        red_band = red_src.read(1)
        nir_band = nir_src.read(1)
        green_band = green_src.read(1)
        reg_band = reg_src.read(1)
        
        # NDVI hesapla
        ndvi = calculate_ndvi(red_band, nir_band)
        
        # Ortalama NDVI değeri
        mean_ndvi = ndvi.mean()
        
        # Sonuçları veritabanına ekle
        if conn is not None:
            insert_indices_result(conn, nir_band_file, mean_ndvi)
            print(f"NDVI sonucu PostgreSQL veritabanına eklendi: {nir_band_file}")
    
    # Bağlantıyı kapat
    if conn:
        conn.close()

if __name__ == '__main__':
    main()
