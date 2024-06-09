import sqlite3
import remi.gui as gui
from remi import start, App
from seed_pattern_generator import calculate_seed_pattern

class MyApp(App):
    def __init__(self, *args):
        super(MyApp, self).__init__(*args)

    def main(self):
        # Hauptcontainer erstellen
        container = gui.VBox(width=500, height=500)

        # Dropdown-Menü zur Auswahl der Pflanze
        self.dropdown = gui.DropDown(width=200, height=30)
        self.load_plant_names()
        self.dropdown.onchange.connect(self.on_plant_selected)

        # Label zur Anzeige der Pflanzdaten
        self.info_label = gui.Label("Pflanzdaten werden hier angezeigt", width=400, height=200)

        # Felder zur Eingabe der Bettabmessungen
        self.bed_width_input = gui.TextInput(width=100, height=30, hint='Breite')
        self.bed_height_input = gui.TextInput(width=100, height=30, hint='Höhe')

        # Button zur Musterberechnung
        self.calculate_button = gui.Button("Muster berechnen", width=200, height=30)
        self.calculate_button.onclick.connect(self.calculate_seed_pattern_and_display)

        # Widget zur Anzeige des Musters
        self.seed_pattern_display = gui.Label('', width=400, height=200)

        # Komponenten zum Container hinzufügen
        container.append(self.dropdown)
        container.append(self.info_label)
        container.append(self.bed_width_input)
        container.append(self.bed_height_input)
        container.append(self.calculate_button)
        container.append(self.seed_pattern_display)

        return container

    def load_plant_names(self):
        conn = sqlite3.connect('db/plants.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM Pflanzen")
        plants = cursor.fetchall()
        for plant in plants:
            self.dropdown.append(gui.DropDownItem(plant[0]))
        conn.close()

    def on_plant_selected(self, widget, selected_value):
        conn = sqlite3.connect('db/plants.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Pflanzen WHERE name=?", (selected_value,))
        plant = cursor.fetchone()
        if plant:
            plant_info = f"Name: {plant[1]}\nPflanzabstand: {plant[2]} cm\nReihenabstand: {plant[3]} cm\nSaattiefe: {plant[4]} cm"
        else:
            plant_info = "Keine Daten gefunden."
        self.info_label.set_text(plant_info)
        conn.close()

    def calculate_seed_pattern_and_display(self, widget):
        # Bettabmessungen abrufen
        bed_width = int(self.bed_width_input.get_text())
        bed_height = int(self.bed_height_input.get_text())

        # Ausgewählte Pflanzendaten abrufen
        selected_plant = self.dropdown.get_value()
        conn = sqlite3.connect('db/plants.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Pflanzen WHERE name=?", (selected_plant,))
        plant_data = cursor.fetchall()
        conn.close()

        # Muster berechnen
        seed_pattern = calculate_seed_pattern(bed_width, bed_height, plant_data)

        # Muster anzeigen
        self.display_seed_pattern(seed_pattern)
def calculate_seed_pattern_and_display(self, widget):
        # Bettabmessungen abrufen
        bed_width = int(self.bed_width_input.get_text())
        bed_height = int(self.bed_height_input.get_text())

        # Ausgewählte Pflanzendaten abrufen
        selected_plant = self.dropdown.get_value()
        conn = sqlite3.connect('db/plants.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Pflanzen WHERE name=?", (selected_plant,))
        plant_data = cursor.fetchall()
        conn.close()

        # Muster berechnen
        seed_pattern = calculate_seed_pattern(bed_width, bed_height, plant_data)

        # Muster im Terminal anzeigen
        display_seed_pattern(seed_pattern)

        # Muster im Webbrowser anzeigen
        self.display_seed_pattern(seed_pattern)

# Anwendung starten
if __name__ == "__main__":
    start(MyApp, address='0.0.0.0', port=8081, start_browser=True)

# Anwendung starten
if __name__ == "__main__":
    start(MyApp, address='0.0.0.0', port=8081, start_browser=True)
