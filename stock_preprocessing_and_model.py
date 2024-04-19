import datetime
import numpy as np
import pandas as pd
import yfinance as yf
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import TimeSeriesSplit
from keras.models import Sequential
from keras.layers import Dense,LSTM
import matplotlib.pyplot as plt


def data_download(ticker):
    end_date = datetime.datetime.now().date()
    start_date = end_date - datetime.timedelta(days=365*10)
    data = yf.download(ticker, start=start_date, end=end_date)
    return data


def adding_parameter(data):

    data['Date']=pd.to_datetime(data['Date'])

    data['Yesterday_Close'] = data['Adj Close'].shift(1)
    data['Tomorrow_Close'] = data['Adj Close'].shift(-1)

    data['10-day SMA'] = data['Adj Close'].rolling(window=10).mean()
    data['20-day SMA'] = data['Adj Close'].rolling(window=20).mean()
    data['50-day SMA'] = data['Adj Close'].rolling(window=50).mean()

    data['12-day EMA'] = data['Adj Close'].ewm(span=12, adjust=False).mean()
    data['26-day EMA'] = data['Adj Close'].ewm(span=26, adjust=False).mean()
    data['50-day EMA'] = data['Adj Close'].ewm(span=50, adjust=False).mean()

    data.dropna(inplace=True)

    return data


def preprocess(data):
    features = ['Open', 'High', 'Low', 'Volume', 'Adj Close', 'Yesterday_Close',
            '10-day SMA', '20-day SMA', '50-day SMA', '12-day EMA', '26-day EMA', '50-day EMA']
    
    data['Tomorrow Price'] = data['Adj Close'].shift(-1)

    scaler = MinMaxScaler()
    feature_transform = scaler.fit_transform(data[features])
    feature_transform = pd.DataFrame(columns=features, data=feature_transform, index=data.index)

    timesplit = TimeSeriesSplit(n_splits=5)
    for train_index, test_index in timesplit.split(feature_transform):
        X_train, X_test = feature_transform[:len(train_index)], feature_transform[len(train_index):(len(train_index) + len(test_index))]
        y_train, y_test = data['Tomorrow Price'][:len(train_index)].values.ravel(), data['Tomorrow Price'][len(train_index):(len(train_index) + len(test_index))].values.ravel()

    trainX = np.array(X_train)
    testX = np.array(X_test)
    X_train = trainX.reshape(X_train.shape[0],1, X_train.shape[1])
    X_test = testX.reshape(X_test.shape[0],1, X_test.shape[1])

    return X_train,y_train,X_test,y_test


def model_training(X_train,y_train):

    model=Sequential()

    model.add(LSTM(128, input_shape=(1,X_train.shape[2]), activation='relu', return_sequences=True))
    model.add(LSTM(64, activation='relu', return_sequences=True))
    model.add(LSTM(32, activation='relu', return_sequences=True))
    model.add(LSTM(16, activation='relu', return_sequences=True))
    model.add(LSTM(8, activation='relu', return_sequences=False))  
    model.add(Dense(1))


    model.compile(loss='mean_squared_error', optimizer='adam')
    history = model.fit(X_train, y_train, epochs=10, batch_size=8, verbose=1, shuffle=False)

    return model


def pipeline(ticker):
    data=data_download(ticker)
    X_train,y_train,X_test,y_test=preprocess(data)
    model=model_training(X_train,y_train,X_test,y_test)
    return model
