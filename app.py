from flask import Flask, render_template, request, redirect, url_for, jsonify, session
import mysql.connector
import bcrypt
from flask import Flask, render_template, request, redirect, url_for, flash
app = Flask(__name__)

# Configure your MySQL database connection
db_host = 'localhost'
db_user = 'root'
db_password = 'tahbib'
db_name = 'dbms'
'''USE dbms;
CREATE TABLE user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL
);
'''
# Add a secret key for session management
app.secret_key = 'your_secret_key'

app.secret_key = 'your_secret_key'

# Create a MySQL connection
connection = mysql.connector.connect(
    host=db_host,
    user=db_user,
    password=db_password,
    database=db_name
)

cursor = connection.cursor()

# Define a function to verify passwords
def verify_password(user_password, hashed_password):
    return bcrypt.checkpw(user_password.encode('utf-8'), hashed_password.encode('utf-8'))

# Registration Route

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Hash the password before storing it in the database
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Insert the username and hashed_password into the 'users' table
        cursor.execute('INSERT INTO user (username, password) VALUES (%s, %s)', (username, hashed_password))
        connection.commit()

        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        user_password = request.form['password']

        # Print the SQL query for debugging
        print(f"SELECT password FROM user WHERE username = '{username}'")

        # Query the 'user' table to retrieve the hashed password for the given username
        cursor.execute('SELECT password FROM user WHERE username = %s', (username,))
        result = cursor.fetchone()

        if result:
            hashed_password_from_db = result[0]
            if verify_password(user_password, hashed_password_from_db):
                # Passwords match, login successful
                session['username'] = username
                flash('Login successful!', 'success')
                return redirect(url_for('dashboard'))
        
        # If username or password is incorrect or user not found
        flash('Invalid username or password. Please try again.', 'error')

    return render_template('login.html')
# Dashboard route, where the user goes after successful login
@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return render_template('dashboard.html', username=session['username'])
    else:
        flash('You must log in to access the dashboard.', 'info')
        return redirect(url_for('login'))

# Logout route
@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

# Create the 'vendor_data' table if it doesn't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS vendor_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    email VARCHAR(255),
    contact VARCHAR(255),
    service_type VARCHAR(255),
    vendor_number VARCHAR(255)  
)
''')
cursor.execute('''
CREATE TABLE IF NOT EXISTS user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL
);''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS initator_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    project_number VARCHAR(255),
    name VARCHAR(255),
    date DATE,
    ownership VARCHAR(255),
    description VARCHAR(255)
)
''')



cursor.execute('''
CREATE TABLE IF NOT EXISTS materials (
    material_id INT AUTO_INCREMENT PRIMARY KEY,
    disk TEXT,
    ram TEXT,
    os TEXT,
    assigned_date DATE,
    completed_date DATE
)

    ''')


cursor.execute('''
    CREATE TABLE IF NOT EXISTS employees (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255),
        emp_id VARCHAR(255) UNIQUE,  -- Add UNIQUE constraint here
        designation VARCHAR(255),
        email VARCHAR(255),
        password VARCHAR(255)
    )
''')

   #resource_data
cursor.execute('''
CREATE TABLE IF NOT EXISTS resources (
    id INT AUTO_INCREMENT PRIMARY KEY,
    resource_id VARCHAR(255),
    name VARCHAR(255),
    team VARCHAR(255),
    material VARCHAR(255),
    leader_id VARCHAR(255)
)
''')
cursor.execute('''
CREATE TABLE IF NOT EXISTS planning_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    planning_id VARCHAR(255),
    start_date DATE,
    end_date DATE,
    key_deliveries TEXT
)
''')



@app.route('/')
def index():
    return render_template('index.html')


# Vendor Routes
@app.route('/vendor')
def vendor_index():
    cursor.execute('SELECT * FROM vendor_data')
    vendors = cursor.fetchall()
    return render_template('index_vendor.html', vendors=vendors)


@app.route('/save_vendor', methods=['POST'])
def save_vendor():
    vendor_info = {
        'name': request.form['name'],
        'email': request.form['email'],
        'contact': request.form['contact'],
        'service_type': request.form['service_type'],
        'vendor_number': request.form['vendor_number']
    }
    cursor.execute('''
        INSERT INTO vendor_data (name, email, contact, service_type, vendor_number)
        VALUES (%s, %s, %s, %s, %s)
    ''', (vendor_info['name'], vendor_info['email'], vendor_info['contact'],
          vendor_info['service_type'], vendor_info['vendor_number']))
    connection.commit()
    return redirect(url_for('vendor_index'))

@app.route('/update_vendor/<int:vendor_id>', methods=['POST'])
def update_vendor(vendor_id):
    data = request.get_json()
    cursor.execute('''
        UPDATE vendor_data
        SET name = %s, email = %s, contact = %s, service_type = %s, vendor_number = %s
        WHERE id = %s
    ''', (data['name'], data['email'], data['contact'], data['service_type'],
          data['vendor_number'], vendor_id))
    connection.commit()
    return jsonify({'message': 'Vendor updated successfully'})

@app.route('/delete_vendor/<int:id>', methods=['POST'])
def delete_vendor(id):
    cursor.execute('DELETE FROM vendor_data WHERE id = %s', (id,))
    connection.commit()
    return jsonify({'message': 'Vendor deleted successfully'})
#project initiator

# Project Initiator Routes
@app.route('/initiator')
def initiator_index():
    cursor.execute('SELECT * FROM initator_data')
    initiators = cursor.fetchall()
    return render_template('index_initiator.html', initiators=initiators)

@app.route('/save_initiator', methods=['POST'])
def save_initiator():
    initiator_info = {
        'project_number': request.form['project_number'],
        'name': request.form['name'],
        'date': request.form['date'],
        'ownership': request.form['ownership'],
        'description': request.form['description']
    } 

 

    cursor.execute('''
        INSERT INTO initator_data (project_number, name, date, ownership, description)
        VALUES (%s, %s, %s, %s, %s)
    ''', (initiator_info['project_number'], initiator_info['name'], 
          initiator_info['date'], initiator_info['ownership'], 
          initiator_info['description']))
    connection.commit()
    return redirect(url_for('initiator_index'))


@app.route('/update_initiator/<int:initiator_id>', methods=['POST'])
def update_initiator(initiator_id):
    data = request.get_json()
    cursor.execute('''
        UPDATE initator_data
        SET project_number = %s, name = %s, date = %s, ownership = %s, description = %s
        WHERE id = %s
    ''', (data['project_number'], data['name'], data['date'], 
          data['ownership'], data['description'], initiator_id))
    connection.commit()
    return jsonify({'message': 'Initiator updated successfully'})

@app.route('/delete_initiator/<int:id>', methods=['POST'])
def delete_initiator(id):
    cursor.execute('DELETE FROM initator_data WHERE id = %s', (id,))
    connection.commit()
    return jsonify({'message': 'Initiator deleted successfully'})


#resources

@app.route('/resources')
def resources_index():
    cursor.execute('SELECT * FROM resources')
    resources = cursor.fetchall()
    return render_template('index_resources.html', resources=resources)

# Save Resource Route
@app.route('/save_resource', methods=['POST'])
def save_resource():
    resource_id = request.form['resource_id']
    name = request.form['name']
    team = request.form['team']
    material = request.form['material']
    leader_id = request.form['leader_id']
    cursor.execute('''
        INSERT INTO resources (resource_id, name, team, material, leader_id)
        VALUES (%s, %s, %s, %s, %s)
    ''', (resource_id, name, team, material, leader_id))
    connection.commit()
    return redirect(url_for('resources_index'))

# Update Resource Route
@app.route('/update_resource/<int:resource_id>', methods=['POST'])
def update_resource(resource_id):
    try:
        data = request.get_json()
        resource_id_updated = data.get('resource_id')
        name = data.get('name')
        team = data.get('team')
        material = data.get('material')
        leader_id = data.get('leader_id')

        cursor.execute('''
            UPDATE resources
            SET resource_id = %s, name = %s, team = %s, material = %s, leader_id = %s
            WHERE id = %s
        ''', (resource_id_updated, name, team, material, leader_id, resource_id))
        connection.commit()
        
        return jsonify({'message': 'Resource updated successfully'})
    except Exception as e:
        print(e)
        return jsonify({'message': 'An error occurred'}), 500


@app.route('/delete_resource/<int:resource_id>', methods=['POST'])
def delete_resource(resource_id):
    cursor.execute('DELETE FROM resources WHERE id = %s', (resource_id,))
    connection.commit()
    return jsonify({'message': 'Resource deleted successfully'})


#Materials

@app.route('/materials')
def materials_index():
    cursor.execute('SELECT * FROM materials')
    materials = cursor.fetchall()
    return render_template('index_materials.html', materials=materials)

@app.route('/save_material', methods=['POST'])
def save_material():
    material_info = {
        'disk': request.form['disk'],
        'ram': request.form['ram'],
        'os': request.form['os'],
        'assigned_date': request.form['assigned_date'],
        'completed_date': request.form['completed_date']
    }
    cursor.execute('''
        INSERT INTO materials (disk, ram, os, assigned_date, completed_date)
        VALUES (%s, %s, %s, %s, %s)
    ''', (material_info['disk'], material_info['ram'], material_info['os'],
          material_info['assigned_date'], material_info['completed_date']))
    connection.commit()
    return redirect(url_for('materials_index'))

@app.route('/update_material/<int:material_id>', methods=['POST'])
def update_material(material_id):
    data = request.get_json()
    try:
        cursor.execute('''
            UPDATE materials 
            SET disk = %s, ram = %s, os = %s, assigned_date = %s, completed_date = %s 
            WHERE material_id = %s
        ''', (data['disk'], data['ram'], data['os'], data['assigned_date'], data['completed_date'], material_id))
        connection.commit()
        return jsonify({'message': 'Material updated successfully'})
    except Exception as e:
        print(e)
        return jsonify({'message': 'An error occurred'}), 500


@app.route('/delete_material/<int:material_id>', methods=['POST'])
def delete_material(material_id):
    try:
        cursor.execute('DELETE FROM materials WHERE material_id = %s', (material_id,))
        connection.commit()
        return jsonify({'message': 'Material deleted successfully'})
    except Exception as e:
        print(e)
        return jsonify({'message': 'An error occurred'}), 500

#employees
# Employee Routes

@app.route('/employees')
def employees_index():
    cursor.execute('SELECT * FROM employees')
    employees = cursor.fetchall()
    return render_template('index_employees.html', employees=employees)

@app.route('/save_employee', methods=['POST'])
def save_employee():
    name = request.form['name']
    emp_id = request.form['emp_id']
    designation = request.form['designation']
    email = request.form['email']
    password = request.form['password']

    try:
        cursor.execute('''
            INSERT INTO employees (name, emp_id, designation, email, password)
            VALUES (%s, %s, %s, %s, %s)
        ''', (name, emp_id, designation, email, password))
        connection.commit()
        return redirect(url_for('employees_index'))
    except mysql.connector.IntegrityError as e:
        # Handle the error when duplicate emp_id is inserted
        flash('Employee with the same Employee ID already exists. Please choose a unique Employee ID.', 'error')
        return redirect(url_for('employees_index'))

@app.route('/update_employee/<int:id>', methods=['POST'])
def update_employee(id):
    data = request.get_json()
    cursor.execute('''
        UPDATE employees
        SET name = %s, emp_id = %s, designation = %s, email = %s, password = %s
        WHERE id = %s
    ''', (data['name'], data['emp_id'], data['designation'], data['email'], data['password'], id))
    connection.commit()

    return jsonify({'message': 'Employee updated successfully'})

@app.route('/delete_employee/<int:id>', methods=['POST'])
def delete_employee(id):
    cursor.execute('DELETE FROM employees WHERE id = %s', (id,))
    connection.commit()
    return jsonify({'message': 'Employee deleted successfully'})
#planning 

# Add a route to display the Planning List
@app.route('/planning')
def planning_index():
    cursor.execute('SELECT * FROM planning_data')
    plannings = cursor.fetchall()
    return render_template('index_planning.html', plannings=plannings)

# Add a route to save Planning
@app.route('/save_planning', methods=['POST'])
def save_planning():
    planning_id = request.form['planning_id']
    start_date = request.form['start_date']
    end_date = request.form['end_date']
    key_deliveries = request.form['key_deliveries']
    
    cursor.execute('''
        INSERT INTO planning_data (planning_id, start_date, end_date, key_deliveries)
        VALUES (%s, %s, %s, %s)
    ''', (planning_id, start_date, end_date, key_deliveries))
    
    connection.commit()
    return redirect(url_for('planning_index'))

# Add a route to update Planning
@app.route('/update_planning/<int:planning_id>', methods=['POST'])
def update_planning(planning_id):
    data = request.get_json()
    try:
        cursor.execute('''
            UPDATE planning_data
            SET planning_id = %s, start_date = %s, end_date = %s, key_deliveries = %s
            WHERE id = %s
        ''', (data['new_planning_id'], data['start_date'], data['end_date'], data['key_deliveries'], planning_id))

        connection.commit()
        return jsonify({'message': 'Planning updated successfully'})
    except Exception as e:
        print(e)
        return jsonify({'message': 'An error occurred'}), 500


# Add a route to delete Planning
@app.route('/delete_planning/<int:id>', methods=['POST'])
def delete_planning(id):
    cursor.execute('DELETE FROM planning_data WHERE id = %s', (id,))
    connection.commit()
    return jsonify({'message': 'Planning deleted successfully'})



if __name__ == '__main__':
    app.run(debug=True)