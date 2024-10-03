import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

@st.cache_data
def load_data(file_path):
    return pd.read_csv(file_path)

day_df = load_data('data_final.csv')

sns.set_theme(style="white")
palette = sns.color_palette("Blues_d", n_colors=4)

st.title('Dashboard Analisis Penyewaan Sepedah')

st.sidebar.header('Pilihan')

selected_years = st.sidebar.multiselect('Pilih Tahun', options=[2011, 2012], default=[2011, 2012])
selected_weathers = st.sidebar.multiselect('Pilih Kondisi Cuaca', options=['Clear', 'Cloudy', 'Rain/Snow'], default=['Clear', 'Cloudy', 'Rain/Snow'])
selected_holidays = st.sidebar.multiselect('Pilih Hari Libur/Hari Kerja', options=['Working Day', 'Holiday'], default=['Working Day', 'Holiday'])
selected_rental_categories = st.sidebar.multiselect('Pilih Kategori Rental', options=['High', 'Medium', 'Low'], default=['High', 'Medium', 'Low'])

def filter_data(df):
    if selected_years:
        df = df[df['yr'].isin([0 if year == 2011 else 1 for year in selected_years])]

    if selected_weathers:
        weather_map = {'Clear': 1, 'Cloudy': 2, 'Rain/Snow': 3}
        df = df[df['weathersit'].isin([weather_map[weather] for weather in selected_weathers])]

    if selected_holidays:
        holiday_map = {'Working Day': 0, 'Holiday': 1}
        df = df[df['holiday'].isin([holiday_map[holiday] for holiday in selected_holidays])]

    if selected_rental_categories:
        df = df[df['rental_category'].isin(selected_rental_categories)]
    
    return df

day_df = filter_data(day_df)

if day_df.empty:
    st.write("No data available for the selected filters.")
else:
    monthly_avg = day_df.groupby(['yr', 'mnth'])['cnt'].mean().reset_index()

    st.subheader('Pertanyaan 1: Bagaimana pola penyewaan sepeda berdasarkan bulan pada tahun 2011 dan 2012?')
    st.subheader('Rata-Rata Penyewaan Sepeda per Bulan')
    plt.figure(figsize=(12, 6))
    plot = sns.lineplot(data=monthly_avg, x='mnth', y='cnt', hue='yr', marker='o', palette=palette)
    plt.title('Average Bike Rentals per Month')
    plt.xlabel('Month')
    plt.ylabel('Average Rentals')
    plt.xticks(ticks=np.arange(1, 13), labels=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    plt.legend(title='Year', labels=['2011', '2012'])
    plt.grid(True)
    plt.tight_layout()
    st.pyplot(plt)

    st.markdown(""" 
    **Insights:**
    - Secara keseluruhan, jumlah penyewaan sepeda mengalami peningkatan dari tahun 2011 ke 2012, menunjukkan peningkatan minat terhadap penggunaan sepeda.
    - Terdapat pola musiman yang jelas, dengan penyewaan lebih tinggi pada bulan-bulan hangat (Maret hingga Agustus).
    - Titik terendah penyewaan terjadi pada bulan Januari, sementara titik tertinggi terjadi pada bulan Juni (2011) dan September (2012).
    """)

    weather_stats = day_df.groupby('weathersit')['cnt'].mean().reset_index()
    weather_stats['weathersit'] = weather_stats['weathersit'].map({1: 'Clear', 2: 'Cloudy', 3: 'Rain/Snow'})

    st.subheader('Pertanyaan 2: Apa efek dari berbagai kondisi cuaca terhadap jumlah penyewaan sepeda?')
    st.subheader('Rata-Rata Penyewaan Sepeda Berdasarkan Kondisi Cuaca')
    plt.figure(figsize=(12, 6))
    sns.barplot(data=weather_stats, x='weathersit', y='cnt', color='#619eff')
    plt.title('Average Rentals Based on Weather Conditions')
    plt.xlabel('Weather Condition')
    plt.ylabel('Average Rentals')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    st.pyplot(plt)

    st.markdown(""" 
    **Insights:**
    - Cuaca cerah (Clear) berpengaruh besar pada jumlah penyewaan, jauh lebih tinggi dibanding kondisi lainnya.
    - Cuaca berawan (Cloudy) sedikit mengurangi minat penyewaan, tetapi masih cukup mendukung.
    - Cuaca hujan/salju (Rain/Snow) menyebabkan penurunan signifikan dalam penyewaan sepeda.
    """)

    holiday_stats = day_df.groupby('holiday')['cnt'].mean().reset_index()
    holiday_stats['holiday'] = holiday_stats['holiday'].map({0: 'Working Day', 1: 'Holiday'})

    st.subheader('Pertanyaan 3: Apakah hari libur dan hari kerja mempengaruhi penyewaan sepeda?')
    st.subheader('Rata-Rata Penyewaan Sepeda pada Hari Libur dan Hari Kerja')
    plt.figure(figsize=(12, 6))
    sns.barplot(data=holiday_stats, x='holiday', y='cnt', color="#619eff")
    plt.title('Average Rentals on Holidays and Working Days')
    plt.xlabel('Working Day / Holiday')
    plt.ylabel('Average Rentals')
    plt.xticks(rotation=0)
    plt.grid(True)
    plt.tight_layout()
    st.pyplot(plt)

    st.markdown(""" 
    **Insights:**
    - Hari kerja lebih dominan dalam penyewaan sepeda dibanding hari libur.
    - Perbedaan rata-rata penyewaan pada hari kerja dan hari libur cukup signifikan, menunjukkan pengaruh lebih besar dari hari kerja.
    """)

    def categorize_rentals(cnt):
        if cnt < 2000:
            return 'Low'
        elif 2000 <= cnt < 4000:
            return 'Medium'
        else:
            return 'High'

    day_df['rental_category'] = day_df['cnt'].apply(categorize_rentals)
    category_order = ['High', 'Medium', 'Low']
    day_df['rental_category'] = pd.Categorical(day_df['rental_category'], categories=category_order, ordered=True)

    category_stats = day_df.groupby('rental_category')['cnt'].agg(['count', 'min', 'max', 'mean']).reset_index()

    st.subheader("Analisis Lanjutan (Clustering)")
    st.subheader("Kategori Penyewaan Sepeda Berdasarkan Jumlah Total Penyewaan")
    st.write("Statistik Penyewaan Sepeda Berdasarkan Kategori:")
    st.dataframe(category_stats)

    plt.figure(figsize=(12, 6))

    rental_counts = day_df['rental_category'].value_counts().reindex(selected_rental_categories, fill_value=0)

    sns.barplot(x=rental_counts.index, y=rental_counts.values, color="#619eff")

    plt.title('Distribution of Bike Rentals by Category', fontsize=14)
    plt.xlabel('Rental Category', fontsize=12)
    plt.ylabel('Count', fontsize=12)
    plt.grid(True)
    plt.tight_layout()
    st.pyplot(plt)

    st.markdown(""" 
    **Insights:**
    - Kategori **High** menunjukkan dominasi jelas dengan rata-rata 5595 penyewaan.
    - **Variasi dalam Kategori High**: Rentang nilai penyewaan berkisar dari nilai minimum 4010 hingga maksimum 8173, menunjukkan variasi preferensi pelanggan.
    - **Kategori Medium**: Jumlah penyewaan sebanyak 181 dengan rata-rata 3108, menunjukkan permintaan signifikan.
    - **Kategori Low**: Hanya 98 penyewaan dengan rata-rata 1398, menunjukkan aktivitas penyewaan yang jarang terjadi.
    """)
