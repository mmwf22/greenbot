from remi import start, App
from remi.gui import VBox, HBox, Button, Label, Table, TableRow, TableItem, CheckBox, TextInput, TabBox
from controller.plant_robot_controller import PlantRobotController
from model import db


class PlantRobotApp(App):
    def __init__(self, *args, **kwargs):
        print("PlantRobotApp: __init__ aufgerufen")
        super(PlantRobotApp, self).__init__(*args, **kwargs)
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
            'Rosenkohl': '🌱',
            'Tomaten': '🍅',
            'Cherry-Tomaten': '🍒',
            'Schnittsalat': '🥗',
            'Mangold': '🥬',
            'Petersilie': '🌿',
            'Dill': '🌿'
        }

    def main(self):
        if not hasattr(self, 'controller'):
            self.controller = PlantRobotController(self)
            print("PlantRobotApp: Controller initialisiert in main")

        print("PlantRobotApp: main aufgerufen")
        self.main_container = HBox(width='100%', height='100%', style={'background-color': '#f8f8f8'})

        left_container = VBox(width='75%', height='100%', style={'border': '1px solid #ccc', 'background-color': '#fff'})
        self.main_container.append(left_container)

        self.pattern_grid = Table(width='100%', height='100%', style={'border': '1px solid #ccc', 'background-color': '#fff'})
        left_container.append(self.pattern_grid)

        right_container = VBox(width='25%', height='100%', style={'border': '1px solid #ccc', 'background-color': '#fff', 'padding': '10px'})
        self.main_container.append(right_container)

        tab_box = TabBox(width='100%', height='70%', style={'background-color': '#fff'})
        right_container.append(tab_box)

        # Informations-Panel hinzufügen
        self.info_panel = VBox(width='100%', height='20%', style={'border-top': '1px solid #ccc', 'background-color': '#fff', 'padding': '10px', 'overflow-y': 'scroll'})
        right_container.append(self.info_panel)

        # Greenbot-Logo hinzufügen
        self.logo = Label("🌱 Greenbot", width='100%', height='auto', style={'font-size': '20px', 'text-align': 'center', 'margin-top': '10px'})
        right_container.append(self.logo)

        # Tab für Pflanzenliste
        plant_list_container = VBox(width='100%', height='100%', style={'padding': '10px'})
        scroll_container = VBox(width='100%', height='85%', style={'overflow-y': 'auto', 'border': '1px solid #ccc', 'margin-bottom': '10px'})
        self.plant_buttons_container = VBox(width='100%', height='auto', style={'border': '1px solid #ccc'})
        scroll_container.append(self.plant_buttons_container)
        plant_list_container.append(scroll_container)
        tab_box.add_tab(plant_list_container, 'Pflanzen')

        # Tab für Beetgrösse
        beet_size_container = VBox(width='100%', height='100%', style={'padding': '10px'})
        self.beet_width_input = TextInput(single_line=True, hint='Breite in cm', style={'margin': '5px', 'padding': '5px', 'font-size': '12px'})
        self.beet_height_input = TextInput(single_line=True, hint='Höhe in cm', style={'margin': '5px', 'padding': '5px', 'font-size': '12px'})
        self.set_beet_size_button = Button("Beetgrösse setzen", style={
            'margin': '5px', 'padding': '5px', 'font-size': '12px', 'font-weight': 'bold',
            'background-color': '#FF9800', 'color': 'white', 'border': 'none',
            'border-radius': '4px', 'box-shadow': '0 4px 8px 0 rgba(0, 0, 0, 0.2)',
            'transition': '0.3s', 'cursor': 'pointer'
        })
        self.set_beet_size_button.onclick.do(self.set_beet_size)
        beet_size_container.append(Label('Beetgrösse eingeben:', style={'font-size': '12px', 'font-weight': 'bold'}))
        beet_size_container.append(self.beet_width_input)
        beet_size_container.append(self.beet_height_input)
        beet_size_container.append(self.set_beet_size_button)

        # Buttons für Standard-Beetgrössen
        standard_sizes_container = HBox(width='100%', height='auto', style={'margin-bottom': '10px', 'justify-content': 'space-between'})
        self.standard_size_100_button = Button("100x100 cm", style={'margin': '5px', 'padding': '5px', 'font-size': '12px', 'font-weight': 'bold', 'background-color': '#8BC34A', 'color': 'white'})
        self.standard_size_150_button = Button("150x150 cm", style={'margin': '5px', 'padding': '5px', 'font-size': '12px', 'font-weight': 'bold', 'background-color': '#8BC34A', 'color': 'white'})
        self.standard_size_200_button = Button("200x200 cm", style={'margin': '5px', 'padding': '5px', 'font-size': '12px', 'font-weight': 'bold', 'background-color': '#8BC34A', 'color': 'white'})
        self.standard_size_100_button.onclick.do(self.set_standard_size, 100, 100)
        self.standard_size_150_button.onclick.do(self.set_standard_size, 150, 150)
        self.standard_size_200_button.onclick.do(self.set_standard_size, 200, 200)
        standard_sizes_container.append(self.standard_size_100_button)
        standard_sizes_container.append(self.standard_size_150_button)
        standard_sizes_container.append(self.standard_size_200_button)
        beet_size_container.append(standard_sizes_container)
        tab_box.add_tab(beet_size_container, 'Beetgrösse')

        # Tab für Aktionen
        actions_container = VBox(width='100%', height='100%', style={'padding': '10px'})
        self.confirm_button = Button("Saatmuster erstellen", style={
            'margin': '5px', 'padding': '5px', 'font-size': '14px', 'font-weight': 'bold',
            'background-color': '#4CAF50', 'color': 'white', 'border': 'none',
            'border-radius': '4px', 'box-shadow': '0 4px 8px 0 rgba(0, 0, 0, 0.2)',
            'transition': '0.3s', 'cursor': 'pointer'
        })
        print("PlantRobotApp: confirm_button erstellt")
        self.confirm_button.onclick.do(self.controller.generate_pattern)
        actions_container.append(self.confirm_button)

        self.sow_button = Button("Saatmuster bestätigen", style={
            'margin': '5px', 'padding': '5px', 'font-size': '14px', 'font-weight': 'bold',
            'background-color': '#2196F3', 'color': 'white', 'border': 'none',
            'border-radius': '4px', 'box-shadow': '0 4px 8px 0 rgba(0, 0, 0, 0.2)',
            'transition': '0.3s', 'cursor': 'pointer'
        })
        print("PlantRobotApp: sow_button erstellt")
        self.sow_button.onclick.do(self.controller.confirm_sow)
        actions_container.append(self.sow_button)
        tab_box.add_tab(actions_container, 'Aktionen')

        self.load_plants_from_db()

        # Standardwerte für Beetgrösse setzen
        self.beet_width_input.set_value("100")
        self.beet_height_input.set_value("100")
        self.controller.set_beet_size(100, 100)
        self.display_confirmation_message("Standardgrösse gesetzt: Breite = 100 cm, Höhe = 100 cm")

        return self.main_container

    def set_beet_size(self, widget):
        print("PlantRobotApp: set_beet_size aufgerufen")
        try:
            beet_width = int(self.beet_width_input.get_value())
            beet_height = int(self.beet_height_input.get_value())
            self.controller.set_beet_size(beet_width, beet_height)
            print(f"Beetgrösse gesetzt auf: Breite = {beet_width} cm, Höhe = {beet_height} cm")
            self.display_confirmation_message(f"Beetgrösse gesetzt auf: Breite = {beet_width} cm, Höhe = {beet_height} cm")
        except ValueError:
            self.display_confirmation_message("Ungültige Eingabe für die Beetgrösse")

    def set_standard_size(self, widget, width, height):
        self.beet_width_input.set_value(str(width))
        self.beet_height_input.set_value(str(height))
        self.controller.set_beet_size(width, height)
        self.display_confirmation_message(f"Standardgrösse gesetzt: Breite = {width} cm, Höhe = {height} cm")

    def load_plants_from_db(self):
        print("PlantRobotApp: load_plants_from_db aufgerufen")
        plants = db.load_plants_from_db()
        for plant in plants:
            plant_box = HBox(style={'margin': '5px', 'align-items': 'center'})
            checkbox = CheckBox()
            checkbox.set_value(False)
            checkbox.attributes['value'] = plant[0].strip()
            checkbox.onchange.do(self.on_plant_checkbox_change)
            plant_label = Label(plant[0], style={'margin-left': '5px', 'font-size': '14px', 'font-weight': 'bold', 'color': 'black', 'background-color': 'transparent'})
            plant_label.onclick.do(self.on_plant_button_click, plant)
            plant_box.append(checkbox)
            plant_box.append(plant_label)
            self.plant_buttons_container.append(plant_box)

        # Scrollposition auf 0 setzen (JavaScript verwenden)
        self.execute_javascript("""
            var container = document.querySelector('.remi-container');
            container.scrollTop = 0;
            container.scrollLeft = 0;
        """)

    def on_plant_checkbox_change(self, widget, value):
        print(f"PlantRobotApp: on_plant_checkbox_change aufgerufen - Wert: {value}")
        plant_name = widget.attributes['value'].strip()
        checked = widget.get_value()

        plant = next((p for p in db.load_plants_from_db() if p[0] == plant_name), None)
        if plant:
            if checked:
                if plant not in self.selected_plants:
                    self.selected_plants.append(plant)
            else:
                self.selected_plants = [p for p in self.selected_plants if p[0] != plant[0]]

    def display_pattern_grid(self, beet_grid):
        print("PlantRobotApp: display_pattern_grid aufgerufen")
        self.pattern_grid.empty()
        for row in beet_grid:
            table_row = TableRow()
            for cell in row:
                plant_name = cell if cell else ''
                table_item = TableItem(self.unicode_icons.get(plant_name, ''), style={
                    'width': '30px', 'height': '30px', 'text-align': 'center', 'vertical-align': 'middle',
                    'border': '1px solid #ddd'
                })
                if plant_name:
                    table_item.attributes['title'] = plant_name  # Tooltip hinzufügen
                table_item.attributes['onmouseover'] = "this.style.fontSize='{}px'".format(int(30 * 2.5))
                table_item.attributes['onmouseout'] = "this.style.fontSize='{}px'".format(int(30 * 0.8))
                table_item.onclick.do(self.on_cell_click, table_item, cell)
                table_row.append(table_item)
            self.pattern_grid.append(table_row)

    def display_not_planted(self, not_planted):
        print("PlantRobotApp: display_not_planted aufgerufen")
        self.info_panel.empty()
        self.info_panel.append(Label("Nicht gepflanzt:", style={'font-size': '16px', 'font-weight': 'bold', 'color': 'red'}))
        for plant in not_planted:
            self.info_panel.append(Label(plant, style={'font-size': '14px', 'color': 'red'}))

    def display_no_plants_selected(self):
        print("PlantRobotApp: display_no_plants_selected aufgerufen")
        self.info_panel.empty()
        self.info_panel.append(Label("Keine Pflanzen ausgewählt.", style={'font-size': '16px', 'color': 'red'}))

    def display_confirmation_message(self, message):
        print("PlantRobotApp: display_confirmation_message aufgerufen")
        self.info_panel.empty()
        self.info_panel.append(Label(message, style={'font-size': '16px', 'color': 'green'}))

    def generate_sowing_pattern_grid(self, pattern, beet_width, beet_height):
        print("PlantRobotApp: generate_sowing_pattern_grid aufgerufen")
        beet_grid = [['' for _ in range(beet_width)] for _ in range(beet_height)]

        for row in pattern:
            for plant, x_pos, y_pos in row:
                if 0 <= x_pos < beet_width and 0 <= y_pos < beet_height:
                    beet_grid[int(y_pos)][int(x_pos)] = plant

        return beet_grid

    def on_plant_button_click(self, widget, plant):
        print(f"PlantRobotApp: on_plant_button_click aufgerufen - Pflanze: {plant}")
        self.info_panel.empty()
        self.info_panel.append(Label(f"Name: {plant[0]}", style={'font-size': '16px', 'font-weight': 'bold'}))
        self.info_panel.append(Label(f"Pflanzabstand: {plant[1]} cm", style={'font-size': '14px'}))
        self.info_panel.append(Label(f"Reihenabstand: {plant[2]} cm", style={'font-size': '14px'}))

    def on_cell_click(self, widget, item, cell):
        print(f"PlantRobotApp: on_cell_click aufgerufen - Zelle: {cell}")
        widget.style['font-size'] = '{}px'.format(int(widget.style['font-size'].replace('px', '')) * 1.5)

if __name__ == "__main__":
    print("main: Anwendung startet")
    start(PlantRobotApp, address='0.0.0.0', port=8081, start_browser=True)
