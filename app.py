#import os
#import re
import time
import pandas as pd
import numpy as np
import streamlit as st
from FeaturesTransformer import FeaturesTransformer

st.set_page_config(
     page_title='PREDICTION SALE PRICE',
     layout="wide",
     initial_sidebar_state="expanded",
)

st.title('Демонстрационное приложение рассчета цены объекта недвижимости')
st.sidebar.header('Объект недвижимости:')

o = FeaturesTransformer()

form = st.sidebar.form(key='raw_X')

BOROUGH = ''#form.selectbox('BOROUGH:', o.category_dictionary['BOROUGH'], help='округ')
NEIGHBORHOOD = form.selectbox('NEIGHBORHOOD:', o.category_dictionary['NEIGHBORHOOD'],  help='район')
BUILDING_CLASS_CATEGORY = form.selectbox('BUILDING CLASS CATEGORY:',
                                         o.category_dictionary['BUILDING CLASS CATEGORY'],
                                         help='категория недвижимости')

#ZIP_CODE = form.selectbox('ZIP CODE:', o.category_dictionary['ZIP CODE'], help='почтовый индекс')
ZIP_CODE_filtered = (o.cat_intersections[o.cat_intersections['NEIGHBORHOOD'] == NEIGHBORHOOD]['ZIP CODE'].unique())
ZIP_CODE = form.selectbox('ZIP CODE:',
                          [str(x) for x in ZIP_CODE_filtered],
#                          o.cat_intersections[o.cat_intersections['NEIGHBORHOOD'] == NEIGHBORHOOD]['ZIP CODE'],
                          help='почтовый индекс')

ADDRESS = ''#form.text_input(label='ADDRESS:', value='870 7 AVENUE', help="адрес в формате: '870 7 AVENUE'")
LAND_SQUARE_FEET = form.number_input(label='LAND SQUARE FEET:',
                                     min_value=50,
                                     max_value=10000,
                                     value=2500,
                                     step=1,
                                     help='площадь в кв. футах')
GROSS_SQUARE_FEET = form.number_input(label='GROSS SQUARE FEET:',
                                      min_value=50,
                                      max_value=10000,
                                      value=1680,
                                      step=1,
                                      help='площадь в кв. футах')
YEAR_BUILT = form.slider(label='YEAR BUILT:',
                         min_value=1850,
                         max_value=2019,
                         value=1980,
                         step=1,
                         help='год постройки дома')

submitted = form.form_submit_button("Рассчитать цену")    

raw_X = [BOROUGH, NEIGHBORHOOD, BUILDING_CLASS_CATEGORY, ZIP_CODE, ADDRESS, LAND_SQUARE_FEET, GROSS_SQUARE_FEET, YEAR_BUILT]
o.raw_X_to_df(raw_X)

if not submitted:
    warning_mess = st.info('Введите данные объекта недвижимости на боковой панели и нажмите **Рассчитать цену**')
else:
    with st.spinner(text='Выполнение...'):
        time.sleep(1)
    my_table = st.table(o.df[o.features_columns])
    st.markdown(f'### PREDICTION SALE PRICE: `{o.predict_sale_price()}`')
