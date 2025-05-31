import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import glob
import os
import urllib
import datetime


def download_data(province_id, year1=1981, year2=2024):
    data_folder = 'data'
    os.makedirs(data_folder, exist_ok=True)
    url = f"https://www.star.nesdis.noaa.gov/smcd/emb/vci/VH/get_TS_admin.php?country=UKR&provinceID={province_id}&year1={year1}&year2={year2}&type=Mean"
    vhi_url = urllib.request.urlopen(url)
    current_datetime = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M')
    filename = f'vhi_id__{province_id}__{current_datetime}.csv'
    file_path = os.path.join(data_folder, filename)
    with open(file_path, 'wb') as out:
        out.write(vhi_url.read())

# Чтение и очистка файлов
def create_data_frame(folder_path):
    csv_files = glob.glob(folder_path + "/*.csv")
    headers = ['Year', 'Week', 'SMN', 'SMT', 'VCI', 'TCI', 'VHI', 'empty']
    frames = []
    for file in csv_files:
        region_id = int(file.split('__')[1])
        # skiprows=[0] — пропускаем строку с "<pre>"
        df = pd.read_csv(file, header=1, names=headers, skiprows=[0])
        df = df.drop(df.index[-1])
        df = df.drop(df.loc[df['VHI'] == -1].index)
        df = df.drop('empty', axis=1)
        df.insert(0, 'region_id', region_id, True)
        df['Week'] = df['Week'].astype(int)
        df['Year'] = df['Year'].astype(int)
        frames.append(df)
    result = pd.concat(frames).drop_duplicates().reset_index(drop=True)
    result = result.loc[(result.region_id != 12) & (result.region_id != 20)]
    return result

df = create_data_frame('./data')

reg_id_name = {
    1: 'Вінницька', 2: 'Волинська', 3: 'Дніпропетровська', 4: 'Донецька', 5: 'Житомирська',
    6: 'Закарпатська', 7: 'Запорізька', 8: 'Івано-Франківська', 9: 'Київська', 10: 'Кіровоградська',
    11: 'Луганська', 13: 'Миколаївська', 14: 'Одеська', 15: 'Полтавська', 16: 'Рівненська',
    17: 'Сумська', 18: 'Тернопільська', 19: 'Харківська', 21: 'Хмельницька', 22: 'Черкаська',
    23: 'Чернівецька', 24: 'Чернігівська'
}

st.title("Аналіз індексів VCI, TCI, VHI")

index_option = st.selectbox("Виберіть індекс:", ['VCI', 'TCI', 'VHI'])
region_option = st.selectbox("Виберіть область:", list(reg_id_name.values()))
year_range = st.slider("Роки:", 1981, 2024, (2000, 2024))
week_range = st.slider("Тижні:", 1, 52, (1, 52))

df_filtered = df[
    (df['Year'].between(*year_range)) &
    (df['Week'].between(*week_range)) &
    (df['region_id'] == list(reg_id_name.keys())[list(reg_id_name.values()).index(region_option)])
]

st.write("Відфільтровані дані:")
st.dataframe(df_filtered)

fig, ax = plt.subplots()
sns.lineplot(data=df_filtered, x='Week', y=index_option, ax=ax)
st.pyplot(fig)
