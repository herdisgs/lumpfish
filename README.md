# Húnaflói Lumpfish Fisheries - Bycatch Analysis
This project is a Python Dash web application offering a visual analysis of bycatch in Húnaflói lumpfish fisheries, Iceland.

The application provides an interactive interface for exploring trends in the fisheries data. Users can select different variables and boats to generate a visual breakdown of the cumulative catch and bycatch by species.

You can visit the app online here: https://herdiss.pythonanywhere.com/

# Installation
The project relies on several Python packages including Dash, Dash Bootstrap Components, Plotly, and Pandas.

You can install these dependencies like this:

```sh
pip install dash dash-bootstrap-components plotly pandas
```

# Usage
To run the app, navigate to the project's directory and run the following command:

```sh
python app.py
```
Then open a web browser and navigate to http://127.0.0.1:8050/

# Data
The data used in this project includes the following datasets:

lump_data.csv - main fisheries data

birds.csv - data on bird bycatch

mammals.csv - data on mammal bycatch

parameter_names.txt - parameter names for the main fisheries data

# Contributions
The data was collected in collaboration with Icelandic lumpfish fishermen

# Author
Herdís G. R. Steinsdóttir

herdisgs@gmail.com
