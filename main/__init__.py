from flask import Flask, request, jsonify, render_template
import os
import datetime

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        #DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    tempStore = []
    dateStore = []

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, Michelle!'

    @app.route('/data/<sensor>', methods=['POST'])
    def add_message(sensor):
        content = request.json
        time = int(content['time'])
        time = datetime.datetime.fromtimestamp(time).strftime('%Y-%m-%d %H:%M:%S')
        tempStore.append(content['seqNumber'])
        dateStore.append(time)
        if len(tempStore) > 10:
            del tempStore[0]
            del dateStore[0]
        print(tempStore)
        print(content['device'])
        return ('', 200)

    @app.route('/')
    def show_graph():
        return render_template('index.html', temps=tempStore, dates=dateStore)

    if __name__ == '__main__':
        port = int(os.environ.get('PORT', 8080))
        app.run(host= '0.0.0.0',port=port,debug=True)

    return app
