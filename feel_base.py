from feel_database import Database as db
import md5, base64, uuid, hashlib
import tornado.web
cursor = db.cursor

def safe_execute(query):
    try:
        print "executing query; {0}.".format(query)
        cursor.execute(query)
        return True
    except Exception as ex:
        print type(ex)
        print ex.args
        return False   

def get_field_info(phone_number, email):
        if phone_number == None:
                field_name = 'email'
                field_value = email
        else:
                field_name = 'phone_number'
                field_value = phone_number
        return field_name, field_value       
      
class BaseHandler(tornado.web.RequestHandler):
    
       
    def get_current_user_key(self):
        return self.get_secure_cookie("key")
    
    def get_current_user_password(self):
        return self.get_secure_cookie("pass")
    
    def get_user_id_of_phone_number(self, phone_number):
        query = "SELECT * FROM feel_user WHERE `phone_number`={} LIMIT 1".format(phone_number)
        if(safe_execute(query)):
            result = cursor.fetchone()
            if result:
                return result[0]
            else:
                print "phone number is not in database"
                return 1
        else:
            return 1 #for testing purposes...

        
    def get_current_user_id(self):
        if self.is_user_logged_in():
            key = self.get_current_user_key()
            query = "SELECT * FROM feel_login WHERE `key`='{0}' LIMIT 1".format(key)
            if safe_execute(query):
                result = cursor.fetchone()
                if result!=None:
                    return result[0]
        return None
                
    def is_user_logged_in(self):
        key = self.get_current_user_key()
        if key:
            query = "SELECT * FROM feel_login WHERE `key`='{}' LIMIT 1".format(key)
            if safe_execute(query):
                result = cursor.fetchone()
                return (result!=None)

        return False
       
    def get_user_id(self, password, email=None, phone_number=None):
        field_name, field_value = get_field_info(phone_number, email)
        query = "SELECT `id`, `password` FROM feel_user WHERE {0}='{1}'".format(field_name, field_value)
        if(safe_execute(query)):
            result = cursor.fetchone()
            if(result != None):
                if (result[1] == hashlib.md5('mac').hexdigest()):
                    return result[0]
                else:
                    return False
                    print "wrong password"
        return False
        
                   
    def do_login(self, password, email=None, phone_number=None):
        key = base64.b64encode(uuid.uuid4().bytes + uuid.uuid4().bytes)
        self.set_secure_cookie('key', key)
        self.set_secure_cookie('pass', password)
        
        user_id = self.get_user_id(password, email, phone_number)
        print "executing deletion.." #in case user just closed web browser To be changed
        safe_execute("DELETE FROM feel_login WHERE `user_id`='{0}'".format(user_id))
        if(user_id):
            query = "INSERT INTO feel_login (`user_id`, `key`) VALUES ('{0}','{1}')".format(user_id, key)
            return safe_execute(query)
        else:
            return False
    
    def logout(self):
        query = "DELETE FROM feel_login WHERE `key`='{}'".format(self.get_current_user_key())
        return safe_execute(query)
        
    # Registers a user with password and either phone number or email
    def register(self, password, phone_number=None, email=None):
        try:
            assert (phone_number!=None or email!=None)
            enc_pass = hashlib.md5(password).hexdigest()
            field_name, field_value = get_field_info(phone_number, email)
            query = """INSERT IGNORE INTO feel_user (`{0}`, `password`) VALUES 
            ('{1}', '{2}')""".format(field_name, field_value, enc_pass)
            return safe_execute(query)
        except AssertionError:
            return False
        
       
       
#    def save_picture_analysis(self, response):
#        if response['status'] == 'success':
#            mood = response['photos'][0]['tags'][0]['attributes']['mood']
#            email = self.get_current_user_email()
#            query = "INSERT INTO feel_picture (email, mood, confidence) VALUES ('{0}','{1}',{2})".format(email, mood['value'], mood['confidence'])
#            return safe_execute(query)
#        return False
#    
#    # TODO: pass other email fields into text analysis.
#    def save_text_analysis(self,response):
#        sentiment = response['docSentiment']['type']
#        score = response['docSentiment']['score']
#        text = response['text']
#        email = self.get_current_user_email()
#        query = "INSERT INTO text (email , text, sentiment, score) VALUES ('{0}','{1}','{2}',{3})".format(email, text, sentiment, score )
#        return safe_execute(query)
#    

    
    
    
        
    
        
       
            
    
    
