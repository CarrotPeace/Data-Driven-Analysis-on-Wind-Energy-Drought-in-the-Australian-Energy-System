from temporal_analysis_plots import temporal_analysis_plots
from geo_plots import geo_plots

import pandas as pd
import matplotlib.pyplot as plt
import calendar
import numpy as np
import os
from dateutil import parser
import geopandas as gpd
import seaborn as sns


def read_drought_details_csv(windfarm_name, plots_directory):
    file_path = os.path.join(
        plots_directory, f'{windfarm_name}_drought_periods.csv')
    if os.path.exists(file_path):
        drought_details_df = pd.read_csv(file_path)
        drought_details_df['Start'] = drought_details_df['Start'].apply(
            parser.parse)
        drought_details_df['End'] = drought_details_df['End'].apply(
            parser.parse)
        return drought_details_df
    else:
        return None


def save_all_drought_details(windfarm_names, plots_directory, output_file):
    all_drought_details = []

    for windfarm_name in windfarm_names:
        drought_details_df = read_drought_details_csv(
            windfarm_name, plots_directory)
        if drought_details_df is not None:
            drought_details_df['Windfarm'] = windfarm_name
            all_drought_details.append(drought_details_df)

    if all_drought_details:
        combined_drought_details_df = pd.concat(
            all_drought_details, ignore_index=True)
        combined_drought_details_df.to_csv(output_file, index=False)
    else:
        print("No drought details found for the provided wind farms.")


plots_directory = './BARRA_DATA/Gen_Plots'
all_drought_file = './BARRA_DATA/all_drought_details.csv'

# Read the common windfarms from the file
common_windfarms_file = os.path.join(plots_directory, 'common_windfarms.txt')
with open(common_windfarms_file, 'r') as file:
    common_windfarms = file.read().splitlines()

save_all_drought_details(common_windfarms, plots_directory, all_drought_file)

# Load the data
drought_details = pd.read_csv('G:/BARRA_DATA/all_drought_details.csv')

# Convert Start and End columns to datetime
drought_details['Start'] = pd.to_datetime(
    drought_details['Start'], format='%Y-%m-%d %H:%M:%S')
drought_details['End'] = pd.to_datetime(
    drought_details['End'], format='%Y-%m-%d %H:%M:%S')

# Add columns for year, month, and season
drought_details['Year'] = drought_details['Start'].dt.year
drought_details['Month'] = drought_details['Start'].dt.month
drought_details['Season'] = drought_details['Start'].dt.month % 12 // 3 + 1

# Define scales and initialize drought data container
time_scales = ['1h', '4h', '12h', '1D', '2D', '3D', '5D']
all_drought_durations = {scale: {} for scale in time_scales}

# Load the model fit results and geographical data
wind_farm_model_latlon = pd.read_csv(
    './windfarms_model_lat_lon.csv')

# Merge drought details with wind farm locations
drought_details_with_latlon = drought_details.merge(wind_farm_model_latlon[[
    'windfarm', 'latitude', 'longitude', 'best_model']], left_on='Windfarm', right_on='windfarm', how='left')

# Geographical analysis
drought_details_with_latlon = drought_details_with_latlon.dropna(
    subset=['latitude', 'longitude'])

# Define colors for the different models
model_colors = {
    'weibull_min': '#e31a1c',
    'burr': '#1f78b4',
    'gengamma': '#33a02c'
}

# Define the scales to analyze
scales = drought_details['Scale'].unique()

# Separate the data by scale
drought_data_by_scale = {
    scale: drought_details[drought_details['Scale'] == scale] for scale in scales}

# Create a folder to save the plots
output_folder = 'G:/BARRA_DATA/plots'
os.makedirs(output_folder, exist_ok=True)

# Plot ECDF for drought durations by time scale
fig, ax = plt.subplots(figsize=(9, 4))

for scale in time_scales:
    scale_data = drought_details[drought_details['Scale'] == scale]
    sns.ecdfplot(data=scale_data, x='Duration', ax=ax, label=scale)

ax.set_xlabel('Drought Duration (days)')
ax.set_ylabel('Cumulative Probability')
ax.set_title('ECDF of Drought Durations by Time Scale')
ax.legend()
ax.grid(True)
plt.tight_layout()
plt.savefig(os.path.join(output_folder, 'ecdf_plot.png'))

#  Plot the temporal analysis plots
temporal_analysis_plots(all_drought_file, output_folder)


# Load the natural earth dataset from a local file
local_path = './ne_110m_admin_0_countries/ne_110m_admin_0_countries.shp'
australia = gpd.read_file(local_path)
australia = australia[australia.NAME == "Australia"]

geo_plots(australia, drought_details_with_latlon,
          model_colors, time_scales, output_folder)

# Ensuring all figures have appropriate labels, titles, grid, and layout settings
plt.rcParams.update({'font.size': 14})
