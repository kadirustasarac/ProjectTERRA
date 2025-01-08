# Drone Görüntü Birleştirme ve NDVI Analizi

## İçindekiler
- [Proje Hakkında](#proje-hakkında)
- [Özellikler](#özellikler)
- [Kullanılan Teknolojiler](#kullanılan-teknolojiler)
- [Kurulum](#kurulum)
- [Kullanım](#kullanım)
- [Katkıda Bulunma](#katkıda-bulunma)
- [Lisans](#lisans)

---

## Proje Hakkında
Bu proje, drone ile çekilen görüntüleri işleyerek birleştirilmiş bir kompozit görüntü oluşturmayı amaçlamaktadır. Birleştirme işlemi tamamlandıktan sonra, bitki sağlığı ve yoğunluğu hakkında değerli bilgiler çıkarmak için NDVI (Normalize Edilmiş Fark Bitki İndeksi) analizi yapılır.

Bu araç, tarım, çevre izleme ve arazi yönetimi gibi alanlarda, drone görüntülerinden verimli bir iş akışı ile eyleme dönüştürülebilir veriler elde etmek için kullanılabilir.

## Özellikler
- **Görüntü Birleştirme**: Birden fazla örtüşen drone görüntüsünü tek bir panoramik görüntüye dönüştürür.
- **NDVI Analizi**: Bitki sağlığını değerlendirmek için birleştirilmiş görüntülerden NDVI hesaplar.
- **Yüksek Doğruluk**: Hassas birleştirme ve NDVI hesaplaması için gelişmiş algoritmalar kullanır.
- **Kullanım Kolaylığı**: Drone görüntülerinin hızlı bir şekilde işlenmesi için basit bir arayüz.

## Kullanılan Teknolojiler
- **Python**: Uygulamanın temel programlama dili.
- **OpenCV**: Görüntü birleştirme ve işleme için kullanılır.
- **NumPy**: Verimli sayısal hesaplamalar için.
- **Matplotlib**: NDVI sonuçlarını görselleştirmek için.
- **GDAL** (isteğe bağlı): Coğrafi referanslama ve mekansal veri işlemleri için.

## Kurulum
Proje kurulumunu şu adımları izleyerek yapabilirsiniz:

1. Depoyu klonlayın:
   ```bash
   git clone https://github.com/yourusername/drone-image-stitching-ndvi.git
   cd drone-image-stitching-ndvi
   ```

2. Sanal bir ortam oluşturun (isteğe bağlı ama önerilir):
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows için: venv\Scripts\activate
   ```

3. Gerekli bağımlılıkları yükleyin:
   ```bash
   pip install -r requirements.txt
   ```

4. OpenCV, NumPy ve Matplotlib gibi gerekli kütüphanelerin kurulu olduğundan emin olun.

## Kullanım
1. Drone ile çekilmiş görüntülerinizi `input_images/` dizinine yerleştirin.
2. Ana scripti çalıştırın:
   ```bash
   python main.py
   ```
3. Birleştirilmiş görüntü `output/` dizininde kaydedilecektir.
4. NDVI sonuçları `output/ndvi/` dizininde saklanacak ve görselleştirilecektir.

### Örnek İş Akışı
- Giriş görüntüleri: `input_images/` dizininde bulunan drone görüntüleri.
- Çıktı dosyaları:
  - `stitched_image.jpg`: Panoramik görüntü.
  - `ndvi_image.jpg`: NDVI görüntüsü.

## Katkıda Bulunma
Katkılar memnuniyetle karşılanır! Katkıda bulunmak için şu adımları izleyin:

1. Depoyu fork edin.
2. Yeni bir özellik dalı oluşturun:
   ```bash
   git checkout -b ozellik-adi
   ```
3. Değişikliklerinizi kaydedin:
   ```bash
   git commit -m "Yeni bir özellik ekle"
   ```
4. Dalınızı ittirin:
   ```bash
   git push origin ozellik-adi
   ```
5. Bir pull request oluşturun.

## Lisans
Bu proje MIT Lisansı altında lisanslanmıştır. Daha fazla bilgi için `LICENSE` dosyasına bakın.

---

**Uyarı**: Drone görüntülerinizin coğrafi referanslı ve doğru formatlarda olduğundan emin olun, böylece en iyi sonuçları alabilirsiniz.
