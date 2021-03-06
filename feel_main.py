from handlers.data.receivers.feel_eda import EDAReceiveHandler
from handlers.data.receivers.feel_event import EventReceiveHandler
from handlers.data.receivers.feel_event_feedback import EventFeedbackHandler

from handlers.data.senders.feel_event import EventSendHandler
from handlers.data.senders.feel_populate import PopulateHandler
from handlers.data.senders.feel_eda import EDASendHandler

from handlers.ui.feel_home import HomeHandler
from handlers.utils.feel_login import LoginHandler
from handlers.utils.feel_logout import LogoutHandler
from handlers.utils.feel_reg import RegHandler

import tornado.ioloop
import tornado.web
import os 
        
settings = {
    "static_path":os.path.join(os.path.dirname(__file__), "static"),
    "cookie_secret" :'UcCbwfNHSoSUQKnC6gVhR/+nKf4MIUxruhq3buIEkYk='
}

application = tornado.web.Application([
    (r"/", HomeHandler),
    (r"/reg", RegHandler),
    (r"/login",LoginHandler),
    (r"/logout",LogoutHandler),
    (r"/eda_post", EDAReceiveHandler),
    (r"/eda_get", EDASendHandler),
    (r"/event_post", EventReceiveHandler),
    (r"/event_get", EventSendHandler),
    (r"/populate", PopulateHandler),
    (r"/feedback", EventFeedbackHandler),
], **settings )


    
if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
    
