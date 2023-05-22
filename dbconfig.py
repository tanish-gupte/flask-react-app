import pymysql

def connectDB ():
    return pymysql.connect(
        user = 'AstroTeamMysqlDB',
        password = 'Astro1234',
        host = 'astrodatabase.c9jrbrhejvei.ap-south-1.rds.amazonaws.com',
        database = 'AstroMysqlDB'
    )