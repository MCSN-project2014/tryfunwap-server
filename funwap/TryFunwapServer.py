from flask import Flask
from flask import request, make_response, current_app
from functools import update_wrapper
from datetime import timedelta
import subprocess
from subprocess import TimeoutExpired
import uuid
import os

app = Flask(__name__)


def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, str):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, str):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator


@app.route('/interpret', methods=['POST', 'GET'])
@crossdomain(origin='*')
def interpret():
    if request.method == 'POST':
        dataRow = request.data.decode('utf-8')

        if dataRow == '' and request.form.get('json') is not None:
            dataRow = request.form['json']
        elif dataRow == '':
            return 'data error'

        fileName = "bin/"+str(uuid.uuid4())+".fun"
        out_file = open(fileName, "w")
        out_file.write(dataRow)
        out_file.close()

        return runCommand(['mono', 'bin/funwapi.exe', fileName], fileName)

    return 'run'


@app.route('/compile', methods=['POST', 'GET'])
@crossdomain(origin='*')
def compile():
    if request.method == 'POST':
        dataRow = request.data.decode('utf-8')

        if dataRow == '' and request.form.get('json') is not None:
            dataRow = request.form['json']
        elif dataRow == '':
            return 'data error'

        fileName = "bin/"+str(uuid.uuid4())+".fun"
        out_file = open(fileName, "w")
        out_file.write(dataRow)
        out_file.close()

        fileNameOut = "bin/"+str(uuid.uuid4())+".fs"
        out = runCommand(['mono', 'bin/funwapc.exe', fileName, '-o', fileNameOut], fileName)

        try:
            with open(fileNameOut, 'r') as content_file:
                out = out + '\n' + content_file.read()
        except:
            return out

        os.remove(fileNameOut)
        return out

    return 'run'


def runCommand(command, fileName):
    try:
        p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate(timeout=30)
        err = err.decode('utf-8')
        out = out.decode('utf-8')

        if err == '':
            print('result: ' + out)
            os.remove(fileName)
            return out
        else:
            print('error: ' + err)
            os.remove(fileName)
            return "server internal error"

    except TimeoutExpired:
        p.kill()
        os.remove(fileName)
        return 'operation too long'
