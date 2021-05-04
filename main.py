from flask import Flask, request, make_response, redirect, render_template
from flask_bootstrap import Bootstrap

app = Flask(__name__, template_folder='./templates', static_folder='./static')
bootstrap = Bootstrap(app)

todos = ['Buy coffee', 'Send purchase request', 'Deliver video to producer']

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html.j2', error=error)

@app.errorhandler(500)
def internal_server_error(error):
    return render_template('500.html.j2', error=error)

@app.route('/')
def index():
    user_ip = request.remote_addr

    response = make_response(redirect('/hello'))
    response.set_cookie('user_ip', user_ip)

    return response

# @app.route('/')
# def index():
#     raise(Exception('500 error'))

@app.route('/hello')
def hello():
    user_ip = request.cookies.get('user_ip')
    context = {
        'user_ip': user_ip,
        'todos': todos,
    }

    return render_template('hello.html.j2', **context)

if __name__ == '__main__':
    app.run(port=5000, debug=True)
