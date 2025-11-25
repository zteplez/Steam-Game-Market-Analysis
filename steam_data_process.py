import pandas as pd
import numpy as np
from collections import Counter

class RealSteamDataProcessor:    
    def __init__(self):
        self.raw_data = None
        self.processed_libraries = None
        self.metadata = None
        self.game_counts = {}
        
    def load_and_process(self, file_path='data/steam-200k.csv', 
                        min_hours=2.0, 
                        sample_users=10000,
                        min_games_per_user=3):
                
        print("="*70)
        print("🎮 GERÇEK STEAM VERİ SETİ İŞLENİYOR")
        print("="*70)
        
        print("\n📁 Adım 1: Veri yükleniyor...")
        try:
            self.raw_data = pd.read_csv(
                file_path, 
                names=['user_id', 'game', 'behavior', 'hours', 'empty'],
                encoding='utf-8'
            )
            print(f"✅ {len(self.raw_data):,} satır yüklendi")
            print(f"   • Toplam oyuncu: {self.raw_data['user_id'].nunique():,}")
            print(f"   • Toplam oyun: {self.raw_data['game'].nunique():,}")
            
        except FileNotFoundError:
            print(f"❌ Dosya bulunamadı: {file_path}")
            print("   Lütfen dosyanın doğru konumda olduğundan emin olun.")
            return None, None, None, None
        
        print("\n🔍 Adım 2: Veri filtreleniyor...")
        
        play_data = self.raw_data[self.raw_data['behavior'] == 'play'].copy()
        print(f"✅ 'play' davranışları: {len(play_data):,} satır")
        
        play_data = play_data[play_data['hours'] >= min_hours]
        print(f"✅ {min_hours}+ saat oynananlar: {len(play_data):,} satır")
        
        print(f"\n👥 Adım 3: {sample_users:,} kullanıcı örnekleniyor...")
        
        # Her kullanıcının oyun sayısını hesapla
        user_game_counts = play_data.groupby('user_id').size()
        
        valid_users = user_game_counts[user_game_counts >= min_games_per_user].index
        print(f"✅ {min_games_per_user}+ oyunu olan kullanıcı: {len(valid_users):,}")
        
        if len(valid_users) > sample_users:
            sampled_users = np.random.choice(valid_users, size=sample_users, replace=False)
        else:
            sampled_users = valid_users
            print(f"⚠️  Yeterli kullanıcı yok, {len(sampled_users):,} kullanıcı kullanılacak")
        
        filtered_data = play_data[play_data['user_id'].isin(sampled_users)]
        print(f"✅ Final veri: {len(filtered_data):,} satır")
        
        # 4. En popüler oyunları bul (çok nadir oyunları çıkar)
        print("\n🎯 Adım 4: Popüler oyunlar belirleniyor...")
        
        game_popularity = filtered_data['game'].value_counts()
        # En az 10 kullanıcıda olan oyunlar
        popular_games = game_popularity[game_popularity >= 10].index.tolist()
        
        filtered_data = filtered_data[filtered_data['game'].isin(popular_games)]
        print(f"✅ {len(popular_games):,} popüler oyun seçildi")
        print(f"✅ Final veri: {len(filtered_data):,} satır")
        
        print("\n📚 Adım 5: Oyuncu kütüphaneleri oluşturuluyor...")
        
        player_libraries = []
        for user_id in sampled_users:
            user_games = filtered_data[filtered_data['user_id'] == user_id]['game'].tolist()
            if user_games:
                player_libraries.append(user_games)
        
        print(f"✅ {len(player_libraries):,} kütüphane oluşturuldu")
        
        # İstatistikler
        library_sizes = [len(lib) for lib in player_libraries]
        print(f"   • Ortalama oyun/kütüphane: {np.mean(library_sizes):.1f}")
        print(f"   • En fazla oyun: {max(library_sizes)}")
        print(f"   • En az oyun: {min(library_sizes)}")
        
        # 6. Oyun sayılarını hesapla
        print("\n📊 Adım 6: Oyun istatistikleri hesaplanıyor...")
        
        game_counts = {}
        for library in player_libraries:
            for game in library:
                game_counts[game] = game_counts.get(game, 0) + 1
        
        print(f"✅ {len(game_counts):,} farklı oyun")
        
        # En popüler 10 oyun
        print("\n🏆 En Popüler 10 Oyun:")
        sorted_games = sorted(game_counts.items(), key=lambda x: x[1], reverse=True)
        for i, (game, count) in enumerate(sorted_games[:10], 1):
            percentage = (count / len(player_libraries)) * 100
            print(f"   {i:2d}. {game:<40} {count:>5} oyuncu (%{percentage:.1f})")
        
        # 7. DataFrame formatına çevir (opsiyonel - Streamlit için)
        print("\n🔄 Adım 7: DataFrame formatına çeviriliyor...")
        
        # Tüm oyunların listesi
        all_games = sorted(game_counts.keys())
        
        # Her kullanıcı için True/False matrisi oluştur
        data_dict = {}
        for i, library in enumerate(player_libraries):
            row = {game: (game in library) for game in all_games}
            data_dict[i] = row
        
        libraries_df = pd.DataFrame.from_dict(data_dict, orient='index')
        print(f"✅ DataFrame: {libraries_df.shape[0]} oyuncu x {libraries_df.shape[1]} oyun")
        
        print("\n🏷️  Adım 8: Metadata oluşturuluyor...")
        
        metadata_list = []
        for game in all_games:
            genre = self._guess_genre(game)
            
            popularity = game_counts[game] / len(player_libraries)
            
            metadata_list.append({
                'Game': game,
                'Genre': genre,
                'Popularity_Score': popularity
            })
        
        metadata_df = pd.DataFrame(metadata_list)
        print(f"✅ {len(metadata_df)} oyun metadata'sı oluşturuldu")
        
        genre_dist = metadata_df['Genre'].value_counts()
        print("\n🎨 Genre Dağılımı:")
        for genre, count in genre_dist.items():
            print(f"   • {genre:<15} {count:>4} oyun")
        
        print("\n💾 Adım 9: Dosyalara kaydediliyor...")
        
        libraries_df.to_csv('steam_libraries.csv')
        metadata_df.to_csv('steam_metadata.csv', index=False)
        
        print("✅ steam_libraries.csv kaydedildi")
        print("✅ steam_metadata.csv kaydedildi")
        
        print("\n" + "="*70)
        print("✅ VERİ İŞLEME TAMAMLANDI!")
        print("="*70)
        print("\nŞimdi Streamlit dashboard'unu çalıştırabilirsiniz:")
        print("   streamlit run steam_dashboard.py")
        
        return libraries_df, metadata_df, player_libraries, game_counts
    
    def _guess_genre(self, game_name):
        """Oyun isminden basit genre tahmini yap"""
        game_lower = game_name.lower()
        
        fps_keywords = ['counter-strike', 'call of duty', 'battlefield', 'half-life',
                       'team fortress', 'left 4 dead', 'borderlands', 'payday',
                       'killing floor', 'bioshock', 'far cry', 'crysis']
        
        rpg_keywords = ['fallout', 'elder scrolls', 'skyrim', 'witcher', 'dragon age',
                       'mass effect', 'final fantasy', 'dark souls', 'divinity',
                       'pillars of eternity', 'baldur', 'neverwinter']
        
        strategy_keywords = ['civilization', 'total war', 'xcom', 'crusader kings',
                            'europa universalis', 'hearts of iron', 'stellaris',
                            'age of empires', 'starcraft', 'warcraft']
        
        moba_keywords = ['dota', 'league of legends', 'smite', 'heroes of the storm']
        
        sandbox_keywords = ['minecraft', 'terraria', 'rust', 'ark', 'dont starve',
                           'subnautica', 'the forest', '7 days to die']
        
        indie_keywords = ['ftl', 'binding of isaac', 'hotline miami', 'bastion',
                         'transistor', 'limbo', 'braid', 'super meat boy',
                         'to the moon', 'undertale', 'stardew valley']
        
        horror_keywords = ['resident evil', 'silent hill', 'dead space', 'outlast',
                          'amnesia', 'alien', 'dying light']
        
        sports_keywords = ['fifa', 'nba', 'nhl', 'madden', 'rocket league',
                          'forza', 'gran turismo', 'dirt', 'f1']
        
        for keyword in fps_keywords:
            if keyword in game_lower:
                return 'FPS'
        
        for keyword in rpg_keywords:
            if keyword in game_lower:
                return 'RPG'
        
        for keyword in strategy_keywords:
            if keyword in game_lower:
                return 'Strategy'
        
        for keyword in moba_keywords:
            if keyword in game_lower:
                return 'MOBA'
        
        for keyword in sandbox_keywords:
            if keyword in game_lower:
                return 'Sandbox'
        
        for keyword in indie_keywords:
            if keyword in game_lower:
                return 'Indie'
        
        for keyword in horror_keywords:
            if keyword in game_lower:
                return 'Horror'
        
        for keyword in sports_keywords:
            if keyword in game_lower:
                return 'Sports'
        
        return 'Action'
    
    def get_statistics(self):
        """Veri seti hakkında detaylı istatistikler"""
        if self.raw_data is None:
            print("❌ Önce veriyi yüklemelisiniz!")
            return
        
        print("\n" + "="*70)
        print("📊 VERİ SETİ İSTATİSTİKLERİ")
        print("="*70)
        
        print(f"\n🎮 Genel Bilgiler:")
        print(f"   • Toplam kayıt: {len(self.raw_data):,}")
        print(f"   • Toplam oyuncu: {self.raw_data['user_id'].nunique():,}")
        print(f"   • Toplam oyun: {self.raw_data['game'].nunique():,}")
        
        print(f"\n📊 Davranış Dağılımı:")
        behavior_dist = self.raw_data['behavior'].value_counts()
        for behavior, count in behavior_dist.items():
            percentage = (count / len(self.raw_data)) * 100
            print(f"   • {behavior:<10} {count:>8,} (%{percentage:.1f})")
        
        print(f"\n⏱️  Oynama Saati İstatistikleri:")
        play_hours = self.raw_data[self.raw_data['behavior'] == 'play']['hours']
        print(f"   • Ortalama: {play_hours.mean():.1f} saat")
        print(f"   • Medyan: {play_hours.median():.1f} saat")
        print(f"   • Maksimum: {play_hours.max():.1f} saat")
        print(f"   • Minimum: {play_hours.min():.1f} saat")


def main():
    """Ana işlem fonksiyonu"""
    
    print("""
    ╔═══════════════════════════════════════════════════════════════╗
    ║                                                               ║
    ║     🎮 GERÇEK STEAM VERİ SETİ İŞLEYİCİ                      ║
    ║     Market Basket Analysis için Veri Hazırlama              ║
    ║                                                               ║
    ╚═══════════════════════════════════════════════════════════════╝
    """)
    
    # İşleyici oluştur
    processor = RealSteamDataProcessor()
    
    # Parametreler
    print("\n⚙️  PARAMETRELER:")
    print("   • Dosya: steam-200k.csv")
    print("   • Minimum oynama saati: 2.0 saat")
    print("   • Örneklenecek kullanıcı: 10,000")
    print("   • Minimum oyun/kullanıcı: 3")
    print()
    
    input("Enter tuşuna basarak işlemi başlatın...")
    print()
    
    # Veriyi işle
    libraries_df, metadata_df, player_libraries, game_counts = processor.load_and_process(
        file_path='steam-200k.csv',
        min_hours=2.0,
        sample_users=10000,
        min_games_per_user=3
    )
    
    if libraries_df is not None:
        print("\n" + "="*70)
        print("🎉 BAŞARILI! Artık dashboard'u çalıştırabilirsiniz!")
        print("="*70)
        print("\nKomut:")
        print("   streamlit run steam_dashboard.py")
        print()


if __name__ == "__main__":
    main()