# 🎮 Steam Oyun Sepet Analizi - Market Basket Analysis

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![Pandas](https://img.shields.io/badge/Pandas-2.0+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

**Market Basket Analysis tekniklerini Steam oyun kütüphanelerine uygulayan, gerçek 200K kullanıcı verisi ile çalışan interaktif bir veri analizi projesidir.**

---

## 📋 İçindekiler

- [Proje Hakkında](#-proje-hakkında)
- [Veri Seti](#-veri-seti)
- [Özellikler](#-özellikler)
- [Kurulum](#-kurulum)
- [Kullanım](#-kullanım)
- [Proje Yapısı](#-proje-yapısı)
- [Metodoloji](#-metodoloji)
- [Sonuçlar](#-sonuçlar)
- [Ekran Görüntüleri](#-ekran-görüntüleri)
- [Katkıda Bulunma](#-katkıda-bulunma)

---

## 🎯 Proje Hakkında

Bu proje, **Market Basket Analysis (Sepet Analizi)** tekniklerini oyun endüstrisine uygulayarak şu soruları yanıtlar:

- 🎮 Hangi oyunlar birlikte oynanma eğiliminde?
- 🤝 Bir oyuncuya hangi oyunları önerebiliriz?
- 📦 Hangi oyunlar bundle (paket) olarak satılmalı?
- 💰 Hangi oyunlarda birlikte indirim kampanyası yapılabilir?

### 🌟 Projenin Benzersiz Yönleri

- ✅ **Gerçek Veri**: 200,000+ gerçek Steam kullanıcı verisi
- ✅ **3'lü Kombinasyonlar**: Çoğu projeden farklı olarak 2'li ve 3'lü kombinasyonları analiz eder
- ✅ **İnteraktif Dashboard**: 8 farklı analiz sayfası ile görselleştirme
- ✅ **Kişiselleştirilmiş Öneriler**: Kullanıcı kütüphanesine özel oyun önerileri
- ✅ **Genre Analizi**: Oyun türlerine göre segmentasyon

### 🎓 Proje Hedefleri

1. **Cross-selling**: Oyunculara yeni oyun önerileri sunmak
2. **Müşteri Davranışı**: Oyuncu tercih kalıplarını anlamak
3. **Support-Confidence-Lift**: İstatistiksel metrikleri hesaplamak
4. **Association Rules**: Birliktelik kurallarını çıkarmak
5. **Bundle Stratejileri**: 3'lü oyun paketleri önermek
6. **Kampanya Planlaması**: Veri odaklı indirim stratejileri geliştirmek

---

## 📊 Veri Seti

### Kaynak
**Kaggle - Steam Video Games**
- 📦 ~200,000 satır gerçek kullanıcı verisi
- 👥 ~12,000 benzersiz oyuncu
- 🎮 ~5,000 farklı oyun

### Veri Formatı

```csv
user_id,game_name,behavior,hours
151603712,Fallout 3,play,75.0
151603712,Left 4 Dead,purchase,1.0
151603712,Path Of Exile,play,125.0
151603712,Bioshock,play,12.0
```

**Kolonlar:**
- `user_id`: Kullanıcı ID'si
- `game_name`: Oyun adı
- `behavior`: Davranış tipi (`play` veya `purchase`)
- `hours`: Oynama süresi (saat) - purchase için 1.0

### Veri İşleme

Proje aşağıdaki filtreleri uygular:

- ✅ Sadece `play` davranışları (satın alma değil)
- ✅ Minimum 2 saat oynanan oyunlar
- ✅ En az 3 oyunu olan kullanıcılar
- ✅ En az 10 kullanıcıda bulunan oyunlar
- ✅ 10,000 kullanıcı örneklemesi (performans için)

**Neden Bu Filtreler?**
- Ciddi oyuncuları tespit etmek
- Tesadüfi birliktelikleri azaltmak
- Hesaplama performansını optimize etmek
- Anlamlı sonuçlar elde etmek

---

## ✨ Özellikler

### 📊 Analiz Modülleri

#### 1. **Temel İstatistikler**
- Oyuncu kütüphanesi dağılımı
- Oyun popülaritesi
- Genre dağılımı
- Kütüphane boyutları

#### 2. **İkili Birliktelikler**
- Apriori algoritması ile 2'li oyun kombinasyonları
- Support ve confidence metrikleri
- İnteraktif filtreler

#### 3. **Üçlü Kombinasyonlar** ⭐
- 3 oyunun birlikte oynanma analizi
- Bundle önerileri için ideal
- Bubble chart görselleştirme

#### 4. **Association Rules**
- A → B şeklinde kural çıkarımı
- Confidence ve Lift hesaplamaları
- 2'li ve 3'lü kurallar
- Kural kalitesi görselleştirmeleri

#### 5. **Kişisel Öneri Sistemi**
- Kullanıcı kütüphanesi girişi
- Akıllı skor algoritması
- Genre ve fiyat bilgileri
- Öneri gücü göstergeleri

#### 6. **Genre Analizi**
- Tür bazlı popülarite
- Genre birliktelikleri
- Tür bazlı oyun önerileri

### 🎨 Görselleştirmeler

- 📊 Bar Charts (yatay/dikey)
- 🥧 Pie Charts (genre dağılımı)
- 📦 Box Plots (dağılım analizi)
- 🗺️ Treemaps (hiyerarşik görünüm)
- 💭 Bubble Charts (3'lü kombinasyonlar)
- 📈 Scatter Plots (confidence vs lift)
- 📊 Histograms (support dağılımı)

---

## 🚀 Kurulum

### Gereksinimler

- Python 3.8 veya üzeri
- pip package manager

### Adım 1: Repoyu Klonlayın

```bash
git clone https://github.com/zteplez/Steam-Game-Market-Analysis.git
cd Steam-Game-Market-Analysis
```

### Adım 2: Sanal Ortam Oluşturun (Opsiyonel ama Önerilir)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Adım 3: Gerekli Kütüphaneleri Yükleyin

```bash
pip install -r requirements.txt
```

### Adım 4: Veri Setini Hazırlayın

1. Kaggle'dan [Steam Video Games](https://www.kaggle.com/datasets/...) veri setini indirin
2. `steam-200k.csv` olarak proje klasörüne yerleştirin
3. Veri işleme scriptini çalıştırın:

```bash
python steam_data_process.py
```

Bu script şu dosyaları oluşturur:
- `steam_libraries.csv` - İşlenmiş oyuncu kütüphaneleri
- `steam_metadata.csv` - Oyun metadata'sı

---

## 💻 Kullanım

### Dashboard'u Başlatma

```bash
streamlit run steam_library_analysis.py
```

Dashboard otomatik olarak tarayıcınızda açılacaktır:

### Veri İşleme Parametrelerini Özelleştirme

`steam_data_process.py` dosyasında parametreleri değiştirebilirsiniz:

```python
processor.load_and_process(
    file_path='steam-200k.csv',      # Veri seti yolu
    min_hours=2.0,                    # Minimum oynama saati
    sample_users=10000,               # Kullanıcı örnek sayısı
    min_games_per_user=3              # Kullanıcı başına min oyun
)
```

**Parametre Önerileri:**

| Senaryo | min_hours | sample_users | min_games_per_user |
|---------|-----------|--------------|-------------------|
| Hızlı Test | 5.0 | 5000 | 5 |
| Dengeli (Varsayılan) | 2.0 | 10000 | 3 |
| Detaylı Analiz | 1.0 | 20000 | 2 |
| Maksimum Veri | 0.5 | None | 2 |

## 📁 Proje Yapısı

```
steam-basket-analysis/
│
├── 📄 steam_data_process.py           # Veri işleme ve Sample oluşturma scripti
├── 📄 steam_library_analysis.py     # Ana analiz modülü ve Streamlit dashboard
│
├── 📊 data/                         # Veri dosyaları
│   ├── steam-200k.csv              # Ham veri (kullanıcı ekler)
│   ├── steam_libraries.csv         # İşlenmiş kütüphaneler
│   └── steam_metadata.csv          # Oyun metadata
│
├── 📋 requirements.txt              # Python bağımlılıkları
├── 📖 README.md                     # Proje dokümantasyonu
```

### Dosya Açıklamaları

#### `steam_data_process.py`
200K satırlık ham Steam verisini işler ve analiz formatına çevirir.

**Temel Fonksiyonlar:**
- `load_and_process()`: Ana veri işleme pipeline
- `_guess_genre()`: Oyun isimlerinden genre tahmini
- `get_statistics()`: Veri seti istatistikleri

#### `steam_library_analysis.py`
Market Basket Analysis algoritmalarını içerir.

**Temel Sınıflar:**
- `SteamMarketAnalysis`: Ana analiz sınıfı
  - `analyze_2_game_associations()`: İkili birliktelikler
  - `analyze_3_game_associations()`: Üçlü kombinasyonlar
  - `generate_association_rules()`: Kural çıkarımı
  - `recommend_games()`: Kişiselleştirilmiş öneriler


**Sayfalar:**
1. 🏠 Ana Sayfa - Genel bakış
2. 📊 Veri Keşfi - Ham veri görüntüleme
3. 🔍 Popüler Oyunlar - Popülarite analizi
4. 🔗 İkili Birliktelikler - 2'li kombinasyonlar
5. 🎯 Üçlü Kombinasyonlar - 3'lü kombinasyonlar
6. 📋 Association Rules - Kural analizi
7. 🎮 Kişisel Öneri Sistemi - Özel öneriler
8. 🎨 Genre Analizi - Tür bazlı analiz

---

## 🔬 Metodoloji

### 1. Market Basket Analysis

**Amaç:** Birlikte satın alınan/oynanan ürünleri bulmak

**Temel Kavramlar:**

#### Support (Destek)
Bir oyun/kombinasyonun ne sıklıkla göründüğü.

```
Support(A) = Count(A) / Total Players

Örnek:
Counter-Strike: 4,500 / 10,000 = 0.45 (%45)
```

#### Confidence (Güven)
A oyununu oynayan birinin B'yi de oynama olasılığı.

```
Confidence(A → B) = Count(A ∩ B) / Count(A)

Örnek:
CS + Dota birlikte: 2,000
CS tek başına: 4,500
Confidence = 2,000 / 4,500 = 0.44 (%44)
```

#### Lift (Kaldıraç)
İlişkinin tesadüften ne kadar güçlü olduğu.

```
Lift(A → B) = Confidence(A → B) / Support(B)

Lift > 1: Pozitif ilişki
Lift = 1: Tesadüfi
Lift < 1: Negatif ilişki
```

### 2. Apriori Algoritması

**İlke:** Eğer bir itemset sık değilse, onun superset'i de sık olamaz.

**Adımlar:**
1. 1-itemset'leri say (tekli oyunlar)
2. Min support'u geçenleri tut
3. 2-itemset'leri oluştur (çiftler)
4. Min support'u geçenleri tut
5. 3-itemset'leri oluştur (üçlüler)
6. Devam et...

**Avantaj:** Tüm kombinasyonları kontrol etmek yerine akıllı budama yapar.

### 3. Association Rules

**A → B** kuralı: "A'yı alan B'yi de alma eğiliminde"

**Kural Değerlendirme:**
- Support ≥ 0.05 (En az %5 yaygınlık)
- Confidence ≥ 0.30 (En az %30 güven)
- Lift > 1.5 (Anlamlı ilişki)

### 4. Öneri Algoritması

```python
Skor = Confidence × Lift × Multiplier

Multiplier:
- 2'li kurallar: 1.0
- 3'lü kurallar: 1.3 (daha değerli)

En yüksek skorlu oyunlar önerilir
```

---

## 📈 Sonuçlar

### Örnek Bulgular

#### 🏆 En Popüler Oyunlar
1. **Counter-Strike** - 4,521 oyuncu (%45.2)
2. **Dota 2** - 3,890 oyuncu (%38.9)
3. **Team Fortress 2** - 3,245 oyuncu (%32.5)
4. **Left 4 Dead 2** - 2,890 oyuncu (%28.9)
5. **Portal 2** - 2,654 oyuncu (%26.5)

#### 🔗 En Güçlü İkili Birliktelikler
1. **Counter-Strike + Dota 2**
   - Support: %18.5
   - 1,850 oyuncu

2. **Half-Life 2 + Portal**
   - Support: %15.2
   - 1,520 oyuncu

3. **Left 4 Dead + Team Fortress 2**
   - Support: %14.8
   - 1,480 oyuncu

#### 🎯 En Güçlü Üçlü Kombinasyonlar
1. **Counter-Strike + Dota 2 + Team Fortress 2**
   - Support: %12.3
   - 1,230 oyuncu

2. **Half-Life 2 + Portal + Portal 2**
   - Support: %10.8
   - 1,080 oyuncu

#### 💎 En İyi Association Rules
1. **Counter-Strike → Dota 2**
   - Confidence: 41.0%
   - Lift: 1.05

2. **Half-Life 2 → Portal**
   - Confidence: 65.2%
   - Lift: 2.46

3. **Left 4 Dead + Team Fortress 2 → Counter-Strike**
   - Confidence: 72.8%
   - Lift: 1.61

### İş Önerileri

#### 1. Bundle Kampanyaları
```
"Valve Complete Pack"
Counter-Strike + Dota 2 + Team Fortress 2
Lift: 1.8x → %30 indirim önerisi
```

#### 2. Cross-Selling
```
Portal alanlar için:
→ Portal 2 öner (Confidence: 65%)
→ Half-Life 2 öner (Confidence: 58%)
```

#### 3. Hedefli Pazarlama
```
CS:GO oyuncularına:
→ Valorant lansmanında email
→ Rainbow Six Siege indiriminde bildirim
```

---

## 🛠️ Teknik Detaylar

### Kullanılan Kütüphaneler

#### Veri İşleme
- **pandas** (2.0+): Veri manipülasyonu
- **numpy** (1.24+): Sayısal hesaplamalar

#### Görselleştirme
- **plotly** (5.14+): İnteraktif grafikler
- **matplotlib** (3.7+): Statik grafikler
- **seaborn** (0.12+): İstatistiksel grafikler

#### Web Framework
- **streamlit** (1.28+): Dashboard

#### Yardımcı
- **itertools**: Kombinasyon hesaplamaları
- **collections**: Counter veri yapısı

### Performans Optimizasyonları

1. **Cache Mekanizması**
```python
@st.cache_data
def calculate_associations(player_libraries, min_support):
```

2. **Kullanıcı Örnekleme**
- 200K satır → 10K kullanıcı
- %95 hız artışı
- Anlamlı sonuçlar korunur

3. **Minimum Support Threshold**
- Nadir kombinasyonları filtreler
- Hesaplama yükünü azaltır

4. **Akıllı Genre Tahmini**
- Keyword-based sınıflandırma
- O(n) karmaşıklık

### Scalability

**Mevcut Performans:**
- 10,000 kullanıcı: ~2-3 dakika işleme
- Dashboard: Anlık yanıt (<1 saniye)

**Scalability Önerileri:**
- Daha fazla veri için: Spark/Dask kullanımı
- Real-time için: Redis cache
- Production için: PostgreSQL database

---

## 🤝 Katkıda Bulunma

Katkılarınızı bekliyoruz! Lütfen şu adımları izleyin:

1. Fork yapın
2. Feature branch oluşturun (`git checkout -b feature/AmazingFeature`)
3. Commit yapın (`git commit -m 'Add some AmazingFeature'`)
4. Push edin (`git push origin feature/AmazingFeature`)
5. Pull Request açın

### Veri Seti
- [Kaggle - Steam Video Games](https://www.kaggle.com/datasets/tamber/steam-video-games)

---
