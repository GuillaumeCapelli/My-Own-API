from flask import Flask, request, abort, json
from flask_basicauth import BasicAuth
import pymysql
import os
import math
from collections import defaultdict
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)
app.config.from_file("flask_config.json", load=json.load)
auth = BasicAuth(app)

MAX_PAGE_SIZE = 100


swaggerui_blueprint = get_swaggerui_blueprint(
    base_url='/docs',
    api_url='/static/openapi.yaml',
)
app.register_blueprint(swaggerui_blueprint)


def remove_null_fields(obj):
    return {k: v for k, v in obj.items() if v is not None}

@app.route("/")
@auth.required
def home():
    homepage = """
    <title>elcome to my API</title>
    <body>
    <h1>HERE'S MY COMMANDS:</h1>
    <p>
    "/customers" "/customers/IDofthemovie" or "customers?page=1 or 2 or 10 or 200"
    </body>
    
    """
    return homepage

@app.route("/customers/<int:customer_id>")
@auth.required
def customer(customer_id):
    db_conn = pymysql.connect(host="localhost", user="root", password=os.getenv("MySQL_password"), database="classicmodels",
                              cursorclass=pymysql.cursors.DictCursor)

    with db_conn.cursor() as cursor:
        cursor.execute("""
            SELECT * FROM customers WHERE customerNumber=%s
        """, (customer_id,))
        customer = cursor.fetchone()

    if not customer:
        abort(404)

    customer = remove_null_fields(customer)
    db_conn.close()
    return customer

@app.route("/customers")
@auth.required
def customers():
    page = int(request.args.get('page', 0))
    page_size = int(request.args.get('page_size', MAX_PAGE_SIZE))
    page_size = min(page_size, MAX_PAGE_SIZE)

    db_conn = pymysql.connect(host="localhost", user="root", password=os.getenv("MySQL_password"), database="classicmodels",
                              cursorclass=pymysql.cursors.DictCursor)

    with db_conn.cursor() as cursor:
        cursor.execute("""
            SELECT * FROM customers
            ORDER BY customerNumber
            LIMIT %s
            OFFSET %s
        """, (page_size, page * page_size))       
        customers = cursor.fetchall()

    with db_conn.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) AS total FROM customers")
        total = cursor.fetchone()
        last_page = math.ceil(total['total'] / page_size)
    
    db_conn.close()
    return {
        'customers': customers,
        'next_page': f'/customers?page={page+1}&page_size={page_size}',
        'last_page': f'/customers?page={last_page}&page_size={page_size}',
    }

@app.route("/employees/<int:employee_id>")
@auth.required
def employee(employee_id):
    db_conn = pymysql.connect(host="localhost", user="root", password=os.getenv("MySQL_password"), database="classicmodels",
                              cursorclass=pymysql.cursors.DictCursor)

    with db_conn.cursor() as cursor:
        cursor.execute("""
            SELECT * FROM employees WHERE employeeNumber=%s
        """, (employee_id,))
        employee = cursor.fetchone()

    if not employee:
        abort(404)

    employee = remove_null_fields(employee)
    db_conn.close()
    return employee

@app.route("/employees")
@auth.required
def employees():
    page = int(request.args.get('page', 0))
    page_size = int(request.args.get('page_size', MAX_PAGE_SIZE))
    page_size = min(page_size, MAX_PAGE_SIZE)

    db_conn = pymysql.connect(host="localhost", user="root", password=os.getenv("MySQL_password"), database="classicmodels",
                              cursorclass=pymysql.cursors.DictCursor)

    with db_conn.cursor() as cursor:
        cursor.execute("""
            SELECT * FROM employees
            ORDER BY employeeNumber
            LIMIT %s
            OFFSET %s
        """, (page_size, page * page_size))       
        employees = cursor.fetchall()

    with db_conn.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) AS total FROM employees")
        total = cursor.fetchone()
        last_page = math.ceil(total['total'] / page_size)
    
    db_conn.close()
    return {
        'employees': employees,
        'next_page': f'/employees?page={page+1}&page_size={page_size}',
        'last_page': f'/employees?page={last_page}&page_size={page_size}',
    }


