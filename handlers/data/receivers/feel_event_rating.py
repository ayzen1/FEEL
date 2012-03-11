from feel_base import BaseHandler
from feel_data_receiver_util import save_event_rating

class EventRatingHandler(BaseHandler):
    
    def post(self): # 
        
        recall = self.request.arguments['recall'][0]
        stress = self.request.arguments['stress'][0]
        event_id = self.request.arguments['event_id'][0]
        event_type = self.request.arguments['event_type'][0]
        
        ratings = {'recall':recall, 'stress':stress}
        save_event_rating(event_id, event_type, ratings)
            