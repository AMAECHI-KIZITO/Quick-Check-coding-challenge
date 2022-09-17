import schedule
import time

def vvv():
    print('ok')

schedule.every(10).seconds.do(vvv)
