from feel_base import BaseHandler

class RegHandler(BaseHandler):

        def post(self):
            try:
                phone_number = self.request.arguments['phone_number'][0]
            except KeyError:
                phone_number = None
            try:
                email = self.request.arguments['email'][0]
            except KeyError:
                email = None
            
            try:
                assert (phone_number!=None or email!=None)
                password = self.request.arguments['password'][0]
    
                if self.register(password, phone_number=phone_number, email=email):
                        self.write("registered successfully")
                        self.redirect('/')
                else:
                        print "could not register"
                        self.redirect('/reg')
            except AssertionError:
                self.write("You should register either phone number or email")
