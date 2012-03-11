from feel_base import BaseHandler
from feel_data_receiver_util import save_event_rating
from feel_data_receiver_util import is_asking_feedback

event_type_to_numbers = {'Phone Call':3, 'Email':1, 'Calendar':2}

class EventFeedbackHandler(BaseHandler):
    
    def get(self):
        type = self.request.arguments['type'][0]
        event_id = self.request.arguments['event_id'][0]
        event_type = self.request.arguments['event_type'][0] 
        
        if type=='should_popup':
                if is_asking_feedback(event_type, event_id):
                    self.write({'response':'yes'})
                else:
                    self.write({'response':'no'})
        elif type=='user_response':
            recall = self.request.arguments['recall'][0]
            stress = self.request.arguments['stress'][0]
            ratings = {'recall':recall, 'stress':stress}
            
            event_type = event_type_to_numbers[event_type]
            save_event_rating(event_type, event_id, ratings)