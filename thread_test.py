import threading
import time

snowCnt = 0
eastCnt = 0


class FetchThread (threading.Thread):
    def __init__(self, name, counter):
        threading.Thread.__init__(self)
        self.name = name
        self.counter = counter

    def run(self):
        print("开始线程：" + self.name)
        print_time(self.name, self.counter, 5)
        print("\n退出线程：" + self.name)


def print_time(threadName, delay, counter):
    global snowCnt, eastCnt
    for i in range(10):
        time.sleep(0.3)
        snowCnt = snowCnt + 1
        eastCnt = eastCnt + 2
        print('\rSnowball:%d Eastmoney:%d' % (snowCnt, eastCnt), end='')


# 创建新线程
thread1 = FetchThread("Thread-snowball", 1)
thread2 = FetchThread("Thread-eastmoney", 2)


# 开启新线程
thread1.start()
thread2.start()
thread1.join()
thread2.join()

print("\n退出主线程")
