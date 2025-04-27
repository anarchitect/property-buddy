import random

def generate_unique_id(source_string):
    """
    Generates a 6-digit unique identifier where the first part is retrieved
    from a string after a hyphen (with no character requirements), and the
    second part is a random three-digit number.

    Args:
        source_string (str): A string containing a hyphen, where the part after
                             the hyphen is used for the first part.

    Returns:
        str: A unique identifier in the format 'XXX-XXX'.
    
    Example:
        If the source_string is "unit-3", the first part after the hyphen
        would be "3", and the second part would be a random number between
        100 and 999.
        Example Output: "3-456" (where "456" is a random number)
    """
    # Extract the part after the hyphen
    first_part = source_string 
    # //.split('-')[-1]
    # Generate the second part randomly
    second_part = f"{random.randint(100, 999)}"
    unique_id = f"{first_part}-{second_part}"
    return unique_id

# Example usage
# if __name__ == "__main__":
#     source = "unit-3"
#     unique_id = generate_unique_id(source)
#     print(f"Generated Unique ID: {unique_id}")
#     # Extract the part after the hyphen
#     first_part = source_string.split('-')[-1][:3]
#     # Generate the second part randomly
#     second_part = f"{random.randint(100, 999)}"
#     unique_id = f"{first_part}-{second_part}"
#     return unique_id

# # Example usage
# if __name__ == "__main__":
#     source = "ABC-DEF"
#     unique_id = generate_unique_id(source)
#     print(f"Generated Unique ID: {unique_id}")