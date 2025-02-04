from flask import Flask, request, jsonify, Response, render_template, flash, redirect, url_for
from flask_pymongo import PyMongo
from bson import json_util, ObjectId
import os

app = Flask(__name__)

app.secret_key = os.urandom(24)

app.config['MONGO_URI'] = 'mongodb+srv://minguitojefe:12345@cluster0.nxdnc.mongodb.net/flask_practice'
mongo = PyMongo(app)

@app.route('/', methods=['GET'])
def index():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            flash('Todos los campos son obligatorios.')

        user = mongo.db.users.find_one({"username": username, "password": password})

        if user:
            if user['password'] == password:
                return redirect(url_for('perfil', user_id=user['_id']))
            else:
                return 'Usuario no encontrado', 404
        else:
            return 'Usuario no encontrado, 404'

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        name = request.form.get('name')
        username = request.form.get('username')
        password = request.form.get('password')


        if not name or not username or not password:
            flash('Todos los campos son obligatorios.')
            return redirect(url_for('register'))

        usuario_existente = mongo.db.users.find_one({"username": username})
        if usuario_existente:
            flash('El usuario ya existe.')
            return redirect(url_for('register'))

        mongo.db.users.insert_one({
            "name": name,
            "username": username,
            "password": password
        })

        flash('Usuario registrado correctamente.')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/users', methods=['GET'])
def get_user():

    users = mongo.db.users.find()
    return render_template('users.html', users=users)

@app.route('/perfil/<user_id>', methods=['GET'])
def perfil(user_id):

    user = mongo.db.users.find_one({'_id': ObjectId(user_id)})
    if user:
        return render_template('perfil.html', user=user)
    else:
        return 'Usuario no encontrado', 404

if __name__ == '__main__':
    app.run(debug=True)