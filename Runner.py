import SSide, CSide

class Runner(object):
    def __init__(self):
        self.sside = SSide.Server()
        self.cside = CSide.Client(5)
    
    def start(self):
        self.sside.set_peer(self.cside.i_port)
        self.cside.set_peer(self.sside.i_port)
        self.sside.start()
        self.cside.start()

runner = Runner()
runner.start()