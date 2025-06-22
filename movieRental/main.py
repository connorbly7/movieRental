from extract import extract_data
from transform import transform_data
from load import load_data


# Extract data
customers, employees, movies, rentals = extract_data()

# Transform data
customers, employees, movies, rentals = transform_data(customers, employees, movies, rentals)

# Load data
load_data(customers, employees, movies, rentals)
