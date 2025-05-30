# Отчёт в Google Sheets для QRKot

### Описание
В проекте реализована интеграция Google API в приложение сбора пожертвований QRKot. Добавлена возможность формирования отчёта в гугл-таблице. В таблице формируется список закрытых проектов, отсортированных по скорости сбора средств — от тех, что закрылись быстрее всего, до тех, что долго собирали нужную сумму.

Примеры запросов к API, варианты ответов и ошибок приведены в документации проекта, доступной по адресу [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

### Технологии
- Python 3.8.9
- FastAPI 0.78.0

### Шаблон наполнения файла `QRkot_spreadsheets/.env`
```
APP_TITLE=Приложение QRKot
APP_DESCRIPTION=Сервис сбора пожертвований для поддержки котиков.
DATABASE_URL=sqlite+aiosqlite:///./fastapi.db
SECRET=secret
TYPE=service_account
PROJECT_ID=your-projectid-123456
PRIVATE_KEY_ID=your123private45key6789id0
PRIVATE_KEY=-----BEGIN PRIVATE KEY-----your123private45key67890-----END PRIVATE KEY-----
CLIENT_EMAIL=client@your-projectid-123456.iam.gserviceaccount.com
CLIENT_ID=123456789012345678901
AUTH_URI=https://accounts.google.com/o/oauth2/auth
TOKEN_URI=https://oauth2.googleapis.com/token
AUTH_PROVIDER_X509_CERT_URL=https://www.googleapis.com/oauth2/v1/certs
CLIENT_X509_CERT_URL=https://www.googleapis.com/robot/v1/metadata/x509/client%40your-projectid-123456.iam.gserviceaccount.com
EMAIL=user@gmail.com
```

### Запуск проекта
- Клонируйте репозиторий и перейдите в папку проекта:
```
git clone git@github.com:IvalexAnna/QRkot_spreadsheets.git
```
```
cd cat_charity_fund
```
- Установите и активируйте виртуальное окружение:
```
python3 -m venv venv
```
```
source venv/Scripts/activate
```
- Установите зависимости из файла requirements.txt:
```
python3 -m pip install --upgrade pip
```
```
pip install -r requirements.txt
```
- Запустите проект командой:
```
uvicorn app.main:app
```

### Автор
Ivanova Anna