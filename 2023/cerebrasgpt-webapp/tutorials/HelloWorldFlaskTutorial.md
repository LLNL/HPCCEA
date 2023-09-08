
# Hello World Flask Tutorial 

- Create new directory for Hello World Flask App
```
mkdir hello
cd hello
```

- Create virtual environment for Flask python and activate it (if you want to leave venv, use: **deactivate**)

```
python3 -m venv venv
source venv/bin/activate
```

- Install flask

```
pip3 install flask
```

- In **app.py**

```
from flask import Flask
 
app = Flask(__name__)
 
@app.route('/')
def index():
    return 'Hello World!'
 
app.run(debug=True, host='0.0.0.0', port=5000)
```

- Run the app

```
python3 app.py
```

- In Firefox, type in the browser: http://HOSTNAME:5000 and see your website pop up! (Replace HOSTNAME with your actual hostname)
