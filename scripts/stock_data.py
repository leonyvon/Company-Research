"""
股票财务数据查询工具
提供财务数据、股东数据、新闻资讯获取功能
"""

import sys
import json
import datetime
import pandas as pd
import tushare as ts

# Tushare API配置
TUSHARE_TOKEN = "f0ab2f26a58d6e62cda77f4a8418c324fbc6dfd5d702fa1fc0a2d870"
pro = ts.pro_api(TUSHARE_TOKEN)

# 清除代理
import os
for env_var in ['HTTP_PROXY', 'HTTPS_PROXY', 'http_proxy', 'https_proxy', 'NO_PROXY', 'no_proxy']:
    os.environ[env_var] = ''

try:
    import adata
    ADATA_AVAILABLE = True
except ImportError:
    ADATA_AVAILABLE = False

try:
    import akshare as ak
    AKSHARE_AVAILABLE = True
except ImportError:
    AKSHARE_AVAILABLE = False


def get_holder_data(code):
    """获取股东数据"""
    end = datetime.datetime.now().date()
    start = end - datetime.timedelta(days=365)
    end = end.strftime("%Y%m%d")
    start = start.strftime("%Y%m%d")

    # 股东数变化
    df1 = pro.stk_holdernumber(
        ts_code=code,
        start_date=start,
        end_date=end,
        fields="ts_code,ann_date,holder_num",
    )
    df1 = df1.rename(columns={"ts_code": "code", "ann_date": "time"})
    df1.time = pd.to_datetime(df1.time)
    df1 = df1.sort_values("time")
    df1 = df1.drop_duplicates(subset="holder_num", keep="last").drop_duplicates(
        "time", keep="last"
    )
    df1 = df1.dropna()
    df1.time = df1.time.dt.strftime("%Y%m%d")

    # 十大流通股东
    df2 = pro.top10_floatholders(ts_code=code, start_date=start, end_date=end)
    df2 = df2.rename(columns={"ts_code": "code", "ann_date": "time"})
    df2.time = pd.to_datetime(df2.time)
    newest_time = df2.time.max()
    df2 = df2[df2.time == newest_time]
    nan_data = df2.loc[df2.hold_change.isnull(), 'hold_change']
    df2.loc[df2.hold_change.isnull(), 'hold_change'] = df2.loc[nan_data.index, 'hold_amount']
    df2['hold_change'] = df2['hold_change'] / df2['hold_amount']
    df2.drop(["hold_amount", "time"], axis=1, inplace=True)

    # 十大股东
    df3 = pro.top10_holders(ts_code=code, start_date=start, end_date=end)
    df3 = df3.rename(columns={"ts_code": "code", "ann_date": "time"})
    df3.time = pd.to_datetime(df3.time)
    newest_time = df3.time.max()
    df3 = df3[df3.time == newest_time]
    nan_data = df3.loc[df3.hold_change.isnull(), 'hold_change']
    df3.loc[df3.hold_change.isnull(), 'hold_change'] = df3.loc[nan_data.index, 'hold_amount']
    df3['hold_change'] = df3['hold_change'] / df3['hold_amount']
    df3.drop(["hold_amount", "time"], axis=1, inplace=True)

    return df1, df2, df3


def holder_data_handler(codes: list[str]) -> str:
    """获取股东数据"""
    all_results = []

    for code in codes:
        try:
            holdernum, float_top10, top10 = get_holder_data(code)
            holdernum['stock_code'] = code
            float_top10['stock_code'] = code
            top10['stock_code'] = code

            result = f"# {code} 近一年股东数据\n## 股东数\n{holdernum.to_csv(index=False)}\n## 十大流通股东\n{float_top10.to_csv(index=False)}\n## 十大股东\n{top10.to_csv(index=False)}\n"
            all_results.append(result)
        except Exception as e:
            all_results.append(f"# {code} 数据获取失败: {str(e)}\n")

    return "\n".join(all_results)


def financial_data_handler(codes: list[str]) -> str:
    """获取财务数据"""
    if not ADATA_AVAILABLE:
        return "error,adata库未安装，请运行: pip install adata"

    end = datetime.datetime.now()
    start = (end - datetime.timedelta(days=365)).strftime("%Y%m%d")
    end = end.strftime("%Y%m%d")

    all_results = []

    for code in codes:
        try:
            # 估值数据
            df = pro.daily_basic(
                ts_code=code,
                start_date=start, end_date=end,
                fields='trade_date,pe,pe_ttm,pb,ps,ps_ttm,dv_ratio,dv_ttm,total_mv,circ_mv'
            )
            df['total_mv'] *= 10000
            df['circ_mv'] *= 10000
            df = df.set_index("trade_date").sort_index()
            df_250_describe = df.iloc[-250:].describe(percentiles=[.1, .25, .5, .75, .9])
            df_newest = df.iloc[[-1]].copy()
            df_newest.index = ['current']
            value_df = pd.concat([df_250_describe, df_newest]).reset_index()
            value_df['stock_code'] = code
            value_df = value_df.astype(str)

            # 核心财务指标
            pure_code = "".join(filter(str.isdigit, code))
            df = adata.stock.finance.get_core_index(pure_code)

            df['report_date'] = pd.to_datetime(df['report_date'])
            df = df.sort_values("report_date", ascending=True)
            target_dates = df['report_date'].unique()[-12:].tolist()
            target_df = df[df['report_date'].isin(target_dates)].copy()
            target_df.drop(['stock_code', 'short_name'], axis=1, inplace=True, errors='ignore')
            target_df.drop(['total_asset_turn_days', 'inv_turn_days', 'acct_recv_turn_days'],
                          axis=1, inplace=True, errors='ignore')
            target_df['report_date'] = target_df['report_date'].dt.strftime("%Y-%m-%d")
            target_df['stock_code'] = code
            target_df = target_df.astype(str)

            result = f"# {code} 财务与估值数据\n## 近12期核心财务指标\n{target_df.to_csv(index=False)}\n## 近一年估值统计\n{value_df.to_csv(index=False)}\n"
            all_results.append(result)
        except Exception as e:
            all_results.append(f"# {code} 数据获取失败: {str(e)}\n")

    return "\n".join(all_results)


def news_handler(keyword: list) -> str:
    """搜索金融资讯"""
    if not AKSHARE_AVAILABLE:
        return "error,akshare库未安装，请运行: pip install akshare"

    all_news = "# 新闻简报\n"
    for kw in keyword:
        all_news += f"\n关键词: {kw}\n"
        try:
            news_df = ak.stock_news_em(symbol=kw)
            news_df = news_df[
                news_df["文章来源"].isin(
                    ['证券时报网', "证券时报", "证券日报", "第一财经", '财联社', "财中社",
                     "中国证券报", "中国经济网", "新华社", "新华财经",
                     "中国新闻网", "每日经济新闻", "东方财富研究中心",
                     "经济参考报", "经济日报", "人民日报"]
                )
            ]
            news_df = news_df[['新闻标题', '新闻内容', '发布时间']]
            news_df.columns = ['title', 'content', 'pub_time']
            news_df.drop_duplicates(subset="title", keep='first', inplace=True)
            now = datetime.datetime.now()
            news_df.pub_time = pd.to_datetime(news_df.pub_time)
            news_df = news_df[news_df.pub_time >= now - datetime.timedelta(days=10)]
            news_df.sort_values("pub_time", inplace=True)
            result = news_df.to_csv(index=False)
            all_news += result + "\n"
        except Exception as e:
            all_news += f"获取新闻失败: {str(e)}\n"

    return all_news


if __name__ == "__main__":
    # 命令行调用格式:
    # python stock_data.py holder_data_handler "000001.SZ"
    # python stock_data.py financial_data_handler "000001.SZ"
    # python stock_data.py news_handler "平安银行"

    if len(sys.argv) < 2:
        print("用法:")
        print("  python stock_data.py holder_data_handler <股票代码>")
        print("  python stock_data.py financial_data_handler <股票代码>")
        print("  python stock_data.py news_handler <关键词>")
        sys.exit(1)

    action = sys.argv[1]

    if action == "holder_data_handler" and len(sys.argv) > 2:
        code = sys.argv[2]
        result = holder_data_handler([code])
        print(result)

    elif action == "financial_data_handler" and len(sys.argv) > 2:
        code = sys.argv[2]
        result = financial_data_handler([code])
        print(result)

    elif action == "news_handler" and len(sys.argv) > 2:
        keyword = sys.argv[2:]
        result = news_handler(keyword)
        print(result)

    else:
        print("用法:")
        print("  python stock_data.py holder_data_handler <股票代码>")
        print("  python stock_data.py financial_data_handler <股票代码>")
        print("  python stock_data.py news_handler <关键词>")