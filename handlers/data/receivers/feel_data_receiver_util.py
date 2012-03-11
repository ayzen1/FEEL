import feel_base as FB
import datetime
from edatoolkit import qLogFile

phone_call_params = {'contactName':'contact_name', 'phoneNumber':'phone_number','startTime':'start_time','endTime':'end_time'}
calendar_params = {'startTime':'start_time','endTime':'end_time','allDay':'all_day','location':'location',
                       'title':'title','attendees':'attendees','reminder':'reminder','details':'details'}
email_params = {'from':'sender','subject':'subject','text':'text','sentAt':'sent_at','recipients_to':'recipients_to',
                    'recipients_cc':'recipients_cc','viewStart':'view_start','viewEnd':'view_end'}
time_params = ['sentAt','viewStart','viewEnd','reminder','startTime','endTime']
type_to_params = {1:email_params, 3:phone_call_params, 2:calendar_params}
type_to_tables = {1:'feel_email', 3:'feel_phone_call', 2:'feel_calendar'}

encrypt_params = ['from','subject','text', 'recipients_to','recipients_cc',
                  'contactName','phoneNumber',
                  'title', 'attendees','location']

incoming_time_format = "%Y-%b-%d %H:%M:%S"
server_time_format = "%Y-%m-%d %H:%M:%S"

SLICE_LENGTH = datetime.timedelta(minutes = 30) #length of eda slices in minutes

def handle_event(user_id, request):
    event_type = int(request.arguments['type'][0])
    args = get_event_args(type_to_params[int(event_type)], request)
    save_event(user_id, args, event_type)
        
# returns dictionary of parameters, where keys are the strings used in client side
def get_event_args(params, request):
    args = dict()
    for param in params:
        try:
            arg = request.arguments[param][0]
            if arg == '':   # in case http post includes param name but there is no info. subject to change
                arg = None
        except KeyError:
            pass
        if arg!=None:
            args[param] = arg
    return args

# original dictionary of arguments in httprequest are passed
def save_event(user_id, args, event_type):
    params_map = type_to_params[event_type]
    table = type_to_tables[event_type]
        
    fields_string = " (user_id,"
    values_string = '('+str(user_id) + ','
    for param in args.keys():
        val = args[param]
        if (param in time_params):
                time_object = datetime.datetime.strptime(val, incoming_time_format)
                val = time_object.strftime(server_time_format) 
                
        if param in encrypt_params:
            pub_key = user_id
            val = encrypt(val)
        values_string = values_string + "\'"+val+"\',"
        fields_string = fields_string + params_map[param]+","
          
    fields_string = fields_string[0:len(fields_string)-1] + ") "
    values_string = values_string[0:len(values_string)-1] + ")"
    
    
    query = "INSERT IGNORE INTO " + table + fields_string + "VALUES " + values_string
    if (FB.safe_execute(query)):
        save_event_summary(user_id, event_type, table, args)
    else:
        print "could not save event summary"
        return False
    
# this is called right after all the event data is saved in appropriate table    
def save_event_summary(user_id, event_type, table, args):  
    fetch_id_query = "SELECT LAST_INSERT_ID()"
    if(FB.safe_execute(fetch_id_query)):
        result = FB.cursor.fetchone()
        event_id = result[0]
        fetch_query = "SELECT * FROM "+table+" WHERE id={0}".format(event_id)
        if(FB.safe_execute(fetch_query)):
            result = FB.cursor.fetchone()
            event_id = result[0]
      
    if event_type == 1:
        event_time = args['viewStart']
        memo = args['from']+" - "+args['subject'] 
    elif event_type == 3:
        event_time = args['startTime']
        memo = args['phoneNumber']            
    elif event_type == 2:
        event_time = args['startTime']
        memo = args['title']          
    
    summary_query = """INSERT IGNORE INTO feel_event_summary (event_id, user_id, 
            event_type, event_time, memo) VALUES 
            ({0},{1},{2},'{3}','{4}')""".format(event_id, user_id, event_type, event_time, memo)
    return FB.safe_execute(summary_query)
   
# receives a dictionary of user ratings     
def save_event_rating(event_id, event_type, rating_dict):   
    stress= rating_dict['stress']
    recall = rating_dict['recall']
    query = """UPDATE feel_event_summary SET stress_rating ={0}, recall_rating={1}
                WHERE event_id={2} AND event_type={3}""".format(int(stress), int(recall), event_id, event_type)
    
    return FB.safe_execute(query)
    
    

def save_eda_file_in_slices(user_id, file_name):
    eda_file = qLogFile(file_name)
    slice_start_time = eda_file.startTime #datetime.datetime object
    end_time = eda_file.endTime
    while slice_start_time < end_time:
        slice_end_time = slice_start_time + SLICE_LENGTH if (slice_start_time + SLICE_LENGTH < end_time) else end_time
        
        slice = eda_file.qLogFileSlice(slice_start_time,slice_end_time)
        sample_rate = eda_file.sampleRate
        eda = ",".join(str(x) for x in slice[0])
        temperature =",".join(str(x) for x in slice[1])
        acc_x = ",".join(str(x) for x in slice[2])
        acc_y = ",".join(str(x) for x in slice[3])
        acc_z = ",".join(str(x) for x in slice[4])
                
        save_eda_data(user_id, slice_start_time, slice_end_time, sample_rate, eda, temperature, acc_x, acc_y, acc_z)
        
        slice_start_time = slice_start_time + SLICE_LENGTH
 
# takes datetime objects for start_time and end_time           
def save_eda_data(user_id, start_time, end_time, sample_rate, eda, temperature, acc_x, acc_y, acc_z):
    import pytz
    
    start_time_string = start_time.astimezone(pytz.utc).strftime(server_time_format)
    end_time_string = end_time.astimezone(pytz.utc).strftime(server_time_format)
    
    query = """INSERT IGNORE INTO feel_eda (`user_id`, `start_time`, `end_time`, `sampling_rate`, `eda`,
         `temperature`, `acc_x`, `acc_y`, `acc_z`) VALUES ('{0}','{1}','{2}','{3}',
         '{4}','{5}','{6}','{7}','{8}')""".format(user_id, start_time_string,
                                                   end_time_string, sample_rate, eda,
                                                    temperature, acc_x, acc_y, acc_z)
    return FB.safe_execute(query)