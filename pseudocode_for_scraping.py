#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 22 18:26:26 2021

@author: gopal
"""

# %%
paths = {'data_filepath': "/Users/gopal/Projects/DataScience/india_soilhealth/data",
         'index_filepath': "/Users/gopal/Projects/DataScience/india_soilhealth/index",
         'download_filepath': "/Users/gopal/Downloads/NutrientsStatusReportFarmerWise.csv"
}



    state_districts_df = pd.DataFrame(data, columns = ['State', 'District'])
    state_filepath = os.path.join(paths['index_filepath'], state_name + "_districts.csv")
    state_districts_df.to_csv(state_filepath)
    
x = 1
# %%
# The general strategy is:
If states file exists:
    Load states file
Else:
    look up states from website
    save states from website

For each state in states:
    state_set = 0 # when beginning state, not that it has not yet been set in driver
    If state_districts file exists:
        Load state_districts
    Else:
        Look up state_districts from website
        Save state_districts from website
    
    For each district in districts:
        district_set = 0 # when beginning district, not that it has not yet been set in driver
        
        If district_subdistricts file exists:
            Load district_subdistricts
        Else:
            Look up district_subdistricts from website
            Save district_subdistricts from website
        
        For each subdistrict in subdistricts:
            subdistrict_set = 0 # when beginning subdistrict, not that it has not yet been set in driver
        
            If subdistrict_vilages file exists:
                Load subdistrict_vilages
            Else:
                Look up subdistrict_vilages from website
                Save subdistrict_vilages from website
            
            For each village in villages:
                
                If village file already exists:
                    return
                Else:
                    if state_set == 0:
                        set state
                        state_set = 1
                    if district_set == 0:
                        set district
                        district_set = 1
                    if subdistrict_set == 0:
                        set subdistrict
                        subdistrict_set = 1
                    set village, DOWNLOAD DATA
            