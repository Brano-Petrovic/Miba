from flask import Flask, render_template, session
from requests import Session
#from gevent.pywsgi import WSGIServer

app = Flask(__name__)
app.secret_key = 'some secret key'


@app.route('/', methods=['GET', 'POST'])
def main_page():

    return render_template("cockpit.html")


# region System parts and flask parts

if __name__ == '__main__':
    app.config['SESSION_TYPE'] = 'memcached'
    sess = Session()
    app.debug = True
    app.run(threaded=True, host='0.0.0.0', port=80)

    #server = WSGIServer(('0.0.0.0', 80), app)
    #server.serve_forever()

# endregion


