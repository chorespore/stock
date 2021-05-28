import quandl
import csv
import numpy as np
import pandas as pd
import tensorflow as tf
from datetime import date
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.layers import Dense, Dropout, LSTM


# 时间点长度
time_span = 30
start = date(2000, 10, 12)
end = date.today()
tmp_lst = []
with open('./snowball/SZ000001.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        tmp_lst.append(row)
stock_quotes = pd.DataFrame(tmp_lst[1:], columns=tmp_lst[0])
# print(stock_quotes.shape)
# print(stock_quotes.head())
# print(stock_quotes.tail())


# 划分训练集与验证集
# stock_quotes = stock_quotes[['open', 'high', 'low', 'close', 'dollar_volume']]
stock_quotes = stock_quotes[['open', 'high', 'low', 'close']]
stock_quotes = pd.DataFrame(stock_quotes, dtype=np.float)
train = stock_quotes[0:4200 + time_span]
valid = stock_quotes[4200 - time_span:]

# 归一化
scaler = MinMaxScaler(feature_range=(0, 1))
# scaled_data = scaler.fit_transform(train)
scaled_data = np.array(train)
x_train, y_train = [], []


# 训练集
for i in range(time_span, len(train)):
    x_train.append(scaled_data[i - time_span:i])
    res = 0 if scaled_data[i, 3] <= 0.5 else 1
    y_train.append(res)
    # print(scaled_data[i, 3], res)

x_train, y_train = np.array(x_train), np.array(y_train)


# 验证集
# scaled_data = scaler.fit_transform(valid)
scaled_data = np.array(valid)
x_valid, y_valid = [], []
for i in range(time_span, len(valid)):
    x_valid.append(scaled_data[i - time_span:i])
    res = 0 if scaled_data[i, 3] <= 0.5 else 1
    y_valid.append(res)

x_valid, y_valid = np.array(x_valid), np.array(y_valid)
print(y_train)
print(y_valid)


def convert():
    tmp_lst = []
    with open('./snowball/000001.SZ.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            tmp_lst.append(row)
    stock_quotes = pd.DataFrame(tmp_lst[-1:2:-1], columns=tmp_lst[0])
    for i, row in stock_quotes.iterrows():
        row['open'] = convert_field(row['open'], row['pre_close'])
        row['high'] = convert_field(row['high'], row['pre_close'])
        row['low'] = convert_field(row['low'], row['pre_close'])
        row['close'] = convert_field(row['close'], row['pre_close'])
    stock_quotes.to_csv('./snowball/SZ000001.csv', index=False)


def convert_field(target, anchor):
    res = ((float(target) - float(anchor)) / float(anchor) * 10 + 1) / 2
    if res < 0:
        return 0.0
    elif res > 1:
        return 1.0
    return res


def train():
    # 超参数
    epochs = 3
    batch_size = 16
    # LSTM 参数: return_sequences=True LSTM输出为一个序列。默认为False，输出一个值。
    # input_dim： 输入单个样本特征值的维度
    # input_length： 输入的时间点长度
    model = tf.keras.Sequential()
    print('input_dim:', x_train.shape[-1], 'input_length:', x_train.shape[1])
    model.add(LSTM(units=100, return_sequences=True, input_dim=x_train.shape[-1], input_length=x_train.shape[1]))
    model.add(LSTM(units=50))
    model.add(Dense(1))
    model.compile(loss='mean_squared_error', optimizer='adam')
    model.fit(x_train, y_train, epochs=epochs, batch_size=batch_size, verbose=1)
    model.save('./snowball/model_LSTM.h5')


def train_sigmoid():
    # 超参数
    epochs = 100
    batch_size = 32
    # LSTM 参数: return_sequences=True LSTM输出为一个序列。默认为False，输出一个值。
    # input_dim： 输入单个样本特征值的维度
    # input_length： 输入的时间点长度
    model = tf.keras.Sequential()
    print('input_dim:', x_train.shape[-1], 'input_length:', x_train.shape[1])
    model.add(LSTM(units=128, activation='relu', return_sequences=True, input_dim=x_train.shape[-1], input_length=x_train.shape[1]))
    model.add(Dropout(0.4))
    model.add(LSTM(units=64, activation='relu'))
    model.add(Dropout(0.4))
    model.add(Dense(1, activation='sigmoid'))

    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    hist = model.fit(x_train, y_train, epochs=epochs, batch_size=batch_size, verbose=1)
    model.save('./snowball/model_LSTM.h5')
    plt.plot(hist.history['loss'], label='loss')
    plt.plot(hist.history['accuracy'], label='acc')
    plt.legend()
    plt.show()


def test():
    global y_valid
    model = tf.keras.models.load_model('./snowball/model_LSTM.h5')
    closing_price = model.predict(x_valid)
    print(closing_price)
    print(y_valid)
    # scaler.fit_transform(pd.DataFrame(valid['Close'].values))
    scaler.fit_transform(pd.DataFrame(valid['close'].values))
    # 反归一化
    # closing_price = scaler.inverse_transform(closing_price)
    # y_valid = scaler.inverse_transform([y_valid])
    # print(y_valid)
    # print(closing_price)
    rms = np.sqrt(np.mean(np.power((y_valid - closing_price), 2)))
    print(rms)
    print(closing_price.shape)
    print(y_valid.shape)

    plt.figure(figsize=(16, 8))
    dict_data = {
        'Predictions': closing_price.reshape(1, -1)[0],
        'Close': y_valid
    }
    prediction = []
    for i in closing_price.reshape(1, -1)[0]:
        prediction.append(0 if i <= 0.5 else 1)
    print(dict_data)
    data_pd = pd.DataFrame(dict_data)
    correct = 0
    for i in range(len(y_valid)):
        print(y_valid[i], prediction[i])
        if y_valid[i] == prediction[i]:
            correct = correct + 1
    print(len(y_valid), correct, format(correct / len(y_valid), '.2f') + '%')

    # plt.plot(data_pd[['Close', 'Predictions']])
    # plt.plot([y_valid, prediction])
    # plt.show()


if __name__ == '__main__':
    # convert()
    train_sigmoid()
    # test()
    print('ok')
