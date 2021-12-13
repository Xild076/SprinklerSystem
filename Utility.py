import enum, datetime
import socket, pickle, threading


class Comm(object):
    def __init__(self, signature):
        self.signature = signature
        self.logger = Logger(print=True)
        self.i_socket, self.i_host, self.i_port = self.new_socket()
        self.e_socket, self.e_host, self.e_port = socket.socket(socket.AF_INET, socket.SOCK_STREAM), None, None
        self.operations = {"i": [threading.Lock(), list()], "e": [threading.Lock(), list()]}
        self.saved_data = list()
        self.task = None
        self.update = None
        self.threadpool = list()

    def export_data(self, value):
        self.logger.log(self.signature, "Data appended to Export", Logger.LogType.DEBUG)
        self.operations.get("e")[1].append(value)

    def receive_data(self):
        self.logger.log(self.signature, "Function: receive_data", Logger.LogType.STARTUP)
        while True:
            self.i_socket.listen(5)
            conn, address = self.i_socket.accept()
            with conn:
                while True:
                    data = conn.recv(8192)
                    if data:
                        self.operations.get("i")[0].acquire()
                        loaded_data = pickle.loads(data)
                        list_max(self.saved_data, 100, loaded_data)
                        self.operations.get("i")[1].append(loaded_data)
                        self.operations.get("i")[0].release()
                    else:
                        pass
    
    def sending_data(self):
        self.logger.log(self.signature, "Function: export_data", Logger.LogType.STARTUP)
        while True:
            data = None
            self.operations.get("e")[0].acquire()
            if self.operations.get("e")[1]:
                data = pickle.dumps(self.operations.get("e")[1].pop(0))
            self.operations.get("e")[0].release()
            if data:
                try:
                    self.e_socket.connect((self.e_host, self.e_port))
                    self.e_socket.sendall(data)
                except Exception as ee:
                    pass
    
    def run_task(self):
        self.logger.log(self.signature, "Function: run_task", Logger.LogType.STARTUP)
        while True:
            if self.task != None:
                data = None
                self.operations.get("i")[0].acquire()
                if self.operations.get("i")[1]:
                    self.operations.get("i")[1].pop(0)
                self.operations.get("i")[0].release()
                if data:
                    self.task(data, self.operations.get("e")[1])
    
    def run_update(self):
        self.logger.log(self.signature, "Function: run_update", Logger.LogType.STARTUP)
        while True:
            if self.update != None:
                self.update(self.saved_data[-1], self.operations.get("e")[1])
    
    def set_peer(self, port_id):
        self.logger.log(self.signature, "Setting peer", Logger.LogType.STARTUP)
        self.e_port = port_id

    def new_socket(self):
        self.logger.log(self.signature, "Creating new socket", Logger.LogType.DEBUG)
        ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ss.bind((socket.gethostname(), 0))
        host, port = ss.getsockname()[0], ss.getsockname()[1]
        return ss, host, port

    def start(self):
        self.logger.log(self.signature, f"Running on {self.e_host} with exporting port {self.e_port} and in port {self.i_port}", Logger.LogType.STARTUP)
        self.threadpool.append(threading.Thread(target=self.receive_data))
        self.threadpool.append(threading.Thread(target=self.sending_data))
        self.threadpool.append(threading.Thread(target=self.run_task))
        self.threadpool.append(threading.Thread(target=self.run_update))
        for threads in self.threadpool:
            threads.start()


class Holder(object):
    class MSGType(enum.Enum):
        REQUEST = 0,
        COMMAND = 1,
        UPDATE = 2,
        KILL = 3
    
    class RequestType(enum.Enum): #Use as update type
        VALVE_AMOUNT = 0,
        VALVE_STATUS = 1
    
    class CommandHolder(object):
        def __init__(self, valve_number, valve_value):
            self.valve_number = valve_number
            self.valve_value = valve_value #On/Off value
    
    class UpdateHolder(object):
        def __init__(self, request_type, data):
            self.request_type = request_type
            self.data = data
    
    def __init__(self, msg_type=MSGType.KILL, msg_value=None):
        self.msg_type = msg_type
        self.msg_value = msg_value


class Logger(object):
    
    class LogType(enum.Enum):
        CLEAR = 0,
        DEBUG = 1,
        ERROR = 2,
        STARTUP = 3
    
    def __init__(self, file="log.txt", print=False):
        self.file = file
        self.print = print
    
    def log(self, signature, msg, log_type):
        file = open(self.file, "a")
        text = ""
        if log_type == Logger.LogType.CLEAR:
            text += "  ------  "
        else:
            if log_type == Logger.LogType.DEBUG:
                text += "DEBUG -- "
            elif log_type == Logger.LogType.ERROR:
                text += "ERROR -- "
            elif log_type == Logger.LogType.STARTUP:
                text += "STARTUP -- "
            text += signature
            text += " ["
            text += datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S.%f')
            text += "]: "
            text += msg

        if self.print:
            print(text)
        
        text += "\n"
        file.write(text)
        file.close()


def set_vals_dict(dictionary, key, value=None):
    dictionary[key] = value


def list_max(given_list, max_value, data):
    if len(given_list) >= max_value:
        given_list.pop(0)
    given_list.append(data)


def input_check(possible_dict):
    possible_list = list(possible_dict)
    question = "Please enter your choice ("
    for items in possible_list:
        question += str(items) + ": " + possible_dict.get(items) + ", "
    question += ")"
    while True:
        print(question)
        intake = input()
        try:
            intake = int(intake)
            if intake in possible_list:
                pass
            else:
                int("HILLO")
            return intake
        except:
            print("Please input a valid input.")