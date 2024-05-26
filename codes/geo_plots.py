import os
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np


def geo_plots(australia, drought_details_with_latlon, model_colors, time_scales, output_folder):
    # Plot wind farm locations on the map of Australia with different colors for different models
    fig, ax = plt.subplots(figsize=(10, 10))
    australia.plot(ax=ax, color='white', edgecolor='black')

    # Create GeoDataFrame with correct CRS
    geo_df = gpd.GeoDataFrame(drought_details_with_latlon, geometry=gpd.points_from_xy(
        drought_details_with_latlon['longitude'], drought_details_with_latlon['latitude']), crs="EPSG:4326")

    # Plot each model type with different colors and larger markers
    for model, color in model_colors.items():
        model_data = geo_df[geo_df['best_model'] == model]
        ax.scatter(
            model_data['longitude'], model_data['latitude'],
            label=model, s=100,  # Increase scatter size
            alpha=0.7
        )

    ax.set_title(
        'Wind Farm Locations with Best Fit Models in Southeast Australia')
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    ax.legend(title='Best Fit Model')
    ax.grid(True)

    plt.tight_layout()
    plt.savefig(os.path.join(output_folder, 'wind_farm_models.png'))

    # Prepare data for plot (Frequency and Duration)
    drought_details_with_latlon['Frequency'] = drought_details_with_latlon.groupby(
        'Windfarm')['Windfarm'].transform('count')
    drought_details_with_latlon['Duration'] = (
        drought_details_with_latlon['End'] - drought_details_with_latlon['Start']).dt.total_seconds() / (24 * 3600)

    # Add jitter to latitude and longitude to reduce overlap
    np.random.seed(0)  # for reproducibility
    drought_details_with_latlon['latitude_jitter'] = drought_details_with_latlon['latitude'] + \
        np.random.normal(0, 0.05, drought_details_with_latlon.shape[0])
    drought_details_with_latlon['longitude_jitter'] = drought_details_with_latlon['longitude'] + \
        np.random.normal(0, 0.05, drought_details_with_latlon.shape[0])

    # Create subplots for scatter plots for each time scale
    fig, axes = plt.subplots(nrows=2, ncols=4, figsize=(18, 8))
    axes = axes.flatten()

    for i, scale in enumerate(time_scales):
        if i >= len(axes):
            break
        ax = axes[i]
        australia.plot(ax=ax, color='white', edgecolor='black')

        scale_data = drought_details_with_latlon[drought_details_with_latlon['Scale'] == scale]
        scatter = ax.scatter(
            scale_data['longitude_jitter'], scale_data['latitude_jitter'],
            s=scale_data['Frequency'] * 0.5,  # Reduce size multiplier
            c=scale_data['Duration'],  # Duration represented by color
            cmap='coolwarm', alpha=1, edgecolors="w", linewidth=0.5
        )

        # Create a colorbar with the same colormap and normalization
        norm = plt.Normalize(
            scale_data['Duration'].min(), scale_data['Duration'].max())
        sm = plt.cm.ScalarMappable(cmap='coolwarm', norm=norm)
        sm.set_array([])
        cbar = plt.colorbar(sm, ax=ax)
        cbar.set_label('Drought Duration (Days)')

        ax.set_title(f'{scale} Droughts\n(Frequency and Duration)')
        ax.set_xlabel('Longitude')
        ax.set_ylabel('Latitude')
        ax.grid(True)

    # Remove unused subplots
    for j in range(i + 1, len(axes)):
        fig.delaxes(axes[j])

    # Adjust layout
    plt.tight_layout()
    plt.savefig(os.path.join(output_folder, 'wind_farm_scatter_by_scale.png'))
