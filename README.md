# AirBnB-Price-Analysis

Welcome to the AirBnB Price Analysis repository! This project aims to analyze Airbnb pricing trends and patterns using data analytics and visualization techniques.

## Introduction

This project is designed to perform a comprehensive analysis of Airbnb prices across various cities. The study aims to better comprehend if airbnb pricing can be a valid indicator for cost of living when compared with various other metrics.

## Installation

To get started with this project, you need to clone the repository and install the necessary dependencies:

pandas, numpy, matplotlib, plotly, seaborn, scikit-learn, streamlit, pyairbnb, json.

## Usage

The project consists of various scripts and notebooks for processing and analyzing data:

- EDA is the main notebook where the exploratory data analysis is happening, with many dataframe manipulations and quick vizualizations.
- airbnb_extractor.py uses the web scraper develped by https://github.com/johnbalvin/pyairbnb to extract information and save it as a json.
- cost_of_living_extractor.py uses the API https://rapidapi.com/ditno-ditno-default/api/cities-cost-of-living1 to extract varius metrics on cost of living for a given country/city.
- dashboard.py is a streamlit app developed to visualize all the work performed.

To run, open a terminal:

streamlit run dashboard.py

## Features
- Price trend analysis across multiple cities
- Correlation analysis of pricing with various economic indicators
- Interactive visualizations using libraries like Plotly
- Statistical analysis to determine significant factors affecting pricing


## Contributing

Contributions are welcome! If you are interested in improving this project, please fork this repository and submit a pull request with your proposed changes.

- Fork the repository
- Create a new branch (git checkout -b feature/YourFeature)
- Commit your changes (git commit -m 'Add some feature')
- Push to the branch (git push origin feature/YourFeature)
- Open a pull request

## Contact

For any questions, feel free to reach out:

Eduardo Parracho, eduardofilipe.parracho@gmail.com

