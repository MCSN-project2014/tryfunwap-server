from flask import Flask
from flask import render_template
from flask import request
import subprocess
from subprocess import TimeoutExpired
import uuid
import os

app = Flask(__name__)


@app.route('/interpret', methods=['POST', 'GET'])
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
