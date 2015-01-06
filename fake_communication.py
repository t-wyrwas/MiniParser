import time


class FakeSerialSource:

    def __init__(self, logs):
        self._logs = logs
        self._run = True

    def run(self):
        d = 0
        while True:
            if self._run == False:
                print "Fake -> stop!"
                break
            if d == 2:
                d = 0
            time.sleep(1)
            if d == 0:
                self._logs.append("one of many not relevant logs")
            if d == 1:
                self._logs.append("TEST_SIG---> log")
            d += 1
            print "Fake -> dump's length: ", len(self._logs)

    def stop(self):
        self._run = False