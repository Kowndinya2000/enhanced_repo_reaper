import multiprocessing
import multiprocessing.pool


class NonDaemonicProcess(multiprocessing.Process):
    def _get_daemon(self):
        return False

    def _set_daemon(self, value):
        pass

    daemon = property(_get_daemon, _set_daemon)


class NonDaemonicProcessPool(multiprocessing.pool.Pool):
    Process = NonDaemonicProcess

# class NonDaemonicProcessPool(type(multiprocessing.get_context())):
#     Process = NonDaemonicProcess
# class MyPool(multiprocessing.pool.Pool):
#     def __init__(self,*args,**kwargs):
#         kwargs['context'] = NonDaemonicProcessPool()
#         super(MyPool,self).__init__(*args,**kwargs)

# class NonDaemonicProcessPool(multiprocessing.pool.Pool):
#     def Process(self, *args, **kwds):
#         proc = super(NonDaemonicProcessPool, self).Process(*args, **kwds)
# class NonDaemonicProcess(proc.__class__):
#     """Monkey-patch process to ensure it is never daemonized"""
#     #property
#     def daemon(self):
#         return False
#     #daemon.setter
#     def daemon(self, val):
#         pass
#         proc.__class__ = NonDaemonicProcess
        
# class NonDaemonicProcess(multiprocessing.Process):
#     #property
#     def daemon(self):
#         return False
#     #daemon.setter
#     def daemon(self, value):
#         pass
# class NonDaemonicProcessPool(type(multiprocessing.get_context())):
#     Process = NonDaemonicProcess
# # We sub-class multiprocessing.pool.Pool instead of multiprocessing.Pool
# # because the latter is only a wrapper function, not a proper class.
# class MyPool(multiprocessing.pool.Pool):
#     def __init__(self, *args, **kwargs):
#         kwargs['context'] = NonDaemonicProcessPool()
#         super(MyPool, self).__init__(*args, **kwargs)
# class NonDaemonicProcessPool(multiprocessing.pool.Pool):
#     def Process(self, *args, **kwds):
#         proc = super(NonDaemonicProcessPool, self).Process(*args, **kwds)

#         class NonDaemonicProcess(proc.__class__):
#             """Monkey-patch process to ensure it is never daemonized"""
#             def _get_daemon(self):
#                 return False
        
#             def _set_daemon(self, value):
#                 pass
#             daemon = property(_get_daemon, _set_daemon)

#         proc.__class__ = NonDaemonicProcess
#         return proc