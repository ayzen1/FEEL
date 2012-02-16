import datetime
import feel_base as FB
import math
from handlers.data.receivers.feel_data_receiver_util import type_to_tables
from feel_base import safe_execute

db2user_event_types = {1:'Email', 2:'Calendar', 3:'Phone Call'}
user2db_event_types = {'Email':1, 'Calendar':2, 'Phone Call':3}

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
                   WHERE user_id = {0}
                   ORDER BY {1} {2} LIMIT {3}, {4}""".format(user_id, sidx, sord, int(start), int(limit))
        if(FB.safe_execute(query)):
            result = FB.cursor.fetchall()
            if len(result) > 0:
                rows = []
                id = 0
                for row in result:
                    event_id = int(row[0])
                    event_type = db2user_event_types[row[2]]
                    # "%Y-%m-%d %H:%M:%S"
                    event_time = row[3].strftime("%Y-%m-%d %H:%M:%S")
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
        
def get_eda_data_for_event(user_id, event_type, event_id, read_type):     
    event_type =  user2db_event_types[event_type]
    table = type_to_tables[event_type]  
    if event_type == 2 or event_type == 3:
        start = 'start_time'
        end = 'end_time'
    else:
        start = 'view_start'
        end = 'view_end'
    query = """SELECT `{0}`, `{1}` FROM `{2}` WHERE `id`={3}""".format(start, end, table, event_id)
    if(safe_execute(query)):
        result = FB.cursor.fetchone()
        start_time = result[0].strftime("%Y-%m-%d %H:%M:%S")
        end_time = (result[1] +datetime.timedelta(minutes=10)).strftime("%Y-%m-%d %H:%M:%S")
        return get_eda_data(user_id, start_time, end_time, read_type)
    return None

def get_eda_data(user_id, start_time, end_time, read_type, hand_side = 'RIGHT'):
    
    query = """SELECT start_time, end_time, sampling_rate, eda
                 FROM feel_eda WHERE user_id = {0} AND hand_side='{1}' AND 
                start_time BETWEEN '{2}' AND '{3}'
            """.format(user_id, hand_side, start_time, end_time)
    
    if(FB.safe_execute(query)):
        result = FB.cursor.fetchall()
      
        start_time = datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")+datetime.timedelta(minutes=10)
        end_time = datetime.datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
        
        response = []
        
        row_num = 0
        row_end  = start_time
        while(start_time < end_time):
            try:
                row = result[row_num]
                
                sampling_rate = row[2]
                row_start = row[0]
                if(start_time < row_start):
                    #fill the gap
                    print "filling the start gap"
                    delta = row_start - start_time
                    empty_seconds = delta.seconds   # assumed empty seconds are no longer than a day!
                    response.extend([0]*sampling_rate*empty_seconds)
                    start_time = row_start
                    
                row_end = row[1]
                if (row_end > end_time):
                    print "trimming from end"
                    # trim from end
                    row_length = row_end - row_start    #length of data in db
                    post_length = end_time - row_start  #length of data to be appended
                    row_seconds = row_length.seconds
                    post_seconds = post_length.seconds
                    
                    partition_index = (row_seconds - post_seconds)*sampling_rate - 1    # #of readings to grab from row
                    readings = row[3]
                    readings_list = readings.split(',')
                    readings_partition = readings_list[0:partition_index]
                    response.extend(readings_partition)
                    break
                
                response =response.extend(row[3].split(','))
                start_time = row_end
                row_num = row_num + 1
            except IndexError:
                #fill row_end till end_time with zeros
                print "filling the end gap"
                if not vars().has_key('sampling_rate'):
                    sampling_rate = 8
                delta = end_time - row_end 
                delta_length = delta.seconds  #length of data to be appended
                response.extend([0]*delta_length*sampling_rate)
                break        
        #print "seconds:" + str(len(response[read_type].split(',')) /sampling_rate ) 
        print response
        return {read_type:response}                
                            
                        
                
                
                
                
                