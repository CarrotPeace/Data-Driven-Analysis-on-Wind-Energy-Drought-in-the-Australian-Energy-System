import os
import pandas as pd
import matplotlib.pyplot as plt
import calendar


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


def temporal_analysis_plots(all_drought_file, output_folder):
    fontsize = 14
    drought_details = pd.read_csv(all_drought_file)
    drought_details['Start'] = pd.to_datetime(drought_details['Start'])
    time_scales = ['1h', '4h', '12h', '1D', '2D', '3D', '5D']
    seasons = ['Spring', 'Summer', 'Autumn', 'Winter']

    fig, axes = plt.subplots(2, 4, figsize=(18, 8))
    axes = axes.flatten()

    for i, scale in enumerate(time_scales):
        ax = axes[i]
        drought_details_scale = drought_details[drought_details['Scale'] == scale]
        drought_details_scale.loc[:,
                                  'Year'] = drought_details_scale['Start'].dt.year
        annual_counts = drought_details_scale.groupby('Year').size()

        annual_counts.plot(kind='bar', ax=ax, color='#2ca02c',
                           edgecolor='black', title=f'Annual Wind Drought Events ({scale})')
        ax.set_title(
            f'Annual Wind Drought Events ({scale})', fontsize=fontsize)
        ax.set_xlabel('Year', fontsize=fontsize)
        ax.set_ylabel('Number of Events', fontsize=fontsize)
        ax.tick_params(axis='both', which='major', labelsize=fontsize)
        ax.grid(True)

    # Remove any unused subplots
    for j in range(len(time_scales), len(axes)):
        fig.delaxes(axes[j])

    plt.tight_layout()
    plt.savefig(os.path.join(output_folder, 'annual_trends.png'))

    fig, axes = plt.subplots(2, 4, figsize=(18, 8))
    axes = axes.flatten()

    for i, scale in enumerate(time_scales):
        ax = axes[i]
        drought_details_scale = drought_details[drought_details['Scale'] == scale]
        drought_details_scale.loc[:,
                                  'Month'] = drought_details_scale['Start'].dt.month
        monthly_counts = drought_details_scale.groupby('Month').size()

        monthly_counts.index = [calendar.month_abbr[i]
                                for i in monthly_counts.index]
        monthly_counts.plot(kind='bar', ax=ax, color='#1f77b4',
                            edgecolor='black', title=f'Monthly Wind Drought Events ({scale})')
        ax.set_title(
            f'Monthly Wind Drought Events ({scale})', fontsize=fontsize)
        ax.set_xlabel('Month', fontsize=fontsize)
        ax.set_ylabel('Number of Events', fontsize=fontsize)
        ax.tick_params(axis='both', which='major', labelsize=fontsize)
        ax.grid(True)

    # Remove any unused subplots
    for j in range(len(time_scales), len(axes)):
        fig.delaxes(axes[j])

    plt.tight_layout()
    plt.savefig(os.path.join(output_folder, 'monthly_trends.png'))

    fig, axes = plt.subplots(2, 4, figsize=(18, 8))
    axes = axes.flatten()

    for i, scale in enumerate(time_scales):
        ax = axes[i]
        drought_details_scale = drought_details[drought_details['Scale'] == scale]
        drought_details_scale.loc[:,
                                  'Season'] = drought_details_scale['Start'].dt.month % 12 // 3 + 1
        seasonal_counts = drought_details_scale.groupby('Season').size()

        seasonal_counts.plot(kind='bar', ax=ax, color='#ff7f0e',
                             edgecolor='black', title=f'Seasonal Wind Drought Events ({scale})')
        ax.set_title(
            f'Seasonal Wind Drought Events ({scale})', fontsize=fontsize)
        ax.set_xlabel('Season', fontsize=fontsize)
        ax.set_ylabel('Number of Events', fontsize=fontsize)
        ax.tick_params(axis='both', which='major', labelsize=fontsize)
        ax.set_xticklabels(['Spring', 'Summer', 'Autumn', 'Winter'])
        ax.grid(True)

    # Remove any unused subplots
    for j in range(len(time_scales), len(axes)):
        fig.delaxes(axes[j])

    plt.tight_layout()
    plt.savefig(os.path.join(output_folder, 'seasonal_trends.png'))
