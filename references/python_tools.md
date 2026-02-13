# Python工具脚本使用说明

## 概述

本技能使用独立的Python脚本工具替代原有的MCP服务器方式，提供更灵活、即插即用的使用体验。所有工具均可通过Bash命令直接调用。

## 工具脚本结构

```
scripts/
├── ollama_searcher.py      # 智能搜索工具
├── stock_inform.py         # 股票基本信息查询
├── stock_data.py           # 财务数据获取
└── README.md               # 详细安装说明
```

## 工具详细说明

### 1. ollama_searcher.py

**功能**: 调用Ollama进行智能搜索和摘要生成。可能需要等待至少20秒才能完成。

**参数**:
- `keyword` (str): 搜索关键词

**使用场景**:
- 公司新闻搜索
- 行业动态跟踪
- 管理层信息收集
- 竞争分析

**命令格式**:
```bash
python scripts/ollama_searcher.py "关键词"
```

**返回值**:
- JSON格式，包含搜索结果摘要或错误信息

**示例**:
```bash
# 搜索公司基本信息
python scripts/ollama_searcher.py "贵州茅台 基本信息"

# 搜索行业趋势
python scripts/ollama_searcher.py "人工智能 行业趋势 2025"
```

**依赖**:
- ollama Python库（可选）
- Ollama服务需要运行

---

### 2. stock_inform.py

**功能**: 股票基本信息查询

#### 2.1 code_name_transformer

**功能**: 股票代码和名称互转

**参数**:
- `content` (str): 股票代码或名称

**支持格式**:
- 代码转名称: `"000001"` → `"000001.SZ"`
- 名称转代码: `"平安银行"` → `"000001.SZ"`

**命令格式**:
```bash
python scripts/stock_inform.py code_name_transformer "代码或名称"
```

**返回值**:
- CSV格式字符串，包含代码和名称对应关系

**示例**:
```bash
# 名称转代码
python scripts/stock_inform.py code_name_transformer "平安银行"

# 代码转名称
python scripts/stock_inform.py code_name_transformer "000001"
```

#### 2.2 query_stock_info

**功能**: 查询股票的所属概念、行业板块和风险提示

**参数**:
- `codes` (str): 股票代码，如 `"000001.SZ"`

**返回值**:
- 文本格式，包含：
  - 股票代码
  - 所属概念（name, reason）
  - 行业板块（plate_name）
  - 风险提示（t_type, reason）

**命令格式**:
```bash
python scripts/stock_inform.py query_stock_info "股票代码"
```

**示例**:
```bash
# 查询股票信息
python scripts/stock_inform.py query_stock_info "000001.SZ"
```

**依赖**:
- tushare
- adata

---

### 3. stock_data.py

**功能**: 财务数据和股东数据获取

#### 3.1 financial_data_handler

**功能**: 获取财务数据

**参数**:
- `codes` (str): 股票代码，如 `"000001.SZ"`

**返回数据**:
- 近12期核心财务指标（营收、利润、毛利率等）
- 近一年估值统计（PE、PB、PS等分位数）

**命令格式**:
```bash
python scripts/stock_data.py financial_data_handler "股票代码"
```

**示例**:
```bash
# 获取财务数据
python scripts/stock_data.py financial_data_handler "000001.SZ"
```

#### 3.2 holder_data_handler

**功能**: 获取股东数据

**参数**:
- `codes` (str): 股票代码

**返回数据**:
- 股东数变化趋势
- 十大流通股东
- 十大股东信息
- 机构持股变化

**命令格式**:
```bash
python scripts/stock_data.py holder_data_handler "股票代码"
```

**示例**:
```bash
# 获取股东数据
python scripts/stock_data.py holder_data_handler "000001.SZ"
```

#### 3.3 news_handler

**功能**: 搜索金融资讯

**参数**:
- `keyword` (str...): 搜索关键词列表，支持多个关键词

**特点**:
- 支持多个关键词串联搜索
- 返回新闻简报
- 包含相关性和时效性排序

**命令格式**:
```bash
python scripts/stock_data.py news_handler "关键词1" "关键词2" ...
```

**示例**:
```bash
# 单关键词搜索
python scripts/stock_data.py news_handler "平安银行"

# 多关键词搜索
python scripts/stock_data.py news_handler "平安银行" "业绩预告"
```

**依赖**:
- tushare
- adata
- akshare

---

## 在Claude Code中的调用方式

### 使用Bash工具

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

---

## 组合调用流程

以下是一个完整的公司调研流程示例：

```python
# 1. 代码转换
bash python "E:\\AI\\SKILLS\\company-research\\scripts\\stock_inform.py" code_name_transformer "平安银行"

# 2. 基本信息查询
bash python "E:\\AI\\SKILLS\\company-research\\scripts\\stock_inform.py" query_stock_info "000001.SZ"

# 3. 财务数据分析
bash python "E:\\AI\\SKILLS\\company-research\\scripts\\stock_data.py" financial_data_handler "000001.SZ"

# 4. 股东数据分析
bash python "E:\\AI\\SKILLS\\company-research\\scripts\\stock_data.py" holder_data_handler "000001.SZ"

# 5. 新闻搜索
bash python "E:\\AI\\SKILLS\\company-research\\scripts\\stock_data.py" news_handler "平安银行"

# 6. 深度分析
bash python "E:\\AI\\SKILLS\\company-research\\scripts\\ollama_searcher.py" "平安银行 最新动态"
```

---

## 错误处理

### 常见错误

1. **模块未找到**:
   - 错误: `ModuleNotFoundError: No module named 'tushare'`
   - 解决: 运行 `pip install tushare`

2. **Ollama连接失败**:
   - 错误: Ollama库不可用或服务未运行
   - 解决: 安装Ollama并运行 `ollama serve`

3. **API错误**:
   - 错误: Tushare API返回错误
   - 解决: 检查Token是否正确，访问频率是否超限

4. **数据返回为空**:
   - 错误: 查询结果为空
   - 解决: 验证股票代码格式是否正确

### 调试建议

```bash
# 检查Python环境
python --version

# 检查已安装包
pip list | grep -E "tushare|adata|akshare"

# 测试脚本语法
python -m py_compile scripts/stock_inform.py
```

---

## 性能优化

1. **批量处理**: 虽然脚本支持单个代码查询，但可以快速连续调用多个
2. **缓存结果**: 重复查询时可以考虑保存结果避免重复调用
3. **异步调用**: 在Claude Code中，可以同时发起多个Bash调用提高效率
4. **增量更新**: 只查询最新数据，避免重复获取历史数据

---


## 配置文件

### requirements.txt

所有依赖包都在 `requirements.txt` 中定义，可以使用以下命令安装：

```bash
pip install -r requirements.txt
```

### Tushare Token配置

在以下文件中配置Tushare Token：
- `scripts/stock_inform.py`
- `scripts/stock_data.py`

找到以下行并替换Token：
```python
TUSHARE_TOKEN = "你的Tushare_Token"
```

---

## 更新日志

### v2.0 (Python脚本版)
- 移除MCP服务器依赖
- 改为独立Python脚本
- 支持通过Bash直接调用
- 简化安装和配置流程
- 提升可移植性和兼容性