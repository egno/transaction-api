from oper import *

print(do(type='CustomerPayment', business='31e2fde3-85c7-11e9-b72c-37effc36ab5e', amount=25.06))

print(do(type='SMSReserveSum',
         business='31e2fde3-85c7-11e9-b72c-37effc36ab5e', amount=24.01))

print(do(type='CustomerAccountBalance',
         business='31e2fde3-85c7-11e9-b72c-37effc36ab5e'))

