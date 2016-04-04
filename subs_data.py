import requests
import random
import uuid
import time

APS_HOST = 'yul01dev28msdp03.ops.dot'
APS_PORT = 8090
APS_USER = 'msdp.admin@radialpoint.com'
APS_PASS = 'msdpadmin'

UNITS = [27, 33, 37, 38, 39, 48]

auth = requests.auth.HTTPBasicAuth(APS_USER, APS_PASS)
root_url = 'http://%s:%s/aps/services/rest/softwareProviderUnit/' %(APS_HOST, APS_PORT)

def rand_list(l):
    i = random.randint(0, len(l)-1)
    return l[i]

def get_unit():
    return rand_list(UNITS)

def get_product(unit):
    url = '%s%s/product' %(root_url, unit)
    #print url
    r = requests.get(url, auth=auth)
    products = r.json()
    skus = []
    for product in products:
        skus.append(product['productId'])
    return  rand_list(skus)
    
def create_subscriber(unit):
    sub_id = str(uuid.uuid4())
    body = {
        'subscriberId' : sub_id,
        'credentials' : sub_id,
        'accountId' : sub_id
    }
    url = '%s%s/account' %(root_url, unit)
    #print url
    r = requests.post(url, auth=auth, data=body)
    return sub_id
    
def subscribe():
    unit = get_unit()
    product = get_product(unit)
    sub_id = create_subscriber(unit)
    url = '%s%s/account/%s/subscription' %(root_url, unit, sub_id)
    body = {
        'productIdsCsv':product
    }
    #print url
    #print body
    print 'Adding product %s to subscriber %s, unit %s' %(product, sub_id, unit)
    r = requests.post(url, auth=auth, data=body)
    return r

    
while True:
    print subscribe()
    wait = random.randint(1, 5)
    print 'Pause for %s seconds...' %wait
    time.sleep(wait)
    
    
    
    