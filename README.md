# Backend

## 1. Set up a virtual environment

```sh
cd nexchange
python -m venv env
source env/bin/activate
pip install -r requirements.txt
```

## 2. run migrations and app

```sh
python manage.py migrate
python manage.py runserver
```

# Frontend

## 1. Install modules

```sh
cd frontend/nexchange-frontend
npm install
```

## 2. run the app
npm run dev