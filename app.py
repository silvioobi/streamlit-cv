import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from streamlit_folium import st_folium
import folium

# Load CV data
cv_file = "CV.xlsx"
cv_data = pd.read_excel(cv_file)
cv_data.rename(columns={"Bezeichnung": "Task", "Start": "Start", "Ende": "Finish", "Kategorie": "Type"}, inplace=True)

def format_description(text):
    if pd.isna(text):
        return ""
    return text.replace(" •", "\n•").strip()

cv_data["Formatted Beschreibung"] = cv_data["Beschreibung"].apply(format_description)
position_descriptions = {
    row["Task"]: (row["Institution"], row["Formatted Beschreibung"]) for _, row in cv_data.iterrows()
}

# Load social media
linkedin_url = ""
try:
    social_df = pd.read_excel("Social Media.xlsx")
    linkedin_row = social_df[social_df["Social Media"].str.lower() == "linkedin"]
    if not linkedin_row.empty:
        linkedin_url = linkedin_row.iloc[0]["URL"]
except:
    st.warning("Social Media Datei konnte nicht geladen werden oder fehlt.")

certificates = [
    "Hermes 5.1 Advanced",
    "Certified Project Management Associate IPMA Level D",
    "First"
]

st.set_page_config(layout="wide")
st.title("Lebenslauf Silvio Oberholzer")

# Oberer Block in Container mit zwei Spalten
with st.container():
    col_left, col_right = st.columns([1, 2], gap="large")

    with col_left:
        st.subheader("Persönliche Angaben")
        st.markdown("**Name:** Silvio Oberholzer")
        st.markdown("**Email:** silvio_oberholzer@hotmail.com")
        st.markdown("**Mobile:** +41 78 917 19 94")
        st.markdown("**Hobbies:** Tennis, Padel, Darts, Wandern, Joggen, Kochen")
        if linkedin_url:
            st.markdown(f"**LinkedIn:** [Profil ansehen]({linkedin_url})")

        try:
            st.image("profilbild.jpg", width=200)
        except:
            st.warning("Bild nicht gefunden. Stelle sicher, dass 'profilbild.jpg' im Projektordner liegt.")

        try:
            st.markdown("**Wohnort:**")
            map_data = folium.Map(location=[47.33078, 9.42634], zoom_start=12)
            folium.Marker([47.33078, 9.42634], popup="Meine Adresse").add_to(map_data)
            st_data = st_folium(map_data, width=300, height=200)
        except:
            st.warning("Karte konnte nicht geladen werden.")

    with col_right:
        st.subheader("Beruflicher Werdegang und Aus-/Weiterbildungen")
        fig = px.timeline(cv_data, x_start="Start", x_end="Finish", y="Task", color="Type")
        fig.update_yaxes(autorange="reversed", title=None)
        fig.update_layout(height=400, font=dict(size=14), margin=dict(t=30, b=30))
        st.plotly_chart(fig, use_container_width=True)

        clicked_task = st.selectbox("Wähle eine Position zur Anzeige der Beschreibung:", cv_data["Task"].tolist())
        if clicked_task:
            institution, beschreibung = position_descriptions.get(clicked_task, ("", "Keine Beschreibung verfügbar."))
            st.markdown(f"<b>Beschreibung:</b><br><div style='white-space: pre-wrap'>{institution}</div>",
                        unsafe_allow_html=True)
            st.markdown(f"<b>Beschreibung:</b><br><div style='white-space: pre-wrap'>{beschreibung}</div>",
                        unsafe_allow_html=True)

# Unterer Block: Kenntnisse und Zertifikate
col3, col4 = st.columns([1, 1], gap="large")

with col3:
    st.subheader("Kenntnisse")
    try:
        kenntnisse_df = pd.read_excel("Kenntnisse.xlsx")
        kenntnisse_filtered = kenntnisse_df.dropna(subset=["quantitative Beurteilung"])

        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=kenntnisse_filtered["quantitative Beurteilung"].tolist(),
            theta=kenntnisse_filtered["Kenntnis"].tolist(),
            fill='toself',
            name='Skill-Level'
        ))
        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 5])),
            showlegend=False,
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
    except FileNotFoundError:
        st.error(f"Datei 'Kenntnisse.xlsx' nicht gefunden.")

st.subheader("Datenanalysen & Berichte")

analysen_links = {
    "Analyse Laufzeiten vom Auffahrtslauf 2024": "https://www.linkedin.com/pulse/analyse-der-marathon-und-halbmarathon-daten-vom-silvio-oberholzer-euaef/?trackingId=NGnqJvFgQlKk97wAqfZh1w%3D%3D",
    "Power BI Bericht - Passantenfrequenz Stadt St.Gallen": "https://dalix.ch/passantenfrequenz-in-der-st-galler-innenstadt/",
    "Power BI Bericht - Entwicklung Bevölkerung Stadt St.Gallen": "https://dalix.ch/entwicklung-der-bevoelkerung-der-stadt-st-gallen/",
    "Power BI Bericht - Axa Women's Super League": "https://dalix.ch/die-axa-womens-super-league-verabschiedet-sich-in-die-winterpause/",
}

for titel, link in analysen_links.items():
    st.markdown(f"- [{titel}]({link})")

with col4:
    st.subheader("Zertifikate")
    for cert in certificates:
        st.markdown(f"- {cert}")
