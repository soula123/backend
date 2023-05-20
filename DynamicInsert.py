import sqlite3
import cx_Oracle
import re
# Connect to the first database
connection = cx_Oracle.connect('root/root@172.17.0.2:1521/ORCLCDB')
c1 = connection.cursor()


# Execute the SELECT query on the first database
query = """
        SELECT countries.country_name , countries.country_id ,regions.region_name 
        FROM countries 
        INNER JOIN regions 
        ON regions.region_id = countries.region_id
        """
c1.execute(query)

# Fetch the results of the query and the column names
results = c1.fetchall()
col_names = [desc[0] for desc in c1.description]
col_info = c1.description
# Generate the INSERT statement dynamically based on the column names
insert_statement = "INSERT INTO table_name (" + ", ".join(col_names) + ") VALUES (" + ", ".join("?" * len(col_names)) + ")"


# Extract table and column names using regular expressions
table1_columns = re.findall(r'countries\.(\w+)', query)
table2_columns = re.findall(r'regions\.(\w+)', query)
tables = list(set(re.findall(r'\b[A-Za-z]+\b', query)))
print(tables)
"""
# Insert the results into the second database
for row in results:
    #c2.execute(insert_statement, row)
    print(insert_statement, row)

# Commit the changes to the second database
conn2.commit()

# Close the connections
c1.close()
c2.close()
conn1.close()
conn2.close()
"""
c1.close()
connection.close()