from flask import Flask, request, jsonify
from token_forge import generate_token, authenticate_token
import logging

app = Flask(__name__)

logging.basicConfig(filename='app.log',
                    level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

public_endpoints = { 
        'POST': ['/generate']
    }

@app.before_request
def before_request():
    if request.method in public_endpoints and request.path in public_endpoints[request.method]:
        return

    auth_header = request.headers.get('Authorization', '')
    token = ''
    if auth_header.startswith('Bearer '):
        token = auth_header[len('Bearer '):]

    is_valid, _ = authenticate_token(token)
    if not token or not is_valid:
        return jsonify({'message': 'Unauthorized access'}), 401

@app.route('/')
def home():
    return "Hello, welcome to the secured Flask app!"

@app.route('/generate', methods=['POST'])
def generate_new_token():
    user_data = {
        'user_id': '12345',
        'username': 'gemini',
        'roles': 'admin'
    }
    token = generate_token(user_data['user_id'], user_data['username'], user_data['roles'])
    return jsonify({'token': token})

if __name__ == "__main__":
    app.run(debug=True)
