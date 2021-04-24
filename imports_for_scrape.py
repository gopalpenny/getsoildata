#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 24 16:12:19 2021

@author: gopal
"""

# All of these are imports needed for scraping_india_soilhealth_final.py

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