import sqlite3
import remi.gui as gui
from remi import start, App

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

        # Komponenten zum Container hinzufügen
        container.append(self.dropdown)
        container.append(self.info_label)

        return container

    def load_plant_names(self):
        conn = sqlite3.connect('db\plants.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM Pflanzen")
        plants = cursor.fetchall()
        for plant in plants:
            self.dropdown.append(gui.DropDownItem(plant[0]))

        conn.close()

    def on_plant_selected(self, widget, selected_value):
        conn = sqlite3.connect('db\plants.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Pflanzen WHERE name=?", (selected_value,))
        plant = cursor.fetchone()
        if plant:
            plant_info = f"Name: {plant[1]}\nPflanzabstand: {plant[2]} cm\nReihenabstand: {plant[3]} cm\nSaattiefe: {plant[4]} cm"
        else:
            plant_info = "Keine Daten gefunden."
        
        self.info_label.set_text(plant_info)
        conn.close()

# Anwendung starten
if __name__ == "__main__":
    start(MyApp, address='0.0.0.0', port=8081, start_browser=True)