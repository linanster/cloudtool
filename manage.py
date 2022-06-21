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


# python3 manage.py runserver -h 0.0.0.0 -p 5000 -r -d
if __name__ == '__main__':

    manager.run()
