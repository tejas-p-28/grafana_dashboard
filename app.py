# import requests
# import pandas as pd
# from geopy.geocoders import GoogleV3
# from pandas import json_normalize
# import os
# from dotenv import load_dotenv
# global api_key
# load_dotenv()
# api_key = os.getenv('api_key')
# import json
# import warnings
# warnings.filterwarnings('ignore')

# # data = pd.DataFrame('data.json')
# # print(data.head())
# # data = "E:/scano/data.json"
# # print(data)


# # df.to_json('testing.json', orient="records", date_format="iso")
# # api_url = "http://182.168.1.210:3100/v1/analytics/get-month-wise-analytics?startDate=01/06/2024&endDate=30/06/2024"
# # api_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6IiIsImlkIjoiNjU5MDA4ODljMGIxMzhlYTY0MGJjZDE1IiwiaWF0IjoxNzM2NTA5NDM0fQ.rUVa4DQEPoznXph72mI4jDAnWVTS3pFmkbsrdibBbjM"

# # headers = {
# #     "Authorization": f"Bearer {api_key}"
# # }

# # response = requests.get(api_url, headers=headers)
# # print(response.json())
# # response = pd.DataFrame(response)
# # response.to_json('test.json')


# import pandas as pd
# import json 
# def fetch_data_from_api(url, auth_token):
#     headers = {
#         'Authorization' : f'Bearer {auth_token}',
#         'Content-Type' : 'application/json'
#     }
#     try:
#         response = requests.get(url, headers=headers)
#         response.raise_for_status()
#         data = response.json()
#         return data
#     except Exception as e:
#         print(f'Error fetching data from api : {e}')
#         return None

# def preprocessed_data(data):
#     df = pd.DataFrame(data)
#     df['city'] = df['address'].apply(get_city_from_address)
#     df['city'] = df['city'].apply(check_city_null)
#     df['state'] = df['city'].apply(get_state_from_city)
#     df['state'] = df['state'].apply(check_null_state)
#     # print(df.head())
#     df = df[['kiosk', 'diseaseWiseMonthCount', 'city', 'state']]
#     flattened_data = []
#     for _, row in df.iterrows():
#         for entry in row['diseaseWiseMonthCount']:
#             disease_month = entry['month']
#             disease_counts = entry['diseaseWiseCount']
#             for disease, count in disease_counts.items():
#                 flattened_data.append({
#                     'kiosk': row['kiosk'],
#                     'city': row['city'],
#                     'state' : row['state'],
#                     'disease_month' : disease_month,
#                     'disease_list': disease,
#                     'disease_count': count
#                 })
#     flattened_df = pd.DataFrame(flattened_data)
#     flattened_df.isna().sum()
#     print(flattened_df.nunique())
#     flattened_df.drop_duplicates(inplace=True)
#     flattened_df.dropna().reset_index(drop=True)
#     remove_nulls(flattened_df)
#     print(flattened_df.nunique())
#     file_path = 'testing.json'
#     df.to_json(file_path, orient='records')

# def remove_nulls(df):
#     if isinstance(df, dict):
#         # For dictionaries, remove keys with None values
#         return {key: remove_nulls(value) for key, value in df.items() if value is not []}
#     elif isinstance(df, list):
#         # For lists, filter out None values and clean each element
#         return [remove_nulls(item) for item in df if item is not []]
#     else:
#         # Return the data if it's neither a dict nor a list
#         return df


# def check_null_state(state):
#     if state == None:
#         return 'State'
#     else:
#         return state

# def check_city_null(city):
#     if city == None:
#         return 'City'
#     else:
#         return city

# def get_city_from_address(address):
#     geolocator = GoogleV3(api_key=api_key)
#     location = geolocator.geocode(address)
#     if location:
#         address_components = location.raw.get('address_components', [])
#         for component in address_components:
#             if 'locality' in component['types']:
#                 return component['long_name']
#         return location.address
#     else:
#         return None


# def get_state_from_city(city):
#     geolocator = GoogleV3(api_key=api_key)
#     location = geolocator.geocode(city)
#     if location:
#         address_components = location.raw.get('address_components', [])
#         for component in address_components:
#             if 'administrative_area_level_1' in component['types']:
#                 return component['long_name']
#         return location.address
#     return None
# def execute_preprocess():
#     url = 'http://182.168.1.210:3100/v1/analytics/get-month-wise-analytics?startDate=01/12/2024&endDate=30/12/2024'
#     auth_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6IiIsImlkIjoiNjU5MDA4ODljMGIxMzhlYTY0MGJjZDE1IiwiaWF0IjoxNzM2NTA5NDM0fQ.rUVa4DQEPoznXph72mI4jDAnWVTS3pFmkbsrdibBbjM'
#     data = fetch_data_from_api(url, auth_token)
 
#     if data:
#         # print(data)
#         preprocessed_data(data)
#     else:
#         print('data not available')
# execute_preprocess()

# # Sample DataFrame
# # data = {
# #     "id": [1, 2, 3],
# #     "name": ["Alice", "Bob", "Charlie"],
# #     "age": [25, 30, 35]
# # }

# # df = pd.DataFrame(data)

# # # Save DataFrame to JSON file
# # file_path = "testing.json"
# # df.to_json(file_path, orient="records", indent=4)

# # print(f"DataFrame saved to {file_path}")


from flask import Flask, jsonify, request, make_response
from flask_cors import CORS
import pandas as pd
import jwt
import datetime
# from flask_jwt_extended import create_access_token, jwt_required, JWTManager
# Create a Flask application
app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'thisistestapi'
# jwt = JWTManager(app)
# user_db = {
#     'username' : 'user1',
#     'password' : 'password123'
# }

def load_csv(file_path):
    try:
        return pd.read_csv(file_path)
    except Exception as e:
        return 'Error getting csv : {e}'
# Define a route
@app.route('/protected')
def protected():
    return ''

@app.route('/unprotected')
def unprotected():
    return ''


@app.route('/login')
def login():
    auth = request.authorization
    # # print(data)
    # username = data.json.get('username')
    # password = data.json.get('password')
    if auth and auth.password == 'pass123':
        token = jwt.encode({'user' : auth.username, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])
        # token = create_access_token(identity=username)
        # print(token)
        return jsonify({'token': token})
        # return jsonify({'access_token': token}),200
    return make_response('Could not verify!', 401, {'WWW-Authenticate' : 'Basic realm = Login required'})

@app.route('/')
def home():
    return "Hello, Flask server on!"

@app.route('/monthdisease')
def monthdisease_count():
    file_path = "E:/scano/scano_analysis automated/monthwise_disease_count.csv"
    df = load_csv(file_path)
    if isinstance(df, str):
        return jsonify({f'error : {df}'})
    month = df.to_dict(orient='records')
    return jsonify(month),200,{'Content-Type' : 'application/json'}

@app.route('/patient')
def patient_count():
    file_path = 'E:/scano/scano_analysis automated/patient_wise_count.csv'
    df = load_csv(file_path)
    if isinstance(df, str):
        return jsonify({f'error : {df}'})
    patient = df.to_dict(orient='records')
    return jsonify(patient), 200, {'Content-Type' : 'application/json'}

@app.route('/disease')
def disease_count():
    file_path ='E:/scano/scano_analysis automated/total_disease_counts.csv'
    df = load_csv(file_path)
    if isinstance(df, str):
        return jsonify({f'error : {df}'})
    disease = df.to_dict(orient='records')
    return jsonify(disease), 200,{'Content-Type' : 'application/json'}

# @app.route('/protected', methods=['GET'])
# def protected():
#     return jsonify({'msg : This is a protected'}),200
# Run the app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
