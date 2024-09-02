import rasterio
import numpy as np
import sqlite3

# TIFF dosyasının yolu
tiff_file = r'C:\Users\W10\Desktop\GithubProjects\ProjectTERRA\images\GREEN.TIF'

# NDVI hesaplama fonksiyonu
def calculate_ndvi(red_band, nir_band):
    ndvi = (nir_band.astype(float) - red_band.astype(float)) / (nir_band + red_band)
    ndvi = np.clip(ndvi, -1, 1)
    return ndvi

# VARI hesaplama fonksiyonu
def calculate_vari(red_band, green_band, blue_band):
    vari = (green_band.astype(float) - red_band.astype(float)) / (green_band + red_band - blue_band)
    vari = np.clip(vari, -1, 1)
    return vari

# CWSI hesaplama fonksiyonu
def calculate_cwsi(red_band, thermal_band):
    cwsi = (thermal_band.astype(float) - red_band.astype(float)) / (thermal_band + red_band)
    cwsi = np.clip(cwsi, -1, 1)
    return cwsi

# Veritabanı bağlantı ve tablo oluşturma fonksiyonu
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(f"SQLite versiyonu: {sqlite3.version}")
    except sqlite3.Error as e:
        print("DB Connection is being crashed")
    return conn

def create_table(conn):
    try:
        sql_create_indices_table = """ CREATE TABLE IF NOT EXISTS indices_results (
                                        id integer PRIMARY KEY,
                                        file_name text NOT NULL,
                                        mean_ndvi real,
                                        mean_vari real,
                                        mean_cwsi real
                                    ); """
        cursor = conn.cursor()
        cursor.execute(sql_create_indices_table)
    except sqlite3.Error as e:
        print(e)

# Veritabanına sonuç ekleme fonksiyonu
def insert_indices_result(conn, file_name, mean_ndvi, mean_vari, mean_cwsi):
    sql = ''' INSERT INTO indices_results(file_name, mean_ndvi, mean_vari, mean_cwsi)
              VALUES(?,?,?,?) '''
    cursor = conn.cursor()
    cursor.execute(sql, (file_name, mean_ndvi, mean_vari, mean_cwsi))
    conn.commit()

# Ana fonksiyon
def main():
    database = r'C:\Users\W10\Desktop\GithubProjects\ProjectTERRA\indices_results.db'
    
    # Veritabanı bağlantısı
    conn = create_connection(database)
    
    # Tablo oluştur
    if conn is not None:
        create_table(conn)
    
    with rasterio.open(tiff_file) as src:
        print(f"Toplam bant sayısı: {src.count}")
        
        # Bant sayısına göre işlemler
        if src.count >= 4:
            red_band = src.read(3)    # Kırmızı bant
            nir_band = src.read(4)    # Yakın kızılötesi bant
            green_band = src.read(2)  # Yeşil bant
            blue_band = src.read(1)   # Mavi bant
            
            # NDVI, VARI ve CWSI hesaplamaları
            ndvi = calculate_ndvi(red_band, nir_band)
            vari = calculate_vari(red_band, green_band, blue_band)
            
            # CWSI için termal bant kontrolü
            if src.count >= 5:
                thermal_band = src.read(5) # Termal bant (örnek olarak bant 5)
                cwsi = calculate_cwsi(red_band, thermal_band)
                mean_cwsi = cwsi.mean()
            else:
                mean_cwsi = None
        else:
            print("Yeterli bant bulunmuyor. Hesaplamalar yapılamaz.")
            return
        
        # Ortalama değerleri hesapla
        mean_ndvi = ndvi.mean()
        mean_vari = vari.mean()
        
        # Sonuçları veritabanına ekle
        if conn is not None:
            insert_indices_result(conn, tiff_file, mean_ndvi, mean_vari, mean_cwsi)
            print(f"NDVI, VARI ve CWSI sonuçları veritabanına eklendi: {tiff_file}")
    
    # Bağlantıyı kapat
    if conn:
        conn.close()

if __name__ == '__main__':
    main()
