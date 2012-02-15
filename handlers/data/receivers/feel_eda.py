from feel_base import BaseHandler
from feel_data_receiver_util import save_eda_file_in_slices
import datetime

class EDAReceiveHandler(BaseHandler):

    def post(self):
        
        if self.is_user_logged_in():
            uploaded_file =  self.request.files.get("eda")[0]
            file_name = self.get_current_user_email().partition('.')[0]+"-eda-"+datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
            output_file = open("uploads/eda/" + file_name, 'w' )
            user_id = self.get_current_user_id()
            save_eda_file_in_slices(user_id, "uploads/eda/" + file_name)
            output_file.write(uploaded_file['body'])
            self.finish("file has been uploaded")
        else:
            print "user is not logged in"
            self.redirect("/login")
            
   
                                                      
            