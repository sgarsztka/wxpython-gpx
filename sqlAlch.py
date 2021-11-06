from sqlalchemy import create_engine,inspect, select
from sqlalchemy import Column, Table, Integer, String, MetaData, REAL, DATETIME




def createDb():
    engine = create_engine("sqlite:///sqlDb.db", echo=True)
    insp = inspect(engine)
    meta = MetaData()
    if not insp.has_table('users'):
        users = Table(
            'users',meta,
            Column('id',Integer, primary_key=True),
            Column('name',String),
            Column('password',String),
        )

        gpxTracks = Table(
            'gpxTracks',meta,
            Column('id',Integer,primary_key=True),
            Column('user',String),
            Column('avgSpeed',REAL),
            Column('distance',REAL),
            Column('avgHr',REAL),
            Column('date',DATETIME),
            Column('rideTime',String),
            Column('points', String),
            Column('hr', String),
            Column('elevation', String),

        )
        meta.create_all(engine)


def insertUser(name,password):
    engine = create_engine("sqlite:///sqlDb.db",echo=True)
    metadata = MetaData()
    userstable = Table('users', metadata, autoload=True, autoload_with=engine)
    userIns = userstable.insert().values(name = name, password=password)
    results = engine.execute(userIns)



def insertGpxTrack(username,avgSpeed,distance,avgHr,date,rideTime,points,hr,elevation):
    engine = create_engine("sqlite:///sqlDb.db", echo=True)
    metadata = MetaData()
    gpxTracksTable = Table('gpxTracks', metadata, autoload=True, autoload_with=engine)
    trackInsert = gpxTracksTable.insert().values(user=username,
                                                 avgSpeed=avgSpeed, distance=distance, avgHr=avgHr,
                                                 date=date, rideTime=rideTime, points=points, hr=hr,
                                                 elevation=elevation)
    results = engine.execute(trackInsert)


def checkUser(name,password):
    engine = create_engine("sqlite:///sqlDb.db", echo=True)
    metadata = MetaData()
    userstable = Table('users', metadata, autoload=True, autoload_with=engine)
    query = select([userstable]).where(userstable.columns.name == name)
    results = engine.execute(query)
    user = results.fetchall()
    if user:
        try:
            if name == user[0][1] and password == user[0][2]:
                return True
        except:
            print("Sql exception")
    else:
        return False