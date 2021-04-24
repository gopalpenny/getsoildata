#!/usr/bin/env python

import os
import subprocess
import time
import numpy as np

key_word = '/Users/gopal/Projects/DataScience/india_soilhealth/index/West Bengal_districts.csv'

i = 1
continue_var = True
while continue_var:
    try:
        print('making a run ' + str(i))
        subprocess.run('./scrape_india_soilhealth_functions.py')
    except:
        print('error received')

    i = i + 1
    continue_var = not(os.path.isfile(key_word)) and i < 100


print('reached key file')

