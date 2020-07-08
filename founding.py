from flask import Flask, request
import mysql.connector, json
from mysql.connector import errorcode

app = Flask(__name__)
dbconfig = {
    'user' :'<fill_in>',
    'password' : '<fill_in>',
    'host' : '127.0.0.1',
    'db' : '<fill_in>'
}

@app.route('/business/alias/<business_name>', methods=['GET'])
def get_business(business_name = None):
    response = {
        'status' : {
            'code': None,
            'msg' : None
        },
        'business' : {
            'id' : None,
            'name' : None
        }
    } 

    try:
        # Connection to the database
        connection = mysql.connector.connect(**dbconfig)
        cursor = connection.cursor()
        query = ("SELECT id, name FROM business WHERE name like %s")
        business_name = business_name + "%"
        args = [business_name]
        cursor.execute(query, args)

        db_response = cursor.fetchall()

        print('Select query successful')
        if(len(db_response) != 0):
            response['business']['id'] = db_response[0][0]
            response['business']['name'] = db_response[0][1]
            response['status']['code'] = 200
            response['status']['msg'] = 'Database search successful'
        else:
            response['status']['code'] = 404
            response['status']['msg'] = 'None found'
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(str(err.errno) + ': Select query unsuccessful with databse error: ' + err.msg)
        response['status']['code'] = 500
        response['status']['msg'] = 'Database search unsuccessful'
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("MYSQL connection is closed")
        return response

@app.route('/business/submission', methods=['PUT'])
def send_submission():
    response = {
        'status' : {
            'code': None,
            'msg' : None
        }
    } 
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

    try:
        # Connection to the database
        connection = mysql.connector.connect(**dbconfig)
        cursor = connection.cursor()
        args = [business_id, price_category, price_rating, price_suggestion, quality_category, quality_rating, quality_suggestion, environment_category, environment_rating, environment_suggestion, service_category, service_rating, service_suggestion]
        cursor.callproc("insert_submission", args)
        connection.commit()
        response['status']['code'] = 200
        response['status']['msg'] = 'Submission successful'
        print(response['status']['msg'])
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(str(err.errno) + ': Submission unsuccessful with databse error: ' + err.msg)
        response['status']['code'] = 500
        response['status']['msg'] = 'Submission unsuccessful'
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("MYSQL connection is closed")
        return response
        