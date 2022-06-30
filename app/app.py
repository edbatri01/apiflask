from flask import Flask, render_template, request, redirect, url_for, jsonify, json, Response, make_response
from flask_mysqldb import MySQL
from jwt import encode, decode, exceptions
import jwt
import datetime
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
import base64

app = Flask(__name__)

key_token = 'SECRET'

#conexión mysql
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'b@11inas'
app.config['MYSQL_DB'] = 'mypet'

conexion = MySQL(app)

n=30

@app.route('/login', methods=['POST'])
def login():
    auth = request.get_json()
    password = base64.b64decode(auth['password']).decode('utf-8')
    print('lo que llegó ',auth['username'],auth['password'])
    if not auth or not auth['username'] or not auth['password']:
        return josonify({"message":"No verificado","status_code":401})  
    else:
        data = ''
        cursor = conexion.connection.cursor()
        sql = f"""select username from users where username = '{auth['username']}';"""  
        if cursor.execute(sql):
            print('entra')
        else:
            print('no entra')
        
        data = cursor.fetchall()
        conexion.connect.close()
        if len(data)>=1:
            cursor = conexion.connection.cursor()
            sql = f"""select username from users where username = '{auth['username']}' AND password = "{password}";"""
            cursor.execute(sql)
            data = ''
            data = cursor.fetchall()
            conexion.connect.close()
            if len(data)>=1:

                token = jwt.encode({"public_id":auth['username'],"exp":datetime.datetime.utcnow()+datetime.timedelta(minutes=n)},key_token)
                return token
            else:
                return make_response('usuario o contraseña no valido',  400)
                #return Response("{'message':'Usuario o contraseña invalida'}", status=400, mimetype='application/json')
        else:
            return Response("{'message':'Usuario no existe'}", status=400, mimetype='application/json')

@app.route('/validate', methods=['GET'])
def home():
    print(request.headers['X-Access-Tokens'])
    
    if 'x-access-tokens' in request.headers:
        token = request.headers['x-access-tokens']
        

    if not token:
        return make_response('token invalido',401)
    else:
        try:
            
            validate_token = jwt.decode(request.headers['X-Access-Tokens'],key_token,algorithms=['HS256'])
            data = ''
            cursor = conexion.connection.cursor()
            print(validate_token['public_id'])
            sql = f"""SELECT username FROM users WHERE username = '{validate_token['public_id']}';"""
            cursor.execute(sql)
            data = cursor.fetchall()
            conexion.connect.close()
            if len(data)>=1:
                
                return make_response('token valido',200)
            else:
                return make_response('token invalido',401)
        except jwt.ExpiredSignature as ex:
            return make_response('token expirado',401)
        
       

@app.route('/register', methods=['POST'])
def register():
    register = request.get_json()
    username = base64.b64decode(register['username']).decode('utf-8')
    password = base64.b64decode(register['password']).decode('utf-8')
    email_address = base64.b64decode(register['email_address']).decode('utf-8')
    print('decodificado: ',username,password,email_address)
    try:
        data = ''
        cursor = conexion.connection.cursor()
        sql = f"""SELECT username FROM users WHERE username = '{username}';"""
        cursor.execute(sql)
        data = cursor.fetchall()
        conexion.connect.close()
        print(len(data))
        if len(data)>=1:
            return make_response('usuario ya existe',400)
        else:
            data = ''
            cursor = conexion.connection.cursor()
            sql = f"""INSERT INTO users (username,password,email_address) VALUES ("{username}","{password}","{email_address}");"""
            cursor.execute(sql)
            conexion.connection.commit()
            return make_response('usuario registrado correctamente',200)
            
    except Exception as ex:
        print(ex)
        return make_response('error',500)
    






# def page_no_found(error):
#     #return render_template('404.html'), 404 
#     return redirect(url_for('index')) 

if __name__ == '__main__':
    
    app.run(debug=True, port=5000, host='0.0.0.0')

# @app.before_request
# def before_request():
#     print('before')

# @app.after_request
# def after_request(response):
#     print('after')
#     return response

# @app.route('/')
# def index():
#     cursos = ['PHP', 'Python', 'javascript','java', 'kotlin', 'Dart']
#     #diccionario
#     data = {
#         'titulo': 'Index',
#         'bienvenida': 'saludos',
#         'cursos': cursos,
#         'numero_cursos': len(cursos)
#     }
#     return render_template('index.html',data=data)

# @app.route('/contact/<nombre>/<int:edad>')
# def contact(nombre,edad ):
#     data = {
#         'titulo':'contacto',
#         'nombre':nombre,
#         'edad':edad
#     }
#     return render_template('contact.html',data=data)

# def query_string():
#     print(request)
#     print(request.args)
#     print(request.args.get('param1'))
#     return 'ok'

