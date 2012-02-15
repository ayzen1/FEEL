import datetime
import feel_base as FB
import math

event_types_map = {1:'Email', 2:'Calendar', 3:'Phone Call'}

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
                    event_type = event_types_map[row[2]]
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
                response = {"page":int(page), "records":limit,"total":len(result),"events":rows}
                return response
            return None
        return None
        
        

def get_eda_data(user_id, start_time, end_time, read_type, hand_side):
    
    query = """SELECT start_time, end_time, sampling_rate, eda
                 FROM feel_eda WHERE user_id = {0} AND hand_side={1} AND 
                start_time BETWEEN '{2}' AND '{3}'
            """.format(user_id, hand_side, start_time, end_time)
    
    if(FB.safe_execute(query)):
        result = FB.cursor.fetchall()
      
        start_time = datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
        end_time = datetime.datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
        
        response = {read_type:''}
        
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
                    response[read_type] = response[read_type] + '0,'*sampling_rate*empty_seconds
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
                    response[read_type] = response[read_type]+','.join(readings_partition)
                    break
                
                response[read_type] = response[read_type] + row[3]
                start_time = row_end
                row_num = row_num + 1
            except IndexError:
                #fill row_end till end_time with zeros
                
                print "filling the end gap"
                delta = end_time - row_end 
                delta_length = delta.seconds  #length of data to be appended
                readings = '0,'*delta_length*sampling_rate
                response[read_type] = response[read_type]+readings
                break
            
        print "seconds:" + str(len(response[read_type].split(',')) /sampling_rate ) 
        return response                
                            
                        
                
                
                
                
                