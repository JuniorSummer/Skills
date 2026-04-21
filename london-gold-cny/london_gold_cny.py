#!/usr/bin/env python3
"""
伦敦金人民币价格查询
查询伦敦金（现货黄金）价格，自动输出人民币/克和美元/盎司双单位价格
"""

import json
import os
import sys
import urllib.request
import urllib.error
from datetime import datetime

# 1 盎司 = 31.1034768 克
OUNCE_TO_GRAM = 31.1034768


def get_jisu_gold_price(api_key):
    """从极速数据JisuAPI获取伦敦金价格"""
    # 使用伦敦金专用接口
    url = f"https://api.jisuapi.com/gold/london?appkey={api_key}"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
            if data.get('status') != 0:  # status 是整数 0，不是字符串 '0'
                return None
            # 查找伦敦金数据
            for item in data.get('result', []):
                if '伦敦金' in item.get('type', ''):
                    return item
            return None
    except Exception as e:
        print(f"JisuAPI error: {e}", file=sys.stderr)
        return None


def get_usd_cny_rate():
    """获取美元兑人民币汇率"""
    try:
        # 使用 exchangerate-api 或备用接口
        urls = [
            "https://api.exchangerate-api.com/v4/latest/USD",
            "https://open.er-api.com/v6/latest/USD",
        ]
        
        for url in urls:
            try:
                req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req, timeout=10) as response:
                    data = json.loads(response.read().decode('utf-8'))
                    rate = data.get('rates', {}).get('CNY')
                    if rate:
                        return float(rate)
            except:
                continue
    except Exception as e:
        print(f"Rate API error: {e}", file=sys.stderr)
    
    # 默认汇率
    return 7.25


def usd_ounce_to_cny_gram(usd_per_ounce, exchange_rate):
    """将美元/盎司转换为人民币/克"""
    # 1 盎司 = 31.1034768 克
    OUNCE_TO_GRAM = 31.1034768
    return (usd_per_ounce * exchange_rate) / OUNCE_TO_GRAM


def format_output_jisu(gold_data, exchange_rate):
    """格式化JisuAPI输出"""
    # 极速数据的 price 是 美元/盎司
    price_usd_per_ounce = float(gold_data.get('price', 0))
    open_usd = float(gold_data.get('openingprice', gold_data.get('price', 0)))
    high_usd = float(gold_data.get('maxprice', gold_data.get('price', 0)))
    low_usd = float(gold_data.get('minprice', gold_data.get('price', 0)))
    prev_close_usd = float(gold_data.get('lastclosingprice', gold_data.get('price', 0)))
    
    # 转换为人民币/克: 美元/盎司 * 汇率 / 31.1
    cny_per_gram = price_usd_per_ounce * exchange_rate / OUNCE_TO_GRAM
    open_cny_gram = open_usd * exchange_rate / OUNCE_TO_GRAM
    high_cny_gram = high_usd * exchange_rate / OUNCE_TO_GRAM
    low_cny_gram = low_usd * exchange_rate / OUNCE_TO_GRAM
    prev_close_cny_gram = prev_close_usd * exchange_rate / OUNCE_TO_GRAM
    
    updatetime = gold_data.get('updatetime', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    change_amount = gold_data.get('changequantity', '0')
    change_percent = gold_data.get('changepercent', '0%')
    
    result = {
        "品种": "伦敦金",
        "更新时间": updatetime,
        "汇率": {
            "美元兑人民币": round(exchange_rate, 4)
        },
        "美元价格(美元/盎司)": {
            "当前价": round(price_usd_per_ounce, 2),
            "开盘价": round(open_usd, 2),
            "最高价": round(high_usd, 2),
            "最低价": round(low_usd, 2),
            "昨收价": round(prev_close_usd, 2)
        },
        "人民币价格(元/克)": {
            "当前价": round(cny_per_gram, 2),
            "开盘价": round(open_cny_gram, 2),
            "最高价": round(high_cny_gram, 2),
            "最低价": round(low_cny_gram, 2),
            "昨收价": round(prev_close_cny_gram, 2)
        },
        "涨跌": {
            "涨跌额": change_amount,
            "涨跌幅": change_percent
        },
        "单位说明": "人民币/克 (按当前汇率换算，仅供参考)",
        "数据来源": "极速数据 JisuAPI"
    }
    
    return result



def main():
    """主函数 - 只使用极速数据JisuAPI"""
    # 获取汇率
    exchange_rate = get_usd_cny_rate()
    
    # 使用JisuAPI
    api_key = os.environ.get('JISU_API_KEY')
    
    if not api_key:
        error_result = {
            "错误": "未配置 JISU_API_KEY 环境变量",
            "时间": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "说明": "请配置极速数据API Key"
        }
        print(json.dumps(error_result, ensure_ascii=False, indent=2))
        sys.exit(1)
    
    gold_data = get_jisu_gold_price(api_key)
    if gold_data:
        result = format_output_jisu(gold_data, exchange_rate)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return
    
    # 获取失败
    error_result = {
        "错误": "无法获取伦敦金价格数据",
        "时间": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "说明": "极速数据API不可用，请检查网络或API Key"
    }
    print(json.dumps(error_result, ensure_ascii=False, indent=2))
    sys.exit(1)


if __name__ == '__main__':
    main()
