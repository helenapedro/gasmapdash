import mysql.connector
import json

# Read the scraped data from the JSON file
file_path = './gas_stations.json'
with open(file_path, 'r', encoding='utf-8') as file:
    scraped_data = json.load(file)

# Setup your database connection
db_connection = mysql.connector.connect(
    host="srv1146.hstgr.io",
    user="u894841105_mapeamento0317",
    password="Mapeamento03176",
    database="u894841105_mapeamento"
)
cursor = db_connection.cursor()

# Delete all records for operator_id = 3 (uncomment if you need to reset previous data)
# delete_query = "DELETE FROM gas_stations WHERE operator_id = %s"
# cursor.execute(delete_query, (3,))
# db_connection.commit()

# Begin transaction
db_connection.start_transaction()

# Map the scraped data and insert it into the gas_stations table
if isinstance(scraped_data, list): 
    for station in scraped_data:  # Directly iterate over the list
        # Extract the municipality name from the city field (assumes format "City - Municipality")
        city = station['city']
        municipality_name = city.split(" - ")[-1]  # Extract the part after the dash
        
        # Query for the municipality_id and province_id based on the extracted municipality_name
        municipality_query = "SELECT municipality_id, province_id FROM Municipalities WHERE municipality_name = %s"
        cursor.execute(municipality_query, (municipality_name,))
        municipality_result = cursor.fetchone()
        
        # If municipality doesn't exist, insert it
        if not municipality_result:
            # Extract the province_id (assuming the province is part of the city, e.g., "Dande")
            province_name = city.split(" - ")[-1]  # Assuming the province is the part after the dash
            # Query to get the province_id based on the province name
            cursor.execute("SELECT province_id FROM Provinces WHERE province_name = %s", (province_name,))
            province_result = cursor.fetchone()
            if province_result:
                province_id = province_result[0]
            else:
                # Set default or handle the case when the province is not found
                province_id = None
            
            # Insert the new municipality into the Municipalities table
            insert_municipality_query = """
                INSERT INTO Municipalities (municipality_name, province_id)
                VALUES (%s, %s)
            """
            cursor.execute(insert_municipality_query, (municipality_name, province_id))
            db_connection.commit()
            
            # Fetch the municipality_id after insertion
            municipality_id = cursor.lastrowid
        else:
            # If municipality exists, use the existing municipality_id and province_id
            municipality_id, province_id = municipality_result

        # Ensure the country_id is 1 (Angola)
        country_id = 1
        
        # Insert the data into the gas_stations table
        insert_query = """
            INSERT INTO gas_stations (station_name, address, latitude, longitude, municipality_id, operator_id)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (
            station['name'],  # station_name
            station['address'],  # address
            station['latitude'],  # latitude
            station['longitude'],  # longitude
            municipality_id,  # municipality_id (existing or newly inserted)
            3  # operator_id is 3 (Pumangol)
        ))
        db_connection.commit()

# Commit the transaction after all inserts
db_connection.commit()

# Close the cursor and connection
cursor.close()
db_connection.close()
