# Pflanzeninformationen
plants = {
    "Karotten": {"plant_spacing": 1, "row_spacing": 10},
    "Salat": {"plant_spacing": 25, "row_spacing": 25},
    "Rote Beete" : {"plant_spacing": 5, "row_spacing": 20}
}

# Beetgröße (in cm)
beet_width = 100
beet_height = 100

def calculate_sowing_pattern(beet_width, beet_height, plants):
    pattern = []
    y_position = 0
    plant_types = list(plants.keys())
    plant_index = 0

    while y_position < beet_height:
        plant = plant_types[plant_index % len(plant_types)]
        row_spacing = plants[plant]["row_spacing"]
        plant_spacing = plants[plant]["plant_spacing"]
        initial_x_position = round(plant_spacing / 2)

        if y_position + row_spacing > beet_height:
            break

        row = []
        x_position = initial_x_position

        while x_position < beet_width:
            row.append(plant[0])  # Use the first letter of the plant name
            x_position += plant_spacing

        pattern.append((plant, row, y_position))
        y_position += row_spacing
        plant_index += 1

    return pattern

def print_sowing_pattern(pattern, plants, beet_width, beet_height):
    beet_grid = [['.' for _ in range(beet_width)] for _ in range(beet_height)]

    for plant, row, y_start in pattern:
        plant_spacing = plants[plant]["plant_spacing"]
        initial_x_position = round(plant_spacing / 2)
        for i, plant_name in enumerate(row):
            x_position = initial_x_position + i * plant_spacing
            if x_position < beet_width:
                beet_grid[y_start][x_position] = plant_name

    for line in beet_grid:
        print("".join(line))

# Saatmuster berechnen
sowing_pattern = calculate_sowing_pattern(beet_width, beet_height, plants)

# Saatmuster ausgeben
print_sowing_pattern(sowing_pattern, plants, beet_width, beet_height)
