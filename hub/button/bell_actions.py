"""
Blind actions for bell

"""


class BellAction(object):
    def run(self, signal):
        print('RING BELL!!!!')
        return True
