```
python3 -m venv .venv

pip3 install -r requirements.txt

python3 manage.py migrate

export DEBUG=True

python3 manage.py runserver
```