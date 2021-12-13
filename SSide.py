#Server Side

from Utility import Comm, input_check
from Utility import Holder, Holder


class Server(Comm):
    def __init__(self):
        super().__init__("Server")
        self.valve_amount = None
        self.export_data(Holder(Holder.MSGType.REQUEST, Holder.RequestType.VALVE_AMOUNT))
        self.wfu = False #Waiting for status update
    
    def update(self, saved_data, export_list):
        if self.valve_amount != None:
            pass
        else:
            intake = input_check({0: "Command", 1: "Request update", 2: "Kill"})
            if intake == 0:
                what_valve = input_check({{key: str(key) for key in range(self.valve_amount)}})
                what_value = input_check({True: "On", False: "Off"})
                self.export_data(Holder(Holder.MSGType.COMMAND, Holder.CommandHolder(what_valve, what_value)))
            if intake == 1:
                self.export_data(Holder(Holder.MSGType.REQUEST, Holder.RequestType.VALVE_STATUS))
                self.wfu = True
            
    def action(self, data, export_list):
        if data.msg_type == Holder.MSGType.UPDATE:
            if data.msg_value.request_type == Holder.RequestType.VALVE_AMOUNT:
                self.valve_amount = data.msg_value.data
            if data.msg_value.request_type == Holder.RequestType.VALVE_STATUS:
                data.msg_value.data
                if self.wfu:
                    print(f"Status update: {data.msg_value.data}")
                    