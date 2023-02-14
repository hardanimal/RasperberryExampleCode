import threading

class _Timer(threading.Thread):
    """Call a function after a specified number of seconds:
            t = Timer(30.0, f, args=[], kwargs={})
            t.start()
            t.cancel() # stop the timer's action if it's still waiting
    """

    def __init__(self, interval, function, args=[], kwargs={}):
        Thread.__init__(self)
        self.interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.finished = Event()

    def cancel(self):
        """Stop the timer if it hasn't finished yet"""
        self.finished.set()

    def run(self):
        self.finished.wait(self.interval)
        if not self.finished.is_set():
            self.function(*self.args, **self.kwargs)
        self.finished.set()
        
        
def hello():
    print("hello world!")
    
    
t = _Timer(1000, hello)
t.start