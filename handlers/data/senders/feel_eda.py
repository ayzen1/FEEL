from feel_base import BaseHandler
from feel_data_sender_util import get_eda_data

class EDASendHandler(BaseHandler):
    
    def get(self):
        user_id = self.get_current_user_id()
        start_time = self.request.arguments['startTime'][0]
        end_time = self.request.arguments['endTime'][0]
        #read_type = self.request.arguments['type'][0]
        side = self.request.arguments['side'][0]
        
        
        data = get_eda_data(user_id, start_time, end_time, 'eda', side)
        self.write(data)
    def post(self):
        pass