import json
import csv
import time
import os
import datetime

def read_and_write_data(json_file, csv_file):
    try:
        full_json_path = os.path.join(os.getcwd(), json_file)

        with open(full_json_path, 'r') as f:
            data = json.load(f)

        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

        with open(csv_file, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([timestamp, data['total_batches'], data['total_positions'], data['total_nodes']])

        # Ausgabe der Werte in der Konsole
        print(f"Daten geschrieben: {timestamp}, {data['total_batches']}, {data['total_positions']}, {data['total_nodes']}")


    except FileNotFoundError:
        print(f"Datei '{json_file}' nicht gefunden.")
    except json.JSONDecodeError:
        print("Fehler beim Parsen der JSON-Datei.")
    except Exception as e:
        print(f"Ein unerwarteter Fehler ist aufgetreten: {e}")


def create_csv_if_not_exists(csv_file):
    if not os.path.exists(csv_file):
        try:
            with open(csv_file, 'w', newline='') as csvfile:
                pass  # Keine Header-Zeile schreiben
            print(f"CSV-Datei '{csv_file}' wurde erstellt.")
        except Exception as e:
            print(f"Fehler beim Erstellen der CSV-Datei: {e}")


if __name__ == "__main__":
    json_file = r'C:\Users\bou\.fishnet-stats'  # Pfad anpassen!
    csv_file = 'FishnetCSV1.csv'

    create_csv_if_not_exists(csv_file)

    while True:
        now = datetime.datetime.now()
        next_hour = now + datetime.timedelta(hours=1)
        next_hour = next_hour.replace(minute=0, second=0, microsecond=0)
        wait_seconds = (next_hour - now).total_seconds()

        next_execution_time = next_hour  # Store for printing

        print(f"Nächste Ausführung: {next_execution_time.strftime('%Y-%m-%d %H:%M:%S')}")

        time.sleep(wait_seconds)

        read_and_write_data(json_file, csv_file)  # Write data at the top of the hour

        time.sleep(1) # Small delay to avoid potential issues.