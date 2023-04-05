from data_gov_my.catalog_utils.catalog_variable_classes.Generalv2 import GeneralChartsUtil

import pandas as pd
import numpy as np
import json
from dateutil.relativedelta import relativedelta
from mergedeep import merge


class CatalogueDataHandler() :

    def __init__(self, chart_type, data, params) :
        self._chart_type = chart_type
        self._data = data
        self._params = params

    
    def get_results(self) :
        if self._chart_type == 'BAR' or self._chart_type == 'HBAR' :
            return self.bar_handler()

    def bar_handler(self) :
        lang = self.default_param_value('lang', 'en', self._params)

        intro = self._data["chart_details"]["intro"]  # Get intro
        table_data = self._data["chart_details"]["chart"]["table_data"]["data"]
        table_cols = self._data["chart_details"]["chart"]["table_data"]["columns"]
        chart_data = self._data["chart_details"]["chart"]["chart_data"]  # Get chart data

        defaults_api = {} # Creates a default API

        has_date = self.chart_has_date(self._data["API"])

        if has_date : 
            defaults_api["date_range"] = has_date
            self._data["API"].pop("has_date")

        for d in self._data["API"]["filters"]: # Gets all the default API values
            defaults_api[d["key"]] = d["default"]["value"]

        for k, v in defaults_api.items():
            key = self._params[k][0] if k in self._params else v
            if ( key in table_data ) and ( key in chart_data ):
                table_data = table_data[key]
                chart_data = chart_data[key]
            else:
                tbl_data = {}
                chart = {}
                break
        
        self.extract_lang(lang)

        table = {}
        table["columns"] = table_cols[lang]
        table["data"] = table_data

        res = {}
        res["chart_data"] = chart_data
        res["table_data"] = table
        res["intro"] = self.extract_lang_intro(lang, intro)

        self._data["chart_details"] = res
        
        return self._data
    

    '''
    Check if a chart has a date range element
    '''
    def chart_has_date(self, api_data) :
        if 'has_date' in api_data :
            return api_data['has_date']

        return None
    
    '''
    Sets default if key isn't in request parameters
    '''
    def default_param_value(self, key, default, params) :
        if key in params : 
            return params[key][0]
        
        return default
    
    '''
    Extract languages in other parts of the meta
    '''
    def extract_lang(self, lang) :
        temp = self._data["metadata"]["dataset_desc"][lang]
        self._data["metadata"]["dataset_desc"] = temp

        temp = self._data["explanation"][lang]
        self._data["explanation"] = temp

    '''
    Extract languages from intro key
    '''
    def extract_lang_intro(self, lang, intro) :
        lang_info = intro[lang]
        intro.pop("en")
        intro.pop("bm")
        intro.update(lang_info)
        return intro


