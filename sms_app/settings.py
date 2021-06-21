import os

SECRET_KEY = os.environ.get('SECRET_KEY')
MONGO_PASS = os.environ.get('MONGO_PASS')
MONGO_URI='mongodb+srv://dbAdmin:{}@cluster0.kqkws.mongodb.net/showmesigfox_db?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE'.format(MONGO_PASS)