import pandas as pd
import geopandas
import streamlit as st
import numpy as np
import folium
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster
import plotly.express as px
from datetime import datetime


st.set_page_config(layout='wide')
@st.cache(allow_output_mutation= True)

def get_data(path):
    data = pd.read_csv(path,sep =';')
    col = ['price']
    data[col] = data[col].apply(lambda x: x.str.replace(',', '.').astype('float'))
    data['date'] = pd.to_datetime(data["date"])
    return data

@st.cache( allow_output_mutation= True)
def get_geofile(url):
    geofile = geopandas.read_file(url)

    return geofile
@st.cache( allow_output_mutation= True)
def filter_data(data,f_date):
    f_date = datetime.strptime(f_date, '%Y-%m-%d')
    data['date'] = pd.to_datetime(data["date"])
    df = data.loc[data['date']<pd.Timestamp(f_date).to_pydatetime()]
    df = df[['date','price']].groupby('date').mean().reset_index()
    return df
def set_feature(data):
    # add new features
    data['price_m2'] = data['price'] / data['sqft_lot']
    return data
def overview_data(data):

    f_attributes = st.sidebar.multiselect("Enter columns", data.columns)
    f_zipcode = st.sidebar.multiselect("Enter zipcode", data['zipcode'].unique())
    st.title("Data Overview")
    # atributos = selecionar a coluna
    # zipcode= selecionar a linha
    # 0 + 0 =retorna o dataset original
    if (f_zipcode != []) & (f_attributes != []):
        data = data.loc[data['zipcode'].isin(f_zipcode), f_attributes]
    elif (f_zipcode != []) & (f_attributes == []):
        data = data.loc[data['zipcode'].isin(f_zipcode), :]
    elif (f_zipcode == []) & (f_attributes != []):
        data = data.loc[:, f_attributes]
    else:
        data = data.copy()

    st.dataframe(data, height=400)
    c1, c2 = st.columns((2, 1))

    df1 = data[['id', 'zipcode']].groupby('zipcode').count().reset_index()
    df2 = data[['price', 'zipcode']].groupby('zipcode').mean().reset_index()
    df3 = data[['sqft_living', 'zipcode']].groupby('zipcode').mean().reset_index()
    df4 = data[['price_m2', 'zipcode']].groupby('zipcode').mean().reset_index()
    # merge(juntar)

    m1 = pd.merge(df1, df2, on='zipcode', how='inner')
    m2 = pd.merge(m1, df3, on='zipcode', how='inner')
    df = pd.merge(m2, df4, on='zipcode', how='inner')
    # renomear as colunas:
    df.columns = ['Zipcode', 'Total Houses', 'Price', 'SQRT LIVING', 'Price/m2']

    c1.header("Average metrics")
    c1.dataframe(df, height=600)
    num_attributes = data.select_dtypes(include=['int64', 'float64'])

    media = pd.DataFrame(num_attributes.apply(np.mean))
    mediana = pd.DataFrame(num_attributes.apply(np.median))
    std = pd.DataFrame(num_attributes.apply(np.std))

    max_ = pd.DataFrame(num_attributes.apply(np.max))
    min_ = pd.DataFrame(num_attributes.apply(np.min))

    df6 = pd.concat([max_, min_, media, mediana, std], axis=1)
    df6.columns = ['attributes', 'max', 'mean', 'median', 'desvio']

    c2.header("Descriptive Statistic")
    c2.dataframe(df6, height=400)
    return None
def portfolio_density(data,geofile):
    st.title("Region Overview")
    c1, c2 = st.columns((1, 1))
    data.loc[data['lat'] > 100.00, 'lat'] = data['lat'] / 10
    df = data.sample(1000)
    c1.header("Portfolio Density")
    # Base Map - folium
    density_map = folium.Map(location=[data['lat'].mean(), data['long'].mean()], default_zoom_start=15)

    marker_cluster = MarkerCluster().add_to(density_map)
    for name, row in df.iterrows():
        folium.Marker([row['lat'], row['long']], popup='Price R$:{0}. Features:{1} bedrooms,{2} bathrooms,'
                                                       'year built:{3}'.format(row['price'],
                                                                               row['bedrooms'], row['bathrooms'],
                                                                               row['yr_built'])).add_to(marker_cluster)
    with c1:
        folium_static(density_map)

    # ==================
    # Region Price Map
    # ==================
    c2.header('Price Density')

    df = data[['price', 'zipcode']].groupby('zipcode').mean().reset_index()
    df.columns = ['ZIP', 'PRICE']

    df = df.sample(10)
    geofile = geofile[geofile['ZIP'].isin(df['ZIP'].tolist())]
    region_price_map = folium.Map(location=[data['lat'].mean(), data['long'].mean()], default_zoom_start=15)

    region_price_map.choropleth(data=df, geo_data=geofile, columns=['ZIP', 'PRICE'], key_on='feature.properties.ZIP',
                                fill_color='YlOrRd', fill_opacity=0.7)
    with c2:
        folium_static(region_price_map)

    return None
def attributes_distribution(data):
    st.sidebar.title('Attributes Options')
    st.title("House Attributes")

    # filters
    f_bedrooms = st.sidebar.selectbox('Max number of bedrooms', sorted(set(data['bedrooms'].unique())))
    bath = st.sidebar.selectbox('Max number of bathrooms', sorted(set(data['bathrooms'].unique())))
    # House per bedrooms
    df = data[data['bedrooms'] <= f_bedrooms]
    fig = px.histogram(df, x='bedrooms', nbins=19)
    st.plotly_chart(fig, use_container_width=True)

    # House per bethrooms
    df1 = data[data['bathrooms'] <= bath]
    fig = px.histogram(data, x='bathrooms', nbins=19)
    st.plotly_chart(fig, use_container_width=True)

    return None



if __name__ == '__main__':
    #data extraction:
    #get data
    path = 'kc_house_data.csv'
    data = get_data(path)

    #get geofile
    url = 'https://opendata.arcgis.com/datasets/83fc2e72903343aabff6de8cb445b81c_2.geojson'
    geofile = get_geofile(url)

    #transformation
    data =set_feature(data)

    overview_data(data)

    portfolio_density(data,geofile)

    attributes_distribution(data)










# ====================
#Statistic Descriptive
# ====================


# st.write(f_attributes)
# st.write(f_zipcode)
#
# st.write(data.head())
#=======================
# Densidade de portfólio
#========================

#==================
#Histogramas
#==================


