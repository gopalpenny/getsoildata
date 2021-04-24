#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 24 15:37:30 2021

@author: gopal
"""

# %%

import os
from scrape_india_soilhealth_final import *

# %%
from multiprocessing import Process



if __name__ == '__main__':

    NUM_PROC = 10
    N_villages = 50
    #run_soilhealth_scraper(project_path, download_path, N_villages = 5)
    project_path = "/Users/gopal/Projects/DataScience/india_soilhealth"
    download_path = "/Users/gopal/Downloads"
    
    processes = []
    
    for i in range(NUM_PROC):
        p = Process(target = run_soilhealth_scraper, args = [project_path, download_path, N_villages])
        p.start()
        processes.append(p)
            
    for p in processes:
       p.join()
