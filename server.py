

from bottle import request, response
from truckpad.bottle.cors import CorsPlugin, enable_cors

from models import Todo, Users
from dotenv import load_dotenv

import json
import bottle
import jwt
import time

load_dotenv()
SECRET_KEY = 'This is a Secret'
app = bottle.Bottle()


def checkiftokenisvalid(func):
    def wrapper(*args):
        jwtToken = request.get_header('jwtToken')

        if not jwtToken:
            return {'status': 'Token not found'}

        payload = jwt.decode(jwtToken, SECRET_KEY, algorithms=['HS256'])

        received_user = payload.get('username')
        received_expire_time = payload.get('expire_time')
        received_issual_time = payload.get('issual_time')

        if int(time.time()) > received_expire_time:

            print('current tym', int(time.time()))
            print('expire tym', received_expire_time)
            print('issue tym', received_issual_time)
            return 'Token Expired'

        return func(received_user)

    return wrapper


@enable_cors
@app.post('/api/auth/register')
def register():
    if request.method == 'POST':
        received_json_data = request.json
        print(received_json_data)
        try:

            password = received_json_data.get('password')

            user = Users.create(
                name=received_json_data.get('username'),
                password=Users.gen_hash(password))

            user.save()

            response.status = 201
            return {'status': f'user {user.name} successfully registered!'}

        except:
            return {'status': f'user {received_json_data.get("username")}  already registered'}

    else:
        return {'status': f'wrong method, {request.method}'}


@enable_cors
@app.post('/api/auth/login')
def login_required():
    if request.method == 'POST':

        if request.json:
            received_json_data = request.json
        elif request.body:
            received_json_data = json.load(request.body)
        else:
            response.status = 400
            return {'status': 'Body no found'}

        print(received_json_data)
        username = received_json_data.get('username')
        password = received_json_data.get('password')

        try:
            user = Users.get(name=username)
            if not user.verify(password):
                return 'Password incorrect'

        except Users.DoesNotExist:
            return {'status': 'Unregistered user'}

        refresh_token_content = {}

        if user:
            refresh_token_content = {
                'user_id': user.id,
                'username': user.name,
                'password': user.password
            }

        refresh_token = {
            'refreshToken': jwt.encode(refresh_token_content, SECRET_KEY, algorithm='HS256')
        }

        temp = refresh_token.get('refreshToken')
        actual_refresh_token = temp

        ts = int(time.time())
        access_token_content = {
            'username': user.name,
            'password': user.password,
            'issual_time': ts,
            'expire_time': ts + 3500
        }

        jwt_token = {'token': jwt.encode(
            access_token_content, SECRET_KEY, algorithm='HS256')}
        u = jwt_token.get('token')
        actual_access_token = u
        ts = float(time.time())

        final_payload_x = {'user':
                           {
                               'userName': user.name,
                               'issual_time': int(ts),
                               'expire_time': int(ts + 3500)
                           },
                           'jwtToken': actual_access_token,
                           'refreshToken': actual_refresh_token
                           }

        response.content_type = 'application/json'
        return json.dumps(final_payload_x)

    else:
        return {'status': 'method not authorized'}


@enable_cors
@app.post('/api/create')
@checkiftokenisvalid
def create(userinfo):
    data = request.json
    user = Users.get(name=userinfo)
    
    Todo.create(
        titulo=data['titulo'],
        descripcion=data['descripcion'],
        user_id=user.id
    )
    response.status = 201
    return data


@enable_cors
@app.get('/api/all')
@checkiftokenisvalid
def list_to_do(userinfo):
    user_id = Users.get(name=userinfo).id
    query = Todo.getById(user_id)
    result = []
    data = {"id" : 0, "user_id" : 0, "titulo" : '', "descripcion" : ''}
    for i in query:
        data["id"] = i[0]
        data["user_id"] = i[1]
        data["titulo"] = i[2]
        data["descripcion"] = i[3]
        result.append(data)
        data = {"id" : 0, "user_id" : 0, "titulo" : '', "descripcion" : ''}
    print(result)
    return {'data': result}


@enable_cors
@app.post('/api')
@checkiftokenisvalid
def index(userinfo):

    if user:
        return f'Welcome {userinfo.user}'

    else:
        return 'Error, not authorized'


if __name__ == '__main__':

    try:
        user = Users.get(name='jonathan')

    except Users.DoesNotExist:

        user = Users.create(
            name='jonathan',
            password=Users.gen_hash("123456")
        )

        user.save()

    app.install(CorsPlugin(origins=['*']))
    app.run(debug=True, reloader=True, port=8000)
