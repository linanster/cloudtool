SECRET_KEY = "youdonotknowme"
SQLALCHEMY_TRACK_MODIFICATIONS = False
DEBUG = False

SQLALCHEMY_BINDS = {
'mysql_gecloudtool_toolrecord': 'mysql+pymysql://root1:123456@localhost:3306/gecloudtool',
}

