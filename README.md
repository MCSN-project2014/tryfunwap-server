![alt text](public/fun_logo.jpg)
# Funwap dasync Server
This is the the funwap dasync server, for execute remote code send from the funwap dasync command by the interpreter or the compiler. The server is write in python and c#, with Flask micro-framework and .NET 4.5. The server receive a json with the code and the parameter of the function that have to be executed, and the server execute the c# interpreter to get the result and send back to the client. 

###Installation Instruction:
The following guide have to be adopted only to try or debug the funwap server. To deploy the server in a production ambient must following the standard deployment option in the [official Flask site] (http://flask.pocoo.org/docs/0.10/deploying/).
- ####Windows:
  - download [python-3.4](https://www.python.org/ftp/python/3.4.2/python-3.4.2.msi)
  - during the installation insured to check the option 'Add python.exe to Path' or add the python folder and the scripts folder in the PATH ambient variable on your own.
  - double click the `InstallServer.bat` file and waiting is termination (the installation script need an internet connection).
  - to start the server double click on the `StartServer.bat` file.


- ####Linux
  - install `python-3.4`, `python-pip` and `mono-3.10` for your distribution
  - open a terminal and run the command `pip install virtualenv` as a root
  - on a terminal go to the funwap-server folder and as a user execute the following command:
    - `virtualenv -p <python-3.4 path> venv`
    - `source venv/bin/activate`
    - `pip install -r requirements.txt`
  - now you can start the sever with the command `python run.py`, to close the virtualenv do the command `deactivate`
