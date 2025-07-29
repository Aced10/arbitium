import asyncio
import pandas as pd
from app.core.db import db
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from sklearn.preprocessing import MinMaxScaler
import joblib

async def load_data():
    cursor = db.opportunities.find({})
    data = await cursor.to_list(length=None)
    return pd.DataFrame(data)

def prepare_dataset(df, threshold=0.5):
    df = df.dropna(subset=["buy_price","sell_price","profit_percent"])
    features = df[["buy_price","sell_price","profit_percent"]].values
    scaler = MinMaxScaler()
    X = scaler.fit_transform(features)
    y = (df["profit_percent"] > threshold).astype(int).values
    X = X.reshape((X.shape[0], 1, X.shape[1]))
    joblib.dump(scaler, 'model/scaler.pkl')
    return X, y

def build_model(input_shape):
    model = Sequential()
    model.add(LSTM(64, input_shape=input_shape))
    model.add(Dense(1, activation='sigmoid'))
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    return model

async def train_and_save():
    df = await load_data()
    X, y = prepare_dataset(df)
    model = build_model((X.shape[1], X.shape[2]))
    model.fit(X, y, epochs=10, batch_size=32)
    model.save('model/arbitraje_model.h5')

if __name__ == '__main__':
    asyncio.run(train_and_save())