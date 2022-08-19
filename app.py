import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go

def plot_map(data_plot,option):
    choropleth_map = go.Figure(
        data={
            'type': 'choropleth',
            'locations': list(data_plot.index),
            'locationmode': 'country names',
            'colorscale': 'greens',
            'z': data_plot["salary_in_usd"],
            'colorbar': {'title': 'World Population in 2020'},
            'marker': {
                'line': {
                    'color': 'rgb(255,255,255)',
                    'width': 2
                }
            }
        },
        layout={
            'geo': {
                'scope': 'world',
            }
        })
    choropleth_map.update_layout(
        title={
            'text': option + " average annual salary map",
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'}
    )
    return choropleth_map

job_list = []
with open('job_names.txt') as f:
    for line in f:
        job_list.append(line.replace("'","").split(",")[0].strip())
job_list.append("All")

st.title("Data Science Job Salaries")

data = pd.read_csv("ds_salaries.csv")
st.write(data[:10])

option = st.selectbox(
     'Please choose a data science job',
     job_list)

if option != "All":
    fig = px.box(data[data["job_title"] == option], x="experience_level", y="salary_in_usd", points="all",
                 title="Average annual dollar salaries of " + option + " by experience level")
    st.plotly_chart(fig)

    data_option = data[data["job_title"] == option]

    data_plot = data_option.groupby('company_name')[['salary_in_usd', 'salary']].mean()
    st.plotly_chart(plot_map(data_plot,option))
else:
    fig = px.box(data, x="experience_level", y="salary_in_usd", points="all",
                 title="Average annual dollar salaries of " + option + " by experience level")
    st.plotly_chart(fig)

    data_plot = data.groupby('company_name')[['salary_in_usd', 'salary']].mean()
    st.plotly_chart(plot_map(data_plot, "All"))
