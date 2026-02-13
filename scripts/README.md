# 公司深度调研工具 - 安装与使用说明

## 环境要求

- Python 3.8 或更高版本
- 推荐使用 conda 环境或 venv 虚拟环境

## 安装步骤

### 1. 安装依赖包

```bash
pip install -r requirements.txt
```

### 2. 配置 Tushare API Token

在脚本文件 `stock_inform.py` 和 `stock_data.py` 中，将 `TUSHARE_TOKEN` 替换为您自己的 Tushare Token。

获取 Token: https://tushare.pro/register

### 3. 配置 Ollama (可选)

如需使用智能搜索功能，需要安装并运行 Ollama：

```bash
# 安装 Ollama
# 访问 https://ollama.ai 下载安装

# 启动 Ollama 服务
ollama serve

# 安装 gemini-3-flash-preview:cloud
ollama pull gemini-3-flash-preview:cloud
```

## 脚本说明

### 1. ollama_searcher.py
智能搜索和摘要生成工具

**用法：**
```bash
python scripts/ollama_searcher.py "搜索关键词"
```

**示例：**
```bash
python scripts/ollama_searcher.py "贵州茅台 基本信息"
python scripts/ollama_searcher.py "人工智能 行业趋势 2025"
```

### 2. stock_inform.py
股票基本信息查询工具

**用法：**
```bash
# 股票代码/名称转换
python scripts/stock_inform.py code_name_transformer "平安银行"

# 查询股票信息
python scripts/stock_inform.py query_stock_info "000001.SZ"
```

**示例：**
```bash
# 代码转名称
python scripts/stock_inform.py code_name_transformer "000001"

# 名称转代码
python scripts/stock_inform.py code_name_transformer "平安银行"

# 查询股票信息
python scripts/stock_inform.py query_stock_info "000001.SZ"
```

### 3. stock_data.py
财务数据查询工具

**用法：**
```bash
# 获取股东数据
python scripts/stock_data.py holder_data_handler "000001.SZ"

# 获取财务数据
python scripts/stock_data.py financial_data_handler "000001.SZ"

# 搜索新闻
python scripts/stock_data.py news_handler "平安银行"
```

**示例：**
```bash
# 获取股东数据
python scripts/stock_data.py holder_data_handler "000001.SZ"

# 获取财务数据
python scripts/stock_data.py financial_data_handler "000001.SZ"

# 搜索新闻
python scripts/stock_data.py news_handler "平安银行"
python scripts/stock_data.py news_handler "平安银行" "业绩预告"
```

## 在 Claude Code 中的使用

### 使用 Bash 工具调用

```python
# 股票代码/名称转换
bash python "E:\\AI\\SKILLS\\company-research\\scripts\\stock_inform.py" code_name_transformer "平安银行"

# 查询股票信息
bash python "E:\\AI\\SKILLS\\company-research\\scripts\\stock_inform.py" query_stock_info "000001.SZ"

# 获取财务数据
bash python "E:\\AI\\SKILLS\\company-research\\scripts\\stock_data.py" financial_data_handler "000001.SZ"

# 获取股东数据
bash python "E:\\AI\\SKILLS\\company-research\\scripts\\stock_data.py" holder_data_handler "000001.SZ"

# 搜索新闻
bash python "E:\\AI\\SKILLS\\company-research\\scripts\\stock_data.py" news_handler "平安银行"

# Ollama智能搜索
bash python "E:\\AI\\SKILLS\\company-research\\scripts\\ollama_searcher.py" "贵州茅台 基本信息"
```

### 完整调研流程示例

```
1. 首先使用 code_name_transformer 获取正确的股票代码
2. 使用 query_stock_info 获取行业和概念信息
3. 使用 financial_data_handler 获取财务数据
4. 使用 holder_data_handler 获取股东数据
5. 使用 news_handler 获取相关新闻
6. 使用 ollama_searcher 进行深度分析
7. 基于以上数据生成报告
```

## 注意事项

1. **Tushare API 限制**: Tushare 有访问频率限制，建议合理控制调用频率
2. **数据时效性**: 财务数据更新存在延迟，通常在财报发布后1-2周内更新
3. **Ollama 首次运行**: Ollama 首次使用时可能需要下载模型，请耐心等待
4. **代理设置**: 脚本已清除代理设置，如需使用代理请修改代码

## 故障排除

### 常见问题

1. **"tushare模块未找到"**: 运行 `pip install tushare`
2. **"adata模块未找到"**: 运行 `pip install adata`
3. **"akshare模块未找到"**: 运行 `pip install akshare`
4. **"Ollama连接失败"**: 确保Ollama服务正在运行，运行 `ollama serve`
5. **"Tushare API错误"**: 检查Token是否正确，访问频率是否超限

### 调试建议

- 使用 `-v` 参数增加输出信息（如需要可修改脚本添加日志）
- 检查网络连接
- 确认Python环境和依赖包版本

## 许可证

本工具仅供学习和研究使用，请遵守相关数据源的使用条款。