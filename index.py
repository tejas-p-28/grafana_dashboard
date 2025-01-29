import requests
import pandas as pd
from geopy.geocoders import GoogleV3
from pandas import json_normalize
import os
import csv
from dotenv import load_dotenv
global api_key
load_dotenv()
api_key = os.getenv('api_key')
import json
import warnings
warnings.filterwarnings('ignore')
from geopy.geocoders import Nominatim     
import pygeohash
import time
import googlemaps





# fetching data from the api hosted
def fetch_data_mwdc(url, auth_token):
    headers = {
        'Authorization' : f'Bearer {auth_token}',
        'Content-Type' : 'application/json'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        return data
    except Exception as e:
        print(f'Error fetching data from api : {e}')
        return None

# fetching data from the api hosted
def fetch_data_tdc(url, auth_token):
    headers = {
        'Authorization' : f'Bearer {auth_token}',
        'Content-Type' : 'application/json'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        disease = response.json()
        return disease
    except Exception as e:
        print(f'Error fetching data from api : {e}')
        return None
    
# fetching data from the api hosted
def fetch_data_pwc(url, auth_token):
    headers = {
        'Authorization' : f'Bearer {auth_token}',
        'Content-Type' : 'application/json'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        patient = response.json()
        return patient
    except Exception as e:
        print(f'Error fetching data from api : {e}')
        return None

geolocator = Nominatim(user_agent='geoapi')
api_key = os.getenv('api_key')
gmaps = googlemaps.Client(key=api_key)
# Function to get latitude, longitude, and geohash
def get_geohash(city, precision=7):
    try:
        result = gmaps.geocode(city)
        if result:
            location = result[0]['geometry']['location']
            return pygeohash.encode(location['lat'], location['lng'], precision=precision)
        else:
            return 'Not available'
    except Exception as e:
        print(f"Error for city '{city}': {e}")
    return None

def preprocessed_data(data):
    df = pd.DataFrame(data)
    df['city'] = df['address'].apply(get_city_from_address)
    df['city'] = df['city'].apply(check_city_null)
    df['state'] = df['city'].apply(get_state_from_city)
    df['state'] = df['state'].apply(check_null_state)
    df['geohash'] = df['city'].apply(get_geohash)
    # df['geohash'] = df['city'].apply(city_to_geohash)
    # print(df.head())
    df = df[['kiosk', 'diseaseWiseMonthCount', 'city', 'state','geohash']]
    # print(df['kiosk'].nunique())
    flattened_data = []
    for _, row in df.iterrows():
        for entry in row['diseaseWiseMonthCount']:
            disease_month = entry['month']
            disease_counts = entry['diseaseWiseCount']
            for disease, count in disease_counts.items():
                flattened_data.append({
                    'kiosk': row['kiosk'],
                    'city': row['city'],
                    'state' : row['state'],
                    'geohash' : row['geohash'],
                    'disease_month' : disease_month,
                    'disease_list': disease,
                    'disease_count': count
                })
    flattened_df = pd.DataFrame(flattened_data)
    flattened_df.isna().sum()
    # print(flattened_df.nunique())
    flattened_df.drop_duplicates(inplace=True)
    flattened_df.dropna().reset_index(drop=True)
    flattened_df = flattened_df.loc[~(flattened_df == 0).any(axis=1)]
    # flattened_df.dropna().reset_index(drop=True)
    # print(flattened_df.nunique())
    # flattened_df.to_csv('monthwise_disease_count.csv')
    file_path = 'E:/scano/scano_analysis automated/monthwise_disease_count.csv'
    append_to_csv(flattened_df, file_path)
    # df.to_csv('E:/scano/scano_analysis automated/all_in_one.csv', encoding='utf-8', index=False)
    # print('data appended successfully')

def total_disease_count(disease):
    tdc = pd.DataFrame(disease)
    tdc.to_csv('E:/scano/scano_analysis automated/testing.csv')
    tdc['city'] = tdc['address'].apply(get_city_from_address)
    tdc['city'] = tdc['city'].apply(check_city_null)
    tdc['state'] = tdc['city'].apply(get_state_from_city)
    tdc['state'] = tdc['state'].apply(check_null_state)
    tdc['geohash'] = tdc['city'].apply(get_geohash)
    tdc = tdc[['kiosk', 'diseaseWiseMonthCount', 'city', 'state','geohash']]
    # print(tdc['kiosk'].unique)
    # print(tdc)
    flattened_disease = []
    for _, row in tdc.iterrows():
        for entry in row['diseaseWiseMonthCount']:
            disease_counts = entry['diseaseWiseCount']
            for diseases, count in disease_counts.items():
                flattened_disease.append({
                    'kiosk': row['kiosk'],
                    'city': row['city'],
                    'state': row['state'],
                    'geohash' : row['geohash'],
                    'disease_list': diseases,
                    'disease_count': count
                })
              


    # l

    # print(flattened_disease)
    # print(flattened_disease.columns)
    # print(flattened_disease['kiosk'].nunique())


    flattened_disease = pd.DataFrame(flattened_disease)
    tdc = pd.DataFrame(flattened_disease)
    tdc.dropna().reset_index(drop=True)
    # print(tdc.columns)
    # print(tdc['kiosk'].nunique())
    # tdc.duplicated().sum()  
    tdc['disease_list'] = tdc['disease_list'].replace({'FILLINGS': 'FILLING','INFLAMMED / RED GUMS': 'INFLAMMED / RED GUM'})
    tdc_sum = tdc.groupby(['kiosk','disease_list'])['disease_count'].sum().reset_index()
    tdc_sum = pd.DataFrame(tdc_sum)
    # print(tdc_sum.head())
    merged_tdc = tdc.merge(tdc_sum, on=['kiosk'], how='left')
    print(merged_tdc.columns)
    # print(merged_tdc.head())
    # print(merged_tdc['kiosk'].nunique())
    merged_tdc.rename(columns={'disease_list_y': 'disease_list', 'disease_count_y': 'disease_count'}, inplace=True)
    merged_tdc = merged_tdc[['kiosk', 'city', 'disease_list', 'disease_count','state','geohash']]
    # print(merged_tdc.nunique())
    tdc = merged_tdc
    tdc = tdc.loc[~(tdc == 0).any(axis=1)]
    tdc.duplicated().sum()
    tdc.drop_duplicates(inplace=True)
    tdc.dropna().reset_index(drop=True)

    file_path = 'E:/scano/scano_analysis automated/total_disease_counts.csv'
    # tdc.to_csv(file_path)
    append_to_csv(tdc, file_path)

def total_patient_count(patient):
    pwc = pd.DataFrame(patient)
    pwc['city'] = pwc['address'].apply(get_city_from_address)
    pwc['city'] = pwc['city'].apply(check_city_null)
    pwc['state'] = pwc['city'].apply(get_state_from_city)
    pwc['state'] = pwc['state'].apply(check_null_state)
    pwc['geohash'] = pwc['city'].apply(get_geohash)
    pwc = pwc[['kiosk', 'monthWiseCounts', 'city', 'state','geohash']]
    flattened_patient = []
    for _, row in pwc.iterrows():
        for entry in row['monthWiseCounts']:
            patient_month = entry['month']
            patient_counts = entry['count']
            flattened_patient.append({
                'kiosk': row['kiosk'],
                'city': row['city'],
                'state' : row['state'],
                'geohash' : row['geohash'],
                'patient_month': patient_month,
                'patient_counts': patient_counts
            })
    flattened_patient = pd.DataFrame(flattened_patient)
    # pwc = pwc.merge(flattened_patient, on=['kiosk','city','state'], how='right')
    pwc = pwc.merge(flattened_patient, on=['kiosk'], how='right')
    pwc.drop(columns=['monthWiseCounts'], inplace=True)
    pwc.duplicated().sum()
    pwc.drop_duplicates(inplace=True)
    pwc = pwc.loc[~(pwc == 0).any(axis=1)]
    pwc.rename(columns={'city_y': 'city', 'state_y':'state', 'geohash_y':'geohash','disease_count_y': 'disease_count'}, inplace=True)
    pwc = pwc[['kiosk', 'city', 'state', 'geohash', 'patient_month', 'patient_counts']]
    pwc.dropna().reset_index(drop=True)
    # pwc.to_csv('patient_wise_counts.csv')
    file_path = 'E:/scano/scano_analysis automated/patient_wise_count.csv'
    append_to_csv(pwc, file_path)

def append_to_csv(dataframe, file_path):
    if isinstance(dataframe, pd.DataFrame):
        # new_df = dataframe
        new_df = dataframe
        new_df.dropna().reset_index(drop = True)
    
    
        if os.path.exists(file_path):
            
            with open(file_path, 'r') as file:
                existing_data = pd.read_csv(file)
                existing_data = pd.DataFrame(existing_data)
                existing_data.dropna().reset_index(drop=True)
                # combined_df = pd.concat([existing_data,new_df])
            # if existing_data.any():
                combined_df = pd.concat([existing_data,new_df]).drop_duplicates()
                combined_df = pd.DataFrame(combined_df)
                combined_df.dropna().reset_index(drop=True)
            combined_df.to_csv(file_path, index = False)
            print('data appended successfully')
                # else:
                #     print('dataframe is empty')
        
    
        else:
            new_df.to_csv(file_path, index=False)
            print(f'file created')
    else:
        raise ValueError('Error getting data')

def check_null_state(state):
    if state == None:
        return 'State'
    else:
        return state

def check_city_null(city):
    if city == None:
        return 'City'
    else:
        return city

def get_city_from_address(address):
    geolocator = GoogleV3(api_key=api_key)
    location = geolocator.geocode(address)
    if location:
        address_components = location.raw.get('address_components', [])
        for component in address_components:
            if 'locality' in component['types']:
                return component['long_name']
        return location.address
    else:
        return None


def get_state_from_city(city):
    geolocator = GoogleV3(api_key=api_key)
    location = geolocator.geocode(city)
    if location:
        address_components = location.raw.get('address_components', [])
        for component in address_components:
            if 'administrative_area_level_1' in component['types']:
                return component['long_name']
        return location.address
    return None

def execute_preprocess():
    url = 'http://182.168.1.210:3100/v1/analytics/get-month-wise-analytics?startDate=01/1/2024&endDate=31/12/2024'
    auth_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6IiIsImlkIjoiNjU5MDA4ODljMGIxMzhlYTY0MGJjZDE1IiwiaWF0IjoxNzM3NjE5MTM0fQ.Up7ez2yuGsdD2a7twwcv4egLvPlnqZjTa7nvhCxGd3g'
    data = fetch_data_mwdc(url, auth_token)
    disease = fetch_data_tdc(url, auth_token)
    patient = fetch_data_pwc(url,auth_token)
    if data and disease and patient:
    # if disease:
        # print(data)
        preprocessed_data(data)
        total_disease_count(disease)
        total_patient_count(patient)
    else:
        print('data not available')

execute_preprocess()


'''
attrition 
calculus 
tooth gap
stains
defective / partial treatment
pit and fissure
inflammed redgums
impacted 3molar pericorontis
fracture
crowns'''