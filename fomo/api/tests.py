from django.test import TestCase
import requests

# Create your tests here.

##########################
# Test passes
print('\n############## TEST 1: PASS')

q_params = {
    'product_name': 't',
    'category_name': 'instr',
    'min_price': 5,
    'max_price': 900,
}

r = requests.get('http://localhost:8000/api/catalog', params=q_params)
print(r.text)

##########################
# Test fails because not all the query parameters are included
print('\n############## TEST 2: FAIL')

q_params = {
    'product_name': 'trumpet',
    'category_name': 'instr',
    'min_price': 5,
    'max_price': 900,
}
r = requests.post('http://localhost:8000/api/catalog', params=q_params)
print(r.text)

##########################
# Test fails because not all the query parameters are included
print('\n############## TEST 3: FAIL')

q_params = {
    'product_name': 't',
    'category_name': 'instr',
    'min_price': 5,
}

r = requests.get('http://localhost:8000/api/catalog', params=q_params)
print(r.text)
