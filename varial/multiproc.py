"""
Management for multiprocessing in varial.
"""


import multiprocessing.pool

import settings


_manager = None
_cpu_sema = None
_kill_request = None  # initialized to 0, if > 0, the process group is killed
_xcptn_lock = None  # used w/o blocking for _kill_request


################################### special worker-pool to allows recursion ###
class _NoDaemonProcess(multiprocessing.Process):
    # make 'daemon' attribute always return False
    def _get_daemon(self):
        return False

    def _set_daemon(self, value):
        pass
    daemon = property(_get_daemon, _set_daemon)

    def run(self):
        try:
            super(_NoDaemonProcess, self).run()
        except (KeyboardInterrupt, IOError):
            exit(-1)


class NoDeamonWorkersPool(multiprocessing.pool.Pool):
    Process = _NoDaemonProcess

    def __init__(self, *args, **kws):
        global _manager, _cpu_sema, _kill_request, _xcptn_lock
        super(NoDeamonWorkersPool, self).__init__(*args, **kws)

        # prepare parallelism (only once for the all processes)
        if not _cpu_sema:
            _manager = multiprocessing.Manager()
            _cpu_sema = _manager.BoundedSemaphore(settings.max_num_processes)
            _kill_request = _manager.Value('i', 0)
            _xcptn_lock = _manager.RLock()
        else:
            _manager = None

    def __del__(self):
        global _manager, _cpu_sema, _kill_request, _xcptn_lock
        _manager = None
        _cpu_sema = None
        _kill_request = None
        _xcptn_lock = None


###################################################### task synchronization ###
def is_kill_requested(request_kill_now=False):
    if request_kill_now:
        if (not _kill_request.value) and _xcptn_lock.acquire(blocking=False):
            _kill_request.value = 1
            _xcptn_lock.release()
            return False
    return bool(_kill_request.value)


def acquire_processing():
    if not _cpu_sema:
        return

    _cpu_sema.acquire()


def release_processing():
    if not _cpu_sema:
        return

    _cpu_sema.release()


