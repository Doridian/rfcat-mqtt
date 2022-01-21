from threading import Timer

from watchdog import watchdog_ping

def do_every(interval, worker_func, iterations = 0):
  if iterations != 1:
    Timer (
      interval,
      do_every, [interval, worker_func, 0 if iterations == 0 else iterations-1]
    ).start()

  worker_func()

def ping_every(interval, dev):
    def ping_func():
        try:
            dev.ping()
            watchdog_ping()
        except Exception as e:
            print(e)
            exit(1)

    do_every(interval, ping_func)
