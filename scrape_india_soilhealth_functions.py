#!/usr/bin/env python
# coding: utf-8

"""
from time import sleep
from selenium import webdriver
#from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome('/Users/gopal/opt/anaconda3/bin/chromedriver')

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#from bs4 import BeautifulSoup
#import requests
import os
#import subprocess
import re
import pandas as pd
import numpy as np

# %%
paths = {'data_filepath': "/Users/gopal/Projects/DataScience/india_soilhealth/data",
         'index_filepath': "/Users/gopal/Projects/DataScience/india_soilhealth/index",
         'download_filepath': "/Users/gopal/Downloads/NutrientsStatusReportFarmerWise.csv"
}


driver.get("https://soilhealth.dac.gov.in/PublicReports/NutrientsStatusReportFarmerWise")
"""

# %%
def get_state_districts(si, smeta, paths, driver):
    """
    This function:
        1. S
    """
    #     si = 3
    state_dropdown.select_by_index(smeta['states_index'][si])
    state_name = smeta['states'][si]
    sleep(2)
    # print(states[si]  + " " + states_index[si])

    # Load districts from dropdown
    district_dropdown = Select(driver.find_element_by_name("District_Code"))

    districts = []
    districts_index = []
    for i in range(len(district_dropdown.options)):
        if i > 0:
            districts.append(district_dropdown.options[i].get_attribute('innerText'))
            districts_index.append(district_dropdown.options[i].get_attribute('index'))

    # Save index of all subdistricts within the district
    data = list(zip(np.repeat(smeta['states'][si], len(districts)), 
                    districts))

    state_districts_df = pd.DataFrame(data, columns = ['State', 'District'])
    state_filepath = os.path.join(paths['index_filepath'], state_name + "_districts.csv")
    state_districts_df.to_csv(state_filepath)

    dmeta = {
        'state_name': state_name,
        'districts': districts,
        'districts_index': districts_index
    }
    return dmeta

# %%
def get_district_subdists(di, dmeta, paths, driver):
    #     di = 1
    district_dropdown = Select(driver.find_element_by_name("District_Code"))
    district_dropdown.select_by_index(dmeta['districts_index'][di])
    district_name = dmeta['districts'][di]

    sleep(2)

    # Load subdistricts from dropdown
    subdist_dropdown = Select(driver.find_element_by_name("sub_district_code"))

    subdists = []
    subdist_index = []
    for i in range(len(subdist_dropdown.options)):
        if i > 0:
            subdists.append(subdist_dropdown.options[i].get_attribute('innerText'))
            subdist_index.append(subdist_dropdown.options[i].get_attribute('index'))

    # Save index of all subdistricts within the district
    data = list(zip(np.repeat(dmeta['state_name'], len(subdists)), 
                    np.repeat(district_name, len(subdists)), 
                    subdists))

    district_subdists_df = pd.DataFrame(data, columns = ['State', 'District', 'Subdistrict'])
    district_filepath = os.path.join(paths['index_filepath'], dmeta['state_name'] + "-" + district_name + "_subdists.csv")
    district_subdists_df.to_csv(district_filepath)

    bmeta = {
        'state_name': dmeta['state_name'],
        'district_name': district_name,
        'subdists': subdists,
        'subdist_index': subdist_index
    }

    return bmeta


# In[164]:
    
#def check_if_villages_complete(subdistrict_village_table):
    


def get_subdist_villages(bi, bmeta, paths, driver):
    # bi = 1
    subdist_dropdown = Select(driver.find_element_by_name("sub_district_code"))
    subdist_dropdown.select_by_index(bmeta['subdist_index'][bi])
    subdist_name = bmeta['subdists'][bi]

    sleep(2)

    # Load villages from dropdown
    village_dropdown = Select(driver.find_element_by_name("Village_Code"))

    villages = []
    villages_index = []
    for i in range(len(village_dropdown.options)):
        if i > 0:
            villages.append(village_dropdown.options[i].get_attribute('innerText'))
            villages_index.append(village_dropdown.options[i].get_attribute('index'))

    # Save index of all villages within the subdistrict
    data = list(zip(np.repeat(bmeta['state_name'], len(villages)), 
                    np.repeat(bmeta['district_name'], len(villages)), 
                    np.repeat(subdist_name, len(villages)),
                    villages))

    subdist_villages_df = pd.DataFrame(data, columns = ['State', 'District', 'Subdistrict', 'Village'])
    subdistrict_filepath = os.path.join(paths['index_filepath'], bmeta['state_name'] + "-" + bmeta['district_name'] + "-" + subdist_name + "_villages.csv")
    subdist_villages_df.to_csv(subdistrict_filepath)
    
    # Get village info
    # for vi in range(len(villages_index)):
    vmeta = {
        'state_name': bmeta['state_name'],
        'district_name': bmeta['district_name'],
        'subdist_name': subdist_name,
        'villages': villages,
        'villages_index': villages_index
    }
    
    return vmeta

def download_village_data(vi, vmeta, paths, driver):
    
    village_name = vmeta['villages'][vi]
    village_filename = re.sub("[\s\/]","",
                          os.path.join(vmeta['state_name'] + "_" + vmeta['district_name'] + "_" + vmeta['subdist_name'] + "_" + village_name + ".csv"))


    
    village_filepath = os.path.join(paths['data_filepath'], village_filename)
    

    if not os.path.isfile(village_filepath):
        driver.switch_to.default_content()

        village_dropdown = Select(driver.find_element_by_name("Village_Code"))
        village_dropdown.select_by_index(vmeta['villages_index'][vi])
        sleep(2)

        # Click "View" button
        view_button = driver.find_element_by_id('confirmLink')
        view_button.click()
        
        # Remove old file while waiting to load
        if os.path.isfile(paths['download_filepath']):
            os.remove(paths['download_filepath'])
        
        # Wait 2 seconds before switching frames
        sleep(2)

        driver.switch_to.default_content()
        
        try:
            element = WebDriverWait(driver, 15).until(
                EC.frame_to_be_available_and_switch_to_it(0)
            )
        finally:
            print('switched to frame')

        try:
            element = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.ID, 'ReportViewer1_ctl05_ctl04_ctl00_ButtonImg'))
            )
        finally:
            print('got button')

        # wait 1 second to ensure button can be clicked
        sleep(2)


        # Save the data
        save_button = driver.find_element_by_id('ReportViewer1_ctl05_ctl04_ctl00_ButtonImg')
        save_button.click()

        try:
            element = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.LINK_TEXT, 'CSV (comma delimited)'))
            )
        finally:
            print('got csv button')

        # wait 1 second to ensure button can be clicked
        sleep(2)
        csv_button = driver.find_element_by_link_text("CSV (comma delimited)")
        csv_button.click()

        driver.switch_to.default_content()
        
        print('saved ' + village_filepath)

        # 
        sleep(5)
        os.rename(paths['download_filepath'], village_filepath)



# %%
"""
# Load states from States dropdown
driver.switch_to.default_content()
state_dropdown = Select(driver.find_element_by_name("State_Code"))

states = []
states_index = []
for i in range(len(state_dropdown.options)):
    if i > 0:
        states.append(state_dropdown.options[i].get_attribute('innerText'))
        states_index.append(state_dropdown.options[i].get_attribute('index'))
        
smeta = {
        'states': states,
        'states_index': states_index
    }

for si in range(len(states_index)):
    # si = 4
    dmeta = get_state_districts(si, smeta, paths, driver)
    
    for di in range(len(dmeta['districts'])):
        # di = 4
        bmeta = get_district_subdists(di, dmeta, paths, driver)
        
        for bi in range(len(bmeta['subdists'])):
            # bi = 2
            vmeta = get_subdist_villages(bi, bmeta, paths, driver)
            
            for vi in range(len(vmeta['villages'])):
                # vi = 2
                download_village_data(vi, vmeta, paths, driver)



vi

bi

di

si

"""

