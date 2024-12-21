import streamlit as st
import pandas as pd
import numpy as np
import datautils as du
import plotly.express as px
import statsmodels.api as sm


st.set_page_config(
page_title="Airbnb Analysis💶",
layout="wide", # or wide
page_icon="📈", # choose your favorite icon
initial_sidebar_state="expanded" # or expanded
)

airbnb_df = du.get_airbnb_data()
cost_df = du.get_cost_data()

st.title("🏤 AirBnB Price vs Cost of Living in Europe 💶")


st.header("Airbnb Price distribution in European Cities") ###########################################################

city_sel = st.multiselect("Select a city", airbnb_df.city.unique(), key="city")

# Filter the DataFrame based on the selection and combine for plotting
filtered_df = airbnb_df[airbnb_df.city.isin(city_sel)]

# Check if the dataframe is not empty after filtering
if not filtered_df.empty:
    # Create a histogram, using 'color' to differentiate by city
    fig = px.histogram(
        filtered_df, 
        x='price', 
        color='city',  # Use the 'city' column for color coding
        nbins=100, 
        title='Airbnb Prices Distribution by City (per night in €)',
        labels={'price': 'Price', 'count': 'Count'},
        opacity=1, 
        barmode='group',
        color_discrete_sequence=px.colors.qualitative.Set2
    )

    # Update the layout of the plot
    fig.update_layout(
        xaxis_title='Airbnb Price',
        yaxis_title='Number of Listings',
        bargap=0.05  # Gap of 5% between bars
    )  

    st.plotly_chart(fig)
    
st.subheader("Airbnb Price Comparisson") ###########################################################

for city in cost_df['city'].unique():
    cost_df.loc[cost_df['city'] == city, 'avg_airbnb_price'] = airbnb_df[airbnb_df['city'] == city]['price'].mean()
    cost_df.loc[cost_df['city'] == city, 'median_airbnb_price'] = airbnb_df[airbnb_df['city'] == city]['price'].median()
    cost_df.loc[cost_df['city'] == city, 'avg_fee'] = airbnb_df[airbnb_df['city'] == city]['fee'].median()


st.title("Average Airbnb Prices by City")
cost_df.sort_values(by=['avg_airbnb_price'], inplace=True, ascending=False) 

selected_columns = ['city', 'avg_airbnb_price', 'median_airbnb_price', 'avg_fee']

filtered_df = cost_df[selected_columns]

# Melt the DataFrame to a long format for plotting
filtered_df_melted = filtered_df.melt(id_vars='city', var_name='price_type', value_name='price')

# Create a grouped bar chart
fig = px.bar(filtered_df_melted, x='city', y='price', color='price_type',
             barmode='group', 
             labels={'price': 'Airbnb Price', 'price_type': 'Price Type'},
             title='Average and Median Airbnb Prices by City (per night in €)')

# Display the Plotly chart
st.plotly_chart(fig)

st.header("Cost of Living") #############################################################

st.subheader("Cost of Living Comparisson")

# Allow selection of a city
city_sel = st.selectbox("Select a city", cost_df['city'].unique())

# Filter the data for the selected city
city_data = cost_df[cost_df['city'] == city_sel].reset_index(drop=True)

# Columns to visualize
selected_columns = ['sqrtm_suburbs', 'sqrtm_center', 'rent_onebed_suburbs', 'rent_onebed_center', 'rent_threebed_suburbs', 'rent_threebed_center']

# Calculate averages across all cities for comparison
averages = cost_df[selected_columns].mean()

# Prepare data for plotting
plot_data = []
for col in selected_columns:
    plot_data.append({'Category': col, 'Value': city_data[col].iloc[0], 'Type': city_sel})
    plot_data.append({'Category': col, 'Value': averages[col], 'Type': 'Average'})

# Convert list to DataFrame
plot_df = pd.DataFrame(plot_data)

# Create the bar chart
fig = px.bar(plot_df, x='Category', y='Value', color='Type', color_discrete_sequence=px.colors.qualitative.Pastel,
             barmode='group',
             title=f'Comparison of {city_sel} Cost of living with Average',
             labels={'Value': 'Value', 'Category': 'Category'})

# Display the bar chart in Streamlit
st.plotly_chart(fig)

other_columns = ['mcmeal', 'beer', 'salary_after_tax', 'utilities']
col1, col2, col3, col4 = st.columns(4, gap="small")

card1 = col1.container(border=True)
card2 = col2.container(border=True)
card3 = col3.container(border=True)
card4 = col4.container(border=True)

averages = cost_df[other_columns].mean()
with card1:
    st.metric(label=other_columns[0], 
              value=str(round(city_data[other_columns[0]].iloc[0],2))+"€",
              delta=str(round(-averages[other_columns[0]] + city_data[other_columns[0]].iloc[0],2))+"€",
              delta_color="inverse",
              help="Average : "+str(round(averages[other_columns[0]],2))+"€",
              )
with card2:    
    st.metric(label=other_columns[1], 
              value=str(round(city_data[other_columns[1]].iloc[0],2))+"€",
              delta=str(round(-averages[other_columns[1]] + city_data[other_columns[1]].iloc[0],2))+"€",
              delta_color="inverse",
              help="Average : "+str(round(averages[other_columns[1]],2))+"€",
    )
with card3:
    st.metric(label=other_columns[2], 
              value=str(round(city_data[other_columns[2]].iloc[0],2))+"€",
              delta=str(round(-averages[other_columns[2]] + city_data[other_columns[2]].iloc[0],2))+"€",  
              help="Average : "+str(round(averages[other_columns[2]],2))+"€",                
              )
with card4:
    st.metric(label=other_columns[3], 
              value=str(round(city_data[other_columns[3]].iloc[0],2))+"€",
              delta=str(round(-averages[other_columns[3]] + city_data[other_columns[3]].iloc[0],2))+"€",
              delta_color="inverse",
              help="Average : "+str(round(averages[other_columns[3]],2))+"€",
              )
              
st.divider()
st.header("Airbnb Prices vs Cost of Living")

st.subheader("Pearson, Spearman, and Kendall Correlation Analysis")

st.text("Pearson Correlation Coefficient - To check for linear relationships between Airbnb prices and multiple metrics of cost of living.")

st.text("Spearman Correlation Coefficient - To check for monotonic relationships between Airbnb prices and multiple metrics of cost of living.")

st.text("Kendall Correlation Coefficient - Similar to Spearman's, but especially useful for small sample sizes.")

corr = du.get_avg_correlation_metrics()
corr.sort_values(by='pearson', ascending=False, inplace=True)

fig = px.line(corr, x='category', y=['pearson', 'spearman', 'kendall'],
             title='Correlation Analysis',
             labels={'category': 'Category', 'value': 'Correlation Coefficient'})

# Display the bar chart in Streamlit
st.plotly_chart(fig)

st.subheader("Vizualization of Correlation - Rent for 3 Bedroom Apartments in suburbs")

fig = px.scatter(cost_df, x='rent_threebed_suburbs', y='avg_airbnb_price', color='city',
                 title='Vizualization of Correlation - Rent for 3 Bedroom Apartments in suburbs',
                 labels={'rent_threebed_suburbs': 'Rent for 3 Bedroom Apartments in suburbs', 'avg_airbnb_price': 'Average Airbnb Price'},
                 trendline="ols",
                 trendline_color_override="white",
                 trendline_scope="overall",
                 color_discrete_sequence=px.colors.qualitative.Pastel)

# Display the bar chart in Streamlit
st.plotly_chart(fig)

col1, col2, col3 = st.columns(3, gap="small")

card1 = col1.container(border=True)
card2 = col2.container(border=True)
card3 = col3.container(border=True)

with card1:
    st.metric(label="Pearson", value=str(round(corr.loc[corr['category'] == 'rent_threebed_suburbs', 'pearson'].iloc[0],3)))
with card2:
    st.metric(label="Spearman", value=str(round(corr.loc[corr['category'] == 'rent_threebed_suburbs', 'spearman'].iloc[0],3)))
with card3:
    st.metric(label="Kendall", value=str(round(corr.loc[corr['category'] == 'rent_threebed_suburbs', 'kendall'].iloc[0],3)))


st.subheader("Vizualization of Correlation - Rent for 1 Bedroom Apartments in center")

fig = px.scatter(cost_df, x='rent_onebed_center', y='avg_airbnb_price', color='city',
                 title='Vizualization of Correlation - Rent for 1 Bedroom Apartments in center',
                 labels={'rent_onebed_center': 'Rent for 1 Bedroom Apartments in center', 'avg_airbnb_price': 'Average Airbnb Price'},
                 trendline="ols",
                 trendline_color_override="white",
                 trendline_scope="overall",
                 color_discrete_sequence=px.colors.qualitative.Pastel)

# Display the bar chart in Streamlit
st.plotly_chart(fig)

col1, col2, col3 = st.columns(3, gap="small")

card1 = col1.container(border=True)
card2 = col2.container(border=True)
card3 = col3.container(border=True)

with card1:
    st.metric(label="Pearson", value=str(round(corr.loc[corr['category'] == 'rent_onebed_center', 'pearson'].iloc[0],3)))
with card2:
    st.metric(label="Spearman", value=str(round(corr.loc[corr['category'] == 'rent_onebed_center', 'spearman'].iloc[0],3)))
with card3:
    st.metric(label="Kendall", value=str(round(corr.loc[corr['category'] == 'rent_onebed_center', 'kendall'].iloc[0],3)))



st.subheader("In prespective:")

most_corr = cost_df[['city', 'rent_onebed_center', 'rent_threebed_suburbs','avg_airbnb_price']]

most_corr.sort_values(by='avg_airbnb_price', ascending=False, inplace=True)


fig = px.bar(most_corr, x='city', y=['rent_onebed_center', 'rent_threebed_suburbs','avg_airbnb_price'],
             barmode='group',
             title='In prespective',
             labels={'rent_onebed_center': 'Rent for 1 Bedroom Apartments in center', 'rent_threebed_suburbs': 'Rent for 3 Bedroom Apartments in suburbs', 'avg_airbnb_price': 'Average Airbnb Price'},
             color_discrete_sequence=px.colors.qualitative.Pastel)

# Display the bar chart in Streamlit
st.plotly_chart(fig)
