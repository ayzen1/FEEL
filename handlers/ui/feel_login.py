from feel_base import BaseHandler
import base64, uuid

class LoginHandler(BaseHandler):
 
    def post(self):
        try:
            phone_number = self.request.arguments['phone_number'][0]
        except KeyError:
            phone_number = None
        try:
            email = self.request.arguments['email'][0]
        except KeyError:
            email = None
        
        password = self.request.arguments['password'][0]
        
        if self.is_correct_login(password, phone_number= phone_number, email=email,):
            key = base64.b64encode(uuid.uuid4().bytes + uuid.uuid4().bytes)
            if(self.save_login(key, email=email, phone_number=phone_number)):
                self.write("successful login")
                self.set_secure_cookie('key', key)
                self.redirect("/")
            else:
                self.write("could not login=(")
                self.redirect('/login')
        else:
            print "incorrect login"
            self.redirect('/login')
