import json
import pyodbc
import os

# Azure SQL Database connection details
server = os.getenv("AZURE_SQL_SERVER")  # e.g., "your-server.database.windows.net"
database = os.getenv("AZURE_SQL_DATABASE")  # e.g., "your-database"
username = os.getenv("AZURE_SQL_USERNAME")  # e.g., "your-username"
password = os.getenv("AZURE_SQL_PASSWORD")  # e.g., "your-password"

def query_azure_sql(query):
    """
    Executes a query on the Azure SQL Database and returns the results.

    :param query: SQL query string
    :return: Query results as a list of tuples
    """
    
    try:
        # Establish the connection
        connection_string = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}"
        with pyodbc.connect(connection_string) as conn:
            with conn.cursor() as cursor:
                cursor.execute(query)
                results = cursor.fetchall()
                columns = [column[0] for column in cursor.description]
                data = [dict(zip(columns, row)) for row in results]
                json_data = json.dumps(data, default=str)  # Convert to JSON string if needed
                return json_data
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Example usage
if __name__ == "__main__":
    sample_query = "SELECT TOP 1 due_date FROM payment WHERE status = 'Pending' ORDER BY due_date ASC;"
    results = query_azure_sql(sample_query)
    if results:
        for row in results:
            print(row)