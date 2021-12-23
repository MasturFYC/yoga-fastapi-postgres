Change env connection
===
```sh
DATABASE_URL = 'postgresql://{}:{}@{}:{}/{}?sslmode={}'.format(db_username,db_password, host_server, db_server_port, database_name, ssl_mode)
```

Install Virtual Environment
===
```sh
apt install python3-venv
python3 -m venv env
source ./env/bin/activate
python -m pip install -U pip
pip install -r requirements.txt
pip install databases[postgresql]
```

Run app
===
```sh
uvicorn main:app --reload
```
or
```sh
uvicorn --port 8000 --host 127.0.0.1 main:app --reload
```

Deployment command
===
```sh
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
```