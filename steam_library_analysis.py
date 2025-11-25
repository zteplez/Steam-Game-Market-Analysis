import streamlit as st
import pandas as pd
import numpy as np
from itertools import combinations
import plotly.express as px
import plotly.graph_objects as go
from collections import Counter
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(
    page_title="Steam Oyun Analizi",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1e3a8a;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #475569;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
    }
    .game-card {
        background: #f8fafc;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #3b82f6;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-header">🎮 Steam Oyun Sepet Analizi</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Oyun Önerileri ve Birliktelik Keşfi</p>', unsafe_allow_html=True)
st.markdown("---")

@st.cache_data
def load_data():
    """Veriyi yükle ve hazırla"""
    try:
        libraries = pd.read_csv('data/steam_libraries.csv', index_col=0)
        
        try:
            metadata = pd.read_csv('data/steam_metadata.csv')
        except:
            metadata = None
        
        player_libraries = []
        for i, row in libraries.iterrows():
            library = [game for game in libraries.columns if row[game] == True or row[game] == 'True']
            if library:
                player_libraries.append(library)
        
        game_counts = {}
        for library in player_libraries:
            for game in library:
                game_counts[game] = game_counts.get(game, 0) + 1
        
        return libraries, metadata, player_libraries, game_counts
    
    except FileNotFoundError:
        st.error("❌ Veri dosyaları bulunamadı! Lütfen 'steam_libraries.csv' dosyasının mevcut olduğundan emin olun.")
        return None, None, None, None

@st.cache_data
@st.cache_data
def calculate_associations(player_libraries, min_support=0.05):
    """2'li ve 3'lü birliktelikleri hesapla"""
    total_players = len(player_libraries)
    min_count = int(min_support * total_players)
    
    # 2'li birliktelikler
    assoc_2_counts = {}
    for library in player_libraries:
        if len(library) >= 2:
            for game1, game2 in combinations(sorted(library), 2):
                pair = (game1, game2)
                assoc_2_counts[pair] = assoc_2_counts.get(pair, 0) + 1
    
    associations_2 = {}
    for pair, count in assoc_2_counts.items():
        if count >= min_count:
            associations_2[pair] = {
                'count': count,
                'support': count / total_players
            }
    
    # 3'lü birliktelikler
    assoc_3_counts = {}
    for library in player_libraries:
        if len(library) >= 3:
            for game1, game2, game3 in combinations(sorted(library), 3):
                triple = (game1, game2, game3)
                assoc_3_counts[triple] = assoc_3_counts.get(triple, 0) + 1
    
    associations_3 = {}
    for triple, count in assoc_3_counts.items():
        if count >= min_count:
            associations_3[triple] = {
                'count': count,
                'support': count / total_players
            }
    
    return associations_2, associations_3

@st.cache_data
def generate_rules(associations_2, associations_3, game_counts, total_players, min_confidence=0.30):
    """Association rules oluştur"""
    rules = []
    
    # 2'li kurallar
    for (game1, game2), info in associations_2.items():
        together_count = info['count']
        
        # game1 → game2
        confidence1 = together_count / game_counts[game1]
        if confidence1 >= min_confidence:
            lift1 = confidence1 / (game_counts[game2] / total_players)
            rules.append({
                'antecedent': game1,
                'consequent': game2,
                'support': info['support'],
                'confidence': confidence1,
                'lift': lift1,
                'type': '2-game'
            })
        
        # game2 → game1
        confidence2 = together_count / game_counts[game2]
        if confidence2 >= min_confidence:
            lift2 = confidence2 / (game_counts[game1] / total_players)
            rules.append({
                'antecedent': game2,
                'consequent': game1,
                'support': info['support'],
                'confidence': confidence2,
                'lift': lift2,
                'type': '2-game'
            })
    
    # 3'lü kurallar
    for (game1, game2, game3), info in associations_3.items():
        together_count = info['count']
        
        # Her üçlü için farklı kombinasyonlar
        pairs = [
            ((game1, game2), game3),
            ((game1, game3), game2),
            ((game2, game3), game1)
        ]
        
        for (g1, g2), consequent in pairs:
            pair_key = tuple(sorted([g1, g2]))
            if pair_key in associations_2:
                pair_count = associations_2[pair_key]['count']
                confidence = together_count / pair_count
                
                if confidence >= min_confidence:
                    lift = confidence / (game_counts[consequent] / total_players)
                    rules.append({
                        'antecedent': f"{g1} + {g2}",
                        'consequent': consequent,
                        'support': info['support'],
                        'confidence': confidence,
                        'lift': lift,
                        'type': '3-game'
                    })
    
    return sorted(rules, key=lambda x: x['confidence'], reverse=True)

@st.cache_data
def generate_rules(associations_2, game_counts, total_players, min_confidence=0.30):
    """Association rules oluştur"""
    rules = []
    
    for (game1, game2), info in associations_2.items():
        together_count = info['count']
        
        confidence1 = together_count / game_counts[game1]
        if confidence1 >= min_confidence:
            lift1 = confidence1 / (game_counts[game2] / total_players)
            rules.append({
                'antecedent': game1,
                'consequent': game2,
                'support': info['support'],
                'confidence': confidence1,
                'lift': lift1,
                'type': '2-game'
            })
        
        confidence2 = together_count / game_counts[game2]
        if confidence2 >= min_confidence:
            lift2 = confidence2 / (game_counts[game1] / total_players)
            rules.append({
                'antecedent': game2,
                'consequent': game1,
                'support': info['support'],
                'confidence': confidence2,
                'lift': lift2,
                'type': '2-game'
            })
    
    return sorted(rules, key=lambda x: x['confidence'], reverse=True)

libraries, metadata, player_libraries, game_counts = load_data()

if libraries is not None and player_libraries is not None:
    
    st.sidebar.title("📋 Menü")
    st.sidebar.markdown("---")
    
    page = st.sidebar.selectbox(
        "Analiz türünü seçin:",
        [
            "🏠 Ana Sayfa",
            "📊 Veri Keşfi",
            "🔍 Popüler Oyunlar",
            "🔗 İkili Birliktelikler",
            "🎯 Üçlü Kombinasyonlar",
            "📋 Association Rules",
            "🎮 Kişisel Öneri Sistemi",
            "🎨 Genre Analizi"
        ]
    )
    
    st.sidebar.markdown("---")
    
    if page == "🏠 Ana Sayfa":
        st.header("🏠 Hoş Geldiniz!")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("🎮 Toplam Oyuncu", len(player_libraries))
        
        with col2:
            st.metric("🎯 Toplam Oyun", len(game_counts))
        
        with col3:
            avg_games = np.mean([len(lib) for lib in player_libraries])
            st.metric("📚 Ort. Oyun/Kütüphane", f"{avg_games:.1f}")
        
        with col4:
            total_ownership = sum(game_counts.values())
            st.metric("💎 Toplam Sahiplik", total_ownership)
        
        st.markdown("---")
                
        st.subheader("⚡ Temel İstatistikler")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**🏆 En Popüler 5 Oyun**")
            sorted_games = sorted(game_counts.items(), key=lambda x: x[1], reverse=True)
            for i, (game, count) in enumerate(sorted_games[:5], 1):
                percentage = (count / len(player_libraries)) * 100
                st.write(f"{i}. **{game}**")
                st.progress(percentage / 100)
                st.caption(f"{count} oyuncu (%{percentage:.1f})")
        
        with col2:
            if metadata is not None:
                st.markdown("**🎨 Tür Dağılımı**")
                genre_counts = metadata['Genre'].value_counts()
                fig = px.pie(
                    values=genre_counts.values,
                    names=genre_counts.index,
                    hole=0.4,
                    color_discrete_sequence=px.colors.qualitative.Set3
                )
                fig.update_layout(height=600, showlegend=True)
                st.plotly_chart(fig, use_container_width=True)
        
        with col3:
            st.markdown("**📊 Kütüphane Dağılımı**")
            library_sizes = [len(lib) for lib in player_libraries]
            fig = go.Figure(data=[go.Histogram(x=library_sizes, nbinsx=20)])
            fig.update_layout(
                xaxis_title="Oyun Sayısı",
                yaxis_title="Oyuncu Sayısı",
                height=600
            )
            st.plotly_chart(fig, use_container_width=True)
    
    elif page == "📊 Veri Keşfi":
        st.header("📊 Veri Keşfi")
        
        tab1, tab2, tab3 = st.tabs(["Ham Veri", "İstatistikler", "Örnek Kütüphaneler"])
        
        with tab1:
            st.subheader("Ham Veri Görünümü")
            
            col1, col2 = st.columns([3, 1])
            with col1:
                show_rows = st.slider("Gösterilecek satır sayısı:", 5, 50, 10)
        
            
            

            st.dataframe(libraries.head(show_rows), use_container_width=True)
            st.caption(f"Toplam: {len(libraries)} oyuncu x {len(libraries.columns)} oyun")
        
        with tab2:
            st.subheader("Detaylı İstatistikler")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**📚 Kütüphane Boyutları**")
                library_sizes = [len(lib) for lib in player_libraries]
                stats_df = pd.DataFrame({
                    'Metrik': ['Ortalama', 'Medyan', 'En Fazla', 'En Az', 'Std. Sapma'],
                    'Değer': [
                        f"{np.mean(library_sizes):.2f}",
                        f"{np.median(library_sizes):.0f}",
                        f"{max(library_sizes)}",
                        f"{min(library_sizes)}",
                        f"{np.std(library_sizes):.2f}"
                    ]
                })
                st.dataframe(stats_df, use_container_width=True, hide_index=True)
            
            with col2:
                st.markdown("**🎯 Oyun Popülaritesi**")
                pop_stats = pd.Series(game_counts.values())
                pop_df = pd.DataFrame({
                    'Metrik': ['Ortalama Sahiplik', 'En Popüler', 'En Az Popüler', 'Medyan'],
                    'Değer': [
                        f"{pop_stats.mean():.0f}",
                        f"{pop_stats.max()}",
                        f"{pop_stats.min()}",
                        f"{pop_stats.median():.0f}"
                    ]
                })
                st.dataframe(pop_df, use_container_width=True, hide_index=True)
            
            col1 = st.columns(1)[0]
            
            with col1:
                fig = px.histogram(
                    x=library_sizes,
                    nbins=25,
                    title="Kütüphane Boyutları Dağılımı",
                    labels={'x': 'Oyun Sayısı', 'y': 'Oyuncu Sayısı'}
                )
                st.plotly_chart(fig, use_container_width=True)
            
        
        with tab3:
            st.subheader("Örnek Oyuncu Kütüphaneleri")
            
            num_examples = st.slider("Kaç örnek görmek istersiniz?", 3, 10, 5)
            
            for i in range(min(num_examples, len(player_libraries))):
                with st.expander(f"🎮 Oyuncu {i+1} - {len(player_libraries[i])} oyun"):
                    games_str = " • ".join(player_libraries[i])
                    st.markdown(f"**Oyunlar:** {games_str}")
                    
                    if metadata is not None:
                        genres = []
                        for game in player_libraries[i]:
                            game_info = metadata[metadata['Game'] == game]
                            if not game_info.empty:
                                genres.append(game_info.iloc[0]['Genre'])
                        
                        genre_counts = Counter(genres)
                        st.markdown(f"**Türler:** {dict(genre_counts)}")
    
    elif page == "🔍 Popüler Oyunlar":
        st.header("🔍 Popüler Oyunlar Analizi")
        
        col1, col2 = st.columns([1, 3])
        
        with col1:
            st.subheader("Filtreler")
            
            top_n = st.slider("Gösterilecek oyun sayısı:", 5, 30, 15)
            
            chart_type = st.radio(
                "Grafik türü:",
                ["Bar Chart (Yatay)", "Bar Chart (Dikey)"]
            )
            
            if metadata is not None:
                filter_genre = st.multiselect(
                    "Türe göre filtrele:",
                    options=["Tümü"] + sorted(metadata['Genre'].unique().tolist()),
                    default=["Tümü"]
                )
            else:
                filter_genre = ["Tümü"]
        
        with col2:
            if metadata is not None and "Tümü" not in filter_genre:
                filtered_games = metadata[metadata['Genre'].isin(filter_genre)]['Game'].tolist()
                filtered_counts = {g: c for g, c in game_counts.items() if g in filtered_games}
            else:
                filtered_counts = game_counts
            
            sorted_games = sorted(filtered_counts.items(), key=lambda x: x[1], reverse=True)
            top_games = sorted_games[:top_n]
            
            games = [item[0] for item in top_games]
            counts = [item[1] for item in top_games]
            percentages = [(c / len(player_libraries)) * 100 for c in counts]
            
            if chart_type == "Bar Chart (Yatay)":
                fig = px.bar(
                    x=counts,
                    y=games,
                    orientation='h',
                    title=f'En Popüler {top_n} Oyun',
                    labels={'x': 'Oyuncu Sayısı', 'y': 'Oyunlar'},
                    color=counts,
                    color_continuous_scale='viridis'
                )
                fig.update_layout(height=600)
                
            elif chart_type == "Bar Chart (Dikey)":
                fig = px.bar(
                    x=games,
                    y=counts,
                    title=f'En Popüler {top_n} Oyun',
                    labels={'x': 'Oyunlar', 'y': 'Oyuncu Sayısı'},
                    color=counts,
                    color_continuous_scale='plasma'
                )
                fig.update_xaxes(tickangle=45)
                fig.update_layout(height=600)
                
            
            st.plotly_chart(fig, use_container_width=True)
            
            st.subheader("📋 Detaylı Liste")
            
            table_data = []
            for i, (game, count) in enumerate(top_games, 1):
                percentage = (count / len(player_libraries)) * 100
                row = {
                    'Sıra': i,
                    'Oyun': game,
                    'Oyuncu Sayısı': count,
                    'Yüzde': f"%{percentage:.1f}"
                }
                
                if metadata is not None:
                    game_info = metadata[metadata['Game'] == game]
                    if not game_info.empty:
                        row['Tür'] = game_info.iloc[0]['Genre']
                
                table_data.append(row)
            
            df_table = pd.DataFrame(table_data)
            st.dataframe(df_table, use_container_width=True, hide_index=True)
    
    elif page == "🔗 İkili Birliktelikler":
        st.header("🔗 İkili Oyun Birliktelikleri")
        
        col1, col2 = st.columns([1, 3])
        
        with col1:
            st.subheader("Parametreler")
            
            min_support = st.slider(
                "Minimum Support (%):",
                min_value=1,
                max_value=20,
                value=5,
                step=1,
                help="Bir birlikteliğin analize dahil edilmesi için minimum destek yüzdesi"
            ) / 100
            
            show_top_n = st.slider("Gösterilecek birliktelik sayısı:", 10, 50, 20)
            
            sort_by = st.radio(
                "Sıralama kriteri:",
                ["Support", "Oyuncu Sayısı"]
            )
        
        with col2:
            with st.spinner("Birliktelikler hesaplanıyor..."):
                associations_2, _ = calculate_associations(player_libraries, min_support)
            
            if associations_2:
                st.success(f"✅ {len(associations_2)} birliktelik bulundu!")
                
                if sort_by == "Support":
                    sorted_assoc = sorted(associations_2.items(), 
                                        key=lambda x: x[1]['support'], reverse=True)
                else:
                    sorted_assoc = sorted(associations_2.items(), 
                                        key=lambda x: x[1]['count'], reverse=True)
                
                top_assoc = sorted_assoc[:show_top_n]
                
                labels = [f"{pair[0]} + {pair[1]}" for pair, _ in top_assoc]
                counts = [info['count'] for _, info in top_assoc]
                supports = [info['support'] * 100 for _, info in top_assoc]
                
                fig = go.Figure()
                
                fig.add_trace(go.Bar(
                    y=labels,
                    x=counts,
                    orientation='h',
                    name='Oyuncu Sayısı',
                    marker_color='steelblue',
                    text=counts,
                    textposition='auto',
                ))
                
                fig.update_layout(
                    title=f"En Güçlü {show_top_n} İkili Birliktelik",
                    xaxis_title="Oyuncu Sayısı",
                    yaxis_title="Oyun Çiftleri",
                    height=max(400, show_top_n * 25),
                    showlegend=False
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                st.subheader("📋 Detaylı Birliktelik Tablosu")
                
                table_data = []
                for i, (pair, info) in enumerate(top_assoc, 1):
                    table_data.append({
                        'Sıra': i,
                        'Oyun 1': pair[0],
                        'Oyun 2': pair[1],
                        'Oyuncu Sayısı': info['count'],
                        'Support': f"%{info['support'] * 100:.2f}"
                    })
                
                df_assoc = pd.DataFrame(table_data)
                st.dataframe(df_assoc, use_container_width=True, hide_index=True)
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    avg_support = np.mean([info['support'] for _, info in associations_2.items()])
                    st.metric("Ortalama Support", f"%{avg_support * 100:.2f}")
               
    elif page == "🎯 Üçlü Kombinasyonlar":
        st.header("🎯 Üçlü Oyun Kombinasyonları")
        
        col1, col2 = st.columns([1, 3])
        
        with col1:
            st.subheader("Parametreler")
            
            min_support_3 = st.slider(
                "Minimum Support (%):",
                min_value=1,
                max_value=15,
                value=3,
                step=1
            ) / 100
            
            show_top_n_3 = st.slider("Gösterilecek kombinasyon sayısı:", 10, 30, 15)
        
        with col2:
            with st.spinner("3'lü kombinasyonlar hesaplanıyor..."):
                _, associations_3 = calculate_associations(player_libraries, min_support_3)
            
            if associations_3:
                st.success(f"✅ {len(associations_3)} üçlü kombinasyon bulundu!")
                
                sorted_assoc_3 = sorted(associations_3.items(), 
                                       key=lambda x: x[1]['support'], reverse=True)
                
                top_assoc_3 = sorted_assoc_3[:show_top_n_3]
                
                st.subheader("🔥 En Güçlü Üçlü Kombinasyonlar")
                
                for i, (triple, info) in enumerate(top_assoc_3, 1):
                    game1, game2, game3 = triple
                    
                    with st.container():
                        col_rank, col_games, col_stats = st.columns([0.5, 3, 1.5])
                        
                        with col_rank:
                            st.markdown(f"### {i}")
                        
                        with col_games:
                            st.markdown(f"**🎮 {game1}**")
                            st.markdown(f"**🎮 {game2}**")
                            st.markdown(f"**🎮 {game3}**")
                        
                        with col_stats:
                            st.metric("Oyuncu", info['count'])
                            st.metric("Support", f"%{info['support'] * 100:.2f}")
                        
                        st.markdown("---")
                
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    avg_support = np.mean([info['support'] for _, info in associations_3.items()])
                    st.metric("Ort. Support", f"%{avg_support * 100:.2f}")
                with col2:
                    max_count = max([info['count'] for _, info in associations_3.items()])
                    st.metric("Max Oyuncu", max_count)
                with col3:
                    st.metric("Toplam Kombinasyon", len(associations_3))
                with col4:
                    min_count = min([info['count'] for _, info in associations_3.items()])
                    st.metric("Min Oyuncu", min_count)
                
                st.subheader("📊 Kombinasyon Dağılımı")
                
                bubble_data = []
                for triple, info in top_assoc_3:
                    bubble_data.append({
                        'Kombinasyon': f"{triple[0][:10]}+{triple[1][:10]}+{triple[2][:10]}",
                        'Oyuncu': info['count'],
                        'Support': info['support'] * 100,
                        'Tam İsim': f"{triple[0]} + {triple[1]} + {triple[2]}"
                    })
                
                df_bubble = pd.DataFrame(bubble_data)
                fig = px.scatter(
                    df_bubble,
                    x='Support',
                    y='Oyuncu',
                    size='Oyuncu',
                    hover_data=['Tam İsim'],
                    title='Üçlü Kombinasyonlar - Support vs Oyuncu Sayısı'
                )
                st.plotly_chart(fig, use_container_width=True)
            
            else:
                st.warning("❌ Hiç 3'lü kombinasyon bulunamadı. Support değerini düşürmeyi deneyin.")
            
    elif page == "📋 Association Rules":
        st.header("📋 Association Rules (Birliktelik Kuralları)")
        
        col1, col2 = st.columns([1, 3])
        
        with col1:
            st.subheader("Parametreler")
            
            min_support_rule = st.slider(
                "Minimum Support (%):",
                min_value=2,
                max_value=15,
                value=5,
                step=1
            ) / 100
            
            min_confidence = st.slider(
                "Minimum Confidence (%):",
                min_value=10,
                max_value=90,
                value=30,
                step=5,
                help="Kuralın geçerli sayılması için minimum güven yüzdesi"
            ) / 100
            
            min_lift = st.slider(
                "Minimum Lift:",
                min_value=1.0,
                max_value=5.0,
                value=1.0,
                step=0.1,
                help="Lift > 1 pozitif ilişki gösterir"
            )
            
            show_top_rules = st.slider("Gösterilecek kural sayısı:", 10, 50, 20)
            
            rule_type_filter = st.multiselect(
                "Kural tipi:",
                ["2-game","3-game"],
                default=["2-game" ]
            )
        
        with col2:
            with st.spinner("Kurallar oluşturuluyor..."):
                associations_2,_ = calculate_associations(player_libraries, min_support_rule)
                
                if associations_2:
                    rules = generate_rules(associations_2, game_counts, 
                                         len(player_libraries), min_confidence)
                    
                    filtered_rules = [
                        r for r in rules 
                        if r['lift'] >= min_lift and r['type'] in rule_type_filter
                    ]
                    
                    if filtered_rules:
                        st.success(f"✅ {len(filtered_rules)} kural bulundu!")
                        
                        top_rules = filtered_rules[:show_top_rules]
                        
                        st.subheader("💎 En Güçlü Kurallar")
                        
                        table_data = []
                        for i, rule in enumerate(top_rules, 1):
                            table_data.append({
                                'No': i,
                                'Öncül': rule['antecedent'],
                                '→': '→',
                                'Sonuç': rule['consequent'],
                                'Support': f"%{rule['support'] * 100:.2f}",
                                'Confidence': f"%{rule['confidence'] * 100:.1f}",
                                'Lift': f"{rule['lift']:.2f}",
                                'Tip': rule['type']
                            })
                        
                        df_rules = pd.DataFrame(table_data)
                        st.dataframe(df_rules, use_container_width=True, hide_index=True)
                        
                        st.subheader("📖 Detaylı Kural Açıklamaları")
                        
                        for i, rule in enumerate(top_rules[:3], 1):
                            with st.expander(f"🔍 Kural {i}: {rule['antecedent']} → {rule['consequent']}", expanded=(i==1)):
                                col1, col2, col3 = st.columns(3)
                                
                                with col1:
                                    st.metric("Support", f"%{rule['support'] * 100:.2f}")
                                    st.caption("Bu kombinasyonun genel yaygınlığı")
                                
                                with col2:
                                    st.metric("Confidence", f"%{rule['confidence'] * 100:.1f}")
                                    st.caption("Öncülü oynayan birinin sonucu oynama olasılığı")
                                
                                with col3:
                                    st.metric("Lift", f"{rule['lift']:.2f}")
                                    st.caption("Tesadüften ne kadar güçlü")
                                
                                st.markdown("---")
                                st.markdown("**💡 Yorumlama:**")
                                st.write(f"'{rule['antecedent']}' oynayan oyuncuların **%{rule['confidence']*100:.0f}'i** "
                                       f"'{rule['consequent']}' de oynuyor.")
                                st.write(f"Bu ilişki tesadüften **{rule['lift']:.1f} kat** daha güçlü.")
                                
                                if rule['lift'] > 3:
                                    st.success("🔥 Çok güçlü bir birliktelik!")
                                elif rule['lift'] > 2:
                                    st.info("💪 Güçlü bir birliktelik!")
                                else:
                                    st.warning("⚠️ Orta düzeyde bir birliktelik")
                        
                        st.subheader("📈 Kural İstatistikleri")
                        col1, col2, col3, col4 = st.columns(4)
                        
                        with col1:
                            avg_conf = np.mean([r['confidence'] for r in filtered_rules])
                            st.metric("Ort. Confidence", f"%{avg_conf * 100:.1f}")
                        
                        with col2:
                            avg_lift = np.mean([r['lift'] for r in filtered_rules])
                            st.metric("Ort. Lift", f"{avg_lift:.2f}")
                        
                        with col3:
                            strong_rules = len([r for r in filtered_rules if r['lift'] > 2])
                            st.metric("Güçlü Kurallar", strong_rules)
                        
                        with col4:
                            rules_3 = len([r for r in filtered_rules if r['type'] == '3-game'])
                            st.metric("3'lü Kurallar", rules_3)
                    
                    else:
                        st.warning("❌ Filtrelere uygun kural bulunamadı. Parametreleri ayarlayın.")
                else:
                    st.error("❌ Kural oluşturmak için önce birliktelik analizi gerekli.")
    
    elif page == "🎮 Kişisel Öneri Sistemi":
        st.header("🎮 Kişiselleştirilmiş Oyun Önerisi")
        
        st.markdown("""
        Bu sayfada kendi oyun kütüphanenizi oluşturabilir ve size özel oyun önerileri alabilirsiniz!
        """)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("📚 Kütüphanenizi Oluşturun")
            
            all_games = sorted(game_counts.keys())
            
            selected_games = st.multiselect(
                "Sahip olduğunuz oyunları seçin:",
                options=all_games,
                default=[],
                help="En az 2 oyun seçmeniz önerilir"
            )
            
            if selected_games:
                st.success(f"✅ {len(selected_games)} oyun seçtiniz")
                
                st.markdown("**Kütüphaneniz:**")
                cols = st.columns(3)
                for i, game in enumerate(selected_games):
                    with cols[i % 3]:
                        st.markdown(f"✓ {game}")
        
        with col2:
            st.subheader("⚙️ Öneri Ayarları")
            
            num_recommendations = st.slider(
                "Öneri sayısı:",
                min_value=3,
                max_value=15,
                value=8
            )
            
            rec_min_confidence = st.slider(
                "Min Confidence (%):",
                min_value=20,
                max_value=80,
                value=30
            ) / 100
        
        if st.button("🎯 Öneri Al", type="primary", use_container_width=True):
            if len(selected_games) < 2:
                st.warning("⚠️ Lütfen en az 2 oyun seçin!")
            else:
                with st.spinner("Öneriler hesaplanıyor..."):

                    associations_2,_ = calculate_associations(player_libraries, 0.03)
                    rules = generate_rules(associations_2, game_counts, 
                                         len(player_libraries), rec_min_confidence)
                    
                    recommendations = {}
                    
                    for rule in rules:
                        if rule['type'] == '2-game':
                            if rule['antecedent'] in selected_games and rule['consequent'] not in selected_games:
                                game = rule['consequent']
                                score = rule['confidence'] * rule['lift']
                                
                                if game not in recommendations:
                                    recommendations[game] = {
                                        'score': 0,
                                        'reasons': []
                                    }
                                
                                recommendations[game]['score'] += score
                                recommendations[game]['reasons'].append({
                                    'from': rule['antecedent'],
                                    'confidence': rule['confidence'],
                                    'lift': rule['lift']
                                })
                    
                    if recommendations:
                        sorted_recs = sorted(recommendations.items(), 
                                           key=lambda x: x[1]['score'], reverse=True)
                        
                        st.success(f"🌟 Sizin için {len(sorted_recs)} öneri bulundu!")
                        
                        st.markdown("---")
                        st.subheader("🎯 Size Özel Oyun Önerileri")
                        
                        for i, (game, data) in enumerate(sorted_recs[:num_recommendations], 1):
                            with st.container():
                                col1, col2, col3 = st.columns([0.5, 3, 1.5])
                                
                                with col1:
                                    st.markdown(f"### {i}")
                                
                                with col2:
                                    st.markdown(f"### 🎮 {game}")
                                    
                                    best_reason = max(data['reasons'], key=lambda x: x['confidence'])
                                    st.markdown(f"**Çünkü:** '{best_reason['from']}' oynadınız")
                                    st.caption(f"Bu oyuncuların %{best_reason['confidence']*100:.0f}'i '{game}' de oynuyor")
                                    
                                    if metadata is not None:
                                        game_info = metadata[metadata['Game'] == game]
                                        if not game_info.empty:
                                            genre = game_info.iloc[0]['Genre']
                                            st.markdown(f"**Tür:** {genre} ")
                                
                                with col3:
                                    st.metric("Öneri Gücü", f"{data['score']:.2f}")
                                    st.metric("Lift", f"{best_reason['lift']:.2f}x")
                                    
                                    if best_reason['lift'] > 3:
                                        st.success("🔥 Çok Güçlü")
                                    elif best_reason['lift'] > 2:
                                        st.info("💪 Güçlü")
                                    else:
                                        st.warning("⚡ Orta")
                                
                                st.markdown("---")
                    else:
                        st.warning("❌ Kütüphaneniz için öneri bulunamadı. Daha popüler oyunlar eklemeyi deneyin.")
    
    elif page == "🎨 Genre Analizi":
        st.header("🎨 Oyun Türü Analizi")
        
        if metadata is None:
            st.error("❌ Bu analiz için metadata dosyası gerekli!")
        else:
            tab1, tab2, tab3 = st.tabs(["Genre Dağılımı", "Genre Birliktelikleri", "Genre Bazlı Öneriler"])
            
            with tab1:
                st.subheader("🎯 Genre Popülaritesi")
                
                genre_players = {}
                for library in player_libraries:
                    genres_in_lib = set()
                    for game in library:
                        game_info = metadata[metadata['Game'] == game]
                        if not game_info.empty:
                            genre = game_info.iloc[0]['Genre']
                            genres_in_lib.add(genre)
                    
                    for genre in genres_in_lib:
                        genre_players[genre] = genre_players.get(genre, 0) + 1
                
                sorted_genres = sorted(genre_players.items(), key=lambda x: x[1], reverse=True)
                
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    genres = [g for g, _ in sorted_genres]
                    counts = [c for _, c in sorted_genres]
                    
                    fig = px.bar(
                        x=counts,
                        y=genres,
                        orientation='h',
                        title='Genre Bazlı Oyuncu Dağılımı',
                        labels={'x': 'Oyuncu Sayısı', 'y': 'Tür'},
                        color=counts,
                        color_continuous_scale='viridis'
                    )
                    fig.update_layout(height=500)
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    st.markdown("**📋 Detaylı Liste**")
                    for i, (genre, count) in enumerate(sorted_genres, 1):
                        percentage = (count / len(player_libraries)) * 100
                        st.write(f"{i}. **{genre}**")
                        st.progress(percentage / 100)
                        st.caption(f"{count} oyuncu (%{percentage:.1f})")
            
            with tab2:
                st.subheader("🔗 Genre Birliktelikleri")
                
                genre_pairs = {}
                
                for library in player_libraries:
                    genres = []
                    for game in library:
                        game_info = metadata[metadata['Game'] == game]
                        if not game_info.empty:
                            genres.append(game_info.iloc[0]['Genre'])
                    
                    unique_genres = list(set(genres))
                    if len(unique_genres) >= 2:
                        for g1, g2 in combinations(sorted(unique_genres), 2):
                            pair = (g1, g2)
                            genre_pairs[pair] = genre_pairs.get(pair, 0) + 1
                
                sorted_pairs = sorted(genre_pairs.items(), key=lambda x: x[1], reverse=True)
                
                if sorted_pairs:
                    top_pairs = sorted_pairs[:15]
                    
                    pair_labels = [f"{g1} + {g2}" for (g1, g2), _ in top_pairs]
                    pair_counts = [c for _, c in top_pairs]
                    
                    fig = px.bar(
                        x=pair_counts,
                        y=pair_labels,
                        orientation='h',
                        title='En Çok Birlikte Oynanan Genre Çiftleri',
                        labels={'x': 'Oyuncu Sayısı', 'y': 'Genre Çiftleri'},
                        color=pair_counts,
                        color_continuous_scale='plasma'
                    )
                    fig.update_layout(height=500)
                    st.plotly_chart(fig, use_container_width=True)
                    
                    st.markdown("**📊 Detaylı Birliktelik Tablosu**")
                    table_data = []
                    for i, ((g1, g2), count) in enumerate(top_pairs, 1):
                        percentage = (count / len(player_libraries)) * 100
                        table_data.append({
                            'Sıra': i,
                            'Genre 1': g1,
                            'Genre 2': g2,
                            'Oyuncu': count,
                            'Yüzde': f"%{percentage:.1f}"
                        })
                    
                    df_pairs = pd.DataFrame(table_data)
                    st.dataframe(df_pairs, use_container_width=True, hide_index=True)
            
            with tab3:
                st.subheader("🎯 Genre Bazlı Oyun Önerileri")
                
                selected_genre = st.selectbox(
                    "Bir tür seçin:",
                    options=sorted(metadata['Genre'].unique())
                )
                
                if selected_genre:
                    genre_games = metadata[metadata['Genre'] == selected_genre]['Game'].tolist()
                    
                    st.markdown(f"**🎮 {selected_genre} Türündeki Oyunlar ({len(genre_games)} adet)**")
                    
                    genre_game_counts = {g: game_counts.get(g, 0) for g in genre_games}
                    sorted_genre_games = sorted(genre_game_counts.items(), 
                                               key=lambda x: x[1], reverse=True)
                    
                    cols = st.columns(2)
                    for i, (game, count) in enumerate(sorted_genre_games[:10]):
                        with cols[i % 2]:
                            percentage = (count / len(player_libraries)) * 100
                            st.markdown(f"**{i+1}. {game}**")
                            st.progress(percentage / 100)
                            st.caption(f"{count} oyuncu (%{percentage:.1f})")

else:
    st.error("❌ Veri dosyaları yüklenemedi!")
    st.info("Lütfen 'steam_libraries.csv' dosyasının doğru konumda olduğundan emin olun.")
