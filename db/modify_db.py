import sqlite3
import os

# Pfad zur Datenbankdatei
base_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(base_dir, 'plants.db')


def connect_db(db_path):
    """
    Stellt eine Verbindung zur SQLite-Datenbank her.

    Diese Funktion versucht, eine Verbindung zur angegebenen SQLite-Datenbank
    herzustellen. Bei Erfolg wird die Verbindung zurückgegeben, andernfalls
    wird None zurückgegeben.

    Parameter:
        db_path (str): Der Pfad zur SQLite-Datenbank.

    Returns:
        sqlite3.Connection: Das Verbindungsobjekt, falls die Verbindung
        erfolgreich hergestellt wurde, andernfalls None.
    """
    try:
        conn = sqlite3.connect(db_path)
        print(f"Verbunden mit der Datenbank: {db_path}")
        return conn
    except sqlite3.Error as e:
        print(f"Fehler beim Verbinden mit der Datenbank: {e}")
        return None


def print_plants(conn):
    """
    Gibt die Pflanzeninformationen aus der Datenbank in der Konsole aus.

    Diese Funktion ruft alle Pflanzendaten aus der Datenbank ab und druckt
    sie in der Konsole aus.

    Parameter:
        conn (sqlite3.Connection): Das Verbindungsobjekt zur Datenbank.
    """
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Pflanzen")
        plants = cursor.fetchall()
        print("Pflanzen in der Datenbank:")
        for plant in plants:
            print(
                f"ID: {plant[0]}, Name: {plant[1]}, Pflanzabstand: {plant[2]}, "
                f"Reihenabstand: {plant[3]}, Saattiefe: {plant[4]}"
            )
    except sqlite3.Error as e:
        print(f"Fehler beim Abrufen der Pflanzen: {e}")


def remove_duplicate_plants(conn):
    """
    Entfernt doppelte Pflanzeneinträge aus der Datenbank.

    Diese Funktion sucht nach doppelten Pflanzeneinträgen auf Basis des Namens
    und entfernt diese, wobei nur ein Eintrag pro Pflanze erhalten bleibt.

    Parameter:
        conn (sqlite3.Connection): Das Verbindungsobjekt zur Datenbank.
    """
    try:
        cursor = conn.cursor()

        # Finden und Entfernen von doppelten Pflanzen auf Basis des Namens
        cursor.execute(
            """
            DELETE FROM Pflanzen
            WHERE rowid NOT IN (
                SELECT MIN(rowid)
                FROM Pflanzen
                GROUP BY name
            )
            """
        )

        conn.commit()
        print("Doppelte Einträge wurden entfernt.")
    except sqlite3.Error as e:
        print(f"Fehler beim Entfernen von doppelten Einträgen: {e}")


def main():
    """
    Hauptfunktion zum Verbinden mit der Datenbank, Ausdrucken der Pflanzenliste
    und Entfernen von Duplikaten.

    Diese Funktion stellt eine Verbindung zur Datenbank her, druckt die Liste
    der Pflanzen aus, entfernt doppelte Einträge und druckt die aktualisierte
    Pflanzenliste erneut aus.
    """
    conn = connect_db(db_path)
    
    if conn:
        print("Vor dem Entfernen der Duplikate:")
        print_plants(conn)
        remove_duplicate_plants(conn)
        print("\nNach dem Entfernen der Duplikate:")
        print_plants(conn)
        conn.close()


if __name__ == '__main__':
    main()
