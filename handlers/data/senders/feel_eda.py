from feel_base import BaseHandler
from feel_data_sender_util import get_eda_data
from feel_data_sender_util import get_eda_data_for_event
class EDASendHandler(BaseHandler):
    
    def get(self):
        user_id = self.get_current_user_id()
        try:    # requesting data with start/end time args
            start_time = self.request.arguments['startTime'][0]
            end_time = self.request.arguments['endTime'][0]
            side = self.request.arguments['side'][0]
            # client time format here
            # convert start_time, end_time to datetime objects using client_time_format
            data = get_eda_data(user_id, start_time, end_time, side)
        except KeyError: # requesting data for an event
            event_id = self.request.arguments['event_id'][0]
            event_type = self.request.arguments['event_type'][0]
            try:
                side = self.request.arguments['side'][0]
            except KeyError:
                side = 'RIGHT'
            data = get_eda_data_for_event(user_id,  event_type, int(event_id), side)  
            
        if data is not None: # for now, we always return data, if none exists just 0s
            #print "sending data: "+str(data)
            self.write(data)
        else:
            self.write("No EDA data found")
    def post(self):
        pass