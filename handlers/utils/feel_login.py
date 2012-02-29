from feel_base import BaseHandler
import hashlib
class LoginHandler(BaseHandler):
 
    def get(self):
        print hashlib.md5('mac').hexdigest()
        if self.do_login('mac', email='makif@mit.edu'):
            print "test logged in"
        else:
            print "could not do test login"
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
        
        if(self.do_login(password, email=email, phone_number=phone_number)):
            self.write("successful login")
            self.redirect("/")
        else:
            self.write("incorrect login")
            self.redirect('/login')
