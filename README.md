# PayQuity

## Inspiration
The topic I wanted to address was racial and gender pay equity as there are many examples in the modern day of racial and gender minorities unfairly receiving lower salaries compared to their coworkers.

## What it does
The web application allows the user to provide salary information regarding their work and view the salaries of others in similar positions along with associated race and gender data. This has many uses such as allowing users to better negotiate salaries as they will have a better grasp of how much others in the same position are paid. The salary information is crowdsourced anonymously by user contributions and is searchable by a variety of filters.

## How we built it
PayQuity was built in Python and using the following libraries and services:

* [streamlit](https://github.com/streamlit/streamlit) for the web user interface and web application hosting
* [pandas](https://github.com/pandas-dev/pandas) for all data transformation and aggregation
* [plotly](https://github.com/plotly/plotly.py) for the charts
* [Google Cloud Firestore](https://github.com/googleapis/python-firestore) for salary data persistence and retrieval
* [Google OAuth2](https://github.com/googleapis/google-auth-library-python-oauthlib) for securely accessing the Firestore database

## Challenges we ran into
The most significant challenge I ran into was making use of the Google Cloud Firestore database as prior to this event I had not worked with it.

## Accomplishments that we're proud of
I am very happy that I managed to create the web application I had envisioned with all the filtering, storing, and retrieving of salary data correctly working all of which felt a bit daunting when I began the project.

## What we learned
This project was my first exposure to using a managed NoSQL database (Google Cloud Firestore) and I learned a lot about how to store and query data from a document database securely. I also gained experience using pandas both for extracting only relevant data from publicly available datasets to fit my use cases for some of the dropdowns (e.g. Company, Country, City lists) as well as for performing aggregations to show more useful summarized salary data.

## What's next for PayQuity
I plan to improve PayQuity by adding even more filters, finding an automated way or API to keep the list of companies up to date, and adding a comparison feature to allow users to directly compare their salaries to salaries at different companies for the same position. 
