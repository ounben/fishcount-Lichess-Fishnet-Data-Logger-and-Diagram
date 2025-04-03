import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import os
import tkinter as tk
from tkcalendar import Calendar  # Für die Datumsauswahl
from datetime import datetime, timedelta
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.dates as mdates

# Globale Variablen (sofern möglich vermeiden, aber hier für die Tkinter-Integration notwendig)
fig = None
ax1 = None
ax2 = None
line1 = None
line2 = None
canvas = None
df = None
filename = 'FishnetCSV1.csv'  # Dateiname global definieren
click_count = 0
#plt.axvline(x=some_x_value, color='gray', linestyle='--', linewidth=0.5)

def plot_differences(filename, batch_column, node_column): # num_rows entfernt
    global df # df als global deklarieren, da wir es in update_plot brauchen
    try:
        file_size = os.path.getsize(filename)
        if file_size == 0:
            print(f"Error: File '{filename}' is empty.")
            return None, None, None, None, None # df hinzugefügt

        df = pd.read_csv(filename, header=None, names=['Zeitstempel', 'Batch', 'Position', 'Nodes'],
                         parse_dates=['Zeitstempel'], date_format='%Y-%m-%d %H:%M:%S')

        df['Zeitstempel'] = pd.to_datetime(df['Zeitstempel'], errors='coerce')
        df = df.dropna(subset=['Zeitstempel'])

        # Nur Daten des letzten Tages filtern
        # last_day = df['Zeitstempel'].max().date()
        # df = df[df['Zeitstempel'].dt.date == last_day]

        df['Diff_' + batch_column] = df[batch_column].diff()
        df['Diff_' + node_column] = df[node_column].diff() / 1000000000

        fig, ax1 = plt.subplots(figsize=(10, 6))
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H'))

        zero_timestamps = df['Zeitstempel'][df['Zeitstempel'].dt.hour == 0]
        for timestamp in zero_timestamps:
            ax1.axvline(x=timestamp, color='gray', linestyle='--', linewidth=0.5)

        ax1.set_xlabel('Zeitstempel', fontsize=14)
        ax1.set_ylabel(f'Differenz {batch_column}', fontsize=14)
        ax2 = ax1.twinx()

        line1, = ax1.plot(df['Zeitstempel'], df['Diff_' + batch_column], label=f'Differenz {batch_column}')
        line2, = ax2.plot(df['Zeitstempel'], df['Diff_' + node_column], color='green', label=f'Differenz {node_column} (Mrd)')

        ax2.set_ylabel(f'Differenz {node_column} (Mrd)', color='green')
        ax2.axhline(y=df['Diff_' + node_column].mean(), color='green', linestyle='--', label='Mittelwert Node-Differenz')

        last_batch = df[batch_column].iloc[-1]
        #last_batch_diff = df_filtered['batch_column'].iloc[-1]

        current_time = datetime.now().strftime("%H:%M:%S")

        ax1.set_title(f'{batch_column}- und {node_column} pro Stunde (Letzter {batch_column}: {last_batch}) {current_time}')
        #ax1.set_title(f'Batch (Total: {last_batch}, /nAnzahl Batches: {anzahl_batches}, /nMin: {min_batch_diff:.2f}, /nMax: {max_batch_diff:.2f}) /n{current_time}')

        plt.grid(True)
        plt.xticks(rotation=45)

        lines1, labels1 = ax1.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax2.legend(lines1 + lines2, labels1 + labels2, loc="upper left")

        fig.canvas.draw()
        fig.canvas.flush_events()
        #plt.show()

        # direkt update_plot aufrufen, nachdem der Plot erstellt wurde
        if 'cal_von' in globals() and 'cal_bis' in globals(): # überprüfen ob cal_von und cal_bis definiert ist.
            update_plot(batch_column, node_column, cal_von, cal_bis) # Übergabe der Kalenderobjekte
        else:
            print("cal_von oder cal_bis nicht definiert.")

        return fig, ax1, ax2, line1, line2, df

    except (FileNotFoundError, pd.errors.EmptyDataError, pd.errors.ParserError) as e:
        print(f"Error: {e}")
        return None, None, None, None, None, None # df wird auch im Fehlerfall zurückgegeben
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None, None, None, None, None, None # df wird auch im Fehlerfall zurückgegeben

def update_plot(batch_column, node_column, cal_von, cal_bis):
    global fig, canvas, df, ax1, ax2, line1, line2
    try:
        start_date_str = cal_von.get_date()
        end_date_str = cal_bis.get_date()

        print(f"Start date string: {start_date_str}")
        print(f"End date string: {end_date_str}")

        # Konvertiere die Strings in datetime Objekte
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

        # Konvertiere die Datumswerte im DataFrame in Datumsangaben ohne Uhrzeit
        df['Zeitstempel_Datum'] = df['Zeitstempel'].dt.date

        print(f"Erste 5 Einträge in 'Zeitstempel_Datum':\n{df['Zeitstempel_Datum'].head()}")

        mask = (df['Zeitstempel_Datum'] >= start_date) & (df['Zeitstempel_Datum'] <= end_date)
        df_filtered = df[mask]

        print(f"Erste 5 Einträge im DataFrame:\n{df.head()}")
        print(f"Spalten im DataFrame: {df.columns}")
        print(f"Anzahl der Zeilen vor dem Filtern: {len(df)}")
        print(f"Anzahl der Zeilen nach dem Filtern: {len(df_filtered)}")
        print(f"Gefilterte Daten:\n{df_filtered.head()}")

        print(f"Startdatum (Typ: {type(start_date)}): {start_date}")
        print(f"Enddatum (Typ: {type(end_date)}): {end_date}")
        print(f"Erste 5 Zeitstempel im DataFrame:\n{df['Zeitstempel'].head()}")
        print(f"Anzahl der gefilterten Zeilen: {len(df_filtered)}")

        # Debugging-Ausgaben für die Plot-Objekte
        print(f"line1: {line1}")
        print(f"line2: {line2}")
        print(f"ax1: {ax1}")
        print(f"ax2: {ax2}")

        # Überprüfe, ob ALLE notwendigen Objekte NICHT None sind UND df_filtered nicht leer ist
        if (line1 is not None and line2 is not None and ax1 is not None and ax2 is not None and not df_filtered.empty):
            # Debugging-Ausgaben für die Datenübergabe
            print(f"Zeitstempel für line1: {df_filtered['Zeitstempel']}")
            print(f"Diff_Batch für line1: {df_filtered['Diff_Batch']}")
            print(f"Zeitstempel für line2: {df_filtered['Zeitstempel']}")
            print(f"Diff_Nodes für line2: {df_filtered['Diff_Nodes']}")

            line1.set_data(df_filtered['Zeitstempel'], df_filtered['Diff_Batch'])
            line2.set_data(df_filtered['Zeitstempel'], df_filtered['Diff_Nodes'])

            min_zeitstempel = df_filtered['Zeitstempel'].min()
            max_zeitstempel = df_filtered['Zeitstempel'].max()
            ax1.set_xlim(min_zeitstempel, max_zeitstempel)
            ax2.set_xlim(min_zeitstempel, max_zeitstempel)

            ax1.relim()
            ax1.autoscale_view()
            ax2.relim()
            ax2.autoscale_view()
            
            # Berechnungen
            
            gesamt_summe = df_filtered['Diff_Batch'].sum()

            mean_batch_diff = df_filtered['Diff_Batch'].mean()

            min_batch_diff = df_filtered['Diff_Batch'].min()
            #min_batch_diff_timestamps = df.loc[df['Differenz_' + batch] == min_batch_diff, 'Zeitstempel'].tolist()  # Alle Zeitstempel für den minimalen Wert
            min_batch_diff_timestamps = df_filtered.loc[df_filtered['Diff_' + batch_column] == min_batch_diff, 'Zeitstempel'].tolist()

            max_batch_diff = df_filtered['Diff_Batch'].max()
            #max_batch_diff_timestamps = df.loc[df['Differenz_' + batch] == max_batch_diff, 'Zeitstempel'].tolist()  # Alle Zeitstempel für den maximalen Wert
            max_batch_diff_timestamps = df_filtered.loc[df_filtered['Diff_' + batch_column] == max_batch_diff, 'Zeitstempel'].tolist()

            last_batch = df_filtered['Batch'].iloc[-1]

            last_batch_diff = df_filtered['Diff_Batch'].iloc[-1]

            current_time = datetime.now().strftime("%H:%M:%S")
            #anzahl_batches = df_filtered['Batch'].nunique()  # .nunique() zählt eindeutige Werte
            anzahl_batches = len(df_filtered['Batch'])  # Menge der Batches berechnen

            # Zeitstempel für Min und Max der Batch-Differenz finden
            min_timestamp = df_filtered.loc[df_filtered['Diff_' + batch_column] == min_batch_diff, 'Zeitstempel'].iloc[0].strftime("%d.%m.%Y %H:%M") # Nur der erste Zeitstempel
            max_timestamp = df_filtered.loc[df_filtered['Diff_' + batch_column] == max_batch_diff, 'Zeitstempel'].iloc[0].strftime("%d.%m.%Y %H:%M") # Nur der erste Zeitstempel


            # ax1.set_title(f'Batch (Total: {last_batch}, /nDurchschnitt: {mean_batch_diff}, /nMin: {min_batch_diff:.2f}, /nMax: {max_batch_diff:.2f}) /n{current_time}')

            # ERSETZE den gesamten Titelstring jedes Mal neu:
            ax1.set_title('')  # Alten Titel explizit löschen
            ax1.set_title(f'Batch Total: {last_batch}, \nGesamtmenge: {gesamt_summe}, \nDurchschnitt: {mean_batch_diff}, \nMin: {min_batch_diff:.2f}@{min_timestamp}, \nMax: {max_batch_diff:.2f}@{max_timestamp} \n{current_time} {last_batch_diff}')




            fig.tight_layout()
            canvas.draw()
            canvas.flush_events()
            #plt.show()

        else:  # Behandle den Fall, dass df_filtered leer ist ODER eines der Plot-Objekte None ist
            print("Keine Daten für den ausgewählten Zeitraum gefunden oder Plot nicht initialisiert.")
            # Leere den Plot und/oder zeige eine Meldung an (Wichtig, um Fehler zu vermeiden)
            if line1 is not None and line2 is not None and ax1 is not None and ax2 is not None: # Überprüfe, ob die Objekte initialisiert wurden
                line1.set_data([], [])
                line2.set_data([], [])
                ax1.relim()
                ax1.autoscale_view()
                ax2.relim()
                ax2.autoscale_view()
                fig.canvas.draw()
                fig.canvas.flush_events()
            # Zeige eine Meldung in der GUI an (Optional)
            import tkinter.messagebox as messagebox
            messagebox.showinfo("Info", "Keine Daten für den ausgewählten Zeitraum gefunden oder Plot nicht initialisiert.")


    except Exception as e:
        print(f"Unerwarteter Fehler: {e}")
        import tkinter.messagebox as messagebox
        messagebox.showerror("Fehler", f"Ein Fehler ist aufgetreten: {e}")


def update_plot_tag(batch_column, node_column, cal_von, cal_bis):
    global fig, canvas, df, ax1, ax2, line1, line2, click_count
    try:
        click_count += 1
        if click_count == 1:
            # Letzte 30 Tage anzeigen
            end_date = datetime.now().date()
            start_date = end_date - timedelta(days=30)
        else:
            # Daten vom Kalender anzeigen
            start_date = datetime.strptime(cal_von.get_date(), '%Y-%m-%d').date()
            end_date = datetime.strptime(cal_bis.get_date(), '%Y-%m-%d').date()

        df['Zeitstempel_Datum'] = df['Zeitstempel'].dt.date
        df_filtered = df[(df['Zeitstempel_Datum'] >= start_date) & (df['Zeitstempel_Datum'] <= end_date)]

        if df_filtered is not None:
            df_daily = df_filtered.groupby(df_filtered['Zeitstempel'].dt.date).agg({
                'Diff_Batch': 'sum',
                'Diff_Nodes': 'sum',
                'Batch': 'last'
            }).reset_index()

            if not df_daily.empty and line1 and line2 and ax1 and ax2:
                line1.set_data(df_daily['Zeitstempel'], df_daily['Diff_Batch'])
                line2.set_data(df_daily['Zeitstempel'], df_daily['Diff_Nodes'])
                ax1.set_xlim(df_daily['Zeitstempel'].min(), df_daily['Zeitstempel'].max())
                ax2.set_xlim(df_daily['Zeitstempel'].min(), df_daily['Zeitstempel'].max())
                ax1.relim(); ax1.autoscale_view()
                ax2.relim(); ax2.autoscale_view()

                # Formatierung der X-Achse
                ax1.xaxis.set_major_formatter(mdates.ConciseDateFormatter(mdates.AutoDateLocator()))

                gesamt_summe = df_daily['Diff_Batch'].sum()
                mean_batch_diff = df_daily['Diff_Batch'].mean()

                # Aktuellen Tag ausschließen
                today = datetime.now().date()
                df_filtered_min = df_daily[df_daily['Zeitstempel'] != today]

                if not df_filtered_min.empty:
                    min_batch_diff = df_filtered_min['Diff_Batch'].min()
                    min_timestamp = df_filtered_min.loc[df_filtered_min['Diff_' + batch_column] == min_batch_diff, 'Zeitstempel'].iloc[0].strftime("%d.%m.%Y")
                else:
                    min_batch_diff = float('nan') # oder einen anderen Standardwert
                    min_timestamp = "N/A"

                max_batch_diff = df_daily['Diff_Batch'].max()
                max_timestamp = df_daily.loc[df_daily['Diff_' + batch_column] == max_batch_diff, 'Zeitstempel'].iloc[0].strftime("%d.%m.%Y")
                last_batch = df_daily['Batch'].iloc[-1]
                last_batch_diff = df_daily['Diff_Batch'].iloc[-1]
                current_time = datetime.now().strftime("%H:%M:%S")

                ax1.set_title(f'Tägliche Batch Total: {last_batch}, \nGesamtmenge: {gesamt_summe}, \nDurchschnitt: {mean_batch_diff:.2f}, \nMin: {min_batch_diff:.2f}@{min_timestamp}, \nMax: {max_batch_diff:.2f}@{max_timestamp} \n{current_time} {last_batch_diff}')

                # Beispiel für eine dünne gestrichelte vertikale Linie
                ax1.axvline(x=datetime.now().date(), color='gray', linestyle='--', linewidth=0.5)

                fig.tight_layout(); canvas.draw(); canvas.flush_events()
            else:
                if line1 and line2 and ax1 and ax2:
                    line1.set_data([], []); line2.set_data([], [])
                    ax1.relim(); ax1.autoscale_view(); ax2.relim(); ax2.autoscale_view()
                    canvas.draw(); canvas.flush_events()
                messagebox.showinfo("Info", "Keine Daten für den ausgewählten Zeitraum gefunden.")
    except Exception as e:
        messagebox.showerror("Fehler", f"Ein Fehler ist aufgetreten: {e}")

root = tk.Tk()
root.geometry("1200x900")
root.title("Diagramm mit Datumsauswahl")

# Initialisierung des Plots
batch_col = 'Batch'  # Wichtig: Spaltennamen speichern!
node_col = 'Nodes'
fig, ax1, ax2, line1, line2, df = plot_differences(filename, 'Batch', 'Nodes')

# Überprüfe, ob fig, ax1 UND df nicht None sind, bevor fortgefahren wird
if fig is not None and ax1 is not None and df is not None:  # Wichtige Änderung!
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    canvas.draw()

    date_frame = tk.Frame(root)
    date_frame.pack(side=tk.BOTTOM)

    cal_von = Calendar(date_frame, selectmode='day', date_pattern="yyyy-mm-dd")
    cal_von.pack(side=tk.LEFT, padx=10, pady=10)
    cal_bis = Calendar(date_frame, selectmode='day', date_pattern="yyyy-mm-dd")
    cal_bis.pack(side=tk.LEFT, padx=10, pady=10)

    #update_button = tk.Button(date_frame, text="Diagramm aktualisieren", font=("Arial", 14), command=update_plot)
    update_button = tk.Button(date_frame, text="Diagramm aktualisieren", font=("Arial", 14), command=lambda: update_plot(batch_col, node_col, cal_von, cal_bis)) # Lambda Funktion verwenden!

    update_button.pack(side=tk.LEFT, padx=10, pady=10)
    update_plot(batch_col, node_col, cal_von, cal_bis) # Plot sofort aktualisieren.
    update_button.invoke() # simuliert einen Button druck

    update_button_tag = tk.Button(date_frame, text="Diagramm pro Tag", font=("Arial", 14), command=lambda: update_plot_tag(batch_col, node_col, cal_von, cal_bis))
    update_button_tag.pack(side=tk.LEFT, padx=10, pady=10)

    plt.rcParams.update({'font.size': 12})

    root.mainloop()
else:
    print("Fehler beim Erstellen des Plots. Überprüfen Sie die CSV-Datei und die 'plot_differences'-Funktion.")
    # Hier könntest du auch eine Fehlermeldung in der GUI anzeigen, z.B. mit tkinter.messagebox
    import tkinter.messagebox as messagebox
    messagebox.showerror("Fehler", "Fehler beim Laden der Daten. Bitte überprüfen Sie die CSV-Datei.")
