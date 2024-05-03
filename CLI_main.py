'''
SOUTH KOREA COVID-19 DATABASE MANAGEMENT CLI

BY: Harsheit Budhwar
PENNSYLVANIA STATE UNIVERSITY
'''
#==================================================================================#
#==================================================================================#

import psycopg2
import pandas as pd
from tabulate import tabulate




#### Global variables. Mainly for Transaction

# Autocommit 
def set_Autocommit_On():
    global autocommit
    autocommit = True
def set_Autocommit_Off():
    global autocommit
    autocommit = False


def set_Username(name = "postgres"):
    global user
    user = name
def set_Password(passw = "hvb"):
    global password
    password = passw



# Connect to PostgreSQL Database
def connect_database(usr, pword):
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
            database = "south_korea_covid19_db",
        )

    except Exception as error:
        print("Error connecting to database")
        print(error)
        return "Error"
    
    return connection


# Connection and cursor 
def make_Connection():
    global con
    global main_cursor
    con = None

    username = input("Username [postgres]: ")
    password = input("Password [hvb]: ")

    try:  
        con = connect_database(username, password)
        if con == "Error":
            return 1
        main_cursor = con.cursor()
        return 0

    except Exception as error:
        print("Error occured while connecting to database. Exiting")
        return 1



# Main (menu)
def main_menu():
    
    # During initalization of code, set autocommit to on
    set_Autocommit_On()

    # Make Connection
    if(make_Connection() == 1): return()

    
    print("\nWelcome to the South Korea COVID-19 Database\n")
    inp = ""

    while inp == "":
        print("Autocommit: " + str(autocommit))
        print()
        print("Please select an option:")
        print("1- Insert Data")
        print("2- Delete Data")
        print("3- Update Data")
        print("4- Search Data")
        print("5- Aggregate Function")
        print("6- Sortings")
        print("7- Joins")
        print("8- Grouping")
        print("9- Subqueries")
        print("10- Transaction Control")
        print("X- Exit\n")

        inp = input("")


        

        # Input junction. If the function returns 0, it goes back to the main menu
        if inp == "1":
            if (sql_insert(main_cursor)) == 0:
                inp = ""
                print("\n")

        elif inp == "2": 
            if (sql_delete(main_cursor)) == 0:
                inp = ""
                print("\n")

        elif inp == "3": 
            if (sql_update(main_cursor)) == 0:
                inp = ""
                print("\n")

        elif inp == "4": 
            if (sql_search(main_cursor)) == 0:
                inp = ""
                print("\n")

        elif inp == "5": 
            if (sql_aggregate(main_cursor)) == 0:
                inp = ""
                print("\n")

        elif inp == "6": 
            if (sql_sorting(main_cursor)) == 0:
                inp = ""
                print("\n")

        elif inp == "7": 
            if (sql_joins(main_cursor)) == 0:
                inp = ""
                print("\n")

        elif inp == "8": 
            if (sql_grouping(main_cursor)) == 0:
                inp = ""
                print("\n")

        elif inp == "9": 
            if (sql_subqueries(main_cursor)) == 0:
                inp = ""
                print("\n")

        elif inp == "10": 
            if (sql_transactions(main_cursor)) == 0:
                inp = ""
                print("\n")

        elif inp.upper() == "X":
            # Have some manners and say bye!
            print("Goodbye!\n")
            # Close connection 
            con.close()
            return
        else:
            print("Not a valid input\n")
            inp = ""



# Function to execute the querty commands and handle errors
def execute_query(query, args=None, transaction_code=None, get_headers = False):

    try:
       # Transaction code execution
        if (transaction_code != None):
            if(transaction_code == "C"):
                print("Committing transaction...")
                con.commit()
            if(transaction_code == "R"):
                con.rollback()
                print("Rolling back transaction...")
            return "TC recieved"
        
        # Run the query
        if (args != None):
            main_cursor.execute(query, args)
        else:
            main_cursor.execute(query)

        # Return content for SELECT queries
        output = None
        if (str(query).strip().lower()[0:6]) == "select":
            output = main_cursor.fetchall()

        # Commit the changes to the database
        if(autocommit == True):
            if(get_headers):
                # Don't output if it's just getting headers bc that's silly :3
                print("Committing query to database...")
            con.commit()      

        return output
    
    # Error occured at runtime
    except psycopg2.DatabaseError as error:

        # Discard the query changes
        if (con != None):
            print("Error occured. Rolling back")
            con.rollback()
            if (not autocommit):
                set_Autocommit_On()
                print("AutoCommit is now on")
        
        # Report out error
        print("The entered query encountered an error at runtime:")
        print(error)
        #raise
        return "Error"





def sql_insert(cur):
    
    # Declare Variables
    inp = ""
    table_options = {1:"case_", 2:"patientinfo", 3:"time_", 4:"weather", 5:"searchtrends", 6: "region", 7: "policy_"}
    
    
    

    while inp == "":

        # Print insert menu
        print("Select a table to insert data into:")
        print("1- Case (case_)")
        print("2- Patient (patientinfo)")
        print("3- Date (time_)")
        print("4- Weather (weather)")
        print("5- Search Trends (searchtrends)")
        print("6- Region (region)")
        print("7- Policy (policy)")
        print("X- Back to Menu")
        print()


        table_num = input()
        valid_inp = None

        # Return to menu
        if table_num.upper() == "X":
            break

        # Case selected
        if table_num == "1":
            print("Enter row data in following schema: case_id: INT, province: STR(255), city: STR(255), group: STR(255), infection_case: STR(255), confirmed: INT")
            print("Example: 100,'Seoul','Jung-gu',TRUE,'McDonalds', 3")
            
            schema_inp = input()

            # Check inputted schema 
            validate_inp = schema_inp.split(",")
            try: 
                validate_inp[0] = int(validate_inp[0])
                validate_inp[1] = str(validate_inp[1])
                validate_inp[2] = str(validate_inp[2])
                validate_inp[3] = str(validate_inp[3])
                validate_inp[4] = str(validate_inp[4])
                validate_inp[5] = int(validate_inp[5])

                valid_inp = True
            except:
                valid_inp = False


        # PatientInfo selected
        if table_num == "2":
            print("Enter row data in following schema: patient_id: INT, sex: STR(10), age: STR(10), province: STR(255), city: STR(255), infection_case: STR(255), contact_number: STR(255), confirmed_date: DATE, state: STR(255)")
            print("Example: 100,'female','30s','Seoul','Jung-gu','McDonalds', 0, '2020-1-23','released'")
            
            schema_inp = input()

            # Check inputted schema 
            validate_inp = schema_inp.split(",")
            try: 
                validate_inp[0] = int(validate_inp[0])
                validate_inp[1] = str(validate_inp[1])
                validate_inp[2] = str(validate_inp[2])
                validate_inp[3] = str(validate_inp[3])
                validate_inp[4] = str(validate_inp[4])
                validate_inp[5] = str(validate_inp[5])
                validate_inp[6] = str(validate_inp[6])
                validate_inp[7] = str(validate_inp[7])
                validate_inp[8] = str(validate_inp[8])

                valid_inp = True
            except:
                valid_inp = False



        # Date selected
        if table_num == "3":
            print("Enter row data in following schema: date: DATE, test: INT, negative: INT, confirmed: INT, released: INT, deceased: INT")
            print("Example: '2013-01-20', 1, 2, 3, 4, 5")
            
            schema_inp = input()

            # Check inputted schema 
            validate_inp = schema_inp.split(",")
            try: 
                validate_inp[0] = str(validate_inp[0])
                validate_inp[1] = int(validate_inp[1])
                validate_inp[2] = int(validate_inp[2])
                validate_inp[3] = int(validate_inp[3])
                validate_inp[4] = int(validate_inp[4])
                validate_inp[5] = int(validate_inp[5])


                valid_inp = True
            except:
                valid_inp = False



        # Weather selected
        if table_num == "4":
            print("Enter row data in following schema: code: INT, province: STR(255), date: DATE, avg_temp: FLOAT(10,1), min_temp: FLOAT(10,1), max_temp: FLOAT(10,1), precipitation: FLOAT(10,1), max_wind_speed: FLOAT(10,1), most_wind_direction : INT, avg_relative_humidity: FLOAT(10,1)")
            print("Example: 10000,'Seoul','2013-01-20', 1.2, -2.3, 4.0, 0.0, 3.5, 90, 73.0")
            
            schema_inp = input()

            # Check inputted schema 
            validate_inp = schema_inp.split(",")
            try: 
                validate_inp[0] = int(validate_inp[0])
                validate_inp[1] = str(validate_inp[1])
                validate_inp[2] = str(validate_inp[2])
                validate_inp[3] = float(validate_inp[3])
                validate_inp[4] = float(validate_inp[4])
                validate_inp[5] = float(validate_inp[5])
                validate_inp[6] = float(validate_inp[6])
                validate_inp[7] = float(validate_inp[7])
                validate_inp[8] = int(validate_inp[8])
                validate_inp[9] = float(validate_inp[9])

                valid_inp = True
            except:
                valid_inp = False



        # Search Trends selected
        if table_num == "5":
            print("Enter row data in following schema: date: DATE, cold: FLOAT(10,5), flu: FLOAT(10,5), pneumonia: FLOAT(10,5), coronavirus: FLOAT(10,5)")
            print("Example: '2013-01-01', 0.11663, 0.05590, 0.15726, 0.00736")
            
            schema_inp = input()

            # Check inputted schema 
            validate_inp = schema_inp.split(",")
            try: 
                validate_inp[0] = str(validate_inp[0])
                validate_inp[1] = float(validate_inp[1])
                validate_inp[2] = float(validate_inp[2])
                validate_inp[3] = float(validate_inp[3])
                validate_inp[4] = float(validate_inp[4])


                valid_inp = True
            except:
                valid_inp = False



        # Region selected
        if table_num == "6":
            print("Enter row data in following schema: code: INT, province: STR(255), city: STR(255), elementary_school_count: INT, kindergarten_count: INT, university_count: INT, nursing_home_count: INT")
            print("Example: 10241,'Seoul','Jung-gu2', 12, 14, 2, 728")
            
            schema_inp = input()

            # Check inputted schema 
            validate_inp = schema_inp.split(",")
            try: 
                validate_inp[0] = int(validate_inp[0])
                validate_inp[1] = str(validate_inp[1])
                validate_inp[2] = str(validate_inp[2])
                validate_inp[3] = int(validate_inp[3])
                validate_inp[4] = int(validate_inp[4])
                validate_inp[5] = int(validate_inp[5])
                validate_inp[6] = int(validate_inp[6])

                valid_inp = True
            except:
                valid_inp = False



        # Policy selected
        if table_num == "7":
            print("Enter row data in following schema: policy_id: INT, country: STR(255), type: STR(255), gov_policy: STR(255), detail: STR(255), start_date: DATE, end_date: OPTIONAL DATE")
            print("Example: 0,'Korea','Alert','Infectious Disease Alert Level','Level 0 (Green)', '2013-01-03', '2028-01-19'")
            
            schema_inp = input()

            # Check inputted schema 
            validate_inp = schema_inp.split(",")
            try: 
                validate_inp[0] = int(validate_inp[0])
                validate_inp[1] = str(validate_inp[1])
                validate_inp[2] = str(validate_inp[2])
                validate_inp[3] = str(validate_inp[3])
                validate_inp[4] = str(validate_inp[4])
                validate_inp[5] = str(validate_inp[5])
                validate_inp[6] = str(validate_inp[6])

                valid_inp = True
            except:
                valid_inp = False


        # No choice selected
        if valid_inp == None:
            print("Please select a choice\n")
            inp = ""


        # If the check passed, run the query to the database
        if valid_inp == True:
            query = f"INSERT INTO {table_options[int(table_num)]} VALUES ({schema_inp});"

            # Error messages will be handled by execute_query()
            print("Executing...")
            if (execute_query(query)) == None:
                print("Executed succesfully\n")
        
        

        # This is the only error that can occur at this part
        if valid_inp == False:
            print("Invalid Schema entered\n")
                
    
    return 0



def sql_delete(cur):
    
    # Declare Variables
    inp = ""
    table_options = {1:"case_", 2:"patientinfo", 3:"time_", 4:"weather", 5:"searchtrends", 6: "region", 7: "policy_"}
    
    
    

    while inp == "":

        # Print delete menu
        print("1- Case (case_)")
        print("2- Patient (patientinfo)")
        print("3- Date (time_)")
        print("4- Weather (weather)")
        print("5- Search Trends (searchtrends)")
        print("6- Region (region)")
        print("7- Policy (policy)")
        print("X- Back to Menu")
        print()


        table_num = input()
        valid_inp = None

        # Return to menu
        if table_num.upper() == "X":
            break

        # Case selected
        if table_num == "1":
            print("Enter a condition based on the following schema: case_id: INT, province: STR(255), city: STR(255), group: STR(255), infection_case: STR(255), confirmed: INT")
            print("Example: case_id = 100")
            
            valid_inp = True # Valid_imp here means that they selected a valid table
            schema_inp = input()
            

        # PatientInfo selected
        if table_num == "2":
            print("Enter a condition based on the following schema: patient_id: INT, sex: STR(10), age: STR(10), province: STR(255), city: STR(255), infection_case: STR(255), contact_number: STR(255), confirmed_date: DATE, state: STR(255)")
            print("Example: patient_id = 100")
            
            valid_inp = True # Valid_imp here means that they selected a valid table
            schema_inp = input()
            

        # Date selected
        if table_num == "3":
            print("Enter a condition based on the following schema: date: DATE, test: INT, negative: INT, confirmed: INT, released: INT, deceased: INT")
            print("Example: date = '2013-01-20'")
            
            valid_inp = True # Valid_imp here means that they selected a valid table
            schema_inp = input()
            

        # Weather selected
        if table_num == "4":
            print("Enter a condition based on the following schema: code: INT, province: STR(255), date: DATE, avg_temp: FLOAT(10,1), min_temp: FLOAT(10,1), max_temp: FLOAT(10,1), precipitation: FLOAT(10,1), max_wind_speed: FLOAT(10,1), most_wind_direction : INT, avg_relative_humidity: FLOAT(10,1)")
            print("Example: code = 10000 AND date = '2013-01-20'")
            
            valid_inp = True # Valid_imp here means that they selected a valid table
            schema_inp = input()
            

        # Search Trends selected
        if table_num == "5":
            print("Enter a condition based on the following schema: date: DATE, cold: FLOAT(10,5), flu: FLOAT(10,5), pneumonia: FLOAT(10,5), coronavirus: FLOAT(10,5)")
            print("Example: date = '2013-01-01'")
            
            valid_inp = True # Valid_imp here means that they selected a valid table
            schema_inp = input()


        # Region selected
        if table_num == "6":
            print("Enter a condition based on the following schema: code: INT, province: STR(255), city: STR(255), elementary_school_count: INT, kindergarten_count: INT, university_count: INT, nursing_home_count: INT")
            print("Example: code = 10241")
            
            valid_inp = True # Valid_imp here means that they selected a valid table
            schema_inp = input()


        # Policy selected
        if table_num == "7":
            print("Enter a condition based on the following schema: policy_id: INT, country: STR(255), type: STR(255), gov_policy: STR(255), detail: STR(255), start_date: DATE, end_date: OPTIONAL DATE")
            print("Example: policy_id = 0")
            
            valid_inp = True # Valid_imp here means that they selected a valid table
            schema_inp = input()
        

        # No choice selected
        if valid_inp == None:
            print("Please select a choice\n")
            inp = ""

        # No condition entered
        if schema_inp == "":
            print("Please enter a condition\n")
            valid_inp = None
        


        # If the check passed, run the query to the database
        if valid_inp == True:
            query = f"DELETE FROM {table_options[int(table_num)]} WHERE {schema_inp};"

            # Error messages will be handled by execute_query()
            print("Executing...")
            if (execute_query(query)) == None:
                print("Executed succesfully\n")



        # This is the only error that can occur at this part
        if valid_inp == False:
            print("Invalid Schema entered\n")
                
    
    return 0



def sql_update(cur):
    # Declare Variables
    inp = ""
    table_options = {1:"case_", 2:"patientinfo", 3:"time_", 4:"weather", 5:"searchtrends", 6: "region", 7: "policy_"}
    
    
    

    while inp == "":

        # Print update menu
        print("Select a table to update data of:")
        print("1- Case (case_)")
        print("2- Patient (patientinfo)")
        print("3- Date (time_)")
        print("4- Weather (weather)")
        print("5- Search Trends (searchtrends)")
        print("6- Region (region)")
        print("7- Policy (policy)")
        print("X- Back to Menu")
        print()


        table_num = input()
        valid_inp = None

        # Return to menu
        if table_num.upper() == "X":
            break

        # Case selected
        if table_num == "1":
            
            valid_inp = True # Valid_imp here means that they selected a valid table
           
            print("Enter a condition based on the following schema: case_id: INT, province: STR(255), city: STR(255), group: STR(255), infection_case: STR(255), confirmed: INT")
            print("Example: case_id = 100")
            
            schema_inp = input()
            
            print("Enter the new value based on the following schema: case_id: INT, province: STR(255), city: STR(255), group: STR(255), infection_case: STR(255), confirmed: INT")
            print("Example: case_id = 101")
            
            expr_inp = input()

            

        # PatientInfo selected
        if table_num == "2":

            valid_inp = True # Valid_imp here means that they selected a valid table

            print("Enter a condition based on the following schema: patient_id: INT, sex: STR(10), age: STR(10), province: STR(255), city: STR(255), infection_case: STR(255), contact_number: STR(255), confirmed_date: DATE, state: STR(255)")
            print("Example: patient_id = 100")
            
            schema_inp = input()
            
            print("Enter the new value based on the following schema: patient_id: INT, sex: STR(10), age: STR(10), province: STR(255), city: STR(255), infection_case: STR(255), contact_number: STR(255), confirmed_date: DATE, state: STR(255)")
            print("Example: patient_id = 101")
            
            expr_inp = input()

            

        # Date selected
        if table_num == "3":

            valid_inp = True # Valid_imp here means that they selected a valid table

            print("Enter a condition based on the following schema: date: DATE, test: INT, negative: INT, confirmed: INT, released: INT, deceased: INT")
            print("Example: date = '2013-01-20'")
            
        
            schema_inp = input()
            
            print("Enter the new value based on the following schema: DATE, test: INT, negative: INT, confirmed: INT, released: INT, deceased: INT")
            print("Example: date = '2013-01-21'")
            
            expr_inp = input()



        # Weather selected
        if table_num == "4":

            valid_inp = True # Valid_imp here means that they selected a valid table

            print("Enter a condition based on the following schema: code: INT, province: STR(255), date: DATE, avg_temp: FLOAT(10,1), min_temp: FLOAT(10,1), max_temp: FLOAT(10,1), precipitation: FLOAT(10,1), max_wind_speed: FLOAT(10,1), most_wind_direction : INT, avg_relative_humidity: FLOAT(10,1)")
            print("Example: code = 10000 AND date = '2013-01-20'")
            
            schema_inp = input()
            
            print("Enter the new value based on the following schema: code: INT, province: STR(255), date: DATE, avg_temp: FLOAT(10,1), min_temp: FLOAT(10,1), max_temp: FLOAT(10,1), precipitation: FLOAT(10,1), max_wind_speed: FLOAT(10,1), most_wind_direction : INT, avg_relative_humidity: FLOAT(10,1)")
            print("Example: code = '10002' AND date = '2013-01-21'")
            
            expr_inp = input()


        # Search Trends selected
        if table_num == "5":

            valid_inp = True # Valid_imp here means that they selected a valid table

            print("Enter a condition based on the following schema: date: DATE, cold: FLOAT(10,5), flu: FLOAT(10,5), pneumonia: FLOAT(10,5), coronavirus: FLOAT(10,5)")
            print("Example: date = '2013-01-01'")
            
            schema_inp = input()

            print("Enter the new value based on the following schema: date: DATE, cold: FLOAT(10,5), flu: FLOAT(10,5), pneumonia: FLOAT(10,5), coronavirus: FLOAT(10,5)")
            print("Example: date = '2013-01-06'")
            
            expr_inp = input()


        # Region selected
        if table_num == "6":

            valid_inp = True # Valid_imp here means that they selected a valid table

            print("Enter a condition based on the following schema: code: INT, province: STR(255), city: STR(255), elementary_school_count: INT, kindergarten_count: INT, university_count: INT, nursing_home_count: INT")
            print("Example: code = 10241")
            
            
            schema_inp = input()

            print("Enter the new value based on the following schema: code: INT, province: STR(255), city: STR(255), elementary_school_count: INT, kindergarten_count: INT, university_count: INT, nursing_home_count: INT")
            print("Example: code = 10245")
            
            expr_inp = input()



        # Policy selected
        if table_num == "7":

            valid_inp = True # Valid_imp here means that they selected a valid table

            print("Enter a condition based on the following schema: policy_id: INT, country: STR(255), type: STR(255), gov_policy: STR(255), detail: STR(255), start_date: DATE, end_date: OPTIONAL DATE")
            print("Example: policy_id = 0")
            
            schema_inp = input()
            
            print("Enter the new value based on the following schema: policy_id: INT, country: STR(255), type: STR(255), gov_policy: STR(255), detail: STR(255), start_date: DATE, end_date: OPTIONAL DATE")
            print("Example: policy_id = 69")
            
            expr_inp = input()



        # No choice selected
        if valid_inp == None:
            print("Please select a choice\n")
            inp = ""

        # No condition entered
        if schema_inp == "":
            print("Please enter a condition\n")
            valid_inp = None

        # No expression entered
        if expr_inp == "":
            print("Please enter a condition\n")
            valid_inp = None
        


        # If the check passed, run the query to the database
        if valid_inp == True:
            query =  f"UPDATE {table_options[int(table_num)]} SET {expr_inp} WHERE {schema_inp};"
           
            # Error messages will be handled by execute_query()
            print("Executing...")
            if (execute_query(query)) == None:
                print("Executed succesfully\n")



        # This is the only error that can occur at this part
        if valid_inp == False:
            print("Invalid Schema entered\n")
                
    
    return 0



def sql_search(cur):
    
    # Declare Variables
    inp = ""
    table_options = {1:"case_", 2:"patientinfo", 3:"time_", 4:"weather", 5:"searchtrends", 6: "region", 7: "policy_"}
    
    
    

    while inp == "":

        # Print search menu
        print("Select a table to search data from:")
        print("1- Case (case_)")
        print("2- Patient (patientinfo)")
        print("3- Date (time_)")
        print("4- Weather (weather)")
        print("5- Search Trends (searchtrends)")
        print("6- Region (region)")
        print("7- Policy (policy)")
        print("X- Back to Menu")
        print()


        table_num = input()
        valid_inp = None

        # Return to menu
        if table_num.upper() == "X":
            break

        # Case selected
        if table_num == "1":
            print("Enter a condition based on the following schema: case_id: INT, province: STR(255), city: STR(255), group: STR(255), infection_case: STR(255), confirmed: INT")
            print("Example: case_id = 100")
            
            valid_inp = True # Valid_imp here means that they selected a valid table
            schema_inp = input()
            

        # PatientInfo selected
        if table_num == "2":
            print("Enter a condition based on the following schema: patient_id: INT, sex: STR(10), age: STR(10), province: STR(255), city: STR(255), infection_case: STR(255), contact_number: STR(255), confirmed_date: DATE, state: STR(255)")
            print("Example: patient_id = 100")
            
            valid_inp = True # Valid_imp here means that they selected a valid table
            schema_inp = input()
            

        # Date selected
        if table_num == "3":
            print("Enter a condition based on the following schema: date: DATE, test: INT, negative: INT, confirmed: INT, released: INT, deceased: INT")
            print("Example: date = '2013-01-20'")
            
            valid_inp = True # Valid_imp here means that they selected a valid table
            schema_inp = input()
            

        # Weather selected
        if table_num == "4":
            print("Enter a condition based on the following schema: code: INT, province: STR(255), date: DATE, avg_temp: FLOAT(10,1), min_temp: FLOAT(10,1), max_temp: FLOAT(10,1), precipitation: FLOAT(10,1), max_wind_speed: FLOAT(10,1), most_wind_direction : INT, avg_relative_humidity: FLOAT(10,1)")
            print("Example: code = 10000 AND date = '2013-01-20'")
            
            valid_inp = True # Valid_imp here means that they selected a valid table
            schema_inp = input()
            

        # Search Trends selected
        if table_num == "5":
            print("Enter a condition based on the following schema: date: DATE, cold: FLOAT(10,5), flu: FLOAT(10,5), pneumonia: FLOAT(10,5), coronavirus: FLOAT(10,5)")
            print("Example: date = '2013-01-01'")
            
            valid_inp = True # Valid_imp here means that they selected a valid table
            schema_inp = input()


        # Region selected
        if table_num == "6":
            print("Enter a condition based on the following schema: code: INT, province: STR(255), city: STR(255), elementary_school_count: INT, kindergarten_count: INT, university_count: INT, nursing_home_count: INT")
            print("Example: code = 10241")
            
            valid_inp = True # Valid_imp here means that they selected a valid table
            schema_inp = input()


        # Policy selected
        if table_num == "7":
            print("Enter a condition based on the following schema: policy_id: INT, country: STR(255), type: STR(255), gov_policy: STR(255), detail: STR(255), start_date: DATE, end_date: OPTIONAL DATE")
            print("Example: policy_id = 0")
            
            valid_inp = True # Valid_imp here means that they selected a valid table
            schema_inp = input()
        

        # No choice selected
        if valid_inp == None:
            print("Please select a choice\n")
            inp = ""

        # No condition entered
        if schema_inp == "":
            print("Please enter a condition\n")
            valid_inp = None
        


        # If the check passed, run the query to the database
        if valid_inp == True:

            print("Executing...")

            # Get the table headers
            query = f"SELECT column_name FROM information_schema.columns WHERE table_schema = 'public' AND table_name = '{table_options[int(table_num)]}';"
            search_columns = execute_query(query, get_headers=True)

            # Convert returned headers into a good format
            fixed_search_columns = []
            for i in range(len(search_columns)):
                fixed_search_columns.append(search_columns[i][0])


            # Get search results
            query = f"SELECT * FROM {table_options[int(table_num)]} WHERE {schema_inp};"

            # Error messages will be handled by execute_query()
            search_output = execute_query(query)
            if search_output != None and search_output != "Error":
                print("Executed successfully")

                # Try to make pretty output
                try:
                    #Convert to pandas dataframe for better output layout because we're fancy like that :D
                    df = pd.DataFrame(search_output, columns=fixed_search_columns)
                    print(tabulate(df, headers='keys', tablefmt='psql'))
                except:
                    df = pd.DataFrame(search_output)
                    print(tabulate(df, headers='keys', tablefmt='psql'))
            
            else:
                print("Could not output due to error\n")
                return 0
                

        # This is the only error that can occur at this part
        if valid_inp == False:
            print("Invalid Schema entered\n")
                
    
    return 0



def sql_aggregate(cur):

    # Declare Variables
    inp = ""
    table_options = {1:"case_", 2:"patientinfo", 3:"time_", 4:"weather", 5:"searchtrends", 6: "region", 7: "policy_"}
    
    
    

    while inp == "":

        # Print search menu
        print("Select a table to search data from:")
        print("1- Case (case_)")
        print("2- Patient (patientinfo)")
        print("3- Date (time_)")
        print("4- Weather (weather)")
        print("5- Search Trends (searchtrends)")
        print("6- Region (region)")
        print("7- Policy (policy)")
        print("X- Back to Menu")
        print()


        table_num = input()
        valid_inp = None

        # Return to menu
        if table_num.upper() == "X":
            break

        # Case selected
        if table_num == "1":
            print("Enter the column to aggregate with from the following schema: case_id: INT, province: STR(255), city: STR(255), group: STR(255), infection_case: STR(255), confirmed: INT")
            print("Example: 'case_id'")
            
            valid_inp = True # Valid_imp here means that they selected a valid table
            schema_inp = input()
            

        # PatientInfo selected
        if table_num == "2":
            print("Enter the column to aggregate with from the following schema: patient_id: INT, sex: STR(10), age: STR(10), province: STR(255), city: STR(255), infection_case: STR(255), contact_number: STR(255), confirmed_date: DATE, state: STR(255)")
            print("Example: 'patient_id'")
            
            valid_inp = True # Valid_imp here means that they selected a valid table
            schema_inp = input()
            

        # Date selected
        if table_num == "3":
            print("Enter the column to aggregate with from the following schema: date: DATE, test: INT, negative: INT, confirmed: INT, released: INT, deceased: INT")
            print("Example: 'date'")
            
            valid_inp = True # Valid_imp here means that they selected a valid table
            schema_inp = input()
            

        # Weather selected
        if table_num == "4":
            print("Enter the column to aggregate with from the following schema: code: INT, province: STR(255), date: DATE, avg_temp: FLOAT(10,1), min_temp: FLOAT(10,1), max_temp: FLOAT(10,1), precipitation: FLOAT(10,1), max_wind_speed: FLOAT(10,1), most_wind_direction : INT, avg_relative_humidity: FLOAT(10,1)")
            print("Example: 'code'")
            
            valid_inp = True # Valid_imp here means that they selected a valid table
            schema_inp = input()
            

        # Search Trends selected
        if table_num == "5":
            print("Enter the column to aggregate with from the following schema: date: DATE, cold: FLOAT(10,5), flu: FLOAT(10,5), pneumonia: FLOAT(10,5), coronavirus: FLOAT(10,5)")
            print("Example: 'date'")
            
            valid_inp = True # Valid_imp here means that they selected a valid table
            schema_inp = input()


        # Region selected
        if table_num == "6":
            print("Enter the column to aggregate with from the following schema: code: INT, province: STR(255), city: STR(255), elementary_school_count: INT, kindergarten_count: INT, university_count: INT, nursing_home_count: INT")
            print("Example: 'code'")
            
            valid_inp = True # Valid_imp here means that they selected a valid table
            schema_inp = input()


        # Policy selected
        if table_num == "7":
            print("Enter the column to aggregate with from the following schema: policy_id: INT, country: STR(255), type: STR(255), gov_policy: STR(255), detail: STR(255), start_date: DATE, end_date: OPTIONAL DATE")
            print("Example: 'policy_id'")
            
            valid_inp = True # Valid_imp here means that they selected a valid table
            schema_inp = input()

        
        print("Enter the aggregate function such as 'AVG', 'COUNT', 'MAX', 'MIN', 'SUM', ...")
        expr_inp = input()
        

        # No choice selected
        if valid_inp == None:
            print("Please select a choice\n")
            inp = ""

        # No condition entered
        if schema_inp == "":
            print("Please enter a condition\n")
            valid_inp = None

        # No aggregate function entered
        if expr_inp == "":
            print("Please enter a function\n")
            valid_inp = None
        


        # If the check passed, run the query to the database
        if valid_inp == True:


            print("Executing...")



            # Get search results
            query = f"SELECT {expr_inp}({schema_inp}) FROM {table_options[int(table_num)]};"

            # Error messages will be handled by execute_query()
            search_output = execute_query(query)
            if search_output != None and search_output != "Error":
                print("Executed successfully")
                print("Result: " + str(search_output[0][0]) + "\n")
            
            else:
                print("Could not output due to error\n")
                return 0



        # This is the only error that can occur at this part
        if valid_inp == False:
            print("Invalid Schema entered\n")
                
    
    return 0



def sql_sorting(cur):
    
    # Declare Variables
    inp = ""
    table_options = {1:"case_", 2:"patientinfo", 3:"time_", 4:"weather", 5:"searchtrends", 6: "region", 7: "policy_"}
    
    
    

    while inp == "":
        
        # Print sort menu
        print("Select a table to sort data of:")
        print("1- Case")
        print("2- Patient")
        print("3- Date")
        print("4- Weather")
        print("5- Search Trends")
        print("6- Region")
        print("7- Policy")
        print("X- Back to Menu")
        print()


        table_num = input()
        valid_inp = None

        # Return to menu
        if table_num.upper() == "X":
            break

        # Case selected
        if table_num == "1":
            print("Enter the column to sort with from the following schema: case_id: INT, province: STR(255), city: STR(255), group: STR(255), infection_case: STR(255), confirmed: INT")
            print("Example: 'case_id'")
            
            valid_inp = True # Valid_imp here means that they selected a valid table
            schema_inp = input()
            

        # PatientInfo selected
        if table_num == "2":
            print("Enter the column to sort with from the following schema: patient_id: INT, sex: STR(10), age: STR(10), province: STR(255), city: STR(255), infection_case: STR(255), contact_number: STR(255), confirmed_date: DATE, state: STR(255)")
            print("Example: 'patient_id'")
            
            valid_inp = True # Valid_imp here means that they selected a valid table
            schema_inp = input()
            

        # Date selected
        if table_num == "3":
            print("Enter the column to sort with from the following schema: date: DATE, test: INT, negative: INT, confirmed: INT, released: INT, deceased: INT")
            print("Example: 'date'")
            
            valid_inp = True # Valid_imp here means that they selected a valid table
            schema_inp = input()
            

        # Weather selected
        if table_num == "4":
            print("Enter the column to sort with from the following schema: code: INT, province: STR(255), date: DATE, avg_temp: FLOAT(10,1), min_temp: FLOAT(10,1), max_temp: FLOAT(10,1), precipitation: FLOAT(10,1), max_wind_speed: FLOAT(10,1), most_wind_direction : INT, avg_relative_humidity: FLOAT(10,1)")
            print("Example: 'code'")
            
            valid_inp = True # Valid_imp here means that they selected a valid table
            schema_inp = input()
            

        # Search Trends selected
        if table_num == "5":
            print("Enter the column to sort with from the following schema: date: DATE, cold: FLOAT(10,5), flu: FLOAT(10,5), pneumonia: FLOAT(10,5), coronavirus: FLOAT(10,5)")
            print("Example: 'date'")
            
            valid_inp = True # Valid_imp here means that they selected a valid table
            schema_inp = input()


        # Region selected
        if table_num == "6":
            print("Enter the column to sort with from the following schema: code: INT, province: STR(255), city: STR(255), elementary_school_count: INT, kindergarten_count: INT, university_count: INT, nursing_home_count: INT")
            print("Example: 'code'")
            
            valid_inp = True # Valid_imp here means that they selected a valid table
            schema_inp = input()


        # Policy selected
        if table_num == "7":
            print("Enter the column to sort with from the following schema: policy_id: INT, country: STR(255), type: STR(255), gov_policy: STR(255), detail: STR(255), start_date: DATE, end_date: OPTIONAL DATE")
            print("Example: 'policy_id'")
            
            valid_inp = True # Valid_imp here means that they selected a valid table
            schema_inp = input()


        
        print("Enter 'ASC' or 'DESC' ordering")
        expr_inp = input()




        # No choice selected
        if valid_inp == None:
            print("Please select a choice\n")
            inp = ""

        # No condition entered
        if schema_inp == "":
            print("Please enter a condition\n")
            valid_inp = None

        # No sort function entered
        if expr_inp == "":
            print("Please enter a sorting method\n")
            valid_inp = None
        


        # If the check passed, run the query to the database
        if valid_inp == True:

            
            print("Executing...")
            # Get the table headers
            query = f"SELECT column_name FROM information_schema.columns WHERE table_schema = 'public' AND table_name = '{table_options[int(table_num)]}';"
            search_columns = execute_query(query, get_headers=True)

            # Convert returned headers into a good format
            fixed_search_columns = []
            for i in range(len(search_columns)):
                fixed_search_columns.append(search_columns[i][0])


            # Get search results
            query = f"SELECT * FROM {table_options[int(table_num)]} ORDER BY {schema_inp} {expr_inp};"

            # Error messages will be handled by execute_query()
            
            search_output = execute_query(query)
            if search_output != None and search_output != "Error":
                print("Executed successfully")
                #Convert to pandas dataframe for better output layout because we're fancy like that :D
                try:
                    # Column names loaded properly
                    df = pd.DataFrame(search_output, columns=fixed_search_columns)
                    print(tabulate(df, headers='keys', tablefmt='psql'))
                except:
                    # Column names failed to load properly
                    df = pd.DataFrame(search_output)
                    print(tabulate(df, headers='keys', tablefmt='psql'))

            
            else:
                print("Could not output due to error\n")
                return 0

                

        # This is the only error that can occur at this part
        if valid_inp == False:
            print("Invalid Schema entered\n")
                
    
    return 0



def sql_joins(cur):
    
     # Declare Variables
    inp = ""
    table_options = {1:"case_", 2:"patientinfo", 3:"time_", 4:"weather", 5:"searchtrends", 6: "region", 7: "policy_"}
    schema_options = {1:"case_id: INT, province: STR(255), city: STR(255), group: STR(255), infection_case: STR(255), confirmed: INT", 2:"patient_id: INT, sex: STR(10), age: STR(10), province: STR(255), city: STR(255), infection_case: STR(255), contact_number: STR(255), confirmed_date: DATE, state: STR(255)", 3:"date: DATE, test: INT, negative: INT, confirmed: INT, released: INT, deceased: INT", 4:"code: INT, province: STR(255), date: DATE, avg_temp: FLOAT(10,1), min_temp: FLOAT(10,1), max_temp: FLOAT(10,1), precipitation: FLOAT(10,1), max_wind_speed: FLOAT(10,1), most_wind_direction : INT, avg_relative_humidity: FLOAT(10,1)", 5:"date: DATE, cold: FLOAT(10,5), flu: FLOAT(10,5), pneumonia: FLOAT(10,5), coronavirus: FLOAT(10,5)", 6: "code: INT, province: STR(255), city: STR(255), elementary_school_count: INT, kindergarten_count: INT, university_count: INT, nursing_home_count: INT", 7: "policy_id: INT, country: STR(255), type: STR(255), gov_policy: STR(255), detail: STR(255), start_date: DATE, end_date: OPTIONAL DATE"}
    
    

    while inp == "":
        table_choices = [1,2,3,4,5,6,7]
        schema_choices = []
        

        # Print joins menu
        print("Select the first table:")
        print("1- Case (case_)")
        print("2- Patient (patientinfo)")
        print("3- Date (time_)")
        print("4- Weather (weather)")
        print("5- Search Trends (searchtrends)")
        print("6- Region (region)")
        print("7- Policy (policy)")
        print("X- Back to Menu")
        print()


        table_num1 = input()
        valid_inp = None

        # Return to menu
        if table_num1.upper() == "X":
            break

        # Case selected
        if table_num1 in table_choices:
            # Remove that table from the options
            table_choices.remove(table_num1)
            schema_choices.append(schema_options[int(table_num1)])
            # Add that table's schema to the list of options


            print("Enter the second table to join with the first")
            
            print("Options: " + str(table_choices))
            
            table_num2 = input()
            
            if table_num2.upper() == "X":
                break

            if table_num2 in table_choices:
                schema_choices.append(schema_options[int(table_num2)])
                valid_inp = True # Valid_imp here means that they selected a valid table
            
                print("Choose a column to join the two tables between")
                print("Choices: \n" + str(schema_choices[0]) + "\n" + str(schema_choices[1]))
                print("For Date and Search Trends tables: 'time_.date = searchtrends.date'")

                schema_inp = input()
        
        

        # No choice selected
        if valid_inp == None:
            print("Please select a choice\n")
            inp = ""

        # No condition entered
        if schema_inp == "":
            print("Please enter a condition\n")
            valid_inp = None
        


        # If the check passed, run the query to the database
        if valid_inp == True:
            

            print("Executing...")
            # Get the table headers
            query = f"SELECT column_name FROM information_schema.columns WHERE table_schema = 'public' AND table_name = '{table_options[int(table_num1)]}';"
            search_columns1 = execute_query(query, get_headers=True)

            # Convert returned headers into a good format
            fixed_search_columns = []
            for i in range(len(search_columns1)):
                fixed_search_columns.append(search_columns1[i][0])

            query = f"SELECT column_name FROM information_schema.columns WHERE table_schema = 'public' AND table_name = '{table_options[int(table_num2)]}';"
            search_columns2 = execute_query(query, get_headers=True)

            # Convert returned headers into a good format
            for i in range(len(search_columns2)):
                fixed_search_columns.append(search_columns2[i][0])



            # Get search results
            query = f"SELECT * FROM {table_options[int(table_num1)]} INNER JOIN {table_options[int(table_num2)]} ON {schema_inp};"

            # Error messages will be handled by execute_query()
            print("Executing...")
            search_output = execute_query(query)
            if search_output != None and search_output != "Error":
                print("Executed successfully")

                try:
                    #Convert to pandas dataframe for better output layout because we're fancy like that :D
                    df = pd.DataFrame(search_output, columns=fixed_search_columns)
                    print(tabulate(df, headers='keys', tablefmt='psql'))

                except:
                    # Column names failed to load properly
                    df = pd.DataFrame(search_output)
                    print(tabulate(df, headers='keys', tablefmt='psql'))

            
            else:
                print("Could not output due to error\n")
                return 0
                

        # This is the only error that can occur at this part
        if valid_inp == False:
            print("Invalid Schema entered\n")
                
    
    return 0



def sql_grouping(cur):
    
    # Declare Variables
    inp = ""
    table_options = {1:"case_", 2:"patientinfo", 3:"time_", 4:"weather", 5:"searchtrends", 6: "region", 7: "policy_"}
    
    


    while inp == "":

        # Print group menu
        print("Select a table to group data from:")
        print("1- Case (case_)")
        print("2- Patient (patientinfo)")
        print("3- Date (time_)")
        print("4- Weather (weather)")
        print("5- Search Trends (searchtrends)")
        print("6- Region (region)")
        print("7- Policy (policy)")
        print("X- Back to Menu")
        print()


        table_num = input()
        valid_inp = None

        # Return to menu
        if table_num.upper() == "X":
            break

        # Case selected
        if table_num == "1":
            print("Enter the column to group with from the following schema: case_id: INT, province: STR(255), city: STR(255), group: STR(255), infection_case: STR(255), confirmed: INT")
            print("Example: 'province'")
            
            valid_inp = True # Valid_imp here means that they selected a valid table
            schema_inp = input()
            

        # PatientInfo selected
        if table_num == "2":
            print("Enter the column to group with from the following schema: patient_id: INT, sex: STR(10), age: STR(10), province: STR(255), city: STR(255), infection_case: STR(255), contact_number: STR(255), confirmed_date: DATE, state: STR(255)")
            print("Example: 'patient_id'")
            
            valid_inp = True # Valid_imp here means that they selected a valid table
            schema_inp = input()
            

        # Date selected
        if table_num == "3":
            print("Enter the column to group with from the following schema: date: DATE, test: INT, negative: INT, confirmed: INT, released: INT, deceased: INT")
            print("Example: 'date'")
            
            valid_inp = True # Valid_imp here means that they selected a valid table
            schema_inp = input()
            

        # Weather selected
        if table_num == "4":
            print("Enter the column to group with from the following schema: code: INT, province: STR(255), date: DATE, avg_temp: FLOAT(10,1), min_temp: FLOAT(10,1), max_temp: FLOAT(10,1), precipitation: FLOAT(10,1), max_wind_speed: FLOAT(10,1), most_wind_direction : INT, avg_relative_humidity: FLOAT(10,1)")
            print("Example: 'code'")
            
            valid_inp = True # Valid_imp here means that they selected a valid table
            schema_inp = input()
            

        # Search Trends selected
        if table_num == "5":
            print("Enter the column to group with from the following schema: date: DATE, cold: FLOAT(10,5), flu: FLOAT(10,5), pneumonia: FLOAT(10,5), coronavirus: FLOAT(10,5)")
            print("Example: 'date'")
            
            valid_inp = True # Valid_imp here means that they selected a valid table
            schema_inp = input()


        # Region selected
        if table_num == "6":
            print("Enter the column to group with from the following schema: code: INT, province: STR(255), city: STR(255), elementary_school_count: INT, kindergarten_count: INT, university_count: INT, nursing_home_count: INT")
            print("Example: 'code'")
            
            valid_inp = True # Valid_imp here means that they selected a valid table
            schema_inp = input()


        # Policy selected
        if table_num == "7":
            print("Enter the column to group with from the following schema: policy_id: INT, country: STR(255), type: STR(255), gov_policy: STR(255), detail: STR(255), start_date: DATE, end_date: OPTIONAL DATE")
            print("Example: 'policy_id'")
            
            valid_inp = True # Valid_imp here means that they selected a valid table
            schema_inp = input()


        # Since count is the only one that doesn't need a different column to aggregate on
        #expr_schema_inp = "*"
        #if(expr_inp).lower() != "count":
        print("Enter the column to aggregate through from the table")
        expr_schema_inp = input()

        print("Enter the aggregate function such as 'AVG', 'COUNT', 'MAX', 'MIN', 'SUM', ...")
        expr_inp = input()


        # No expr_schema selected
        if expr_schema_inp == "":
            print("Please select a choice\n")
            inp = ""


        # No choice selected
        if valid_inp == None:
            print("Please select a choice\n")
            inp = ""

        # No condition entered
        if schema_inp == "":
            print("Please enter a condition\n")
            valid_inp = None

        # No aggregate function entered
        if expr_inp == "":
            print("Please enter a function\n")
            valid_inp = None
        


        # If the check passed, run the query to the database
        if valid_inp == True:

            
            print("Executing...")

            # Get search results
            query = f"SELECT {schema_inp}, {expr_inp}({expr_schema_inp}) FROM {table_options[int(table_num)]} GROUP BY {schema_inp};"

            # Error messages will be handled by execute_query()
            
            search_output = execute_query(query)
            if search_output != None and search_output != "Error":
                print("Executed successfully")
               
                try:
                    #Convert to pandas dataframe for better output layout
                    df = pd.DataFrame(search_output)
                    print(tabulate(df, headers='keys', tablefmt='psql'))
                except:
                    # Column names failed to load properly
                    df = pd.DataFrame(search_output)
                    print(tabulate(df, headers='keys', tablefmt='psql'))

            else:
                print("Could not output due to error\n")
                return 0



        # This is the only error that can occur at this part
        if valid_inp == False:
            print("Invalid Schema entered\n")
                
    
    return 0



def sql_subqueries(cur):
    
    
    # Declare Variables
    inp = ""
    table_options = {1:"case_", 2:"patientinfo", 3:"time_", 4:"weather", 5:"searchtrends", 6: "region", 7: "policy_"}
    schema_options = {1:"case_id: INT, province: STR(255), city: STR(255), group: STR(255), infection_case: STR(255), confirmed: INT", 2:"patient_id: INT, sex: STR(10), age: STR(10), province: STR(255), city: STR(255), infection_case: STR(255), contact_number: STR(255), confirmed_date: DATE, state: STR(255)", 3:"date: DATE, test: INT, negative: INT, confirmed: INT, released: INT, deceased: INT", 4:"code: INT, province: STR(255), date: DATE, avg_temp: FLOAT(10,1), min_temp: FLOAT(10,1), max_temp: FLOAT(10,1), precipitation: FLOAT(10,1), max_wind_speed: FLOAT(10,1), most_wind_direction : INT, avg_relative_humidity: FLOAT(10,1)", 5:"date: DATE, cold: FLOAT(10,5), flu: FLOAT(10,5), pneumonia: FLOAT(10,5), coronavirus: FLOAT(10,5)", 6: "code: INT, province: STR(255), city: STR(255), elementary_school_count: INT, kindergarten_count: INT, university_count: INT, nursing_home_count: INT", 7: "policy_id: INT, country: STR(255), type: STR(255), gov_policy: STR(255), detail: STR(255), start_date: DATE, end_date: OPTIONAL DATE"}
    
    

    while inp == "":
        table_choices = ["1","2","3","4","5","6","7"]
        
        
        # Print joins menu
        print("1- Case (case_)")
        print("2- Patient (patientinfo)")
        print("3- Date (time_)")
        print("4- Weather (weather)")
        print("5- Search Trends (searchtrends)")
        print("6- Region (region)")
        print("7- Policy (policy)")
        print("X- Back to Menu")
        print()


        table_num = input()
        valid_inp = None

        # Return to menu
        if table_num.upper() == "X":
            break

        # Case selected
        if table_num in table_choices:

            # Choose column1
            print("Enter the column name for the main query")
            print("Choices: \n" + str(schema_options[int(table_num)]))
            print("Example for Case table: 'infection_case'")
            schema_inp = input()

            
            print("Enter the second table to subquery in")
            print("1- Case")
            print("2- Patient")
            print("3- Date")
            print("4- Weather")
            print("5- Search Trends")
            print("6- Region")
            print("7- Policy")
            print("X- Back to Menu")
            print()
            

            table2_num = input()
            

            if table2_num in table_choices:
                valid_inp = True # Valid_imp here means that they selected a valid table
            
                # Choose column1
                print("Enter the column name for the subquery")
                print("Choices: \n" + str(schema_options[int(table2_num)]))
                print("Example for PatientInfo table: 'infection_case'")
                schema2_inp = input()


                print("Enter the condition for the subquery")
                print("Example for PatientInfo table: state = 'deceased'")
                expr_inp = input()

        
        

        # No choice selected
        if valid_inp == None:
            print("Please select a choice\n")
            inp = ""

        # No schema entered
        if schema_inp == "":
            print("Please enter a column\n")
            valid_inp = None
        
        # No schema2 entered
        if schema2_inp == "":
            print("Please enter a subcolumn\n")
            valid_inp = None
        
        # No table entered
        if table_num == "":
            print("Please enter a table\n")
            valid_inp = None

        # No table2 entered
        if table2_num == "":
            print("Please enter a subtable\n")
            valid_inp = None

        # No condition entered
        if expr_inp == "":
            print("Please enter a condition\n")
            valid_inp = None


        # If the check passed, run the query to the database
        if valid_inp == True:
            


            print("Executing...")

            # Get search results
            query = f"SELECT * FROM {table_options[int(table_num)]} WHERE {schema_inp} IN (SELECT {schema2_inp} FROM {table_options[int(table2_num)]} WHERE {expr_inp});"

            # Error messages will be handled by execute_query()
            print("Executing...")
            search_output = execute_query(query)
            if search_output != None and search_output != "Error":
                print("Executed successfully")

                #Convert to pandas dataframe for better output layout because we're fancy like that :D
                df = pd.DataFrame(search_output)
                print(tabulate(df, headers='keys', tablefmt='psql'))


            else:
                print("Could not output due to error\n")
                return 0


                

        # This is the only error that can occur at this part
        if valid_inp == False:
            print("Invalid Schema entered\n")
                
    
    return 0



def sql_transactions(cur):
    
    
    print("Enter one of the following for a transaction operation:")
    print("T- Begin Transaction")
    print("C- Commit")
    print("R- Rollback")
    print("X- Back to Menu")

    transaction_inp = input()


    # Get outta here!
    if transaction_inp == "":
        print("No input entered. Going back to main menu.")

    # Turn on transactions
    if transaction_inp.lower() == "t":
        set_Autocommit_Off()

    # Commit
    if transaction_inp.lower() == "c":
        
        if(execute_query("",transaction_code="C") == "TC recieved"):
            print("Committed. Turning on AutoCommit")
            set_Autocommit_On()

        else:
            print("Error occured committing transaction.")
            return 1

    # Rollback
    if transaction_inp.lower() == "r":
        if(execute_query("",transaction_code="R") == "TC recieved"):
            print("Rolled back. Turning on AutoCommit")
            set_Autocommit_On()
       
        else:
            print("Error occured committing transaction.")
            return 1



    return 0





# Run the main function
if __name__ == "__main__": 
    main_menu() 
