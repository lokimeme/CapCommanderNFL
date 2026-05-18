import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
import joblib
import os
import logging
from typing import Dict

logger = logging.getLogger("CapCommanderML")

class AgingCurvePipeline:
    def __init__(self, model_path: str = "models/aging_curve.joblib"):
        self.model_path = model_path
        self.model = None
        self.feature_cols = ['age', 'position_enc', 'prev_epa', 'years_exp', 'is_qb']

    def _preprocess_data(self, df: pd.DataFrame) -> pd.DataFrame:
        pos_map = {p: i for i, p in enumerate(df['position'].unique())}
        df['position_enc'] = df['position'].map(pos_map)
        df['is_qb'] = (df['position'] == 'QB').astype(int)
        df['prev_epa'] = df['prev_epa'].fillna(0)
        return df

    def train_model(self, historical_data: pd.DataFrame):
        processed_df = self._preprocess_data(historical_data)
        X = processed_df[self.feature_cols]
        y = processed_df['next_year_epa']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        self.model = RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42)
        self.model.fit(X_train, y_train)
        preds = self.model.predict(X_test)
        if not os.path.exists("models"): os.makedirs("models")
        joblib.dump(self.model, self.model_path)

    def predict(self, player_data: Dict) -> float:
        if self.model is None:
            if os.path.exists(self.model_path): self.model = joblib.load(self.model_path)
            else: return player_data['prev_epa'] * 0.9
        input_df = pd.DataFrame([player_data])
        input_df = self._preprocess_data(input_df)
        prediction = self.model.predict(input_df[self.feature_cols])
        return float(prediction[0])

def generate_synthetic_training_data(n_samples: int = 1000) -> pd.DataFrame:
    np.random.seed(42)
    ages = np.random.randint(21, 40, n_samples)
    positions = np.random.choice(['QB', 'RB', 'WR', 'TE', 'OL', 'DL', 'LB', 'CB', 'S'], n_samples)
    prev_epa = np.random.normal(50, 20, n_samples)
    years_exp = ages - 21 + np.random.randint(0, 3, n_samples)
    next_epa = prev_epa * (1 - (ages - 25) * 0.05) + np.random.normal(0, 5, n_samples)
    return pd.DataFrame({
        'age': ages, 'position': positions, 'prev_epa': prev_epa,
        'years_exp': years_exp, 'next_year_epa': next_epa
    })
