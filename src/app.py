from flask import Flask, request, jsonify, Response, render_template, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
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

        user = mongo.db.users.find_one({"username": username})

        if user:
            if check_password_hash(user['password'], password):
                return redirect(url_for('perfil', user_id=user['_id']))
            else:
                flash("Contraseña incorrecta.")
                return redirect(url_for('login'))
        else:
            flash("Usuario no encontrado.")
            return redirect(url_for('login'))

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

        hashed_password = generate_password_hash(password)

        mongo.db.users.insert_one({
            "name": name,
            "username": username,
            "password": hashed_password
        })

        flash('Usuario registrado correctamente.')
        return redirect(url_for('login'))

    return render_template('register.html')

#USERS
@app.route('/users', methods=['GET'])
def users():

    users = mongo.db.users.find()
    return render_template('users.html', users=users)

@app.route('/edit/<user_id>', methods=['GET'])
def edit(user_id):
    
    user_id = ObjectId(user_id)

    user = mongo.db.users.find_one({'_id': user_id})

    if user:
        return render_template('edit_user.html', user=user)
    else:
        flash('Usuario no encontrado.')
        return redirect(url_for('users'))

@app.route('/delete/<user_id>', methods=['POST'])
def delete_user(user_id):

    user_id = ObjectId(user_id)

    mongo.db.users.delete_one({'_id': user_id})

    return redirect(url_for('users'))

@app.route('/update/<user_id>', methods=['POST'])
def update_user(user_id):
    name = request.form.get('name')
    username = request.form.get('username')
    password = request.form.get('password')

    hashed_password = generate_password_hash(password)

    mongo.db.users.update_one(
        {'_id': ObjectId(user_id)},
        {'$set': {'name': name, 'username': username, 'password': hashed_password}}
    )

    flash('Usuario actualizado correctamente.')
    return redirect(url_for('users'))  


@app.route('/perfil/<user_id>', methods=['GET'])
def perfil(user_id):

    user = mongo.db.users.find_one({'_id': ObjectId(user_id)})
    if user:
        return render_template('perfil.html', user=user)
    else:
        return 'Usuario no encontrado', 404

if __name__ == '__main__':
    app.run(debug=True)