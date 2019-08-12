""" 协程的官方文档 """
# import random
# def begin_game():
#     while True:
#         url = yield "The game is beginning"
#         print("your option is: {}".format(url))
#
# def action_game(fun):
#     for i in range(50):
#         key = random.randint(1,50)
#         fun.send(key)
#         print("="*30)
#
# if __name__ == '__main__':
#     fun = begin_game()
#     print(next(fun))
#     action_game(fun)

""" gevent的简单使用 """
import gevent
from gevent.lock import Semaphore

sem = Semaphore(2)

def fun1():
    for i in range(5):
        # sem.acquire()
        print("fun1 is %s"%i)
        gevent.sleep(2)
        # sem.release()

def fun2():
    for i in range(5):
        # sem.acquire()
        print("fun2 is %s"%i)
        gevent.sleep(1)
        # sem.release()

t1 = gevent.spawn(fun1)
t2 = gevent.spawn(fun2)

gevent.joinall([t1, t2])