#!/usr/bin/env python
# coding: utf-8

#from imports_for_scrape import *

from time import sleep
from selenium import webdriver
from pathlib import Path
#from selenium.webdriver.common.keys import Keys


from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#from bs4 import BeautifulSoup
#import requests
import os
#import subprocess
import re
from datetime import datetime, timezone, timedelta
import pandas as pd
import numpy as np



# %%
def get_state_districts(si, smeta, paths, driver, select_params):
    """
    This function obtains all districts for the given state
        1. If state_filepath, loads district directly
        2. Otherwise, scrape districts from driver and save to filepath
    si: index of states in smeta
    smeta: dictionary containing metadata of states, including 'states' (state names), 'states_index' (index)
    paths: dictionary of paths to data, index, and download directories
    driver: selenium driver for webpage
    """

    # si = 4
    state_name = smeta['states'][si]
    state_filepath = os.path.join(paths['index_filepath'], state_name + "_districts.csv")
    
    if os.path.isfile(state_filepath):
        state_districts_df = pd.read_csv(state_filepath)
    else:
        
        state_dropdown = Select(driver.find_element_by_name("State_Code"))
        state_dropdown.select_by_index(smeta['states_index'][si])
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
                        districts,
                        districts_index))
    
        state_districts_df = pd.DataFrame(data, columns = ['State', 'District', 'Index'])
        state_districts_df.to_csv(state_filepath)
        
        
    
    dmeta = {
        'state_name': state_name,
        'districts': state_districts_df.District.tolist(),
        'districts_index': state_districts_df.Index.tolist()
    }
    return dmeta

# %%
def get_district_subdists(di, dmeta, paths, driver, select_params):
    # di = 1
    district_name = dmeta['districts'][di]
    district_filepath = os.path.join(paths['index_filepath'], dmeta['state_name'] + "-" + district_name + "_subdists.csv")
    
    if os.path.isfile(district_filepath):
        district_subdists_df = pd.read_csv(district_filepath)
    else:
    
        # If the state has not yet been selected -- select it
        if select_params['state_select'] == 0:
            state_dropdown = Select(driver.find_element_by_name("State_Code"))
            state_dropdown.select_by_visible_text(dmeta['state_name'])
            sleep(2)
        
        district_dropdown = Select(driver.find_element_by_name("District_Code"))
        district_dropdown.select_by_index(dmeta['districts_index'][di])
    
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
                        subdists,
                        subdist_index))
    
        district_subdists_df = pd.DataFrame(data, columns = ['State', 'District', 'Subdistrict','Index'])
        district_subdists_df.to_csv(district_filepath)

    bmeta = {
        'state_name': dmeta['state_name'],
        'district_name': district_name,
        'subdists': district_subdists_df.Subdistrict.tolist(),
        'subdist_index': district_subdists_df.Index.tolist()
    }

    return bmeta


# %%
    
#def check_if_villages_complete(subdistrict_village_table):
    


def get_subdist_villages(bi, bmeta, paths, driver, select_params):
    # bi = 1
    subdist_name = bmeta['subdists'][bi]
    subdistrict_filepath = os.path.join(paths['index_filepath'], bmeta['state_name'] + "-" + bmeta['district_name'] + "-" + subdist_name + "_villages.csv")
    
    if os.path.isfile(subdistrict_filepath):
        subdist_villages_df = pd.read_csv(subdistrict_filepath)
    else:
        subdist_dropdown = Select(driver.find_element_by_name("sub_district_code"))
        
        # If the state or district have not yet been selected -- select them and update select_params
        if select_params['state_select'] == 0:
            state_dropdown = Select(driver.find_element_by_name("State_Code"))
            state_dropdown.select_by_visible_text(bmeta['state_name'])
            sleep(2)
            
        if select_params['district_select'] == 0:
            district_dropdown = Select(driver.find_element_by_name("District_Code"))
            district_dropdown.select_by_visible_text(bmeta['district_name'])
            sleep(2)
            
        subdist_dropdown.select_by_index(bmeta['subdist_index'][bi])
        
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
                        villages,
                        villages_index))
    
        subdist_villages_df = pd.DataFrame(data, columns = ['State', 'District', 'Subdistrict', 'Village','Index'])
        subdist_villages_df.to_csv(subdistrict_filepath)
    
    # Get village info
    # for vi in range(len(villages_index)):
    vmeta = {
        'state_name': bmeta['state_name'],
        'district_name': bmeta['district_name'],
        'subdist_name': subdist_name,
        'villages': subdist_villages_df.Village.tolist(),
        'villages_index': subdist_villages_df.Index.tolist()
    }
    
    return vmeta

# %%
def download_village_data(vi, vmeta, paths, driver, select_params):
    
    village_name = vmeta['villages'][vi]
    village_filename = re.sub("[\s\/]","",
                          os.path.join(vmeta['state_name'] + "_" + vmeta['district_name'] + "_" + vmeta['subdist_name'] + "_" + village_name + ".csv"))


    
    village_filepath = os.path.join(paths['data_filepath'], village_filename)
    village_temp_filepath = re.sub("\.csv","_temp.txt",village_filepath)
    
    # Only fetch data for village if it does not already exist AND
    # if there is no temporary file corresponding to the village
    if not os.path.isfile(village_filepath) and not os.path.isfile(village_temp_filepath):
        Path(village_temp_filepath).touch()
        
        driver.switch_to.default_content()
        
        # If the state, district, and subdistrict have not yet been selected -- select them and update select_params
        if select_params['state_select'] == 0:
            state_dropdown = Select(driver.find_element_by_name("State_Code"))
            state_dropdown.select_by_visible_text(vmeta['state_name'])
            select_params['state_select'] = 1
            sleep(2)
            
        if select_params['district_select'] == 0:
            district_dropdown = Select(driver.find_element_by_name("District_Code"))
            district_dropdown.select_by_visible_text(vmeta['district_name'])
            select_params['district_select'] = 1
            sleep(2)
            
        if select_params['subdist_select'] == 0:
            subdist_dropdown = Select(driver.find_element_by_name("sub_district_code"))
            subdist_dropdown.select_by_visible_text(vmeta['subdist_name'])
            select_params['subdist_select'] = 1
            sleep(2)
        
        # Select village
        village_dropdown = Select(driver.find_element_by_name("Village_Code"))
        village_dropdown.select_by_index(vmeta['villages_index'][vi])
        select_params['village_select'] = 1
        sleep(1)

        # Click "View" button
        view_button = driver.find_element_by_id('confirmLink')
        view_button.click()
        
        ## Remove old file while waiting to load
        #if os.path.isfile(paths['download_filepath']):
        #    os.remove(paths['download_filepath'])
        
        # Wait 2 seconds before switching frames
        sleep(2)

        driver.switch_to.default_content()
        
        # Wait for web frame with table to exist
        try:
            element = WebDriverWait(driver, 15).until(
                EC.frame_to_be_available_and_switch_to_it(0)
            )
        finally:
            print('switched to frame')

        # Wait for save CSV button to be clickable
        try:
            element = WebDriverWait(driver,15).until(
                EC.element_to_be_clickable((By.ID, 'ReportViewer1_ctl05_ctl04_ctl00_ButtonImg'))
            )
        except:
            print('Save data button did not load within alotted time. Skipping ' + village_filename)
            # return select_params
        finally:
            print('Save button is clickable')
            
        
        # Wait for save CSV button to be selected
        try:
            element = WebDriverWait(driver,15).until(
                EC.visibility_of_element_located((By.ID, 'VisibleReportContentReportViewer1_ctl09'))
            )
        except:
            print('Visibility of table (VisibleReportContentReportViewer1_ctl09) no ID in alotted time. Skipping ' + village_filename)
            # return select_params
        finally:
            print('Table is visible')

        # wait 1 second to ensure button can be clicked
        sleep(1)


        # Save the data
        save_button = driver.find_element_by_id('ReportViewer1_ctl05_ctl04_ctl00_ButtonImg')
        save_button.click()

        try:
            element = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.LINK_TEXT, 'CSV (comma delimited)'))
            )
        except:
            print('Save CSV option did not load within alotted time. Skipping ' + village_filename)
            return select_params
        finally:
            print('CSV option is clickable')

        # wait 1 second to ensure button can be clicked
        sleep(2)
        csv_button = driver.find_element_by_link_text("CSV (comma delimited)")
        csv_button.click()

        driver.switch_to.default_content()

        # 
        sleep(5)
        downloaded_village_file = get_csv_file_matching_village_name(paths['download_path'], village_name)
        os.rename(downloaded_village_file, village_filepath)
        os.remove(village_temp_filepath)
        
        select_params['counter'] = select_params['counter'] + 1
        
        print('pid: ' + str(os.getpid()) + '. saved ' + village_filepath + '. Done with ' + str(select_params['counter']) + ' villages.\n')
        
    return select_params

# %%
def get_csv_file_matching_village_name(download_dir_path, village_name):
    
    current_time = datetime.now()
    download_filenames = [f for f in os.listdir(download_dir_path) if re.match('NutrientsStatusReportFarmerWise.*\.csv',f)]
    
    download_list = []
    for file in download_filenames:
        #file = temp_filenames[1]
        download_filepath = os.path.join(download_dir_path, file)
        mod_time = datetime.fromtimestamp(os.path.getmtime(download_filepath))
        if current_time - mod_time > timedelta(minutes=1):
            os.remove(download_filepath) # delete if file is more than a minute old
        else: # if file is within download timeframe
            file_village = pd.read_csv(download_filepath).village_name[1]
            if file_village.lower() == village_name.lower():
                download_list.append([village_name, mod_time, download_filepath])
    
    download_files = pd.DataFrame(download_list, columns = ['village', 'modtime', 'path'])
    
    if download_files.shape[0] == 0:
        print('no download files found with village matching ', village_name)
    
    return download_files.sort_values('modtime')['path'][0]
            
# %%



# %%

def run_soilhealth_scraper(project_path, download_path, N_villages = 1):
    
    paths = {'data_filepath': os.path.join(project_path, "data"),
         'index_filepath': os.path.join(project_path, "index"),
         'download_path': download_path
         }
    
    # Purge temporary files -- those in data that match .*_temp.txt
    current_time = datetime.now()
    temp_filenames = [f for f in os.listdir(paths['data_filepath']) if re.match('.*_temp\.txt',f)]
    
    for temp_file in temp_filenames:
        #file = temp_filenames[1]
        tempfile_path = os.path.join(paths['data_filepath'], temp_file)
        mod_time = datetime.fromtimestamp(os.path.getmtime(tempfile_path))
        if current_time - mod_time > timedelta(minutes=1):
            os.remove(tempfile_path)
    
    # start selenium driver and load webpage
    driver = webdriver.Chrome('/Users/gopal/opt/anaconda3/bin/chromedriver')
    driver.get("https://soilhealth.dac.gov.in/PublicReports/NutrientsStatusReportFarmerWise")
    
    # Load states from States dropdown
    driver.switch_to.default_content()
    state_dropdown = Select(driver.find_element_by_name("State_Code"))
    
    # Generate list of states from dropdown
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
    
    # Initialize select_params (this variable keeps track of what dropdowns
    # have been selected)
    select_params = {
            'counter': 0,
            'state_select': 0,
            'district_select': 0,
            'subdist_select': 0,
            'village_select': 0
            }
    
    # Loop through each state, district, subdistrict, and village -- grabbing N villages
    # At each level, this generates an index of the sub-level and saves to /index
    # For each village, it downloads a csv of the village (if the file isn't alread generated)
    # Note 1: a _temp.txt file is created for each village while it's processing to prevent other processes from doing the same village
    # Note 2: after the csv file is downloaded, the script checks the village before moving it to /data -- again to allow multiple processes to run at once
    for si in range(len(states_index)):
        # si = 4
        select_params['state_select'] = 0
        dmeta = get_state_districts(si, smeta, paths, driver, select_params)
        
        for di in range(len(dmeta['districts'])):
            # di = 4
            select_params['district_select'] = 0
            bmeta = get_district_subdists(di, dmeta, paths, driver, select_params)
            
            for bi in range(len(bmeta['subdists'])):
                # bi = 2
                select_params['subdist_select'] = 0
                vmeta = get_subdist_villages(bi, bmeta, paths, driver, select_params)
                
                for vi in range(len(vmeta['villages'])):
                    select_params['village_select'] = 0
                    # vi = 2
                    # Try to download each village. If it fails, skip, reset select_params, and proceed
                    try:
                        select_params = download_village_data(vi, vmeta, paths, driver, select_params)
                    except:
                        print('download_village_data for',vmeta['villages'][vi],
                              'village failed. skipping and resetting select_params.')
                        select_params['state_select'] =  0
                        select_params['district_select']= 0
                        select_params['subdist_select'] = 0
                        select_params['village_select'] = 0
                    finally:
                        if not select_params['village_select'] == 0:
                            print('moving to next')
                    
                    if select_params['counter'] >= N_villages:
                        driver.quit()
                        return(0)
    

# %%
if __name__ == '__main__':
    project_path = "/Users/gopal/Projects/DataScience/india_soilhealth"
    download_path = "/Users/gopal/Downloads"
    run_soilhealth_scraper(project_path, download_path, N_villages = 1)
