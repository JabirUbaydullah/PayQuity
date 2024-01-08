import streamlit as st
import pandas as pd
from google.cloud import firestore
import plotly.express as px
from google.oauth2 import service_account
import json


def filter_salary_data(salary_data, search_values, for_plot):
    if "industry" in search_values:
        salary_data = salary_data[salary_data["industry"] == search_values["industry"]]
    if "company" in search_values:
        salary_data = salary_data[salary_data["company"] == search_values["company"]]
    if "position" in search_values:
        salary_data = salary_data[salary_data["position"] == search_values["position"]]
    if "country" in search_values:
        salary_data = salary_data[salary_data["country"] == search_values["country"]]
    if "city" in search_values:
        salary_data = salary_data[salary_data["city"] == search_values["city"]]
    if "years" in search_values:
        salary_data = salary_data[salary_data["years"] == search_values["years"]]
    if not for_plot:
        if "race" in search_values:
            salary_data = salary_data[salary_data["race"] == search_values["race"]]
        if "gender" in search_values:
            salary_data = salary_data[salary_data["gender"] == search_values["gender"]]

    salary_data.columns = map(str.title, salary_data.columns)
    salary_data = salary_data.rename(
        {"Salary": "Annual Salary ($)", "Years": "Years of Experience"},
        axis="columns",
    )

    salary_data = salary_data[
        [
            "Position",
            "Company",
            "Annual Salary ($)",
            "Gender",
            "Race",
            "Years of Experience",
            "City",
            "Country",
        ]
    ]

    return salary_data


def main():
    st.set_page_config(page_title="PayQuity")
    
    st.markdown("<h1 style='text-align: center;'>PayQuity</h1>", unsafe_allow_html=True)

    st.text(" ")
    description = "<p>PayQuity allows the user to enter in information regarding their position and view the salaries of others in similar positions. This will allow users to understand if offers the user recieves are fair. This website also promotes racial and gender pay equity as it allows users to view how salaries compare between different races and genders. Salary information is crowdsourced anonymously by user contributions and searchable by a variety of filters.</p>"

    st.markdown(description, unsafe_allow_html=True)
    st.text(" ")
    search_filters = st.multiselect(
        "Choose Search Filters",
        [
            "Company",
            "Industry",
            "Position",
            "Country",
            "City",
            "Race",
            "Gender",
            "Years of Experience",
        ],
    )

    if "search_industry_names" not in st.session_state:
        company_df = pd.read_csv("companies_data.csv")
        st.session_state["search_industry_names"] = sorted(
            company_df["Industry"].unique().tolist()
        )
        st.session_state["search_company_names"] = sorted(
            company_df["Company"].unique().tolist()
        )

        country_df = pd.read_csv("countries_data.csv")
        st.session_state["search_country_names"] = sorted(
            country_df["Country"].unique().tolist()
        )
        st.session_state["search_city_names"] = sorted(
            country_df["City"].unique().tolist()
        )

    search_filter_row = st.empty()
    search_filter_len = max(1, len(search_filters))
    search_filter_columns = search_filter_row.columns(search_filter_len)

    search_values = dict()

    for idx, f in enumerate(search_filters):
        if f == "Industry":
            search_values["industry"] = search_filter_columns[idx].selectbox(
                "Industry",
                st.session_state["search_industry_names"],
                key="industry-filter",
            )
        elif f == "Company":
            search_values["company"] = search_filter_columns[idx].selectbox(
                "Company",
                st.session_state["search_company_names"],
                key="company-filter",
            )
        elif f == "Position":
            search_values["position"] = search_filter_columns[idx].text_input(
                "Position",
                value=None,
                key="position-filter",
            )
        elif f == "Country":
            search_values["country"] = search_filter_columns[idx].selectbox(
                "Country",
                st.session_state["search_country_names"],
                key="country-filter",
            )
        elif f == "City":
            search_values["city"] = search_filter_columns[idx].selectbox(
                "City",
                st.session_state["search_city_names"],
                key="city-filter",
            )
        elif f == "Years of Experience":
            search_values["years"] = search_filter_columns[idx].number_input(
                "Years of Experience",
                min_value=0,
                max_value=70,
                key="years-filter",
            )
        elif f == "Race":
            search_values["race"] = search_filter_columns[idx].selectbox(
                "Race",
                [
                    "American Indian/Alaska Native",
                    "Asian",
                    "Black or African American",
                    "Native Hawaiian or other Pacific Islander",
                    "White",
                ],
                key="race-filter",
            )
        elif f == "Gender":
            search_values["gender"] = search_filter_columns[idx].selectbox(
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
                key="years-filter",
            )

    search_button = st.button("Search")
    if search_button:
        if "salary_data_" not in st.session_state:
            key_dict = json.loads(st.secrets["textkey"])
            creds = service_account.Credentials.from_service_account_info(key_dict)
            db = firestore.Client(credentials=creds, project="payquity-11a16")

            doc_ref = db.collection("salary-data")
            st.session_state["salary_data_"] = pd.DataFrame(
                [d.to_dict() for d in doc_ref.stream()]
            )

        salary_data = st.session_state["salary_data_"].copy()
        filtered_salary_data = filter_salary_data(
            salary_data, search_values, for_plot=False
        )

        plot_salary_data = filter_salary_data(salary_data, search_values, for_plot=True)

        st.plotly_chart(
            px.strip(
                plot_salary_data,
                x="Race",
                y="Annual Salary ($)",
                color="Race",
                hover_data=[
                    "Position",
                    "Annual Salary ($)",
                    "Gender",
                    "Race",
                    "Years of Experience",
                    "City",
                    "Country",
                ],
            )
        )

        st.plotly_chart(
            px.strip(
                plot_salary_data,
                x="Gender",
                y="Annual Salary ($)",
                color="Gender",
                hover_data=[
                    "Position",
                    "Annual Salary ($)",
                    "Gender",
                    "Race",
                    "Years of Experience",
                    "City",
                    "Country",
                ],
            )
        )

        st.text(" ")

        st.subheader("Result Summary:")
        summarized_filtered_salary_data = (
            filtered_salary_data.copy()
            .drop("Years of Experience", axis="columns")
            .groupby(
                ["Position", "Company", "Gender", "Race", "City", "Country"],
                as_index=False,
            )
            .agg({"Annual Salary ($)": "mean"})
        )

        summarized_filtered_salary_data = summarized_filtered_salary_data.rename(
            {"Annual Salary ($)": "Average Annual Salary ($)"},
            axis="columns",
        )

        summarized_filtered_salary_data["Average Annual Salary ($)"] = (
            summarized_filtered_salary_data["Average Annual Salary ($)"]
            .astype(int)
            .map("{:,}".format)
        )

        filtered_salary_data["Annual Salary ($)"] = (
            filtered_salary_data["Annual Salary ($)"].astype(int).map("{:,}".format)
        )

        st.markdown(
            summarized_filtered_salary_data[
                [
                    "Position",
                    "Company",
                    "Average Annual Salary ($)",
                    "Gender",
                    "Race",
                    "City",
                    "Country",
                ]
            ]
            .sort_values(
                by=["Position", "Company", "Gender", "Race", "City", "Country"]
            )
            .style.hide(axis="index")
            .to_html(),
            unsafe_allow_html=True,
        )

        st.text(" ")
        st.text(" ")

        st.subheader("Search Results:")
        st.markdown(
            filtered_salary_data.sort_values(
                by=[
                    "Position",
                    "Company",
                    "Gender",
                    "Race",
                    "Years of Experience",
                    "City",
                    "Country",
                ]
            )
            .style.hide(axis="index")
            .to_html(),
            unsafe_allow_html=True,
        )


if __name__ == "__main__":
    main()
