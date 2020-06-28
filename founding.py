from flask import Flask, request
import mysql.connector, json
from mysql.connector import errorcode

app = Flask(__name__)
dbconfig = {
    'user' :'hf_founder',
    'password' : 'HonestFeedback123',
    'host' : '127.0.0.1',
    'db' : 'honestfeedback'
}

@app.route('/<business_name>', methods=['GET'])
def get_business(business_name = None):
    response = {
        'status' : '',
        'business-id' : '',
        'business-name' : ''
    } 

    try:
        # Connection to the database
        connection = mysql.connector.connect(**dbconfig)
        cursor = connection.cursor()
        query = ("SELECT id, name FROM business WHERE name like %s")
        business_name = business_name + "%"
        args = [business_name]
        cursor.execute(query, args)

        exec_status = 'Select query successful'

        db_response = cursor.fetchall()

        response['status'] = exec_status
        response['business-id'] = db_response[0][0]
        response['business-name'] = db_response[0][1]
        print(exec_status)
    except mysql.connector.Error as err:
        response['status'] = 'Select query unsuccessful'
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(str(err.errno) + ': Select query unsuccessful with databse error: ' + err.msg)
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("MYSQL connection is closed")
        return response


@app.route('/submission', methods=['PUT'])
def send_submission():
    data = request.get_json()['data']
    business_id = data['business_id']

    price = data['price']
    price_category = price['category']
    price_rating = price['rating']
    price_suggestion = price['suggestion']

    quality = data['quality']
    quality_category = quality['category']
    quality_rating = quality['rating']
    quality_suggestion = quality['suggestion']

    environment = data['environment']
    environment_category = environment['category']
    environment_rating = environment['rating']
    environment_suggestion = environment['suggestion']

    service = data['service']
    service_category = service['category']
    service_rating = service['rating']
    service_suggestion = service['suggestion']

    exec_status = ''
    try:
        # Connection to the database
        connection = mysql.connector.connect(**dbconfig)
        cursor = connection.cursor()
        args = [business_id, price_category, price_rating, price_suggestion, quality_category, quality_rating, quality_suggestion, environment_category, environment_rating, environment_suggestion, service_category, service_rating, service_suggestion]
        cursor.callproc("insert_submission", args)
        connection.commit()
        exec_status = 'Submission successful'
        print(exec_status)
    except mysql.connector.Error as err:
        exec_status = 'Submission unsuccessful'
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(str(err.errno) + ': Submission unsuccessful with databse error: ' + err.msg)
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("MYSQL connection is closed")
        return exec_status
        