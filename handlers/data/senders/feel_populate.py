from feel_base import BaseHandler
from feel_data_sender_util import get_basic_grid_data

class PopulateHandler(BaseHandler):
    
    def get(self):
        if self.is_user_logged_in():
            page = self.request.arguments['page'][0]
            limit = self.request.arguments['rows'][0]
            sord = self.request.arguments['sord'][0]
            try:
                sidx = self.request.arguments['sidx'][0]
            except:
                sidx = 'event_time'
            user_id = self.get_current_user_id()
            
            data = get_basic_grid_data(user_id, int(page), int(limit), sidx, sord)
            print "sending data: " +str(data)
            if(data!= None):
                self.write(data) #sending dict(); so, ContentType is automatically json/application 
        else:
            self.redirect('/login')
    def post(self):
        pass
    