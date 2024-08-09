import os
from remi import start, App
from remi.gui import VBox, HBox, Button, Label, Table, TableRow, TableItem, CheckBox, Widget
import sqlite3

# Globale Variable für die Pflanzenliste
global_plants = []

class PlantRobotApp(App):
    def __init__(self, *args):
        super(PlantRobotApp, self).__init__(*args)
        self.selected_plants = []
        self.unicode_icons = {
            'Kopfsalat': '🥬',
            'Ruebli': '🥕',
            'Randen': '🍠',
            'Buschbohnen': '🌿',
            'Peperoni lang': '🌶️',
            'Glockenpeperoni': '🫑',
            'Chili': '🌶',
            'Kohlrabi': '🥦',
            'Broccoli': '🥦',
            'Rosenkohl': '🌱',
            'Tomaten': '🍅',
            'Cherry-Tomaten': '🍒',
            'Schnittsalat': '🥗',
            'Pak Choi': '🥬',
            'Mangold': '🥬',
            'Basilikum': '🌿',
            'Petersilie': '🌿',
            'Dill': '🌿'
        }

    def main(self):
        # Hauptcontainer als HBox
        self.main_container = HBox(width='100%', height='100%', style={'justify-content': 'space-between', 'background-color': '#f8f8f8'})

        # Linker Bereich: Gitter zur Anzeige des Pflanzenmusters
        self.pattern_grid = Table(width='100%', height='100%', style={'border': '1px solid #ccc', 'background-color': '#fff'})
        self.main_container.append(self.pattern_grid, '75%')

        # Rechter Bereich: VBox für Pflanzeninformationen, Pflanzenliste, Logo und Button
        right_container = VBox(width='25%', height='100%', style={'border': '1px solid #ccc', 'background-color': '#fff', 'padding': '10px'})
        self.main_container.append(right_container)

        # Pflanzeninformationen
        self.plant_info_box = VBox(width='100%', height='30%', style={'margin-bottom': '10px'})
        right_container.append(self.plant_info_box)

        # Scrollbare Liste mit Pflanzen
        self.plant_buttons_container = VBox(width='100%', height='50%', style={'overflow-y': 'scroll', 'border': '1px solid #ccc', 'margin-bottom': '10px'})
        right_container.append(self.plant_buttons_container)

        # Logo
        self.logo = Label("🌱 Greenbot", width='100%', height='10%', style={'font-size': '24px', 'text-align': 'center', 'margin-bottom': '10px'})
        right_container.append(self.logo)

        # Bestätigungsbutton zur Erstellung des Saatmusters
        self.confirm_button = Button("Saatmuster erstellen", style={
            'margin': '10px', 
            'padding': '10px', 
            'font-size': '16px',
            'font-weight': 'bold', 
            'background-color': '#4CAF50', 
            'color': 'white', 
            'border': 'none', 
            'border-radius': '4px', 
            'box-shadow': '0 4px 8px 0 rgba(0, 0, 0, 0.2)', 
            'transition': '0.3s',
            'cursor': 'pointer'
        })
        self.confirm_button.onclick.do(self.create_sowing_pattern)
        right_container.append(self.confirm_button, '10%')

        # Pflanzen aus der Datenbank laden und Buttons erstellen
        self.load_plants_from_db()

        return self.main_container

    def load_plants_from_db(self):
        global global_plants

        # Absoluter Pfad zur Datenbankdatei
        base_dir = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(base_dir, '..', 'db', 'plants.db')

        if not os.path.exists(db_path):
            raise FileNotFoundError(f"Die Datenbankdatei wurde nicht gefunden: {db_path}")

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name, pflanzabstand, reihenabstand FROM Pflanzen")
        global_plants = cursor.fetchall()
        conn.close()

        for plant in global_plants:
            plant_box = HBox(style={'margin': '5px', 'align-items': 'center'})
            checkbox = CheckBox()
            checkbox.set_value(False)
            checkbox.attributes['value'] = plant[0].strip()  # Pflanzennamen als Checkbox-Wert hinzufügen und trimmen
            checkbox.onchange.do(self.on_plant_checkbox_change)
            plant_label = Label(plant[0], style={'margin-left': '5px', 'font-size': '14px', 'font-weight': 'bold'})
            info_button = Button('Info', width=50, height=30, style={'margin-left': '10px'})
            info_button.onclick.do(self.on_plant_button_click, plant)
            plant_box.append(checkbox)
            plant_box.append(plant_label)
            plant_box.append(info_button)
            self.plant_buttons_container.append(plant_box)

    def on_plant_checkbox_change(self, widget, value):
        global global_plants
        plant_name = widget.attributes['value'].strip()  # Sicherstellen, dass der Name getrimmt wird
        checked = widget.get_value()

        # Pflanze anhand des Namens finden
        plant = next((p for p in global_plants if p[0] == plant_name), None)

        if plant:
            if checked:
                if plant not in self.selected_plants:
                    self.selected_plants.append(plant)
                    print(f"Füge {plant[0]} zu ausgewählten Pflanzen hinzu.")
            else:
                self.selected_plants = [p for p in self.selected_plants if p[0] != plant[0]]
                print(f"Entferne {plant[0]} von den ausgewählten Pflanzen.")
        else:
            print(f"Fehler: Pflanze {plant_name} nicht gefunden.")
        
        print(f"Ausgewählte Pflanzen: {[p[0] for p in self.selected_plants]}")

    def create_sowing_pattern(self, widget):
        if not self.selected_plants:
            self.plant_info_box.empty()
            self.plant_info_box.append(Label("Keine Pflanzen ausgewählt.", style={'font-size': '16px', 'color': 'red'}))
            return

        # Beetgröße auf 100x100 Kästchen setzen (1 Kästchen = 1cm)
        beet_width = 60  # Diese Größe repräsentiert 100cm x 100cm (1m x 1m)
        beet_height = 60

        # Saatmuster berechnen und anzeigen
        pattern, not_planted_plants = self.calculate_sowing_pattern(beet_width, beet_height, self.selected_plants)
        beet_grid = self.generate_sowing_pattern_grid(pattern, beet_width, beet_height)

        print(f"Berechnetes Saatmuster:\n{pattern}")
        
        # Pflanzenmuster im GUI anzeigen
        self.display_pattern_grid(beet_grid)

    def on_plant_button_click(self, widget, plant):
        self.plant_info_box.empty()
        self.plant_info_box.append(Label(f"Name: {plant[0]}", style={'font-size': '16px', 'font-weight': 'bold'}))
        self.plant_info_box.append(Label(f"Pflanzabstand: {plant[1]} cm", style={'font-size': '14px'}))
        self.plant_info_box.append(Label(f"Reihenabstand: {plant[2]} cm", style={'font-size': '14px'}))

    def calculate_sowing_pattern(self, beet_width, beet_height, plants):
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

    def generate_sowing_pattern_grid(self, pattern, beet_width, beet_height):
        beet_grid = [['' for _ in range(beet_width)] for _ in range(beet_height)]

        for row in pattern:
            for plant, x_pos, y_pos in row:
                if 0 <= x_pos < beet_width and 0 <= y_pos < beet_height:
                    beet_grid[int(y_pos)][int(x_pos)] = self.unicode_icons.get(plant, '')

        return beet_grid

    def display_pattern_grid(self, beet_grid):
        # Berechnung der Größe des Beetes basierend auf festen Werten
        beet_width = len(beet_grid[0])
        beet_height = len(beet_grid)
        
        # Festlegen der Maximalgröße des Grids in Pixeln (z.B. 900x900)
        max_width_pixels = 900
        max_height_pixels = 900
        
        # Berechnung der Zellengröße
        cell_width = max_width_pixels / beet_width
        cell_height = max_height_pixels / beet_height
        cell_size = min(cell_width, cell_height)
        
        # Anpassung der Zellen
        self.pattern_grid.empty()
        for row in beet_grid:
            table_row = TableRow()
            for cell in row:
                table_item = TableItem(cell, style={
                    'width': f'{cell_size}px', 
                    'height': f'{cell_size}px', 
                    'font-size': f'{int(cell_size * 0.8)}px',  # Schriftgröße an Zellengröße anpassen
                    'text-align': 'center', 
                    'vertical-align': 'middle',
                    'border': '1px solid #ddd'
                })
                table_item.attributes['onmouseover'] = "this.style.fontSize='{}px'".format(int(cell_size * 2.5))
                table_item.attributes['onmouseout'] = "this.style.fontSize='{}px'".format(int(cell_size * 0.8))
                table_item.onclick.do(self.on_cell_click, table_item, cell)
                table_row.append(table_item)
            self.pattern_grid.append(table_row)

    def on_cell_click(self, widget, item, cell):
        widget.style['font-size'] = '{}px'.format(int(widget.style['font-size'].replace('px', '')) * 1.5)

if __name__ == "__main__":
    start(PlantRobotApp, address='0.0.0.0', port=8081, start_browser=True)
