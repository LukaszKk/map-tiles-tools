import multiprocessing.pool


'''
Internal class.
'''
class NoDaemonProcess(multiprocessing.Process):

    @property
    def daemon(self):
        return False

    @daemon.setter
    def daemon(self, val):
        pass


'''
Internal class.
'''
class NoDaemonProcessPool(multiprocessing.pool.Pool):

    def Process(self, *args, **kwds):
        proc = super(NoDaemonProcessPool, self).Process(*args, **kwds)
        proc.__class__ = NoDaemonProcess

        return proc
