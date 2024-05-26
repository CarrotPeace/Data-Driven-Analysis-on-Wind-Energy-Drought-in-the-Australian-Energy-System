import numpy as np


def wind_power_curve(df, cut_in_speed, V0, b, cut_out_speed, rated_power):
    df['q'] = rated_power / (1 + np.exp(-1 * b * (df['r100'] - V0)))
    df['Power'] = np.where((df['r100'] <= cut_in_speed) | (
        df['r100'] >= cut_out_speed), 0, df['q'])

    return df.drop(columns=['q'])
