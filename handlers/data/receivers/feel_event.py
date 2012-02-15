from feel_base import BaseHandler
from feel_data_receiver_util import handle_event

# Use this handler to deal with phone events.

class EventHandler(BaseHandler):
    
    def get(self):
        phone_number = self.request.arguments['userphone'][0]
        user_id = self.get_user_id_of_phone_number(phone_number)
        handle_event(user_id, self.request)
    def post(self):
        pass
