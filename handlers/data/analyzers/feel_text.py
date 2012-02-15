from feel_base import BaseHandler
import urllib2, urllib
import json

_text_url = "http://access.alchemyapi.com/calls/text/TextGetTextSentiment"
_text_api_key = "efb7f61eead18faa96c3aecf5e429bf625e11493"

class TextHandler(BaseHandler):
    def get(self):
        self.write('<html><body><form action="/text" method="post">'
                   '<input type="text" name="text">'
                   '<input type="submit" value="Submit">'
                   '</form></body></html>')
        
    def post(self):
        self.write("text handler!")
        text = self.request.arguments['text'][0]
        
        data = {'apikey':_text_api_key, 'text':text, 'outputMode':'json', 'showSourceText':1}
        
        datagen = urllib.urlencode(data)
        headers = {}
        req= urllib2.Request(_text_url, datagen, headers)
        res = urllib2.urlopen(req)
        res = res.read()
        response = json.loads(res)
        
        if response['status'] == 'OK':
            self.save_text_analysis(response)
            
