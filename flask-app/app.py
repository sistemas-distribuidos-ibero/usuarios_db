from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://postgres:postgres@db:5432/mydatabase'


db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

db.create_all()

@app.route('/users/<int:page>', methods=['GET'])
def get_users(page):
    per_page = 10
    users = User.query.paginate(page, per_page, error_out=False)
    users_data = [{'id': user.id, 'name': user.name, 'email': user.email, 'role_id': user.role_id} for user in users.items]
    return jsonify(users_data)

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    new_user = User(name=data['name'], email=data['email'], role_id=data['role_id'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'}), 201

@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify({'id': user.id, 'name': user.name, 'email': user.email, 'role_id': user.role_id})

@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    user = User.query.get_or_404(id)
    data = request.get_json()
    user.name = data.get('name', user.name)
    user.email = data.get('email', user.email)
    user.role_id = data.get('role_id', user.role_id)
    db.session.commit()
    return jsonify({'message': 'User details updated'})

@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted'})

@app.route('/roles/<int:page>', methods=['GET'])
def get_roles(page):
    per_page = 10
    roles = Role.query.paginate(page, per_page, error_out=False)
    roles_data = [{'id': role.id, 'name': role.name} for role in roles.items]
    return jsonify(roles_data)

@app.route('/roles', methods=['POST'])
def create_role():
    data = request.get_json()
    new_role = Role(name=data['name'])
    db.session.add(new_role)
    db.session.commit()
    return jsonify({'message': 'Role created successfully'}), 201

@app.route('/roles/<int:id>', methods=['GET'])
def get_role(id):
    role = Role.query.get_or_404(id)
    return jsonify({'id': role.id, 'name': role.name})

@app.route('/roles/<int:id>', methods=['PUT'])
def update_role(id):
    role = Role.query.get_or_404(id)
    data = request.get_json()
    role.name = data.get('name', role.name)
    db.session.commit()
    return jsonify({'message': 'Role details updated'})

@app.route('/roles/<int:id>', methods=['DELETE'])
def delete_role(id):
    role = Role.query.get_or_404(id)
    db.session.delete(role)
    db.session.commit()
    return jsonify({'message': 'Role deleted'})

if __name__ == '__main__':
    app.run(debug=True)
