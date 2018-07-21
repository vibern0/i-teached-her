import auth
from flask import Flask, redirect, request, session, Response
app = Flask(__name__)


@app.route('/login',methods = ['POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        return auth.auth_from_sqlite(username, password)
    return ''


@app.route('/info',methods = ['POST'])
def info():
    if request.method == 'POST':
        if request.headers['Content-Type'] == 'application/json':
            content = request.json
            username = auth.get_username_by_token(content['token'])
            if username != None and auth.validate_user_permissions(username):
                result = auth.request_info(content['info'])
                return Response('{{"info":"{0}"}}'.format(result), status=200, mimetype='application/json')
            else:
                content = '{"error_msg": "Invalid token or users doesn\'t have permission!"}'
                return Response(content, status=400, mimetype='application/json')

        content = '{"error_msg": "Wrong data format!"}'
        return Response(content, status=400, mimetype='application/json')


if __name__ == '__main__':
    auth.connect_to_redis()
    app.run(port = 4383, debug = True)