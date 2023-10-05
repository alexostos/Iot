from datetime import datetime
import random
import mysql.connector
import plotly.express as px
import pandas as pd
from dash import Dash, html, dash_table, dcc


def createConnection(user_name, database_name, user_password, host, port):
    """Creates a connection to the mysql database
    
    Parameters
    -----------
        user_name {string} -- The username to the database
        database_name {string} -- The name of the database
        user_password {string} -- The password to the database
        host {string} -- The host of the database
        port {string} -- The port of the database

    Returns
    --------
        tuple -- A tuple containing the connection and the cursor
    """
    cnx = mysql.connector.connect(user=user_name, database=database_name, password=user_password, host=host, port=port)
    cursor = cnx.cursor()
    return (cnx, cursor)

def select_data():
    """Selects all the data from the database"""
    try:
        # Create a connection to the database
        cnx, cursor = createConnection('root', 'new_schema', 'Alex1912', 'localhost', '3306')

        # Query the database
        query = ("SELECT * FROM dht_sensor_data")

        # Execute the query
        cursor.execute(query)

        # Get the data
        data = cursor.fetchall()

        # Return the data
        return data
    
    except mysql.connector.Error as err:
        """Handle possible errors"""
        if err.errno == mysql.connector.errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    finally:
        """Close the connection"""
        if ('cnx' in locals() or 'cnx' in globals()) and ('cursor' in locals() or 'cursor' in globals()):
            cnx.close()
            cursor.close()

def insert_data():
    """Inserts random sensor data into the database"""
    try:
         # Generate random sensor data
        hum = str(random.uniform(0, 100))
        temp = str(random.uniform(0, 100))
        date = str(datetime.now())

        # Create a connection to the database
        # TODO: Call the createConnection() function and store the connection and cursor in variables. 
        # Dont forget to pass in the correct parameters
        cnx, cursor = createConnection('root', 'new_schema', 'Alex1912', 'localhost', '3306')

        # Insert the data into the database
        query = (f"insert into dht_data (humidity, temperature, date_time) values ({hum}, {temp}, '{date}')")

        # TODO: Create the query string that inserts the data you created into the database
        # The query string should be an insert statement that inserts the data into the dht_sensor_data table

        # Insert the data into the database
        # TODO: Execute the query string you created
        cursor.execute(query)

        # Commit the changes
        cnx.commit()

        print("Data inserted successfully")

    except mysql.connector.Error as err:
        """Handle possible errors"""
        if err.errno == mysql.connector.errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    finally:
        """Close the connection"""
        if ('cnx' in locals() or 'cnx' in globals()) and ('cursor' in locals() or 'cursor' in globals()):
            cnx.close()
            cursor.close()

if __name__ == '__main__':
    # Se agregan los 100 datos de la tabla, se llaman a los datos para mostrarlos
    for _ in range(100):
        insert_data()

def fetch_data():
    try:
        cnx, cursor = createConnection('root', 'new_schema', 'Alex1912', 'localhost', '3306')
        query = "SELECT id_dht_data, humidity, temperature FROM dht_data"      
        cursor.execute(query)
        data = cursor.fetchall()
        
        return data

    except mysql.connector.Error as err:
        print(err)

if __name__ == '__main__':
    data = fetch_data()
    df = pd.DataFrame(data, columns=["id", 'humidity', 'temperature'])
    fig = px.line(df, x='id', y=['humidity', 'temperature'], title='Humidity and Temperature Over Time')
    fig.show()

    app = Dash("name")
    app.layout = html.Div([
        html.Div(
            children=[
                html.H1("Actividad datos dash. IOT", style={'text-align': 'center'}),
                html.P("Esta grafica muestra los resultados de la humedad y la temperatura a traves del tiempo, hay que tomar en cuenta que los datos que se muestran no son reales, son generados de manera aleatoria"),
                dcc.Graph(figure=px.line(df, x='id', y=['humidity', 'temperature'], title="Humidity and Temperature vs id")),
            ])
    ])

    app.run_server(debug=True)