# import sqlite3

# # Get Plantdata from Database
# def fetch_plant_data(plant_names):
#     conn = sqlite3.connect('db/plants.db')
#     cursor = conn.cursor()
    
#     placeholders = ','.join('?' for _ in plant_names)
#     query = f"SELECT name, pflanzabstand, reihenabstand FROM Pflanzen WHERE name IN ({placeholders})"
#     cursor.execute(query, plant_names)
    
#     plant_data = cursor.fetchall()
#     conn.close()
    
#     return plant_data

# plant_data = fetch_plant_data(['Kopfsalat', 'Randen', 'Ruebli'])
# print(fetch_plant_data(['Kopfsalat', 'Randen', 'Ruebli']))

import sqlite3

# Function to fetch plant data from the database
def fetch_plant_data(plant_names):
    conn = sqlite3.connect('db/plants.db')
    cursor = conn.cursor()
    
    placeholders = ','.join('?' for _ in plant_names)
    query = f"SELECT name, pflanzabstand, reihenabstand FROM Pflanzen WHERE name IN ({placeholders})"
    cursor.execute(query, plant_names)
    
    plant_data = cursor.fetchall()
    conn.close()
    
    return plant_data

# Function to calculate the seed pattern
def calculate_seed_pattern(bed_width, bed_height, plant_data):
    grid = [['_' for _ in range(bed_width)] for _ in range(bed_height)]
    
    current_row = 0
    for plant in plant_data:
        name, plant_spacing, row_spacing = plant
        plant_spacing = int(plant_spacing)
        row_spacing = int(row_spacing)
        
        # Fill rows with the current plant type
        for _ in range(row_spacing):
            if current_row >= bed_height:
                break
            
            for col in range(0, bed_width, plant_spacing):
                grid[current_row][col] = name[:2]  # Display first two letters of plant name
            
            current_row += 1

            if current_row >= bed_height:
                break
    
    return grid

# Function to display the seed pattern in the terminal
def display_seed_pattern(seed_pattern):
    for row in seed_pattern:
        print(' '.join(row))

if __name__ == "__main__":
    # Sample bed dimensions (adjust as needed)
    bed_width = 200
    bed_height = 100
    
    # Sample plant names
    plant_names = ['Kopfsalat', 'Randen', 'Ruebli']
    
    plant_data = fetch_plant_data(plant_names)
    seed_pattern = calculate_seed_pattern(bed_width, bed_height, plant_data)
    display_seed_pattern(seed_pattern)
