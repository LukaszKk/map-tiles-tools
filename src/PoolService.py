import multiprocessing as mp


'''
UNUSED.
'''
class PoolService:

    def __init__(self):
        self.pool = mp.Pool(mp.cpu_count())

    def run_async(self, func):
        self.pool.apply_async(func)

    def close(self, func=None):
        # func()
        self.pool.close()
        self.pool.terminate()

    def __getstate__(self):
        self_dict = self.__dict__.copy()
        del self_dict['pool']
        return self_dict

    def __setstate__(self, state):
        self.__dict__.update(state)
