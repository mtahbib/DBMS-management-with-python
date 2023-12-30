from flask import Flask, render_template, request, redirect, url_for, jsonify
import mysql.connector

app = Flask(__name__)

# Replace these with your MySQL database credentials
db_host = 'localhost'
db_user = 'root'
db_password ='tahbib'
db_name = 'mybook'

# Create a MySQL connection
connection = mysql.connector.connect(
    host=db_host,
    user=db_user,
    password=db_password,
    database=db_name
)

cursor = connection.cursor()

# Create the 'project_data' table if it doesn't exist
create_table_query = '''
CREATE TABLE IF NOT EXISTS project_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    emp_id INT,
    designation VARCHAR(255),
    email VARCHAR(255),
    password VARCHAR(255)
)
'''
cursor.execute(create_table_query)

@app.route('/')
def index():
    # Fetch and display existing project data
    cursor.execute('SELECT id, name, emp_id, designation, email, password FROM project_data')
    data = cursor.fetchall()
    return render_template('index.html', employees=data)

@app.route('/save', methods=['POST'])
def save():
    data = {
        'name': request.form['name'],
        'emp_id': int(request.form['emp_id']),
        'designation': request.form['designation'],
        'email': request.form['email'],
        'password': request.form['password']
    }

    save_to_database(data)

    return redirect(url_for('index'))

@app.route('/update/<int:id>', methods=['POST'])
def update_employee(id):
    if request.method == 'POST':
        data = request.form
        # Update project data in the database based on the received form data
        update_query = '''
        UPDATE project_data SET name=%s, emp_id=%s, designation=%s, 
        email=%s, password=%s WHERE id=%s
        '''
        cursor.execute(update_query, (
            data.get('name'),
            data.get('emp_id'),
            data.get('designation'),
            data.get('email'),
            data.get('password'),
            id
        ))
        connection.commit()

        return jsonify({'message': 'Employee updated successfully'})

    cursor.execute('SELECT * FROM project_data WHERE id=%s', (id,))
    employee_data = cursor.fetchone()

    return render_template('update.html', employee=employee_data)

@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete_employee(id):
    if request.method == 'POST':
        # Delete project data from the database
        delete_query = 'DELETE FROM project_data WHERE id=%s'
        cursor.execute(delete_query, (id,))
        connection.commit()

        return jsonify({'message': 'Employee deleted successfully'})

    return redirect(url_for('index'))

def save_to_database(data):
    insert_query = '''
    INSERT INTO project_data (name, emp_id, designation, email, password)
    VALUES (%s, %s, %s, %s, %s)
    '''

    cursor.execute(insert_query, (
        data['name'],
        data['emp_id'],
        data['designation'],
        data['email'],
        data['password']
    ))
    connection.commit()

if __name__ == '__main__':
    app.run(debug=True)
