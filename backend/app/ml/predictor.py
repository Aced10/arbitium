from tensorflow.keras.models import load_model
import joblib
import numpy as np

model = load_model('model/arbitraje_model.h5')
scaler = joblib.load('model/scaler.pkl')

def predict_opportunity(buy_price, sell_price, profit_percent):
    features = np.array([[buy_price, sell_price, profit_percent]])
    X = scaler.transform(features)
    X = X.reshape((1, X.shape[0], X.shape[1]))
    prob = float(model.predict(X)[0][0])
    return prob