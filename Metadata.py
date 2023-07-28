import streamlit as st
import pandas as pd
import numpy as np
import datetime
from PIL import Image
from streamlit_pandas_profiling import st_profile_report
import pandas_profiling
import streamlit as st
from st_pages import Page, show_pages, add_page_title


logo = Image.open('logo.png')
st.set_page_config(page_title="Scoring credit", page_icon=logo, layout="wide")
add_page_title("MetaData : Explication des données")


url1 = "https://raw.githubusercontent.com/MKSANE981/ML2DashBoardScoringCredit/main/Predictions.csv"
predictions = pd.read_csv(url1)
predictions = pd.DataFrame(predictions)
if "Unnamed: 0" in predictions.columns:
    predictions.drop(["Unnamed: 0"],axis=1, inplace=True)
url2 = "https://raw.githubusercontent.com/MKSANE981/ML2DashBoardScoringCredit/main/base-test.csv"
test = pd.read_csv(url2)
test = pd.DataFrame(test)
if "Unnamed: 0" in test.columns:
    test.drop(["Unnamed: 0"], axis=1, inplace=True)
url3 = "https://raw.githubusercontent.com/MKSANE981/ML2DashBoardScoringCredit/main/base-training.csv"
training = pd.read_csv(url3)
training = pd.DataFrame(training)
#st.write(test.columns)

## Description des variables
url4 = "https://raw.githubusercontent.com/MKSANE981/ML2DashBoardScoringCredit/main/MetaData.csv"
training = pd.read_csv(url4)
st.data_editor(
    training,
    column_config={
        "sales": st.column_config.ListColumn(
            "Métadonnées",
            help="Explication des variables",
            width="large",
        ),
    },
    hide_index=True,
)
## Pandas Profiling

pr = test.profile_report()
st_profile_report(pr)
