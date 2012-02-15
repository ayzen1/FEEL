from feel_base import BaseHandler
from poster.encode import multipart_encode
import urllib2, json, datetime

_face_api_key="9f5766905329451c675eb672a201d611"
_face_api_secret= "12fd4aba022424d195c4317459c4bf1f"
_face_url = "http://api.face.com/faces/detect.json"

class PictureHandler(BaseHandler):

    def get(self):
        self.write('<html><body><form action="/picture" method="post" enctype="multipart/form-data">'
                   '<input type="file" name="picture">'
                   '<input type="submit" value="Upload">'
                   '</form>'
                   '</body></html>')
    def post(self):
        self.write("pic handler! ")
        pic= self.request.files.get("picture")[0]
        file_name = self.get_current_user_email().partition('.')[0]+"-pic-"+datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")+'.jpeg'
        output_file = open("uploads/pic/" + file_name, 'wb')    # write binary, or pic will get corrupted
        output_file.write(pic['body'])
        output_file.close()
                
        data = {'api_key': _face_api_key,
               'api_secret': _face_api_secret,
               'format': "json",
               'file':file_name,
               'detector':'Aggressive',
               'attributes':'all'}

        data['file'] = open("uploads/pic/"+file_name, 'rb')
        
        datagen, headers = multipart_encode(data)
        data = "".join(datagen)        
        req = urllib2.Request(_face_url, data, headers)
    
        resp = urllib2.urlopen(req)
        print "opened"
        resp = resp.read()
        print resp
        response= json.loads(resp)
        self.handle_response(response)
        

    def handle_response(self, response):
        return self.save_picture_analysis(response)
        
