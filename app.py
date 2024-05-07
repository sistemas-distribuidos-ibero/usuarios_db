from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime
import os
from dotenv import load_dotenv

# Carga las variables de entorno desde el archivo .env
load_dotenv()

app = Flask(__name__)

# Configuración de la conexión a la base de datos MongoDB
mongodb_uri = os.getenv('MONGODB_URI')
if not mongodb_uri:
    raise RuntimeError("MONGODB_URI is not set")

database_name = os.getenv('DATABASE_NAME')
if not database_name:
    raise RuntimeError("DATABASE_NAME is not set")

client = MongoClient(mongodb_uri)
db = client[database_name]

users_collection_name = os.getenv('USERS_COLLECTION_NAME')
if not users_collection_name:
    raise RuntimeError("USERS_COLLECTION_NAME is not set")

users_collection = db[users_collection_name]

# Definición de endpoints de la API para la gestión de usuarios
@app.route('/api/v1/users', methods=['POST'])
def create_user():
    data = request.json
    required_fields = ['username', 'email']
    for field in required_fields:
        if field not in data:
            return jsonify({'message': f'Missing required field: {field}'}), 400

    data['created_at'] = datetime.now()
    user_id = users_collection.insert_one(data).inserted_id
    return jsonify({'message': 'User created successfully', 'user_id': str(user_id)}), 201

@app.route('/api/v1/users', methods=['GET'])
def get_users():
    users = list(users_collection.find())
    return jsonify([{'username': user['username'], 'email': user['email']} for user in users])

@app.route('/api/v1/users/<string:user_id>', methods=['GET'])
def get_user(user_id):
    user = users_collection.find_one({'_id': ObjectId(user_id)})
    if user:
        return jsonify({'username': user['username'], 'email': user['email']})
    else:
        return jsonify({'message': 'User not found'}), 404

@app.route('/api/v1/users/<string:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.json
    data['updated_at'] = datetime.now()
    result = users_collection.update_one({'_id': ObjectId(user_id)}, {'$set': data})
    if result.modified_count:
        return jsonify({'message': 'User updated successfully'})
    else:
        return jsonify({'message': 'User not found'}), 404

@app.route('/api/v1/users/<string:user_id>', methods=['DELETE'])
def delete_user(user_id):
    result = users_collection.delete_one({'_id': ObjectId(user_id)})
    if result.deleted_count:
        return jsonify({'message': 'User deleted successfully'})
    else:
        return jsonify({'message': 'User not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
