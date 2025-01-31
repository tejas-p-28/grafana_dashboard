


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
