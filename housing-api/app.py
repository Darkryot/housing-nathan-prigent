from flask import Flask, request, jsonify
import psycopg2 as psycopg
app = Flask(__name__)


conn = psycopg.connect(database="postgres", user="postgres", password="2005", host="127.0.0.1", port="5432")
conn.autocommit = True
cur = conn.cursor()

cur.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s", ('house',))

exists = cur.fetchone()
if not exists:
    cur.execute('CREATE DATABASE house;')
    print("Database 'house' created successfully!")

elif exists:
    print("The database already exists")

cur.close()
conn.close()


conn = psycopg.connect(database="house", user="postgres", password="2005", host="127.0.0.1", port="5432")
conn.autocommit = True
cur = conn.cursor()


def table_exists(table_name):
    cur.execute('''
        SELECT EXISTS (
            SELECT 1 
            FROM information_schema.tables 
            WHERE table_schema = 'public'  -- Replace with your schema if necessary
            AND table_name = %s
        );
    ''', (table_name,))
    return cur.fetchone()[0]


if not table_exists('houses'):
    cur.execute('''
        CREATE TABLE houses (
            house_id INT UNIQUE,
            longitude FLOAT,
            latitude FLOAT,
            housing_median_age INT,
            total_rooms INT,
            total_bedrooms INT,
            population INT,
            households INT,
            median_income FLOAT,
            median_house_value FLOAT, 
            ocean_proximity VARCHAR(255),
            PRIMARY KEY(house_id)
        )
    ''')
    print("Table 'houses' created successfully!")
else:
    print("Table 'houses' already exists.")


def get_all_houses():
    houses = cur.fetchall()
    dico = dict()
    for house in houses:
        dico.append(house)

    return dico


def get_all_houses():
    cur.execute('SELECT * FROM houses')
    houses = cur.fetchall()

    l_house = []
    columns = [desc[0] for desc in cur.description]
    for house in houses:
        l_house.append(dict(zip(columns, house)))

    return l_house


@app.route('/houses', methods=['GET'])
def get_house():
    houses = get_all_houses()
    return jsonify(houses)


@app.route('/houses', methods=['POST'])
def set_house():
    request_data = request.json

    query = '''
        INSERT INTO houses (
            house_id, longitude, latitude, housing_median_age, total_rooms, total_bedrooms, 
            population, households, median_income, median_house_value, ocean_proximity
        ) 
        VALUES (
            %(house_id)s, %(longitude)s, %(latitude)s, %(housing_median_age)s, %(total_rooms)s, %(total_bedrooms)s, 
            %(population)s, %(households)s, %(median_income)s, %(median_house_value)s, %(ocean_proximity)s
        )
    '''

    cur.execute(query, request_data)

    return jsonify({"message": "House added successfully!"}), 201


if __name__ == '__main__':
    print('''
   
          Pour vérifier la connexion : curl http://localhost:5000/products
 
          Post:
            - On Windows:
                   - Invoke-WebRequest -Uri http://localhost:5000/products -Method 
                     POST -Headers @{"Content-Type"="application/json"} -Body 
                     '{}'
     
            - On Linux:
                    - curl -X POST http://localhost:5000/products -H "Content-Type: application/json" 
                      -d '{"house_id":..., "longitude":..., "latitude":..., "housing_median_age":..., "total_rooms":..., "total_bedrooms":..., 
            "population":..., "households":..., "median_income":..., "median_house_value":..., "ocean_proximity":...}'

            ''')

    app.run(host='0.0.0.0', port=5000, debug=True)