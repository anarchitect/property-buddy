functions = [
    {
        "name": "get_weather",
        "description": "Get the current weather in a city",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {"type": "string", "description": "City name"},
            },
            "required": ["location"],
        },
    },
    {
        "name": "create_maintenance_request",
        "description": "Send a maintenance request to the property manager.",
        "parameters": {
            "type": "object",
            "properties": {
                "description": {"type": "string", "description": "Description of the maintenance issue."},
                "required_category_of_maintenance_provider": {
                    "type": "string",
                    "enum": ["plumber", "electrician", "cleaning", "handyman"],
                    "description": "The category of maintenance request to send to the property manager, which will also be used to send to a list of service providers."
                },
                "is_description_in_english": {
                    "type": "boolean",
                    "description": "Indicates whether the description is in English."
                },
                "translated_english_description": {
                    "type": "string",
                    "description": "The translated description of the maintenance issue in English, if the original description is not in English."
                },
            },
            "required": ["description", "is_description_in_english"],
        },
    },
    {
        "name": "get_maintenance_request_details",
        "description": "Get the status, estimated date, quote, and contact of the service provider of a maintenance request.",
    },
    {
        "name": "get_payments",
        "description": "Get payments information from the payment table.",
        "parameters": {
            "type": "object",
            "properties": {
                "sql_query": {
                    "type": "string",
                    "description": (
                        "Generated SQL query based on the provided description. "
                        "The SQL is for a payment table with these columns "
                        "(amount, due_date, payee, payment_type, status). "
                        "the status column can be one of these values (Paid, Overdue, Pending). "
                        "the table schema is 'CREATE TABLE payment (payment_id INT IDENTITY(1,1) PRIMARY KEY, amount DECIMAL(10, 2) NOT NULL, due_date DATE NOT NULL, payee NVARCHAR(100) NOT NULL, payment_type NVARCHAR(50) NOT NULL, status NVARCHAR(20) NOT NULL), customer_id NVARCHAR(50) NOT NULL;' "
                        "Only generate SQL query with syntax for Azure SQL Database. "
                        "Only generate select SQL query and ensure no SQL vulnerability."
                        "In the columns to be selected in the generated query, if possible, please include as many columns as possible. "
                        "In the generated query, also add a WHERE clause to filter the results based on the customer_id column. and value in the customer_id filter is a placeholder called {customer_id}."
                        "Only generate SQL queries, do not generate natural language."
                    )
                }
            }
        }
    }
]