from feel_base import BaseHandler
from feel_data_receiver_util import save_eda_file_in_slices
import datetime

class EDAReceiveHandler(BaseHandler):
    
    # EDA file with hand-side info is posted here.
    def post(self): # 
        
        if self.is_user_logged_in():
            uploaded_file =  self.request.files.get("eda")[0]
            file_name = str(self.get_current_user_id())+"-eda-"+datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
            try:
                hand_side = self.request.arguments['side'][0]
            except KeyError:
                hand_side = 'RIGHT'
            output_file = open("uploads/eda/" + file_name, 'w' )
            output_file.write(uploaded_file['body'])
            self.finish("file has been uploaded")
            
            user_id = self.get_current_user_id()
            save_eda_file_in_slices(user_id, hand_side, "uploads/eda/" + file_name)
            
        else:
            print "user is not logged in"
            self.redirect("/login")
            
   
                                                      
            