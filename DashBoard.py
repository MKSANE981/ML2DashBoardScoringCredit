## Importation des packages

import streamlit as st
import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import seaborn as sns
from PIL import Image
import joblib
import plotly.express as px
import statistics as stat
from annotated_text import annotated_text

logo = Image.open('logo.png')
st.set_page_config(page_title="Scoring Credit", page_icon=logo, layout="wide")
st.set_option('deprecation.showPyplotGlobalUse', False)

col1, col2 = st.columns([1,5])
with col1:
    st.image(logo)
with col2:
    st.title("Scoring Credit : Global Information")

## Importations des données à partir du dossier GitHub

url1 = "https://raw.githubusercontent.com/MKSANE981/ML2DashBoardScoringCredit/main/Predictions.csv"
predictions = pd.read_csv(url1)
predictions = pd.DataFrame(predictions)

url2 = "https://raw.githubusercontent.com/MKSANE981/ML2DashBoardScoringCredit/main/base-test.csv"
test = pd.read_csv(url2)
test = pd.DataFrame(test)
test = test.rename(columns={test.columns[0]: "ID"})

url3 = "https://raw.githubusercontent.com/MKSANE981/ML2DashBoardScoringCredit/main/base-training.csv"
training = pd.read_csv(url3)
training = pd.DataFrame(training)
training = training.rename(columns={training.columns[0]: "ID"})
training= training.fillna(0)
#st.dataframe(predictions.head(10), use_container_width=True)


################################################

# Définition des fonctions de filtres
@st.cache_data
def apply_filters(df, age_range):
    filtered_df = df.copy()
    # Filtre sur l'identifiant de campagne (campaign_id)
    #if ID:
        #filtered_df = filtered_df[filtered_df["ID"].isin(ID)]

    # Filtre sur l'âge (age)
    if len(age_range):
        filtered_df = filtered_df[(filtered_df["age"] >= age_range[0]) & (filtered_df["age"] <= age_range[1])]
    return filtered_df



# Définitions des fonctions de construction des sorties

def circulaire(filtered_data):
    counts=filtered_data["SeriousDlqin2yrs"].value_counts()
    if counts.value_counts().shape[0]<2:
        unique_value = counts.unique().tolist()[0]
        if unique_value==1:
            label=["Défaut (1)","Non-Défaut (0)"]
        else:
            label=["Non-Défaut (0)", "Défaut (1)"]
        #st.write(counts.value_counts()[0])
        plt.figure(figsize=(6, 6))
        plt.pie([counts.value_counts().tolist()[0],0], labels=label, autopct='%1.2f%%', startangle=140,
                colors=['cornflowerblue', 'lightblue'])
        plt.title(" ")
        plt.axis('equal')  # Pour que le diagramme soit un cercle parfait
        plt.show()
        st.pyplot()

    else:
        plt.figure(figsize=(6, 6))
        plt.pie(counts, labels=["Non-Défaut (0)", "Défaut (1)"], autopct='%1.2f%%', startangle=140, colors=['cornflowerblue', 'lightblue'])
        plt.title(" ")
        plt.axis('equal')  # Pour que le diagramme soit un cercle parfait
        plt.show()
        st.pyplot()

def create_age_boxplot(df):
    filtered_data = df #.dropna(subset=["age", "product_id"])
    plt.figure(figsize=(10, 6))
    sns.boxplot(x="MonthlyIncome", y="age", data=filtered_data)
    plt.xlabel("Revenu mensuel")
    plt.ylabel("Âge")
    plt.title("Box Plot de l'Âge en fonction du Revenu mensuel")
    st.pyplot()

##################################################

age_range = st.sidebar.slider("Sélectionner la plage d'âge", min_value=int(training["age"].min()),
                                  max_value=int(training["age"].max()),
                                  value=(int(training["age"].min()), int(training["age"].max())))
filtered_data = apply_filters(training, age_range)
col1, col2 = st.columns(2)
with col1:
    st.markdown("""<style>.big-font {font-size: 24px;} .huge {font-size: 100px;} .gras{font-size:16px; font-weight: bold;} .color{color:green;font-size: 30px;} </style>
            """, unsafe_allow_html=True)
    st.title(f"👨‍💼👩‍💼")
    st.markdown(
        f'<p class="big-font"><span class="color"> {filtered_data.shape[0]} </span></p>',
        unsafe_allow_html=True)
with col2:
    st.write("Sortie 2")
lig1, lig2, lig3,lig4, lig5 = st.columns([5,1,5,1,5])

with lig1:
    st.write("Retard 30 - 59 jours")
    filtered_data3059 = filtered_data[filtered_data["NumberOfTime30-59DaysPastDueNotWorse"] > 0]
    circulaire(filtered_data3059)
with lig2:
    st.write(" ")
with lig3:
    st.write("Retard 60 - 89 jours")
    filtered_data6089 = filtered_data[filtered_data["NumberOfTime60-89DaysPastDueNotWorse"] > 0]
    circulaire(filtered_data6089)
with lig4:
    st.write(" ")
with lig5:
    st.write("Retard 90 jours et plus")
    filtered_data90 = filtered_data[filtered_data["NumberOfTimes90DaysLate"] > 0]
    circulaire(filtered_data90)

part1, part2 = st.columns(2)
with part1:
    st.markdown(
        f'<p><span class="big-font"> Total lignes de crédit et de prêts ouverts en cours...</span> </p>',
        unsafe_allow_html=True)
    value = "{:.0f}".format(filtered_data["NumberOfOpenCreditLinesAndLoans"].sum())
    st.markdown(
        f'<p class="bigfont"><span class="huge"> {value}</span> </p>',
        unsafe_allow_html=True)

with part2:
    st.markdown(
        f'<p><span class="big-font"> Total Prêts hypothécaires et immobiliers en cours...</span> </p>',
        unsafe_allow_html=True)
    value = "{:.0f}".format(filtered_data["NumberRealEstateLoansOrLines"].sum())
    st.markdown(
        f'<p class="bigfont"><span class="huge"> {value}</span> </p>',
        unsafe_allow_html=True)


st.markdown(
        f'<p><span class="gras"> Retard 30 - 59 jrs</span> : Nombre de fois où l\'emprunteur a été en retard de 30 à 59 jours, mais pas plus, au cours des deux dernières années. </p>',
        unsafe_allow_html=True)

st.markdown(
        f'<p><span class="gras"> Retard 60 - 89 jrs</span> : Nombre de fois où l\'emprunteur a été en retard de 60 à 89 jours, mais pas plus, au cours des deux dernières années. </p>',
        unsafe_allow_html=True)

st.markdown(
        f'<p><span class="gras"> Retard 90 jrs et +</span> : Nombre de fois où l\'emprunteur a été en retard de plus de 90 jours, au cours des deux dernières années. </p>',
        unsafe_allow_html=True)

st.markdown(
        f'<p><span class="gras"> Lignes de crédit et de prêts ouverts</span> : Nombre de prêts en cours (à tempérament comme un prêt automobile ou un prêt hypothécaire) et de lignes de crédit (par exemple, cartes de crédit) </p>',
        unsafe_allow_html=True)

st.markdown(
        f'<p><span class="gras"> Nombre de prêts immobiliers ou de lignes de crédit</span> : Nombre de prêts hypothécaires et immobiliers, y compris les lignes de crédit immobilier </p>',
        unsafe_allow_html=True)

