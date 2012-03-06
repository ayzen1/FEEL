import datetime
import feel_base as FB
import math, random
from handlers.data.receivers.feel_data_receiver_util import type_to_tables
from feel_base import safe_execute

db2user_event_types = {1:'Email', 2:'Calendar', 3:'Phone Call'}
user2db_event_types = {'Email':1, 'Calendar':2, 'Phone Call':3}
#2012-03-02T18:35Z
iso8601_format = "%Y-%m-%dT%H:%M:%SZ"
server_time_format = "%Y-%m-%d %H:%M:%S"
def get_basic_grid_data(user_id, page, limit, sidx, sord):
    
    query = "SELECT COUNT(*) FROM feel_event_summary WHERE user_id='{}'".format(user_id)
    if(FB.safe_execute(query)):
        count = FB.cursor.fetchone()[0]
        if count > 0:
            total_pages = math.ceil(count/limit)
        else:
            total_pages = 0
        if page > total_pages:
            page = total_pages
        
        start = limit*page - limit
        if start < 0:
            start = 0
        
        query = """SELECT event_id, user_id, event_type, event_time, memo FROM feel_event_summary
                   WHERE user_id = {0} ORDER BY {1} {2} LIMIT {3}, {4}""".format(user_id, sidx, sord, int(start), int(limit))
        if(FB.safe_execute(query)):
            result = FB.cursor.fetchall()
            if len(result) > 0:
                rows = []
                id = 0
                for row in result:
                    event_id = int(row[0])
                    event_type = db2user_event_types[row[2]]
                    event_time = row[3].strftime(iso8601_format)
                    memo = row[4]
                    row = {
                           "id": id,
                           "cell":[event_type,
                                   event_time,
                                   memo,
                                   event_id]
                           }
                    rows.append(row)
                    id = id + 1
                response = {"page":int(page), "records":limit,"total":total_pages,"events":rows}
                return response
            return None
        return None

# Returns the requested datatype for the event from start time of the event till
# 10 min after its end.        
def get_eda_data_for_event(user_id, event_type, event_id, read_type, hand_side):     
    event_type =  user2db_event_types[event_type]
    table = type_to_tables[event_type]  
    if event_type == 2 or event_type == 3:
        start = 'start_time'
        end = 'end_time'
    else:
        start = 'view_start'
        end = 'view_end'
    query = "SELECT `{0}`, `{1}` FROM `{2}` WHERE `id`={3}".format(start, end, table, event_id)
    if(safe_execute(query)):
        result = FB.cursor.fetchone()
        start_time = result[0]
        end_time = (result[1] +datetime.timedelta(minutes=10))
        return get_eda_data(user_id, start_time, end_time, read_type, hand_side)
    return None

# Takes start_time, end_time datetime objects
# Currently sending all reading types

def get_eda_data(user_id, start_time, end_time, read_type, hand_side = 'RIGHT'):
    start = start_time.strftime(server_time_format)
    end = end_time.strftime(server_time_format)
    
    query = """SELECT `start_time`, `end_time`, `sampling_rate`, `{0}`, `{1}`,`{2}`,`{3}`,`{4}`
                 FROM feel_eda WHERE `user_id` = {5} AND `hand_side`='{6}' AND 
                start_time BETWEEN '{7}' AND '{8}'
            """.format('eda','temperature','acc_z','acc_y','acc_x', user_id, hand_side, start, end)
    
    if(FB.safe_execute(query)):
        result = FB.cursor.fetchall()
            
        eda_reads, temp_reads, acc_z_reads, acc_y_reads, acc_x_reads = [],[],[],[],[]
        response = {'eda':eda_reads, 'temp':temp_reads, 'acc_z':acc_z_reads, 
                    'acc_y':acc_y_reads, 'acc_x':acc_x_reads}
        
        row_num = 0
        row_end  = start_time
        while(start_time < end_time):
            try:
                row = result[row_num]   # results of reads are in row[3:7]
                row_data = {'eda':row[3],'temp':row[4],'acc_z':row[5],'acc_y':row[6], 'acc_x':row[7]}
                sampling_rate = row[2]
                row_start = row[0]
                if(start_time < row_start):
                    fill_gap(response, row_start, start_time, sampling_rate)                                        
                    start_time = row_start
                    continue
                
                row_end = row[1]
                if (row_end > end_time):
                    fill_end(response, row_data, row_start, row_end, end_time, sampling_rate)
                    break
                
                extend_response(response, row_data)
                
                start_time = row_end
                row_num = row_num + 1
            except IndexError:  # no more row data, fill the end gap from last row_end reading till end_time
                if not vars().has_key('sampling_rate'): # if there was no data at all, sampling rate is not defined.
                    sampling_rate = 8                    
                fill_gap(response, row_end, end_time, sampling_rate)
                break    
            
        rev_response = revise_response(response, user_id)
        return rev_response 

def extend_response(response, data):
        response['eda'].extend(data['eda']) 
        response['temp'].extend(data['temp']) 
        response['acc_z'].extend(data['acc_z']) 
        response['acc_y'].extend(data['acc_y']) 
        response['acc_x'].extend(data['acc_x']) 
        
def fill_gap(response, from_time, to_time, sampling_rate):    
        print "filling gap"
        empty_seconds = get_delta_seconds(from_time, to_time)   # assumed empty seconds are no longer than a day!
        
        data = {}
        data['eda'] = [0]*sampling_rate*empty_seconds
        data['temp'] = [30.0]*sampling_rate*empty_seconds
        data['acc_z'] = [0]*sampling_rate*empty_seconds
        data['acc_y'] = [0]*sampling_rate*empty_seconds
        data['acc_x'] = [0]*sampling_rate*empty_seconds
        extend_response(response, data)
        
                
def fill_end(response, row_data, row_start, row_end, end_time, sampling_rate): 
        # eda, temp, acc_y,z,x 
        print "filling the end by trimming"
        delta_seconds = get_delta_seconds(end_time, row_end)
        partition_index = delta_seconds*sampling_rate - 1    # index to cut from row data
        
        data = {}
        data['eda'] = row_data['eda'].split(',')[0:partition_index]
        data['temp'] = row_data['temp'].split(',')[0:partition_index]
        data['acc_z'] = row_data['acc_z'].split(',')[0:partition_index]
        data['acc_y'] = row_data['acc_y'].split(',')[0:partition_index]
        data['acc_x'] = row_data['acc_x'].split(',')[0:partition_index]
        
        extend_response(response, data)
                    
def get_delta_seconds(start, end):
    delta = end  - start
    return delta.seconds          

# currently randomizing only EDA readings          
def revise_response(response, user_id):
    if is_user_admin(user_id):
        return response
    else:
        k = random.randint(1,9)
        if k <= 3: # randomize 33% of time
            new_eda = randomize_eda_data(response['eda'])
            response['eda'] = new_eda
            return response
        else:
            return response
        
def is_user_admin(user_id):
    query = "SELECT `admin` FROM feel_user WHERE `id` = {0}".format(user_id)
    
    if(FB.safe_execute(query)):
        result = FB.cursor.fetchone()
        if result[0] == 1:
            return True
        else:
            return False
       
                           
# takes a list of EDA readings and randomize them                    
def randomize_eda_data(eda_data):
    print "randomizing eda data"
    max, min = 1.5, 6.0
    data = []
    for i in range(len(eda_data)):
        e = random.uniform(min, max)
        data.append(e)
    return data

# takes a list of randomized eda_data and add peeks to it
def add_peeks_to_eda_data(eda_data):
    pass                
                
                