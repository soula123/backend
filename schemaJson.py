
"""
this code retrieves the schema of an oracle 
database an saves it to a json file called schema.json
"""
import cx_Oracle
import json

# Connect to the database
connection = cx_Oracle.connect('root/root@172.17.0.2:1521/ORCLCDB')

# Get the schema information using a cursor
cursor = connection.cursor()
cursor.execute("""
    SELECT table_name, column_name, data_type
    FROM all_tab_columns
    WHERE owner = :owner
    ORDER BY table_name, column_id
""", owner="ROOT")

# Build the schema dictionary
schema = {}
for table_name, column_name, data_type in cursor:
    if table_name not in schema:
        schema[table_name] = []
    schema[table_name].append((column_name, data_type))
print(schema)
# Save the schema to a JSON file
with open('exemple_schema.json', 'w') as f:
    json.dump(schema, f, indent=4)

# Close the database connection
connection.close()
