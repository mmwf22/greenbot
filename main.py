from view.plant_robot_gui import PlantRobotApp
from remi import start

if __name__ == "__main__":
    """
    Startet die Hauptanwendung des Pflanzroboters.

    Diese Funktion startet den Remi-Webserver und initialisiert die
    PlantRobotApp, die auf die angegebene Adresse und den Port hört.
    """
    print("main: Anwendung startet")
    start(PlantRobotApp, address='0.0.0.0', port=8081, start_browser=True)
