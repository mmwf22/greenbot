from view.plant_robot_gui import PlantRobotApp
from remi import start

if __name__ == "__main__":
    print("main: Anwendung startet")
    start(PlantRobotApp, address='0.0.0.0', port=8081, start_browser=True)
