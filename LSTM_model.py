import pandas as pd
import numpy as np
import get_prices as hist
import tensorflow as tf
from preprocessing import DataProcessing
import pandas_datareader.data as pdr
import fix_yahoo_finance as fix
from matplotlib import pyplot as plt
import tools
fix.pdr_override()

start = "2003-01-01"
end = "2018-01-01"

# hist.get_stock_data("AAPL", start_date=start, end_date=end)
process = DataProcessing("./snowball/stock_prices.csv", 0.9)
process.gen_test(10)
process.gen_train(10)


def train():

    X_train = (process.X_train.reshape((int(len(process.X_train)), 10, 1)) + 10.1) / 20.2
    Y_train = (process.Y_train + 10.1) / 20.2

    X_test = (process.X_test.reshape((int(len(process.X_test))), 10, 1) + 10.1) / 20.2
    Y_test = (process.Y_test + 10.1) / 20.2
    model = tf.keras.Sequential()
    model.add(tf.keras.layers.LSTM(20, input_shape=(10, 1), return_sequences=True))
    model.add(tf.keras.layers.LSTM(20))
    model.add(tf.keras.layers.Dense(1, activation=tf.nn.relu))

    model.compile(optimizer="adam", loss="mean_squared_error")

    # model.fit(X_train, Y_train, epochs=50)

    history = model.fit(X_train, Y_train, epochs=50, batch_size=100, validation_data=(X_test, Y_test), verbose=2, shuffle=False)

    # 绘制损失图
    plt.plot(history.history['loss'], label='train')
    plt.plot(history.history['val_loss'], label='test')
    plt.title('LSTM_600000.SH', fontsize='12')
    plt.ylabel('loss', fontsize='10')
    plt.xlabel('epoch', fontsize='10')
    plt.legend()
    plt.show()

    model.save('./snowball/model.h5')


def test():
    model = tf.keras.models.load_model('./snowball/model.h5')
    data = tools.loadCSV('./snowball/stock_prices.csv')
    begin = 6935
    stock = np.array(data.iloc[begin:begin + 10, 1])
    print(np.array(stock).reshape((1, 10, 1)))
    X_predict = (np.array(stock).reshape((1, 10, 1)) + 10.1) / 20.2
    # print(np.array(X_predict))
    print('res', model.predict(X_predict) * 20.2 - 10.1)

# If instead of a full backtest, you just want to see how accurate the model is for a particular prediction, run this:
# data = pdr.get_data_yahoo("AAPL", "2017-12-19", "2018-01-03")
# stock = data["Adj Close"]
# X_predict = np.array(stock).reshape((1, 10)) / 200
# print(model.predict(X_predict)*200)


if __name__ == '__main__':
    # train()
    test()
