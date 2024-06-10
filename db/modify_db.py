import sqlite3

def print_plants():
    # Connect to the SQLite database
    conn = sqlite3.connect('db/plants.db')
    cursor = conn.cursor()

    # Query to select all plants
    cursor.execute('SELECT * FROM Pflanzen')
    plants = cursor.fetchall()

    # Print each plant with its attributes
    for plant in plants:
        print(f"Name: {plant[1]}, Pflanzabstand: {plant[2]}, Reihenabstand: {plant[3]}, Saattiefe: {plant[4]}")

    # Close the connection
    conn.close()

def lower_values_by_30_percent():
    # Connect to the SQLite database
    conn = sqlite3.connect('db/plants.db')
    cursor = conn.cursor()

    # Query to select all plants
    cursor.execute('SELECT * FROM Pflanzen')
    plants = cursor.fetchall()

    # Calculate the new values and update the database
    for plant in plants:
        name = plant[1]
        pflanzabstand = round(float(plant[2]) * 0.7, 1)
        reihenabstand = round(float(plant[3]) * 0.7, 1)
        saattiefe = float(plant[4])

        cursor.execute('UPDATE Pflanzen SET pflanzabstand = ?, reihenabstand = ?, saattiefe = ? WHERE name = ?', 
                       (pflanzabstand, reihenabstand, saattiefe, name))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

# Call the functions
print("Before lowering values:")
print_plants()

lower_values_by_30_percent()

print("\nAfter lowering values by 30%:")
print_plants()
