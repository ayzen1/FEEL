from feel_base import BaseHandler

class RegHandler(BaseHandler):
        def get(self):
            if self.is_user_logged_in():
                self.redirect("/")
                return
            self.write('<html><body><form action="/reg" method="post">'
                   '<p>Phone Number:<p/><input type="text" name="phone_number"/>'
                   '<p>Password<p/><input type="password" name="password"/>'
                    '<p>Password Confirm</p><input type="password" name="password"/>'
                    '<input type="submit" name="submit"/>'
                   '</form></body></html>')
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
