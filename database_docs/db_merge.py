#research done on http://www.rmunn.com/sqlalchemy-tutorial/tutorial.html
#code explaining and help from http://www.paulsprogrammingnotes.com/2014/01/clonecopy-table-schema-from-one.html
#and also from http://www.tylerlesmann.com/2009/apr/27/copying-databases-across-platforms-sqlalchemy/
from sqlalchemy import create_engine, Table, Column, Integer, Unicode, MetaData, String, Text, update, and_, select, func, types
from sqlalchemy.orm import sessionmaker

def connect_db(URI, PORT, DB, USER, password_file):
    #rename this function to get_engine or something
    """Connects to the database"""
    try:
        fh = open(password_file)
        PASSWORD = fh.readline().strip()
        engine = create_engine("mysql+pymysql://{}:{}@{}:{}/{}".format(USER, PASSWORD, URI, PORT, DB), echo=True)
        return engine
    except Exception as e:
        print("Error Type: ", type(e))
        print("Error Details: ", e)   

def merge():
    # create engine, acknowledge existing columns
    src_engine = connect_db("weatherdb.cnmhll8wqxlt.us-west-2.rds.amazonaws.com", "3306", "WeatherDB", "Administrator", "weatherDB_password.txt")
    src_engine._metadata = MetaData(bind=src_engine)
    src_engine._metadata.reflect(src_engine) # get columns from existing table
    #create table object for the original Table
    orig_table = Table('weather_data', src_engine._metadata)

    # create engine for destination 
    dest_engine = connect_db("DublinBikeProjectDB.cun91scffwzf.eu-west-1.rds.amazonaws.com", "3306", "DublinBikeProjectDB", "theForkAwakens", "db_password.txt")
    dest_engine._metadata = MetaData(bind=dest_engine)
    #make table object for newTable
    new_table = Table('weather_data2', dest_engine._metadata)

    # copy schema and create newTable from oldTable
    for column in orig_table.columns:
        new_table.append_column(column.copy())
    new_table.create()
    return new_table

def write_to_new_table(data, filename):
    #filename not used here but want to use a callback in 
    #write to file... 
    engine = connect_db("DublinBikeProjectDB.cun91scffwzf.eu-west-1.rds.amazonaws.com", "3306", "DublinBikeProjectDB", "theForkAwakens", "db_password.txt")
    Session = sessionmaker(bind=engine)
    session = Session()
    
    for i in data:
        try:
            banking = 1 if (i['banking']) else 0
            bonus = 1 if (i['bonus']) else 0

            station = Station(station_number=i["number"],
                                    station_name=i["name"],
                                    station_address=i["address"],
                                    station_loc_lat=i["position"]["lat"],
                                    station_loc_long=i["position"]["lng"],
                                    banking_available=banking,
                                    bonus=bonus)
            
            session.add(station)
            session.commit()

        except Exception as e:
            print("Error Type: ", type(e))
            print("Error Details: ", e)
            session.rollback()
            continue
    
    session.close()
    engine.dispose()
merge()
'''
Created on Apr 17, 2017

@author: Katherine
'''
