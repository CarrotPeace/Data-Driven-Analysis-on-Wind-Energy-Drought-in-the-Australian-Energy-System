from scipy.stats import weibull_min, burr, gengamma
import numpy as np

models = {
    'weibull_min': weibull_min,
    'burr': burr,
    'gengamma': gengamma
}


def calculate_aic(n, log_likelihood, k):
    return 2 * k - 2 * log_likelihood


def calculate_bic(n, log_likelihood, k):
    return np.log(n) * k - 2 * log_likelihood


def fit_and_select_model(generation_data, windfarm_name):
    best_model_info = {'Model Name': None,
                       'Params': None, 'AIC': np.inf, 'BIC': np.inf}
    n = len(generation_data)

    for model_name, model in models.items():
        try:
            params = model.fit(
                generation_data, floc=0) if model_name == 'weibull_min' else model.fit(generation_data)
            pdf = model.pdf
            log_likelihood = np.sum(np.log(pdf(generation_data, *params)))
            aic = 2 * len(params) - 2 * log_likelihood
            bic = np.log(n) * len(params) - 2 * log_likelihood

            if aic < best_model_info['AIC']:
                best_model_info.update(
                    {'Model Name': model_name, 'Params': params, 'AIC': aic, 'BIC': bic})
        except Exception as e:
            print(f"Error fitting {model_name} for {windfarm_name}: {e}")

    return best_model_info
