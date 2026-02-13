"""
股票基本信息查询工具
提供股票代码/名称转换、概念板块查询、风险提示等功能
"""

import sys
import io
import json
import numpy as np
import pandas as pd
import tushare as ts

# 设置UTF-8输出编码
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

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


def tran_code(codes):
    """转换股票代码为标准格式"""
    codes_t = []
    for i in codes:
        a = "".join(filter(str.isdigit, i))
        codes_t.append(a)
    for i in range(len(codes_t)):
        if codes_t[i][0] == '6':
            codes_t[i] = codes_t[i] + '.SH'
        else:
            codes_t[i] = codes_t[i] + '.SZ'
    return codes_t


def code_to_name(content):
    """股票代码和股票名称互转"""
    if isinstance(content, str):
        content = [content]

    if content[0][0].isdigit():
        mode = 'to_name'
    else:
        mode = 'to_code'

    if mode == 'to_name':
        content = tran_code(content)

    all_df = pro.stock_basic(exchange='', list_status='L', fields='ts_code,name')
    all_df.columns = ['code', 'name']
    if mode == 'to_name':
        result = all_df.loc[all_df.code.isin(content)]
    elif mode == 'to_code':
        result = all_df.loc[all_df.name.isin(content)]
    return result


def code_name_transformer(content: str) -> str:
    """
    股票代码和名称互转

    Args:
        content: 股票代码或名称

    Returns:
        str: CSV格式的转换结果
    """
    try:
        result = code_to_name(content)
        return result.to_csv(index=False)
    except Exception as e:
        return f"error,{str(e)}"


def get_meme(code):
    """获取概念板块"""
    if not ADATA_AVAILABLE:
        return pd.DataFrame(columns=["name", "reason"])
    try:
        meme = adata.stock.info.get_concept_ths(code)
        if meme is None or meme.empty:
            return pd.DataFrame(columns=["name", "reason"])
        return meme[["name", "reason"]]
    except Exception:
        return pd.DataFrame(columns=["name", "reason"])


def get_industry(code):
    """获取行业板块"""
    if not ADATA_AVAILABLE:
        return pd.DataFrame(columns=["plate_name"])
    try:
        indus = adata.stock.info.get_plate_east(code, 1)
        if indus is None or indus.empty:
            return pd.DataFrame(columns=["plate_name"])
        return indus[['plate_name']]
    except Exception:
        return pd.DataFrame(columns=["plate_name"])


def get_risk(code):
    """获取风险提示"""
    if not ADATA_AVAILABLE:
        return pd.DataFrame(columns=["t_type", "reason"])
    try:
        risk = adata.sentiment.mine.mine_clearance_tdx(code)
        if risk is None or risk.empty:
            return pd.DataFrame(columns=["t_type", "reason"])
        risk = risk[['t_type', 'reason']]
        risk = risk.replace(np.nan, '无')
        return risk
    except Exception:
        return pd.DataFrame(columns=["t_type", "reason"])


def query_stock_info(codes: list[str]) -> str:
    """
    查询股票信息（概念、行业、风险）

    Args:
        codes: 股票代码列表

    Returns:
        str: CSV格式的股票信息
    """
    if not ADATA_AVAILABLE:
        return "error,adata库未安装，请运行: pip install adata"

    all_results = []
    for code in codes:
        try:
            clean_code = "".join(filter(str.isdigit, code))

            meme = get_meme(clean_code)
            meme['stock_code'] = code

            indus = get_industry(clean_code)
            indus['stock_code'] = code

            risk = get_risk(clean_code)
            risk['stock_code'] = code

            # 构建CSV格式输出
            result = f"# {code} 股票信息\n## 概念\n{meme.to_csv(index=False)}\n## 行业板块\n{indus.to_csv(index=False)}\n## 风险提示\n{risk.to_csv(index=False)}\n"
            all_results.append(result)
        except Exception as e:
            all_results.append(f"# {code} 数据获取失败: {str(e)}\n")

    return "\n".join(all_results)


if __name__ == "__main__":
    # 命令行调用格式:
    # python stock_inform.py code_name_transformer "平安银行"
    # python stock_inform.py query_stock_info "000001.SZ"

    if len(sys.argv) < 2:
        print("用法:")
        print("  python stock_inform.py code_name_transformer <股票代码或名称>")
        print("  python stock_inform.py query_stock_info <股票代码>")
        sys.exit(1)

    action = sys.argv[1]

    if action == "code_name_transformer" and len(sys.argv) > 2:
        content = sys.argv[2]
        result = code_name_transformer(content)
        print(result)

    elif action == "query_stock_info" and len(sys.argv) > 2:
        code = sys.argv[2]
        result = query_stock_info([code])
        print(result)

    else:
        print("用法:")
        print("  python stock_inform.py code_name_transformer <股票代码或名称>")
        print("  python stock_inform.py query_stock_info <股票代码>")