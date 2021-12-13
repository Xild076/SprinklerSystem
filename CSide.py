# Client/Controller Side
from Utility import set_vals_dict, Comm, Holder
from itertools import repeat
import sys


class Client(Comm):
    def __init__(self, valve_a):
        super().__init__("CLIENT")
        self.valve_amount = valve_a
        self.valve_state = list(repeat(False, valve_a))
    
    def action(self, data, export_list):
        if data.msg_type == Holder.MSGType.REQUEST:
            if data.msg_value == Holder.RequestType.VALVE_AMOUNT:
                export_list.append(Holder(Holder.MSGType.UPDATE, Holder.UpdateHolder(Holder.RequestType.VALVE_AMOUNT, self.valve_amount)))
            elif data.msg_value == Holder.RequestType.VALVE_STATUS:
                export_list.append(Holder(Holder.MSGType.UPDATE, Holder.UpdateHolder(Holder.RequestType.VALVE_STATUS, self.valve_state)))
        if data.msg_type == Holder.MSGType.COMMAND:
            self.valve_state[data.msg_value.valve_number] = data.msg_value.valve_value
        if data.msg_type == Holder.MSGType.KILL:
            sys.exit()