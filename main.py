from flask import Flask, Response
import json

app = Flask(__name__)

@app.route('/hello')
def hello():
    return Response(response=json.dumps({'message': 'hello response'}), status=500)

app.run()