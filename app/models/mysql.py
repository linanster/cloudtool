import random
from datetime import datetime, timedelta
from functools import reduce
from flask_sqlalchemy import SQLAlchemy
from dateutil import tz
#
db_mysql = SQLAlchemy(use_native_unicode='utf8')

class MyBaseModel(db_mysql.Model):
    __abstract__ = True
    id = db_mysql.Column(db_mysql.Integer, nullable=False, autoincrement=True, primary_key=True)
    def save(self):
        try:
            db_mysql.session.add(self)
            db_mysql.session.commit()
            return True
        except Exception as e:
            print(e)
            return False
    def delete(self):
        try:
            db_mysql.session.delete(self)
            db_mysql.session.commit()
            return True
        except Exception as e:
            print(e)
            return False


class ToolRecord(MyBaseModel):
    __bind_key__ = 'mysql_gecloudtool_toolrecord'
    __tablename__ = 'toolrecord'
    # card_date = db_mysql.Column(db_mysql.DateTime, nullable=False)
    card_date = db_mysql.Column(db_mysql.Date, nullable=False)
    create_time = db_mysql.Column(db_mysql.DateTime, nullable=False)
    update_time = db_mysql.Column(db_mysql.DateTime, nullable=False)
    typecode = db_mysql.Column(db_mysql.Integer, nullable=False)
    content = db_mysql.Column(db_mysql.String(500), nullable=False)
    def __init__(self, card_date, create_time, update_time, typecode, content):
        self.card_date = card_date
        self.create_time = create_time
        self.update_time = update_time
        self.typecode = typecode
        self.content = content
    @staticmethod
    def seed():
        p = 'abcdefghigklmnopqrstuvwxyz.,! '
        date_obj_start = datetime.strptime('2022-01-01', '%Y-%m-%d')
        items = []
        for i in range(365):
            # card_date = (date_obj_start + timedelta(i, 0, 0)).strftime('%Y-%m-%d')
            card_date = date_obj_start + timedelta(i, 0, 0)
            create_time = datetime.now()
            update_time = datetime.now()
            typecode = random.choice([1, 2, 3, 4])
            content = reduce(lambda x,y: x+y, random.choices(p, k=random.randint(10, 140)))
            items.append(ToolRecord(card_date, create_time, update_time, typecode, content))
        db_mysql.session.add_all(items)
        db_mysql.session.commit()

