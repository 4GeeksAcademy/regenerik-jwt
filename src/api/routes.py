"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User
from api.utils import generate_sitemap, APIException
from flask_cors import CORS

# Importaciones nuevas:
from flask_bcrypt import Bcrypt 
from flask_jwt_extended import  JWTManager, create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta


api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)


# Nuevas instancias necesarias :
jwt = JWTManager()
bcrypt = Bcrypt()

@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }

    return jsonify(response_body), 200


@api.route('/test')
def test():
    return jsonify({'msg':"test"})

# ---------------------------EJEMPLO RUTA DE REGISTRO---------------------------

@api.route('/users', methods=['POST'])
def create_user():
    try:
        email = request.json.get('email')
        password = request.json.get('password')
        is_active = request.json.get('is_active',True)

        if not email or not password:
            return jsonify({'error': 'Email and  password  are required.'}), 400

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return jsonify({'error': 'Email already exists.'}), 409

        password_hash = bcrypt.generate_password_hash(password).decode('utf-8')


        # Ensamblamos el usuario nuevo
        new_user = User(email=email, password=password_hash, is_active=is_active)


        db.session.add(new_user)
        db.session.commit()

        ok_to_share = {
            "email": new_user.email,
            "id" : new_user.id
        }
        return jsonify({'message': 'User created successfully.','user_created':ok_to_share}), 201

    except Exception as e:
        return jsonify({'error': 'Error in user creation: ' + str(e)}), 500

# ---------------------------EJEMPLO RUTA GENERADORA DE TOKEN // LOGIN---------------------------

@api.route('/token', methods=['POST'])
def get_token():
    try:
        #  Primero chequeamos que por el body venga la info necesaria:
        email = request.json.get('email')
        password = request.json.get('password')

        if not email or not password:
            return jsonify({'error': 'Email and password are required.'}), 400
        
        # Buscamos al usuario con ese correo electronico ( si lo encuentra lo guarda ):
        login_user = User.query.filter_by(email=email).one()

        # Verificamos si encontró el usuario por el email
        if not login_user:
            return jsonify({'error': 'Invalid email.'}), 404

        # Verificamos que el password sea correcto:
        password_from_db = login_user.password #  Si loguin_user está vacio, da error y se va al "Except".
        resultado = bcrypt.check_password_hash(password_from_db, password)
        #                                          12345678 ,    12345677
        # Si es verdadero generamos un token y lo devuelve en una respuesta JSON:
        if resultado:

            expires = timedelta(days=1)  # pueden ser "hours", "minutes", "days","seconds"

            user_id = login_user.id

            access_token = create_access_token(identity=str(user_id), expires_delta=expires)
            return jsonify({ 'access_token':access_token}), 200

        else:
            return jsonify({"Error":"Contraseña  incorrecta"}),404
    
    except Exception as e:
        return {"Error":"El email proporcionado no corresponde a ninguno registrado: " + str(e)}, 500

# ------------------------------EJEMPLO RUTA RESTRINGIDA POR TOKEN-------------------------------


@api.route('/users')
@jwt_required()  # Decorador para requerir autenticación con JWT
def show_users():
    current_user_id = get_jwt_identity()  # Obtiene la id del usuario del token

    if current_user_id:
        users = User.query.all()
        user_list = []
        for user in users:
            user_dict = {
                'id': user.id,
                'email': user.email
            }
            user_list.append(user_dict)
        return jsonify(user_list), 200
    else:
        return {"Error": "Token inválido o no proporcionado"}, 401
    
    

# ------------------------------------------------------------------------------------------------      