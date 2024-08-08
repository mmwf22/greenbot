def calculate_sowing_pattern(plants, beet_width, beet_height):
    pattern = []
    plant_index = 0
    initial_y_position = int(round(plants[0][2] / 2))
    y_position = initial_y_position

    while y_position + int(round(plants[plant_index % len(plants)][2] / 2)) < beet_height:
        plant = plants[plant_index % len(plants)]
        row_spacing = plant[2]
        plant_spacing = plant[1]
        initial_x_position = int(round(plant_spacing / 2))

        row = []
        x_position = initial_x_position
        toggle = False

        while x_position < beet_width:
            row_y_position = y_position if not toggle else y_position + int(round(plant_spacing / 2))
            row.append((plant[0], x_position, row_y_position))
            x_position += plant_spacing
            toggle = not toggle

        pattern.append(row)
        y_position += row_spacing
        plant_index += 1

    planted_plants = set(p[0] for row in pattern for p in row)
    not_planted_plants = [p[0] for p in plants if p[0] not in planted_plants]

    return pattern, not_planted_plants
