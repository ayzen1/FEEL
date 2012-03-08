from feel_base import BaseHandler
from feel_data_sender_util import get_event_data

# Sends all the data associated with an event

class EventSendHandler(BaseHandler):
    
    def get(self):
        user_id = self.get_current_user_id()
        try:
            event_type = self.request.arguments['event_type'][0]
            event_id = self.request.arguments['event_id'][0]
            
            response = get_event_data(user_id, event_type, event_id)
            assert response != None
            self.write(response)
        except: # can be used different reqeusts in the future
            print "problem with http request"
        
    def post(self):
        pass
