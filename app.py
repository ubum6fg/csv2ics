import streamlit as st
import pandas as pd
import datetime
import re

# Funktion zum Parsen der Datumsangaben
def parse_datetime(date_str):
    match = re.match(r"\w+\. (\d{2})\.(\d{2})\.(\d{4}) (\d{2}):(\d{2})-(\d{2}):(\d{2})", date_str)
    if match:
        day, month, year, start_hour, start_minute, end_hour, end_minute = map(int, match.groups())
        start_dt = datetime.datetime(year, month, day, start_hour, start_minute)
        end_dt = datetime.datetime(year, month, day, end_hour, end_minute)
        return start_dt, end_dt
    return None, None

# CSV in ICS konvertieren
def convert_csv_to_ics(csv_file):
    df = pd.read_csv(csv_file, delimiter=';')
    events = []
    
    for _, row in df.iterrows():
        start_dt, end_dt = parse_datetime(row['Zeitraum'])
        if start_dt and end_dt:
            event = f"""BEGIN:VEVENT
SUMMARY:{row['Dienst']}
DTSTART:{start_dt.strftime('%Y%m%dT%H%M%S')}Z
DTEND:{end_dt.strftime('%Y%m%dT%H%M%S')}Z
DESCRIPTION:{row.get('Kommentar', '')}
LOCATION:Flugplatz
BEGIN:VALARM
TRIGGER:-P7D
ACTION:DISPLAY
DESCRIPTION:Erinnerung an den Termin
END:VALARM
END:VEVENT"""
            events.append(event)

    ics_content = "BEGIN:VCALENDAR\nVERSION:2.0\n" + "\n".join(events) + "\nEND:VCALENDAR"
    return ics_content

# Streamlit UI
st.title("CSV zu ICS Konverter 📆")
st.write("Lade eine CSV-Datei hoch, um sie in das ICS-Format umzuwandeln.")

uploaded_file = st.file_uploader("CSV-Datei hochladen", type="csv")

if uploaded_file is not None:
    ics_content = convert_csv_to_ics(uploaded_file)
    st.download_button("ICS-Datei herunterladen", ics_content, "Dienste.ics", "text/calendar")

