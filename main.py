import streamlit as st
import pandas as pd
import numpy as np
import datetime
from PIL import Image
from st_pages import Page, show_pages, add_page_title

logo = Image.open('logo.png')
st.set_page_config(page_title="Scoring credit", page_icon=logo, layout="wide")
add_page_title("Scoring Credit")

show_pages(
    [
        Page("main.py", "Activité bancaire", "📈"),
        Page("DashBoard.py", "Global Information", "📉"),
        Page("ClientInfo.py", "Client Information", "👨‍✈️️"),
        Page("Metadata.py", "Explication des données", ":bar_chart:"),

    ]
)
st.markdown("""<style>.big-font {font-size: 24px; text-align:justify;} .huge {font-size: 40px;font-weight: bold;} .color{color:green;font-size: 30px;} </style>
        """, unsafe_allow_html=True)

st.markdown("<p class='big-font'>L\'activité bancaire est un secteur capital du tissu économique au regard de son "
            "apport aussi bien pour les individus que les entreprises. Ce secteur constitue un "
            "levier de dévélopement dans la mésure où une bonne gestioin du risque bancaire "
            "permet de plus grands octrois de crédit et de plus grands investissements d'où "
            "une amelioration des conditions de vies. Mais  bien souvent  confronté à la difficulté"
            " de cerner la solvabilité des emprunteurs, plusieurs banques retrécissent "
            "leurs octroient de crédits."
            "Notre projet de scoring de crédit s\'inscrit dans le cadre de la proposition"
            " de solution pour palier à ce problème. Le projet vise à développer une "
            "solution pour évaluer de façon précise le risque de crédit des individus et "
            "des entreprises, afin de faciliter une prise de décision financière éclairée "
            "et responsable. </span></p>",
            unsafe_allow_html=True)
st.balloons()

col1,col2,col3=st.columns(3)
with col1:
    st.markdown("<p class='huge'>Global Information 📉</p>",
                unsafe_allow_html=True)
    st.markdown("<p class='big-font'>Trouver sur cet onlget les informations agrégées des clients.</p>",
                unsafe_allow_html=True)
with col2:
    st.markdown("<p class='huge'>Client Information 👨‍✈️</p>",
                unsafe_allow_html=True)
    st.markdown("<p class='big-font'>Cet onglet renseigne sur les informations personnelles des clients ainsi que "
             "ses prêts, le retard de paiement...</p>",
                unsafe_allow_html=True)
with col3:
    st.markdown("<p class='huge'>Explication des données️</p>",
                unsafe_allow_html=True)
    st.markdown("<p class='big-font'>Cet onglet donne des informations sur les différentes variables afin de mieux comprendre"
             "les indicateurs utilisés pour concevoir ces DashBoards</p>",
                unsafe_allow_html=True)

