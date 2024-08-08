from model import db, seed_pattern_generator

class PlantRobotController:
    def __init__(self, view):
        print("PlantRobotController: __init__ aufgerufen")
        self.view = view

    def generate_pattern(self, widget):
        print("PlantRobotController: generate_pattern aufgerufen")
        plants = self.view.selected_plants
        if not plants:
            self.view.display_no_plants_selected()
            return

        try:
            beet_width = int(self.view.beet_width_input.get_value())
            beet_height = int(self.view.beet_height_input.get_value())
        except ValueError:
            self.view.display_confirmation_message("Ungültige Eingabe für die Beetgrösse")
            return

        pattern, not_planted = seed_pattern_generator.calculate_sowing_pattern(plants, beet_width, beet_height)
        beet_grid = self.view.generate_sowing_pattern_grid(pattern, beet_width, beet_height)
        self.view.display_pattern_grid(beet_grid)

        if not_planted:
            self.view.display_not_planted(not_planted)

        # Speichern Sie das Muster für die spätere Übergabe
        self.view.current_pattern = pattern

    def confirm_sow(self, widget):
        print("PlantRobotController: confirm_sow aufgerufen")
        if hasattr(self.view, 'current_pattern'):
            pattern = self.view.current_pattern
            # Logik zur Bestätigung und Weitergabe des Musters an die Motoren
            print(f"Das Saatmuster wird an die Motoren übergeben: {pattern}")
            self.view.display_confirmation_message("Saatmuster erfolgreich übergeben.")
        else:
            self.view.display_confirmation_message("Kein Saatmuster zum Übergeben vorhanden.")

    def set_beet_size(self, width, height):
        print("PlantRobotController: set_beet_size aufgerufen")
        self.beet_width = width
        self.beet_height = height
        print(f"Beetgrösse aktualisiert: Breite = {self.beet_width} cm, Höhe = {self.beet_height} cm")
