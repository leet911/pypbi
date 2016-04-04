from twdb import TWDB
from msdpdb import MSDPDB
from pypbi import PBI
import json, time
import log
log = log.log('log.txt', 'DEBUG')


refresh_token = 'TOKEN'


######
ticket_ds_name = 'TicketData'
ticket_schema = '''{
 "name": "%s",
   "tables": 
   [
     {
       "name": "TicketCounters", "columns": 
         [
           { "name": "StatusDate", "dataType": "DateTime"},
           { "name": "OpenCount", "dataType": "Int64"},
           { "name": "CloseCount", "dataType": "Int64"},
           { "name": "CreateCountWeek", "dataType": "Int64"},
           { "name": "CloseCountWeek", "dataType": "Int64"},
           { "name": "CreateCount24h", "dataType": "Int64"},
           { "name": "CloseCount24h", "dataType": "Int64"},
           { "name": "CreateCountToday", "dataType": "Int64"},
           { "name": "CloseCountToday", "dataType": "Int64"},
           { "name": "CreateCountHour", "dataType": "Int64"},
           { "name": "CloseCountHour", "dataType": "Int64"},
           { "name": "CSAT", "dataType": "Int64"},
           { "name": "LastTicketID", "dataType": "Int64"}          
         ]
      }
    ]
}''' %(ticket_ds_name)

subs_ds_name = 'SubsData'
subs_schema = '''{
 "name": "%s",
   "tables": 
   [
     {
       "name": "SubsCounters", "columns": 
         [
           { "name": "StatusDate", "dataType": "DateTime"},
           { "name": "UnitID", "dataType": "Int64"},
           { "name": "UnitName", "dataType": "String"},
           { "name": "NewSubsToday", "dataType": "Int64"}
         ]
      }
    ]
}''' %(subs_ds_name)
####

twdb = TWDB()
msdpdb = MSDPDB()
pbi = PBI(refresh_token)

def get_dataset_id(schema):
    id = None
    name = json.loads(schema)['name']
    datasets = pbi.get('datasets')['value']
    for dataset in datasets:
        if dataset.get('name', '') == name:
            id = dataset['id']
    if id is None:
        print 'No existing dataset named %s found, creating...' %name
        print pbi.post('datasets', schema)
        id = get_dataset_id(schema)
    return id

def get_schema_table(schema):
    schema = json.loads(schema)
    tables = schema['tables']
    if len(tables) == 1:
        return tables[0]['name']
    else:
        log.error('Multiple tables found for schema %s' %schema)
    
def results_to_str(results):
    data = {'rows':[]}
    for row in results:
        row_data = {}
        for column, value in row.items():
            row_data[column] = value
        data['rows'].append(row_data)
        
    data = json.dumps(data)
    log.debug(data)
    return data

def post_data(schema, data_function, limit=1, wait=60):
    ds_id = get_dataset_id(schema)
    table = get_schema_table(schema)
    suburl = 'datasets/%s/tables/%s/rows' %(ds_id, table)
    i = 0
    while i < limit:
        i += 1
        data = results_to_str(data_function())
        print i, data
        print pbi.post(suburl, data)
        if i < limit:
            time.sleep(wait)
    return i
    
def run_ticket_counter(limit=1, wait=60):
    return post_data(ticket_schema, twdb.get_ticket_counters, limit=limit, wait=wait)
    
def run_subs_counter(limit=1, wait=60):
    return post_data(subs_schema, msdpdb.get_recent_adds, limit=limit, wait=wait)
    
#run_subs_counter()
#run_ticket_counter()
