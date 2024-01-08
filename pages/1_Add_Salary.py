import streamlit as st
import pandas as pd
import uuid
from google.cloud import firestore
from google.oauth2 import service_account
import json


def main():
    st.markdown("<h1 style='text-align: center;'>PayQuity</h1>", unsafe_allow_html=True)

    st.text(" ")

    st.subheader("Add Your Salary Details", divider="blue")

    if "company_names" not in st.session_state:
        df = pd.read_csv("companies_data.csv")
        st.session_state["industry_names"] = sorted(set(df["Industry"].tolist()))
        st.session_state["company_industry"] = df.groupby("Industry")["Company"].apply(
            list
        )

        for k in st.session_state["company_industry"].keys():
            st.session_state["company_industry"][k] = sorted(
                st.session_state["company_industry"][k]
            )

        country_df = pd.read_csv("countries_data.csv")
        st.session_state["country_names"] = sorted(set(country_df["Country"].tolist()))
        st.session_state["city_country"] = country_df.groupby("Country")["City"].apply(
            list
        )

        for k in st.session_state["city_country"].keys():
            st.session_state["city_country"][k] = sorted(
                st.session_state["city_country"][k]
            )

    st.text(" ")

    industry = st.selectbox(
        "Industry",
        st.session_state["industry_names"],
        key="industry",
    )

    company = st.selectbox(
        "Company",
        st.session_state["company_industry"][industry],
        key="company",
    )

    position = st.text_input(
        "Position",
        value=None,
        key="position",
    )

    country = st.selectbox(
        "Country",
        st.session_state["country_names"],
        key="country",
    )

    city = st.selectbox(
        "City",
        st.session_state["city_country"][country],
        key="city",
    )

    salary = st.number_input(
        "Salary ($)",
        min_value=0,
        max_value=100000,
        key="salary",
    )

    years = st.number_input(
        "Years of Experience",
        min_value=0,
        max_value=70,
        key="years",
    )

    race = st.selectbox(
        "Race",
        [
            "American Indian/Alaska Native",
            "Asian",
            "Black or African American",
            "Native Hawaiian or other Pacific Islander",
            "White",
        ],
        key="race",
    )

    gender = st.selectbox(
        "Gender",
        [
            "Male",
            "Female",
            "Agender",
            "Abimegender",
            "Adamas gender",
            "Aerogender",
            "Aesthetigender",
            "Affectugender",
            "Agenderflux",
            "Alexigender",
            "Aliusgender",
            "Amaregender",
            "Ambigender",
            "Ambonec",
            "Amicagender",
            "Androgyne",
            "Anesigender",
            "Angenital",
            "Anogender",
            "Anongender",
            "Antegender",
            "Anxiegender",
            "Apagender",
            "Apconsugender",
            "Astergender",
            "Astral gender",
            "Autigender",
            "Autogender",
            "Axigender",
            "Bigender",
            "Biogender",
            "Blurgender",
            "Boyflux",
            "Burstgender",
            "Caelgender",
            "Cassgender",
            "Cassflux",
            "Cavusgender",
            "Cendgender",
            "Ceterogender",
            "Ceterofluid",
            "Cisgender",
            "Cloudgender",
            "Collgender",
            "Colorgender",
            "Commogender",
            "Condigender",
            "Deliciagender",
            "Demifluid",
            "Demiflux",
            "Demigender",
            "Domgender",
            "Duragender",
            "Egogender",
            "Epicene",
            "Esspigender",
            "Exgender",
            "Existigender",
            "Femfluid",
            "Femgender",
            "Fluidflux",
            "Gemigender",
            "Genderblank",
            "Genderflow",
            "Genderfluid",
            "Genderfuzz",
            "Genderflux",
            "Genderpuck",
            "Genderqueer",
            "Gender witched",
            "Girlflux",
            "Healgender",
            "Mirrorgender",
            "Omnigender",
        ],
        key="gender",
    )

    submitted = st.button("Submit")
    if submitted:
        key_dict = json.loads(st.secrets["textkey"])
        creds = service_account.Credentials.from_service_account_info(key_dict)
        db = firestore.Client(credentials=creds, project="payquity-11a16")

        doc_ref = db.collection("salary-data").document(str(uuid.uuid4()))
        doc_ref.set(
            {
                "industry": industry,
                "company": company,
                "position": position,
                "country": country,
                "city": city,
                "salary": salary,
                "years": years,
                "race": race,
                "gender": gender,
            }
        )


if __name__ == "__main__":
    main()
