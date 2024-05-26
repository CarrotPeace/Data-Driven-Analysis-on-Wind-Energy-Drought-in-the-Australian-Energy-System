from wind_farm_parameters import get_wind_farm_names_from_params, get_wind_farm_param
from wind_speed_distr_model import fit_and_select_model
from wind_power_curve import wind_power_curve
from wind_drought_analysis import normalize_data, create_continuous_speed_series, calculate_srepi, calculate_drought_periods, split_data_on_gaps, process_data_with_moving_window

import os
import pandas as pd
import numpy as np
import glob
import matplotlib.pyplot as plt


wind_speed_path = './BARRA2_wind'
plots_directory = './Windfarms_analysis_plots'
if not os.path.exists(plots_directory):
    os.makedirs(plots_directory)
results_csv_path = os.path.join(plots_directory, 'model_fit_results.csv')
alpha = 0.1

windfarms_speed = [dir_name for dir_name in os.listdir(
    wind_speed_path) if dir_name[0].isupper()]

windfarms_params = get_wind_farm_names_from_params()

common_windfarms = list(set(windfarms_speed) & set(windfarms_params))
common_windfarms.sort()

print("Wind farms included in all datasets:", common_windfarms)
# save the common windfarms to a file
with open(os.path.join(plots_directory, 'common_windfarms.txt'), 'w') as f:
    for windfarm in common_windfarms:
        f.write(windfarm + '\n')

low_prod_threshold_list = {}
results = []
time_scales = ['1h', '4h', '12h', '1D', '2D', '3D', '5D']
window_sizes = {'1h': 1, '4h': 4, '12h': 12,
                '1D': 24, '2D': 48, '3D': 72, '5D': 120}
step_size = 1

all_drought_durations = {scale: {} for scale in time_scales}

for windfarm_name in common_windfarms:
    params = get_wind_farm_param(windfarm_name)
    if not params:
        print(f"Parameters not found for {windfarm_name}. Skipping...")
        continue
    V0, b, cut_in_speed, cut_out_speed, nameplate_power = params

    speed_files = glob.glob(os.path.join(
        wind_speed_path, windfarm_name, '*.csv'))
    df_speed = create_continuous_speed_series(speed_files, windfarm_name)

    df_wind_power_curve = wind_power_curve(
        df_speed, cut_in_speed, V0, b, cut_out_speed, nameplate_power)

    df_wind_power_curve.index = pd.to_datetime(df_wind_power_curve.index)
    df_wind_power_curve = df_wind_power_curve.sort_index()
    # Split data into segments based on gaps
    segments = split_data_on_gaps(df_wind_power_curve)

    # Fit the models, evaluate the best one for each windfarm and visualize the fit
    speed_data = df_speed['r100'].values
    best_model_info = fit_and_select_model(speed_data, windfarm_name)

    plt.figure(figsize=(10, 6))
    count, bins, ignored = plt.hist(
        speed_data, bins=50, density=True, alpha=0.6, color='g', label='Actual Data')
    xmin, xmax = plt.xlim()
    x = np.linspace(xmin, xmax, 100)
    model_func = globals()[best_model_info['Model Name']].pdf
    plt.plot(x, model_func(
        x, *best_model_info['Params']), 'r-', label=f'{best_model_info["Model Name"]} Fit')
    plt.xlabel('Wind Speed (m/s)')
    plt.ylabel('Density')
    plt.title(f'Wind Speed Distribution and Fit for {windfarm_name}')
    plt.legend()
    plt.savefig(os.path.join(plots_directory,
                f'{windfarm_name}_wind_speed_model_fit.png'))
    plt.close()

    params_str = ', '.join(map(str, best_model_info['Params']))
    results.append([windfarm_name, best_model_info['Model Name'],
                   params_str, best_model_info['AIC'], best_model_info['BIC']])
    df_results = pd.DataFrame(results, columns=[
                              'Windfarm', 'Best Fit Model', 'Params (as string)', 'AIC', 'BIC'])
    df_results.to_csv(results_csv_path, index=False)

    df_wind_power_curve['Normalized'] = normalize_data(
        df_wind_power_curve['Power'])

    drought_details_all_scales = []
    for scale in time_scales:
        all_drought_durations[scale][windfarm_name] = []

        window_size = window_sizes[scale]
        for segment in segments:
            if segment.empty:
                continue

            df_windowed = process_data_with_moving_window(
                segment, window_size, step_size)
            if df_windowed.empty:
                continue

            df_windowed_srepi = calculate_srepi(
                df_windowed.to_frame('Power'), 'Power')
            if df_windowed_srepi.empty:
                continue
            threshold = np.percentile(df_windowed_srepi, 10)

            # Calculate drought periods for each segment
            drought_periods = calculate_drought_periods(
                df_windowed_srepi, threshold)

            # Add drought details to the list
            for event in drought_periods:
                event_start = event[0].strftime('%Y-%m-%d %H:%M:%S')
                event_end = event[1].strftime('%Y-%m-%d %H:%M:%S')
                event_duration = (event[1] - event[0]).total_seconds() / 3600
                drought_details_all_scales.append(
                    [windfarm_name, scale, event_start, event_end, event_duration])

        # Visualize Drought Periods
        plt.figure(figsize=(10, 6))
        for segment in segments:
            if segment.empty:
                continue

            df_windowed = process_data_with_moving_window(
                segment, window_size, step_size)
            df_windowed_srepi = calculate_srepi(
                df_windowed.to_frame('Power'), 'Power')
            plt.plot(df_windowed_srepi.index, df_windowed_srepi, label='SREPI')

            for event in drought_periods:
                plt.axvspan(event[0], event[1], color='red', alpha=0.3)

        plt.axhline(y=threshold, color='black', linestyle='--',
                    label=f'10th Percentile Threshold ({threshold:.2f})')
        plt.xlabel('Date')
        plt.ylabel('SREPI')
        plt.title(f'SREPI for {windfarm_name} ({scale} Moving Window)')
        plt.legend()
        plt.tight_layout()
        plt.savefig(os.path.join(plots_directory,
                    f'{windfarm_name}_drought_periods_{scale}.png'))
        plt.close()

        drought_durations = [detail[4]
                             for detail in drought_details_all_scales]
        all_drought_durations[scale][windfarm_name].extend(drought_durations)

    drought_details_df = pd.DataFrame(drought_details_all_scales, columns=[
                                      'Windfarm', 'Scale', 'Start', 'End', 'Duration'])
    drought_details_df['Start'] = pd.to_datetime(drought_details_df['Start'])
    drought_details_df['End'] = pd.to_datetime(drought_details_df['End'])
    drought_details_df.to_csv(os.path.join(
        plots_directory, f'{windfarm_name}_drought_periods.csv'), index=False)
