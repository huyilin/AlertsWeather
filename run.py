import MySQLdb

execfile("alertsweather.py")
db=MySQLdb.Connect(host="localhost",
                   user="team06",
                   passwd="aiM7chah,d",
                   db="randomtrip")
cur=db.cursor()
try:
    cur.execute("drop table if exists weather")
    cur.execute("drop table if exists alerts")
    cur.execute("create table weather(city varchar(30),\
                 date DATE,\
                 description varchar(100))")
    cur.execute("create table alerts(city varchar(30) PRIMARY KEY,\
                 date DATE,\
                 description varchar(100))")
    weather_file=open("weather.csv","r")
    # alerts_file=open("alerts.csv","r")
    for line in weather_file:
        array=line.rstrip('\n').split(',')
        cur.execute("insert into weather(city,date,description) values(%s,%s,%s)",(array[0],array[1],array[2]))
    db.commit()
except:
    db.rollback()
db.close()
