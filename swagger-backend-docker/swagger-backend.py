#!/usr/local/bin/python

import yaml
import os
import json
import subprocess
import random
import shutil

from slugify import slugify

from datetime import datetime

from flask import Flask
from flask import Response
from flask import request

app = Flask(__name__)
my_vars = dict()

def process_session_cookie():
    if 'swagger_backend_session' not in request.cookies:
        random_number = random.randint(10000000, 99999999)
        cookie = 'sw-' + str(random_number)
    else:
        cookie = request.cookies['swagger_backend_session']

    return cookie

@app.route('/swagger-backend/repo', methods=['GET'])
def repo_list():
    files = [f for f in os.listdir(my_vars['repo']) if os.path.isfile(os.path.join(my_vars['repo'], f))]
    output = []
    for f in files:
        o = {}
        o['url'] = '/#/?import=/swagger-backend/repo/' + f + '&no-proxy'
        o['filename'] = f
        output += [o]

    response = app.make_response((json.dumps(output), 200, None))
    response.headers['Content-Type'] = 'application/json'
    return response

@app.route('/swagger-backend/repo/<filename>', methods=['GET'])
def repo_file(filename):
    path = my_vars['repo'] + '/' + filename
    with open(path, 'r') as myfile:
        data = myfile.read()
        
    return Response(data, mimetype='application/x-yaml')

@app.route('/swagger-backend/repo', methods=['PUT'])
def repo_put():
    cookie = process_session_cookie()
    
    d = yaml.load(request.data)

    if d is None:
        print('Error detected')
        return app.make_response(('Yaml content not valid', 500, None))

    if 'info' not in d:
        return app.make_response(('Info section was not found in provided document', 500, None))

    info = d['info']

    if 'title' not in info:
        return app.make_response(('Title must be provided in info section', 500, None))
    if 'version' not in info:
        return app.make_response(('Version must be provided in info section', 500, None))

    title = d['info']['title']
    version = d['info']['version']

    s = title + '-' + version
    slug = slugify(s)

    path = my_vars['repo'] + '/' + slug + '.yml'

    if os.path.isfile(path):
        now = datetime.now()
        f_now = now.strftime('%Y-%m-%d-%H-%M-%S-%f')
        backup_path = my_vars['repo'] + '/backup/' + slug + '-' + f_now + '-' + cookie + '.yml'
        shutil.copyfile(path, backup_path)
        
    with open(path, mode='wb') as a_file:
        a_file.write(request.data)

    response = app.make_response(('', 200, None))
    response.set_cookie('swagger_backend_session', cookie)
    
    return response

def main(repo, debug=False):
    app.debug = debug
    my_vars['repo'] = repo
    app.run(host='0.0.0.0')

if __name__ == "__main__":
    repo = os.environ['SWAGGER_REPOSITORY']
    main(repo, debug=True)




    
