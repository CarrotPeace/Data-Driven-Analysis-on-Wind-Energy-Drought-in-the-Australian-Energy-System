import os
import pandas as pd
from scipy.stats import norm


def map_month_to_season(month):
    seasons = {
        'Summer': [12, 1, 2],
        'Autumn': [3, 4, 5],
        'Winter': [6, 7, 8],
        'Spring': [9, 10, 11]
    }
    for season, months in seasons.items():
        if month in months:
            return season
    return None


def normalize_data(series):
    return (series - series.mean()) / series.std()


def create_continuous_speed_series(speed_files, windfarm_name):
    df_speed_all_years = pd.DataFrame()
    for file in speed_files:
        year = os.path.basename(file).split('_')[-1].split('.')[0]
        df_speed_yearly = pd.read_csv(file)
        df_speed_yearly.index = pd.date_range(
            start=f"{year}-01-01", periods=len(df_speed_yearly), freq="h")
        df_speed_all_years = pd.concat([df_speed_all_years, df_speed_yearly])
    df_speed_all_years['Windfarm'] = windfarm_name
    return df_speed_all_years


def calculate_srepi(df, column):
    df_sorted = df.sort_values(by=column)
    df_sorted['Rank'] = df_sorted[column].rank()
    df_sorted['SREPI'] = norm.ppf((df_sorted['Rank'] + 1) / (len(df) + 2))
    return df_sorted['SREPI']


# Function to calculate drought periods
def calculate_drought_periods(srepi_series, threshold, max_duration_days=15):
    srepi_series = srepi_series.sort_index()
    in_drought = False
    drought_start = None
    drought_periods = []

    for date, value in srepi_series.items():
        if value < threshold:
            if drought_start is None:
                drought_start = date
                in_drought = True
        else:
            if in_drought:
                in_drought = False
                drought_end = srepi_series.index[srepi_series.index.get_loc(
                    date) - 1]
                drought_duration = (drought_end - drought_start).days
                if drought_duration <= max_duration_days and drought_duration > 0:
                    drought_periods.append((drought_start, drought_end))
                drought_start = None

    if in_drought:
        drought_end = srepi_series.index[-1]
        drought_duration = (drought_end - drought_start).days
        if drought_duration <= max_duration_days and drought_duration > 0:
            drought_periods.append((drought_start, drought_end))

    return drought_periods


# Function to handle gaps in data and split into segments
def split_data_on_gaps(df, max_gap_hours=48):
    df = df.sort_index()
    gap_indices = df.index.to_series().diff() > pd.Timedelta(hours=max_gap_hours)
    split_points = gap_indices[gap_indices].index
    segments = []
    start_idx = df.index[0]
    for split_idx in split_points:
        segments.append(df[start_idx:split_idx])
        start_idx = split_idx
    segments.append(df[start_idx:])

    return segments


# Function to process data using moving window
def process_data_with_moving_window(df, window_size, step_size):
    window = df['Power'].rolling(window=window_size)
    df_windowed = window.mean().dropna().iloc[::step_size]
    return df_windowed
