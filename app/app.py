import pandas as pd
import numpy as np
import pickle
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import os


# CONFIGURATION GÉNÉRALE

st.set_page_config(
    page_title="JO 2028 — Prédiction des médailles",
    page_icon="🏅",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Palette inspirée des anneaux olympiques
BLEU   = "#0085C7"
JAUNE  = "#F4C300"
NOIR   = "#1A1A2E"
VERT   = "#009F3D"
ROUGE  = "#DF0024"
PALETTE_SPORTS = [BLEU, JAUNE, ROUGE, VERT, NOIR, "#6C4AB6", "#00B8A9", "#F08A24"]

CSS = f"""
<style>
    .stApp {{ background-color: #FFFFFF; }}

    /* Bandeau de titre façon piste d'athlétisme */
    .header-bar {{
        background: linear-gradient(90deg, {BLEU} 0%, {BLEU} 60%, {JAUNE} 60%, {JAUNE} 80%, {ROUGE} 80%, {ROUGE} 100%);
        height: 8px;
        border-radius: 4px;
        margin-bottom: 1.2rem;
    }}

    h1, h2, h3 {{ color: {NOIR}; font-family: 'Arial', sans-serif; }}

    .kpi-card {{
        background-color: #F4F6F8;
        border-left: 6px solid {BLEU};
        border-radius: 8px;
        padding: 1rem 1.2rem;
        text-align: left;
    }}
    .kpi-value {{ font-size: 2.1rem; font-weight: 800; color: {NOIR}; line-height: 1.1; }}
    .kpi-label {{ font-size: 0.85rem; color: #5A6472; text-transform: uppercase; letter-spacing: 0.04em; }}

    .badge-host {{
        display: inline-block;
        background-color: {JAUNE};
        color: {NOIR};
        font-weight: 700;
        padding: 0.15rem 0.6rem;
        border-radius: 999px;
        font-size: 0.78rem;
        margin-left: 0.4rem;
    }}

    section[data-testid="stSidebar"] {{ background-color: #F4F6F8; }}

    div[data-testid="stMetricValue"] {{ color: {BLEU}; }}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)



# CHARGEMENT DES DONNÉES (mis en cache pour la performance)

@st.cache_data
def charger_donnees():
    base = os.path.dirname(__file__)
    df = pd.read_csv(os.path.join(base, "..", "data", "processed", "df_cleaned.csv"))
    predictions = pd.read_csv(os.path.join(base, "..", "data", "processed", "predictions_2028.csv"))

    cotes_path = os.path.join(base, "..", "data", "processed", "cotes_athletes.csv")
    cotes = pd.read_csv(cotes_path) if os.path.exists(cotes_path) else pd.DataFrame()

    comp_path = os.path.join(base, "..", "data", "processed", "comparaison_modeles.csv")
    comparaison = pd.read_csv(comp_path) if os.path.exists(comp_path) else pd.DataFrame()

    return df, predictions, cotes, comparaison


@st.cache_resource
def charger_modele():
    base = os.path.dirname(__file__)
    chemin = os.path.join(base, "model.pkl")
    if not os.path.exists(chemin):
        return None
    with open(chemin, "rb") as f:
        return pickle.load(f)


try:
    df, predictions, cotes, comparaison = charger_donnees()
except FileNotFoundError as e:
    st.error(
        "Données introuvables. Exécute d'abord le notebook `modelisation_JO2028.ipynb` "
        "en entier : il génère les fichiers attendus dans `data/processed/`.\n\n"
        f"Détail technique : {e}"
    )
    st.stop()

modele_info = charger_modele()
nom_modele = modele_info["nom_modele"] if modele_info else "Modèle non chargé"

PAYS_HOTE_2028 = "United States"


# EN-TÊTE

st.markdown('<div class="header-bar"></div>', unsafe_allow_html=True)
col_titre, col_badge = st.columns([5, 2])
with col_titre:
    st.title(" Performances sportives — JO Los Angeles 2028")
    st.caption(f"Projet fil rouge · Modèle retenu : **{nom_modele}** · Historique 1896–2016")
with col_badge:
    st.markdown(
        f"<div style='text-align:right; padding-top:1.6rem;'>"
        f"<span class='badge-host'>🇺🇸 Pays hôte 2028 : USA</span></div>",
        unsafe_allow_html=True,
    )


# SIDEBAR — FILTRES

st.sidebar.header(" Filtres")

sports_dispo = sorted(df["sport_group"].dropna().unique())
sport_choisi = st.sidebar.selectbox("Sport", ["Tous les sports"] + sports_dispo)

pays_dispo = sorted(df["country"].dropna().unique())
pays_choisis = st.sidebar.multiselect("Pays (vide = tous)", pays_dispo)

st.sidebar.markdown("---")
st.sidebar.caption(
    "Projet fil rouge — Performances sportives JO 2028 Los Angeles\n\n"
    "LAWSON Emmanuella · DOTSU Olympe"
)

# Application des filtres
df_f = df.copy()
pred_f = predictions.copy()
cotes_f = cotes.copy() if not cotes.empty else cotes

if sport_choisi != "Tous les sports":
    df_f = df_f[df_f["sport_group"] == sport_choisi]
    pred_f = pred_f[pred_f["sport_group"] == sport_choisi]
    if not cotes_f.empty:
        cotes_f = cotes_f[cotes_f["sport_group"] == sport_choisi]

if pays_choisis:
    df_f = df_f[df_f["country"].isin(pays_choisis)]
    pred_f = pred_f[pred_f["country"].isin(pays_choisis)]
    if not cotes_f.empty:
        cotes_f = cotes_f[cotes_f["country"].isin(pays_choisis)]


# INDICATEURS CLÉS (KPI)

k1, k2, k3, k4 = st.columns(4)
kpis = [
    (k1, f"{len(df_f):,}".replace(",", " "), "Médailles historiques (filtre actuel)"),
    (k2, f"{df_f['country_code'].nunique()}", "Pays représentés"),
    (k3, f"{pred_f['predicted_medals_2028'].sum():.0f}", "Médailles prédites — 2028"),
    (k4, f"{df_f['sport_group'].nunique()}", "Disciplines couvertes"),
]
for col, value, label in kpis:
    col.markdown(
        f"<div class='kpi-card'><div class='kpi-value'>{value}</div>"
        f"<div class='kpi-label'>{label}</div></div>",
        unsafe_allow_html=True,
    )

st.write("")

# ONGLETS

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    " Historique", "Prédictions 2028", " Type de médaille",
    " Côtes athlètes", " Carte du monde",
])


# TAB 1 — HISTORIQUE

with tab1:
    c1, c2 = st.columns(2)

    with c1:
        st.subheader("Top 10 pays — total médailles")
        top_pays = (df_f.groupby("country").size()
                    .sort_values(ascending=False).head(10).reset_index(name="medailles"))
        fig = px.bar(top_pays, x="medailles", y="country", orientation="h",
                     color_discrete_sequence=[BLEU])
        fig.update_layout(yaxis={'categoryorder': 'total ascending'}, showlegend=False,
                           xaxis_title="Médailles", yaxis_title="")
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.subheader("Évolution dans le temps")
        if pays_choisis:
            pays_evol = pays_choisis
        else:
            pays_evol = list(df_f.groupby("country").size().sort_values(ascending=False).head(5).index)
        evol = (df_f[df_f["country"].isin(pays_evol)]
                .groupby(["year", "country"]).size().reset_index(name="medailles"))
        fig = px.line(evol, x="year", y="medailles", color="country", markers=True,
                       color_discrete_sequence=PALETTE_SPORTS)
        fig.update_layout(xaxis_title="Année", yaxis_title="Médailles")
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Heatmap pays × sport (top 15 pays)")
    top_pays_heat = df.groupby("country").size().sort_values(ascending=False).head(15).index
    heat_data = (df[df["country"].isin(top_pays_heat)]
                 .pivot_table(index="country", columns="sport_group",
                              values="medal", aggfunc="count", fill_value=0))
    fig = px.imshow(heat_data, aspect="auto", color_continuous_scale=[[0, "#F4F6F8"], [1, BLEU]])
    fig.update_layout(xaxis_title="Sport", yaxis_title="Pays")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader(" Effet pays hôte")
    st.info(
        "Historiquement, un pays organisateur remporte en moyenne **davantage de médailles** "
        "l'année où il accueille les Jeux. Cette variable (`is_host`) est intégrée dans le "
        "modèle prédictif — déterminante pour 2028, où **les États-Unis sont l'hôte**."
    )


# TAB 2 — PRÉDICTIONS 2028

with tab2:
    st.subheader("Combien de médailles par sport en 2028 ?")
    par_sport = (pred_f.groupby("sport_group")["predicted_medals_2028"]
                 .sum().sort_values(ascending=False).reset_index())
    fig = px.bar(par_sport, x="sport_group", y="predicted_medals_2028",
                 color="sport_group", color_discrete_sequence=PALETTE_SPORTS,
                 labels={"sport_group": "Sport", "predicted_medals_2028": "Médailles prédites"})
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Top 15 couples pays × sport les plus prometteurs")
    top15 = pred_f.sort_values("predicted_medals_2028", ascending=False).head(15)
    fig = px.bar(top15, x="predicted_medals_2028", y="country", color="sport_group",
                 orientation="h", color_discrete_sequence=PALETTE_SPORTS)
    fig.update_layout(yaxis={'categoryorder': 'total ascending'}, xaxis_title="Médailles prédites", yaxis_title="")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Détail des prédictions")
    cols_detail = [c for c in ["country", "sport_group", "predicted_medals_2028",
                                "predicted_gold", "predicted_silver", "predicted_bronze"]
                   if c in pred_f.columns]
    st.dataframe(
        pred_f.sort_values("predicted_medals_2028", ascending=False)[cols_detail],
        use_container_width=True, hide_index=True,
    )

    if not comparaison.empty:
        with st.expander(" Comparaison des modèles testés (MAE / RMSE / R²)"):
            st.dataframe(comparaison, use_container_width=True, hide_index=True)

    scatter_path = os.path.join(os.path.dirname(__file__), "..", "graphiques", "scatter_pred_vs_reel.png")
    if os.path.exists(scatter_path):
        with st.expander(" Validation du modèle (prédictions vs réalité sur le passé)"):
            st.image(scatter_path, use_container_width=True)

# TAB 3 — TYPE DE MÉDAILLE
with tab3:
    st.subheader("Répartition Or / Argent / Bronze prédite pour 2028")
    cols_type = [c for c in ["predicted_gold", "predicted_silver", "predicted_bronze"] if c in pred_f.columns]

    if cols_type:
        top10_type = pred_f.sort_values("predicted_medals_2028", ascending=False).head(10)
        fig = go.Figure()
        couleurs_medailles = {"predicted_gold": JAUNE, "predicted_silver": "#C0C0C0", "predicted_bronze": "#CD7F32"}
        noms = {"predicted_gold": "Or", "predicted_silver": "Argent", "predicted_bronze": "Bronze"}
        for col in cols_type:
            fig.add_bar(name=noms[col], x=top10_type["country"] + " · " + top10_type["sport_group"],
                        y=top10_type[col], marker_color=couleurs_medailles[col])
        fig.update_layout(barmode="stack", xaxis_title="", yaxis_title="Médailles prédites",
                           legend_title="Type")
        st.plotly_chart(fig, use_container_width=True)

        st.caption(
            "Estimation basée sur le ratio historique Or/Argent/Bronze observé pour chaque "
            "couple pays/sport, appliqué au total de médailles prédit par le modèle."
        )

        st.dataframe(
            top10_type[["country", "sport_group", "predicted_medals_2028"] + cols_type],
            use_container_width=True, hide_index=True,
        )
    else:
        st.warning("Les colonnes de type de médaille ne sont pas présentes dans le fichier de prédictions.")


# TAB 4 — CÔTES ATHLÈTES

with tab4:
    if cotes_f.empty:
        st.warning("Le fichier `cotes_athletes.csv` n'a pas été trouvé. Exécute le notebook de modélisation en entier.")
    else:
        st.subheader("Côtes des athlètes (score basé sur l'historique de médailles)")
        st.caption(
            "Score = Or × 3 + Argent × 2 + Bronze × 1, majoré de 50 % si l'athlète a encore "
            "concouru depuis 2008. Indicateur descriptif, pas une prédiction individuelle "
            "(le dataset ne contient pas d'âge ni de données physiques par athlète)."
        )
        top_athletes = cotes_f.sort_values("cote", ascending=False).head(20)
        fig = px.bar(top_athletes, x="cote", y="athlete", color="sport_group",
                     orientation="h", color_discrete_sequence=PALETTE_SPORTS)
        fig.update_layout(yaxis={'categoryorder': 'total ascending'}, xaxis_title="Côte", yaxis_title="")
        st.plotly_chart(fig, use_container_width=True)

        cols_athl = [c for c in ["athlete", "country", "sport_group", "total_medailles", "or_count", "cote"]
                     if c in top_athletes.columns]
        st.dataframe(top_athletes[cols_athl], use_container_width=True, hide_index=True)


# TAB 5 — CARTE DU MONDE

with tab5:
    st.subheader("Répartition mondiale des médailles prédites — 2028")
    pred_pays = predictions.groupby("country_code")["predicted_medals_2028"].sum().reset_index()
    fig = px.choropleth(
        pred_pays, locations="country_code", color="predicted_medals_2028",
        color_continuous_scale=[[0, "#F4F6F8"], [0.5, JAUNE], [1, ROUGE]],
        labels={"predicted_medals_2028": "Médailles prédites"},
    )
    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))
    st.plotly_chart(fig, use_container_width=True)

    st.caption(
        "Carte construite à partir du total de médailles prédites, toutes disciplines "
        "confondues, par pays."
    )
