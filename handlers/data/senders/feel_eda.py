from feel_base import BaseHandler
from feel_data_sender_util import get_eda_data
from feel_data_sender_util import get_eda_data_for_event
class EDASendHandler(BaseHandler):
    
    def get(self):
        user_id = self.get_current_user_id()
        try:    # requesting data with start/end time args
            start_time = self.request.arguments['startTime'][0]
            end_time = self.request.arguments['endTime'][0]
            #read_type = self.request.arguments['type'][0]
            side = self.request.arguments['side'][0]
            data = get_eda_data(user_id, start_time, end_time, 'eda', side)
        except KeyError: # requesting data for an event
            event_id = self.request.arguments['event_id'][0]
            event_type = self.request.arguments['event_type'][0]
            #side = self.request.arguments['side'][0]
            data = get_eda_data_for_event(user_id,  event_type, int(event_id), 'eda')
            
        if data: # for now, we always return data, if none exists just 0s
            self.write(data)
        else:
            self.write("No EDA data found")
    def post(self):
        pass