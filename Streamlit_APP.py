# -*- coding: utf-8 -*-
"""
Created on Thu May 18 23:04:57 2023

@author: hugom
"""

import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import pandas as pd

#GIT update2

final_score = pd.read_csv('final_score.csv')
df_1 = pd.read_csv('df_1')

categories_2017 = pd.read_csv('categories_2017')
categories_2018 = pd.read_csv('categories_2018')
categories_2019 = pd.read_csv('categories_2019')
categories_2020 = pd.read_csv('categories_2020')
categories_2021 = pd.read_csv('categories_2021')
categories_2022 = pd.read_csv('categories_2022')

categories_2017 = pd.concat([df_1['Constituent Name'], categories_2017], axis=1)
categories_2018 = pd.concat([df_1['Constituent Name'], categories_2018], axis=1)
categories_2019 = pd.concat([df_1['Constituent Name'], categories_2019], axis=1)
categories_2020 = pd.concat([df_1['Constituent Name'], categories_2020], axis=1)
categories_2021 = pd.concat([df_1['Constituent Name'], categories_2021], axis=1)
categories_2022 = pd.concat([df_1['Constituent Name'], categories_2022], axis=1)

benchmark = final_score.iloc[:, 1:].mean()

# Create a new DataFrame with the "Year" and "Benchmark" columns
benchmark = pd.DataFrame({'Year': benchmark.index, 'Benchmark': benchmark.values})

## Streamlit part to display our results
# create first page
page = st.sidebar.selectbox("Select a page", ["Homepage", "Scores", "Peers Overview", "Historical Trend"])

if page == "Homepage":
    st.title('Refinitiv Hackathon')
    st.write("The place where YOU will understand financial data in a simpler way !")
    st.markdown(
        "A word from the founders: 'Our aim is to simplify the financial experience for our users. We want people to easily read financial data and make better investment decisions.'")
    st.markdown(
        "* This isn't just a regular financial data platform. We've collected various financial ratios and multiples, and applied innovative methods such as Singular Value Decomposition to determine the weight of each input. "
        "All of this is distilled into a simple, easy-to-understand score ranging from 0 to 100.")
    st.markdown("We want people to be able to read financial data with a click of a button")

    st.markdown("""
    In order to navigate through this app, use the sidebar on the left to access the three different tabs:

    - **Scores**: View all the scores and the breakdown of each category.
    - **Peers Overview**: Compare the scores of different companies side by side.
    - **Historical Trend**: Display the evolution of the final score for each selected company over the past five years against a benchmark.
    """)

    st.markdown("**Note:** This app is a sample based solely on financial ratios and multiples. It does not consider other factors and is based only on data from 2017 to 2022. These scores are not live and should not be considered as such.")

if page == "Scores":
    # set sidebar
    st.sidebar.title("Select an INDEX")
    index = st.sidebar.selectbox(label="Choose an INDEX", options=['CAC 40'])

    st.sidebar.title("Select a Sector")
    sector = st.sidebar.selectbox(label="Choose a Sector", options=df_1['TRBC Economic Sector Name'].unique())

    # filter df_1 by selected sector and extract unique constituent names
    constituents = df_1[df_1['TRBC Economic Sector Name'] == sector]['Constituent Name'].unique()

    st.sidebar.title("Select a company")
    company = st.sidebar.selectbox(label="Choose a company", options=final_score['Constituent Name'])

    st.sidebar.title("Year")
    selected_year = st.sidebar.selectbox(label="Choose a Year", options=['2022', '2021', '2020', '2019', '2018'])
    selected_column = f'Final Score {selected_year}'

    # Filter data by selected company and column
    company_score = final_score.loc[final_score['Constituent Name'] == company, selected_column].values[0]

    # Get the minimum and maximum scores for the selected year
    selected_year_scores = final_score[f'Final Score {selected_year}']
    lowest_score = selected_year_scores.min()
    highest_score = selected_year_scores.max()

    # Create the gauge chart with the final score, minimum score, and maximum score
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=company_score,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': f"Final Score {selected_year}<br>{company}"},
        delta={'reference': company_score},
        gauge={
            'axis': {'range': [None, 100]},
            'steps': [
                {'range': [0, lowest_score], 'color': 'lightgray'},
                {'range': [lowest_score, highest_score], 'color': 'gray'}
            ],
            'threshold': {
                'line': {'color': 'red', 'width': 4},
                'thickness': 0.75,
                'value': company_score
            }
        }
    ))

    st.plotly_chart(fig)
    st.write(
        'Below this we want to display the breakdown of how the score is calculated with the 6 different categories score we have')

    # Get the category scores for the selected company and year
    selected_categories = globals()[f'categories_{selected_year}']
    # Get the index of the selected company in the category data frame
    company_index = selected_categories[selected_categories['Constituent Name'] == company].index[0]

    company_categories = selected_categories.iloc[company_index, 1:]  # Exclude the 'Constituent Name' column

    # Create a bar chart to display the category scores
    fig_categories = go.Figure(go.Bar(
        x=company_categories.index,
        y=company_categories.values,
        marker_color='steelblue'
    ))

    fig_categories.update_layout(
        title=f"Category Scores for {company} in {selected_year}",
        xaxis_title="Category",
        yaxis_title="Score"
    )

    st.plotly_chart(fig_categories)

if page == "Peers Overview":
    st.title("Peers Overview")
    st.sidebar.title("Select companies to display")

    # Allow multiple company selections
    selected_companies = st.sidebar.multiselect(label="Choose companies", options=final_score['Constituent Name'])

    st.sidebar.title("Year")
    selected_year = st.sidebar.selectbox(label="Choose a Year", options=['2022', '2021', '2020', '2019', '2018'])
    selected_column = f'Final Score {selected_year}'

    # Sorting options
    sort_options = ['None', 'Score : Low-High', 'Score : High-Low']
    selected_sort = st.sidebar.selectbox(label="Sort Order", options=sort_options)

    # Display gauge charts for selected companies
    gauge_charts = []
    for company in selected_companies:
        company_score = final_score.loc[final_score['Constituent Name'] == company, selected_column].values[0]

        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=company_score,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': f"Final Score {selected_year}<br>{company}"},
            gauge={'axis': {'range': [None, 100]}}  # Set the range of the gauge to 100
        ))

        fig.update_layout(
            font=dict(family="Arial, sans-serif", size=18, color="#7f7f7f"),
            width=500,
            height=400,
            margin=dict(l=75, r=75, t=25, b=60)  # Adjust the margin to center the chart
        )

        gauge_charts.append((fig, company_score))

    # Sort companies by their scores
    if selected_sort == 'Score : Low-High':
        sorted_companies = sorted(gauge_charts, key=lambda x: x[1])
    elif selected_sort == 'Score : High-Low':
        sorted_companies = sorted(gauge_charts, key=lambda x: x[1], reverse=True)
    else:  # None, no sorting
        sorted_companies = gauge_charts

    # Display the sorted gauge charts
    for fig, _ in sorted_companies:
        st.plotly_chart(fig)

if page == "Historical Trend":
    # Select multiple companies
    selected_companies = st.sidebar.multiselect(label="Choose companies", options=final_score['Constituent Name'])

    # Get the scores for the selected companies
    selected_scores = final_score[final_score['Constituent Name'].isin(selected_companies)]

    # Sort the columns based on the year
    sorted_columns = sorted(selected_scores.columns,
                            key=lambda x: int(x.split()[-1]) if x.split()[-1].isdigit() else float('inf'))
    selected_scores = selected_scores[sorted_columns]

    # Extract the years
    years = [col.replace('Final Score ', '') for col in sorted_columns if col.startswith('Final Score ')]

    # Create line charts for each selected company
    fig = go.Figure()

    for index, row in selected_scores.iterrows():
        company_name = row['Constituent Name']
        scores = row[sorted_columns].values

        # Add a trace for each company
        fig.add_trace(go.Scatter(x=years, y=scores, mode='lines+markers', name=company_name))

    # Add a trace for the benchmark
    benchmark_scores = final_score.iloc[:, 1:].mean()
    fig.add_trace(go.Scatter(x=years, y=benchmark_scores, mode='lines', name='Benchmark'))

    # Set the chart title and axis labels
    fig.update_layout(title="Scores for Selected Companies",
                      xaxis_title="Year",
                      yaxis_title="Score")

    # Display the line chart
    st.plotly_chart(fig)