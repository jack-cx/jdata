#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2024/4/29 15:00
Desc: 东方财富网-数据中心-特色数据-停复牌信息
https://data.eastmoney.com/tfpxx/
"""

import pandas as pd
import requests
from typing import List

SCRAP_PAGE_SIZE = 25

def stock_tfp_em(date: str = "20240426") -> pd.DataFrame:
    """
    东方财富网-数据中心-特色数据-停复牌信息
    https://data.eastmoney.com/tfpxx/
    :param date: specific date as "2020-03-19"
    :type date: str
    :return: 停复牌信息表
    :rtype: pandas.DataFrame
    """
    url = "https://datacenter-web.eastmoney.com/api/data/v1/get"
    params = {
        "sortColumns": "SUSPEND_START_DATE",
        "sortTypes": "-1",
        "pageSize": "500",
        "pageNumber": "1",
        "reportName": "RPT_CUSTOM_SUSPEND_DATA_INTERFACE",
        "columns": "ALL",
        "source": "WEB",
        "client": "WEB",
        "filter": f"""(MARKET="全部")(DATETIME='{"-".join([date[:4], date[4:6], date[6:]])}')""",
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    total_page = data_json["result"]["pages"]
    big_df = pd.DataFrame()
    for page in range(1, total_page + 1):
        params.update({"pageNumber": page})
        r = requests.get(url, params=params)
        data_json = r.json()
        temp_df = pd.DataFrame(data_json["result"]["data"])
        big_df = pd.concat(objs=[big_df, temp_df], ignore_index=True)

    big_df.reset_index(inplace=True)
    big_df.columns = [
        "序号",
        "代码",
        "名称",
        "停牌时间",
        "停牌截止时间",
        "停牌期限",
        "停牌原因",
        "所属市场",
        "停牌开始日期",
        "预计复牌时间",
        "-",
        "-",
    ]
    big_df = big_df[
        [
            "序号",
            "代码",
            "名称",
            "停牌时间",
            "停牌截止时间",
            "停牌期限",
            "停牌原因",
            "所属市场",
            "预计复牌时间",
        ]
    ]
    big_df["停牌时间"] = pd.to_datetime(big_df["停牌时间"], errors="coerce").dt.date
    big_df["停牌截止时间"] = pd.to_datetime(
        big_df["停牌截止时间"], errors="coerce"
    ).dt.date
    big_df["预计复牌时间"] = pd.to_datetime(
        big_df["预计复牌时间"], errors="coerce"
    ).dt.date
    return big_df

def sse_tpf(date_begin: str, date_end: str) -> pd.DataFrame:
    """_summary_
    上证交易所停复牌信息
    https://www.sse.com.cn/disclosure/dealinstruc/suspension/

    Args:
        date_begin (str): 起始时间  
        date_end (str): 截止时间

    Returns:
        pd.DataFrame: 返回停牌数据
    """

    url = "https://query.sse.com.cn/sseQuery/commonQuery.do"
    headers = {
        "Host": "query.sse.com.cn",
        "Pragma": "no-cache",
        "Referer": "https://www.sse.com.cn/assortment/stock/list/share/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/81.0.4044.138 Safari/537.36",
    }

    _begin = 1

    parms = {
        "isPagination": "true",
        "sqlId": "COMMON_SSE_XXPL_JYTS_TFPXX_L",
        "SEARCH_DATE": date,
        "pageHelp.pageSize": 1,
        "pageHelp.pageNo": _begin,
        "pageHelp.beginPage": _begin,
        "pageHelp.cacheSize": 1, 
        "pageHelp.endPage": _begin,
        "_": "1716875453016"
    }
    data_ret = []
    try:
        r = requests.get(url, params=parms, headers=headers)
        data = r.json()
        total_cnt = data['pageHelp']['total']
        left = total_cnt
        _begin = 1
        while (left > 0):
            page_size = SCRAP_PAGE_SIZE if left >= SCRAP_PAGE_SIZE else left
            parms.update({"pageHelp.pageSize": page_size})
            r = requests.get(url, params=parms, headers=headers)
            data = r.json()
            _tfp_data = data['result']
            data_ret.extend(_tfp_data)
            _begin = _begin + 1
            parms.update({
                "pageHelp.pageNo": _begin,
                "pageHelp.beginPage": _begin,
                "pageHelp.endPage": _begin,
            })
            left = left - page_size
            
    except Exception as e:
        return None
    
    return data_ret

def szse_tpf(date_begin: str, date_end: str) -> List:
    """
    深交所停复牌信息
    https://www.szse.cn/disclosure/memo/index.html
    Args:
        date_begin (str): 起始时间
        date_end (str): 截止时间

    Returns:
        List: _description_
    """
    return 

def bse_tpf(date_begin: str, date_end: str) -> List:
    return

def stock_tfp_detail(date_begin: str, date_end: str) -> pd.DataFrame:
    """
    沪深北交易所停复牌信息
    :param date_begin date_end: specific date as "2020-03-19" or "20200319"
    :type date: str
    :return: 停复牌信息表
    :rtype: pandas.DataFrame
    """

    _data_sse = sse_tpf(date_begin)

    return _data_sse

if __name__ == "__main__":
    stock_tfp_em_df = stock_tfp_em(date="20240426")
    print(stock_tfp_em_df)

    tfp_sse = stock_tfp_detail(date="2024-05-28")
    print(tfp_sse)
