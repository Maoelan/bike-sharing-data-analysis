import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Load the dataset
day_df = pd.read_csv('data_final.csv')

# Set the theme for seaborn
sns.set_theme(style="white")
palette = sns.color_palette("Blues_d", n_colors=4)

# Dashboard title
st.title('Bike Rentals Analysis Dashboard')

# Sidebar selection for years
years = st.sidebar.selectbox('Select Year(s) to Display:', ('Both', '2011', '2012'))

# Filter data based on selection
if years == '2011':
    filtered_df = day_df[day_df['yr'] == 0]  # Assuming 'yr' is 0 for 2011
elif years == '2012':
    filtered_df = day_df[day_df['yr'] == 1]  # Assuming 'yr' is 1 for 2012
else:
    filtered_df = day_df

# Monthly Average Rentals
monthly_avg = filtered_df.groupby(['yr', 'mnth'])['cnt'].mean().reset_index()

# Monthly Average Rentals Plot
st.subheader('Pertanyaan 1:  Bagaimana pola penyewaan sepeda berdasarkan bulan pada tahun 2011 dan 2012?')
st.subheader('Average Bike Rentals per Month')
plt.figure(figsize=(12, 6))
plot = sns.lineplot(data=monthly_avg, x='mnth', y='cnt', hue='yr', marker='o', palette=palette)
plt.title('Average Bike Rentals per Month')
plt.xlabel('Month')
plt.ylabel('Average Rentals')
plt.xticks(ticks=np.arange(1, 13), labels=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
handles, labels = plt.gca().get_legend_handles_labels()
new_labels = ['2011', '2012']
plt.legend(handles=handles, labels=new_labels, title='Year')
plt.grid(True)
plt.tight_layout()
st.pyplot(plt)

# Insights based on Monthly Rentals
st.markdown("""
**Insights:**
- Secara keseluruhan, jumlah penyewaan sepeda mengalami peningkatan dari tahun 2011 ke 2012, menunjukkan peningkatan minat terhadap penggunaan sepeda.
- Terdapat pola musiman yang jelas, dengan penyewaan lebih tinggi pada bulan-bulan hangat (Maret hingga Agustus).
- Titik terendah penyewaan terjadi pada bulan Januari, sementara titik tertinggi terjadi pada bulan Juni (2011) dan September (2012).
""")

# Weather Statistics
weathersit_map = {
    1: 'Clear',
    2: 'Cloudy',
    3: 'Rain/Snow',
}

weather_stats = filtered_df.groupby('weathersit')['cnt'].mean().reset_index()
weather_stats['weathersit'] = weather_stats['weathersit'].map(weathersit_map)

# Weather Condition Plot
st.subheader('Pertanyaan 2: Apa efek dari berbagai kondisi cuaca terhadap jumlah penyewaan sepeda?')
st.subheader('Average Rentals Based on Weather Conditions')
plt.figure(figsize=(12, 6))
sns.barplot(data=weather_stats, x='weathersit', y='cnt', color='#619eff')
plt.title('Average Rentals Based on Weather Conditions')
plt.xlabel('Weather Condition')
plt.ylabel('Average Rentals')
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
st.pyplot(plt)

# Insights based on Weather Conditions
st.markdown("""
**Insights:**
- Cuaca cerah (Clear) berpengaruh besar pada jumlah penyewaan, jauh lebih tinggi dibanding kondisi lainnya.
- Cuaca berawan (Cloudy) sedikit mengurangi minat penyewaan, tetapi masih cukup mendukung.
- Cuaca hujan/salju (Rain/Snow) menyebabkan penurunan signifikan dalam penyewaan sepeda.
""")

# Holiday Statistics
holiday_map = {0: 'Working Day', 1: 'Holiday'}
holiday_stats = filtered_df.groupby('holiday')['cnt'].mean().reset_index()
holiday_stats['holiday'] = holiday_stats['holiday'].map(holiday_map)

# Rentals on Holidays vs. Working Days Plot
st.subheader('Pertanyaan 3: Apakah hari libur dan hari kerja mempengaruhi penyewaan sepeda?')
st.subheader('Average Rentals on Holidays and Working Days')
plt.figure(figsize=(12, 6))
sns.barplot(data=holiday_stats, x='holiday', y='cnt', color="#619eff")
plt.title('Average Rentals on Holidays and Working Days')
plt.xlabel('Working Day / Holiday')
plt.ylabel('Average Rentals')
plt.xticks(rotation=0)
plt.grid(True)
plt.tight_layout()
st.pyplot(plt)

# Insights based on Holidays
st.markdown("""
**Insights:**
- Hari kerja lebih dominan dalam penyewaan sepeda dibanding hari libur.
- Perbedaan rata-rata penyewaan pada hari kerja dan hari libur cukup signifikan, menunjukkan pengaruh lebih besar dari hari kerja.
""")

# Rental Category Analysis
def categorize_rentals(cnt):
    if cnt < 2000:
        return 'Low'
    elif 2000 <= cnt < 4000:
        return 'Medium'
    else:
        return 'High'

filtered_df['rental_category'] = filtered_df['cnt'].apply(categorize_rentals)
category_order = ['High', 'Medium', 'Low']
filtered_df['rental_category'] = pd.Categorical(filtered_df['rental_category'], categories=category_order, ordered=True)

# Statistics of Rentals by Category Plot
st.subheader("Analisis Lanjutan (Clustering)")
st.subheader("Kategori Penyewaan Sepeda Berdasarkan Jumlah Total Penyewaan")
plt.figure(figsize=(12, 6))
sns.countplot(x='rental_category', data=filtered_df, color="#619eff")
plt.title('Distribution of Bike Rentals by Category', fontsize=14)
plt.xlabel('Rental Category', fontsize=12)
plt.ylabel('Count', fontsize=12)
plt.grid(True)
plt.tight_layout()
st.pyplot(plt)

# Insights based on Rental Categories
st.markdown("""
**Insights:**
- Kategori **High** menunjukkan dominasi jelas dengan 408 penyewaan rata-rata 5595.
- **Variasi dalam Kategori High**: Rentang nilai penyewaan berkisar dari 4010 hingga 8173, menunjukkan variasi preferensi pelanggan.
- **Kategori Medium**: Jumlah penyewaan sebanyak 181 dengan rata-rata 3108, menunjukkan permintaan signifikan.
- **Kategori Low**: Hanya 98 penyewaan dengan rata-rata 1398, menunjukkan aktivitas penyewaan yang jarang terjadi.
""")
