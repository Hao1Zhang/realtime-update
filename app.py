from fileinput import filename
from flask import Flask, send_from_directory, Response,request
import os
from datetime import datetime
import time
import json
from flask_cors import CORS, cross_origin

app = Flask(__name__)

cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'

react_folder = 'react'
directory= os.getcwd()+ f'/{react_folder}/build/static'


@app.route('/')
def index():
    ''' User will call with with thier id to store the symbol as registered'''
    path= os.getcwd()+ f'/{react_folder}/build'
    print(path)
    return send_from_directory(directory=path,path='index.html')

#
@app.route('/static/<folder>/<file>')
def css(folder,file):
    ''' User will call with with thier id to store the symbol as registered'''
    
    path = folder+'/'+file
    return send_from_directory(directory=directory,path=path)

message = ""

updated = False
@app.route('/stream')
def stream():

    def get_data():

        while True:
            #gotcha
            global updated
            global message
            if updated:
                yield f'data: {message}\n\n'
                updated = False
    return Response(get_data(), mimetype='text/event-stream')

@app.route('/post',methods=['POST'])
def update_message():
    ''' User will call with thier id to store the symbol as registered'''
    global message
    message = request.form['message']
    global updated
    updated = True
    return json.dumps(request.form), 200
    

if __name__ == '__main__':
    app.run()