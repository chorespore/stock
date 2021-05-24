import quandl
import numpy as np
import pandas as pd
import tensorflow as tf
from datetime import date
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.layers import Dense, Dropout, LSTM


start = date(2000, 10, 12)
end = date.today()
google_stock = pd.DataFrame(quandl.get("WIKI/GOOGL", start_date=start, end_date=end))
print(google_stock.shape)
google_stock.tail()
google_stock.head()

# 时间点长度
time_stamp = 50

# 划分训练集与验证集
google_stock = google_stock[['Open', 'High', 'Low', 'Close', 'Volume']]  # 'Volume'
train = google_stock[0:2800 + time_stamp]
valid = google_stock[2800 - time_stamp:]

# 归一化
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(train)
x_train, y_train = [], []


# 训练集
for i in range(time_stamp, len(train)):
    x_train.append(scaled_data[i - time_stamp:i])
    y_train.append(scaled_data[i, 3])

x_train, y_train = np.array(x_train), np.array(y_train)

# 验证集
scaled_data = scaler.fit_transform(valid)
x_valid, y_valid = [], []
for i in range(time_stamp, len(valid)):
    x_valid.append(scaled_data[i - time_stamp:i])
    y_valid.append(scaled_data[i, 3])

x_valid, y_valid = np.array(x_valid), np.array(y_valid)


# 超参数
epochs = 3
batch_size = 16
# LSTM 参数: return_sequences=True LSTM输出为一个序列。默认为False，输出一个值。
# input_dim： 输入单个样本特征值的维度
# input_length： 输入的时间点长度
model = tf.keras.Sequential()
model.add(LSTM(units=100, return_sequences=True, input_dim=x_train.shape[-1], input_length=x_train.shape[1]))
model.add(LSTM(units=50))
model.add(Dense(1))
model.compile(loss='mean_squared_error', optimizer='adam')
model.fit(x_train, y_train, epochs=epochs, batch_size=batch_size, verbose=1)

closing_price = model.predict(x_valid)
scaler.fit_transform(pd.DataFrame(valid['Close'].values))
# 反归一化
closing_price = scaler.inverse_transform(closing_price)
y_valid = scaler.inverse_transform([y_valid])
# print(y_valid)
# print(closing_price)
rms = np.sqrt(np.mean(np.power((y_valid - closing_price), 2)))
print(rms)
print(closing_price.shape)
print(y_valid.shape)

plt.figure(figsize=(16, 8))
dict_data = {
    'Predictions': closing_price.reshape(1, -1)[0],
    'Close': y_valid[0]
}
data_pd = pd.DataFrame(dict_data)

plt.plot(data_pd[['Close', 'Predictions']])
plt.show()
