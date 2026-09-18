import sqlite3
import json


def create_database():

    connection = None

    try:
        connection = sqlite3.Connection("database.db")
        cursor = connection.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS database(ID INTEGER PRIMARY KEY,CLIENT_NAME TEXT, CONTACT_EMAIL TEXT, BUDGET REAL, TIMEFRAME_TYPE TEXT, TIMEFRAME_NUM INTEGER, SERVICE TEXT, CLIENT_INDUSTRY TEXT, PRODUCT_REQUIREMENTS TEXT, PAIN_POINTS TEXT, VALUE TEXT, URGENCY TEXT, PRIORITY TEXT )")
        connection.commit()
        return("database running succesfully")

    except sqlite3.Error as e:
        print(f"sorry currently experiencing technical issues. Error: {e}")
        return False

    finally:
        if connection is not None:
            connection.close()

        

def fresh_sql_connect():

    connection = sqlite3.Connection("database.db")
    cursor = connection.cursor()

    return connection, cursor


def save_to_database(upd_customer_obj):

    connection = None

    try:
        connection, cursor = fresh_sql_connect()
        pr_rq_str = json.dumps(upd_customer_obj.product_requirements)
        pa_po_str = json.dumps(upd_customer_obj.pain_points)

        cursor.execute("INSERT INTO database(CLIENT_NAME, CONTACT_EMAIL, BUDGET, TIMEFRAME_TYPE, TIMEFRAME_NUM, SERVICE, CLIENT_INDUSTRY, PRODUCT_REQUIREMENTS, PAIN_POINTS, VALUE, URGENCY, PRIORITY) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)", (upd_customer_obj.client_name, upd_customer_obj.contact_email, upd_customer_obj.budget, upd_customer_obj.timeframe_type, upd_customer_obj.timeframe_num, upd_customer_obj.service, upd_customer_obj.client_industry, pr_rq_str, pa_po_str, upd_customer_obj.value, upd_customer_obj.urgency, upd_customer_obj.priority))
        connection.commit()
        print("database save success")
        return True
    
    except sqlite3.Error as e:
        print(f"sorry currently experiencing technical issues. Error: {e}")
        return False

    except Exception as e:
        print(f"sorry currently experiencing technical issues. Error: {e}")
        return False

    finally:   
        if connection is not None:
            connection.close()


def display_database():

    choice = input("Would you like to view the saved database? (yes or no) ")
    choice_l = choice.lower()
    connection = None
    if choice_l == "yes":
        try: 
            connection, cursor = fresh_sql_connect()
            cursor.execute("SELECT * FROM database")
            database = cursor.fetchall()
            query_dict = {}
            i=0
            
            for row in database:
                query_dict[f"entry no. {i}"] = {}
                python_pr_rq = json.loads(row[7])
                python_pa_po = json.loads(row[8])
                query_dict[f"entry no. {i}"]["ID"] = row[0]
                query_dict[f"entry no. {i}"]["client_name"] = row[1]
                query_dict[f"entry no. {i}"]["contact_email"] = row[2]
                query_dict[f"entry no. {i}"]["budget"] = row[3]
                query_dict[f"entry no. {i}"]["timeframe"] = str(row[5])+ "" +str(row[4])
                query_dict[f"entry no. {i}"]["service"] = row[6]
                query_dict[f"entry no. {i}"]["client_industry"] = row[7]
                query_dict[f"entry no. {i}"]["product_requirements"] = python_pr_rq
                query_dict[f"entry no. {i}"]["pain_points"] = python_pa_po
                query_dict[f"entry no. {i}"]["value"] = row[10]
                query_dict[f"entry no. {i}"]["urgency"] = row[11]
                query_dict[f"entry no. {i}"]["priority"] = row[12]
                i= i + 1


            return query_dict

        except sqlite3.Error as e:
            print(f"sorry currently experiencing technical issues. Error: {e}")
            return False

        except Exception as e:
            print(f"sorry currently experiencing technical issues. Error: {e}")
            return False

        finally:
            if connection is not None:
                connection.close()

    if choice_l =="no":
        return "database not shown"

    else:
        return "incorrect input, database not shown"
