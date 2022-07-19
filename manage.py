from flask_script import Manager
from app.app import create_app, envinfo
#

app = create_app()
manager = Manager(app)

@manager.command
def hello():
    print('hello')

@manager.command
def env():
    envinfo()

@manager.command
def createdb_sqlite(table=False, data=False):
    "--table --data"
    from app.models.sqlite import db_sqlite, User
    if table:
        db_sqlite.create_all(bind='sqlite_user_user')
        print('==create sqlite tables==: user')
    if data:
        User.seed()
        print('==initialize sqlite data==')

@manager.command
def deletedb_sqlite(table=False, data=False):
    "--table --data"
    from app.models.sqlite import db_sqlite, User
    if table:
        db_sqlite.drop_all(bind='sqlite_user_user')
        print('==delete sqlite tables==')
        return
    if data:
        User.query.delete()
        db_sqlite.session.commit()
        print('==delete sqlite data==')

@manager.command
def createdb_mysql(table=False, data=False):
    "--table --data"
    from app.models.mysql import db_mysql, ToolRecord
    if table:
        db_mysql.create_all(bind='mysql_gecloudtool_toolrecord')
        print('==create mysql tables==: toolrecord')
    if data:
        ToolRecord.seed()
        print('==insert data==: toolrecord')

@manager.command
def deletedb_mysql(table=False, data=False):
    "--table --data"
    from app.models.mysql import db_mysql, ToolRecord
    if table:
        db_mysql.drop_all(bind='mysql_gecloudtool_toolrecord')
        print('==delete mysql tables==')
        return
    if data:
        ToolRecord.query.delete()
        db_mysql.session.commit()
        print('==delete mysql datas==')

@manager.command
def refresh_auth():
    'load users from config'
    from app.models.sqlite import db_sqlite, User
    from app.config.userlist import users
    db_sqlite.drop_all(bind='sqlite_user_user')
    print('==delete old data==')
    db_sqlite.create_all(bind='sqlite_user_user')
    newusers = []
    for u in users:
        db_sqlite.session.add(User(*u))
        newusers.append(u[0])
    db_sqlite.session.commit()
    print('==load users from config==')
    print(newusers)

# python3 manage.py runserver -h 0.0.0.0 -p 5000 -r -d
if __name__ == '__main__':

    manager.run()
