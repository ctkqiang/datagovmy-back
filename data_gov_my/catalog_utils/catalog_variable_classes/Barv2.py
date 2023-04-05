from data_gov_my.catalog_utils.catalog_variable_classes.Generalv2 import GeneralChartsUtil

import pandas as pd
import numpy as np
import json
from dateutil.relativedelta import relativedelta
from mergedeep import merge


class Bar(GeneralChartsUtil):
    """Bar Class for timeseries variables"""

    chart_type = ""

    # API related fields
    api_filter = []
    translations = {}

    # Chart related
    b_keys = []
    b_x = ""
    b_y = []

    """
    Initiailize the neccessary data for a bar chart
    """

    def __init__(self, full_meta, file_data, cur_data, all_variable_data, file_src):
        GeneralChartsUtil.__init__(self, full_meta, file_data, cur_data, all_variable_data, file_src)

        # Sets API details
        self.chart_type = self.chart['chart_type']
        self.api_filter = self.chart["chart_filters"]["SLICE_BY"]
        self.api = self.build_api_info()

        # Sets chart details
        self.b_keys = self.chart["chart_variables"]["parents"]
        self.b_x = self.chart["chart_variables"]["format"]["x"]
        self.b_y = self.get_y_values()

        # Builds the chart
        self.chart_details["chart"] = self.chart_v2()

        # Sets the catalog data within db input
        self.db_input["catalog_data"] = self.build_catalog_data_info()

    """
    Chart builder version 2
    """
    def chart_v2(self) :
        result = {}
        has_date = False

        df = pd.read_parquet(self.read_from)

        if 'date' in df.columns : 
            self.b_keys.insert(0, 'date')
            has_date = True

        if len(self.b_keys) > 0 : 
            result = self.build_chart_parents(has_date)
        else : 
            result = self.build_chart_self()

        return result

    """
    Builds chart data with 0 nested keys
    """
    def build_chart_self(self) :
        df = pd.read_parquet(self.read_from)
        df = df.replace({np.nan: None})        

        c_vals = {} # Chart Values
        t_vals = {} # Table Values

        t_columns = self.set_table_columns(False)

        rename_cols = {}
        rename_cols[self.b_x] = 'x'

        c_vals['x'] = df[self.b_x].to_list()

        for index, y in enumerate(self.b_y):
            y_list = df[y].to_list()
            y_val = f"y{ index + 1 }"
            rename_cols[y] = y_val
            c_vals[y_val] = y_list
        
        t_vals = (
            df.rename(columns=rename_cols)[list(rename_cols.values())]
            .to_dict("records")
        )        

        overall = {}
        overall["chart_data"] = c_vals
        overall["table_data"] = {}
        overall["table_data"]["columns"] = t_columns
        overall["table_data"]["data"] = t_vals  

        return overall

    """
    Build the Bar chart
    """

    def build_chart_parents(self, has_date):
        df = pd.read_parquet(self.read_from)
        df = df.replace({np.nan: None})

        # Converts all values to : 
        # - A str if its an object
        # - A str with lowercase, and spaces as hyphen

        for key in self.b_keys:
            if df[key].dtype == "object" :
                df[key] = df[key].astype(str)            
            df[key] = df[key].apply(lambda x: x.lower().replace(" ", "-"))

        # Gets all unique groups
        df["u_groups"] = list(df[self.b_keys].itertuples(index=False, name=None))
        u_groups_list = df["u_groups"].unique().tolist()

        chart_res = {}
        table_res = {}
        date_list = None

        if has_date : 
            date_list = df['date'].unique().tolist()
            self.api['has_date'] = date_list[0]

        table_columns = self.set_table_columns(has_date)

        for group in u_groups_list:
            result = {}
            tbl = {}
            for b in group[::-1]:
                result = {b: result}
                tbl = {b: tbl}
            group_l = list(group)

            if len(group) == 1 : 
                group = group[0]
            
            x_list = df.groupby(self.b_keys)[self.b_x].get_group(group).to_list()

            rename_columns = {self.b_x: "x"} # Dict to rename columns for table
            chart_vals = {"date" : date_list, "x": x_list} # Extracted chart values

            # Gets y-values for chart
            for index, y in enumerate(self.b_y):
                y_list = df.groupby(self.b_keys)[y].get_group(group).to_list()
                y_val = f"y{index + 1}"
                rename_columns[y] = y_val
                chart_vals[y_val] = y_list

            # Gets y-values for table
            table_vals = (
                df.rename(columns=rename_columns)
                .groupby(self.b_keys)[list(rename_columns.values())]
                .get_group(group)
                .to_dict("records")
            )

            final_d = chart_vals
            self.set_dict(result, group_l, final_d)
            self.set_dict(tbl, group_l, table_vals)
            merge(chart_res, result)
            merge(table_res, tbl)

        overall = {}
        overall["chart_data"] = chart_res
        overall["table_data"] = {}
        overall["table_data"]["columns"] = table_columns
        overall["table_data"]["data"] = table_res 

        return overall

    """
    Set table columns
    """
    def set_table_columns(self, has_date) :
        res = {}

        res["en"] = {}
        res["bm"] = {}

        if has_date : 
            res['en']['date'] = "Date"
            res['bm']['date'] = "Tarikh"


        if self.translations:
            res['en']['x'] = self.translations["x_en"]
            res['bm']['x'] = self.translations["x_bm"]

            for y_lang in ["en", "bm"] :
                y_list = self.translations[f"y_{y_lang}"]
                for index, c_y in enumerate(y_list):
                    y_val = f"y{ index + 1}"
                    res[y_lang][y_val] = c_y
        else:
            res["en"]["x"] = self.b_x
            res["bm"]["x"] = self.b_x

            for index, y in enumerate(self.b_y):
                for y_lang in ["en", "bm"]:
                    y_val = f"y{ index + 1}"
                    res[y_lang][y_val] = y

        return res       

    """
    Builds the API info for Bar
    """

    def build_api_info(self):
        res = {}

        df = pd.read_parquet(self.read_from)
        api_filters_inc = []

        if self.api_filter:
            for api in self.api_filter:
                fe_vals = df[api].unique().tolist()
                be_vals = (
                    df[api]
                    .apply(lambda x: x.lower().replace(" ", "-"))
                    .unique()
                    .tolist()
                )
                api_obj = self.build_api_object_filter(
                    api, fe_vals[0], be_vals[0], dict(zip(fe_vals, be_vals))
                )
                api_filters_inc.append(api_obj)

        res["API"] = {}
        res["API"]["filters"] = api_filters_inc
        res["API"]["precision"] = self.precision
        res["API"]["chart_type"] = self.chart["chart_type"]

        return res["API"]

    """
    Returns the appropriate y-values
    """
    def get_y_values(self) :
        y_values = self.chart["chart_variables"]["format"]["y"]

        if isinstance(y_values, str) :
            return [y_values]
        
        return y_values