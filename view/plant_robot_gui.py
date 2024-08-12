from remi import start, App
from remi.gui import VBox, HBox, Button, Label, Table, TableRow, TableItem, CheckBox, TextInput, TabBox
from controller.plant_robot_controller import PlantRobotController
from model import db


class PlantRobotApp(App):
    """
    Repräsentiert die Hauptanwendung für den Pflanzroboter.

    Diese Klasse erstellt und verwaltet die grafische Benutzeroberfläche für die
    Interaktion mit dem Pflanzroboter. Sie ermöglicht die Auswahl von Pflanzen,
    die Konfiguration der Beetgrösse und die Erstellung eines Saatmusters.
    """

    def __init__(self, *args, **kwargs):
        """
        Initialisiert die PlantRobotApp.

        Parameter:
            *args: Variable Positionsargumente.
            **kwargs: Variable Schlüsselwortargumente.
        """
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
        """
        Erstellt das Hauptlayout der Anwendung.

        Diese Methode initialisiert die Benutzeroberfläche der Anwendung,
        einschliesslich des Hauptcontainers, der Pflanzentabelle, der Aktionsschaltflächen
        und der Informationsanzeigen.
        
        Returns:
            Widget: Das Haupt-Widget, das das Layout der Anwendung enthält.
        """
        if not hasattr(self, 'controller'):
            self.controller = PlantRobotController(self)
            print("PlantRobotApp: Controller initialisiert in main")

        print("PlantRobotApp: main aufgerufen")
        self.main_container = HBox(
            width='100%', height='100%', style={'background-color': '#f8f8f8'}
        )

        left_container = VBox(
            width='75%', height='100%', 
            style={'border': '1px solid #ccc', 'background-color': '#fff'}
        )
        self.main_container.append(left_container)

        # Feste Grid-Grösse festlegen
        self.pattern_grid = Table(
            width='100%', height='100%', 
            style={
                'border': '1px solid #ccc',
                'background-color': '#fff',
                'table-layout': 'fixed',  # Verhindert das Verändern der Grid-Grösse
                'width': '800px',  # Feste Grösse des Grids in Pixeln
                'height': '800px',
                'overflow': 'hidden'  # Verhindert das Scrollen
            }
        )
        left_container.append(self.pattern_grid)

        right_container = VBox(
            width='25%', height='100%', 
            style={
                'border': '1px solid #ccc', 
                'background-color': '#fff', 
                'padding': '10px'
            }
        )
        self.main_container.append(right_container)

        tab_box = TabBox(
            width='100%', height='70%', style={'background-color': '#fff'}
        )
        right_container.append(tab_box)

        # Informations-Panel hinzufügen
        self.info_panel = VBox(
            width='100%', height='20%', 
            style={
                'border-top': '1px solid #ccc', 
                'background-color': '#fff', 
                'padding': '10px', 
                'overflow-y': 'scroll'
            }
        )
        right_container.append(self.info_panel)

        # Greenbot-Logo hinzufügen
        self.logo = Label(
            "🌱 Greenbot", width='100%', height='auto', 
            style={
                'font-size': '20px', 
                'text-align': 'center', 
                'margin-top': '10px'
            }
        )
        right_container.append(self.logo)

        # Tab für Pflanzenliste
        plant_list_container = VBox(
            width='100%', height='100%', style={'padding': '10px'}
        )
        scroll_container = VBox(
            width='100%', height='85%', 
            style={
                'overflow-y': 'auto', 
                'border': '1px solid #ccc', 
                'margin-bottom': '10px'
            }
        )
        self.plant_buttons_container = VBox(
            width='100%', height='auto', style={'border': '1px solid #ccc'}
        )
        scroll_container.append(self.plant_buttons_container)
        plant_list_container.append(scroll_container)
        tab_box.add_tab(plant_list_container, 'Pflanzen')

        # Tab für Beetgrösse
        beet_size_container = VBox(
            width='100%', height='100%', style={'padding': '10px'}
        )
        self.beet_width_input = TextInput(
            single_line=True, 
            hint='Breite in cm', 
            style={
                'margin': '5px', 
                'padding': '5px', 
                'font-size': '12px'
            }
        )
        self.beet_height_input = TextInput(
            single_line=True, 
            hint='Höhe in cm', 
            style={
                'margin': '5px', 
                'padding': '5px', 
                'font-size': '12px'
            }
        )
        self.set_beet_size_button = Button(
            "Beetgrösse setzen", 
            style={
                'margin': '5px', 
                'padding': '5px', 
                'font-size': '12px', 
                'font-weight': 'bold',
                'background-color': '#FF9800', 
                'color': 'white', 
                'border': 'none',
                'border-radius': '4px', 
                'box-shadow': '0 4px 8px 0 rgba(0, 0, 0, 0.2)',
                'transition': '0.3s', 
                'cursor': 'pointer'
            }
        )
        self.set_beet_size_button.onclick.do(self.set_beet_size)
        beet_size_container.append(Label(
            'Beetgrösse eingeben:', 
            style={'font-size': '12px', 'font-weight': 'bold'}
        ))
        beet_size_container.append(self.beet_width_input)
        beet_size_container.append(self.beet_height_input)
        beet_size_container.append(self.set_beet_size_button)

        # Buttons für Standard-Beetgrössen
        standard_sizes_container = HBox(
            width='100%', height='auto', 
            style={
                'margin-bottom': '10px', 
                'justify-content': 'space-between'
            }
        )
        self.standard_size_100_button = Button(
            "100x100 cm", 
            style={
                'margin': '5px', 
                'padding': '5px', 
                'font-size': '12px', 
                'font-weight': 'bold', 
                'background-color': '#8BC34A', 
                'color': 'white'
            }
        )
        self.standard_size_150_button = Button(
            "150x150 cm", 
            style={
                'margin': '5px', 
                'padding': '5px', 
                'font-size': '12px', 
                'font-weight': 'bold', 
                'background-color': '#8BC34A', 
                'color': 'white'
            }
        )
        self.standard_size_200_button = Button(
            "200x200 cm", 
            style={
                'margin': '5px', 
                'padding': '5px', 
                'font-size': '12px', 
                'font-weight': 'bold', 
                'background-color': '#8BC34A', 
                'color': 'white'
            }
        )
        self.standard_size_100_button.onclick.do(self.set_standard_size, 100, 100)
        self.standard_size_150_button.onclick.do(self.set_standard_size, 150, 150)
        self.standard_size_200_button.onclick.do(self.set_standard_size, 200, 200)
        standard_sizes_container.append(self.standard_size_100_button)
        standard_sizes_container.append(self.standard_size_150_button)
        standard_sizes_container.append(self.standard_size_200_button)
        beet_size_container.append(standard_sizes_container)
        tab_box.add_tab(beet_size_container, 'Beetgrösse')

        # Tab für Aktionen
        actions_container = VBox(
            width='100%', height='100%', style={'padding': '10px'}
        )
        self.confirm_button = Button(
            "Saatmuster erstellen", 
            style={
                'margin': '5px', 
                'padding': '5px', 
                'font-size': '14px', 
                'font-weight': 'bold',
                'background-color': '#4CAF50', 
                'color': 'white', 
                'border': 'none',
                'border-radius': '4px', 
                'box-shadow': '0 4px 8px 0 rgba(0, 0, 0, 0.2)',
                'transition': '0.3s', 
                'cursor': 'pointer'
            }
        )
        print("PlantRobotApp: confirm_button erstellt")
        self.confirm_button.onclick.do(self.controller.generate_pattern)
        actions_container.append(self.confirm_button)

        self.sow_button = Button(
            "Saatmuster bestätigen", 
            style={
                'margin': '5px', 
                'padding': '5px', 
                'font-size': '14px', 
                'font-weight': 'bold',
                'background-color': '#2196F3', 
                'color': 'white', 
                'border': 'none',
                'border-radius': '4px', 
                'box-shadow': '0 4px 8px 0 rgba(0, 0, 0, 0.2)',
                'transition': '0.3s', 
                'cursor': 'pointer'
            }
        )
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
        """
        Setzt die Beetgrösse basierend auf Benutzereingaben.

        Diese Methode wird aufgerufen, wenn der Benutzer die Beetgrösse festlegen möchte.
        Sie aktualisiert die Beetgrösse und zeigt eine Bestätigungsmeldung an.

        Parameter:
            widget (Widget): Das Widget, das das Event ausgelöst hat.
        """
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
        """
        Setzt eine Standard-Beetgrösse.

        Diese Methode wird aufgerufen, wenn der Benutzer eine der vordefinierten
        Beetgrössen auswählt.

        Parameter:
            widget (Widget): Das Widget, das das Event ausgelöst hat.
            width (int): Die Breite des Beets in cm.
            height (int): Die Höhe des Beets in cm.
        """
        self.beet_width_input.set_value(str(width))
        self.beet_height_input.set_value(str(height))
        self.controller.set_beet_size(width, height)
        self.display_confirmation_message(f"Standardgrösse gesetzt: Breite = {width} cm, Höhe = {height} cm")

    def load_plants_from_db(self):
        """
        Lädt die Pflanzen aus der Datenbank und erstellt die Checkboxen in der GUI.

        Diese Methode ruft die Pflanzeninformationen aus der Datenbank ab und erstellt
        dynamisch die entsprechenden GUI-Elemente (Checkboxen) für die Auswahl der Pflanzen.
        """
        print("PlantRobotApp: load_plants_from_db aufgerufen")
        plants = db.load_plants_from_db()
        for plant in plants:
            plant_box = HBox(style={'margin': '5px', 'align-items': 'center'})
            checkbox = CheckBox()
            checkbox.set_value(False)
            checkbox.attributes['value'] = plant[0].strip()
            checkbox.onchange.do(self.on_plant_checkbox_change)
            plant_label = Label(
                plant[0], 
                style={
                    'margin-left': '5px', 
                    'font-size': '14px', 
                    'font-weight': 'bold', 
                    'color': 'black', 
                    'background-color': 'transparent'
                }
            )
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
        """
        Aktualisiert die Liste der ausgewählten Pflanzen.

        Diese Methode wird aufgerufen, wenn der Benutzer eine Checkbox
        zum Auswählen oder Abwählen einer Pflanze aktiviert.

        Parameter:
            widget (Widget): Das Widget, das die Checkbox darstellt.
            value (bool): Der neue Status der Checkbox (ausgewählt oder nicht).
        """
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
        """
        Zeigt das generierte Pflanzmuster im Grid an.

        Diese Methode aktualisiert die GUI mit dem generierten Pflanzmuster
        und platziert die Pflanzen im Grid basierend auf der Eingabe.

        Parameter:
            beet_grid (list): Eine Liste von Listen, die das Pflanzmuster darstellt.
        """
        print("PlantRobotApp: display_pattern_grid aufgerufen")
        self.pattern_grid.empty()
        for row in beet_grid:
            table_row = TableRow()
            for cell in row:
                plant_name = cell if cell else ''
                table_item = TableItem(
                    self.unicode_icons.get(plant_name, ''), 
                    style={
                        'width': '30px', 
                        'height': '30px', 
                        'text-align': 'center', 
                        'vertical-align': 'middle',
                        'border': '1px solid #ddd',
                        'position': 'relative'
                    }
                )
                if plant_name:
                    plant_label = Label(
                        plant_name, 
                        style={
                            'font-size': '12px',
                            'color': 'black',
                            'background-color': 'rgba(255, 255, 255, 0.8)',  # Halbtransparent
                            'position': 'absolute',
                            'top': '0', 'left': '0', 'right': '0', 'bottom': '0',
                            'display': 'none',  # Unsichtbar bis Hover
                            'z-index': '10',
                            'text-align': 'center',
                            'line-height': '30px',
                            'transition': 'opacity 0.3s, transform 0.3s',  # Animation beim Ein- und Ausblenden
                            'opacity': '0',  # Startwert: Unsichtbar
                            'transform': 'scale(0.9)'  # Startwert: Kleiner
                        }
                    )

                    # Mouseover-Effekt: Zeige Label mit Animation
                    table_item.attributes['onmouseover'] = """
                        this.children[0].style.display = 'block';
                        this.children[0].style.opacity = '1';
                        this.children[0].style.transform = 'scale(1)';
                    """

                    # Mouseout-Effekt: Verstecke Label mit Animation
                    table_item.attributes['onmouseout'] = """
                        this.children[0].style.opacity = '0';
                        this.children[0].style.transform = 'scale(0.9)';
                        setTimeout(() => this.children[0].style.display = 'none', 300);
                    """
                    table_item.append(plant_label)
                table_row.append(table_item)
            self.pattern_grid.append(table_row)

    def display_not_planted(self, not_planted):
        """
        Zeigt Pflanzen an, die nicht gepflanzt werden konnten.

        Diese Methode listet die Pflanzen auf, die im aktuellen Pflanzmuster
        keinen Platz gefunden haben und daher nicht angezeigt werden können.

        Parameter:
            not_planted (list): Eine Liste von Pflanzennamen, die nicht gepflanzt wurden.
        """
        print("PlantRobotApp: display_not_planted aufgerufen")
        self.info_panel.empty()
        self.info_panel.append(Label(
            "Nicht gepflanzt:", 
            style={'font-size': '16px', 'font-weight': 'bold', 'color': 'red'}
        ))
        for plant in not_planted:
            self.info_panel.append(Label(
                plant, style={'font-size': '14px', 'color': 'red'}
            ))

    def display_no_plants_selected(self):
        """
        Zeigt eine Nachricht an, wenn keine Pflanzen ausgewählt wurden.

        Diese Methode wird verwendet, um den Benutzer darüber zu informieren,
        dass keine Pflanzen für das Pflanzmuster ausgewählt wurden.
        """
        print("PlantRobotApp: display_no_plants_selected aufgerufen")
        self.info_panel.empty()
        self.info_panel.append(Label(
            "Keine Pflanzen ausgewählt.", 
            style={'font-size': '16px', 'color': 'red'}
        ))

    def display_confirmation_message(self, message):
        """
        Zeigt eine Bestätigungsmeldung an.

        Diese Methode wird verwendet, um eine Nachricht in der GUI anzuzeigen,
        die dem Benutzer bestätigt, dass eine Aktion erfolgreich abgeschlossen wurde.

        Parameter:
            message (str): Die anzuzeigende Bestätigungsnachricht.
        """
        print("PlantRobotApp: display_confirmation_message aufgerufen")
        self.info_panel.empty()
        self.info_panel.append(Label(
            message, style={'font-size': '16px', 'color': 'green'}
        ))

    def generate_sowing_pattern_grid(self, pattern, beet_width, beet_height):
        """
        Generiert das Pflanzmuster für das Beet basierend auf den Eingaben.

        Diese Methode erstellt ein Raster, das die Pflanzenpositionen
        im Beet basierend auf der angegebenen Beetgrösse und dem ausgewählten Muster darstellt.

        Parameter:
            pattern (list): Eine Liste von Pflanzen und deren Positionen.
            beet_width (int): Die Breite des Beets in Zellen.
            beet_height (int): Die Höhe des Beets in Zellen.

        Returns:
            list: Ein zweidimensionales Array, das das Pflanzmuster darstellt.
        """
        print("PlantRobotApp: generate_sowing_pattern_grid aufgerufen")
        grid_width = 25  # Feste Grösse in Zellen
        grid_height = 25

        # Skalierungsfaktoren berechnen
        scale_x = grid_width / beet_width
        scale_y = grid_height / beet_height

        beet_grid = [['' for _ in range(grid_width)] for _ in range(grid_height)]

        for row in pattern:
            for plant, x_pos, y_pos in row:
                scaled_x = min(int(x_pos * scale_x), grid_width - 1)
                scaled_y = min(int(y_pos * scale_y), grid_height - 1)
                
                if 0 <= scaled_x < grid_width and 0 <= scaled_y < grid_height:
                    beet_grid[scaled_y][scaled_x] = plant

        return beet_grid

    def on_plant_button_click(self, widget, plant):
        """
        Zeigt detaillierte Informationen über die ausgewählte Pflanze an.

        Diese Methode wird aufgerufen, wenn der Benutzer auf eine Pflanze klickt,
        und zeigt dann die spezifischen Details der Pflanze an.

        Parameter:
            widget (Widget): Das Widget, das das Event ausgelöst hat.
            plant (tuple): Die Informationen über die Pflanze.
        """
        print(f"PlantRobotApp: on_plant_button_click aufgerufen - Pflanze: {plant}")
        self.info_panel.empty()
        self.info_panel.append(Label(
            f"Name: {plant[0]}", style={'font-size': '16px', 'font-weight': 'bold'}
        ))
        self.info_panel.append(Label(
            f"Pflanzabstand: {plant[1]} cm", style={'font-size': '14px'}
        ))
        self.info_panel.append(Label(
            f"Reihenabstand: {plant[2]} cm", style={'font-size': '14px'}
        ))

    def on_cell_click(self, widget, item, cell):
        """
        Vergrössert die Zelle, wenn auf sie geklickt wird.

        Diese Methode wird aufgerufen, wenn der Benutzer auf eine Zelle im Pflanzmuster
        klickt, und vergrössert die Zelle temporär, um eine bessere Sichtbarkeit zu ermöglichen.

        Parameter:
            widget (Widget): Das Widget, das das Event ausgelöst hat.
            item (TableItem): Das Zellen-Element, das geklickt wurde.
            cell (str): Der Inhalt der Zelle (Name der Pflanze oder leer).
        """
        print(f"PlantRobotApp: on_cell_click aufgerufen - Zelle: {cell}")
        widget.style['font-size'] = '{}px'.format(int(widget.style['font-size'].replace('px', '')) * 1.5)


if __name__ == "__main__":
    print("main: Anwendung startet")
    start(PlantRobotApp, address='0.0.0.0', port=8081, start_browser=True)
