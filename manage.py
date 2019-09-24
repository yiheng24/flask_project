import sys
from models import models
from views import app

commond=sys.argv[1]


if commond =='migrate':
    models.create_all()

elif commond == 'runserver':
    app.run(host='127.0.0.1',port=5000,debug=True)