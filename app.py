import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from streamlit_folium import st_folium
import folium


st.set_page_config(
    layout="wide",
    initial_sidebar_state="collapsed"
)


# Load CV data
cv_file = "CV.xlsx"
cv_data = pd.read_excel(cv_file)
cv_data.rename(columns={"Bezeichnung": "Bezeichnung", "Start": "Start", "Ende": "Finish", "Kategorie": "Kategorie"}, inplace=True)

def format_description(text):
    if pd.isna(text):
        return ""
    return text.replace(" •", "\n•").strip()

cv_data["Formatted Beschreibung"] = cv_data["Beschreibung"].apply(format_description)
position_descriptions = {
    row["Bezeichnung"]: (row["Institution"], row["Formatted Beschreibung"]) for _, row in cv_data.iterrows()
}


analysen_links = {
    "Analyse Laufzeiten vom Auffahrtslauf 2024": "https://www.linkedin.com/pulse/analyse-der-marathon-und-halbmarathon-daten-vom-silvio-oberholzer-euaef/?trackingId=NGnqJvFgQlKk97wAqfZh1w%3D%3D",
    "Power BI Bericht - Passantenfrequenz Stadt St.Gallen": "https://dalix.ch/passantenfrequenz-in-der-st-galler-innenstadt/",
    "Power BI Bericht - Entwicklung Bevölkerung Stadt St.Gallen": "https://dalix.ch/entwicklung-der-bevoelkerung-der-stadt-st-gallen/",
    "Power BI Bericht - Axa Women's Super League": "https://dalix.ch/die-axa-womens-super-league-verabschiedet-sich-in-die-winterpause/",
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
    "First Certificate in English B2"
]

st.title("Lebenslauf Silvio Oberholzer")

# Oberer Block in Container mit zwei Spalten

with st.container():
    col_left, col_right = st.columns([3, 8], gap="large")

    with col_left:
        st.subheader("Persönliche Angaben")
        st.markdown("**Silvio Oberholzer**")


        try:
            st.image("profilbild.jpg", width=200)
        except:
            st.warning("Bild nicht gefunden. Stelle sicher, dass 'profilbild.jpg' im Projektordner liegt.")

        #if linkedin_url:
        #    st.markdown(f"**LinkedIn:** [Profil ansehen]({linkedin_url})")
        if linkedin_url:
            st.markdown(
                f"""
                <div style="display: flex; align-items: center; gap: 10px;">
                    <img src="linkedin.jpg" width="24">
                    <a href="{linkedin_url}" target="_blank" style="text-decoration: none; font-weight: bold; color: white;">
                        Profil ansehen
                    </a>
                </div>
                """,
                unsafe_allow_html=True
            )
        st.markdown("✉️ silvio_oberholzer@hotmail.com")
        st.markdown("📞 +41 78 917 19 94")



        try:
            st.markdown("**Wohnort:**")
            map_data = folium.Map(location=[47.33078, 9.42634], zoom_start=12)
            folium.Marker([47.33078, 9.42634], popup="Meine Adresse").add_to(map_data)
            st_data = st_folium(map_data, width=300, height=200)
        except:
            st.warning("Karte konnte nicht geladen werden.")

        hobbies = ["🎾 Tennis", "🏓 Padel", "🎯 Darts", "🥾 Wandern", "🏃‍♂️ Joggen", "🍳 Kochen"]
        st.markdown("**Hobbies:**<br>" + "<br>".join(hobbies), unsafe_allow_html=True)
        #st.markdown("**Hobbies:** 🎾 Tennis, 🏓 Padel, 🎯 Darts, 🥾 Wandern, 🏃‍ Joggen, 🍳 Kochen")

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
                paper_bgcolor="rgba(0,0,0,0)",  # transparenter Hintergrund
                plot_bgcolor="rgba(0,0,0,0)",
                polar=dict(
                    bgcolor="rgba(0,0,0,0)",
                    radialaxis=dict(
                        visible=True,
                        range=[0, 5],
                        showline=True,
                        linewidth=1,
                        gridcolor="lightgray",
                        linecolor="lightgray",
                        tickfont=dict(color="white", size=12)
                    ),
                    angularaxis=dict(
                        tickfont=dict(size=13, color="white"),
                        rotation=90,
                        direction="clockwise"
                    )
                ),
                font=dict(color="white"),
                showlegend=False,
                height=450
            )
            st.plotly_chart(fig, use_container_width=True)
        except FileNotFoundError:
            st.error(f"Datei 'Kenntnisse.xlsx' nicht gefunden.")

        st.subheader("Datenanalysen & Berichte")

        for titel, link in analysen_links.items():
            st.markdown(f"- [{titel}]({link})")

        st.subheader("Zertifikate")
        for cert in certificates:
            st.markdown(f"- {cert}")


    with col_right:
        st.subheader("Beruflicher Werdegang und Aus-/Weiterbildungen")

        # Gantt-Diagramm mit angepasster Legende
        fig = px.timeline(
            cv_data,
            x_start="Start",
            x_end="Finish",
            y="Bezeichnung",
            color="Kategorie",
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig.update_yaxes(autorange="reversed", title=None)
        fig.update_layout(
            autosize=True,
            font=dict(size=14),
            margin=dict(t=30, b=30, l=20, r=150),
            legend_title_text="Klassifizierung",
            legend=dict(
                orientation="h",  # horizontal
                yanchor="bottom",
                y=1.1,  # etwas oberhalb des Plots
                xanchor="center",
                x=0.5
            )
        )
        st.plotly_chart(fig, use_container_width=True)

        # Details nach Klassifizierung (gleiche Reihenfolge wie im Gantt)
        st.subheader("Details zu den Stationen")

        # Reihenfolge wie im Gantt
        type_order = cv_data["Kategorie"].dropna().unique().tolist()

        for group in type_order:
            group_data = cv_data[cv_data["Kategorie"] == group].sort_values(by="Start", ascending=False)
            st.markdown(f"### {group}")  # Überschrift pro Klassifizierung

            for _, row in group_data.iterrows():
                title = f"{row['Bezeichnung']} ({row['Start'].date()} – {row['Finish'].date()})"
                with st.expander(title):
                    # Institution + Bild
                    bilddatei = row.get("Bild", "")
                    bild_url = f"/Users/silviooberholzer/Documents/Bewerbungen/Meine/aktuell/CV_Visual/{bilddatei}" if pd.notna(bilddatei) else None
                    cols = st.columns([1, 4])

                    with cols[0]:
                        if bild_url and str(bild_url).lower().endswith((".png", ".jpg", ".jpeg")):
                            try:
                                st.image(bild_url, width=150)
                            except Exception as e:
                                st.warning(f"Bild konnte nicht geladen werden: {bild_url}")

                    with cols[1]:
                        st.markdown(f"**Institution:** {row['Institution']}<br><br>", unsafe_allow_html=True)

                    st.markdown(
                        f"**Beschreibung:**<br><div style='white-space: pre-wrap'>{row['Formatted Beschreibung']}</div>",
                        unsafe_allow_html=True
                    )
