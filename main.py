from twdb import TWDB
from msdpdb import MSDPDB
from pypbi import PBI
import json, time
import log
log = log.log('log.txt', 'DEBUG')

#Tom
#refresh_token = 'AAABAAAAiL9Kn2Z27UubvWFPbm0gLQe2AeyczBgGHq66SNxZs_UdVcJadWH1yyOESslkN67k9ww7Qdyt0ivK5PGLHHY4f4w717jGqOCDscZI-AMCyLG9MIRic6KIJeA2LjVhTZ_m5VdC3CGUBJ9FKLoDbyDxepK5Nmfwqs0rFFB4LHThWVvyGvjkjmbrXQ8haDMpeQSSkp6TC0H9h_gzpswTHgjd29ofEzyF6j7CLh3gx-3kHCzaqpPH9uCAI8n0bRc3Dj-2QEmqkqYb2yp4fX7gz159k62n5ocdQsRyRpLCuldcd_kBLy7zOnxTKQfk6FmFukALdkdmjewdk_eD7iacVn4yyo0c6PTHP-9gJvSiFU7AFq66Yc5yhFuvp5QfRd5ATQmi6gxD4cUg2G01vizUPAdRQrfPBrbyGZUi2MUsKF3ud3hxLTMLYzBXPHaDetgprEQRcgvOWNGTsueJOd0Iw08DbrdSN8GHWQ3R_d7a5Pue1lhrNk6kgNdHPNc8hIrcRh-fDyzlLuR9bWjJ65ahbU5qcE-a3iO5Zx3mOqfJ_xbeXHNYd91cvRyb2Fi3a_nhjzGi5QnNhykR2s7C5HixaCxtM5tMJ15VN70rdORgbxqkLqBy-6_boYzGvr5Oyr8Y1VBvlhrqS8PuAosyHMwYDhb2krfBLeYdCd8GCwO_MFjlbwMczsArxNsmao7EWMKH7QRmhrQW8mrzhWPnxk_BClBLEHkiD6KBYhca93-FpTsDvFmUB4_9YNimx0NoOKIeyC9fw0nYIet4E_LdioK-Tm1Fmaus1O9FKf4BWz2Fg7Y-V3LAsVBFpxom-oD5Q2crfVKMFR2dBdJncWwmNvVNDUp-08g4uGi5JmVlQIy9k5UL_uxOnAidLH8y0WpMykFj7mCsgvfvNMfhtupW6QtlG87uUr10V7lA3bQXZfaa3iksTD8534Q6XvGsbtalv3UV64P3IAA'

#Yann
refresh_token = 'AAABAAAAiL9Kn2Z27UubvWFPbm0gLfQFMisngpiuZn6hsPc1Acuog5ficZpkTPfbQOluPNk79RD0tkQrWWdAsxoxQWjQDMglJ69KNNeh498KIzvrPClPdLsTWViykQNWj0bX2GWZYdV6MCpYs707mFwn0ILLjPg9goSzO3isDYQ1ZLqwrE8ZhznS7QEUGxqZ5l03wB-sPD7rEhor7ew1kPqF5uzsGcyCkd8icUbShFTeKVrc348FchdKriV4WwfIAOqRgtEvdeytS-0aOZnCb5LtZWBqhPCqZTJDMw32MuUW2p5OnNcoBLMzYaeFOPp8BgErMEq4v1Bm3JkwRiI5jGXttnMJJKhxJcPKugzjySaZt84OFcNJWhS2prP5iEh7_aLHnOuItFr1xhI5dN-EthIV3KbDD29X6FLa__UusD3yJ44w6yLoV8PE69JfCa_1osVKu0daYMuw1ZUrTTW5t4gTJi4O6Ng1gb6FK-mWFJoqQlMMxgGCHnxSlkE5AbAvjWk9vlLK50Xpmufh9887Hjtwjez5muFiyPfjb-2NlgG0yvHtC7NnsFXmT1YEDIZ4eVZvmaFh0rEadb4d3Ua0ZpvBLX95TiltPURFxNtcVeIO2sFr3qT28y6Qq11zN-J8A_osPQiZ9J6yWPdeTucInuojpdLE4hrWppbBqiD3ANkaj4ZT-z1HUh-y3366mpJXGH-qNUwZabjLlLNjNeSozrwvwFFPSBYyD9Laq16pP73f5FWdTnV4iX9PQ8nKQoiq0Joay6JSDM1i9ht_Mq__p0zZTagaWG0SwmDfhBgAnZffSwhIm47UB10LMMln2FK4DjYGLauXp0f3xYtYgVvRmryBIiZKjm19NhMgPI1RuebNTEIkvthWkOIv5jgWfiKq87o6mHfDmLjyvpvQBZ5WV1070Vl-8E7EkSrbw9bfrWUA5pAQ_wwxEEeSRBVbxy5l1KtRYXvwIAA'


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
