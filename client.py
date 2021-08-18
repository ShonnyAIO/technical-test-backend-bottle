
from bottle import request, template, static_file
import bottle

app = bottle.Bottle()


@app.get('/', method=['GET'])
def index():
    return template('./templates/index.html')


@app.get('/register', method=['GET'])
def register():
    return template('./templates/register.html')


@app.get('/todos', method=['GET'])
def notes():
    return template('./templates/todos.html')


@app.get('/static/<dir:path>/<filename:path>')
def server_static(dir, filename):
    print(dir, filename)
    return static_file(filename, root=f'templates/static/{dir}')


if __name__ == '__main__':
    app.run(debug=True, reloader=True, port=5000)
