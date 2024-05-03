'''
SOUTH KOREA COVID-19 DATABASE CREATION

BY: Harsheit Budhwar
PENNSYLVANIA STATE UNIVERSITY
'''
#==================================================================================#
#==================================================================================#

import psycopg2
import csv



# Connect to PostgreSQL Database
def connect_database(usr, pword, db):
    # For some reason the function parameter autoset isn't working
    if len(usr) == 0:
        usr = "postgres"
    if len(pword) == 0:
        pword = "hvb"

    try:
        connection = psycopg2.connect(
            user = usr,
            password = pword,
            host = "localhost",
            port = "5432",
            database = db,
        )

    except Exception as error:
        print("Error connecting to database " + db)
        print(error)
        return "Error"
    
    return connection





def create_database():
    # Get user info
    user = input("Username [postgres]: ")
    password = input("Password [hvb]: ")


    # Create SK Covid-19 DB
    conn = connect_database(user, password, "postgres")
    if conn == "Error" or conn == None:
        print ("Error creating database")
        return "Error"
    
    cur = conn.cursor()
    
    # Sets autocommit on (Thx stackoverflow <3)
    conn.autocommit = True

    cur.execute('DROP DATABASE IF EXISTS south_korea_covid19_db;')
    cur.execute('CREATE DATABASE south_korea_covid19_db;')
    
    print("Database created")
    conn.close()




    # Connect to SK Covid-19 DB
    conn = connect_database(user, password, "south_korea_covid19_db")
    if conn == "Error" or conn == None:
        print ("Error connecting to database")
        return "Error"
    
    cur = conn.cursor()
    
    # Sets autocommit on (Thx stackoverflow <3)
    conn.autocommit = True
    
    print("Database connected")

    
    
    # Generate database tables
    try:
        cursor = conn.cursor()
        cursor.execute("""
                    CREATE TABLE Time_(
                        date DATE NOT NULL PRIMARY KEY,
                        test INTEGER NOT NULL,
                        negative INTEGER NOT NULL,
                        confirmed INTEGER NOT NULL,
                        released INTEGER NOT NULL,
                        deceased INTEGER NOT NULL
                    );
                    
                    CREATE TABLE PatientInfo(
                        patient_id BIGINT NOT NULL PRIMARY KEY,
                        sex VARCHAR(10),
                        age VARCHAR(18),
                        province VARCHAR(255) NOT NULL,
                        city VARCHAR(255),
                        infection_case VARCHAR(255),
                        contact_number VARCHAR(255),
                        confirmed_date DATE,
                        state VARCHAR(255) NOT NULL
                    );
                       
                    CREATE TABLE Case_(
                        case_id INTEGER NOT NULL PRIMARY KEY,
                        province VARCHAR(255) NOT NULL,
                        city VARCHAR(255) NOT NULL,
                        group_ VARCHAR(255) NOT NULL,
                        infection_case VARCHAR(255) NOT NULL,
                        confirmed INTEGER NOT NULL
                    );
                       
                    CREATE TABLE Weather(
                        code INTEGER NOT NULL,
                        province VARCHAR(255) NOT NULL,
                        date DATE NOT NULL,
                        avg_temp NUMERIC(10,1),
                        min_temp NUMERIC(10,1),
                        max_temp NUMERIC(10,1),
                        precipitation NUMERIC(10,1),
                        max_wind_speed NUMERIC(10,1),
                        most_wind_direction INTEGER,
                        avgrelative_humidity NUMERIC(10,1),
                       
                        PRIMARY KEY(code, date)
                    );
                       
                    CREATE TABLE SearchTrends(
                        date DATE NOT NULL PRIMARY KEY,
                        cold NUMERIC(10,5) NOT NULL,
                        flu NUMERIC(10,5) NOT NULL,
                        pneumonia NUMERIC(10,5) NOT NULL,
                        coronavirus NUMERIC(10,5) NOT NULL
                    );
                       
                    CREATE TABLE Policy_(
                        policy_id INTEGER NOT NULL PRIMARY KEY,
                        country VARCHAR(255) NOT NULL,
                        type VARCHAR(255) NOT NULL,
                        gov_policy VARCHAR(255) NOT NULL,
                        detail_ VARCHAR(255),
                        start_date DATE NOT NULL,
                        end_date DATE
                    );
                       
                    CREATE TABLE Region(
                       code INTEGER NOT NULL PRIMARY KEY,
                       province VARCHAR(255) NOT NULL,
                       city VARCHAR(255) NOT NULL,
                       elementary_school_count INTEGER NOT NULL,
                       kindergarten_count INTEGER NOT NULL,
                       university_count INTEGER NOT NULL,
                       nursing_home_count INTEGER NOT NULL
                    );

                    """)

    
    except psycopg2.DatabaseError as error:
        print("Error creating database tables")
        print(error)
        conn.close()
        return "Error"

    print("Database tables created")

    
    # Fill database with data
    try:
        dataset_location = input("Enter folder path for dataset [E:\\hersh\\Downloads\\Covid19 Data]: ")
        if len(dataset_location) == 0:
            dataset_location = "E:\\hersh\\Downloads\\Covid19 Data"

            
        file_loc = dataset_location + "\\Case.csv"
        with open(file_loc, "r") as f:
            cur.copy_expert("COPY Case_ FROM STDIN WITH DELIMITER ',' CSV HEADER;", f)
            print("Case_ filled")

        file_loc = dataset_location + "\\PatientInfo.csv"
        with open(file_loc, "r") as f:
            cur.copy_expert("COPY PatientInfo FROM STDIN WITH DELIMITER ',' CSV HEADER;", f)
            print("PatientInfo filled")

        file_loc = dataset_location + "\\Policy.csv"
        with open(file_loc, "r") as f:
            cur.copy_expert("COPY Policy_ FROM STDIN WITH DELIMITER ',' CSV HEADER;", f)
            print("Policy filled")

        file_loc = dataset_location + "\\Region.csv"
        with open(file_loc, "r") as f:
            cur.copy_expert("COPY Region FROM STDIN WITH DELIMITER ',' CSV HEADER;", f)
            print("Region filled")

        file_loc = dataset_location + "\\SearchTrend.csv"
        with open(file_loc, "r") as f:
            cur.copy_expert("COPY SearchTrends FROM STDIN WITH DELIMITER ',' CSV HEADER;", f)
            print("SearchTrends filled")

        file_loc = dataset_location + "\\Time.csv"
        with open(file_loc, "r") as f:
            cur.copy_expert("COPY Time_ FROM STDIN WITH DELIMITER ',' CSV HEADER;", f)
            print("Time_ filled")

        file_loc = dataset_location + "\\Weather.csv"
        with open(file_loc, "r") as f:
            cur.copy_expert("COPY Weather FROM STDIN WITH DELIMITER ',' CSV HEADER;", f)
            print("Weather filled")


    except psycopg2.DatabaseError as error:
        print("Error uploading data to database tables")
        print(error)
        conn.close()
        return "Error"

    

    print("Database tables filled")
    conn.close()

    print("\nDatabase creation completed")
    print("\nPlease run CLI_main.py to interact with database.")



create_database()