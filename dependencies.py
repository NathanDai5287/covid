import sys
import os

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import datetime
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta

import requests
import json
from difflib import get_close_matches
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from io import StringIO
from pathlib import Path
from icecream import ic
from functools import lru_cache, reduce
import pickle
from dotenv import load_dotenv
import warnings
from glob import glob

from conversion import Conversion
from location import Location
from pyautowebapi.api import Api
from clean import Clean

# variables
counties: pd.DataFrame = pd.read_csv('docs/counties.csv')

warnings.simplefilter(action='ignore', category=FutureWarning)
