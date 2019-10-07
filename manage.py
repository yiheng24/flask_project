from models import models
from views import app
from flask_script import Manager
from flask_migrate import MigrateCommand

manage=Manager(app)
# @manage.command
# def hello():
#     print('hello')
# @manage.command
# def migrate():
#     return models.create_all()
manage.add_command('db',MigrateCommand)

if __name__=='__main__':
    manage.run()

# commond=sys.argv[1]
# if commond =='migrate':
#     models.create_all()
# elif commond == 'runserver':
#     app.run(host='127.0.0.1',port=5000,debug=True)