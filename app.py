from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime
from dotenv import load_dotenv
import os

# Cargar variables de entorno desde el archivo .env
load_dotenv()

app = Flask(__name__)

# Configuración de la conexión a la base de datos MongoDB
mongodb_uri = os.getenv('MONGODB_URI')
database_name = os.getenv('DATABASE_NAME')
client = MongoClient(mongodb_uri)
db = client[database_name]
users_collection = db[os.getenv('USERS_COLLECTION_NAME')]

# Endpoint para crear un nuevo usuario
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

# Endpoint para obtener todos los usuarios
@app.route('/api/v1/users', methods=['GET'])
def get_users():
    users = list(users_collection.find())
    return jsonify([{'username': user['username'], 'email': user['email']} for user in users])

# Endpoint para obtener un usuario específico
@app.route('/api/v1/users/<string:user_id>', methods=['GET'])
def get_user(user_id):
    user = users_collection.find_one({'_id': ObjectId(user_id)})
    if user:
        return jsonify({'username': user['username'], 'email': user['email']})
    else:
        return jsonify({'message': 'User not found'}), 404

# Endpoint para actualizar un usuario específico
@app.route('/api/v1/users/<string:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.json
    data['updated_at'] = datetime.now()
    result = users_collection.update_one({'_id': ObjectId(user_id)}, {'$set': data})
    if result.modified_count:
        return jsonify({'message': 'User updated successfully'})
    else:
        return jsonify({'message': 'User not found'}), 404

# Endpoint para eliminar un usuario
@app.route('/api/v1/users/<string:user_id>', methods=['DELETE'])
def delete_user(user_id):
    result = users_collection.delete_one({'_id': ObjectId(user_id)})
    if result.deleted_count:
        return jsonify({'message': 'User deleted successfully'})
    else:
        return jsonify({'message': 'User not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
