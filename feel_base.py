from feel_database import Database as db
import tornado.web
cursor = db.cursor

def safe_execute(query):
    try:
        print "attempting to execute query; {0}..".format(query)
        cursor.execute(query)
        return True
    except Exception as ex:
        print type(ex)
        print ex.args
        return False        
      
class BaseHandler(tornado.web.RequestHandler):
    
    def get_current_user_key(self):
        return self.get_secure_cookie("key")
    
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
        
    def get_current_user_info(self):
        key = self.get_current_user_key()
        if key:
            query = "SELECT * FROM feel_login WHERE `key`='{}' LIMIT 1".format(key)
            if safe_execute(query):
                result = cursor.fetchone()
                email, phone_number = result[1], result[2]
                return email, phone_number
        
    def get_current_user_id(self):
        email, phone_number = self.get_current_user_info()
        field_name, field_value = self.get_field_info(phone_number, email)
        query = "SELECT * FROM feel_user WHERE `{0}`='{1}' LIMIT 1".format(field_name, field_value)
        if safe_execute(query):
            result = cursor.fetchone()
            return result[0]
                
    def is_user_logged_in(self):
        key = self.get_current_user_key()
        if key:
            query = "SELECT * FROM feel_login WHERE `key`='{}' LIMIT 1".format(key)
            if safe_execute(query):
                result = cursor.fetchone()
                return (result!=None)

        return False
       
    def is_correct_login(self, password, email=None, phone_number=None):
        field_name, field_value = self.get_field_info(phone_number, email)
        query = "SELECT * FROM feel_user WHERE {0}='{1}'".format(field_name, field_value)
        if(safe_execute(query)):
            result = cursor.fetchone()
            if(result != None):
                if (result[3] == password):
                    return True
        return False
        
                   
    def save_login(self, key, email=None, phone_number=None):
        field_name, field_value = self.get_field_info(phone_number, email)
        query = "INSERT INTO feel_login (`{0}`, `key`) VALUES ('{1}','{2}')".format(field_name, field_value, key)
        return safe_execute(query)
    
    def logout(self):
        query = "DELETE FROM feel_login WHERE `key`='{}'".format(self.get_current_user_key())
        return safe_execute(query)
        
    # Registers a user with password and either phone number or email
    def register(self, password, phone_number=None, email=None):
        try:
            assert (phone_number!=None or email!=None)
            field_name, field_value = self.get_field_info(phone_number, email)
            query = """INSERT INTO feel_user (`{0}`, `password`) VALUES 
            ('{1}', '{2}')""".format(field_name, field_value, password)
            return safe_execute(query)
        except AssertionError:
            return False
        
    def get_field_info(self, phone_number, email):
        if phone_number == None:
                field_name = 'email'
                field_value = email
        else:
                field_name = 'phone_number'
                field_value = phone_number
        return field_name, field_value        
    def save_picture_analysis(self, response):
        if response['status'] == 'success':
            mood = response['photos'][0]['tags'][0]['attributes']['mood']
            email = self.get_current_user_email()
            query = "INSERT INTO feel_picture (email, mood, confidence) VALUES ('{0}','{1}',{2})".format(email, mood['value'], mood['confidence'])
            return safe_execute(query)
        return False
    
    # TODO: pass other email fields into text analysis.
    def save_text_analysis(self,response):
        sentiment = response['docSentiment']['type']
        score = response['docSentiment']['score']
        text = response['text']
        email = self.get_current_user_email()
        query = "INSERT INTO text (email , text, sentiment, score) VALUES ('{0}','{1}','{2}',{3})".format(email, text, sentiment, score )
        return safe_execute(query)
    

    
    
    
        
    
        
       
            
    
    
