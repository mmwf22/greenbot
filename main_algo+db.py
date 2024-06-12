# Improt of needed modules
import sqlite3

# Functions

## Get plant information from DB and save into variable
def fetch_plants_from_db(db_path='db/plants.db'):
    # Connect to DB
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Fetch plant data from DB
    cursor.execute("SELECT name, pflanzabstand, reihenabstand FROM Pflanzen")
    plants = cursor.fetchall()

    conn.close()
    return plants

## Present plant choice to user
def display_plant_options(plants):
    print("Verfügbare Pflanzen:")
    for idx, plant in enumerate(plants, start=1):
        print(f"{idx}. {plant[0]} (Pflanzabstand: {plant[1]} cm, Reihenabstand: {plant[2]} cm)")

## Let the user choose the plants to sow
def get_user_selection(plants):
    selected_plants = []
    while True:
        display_plant_options(plants)
        try:
            choice = int(input("Geben Sie die Nummer der Pflanze ein, die Sie auswählen möchten (0 zum Beenden): "))
            if choice == 0:
                break
            elif 1 <= choice <= len(plants):
                selected_plants.append(plants[choice - 1])
                print(f"Pflanze {plants[choice - 1][0]} hinzugefügt.")
            else:
                print("Ungültige Auswahl. Bitte versuchen Sie es erneut.")
        except ValueError:
            print("Ungültige Eingabe. Bitte geben Sie eine Zahl ein.")
    return selected_plants

## Calculate sowing pattern based on user selection
def calculate_sowing_pattern(bed_width, bed_height, plants):
    pattern = []
    plant_index = 0

    initial_y_position = int(round(plants[0][2] / 2))
    y_position = initial_y_position

    while y_position + int(round(plants[plant_index % len(plants)][2] / 2)) < bed_height:
        plant = plants[plant_index % len(plants)]
        row_spacing = plant[2]
        plant_spacing = plant[1]
        initial_x_position = int(round(plant_spacing / 2))

        row = []
        x_position = initial_x_position
        toggle = False

        while x_position < bed_width:
            # Adjust y_position for zig-zag pattern
            if toggle:
                row_y_position = y_position + int(round(plant_spacing / 2))
            else:
                row_y_position = y_position
            
            row.append((plant[0], x_position, row_y_position))
            x_position += plant_spacing
            toggle = not toggle

        pattern.append(row)
        y_position += row_spacing
        plant_index += 1

    # Determine if any selected plants were not planted
    planted_plants = set(p[0] for row in pattern for p in row)
    not_planted_plants = [p[0] for p in plants if p[0] not in planted_plants]

    return pattern, not_planted_plants

## Print out seeding pattern to console
def print_sowing_pattern(pattern, bed_width, bed_height):
    bed_grid = [['.' for _ in range(bed_width)] for _ in range(bed_height)]

    for row in pattern:
        for plant, x_pos, y_pos in row:
            if 0 <= x_pos < bed_width and 0 <= y_pos < bed_height:
                bed_grid[int(y_pos)][int(x_pos)] = plant[0]

    for line in bed_grid:
        print("".join(line))

    return bed_grid


# Main
plants = fetch_plants_from_db()
selected_plants = get_user_selection(plants)

# Exit programm if no plants have been chosen by user
if not selected_plants:
    print("Keine Pflanzen ausgewählt. Beenden...")
    exit()

## Garden bed size
bed_width = 100
bed_height = 100

## Calculate sowing pattern and print it to console
sowing_pattern, not_planted_plants = calculate_sowing_pattern(bed_width, bed_height, selected_plants)
print_sowing_pattern(sowing_pattern, bed_width, bed_height)

## Print a message if some plants could not be planted
if not_planted_plants:
    print("Die folgenden Pflanzen konnten wegen des begrenzte Platzes nicht gepflanzt werden:")
    for plant in not_planted_plants:
        print(f"- {plant}")
