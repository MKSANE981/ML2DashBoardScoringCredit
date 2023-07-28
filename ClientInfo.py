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

@st.cache_data
def apply_filters(df, ID):
    filtered_df = df.copy()
    # Filtre sur l'identifiant de campagne (campaign_id)
    if ID:
        filtered_df = filtered_df[filtered_df["ID"] == ID]
    # Filtre sur l'âge (age)
    #if len(age_range):
    #    filtered_df = filtered_df[(filtered_df["age"] >= age_range[0]) & (filtered_df["age"] <= age_range[1])]
    return filtered_df

def filters2(df, SeriousDlqin2yrs):
    filtered_df = df.copy()
    # Filtre sur l'identifiant de campagne (campaign_id)
    if ID:
        filtered_df = filtered_df[filtered_df["SeriousDlqin2yrs"]==SeriousDlqin2yrs]
    # Filtre sur l'âge (age)
    #if len(age_range):
    #    filtered_df = filtered_df[(filtered_df["age"] >= age_range[0]) & (filtered_df["age"] <= age_range[1])]
    return filtered_df
def gauge_plot(scor, th):
    scor = int(scor * 100)
    th = int(th * 100)

    if scor >= th:
        couleur_delta = 'red'
    elif scor < th:
        couleur_delta = 'Orange'

    if scor >= th:
        valeur_delta = "red"
    elif scor < th:
        valeur_delta = "green"

    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=scor,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Score du client", 'font': {'size': 25}},
        delta={'reference': int(th), 'increasing': {'color': valeur_delta}},
        gauge={
            'axis': {'range': [None, int(100)], 'tickwidth': 1.5, 'tickcolor': "black"},
            'bar': {'color': "darkblue"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, int(th)], 'color': 'lightgreen'},
                {'range': [int(th), int(scor)], 'color': couleur_delta}],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 1,
                'value': int(th)}}))

    fig.update_layout(paper_bgcolor=None, font={'color': "darkblue", 'family': "Arial"})
    return fig

def hbar(df, label,max_value,marge):
    fig, ax = plt.subplots(figsize=(9, 0.5))
    ax.barh(label, df, align='center')
    ax.invert_yaxis()
    ax.set_xlim(0, max_value+marge)
    ax.set_xlabel(" ")
    ax.set_title(f" {df}")
    plt.show()
    st.pyplot()


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


url4 = "https://raw.githubusercontent.com/MKSANE981/ML2DashBoardScoringCredit/main/prediction_sur_test.csv"
prediction_sur_test = pd.read_csv(url4)
training = pd.DataFrame(prediction_sur_test)
training["ID"] = list(range(1, training.shape[0]+1))
#st.dataframe(prediction_sur_test,use_container_width=True)

#st.dataframe(predictions.head(10), use_container_width=True)

ID = st.sidebar.selectbox("Selectionner l'identifiant",options=training["ID"].to_list())

filtered_data = apply_filters(training, ID)
num=ID-1
Age = filtered_data["age"][num]
SeriousDlqin2yrs = filtered_data["SeriousDlqin2yrs"][num]
RevolvingUtilizationOfUnsecuredLines = filtered_data["RevolvingUtilizationOfUnsecuredLines"][num]
NumberOfTime3059DaysPastDueNotWorse = filtered_data["NumberOfTime30-59DaysPastDueNotWorse"][num]
DebtRatio = filtered_data["DebtRatio"][num]
MonthlyIncome = filtered_data["MonthlyIncome"][num]
NumberOfOpenCreditLinesAndLoans = filtered_data["NumberOfOpenCreditLinesAndLoans"][num]
NumberOfTimes90DaysLate = filtered_data["NumberOfTimes90DaysLate"][num]
NumberRealEstateLoansOrLines = filtered_data["NumberRealEstateLoansOrLines"][num]
NumberOfTime6089DaysPastDueNotWorse = filtered_data["NumberOfTime60-89DaysPastDueNotWorse"][num]
NumberOfDependents = filtered_data["NumberOfDependents"][num]
Probability = filtered_data["Probability"][num]
decision = filtered_data["decision"][num]

DebtRatio = "{:.2f}".format(DebtRatio)
DebtRatio = float(DebtRatio)

RevolvingUtilizationOfUnsecuredLines = RevolvingUtilizationOfUnsecuredLines * 100
RevolvingUtilizationOfUnsecuredLines = "{:.2f}".format(RevolvingUtilizationOfUnsecuredLines)

## Info de la classe
Class_Info = filters2(training,SeriousDlqin2yrs)

Mean_Debt_Ratio = Class_Info["DebtRatio"].mean()
Mean_Debt_Ratio = "{:.2f}".format(Mean_Debt_Ratio)
Mean_Debt_Ratio = float(Mean_Debt_Ratio)

Mean_RevolvingUtilizationOfUnsecuredLines = Class_Info["RevolvingUtilizationOfUnsecuredLines"].mean()
Mean_RevolvingUtilizationOfUnsecuredLines = "{:.2f}".format(Mean_RevolvingUtilizationOfUnsecuredLines)
Mean_RevolvingUtilizationOfUnsecuredLines = float(Mean_RevolvingUtilizationOfUnsecuredLines)

Mean_NumberOfOpenCreditLinesAndLoans = Class_Info["NumberOfOpenCreditLinesAndLoans"].mean()
Mean_NumberOfOpenCreditLinesAndLoans = "{:.2f}".format(Mean_NumberOfOpenCreditLinesAndLoans)
Mean_NumberOfOpenCreditLinesAndLoans = float(Mean_NumberOfOpenCreditLinesAndLoans)

Mean_NumberOfTimes90DaysLate = Class_Info["NumberOfTimes90DaysLate"].mean()
Mean_NumberOfTimes90DaysLate = "{:.2f}".format(Mean_NumberOfTimes90DaysLate)
Mean_NumberOfTimes90DaysLate = float(Mean_NumberOfTimes90DaysLate)

Mean_NumberOfTime3059DaysPastDueNotWorse = Class_Info["NumberOfTime30-59DaysPastDueNotWorse"].mean()
Mean_NumberOfTime3059DaysPastDueNotWorse = "{:.2f}".format(Mean_NumberOfTime3059DaysPastDueNotWorse)
Mean_NumberOfTime3059DaysPastDueNotWorse = float(Mean_NumberOfTime3059DaysPastDueNotWorse)

Mean_NumberOfTime6089DaysPastDueNotWorse = Class_Info["NumberOfTime60-89DaysPastDueNotWorse"].mean()
Mean_NumberOfTime6089DaysPastDueNotWorse = "{:.2f}".format(Mean_NumberOfTime6089DaysPastDueNotWorse)
Mean_NumberOfTime6089DaysPastDueNotWorse = float(Mean_NumberOfTime6089DaysPastDueNotWorse)




seuil = 0.33


col1, col2=st.columns(2)
if ID:
    with col1:
        st.title("Informations phares :")
        st.markdown("""<style>.big-font {font-size: 24px;} .huge {font-size: 100px;} .gras{font-size:16px; font-weight: bold;} .color{color:green;font-size: 30px;} </style>
                """, unsafe_allow_html=True)
        st.markdown(
            f'<p class="big-font">Age : <span class="color"> {Age} </span> ans</p>',
            unsafe_allow_html=True)
        st.markdown(
            f'<p class="big-font">Charge 👨‍👩‍👦‍👦 : <span class="color"> {NumberOfDependents} </span> pers.</p>',
            unsafe_allow_html=True)
        st.markdown(
            f'<p class="big-font">Revenu mensuelle 💰 : <span class="color"> {MonthlyIncome} </span> </p>',
            unsafe_allow_html=True)
        st.markdown(
            f'<p class="big-font">Utilisation renouvelable 💳<br> des lignes non garanties : <span class="color"> {RevolvingUtilizationOfUnsecuredLines} %</span> </p>',
            unsafe_allow_html=True)
    with col2:
        st.markdown(
            f'<p class="big-font">Seuil : <span class="color"> {seuil*100} %</span> </p>',
            unsafe_allow_html=True)
        st.markdown(
            f'<p class="big-font">Décision : <span class="color"> {decision} </span> </p>',
            unsafe_allow_html=True)
        figure = gauge_plot(Probability, seuil)
        st.write(figure)
st.title("Taux d'endettement")
lig1,lig2=st.columns([10,3])
with lig1:
    hbar(DebtRatio, " ",round(DebtRatio+1),round(DebtRatio+1))
with lig2:
    st.metric(label="Par rapport à son groupe", value=Mean_Debt_Ratio, delta=DebtRatio - Mean_Debt_Ratio)


part1,part2=st.columns(2)

with part1:
    st.markdown(
        f'<p><span class="big-font"> Retard 30 - 59 jrs</span> </p>',
        unsafe_allow_html=True)
    value = "{:.0f}".format(NumberOfTime3059DaysPastDueNotWorse)
    st.markdown(
        f'<p class="bigfont"><span class="huge"> {value}</span> </p>',
        unsafe_allow_html=True)
with part2:
    st.markdown(
        f'<p><span class="big-font"> Retard 60 - 89 jrs</span> </p>',
        unsafe_allow_html=True)
    value = "{:.0f}".format(NumberOfTime6089DaysPastDueNotWorse)
    st.markdown(
        f'<p class="bigfont"><span class="huge"> {value}</span> </p>',
        unsafe_allow_html=True)

part3,part4 = st.columns(2)
with part3:
    st.markdown(
        f'<p><span class="big-font"> Lignes de crédit et de prêts ouverts (en cours...)</span> </p>',
        unsafe_allow_html=True)
    value = "{:.0f}".format(NumberOfOpenCreditLinesAndLoans)
    st.markdown(
        f'<p class="bigfont"><span class="huge"> {value}</span> </p>',
        unsafe_allow_html=True)

with part4:
    st.markdown(
        f'<p><span class="big-font"> Prêts hypothécaires et immobiliers (en cours...)</span> </p>',
        unsafe_allow_html=True)
    value = "{:.0f}".format(NumberRealEstateLoansOrLines)
    st.markdown(
        f'<p class="bigfont"><span class="huge"> {value}</span> </p>',
        unsafe_allow_html=True)


st.markdown(
        f'<p><span class="gras"> Utilisation renouvelable des lignes non garanties</span> : Solde total des cartes de crédit et des lignes de crédit personnelles, à l\'exception des biens immobiliers et des dettes à tempérament comme les prêts automobiles, divisé par la somme des limites de crédit. </p>',
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

