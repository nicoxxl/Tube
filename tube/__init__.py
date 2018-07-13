import functools
import inspect
import collections
from time import sleep

class Pipeline:
    def __init__(self, *f):
        self.funcs = list(f)
    
    def add(self, *f):
        self.funcs.extend(f)
    def do(self, data, funcs):
        for data in funcs[0](data):
            if len(funcs) > 1:
                self.do(data, funcs[1:])
            else:
                pass

    def __call__(self, data):
        self.do(data, tuple(self.funcs))
    

class Tube:
    def __init__(self):
        self.sources = set()
        self.processes = collections.defaultdict(list)
        self.running = False

    def process(self, sources, process):
        self.sources.update(sources)
        if isinstance(sources, (list, tuple)):
            process = Pipeline(*process)
        for src in sources:
            self.processes[src].append(process)
    
    def start(self):
        for src in self.sources:
            src.start()
    
    def do(self, stop_on_finished=False):
        self.running = True
        while self.running:
            done_stuff = self.step()
            if stop_on_finished and not done_stuff:
                return
            self.pause()
    
    def step(self):
        # print('.')
        done_stuff = False
        for src in self.sources:
            for data in src.get():
                for process in self.processes[src]:
                    process(data)
                done_stuff = True
        # print(done_stuff)
        return done_stuff
    
    def pause(self):
        '''
        Overidable method to avoid overloading the CPU.
        '''
        sleep(0.1)
    
    def stop(self):
        self.running = False
        for src in self.sources:
            src.stop()

def simple(f):
    @functools.wraps(f)
    def _(*a, **kw):
        yield f(*a, **kw)
    return _