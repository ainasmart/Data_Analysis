import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px

# Create an heading for the application.
st.title("Exploring World Happiness Data")
st.divider()

filepath = "whr_200522.csv"
df = pd.read_csv(filepath)

# Showing the dataframe.
st.dataframe(df)

def yearly_happiness(year):
    """
    Return a map plot of the "Happiness score" for the countries of the world.
    ================================
    parameter:
    year: str datatype
    """
    year_check = df[df["year"].isin([year])]
    country_happiness = (
        year_check.groupby(["Iso alpha", "Country name"])["Happiness score"].mean().reset_index()
    )
    fig = px.choropleth(
        data_frame=country_happiness,
        locations = "Iso alpha",
        color= "Happiness score",
        color_continuous_scale = px.colors.sequential.Viridis,
        hover_name="Country name",
        title= f"Mean Happiness score in {year}",
        # height = 600,
        projection= "natural earth"
    )
    st.plotly_chart(fig)

def card(Country, year):
    country_df = df[df["Country name"] == Country]
    happiness = country_df[country_df["year"] == year]["Happiness score"]
    pc = country_df[country_df["year"] == year]["Perceptions of corruption"]
    gdp = country_df[country_df["year"] == year]["Log GDP per capita"]
    # Create 3 columns.
    col1, col2, col3 = st.columns(3)
    col1.metric("Happiness Score", happiness)
    col2.metric("GDP per Capita", gdp)

def country_gdp(Country):
    """
    Return a line plot of the "Log GDP per capita" for the specified country.
    ================================
    parameter:
    country: str datatype
    """
    country_check = df[df["Country name"] == Country]
    fig = px.line(
        country_check, 
        x= "year", 
        y="Log GDP per capita",
        markers=True,
        line_shape = "spline",
        title=f"Log GDP per capita {Country}")
    # Display the figure.
    st.write(fig)
# Adding side bar to the application.
with st.sidebar:
    # Get the list of years in the dataframe.
    list_year = list(np.sort(df["year"].unique()))
    # Slider.
    year_option = st.select_slider("Year", list_year, list_year[-1])
    # Create a list for the countries.
    country_ls = list(np.sort(df["Country name"].unique()))
    # Drop Down menu.
    country_option =st.selectbox("Country Name", country_ls)
# Call the function.
yearly_happiness(year_option)
card(country_option, year_option)
country_gdp(country_option)
