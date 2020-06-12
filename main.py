import threading

THREAD_NUM = 2
INT_COUNT = 1000000

i = 0
lock = threading.Lock()


def test():
    global i
    for x in range(INT_COUNT):
        # with lock:
        #     i += 1
        i += 1


threads = [threading.Thread(target=test) for t in range(THREAD_NUM)]
for t in threads:
    t.start()

for t in threads:
    t.join()

print(i)
assert i == THREAD_NUM * INT_COUNT