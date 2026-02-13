---
name: company-research
description: 上市公司深度调研技能。整合Python工具脚本进行全方位公司分析，从基本信息搜索到财务数据获取，最终生成结构化的ONE PAGER研究报告（支持Markdown格式）。使用场景：当用户需要分析上市公司、进行投资研究、生成公司调研报告时触发此技能。
---

# 上市公司深度调研技能

## 概述

本技能整合了独立的Python工具脚本，提供完整的上市公司深度调研流程。通过调用Ollama搜索、股票信息查询和财务数据获取工具，生成结构化的ONE PAGER研究报告。报告支持Markdown格式输出，便于不同场景下的使用和分享。

本技能设计为**即插即用**，无需配置MCP服务器，只需通过Bash工具直接调用Python脚本即可。

## 安装步骤

### 1. 安装依赖包

```bash
pip install -r requirements.txt
```

### 2. 配置 Tushare API Token

在 `scripts/stock_inform.py` 和 `scripts/stock_data.py` 中，将 `TUSHARE_TOKEN` 替换为您自己的 Tushare Token。

获取 Token: https://tushare.pro/register

### 3. 配置 Ollama (可选)

如需使用智能搜索功能：
```bash
# 访问 https://ollama.ai 下载安装
# 启动服务
ollama serve
```

详细安装说明请参考 `scripts/README.md`

## 工具脚本调用方式

本技能包含以下Python脚本工具，位于 `scripts/` 目录。详细使用说明请参考 `references/python_tools.md`。

**快速参考**:
- `ollama_searcher.py` - 智能搜索和摘要生成
- `stock_inform.py` - 股票基本信息查询（代码名称转换、概念行业查询）
- `stock_data.py` - 财务数据获取（财务数据、股东数据、新闻搜索）

**调用格式**:
```python
bash python "E:\\AI\\SKILLS\\company-research\\scripts\\<脚本名>.py" <功能> <参数>
```

具体调用示例详见下文"完整调研示例"部分。

## 调研流程

### 阶段1：基本信息收集
1. **公司识别**: 使用 `code_name_transformer` 获取准确的股票代码和名称
2. **行业定位**: 使用 `query_stock_info` 获取行业分类和概念板块
3. **风险初筛**: 查看是否有明确的风险提示
4. **深度信息获取**: 使用 `ollama_searcher` 获取公司基本信息（关键词："[公司名称] 基本信息"）

**参考文档**: `references/industry_research.md` - 行业定位和分析方法

### 阶段2：财务数据分析
1. **财务趋势分析**: 从 `financial_data_handler` 获取近12期财务数据
2. **盈利能力评估**: 关注毛利率、净利率、ROE等关键指标变化
3. **财务健康度**: 分析资产负债率、现金流等健康指标
4. **估值水平**: 基于估值统计数据分析当前估值位置

**参考文档**: `references/financial_analysis.md` - 财务分析框架和方法论

### 阶段3：股东结构分析
1. **股东变化趋势**: 分析股东数量的增减变化
2. **机构持股分析**: 查看十大股东构成
3. **股权集中度**: 评估股权集中程度

### 阶段4：新闻与动态跟踪
1. **近期新闻**: 使用 `news_handler` 搜索公司相关新闻
2. **重要事件**: 关注业绩预告、重大事项等
3. **行业关联**: 搜索行业相关动态
4. **智能分析补充**: 使用 `ollama_searcher` 获取深度分析（关键词："[公司名称] 近期动态"）

**参考文档**: `references/industry_research.md` - 行业政策分析和趋势判断

### 阶段5：综合分析与报告生成
基于实际获取的数据生成结构化报告：
1. **数据整合**: 将各工具获取的数据进行整合
2. **趋势识别**: 识别财务、股东、估值等方面的趋势
3. **风险收益评估**: 基于实际数据评估投资价值
4. **报告撰写**: 使用 `assets/one_pager_template.md` 模板生成报告

**参考文档**:
- `references/financial_analysis.md` - 财务风险评估和预警信号
- `references/industry_research.md` - 行业风险识别和竞争分析

## 完整调研示例

以下是调研"平安银行"的完整流程示例：

```python
# 步骤1：股票代码/名称转换
bash python "E:\\AI\\SKILLS\\company-research\\scripts\\stock_inform.py" code_name_transformer "平安银行"
# 返回: 000001.SZ

# 步骤2：查询股票基本信息
bash python "E:\\AI\\SKILLS\\company-research\\scripts\\stock_inform.py" query_stock_info "000001.SZ"
# 返回: 概念板块、行业分类、风险提示

# 步骤3：获取财务数据
bash python "E:\\AI\\SKILLS\\company-research\\scripts\\stock_data.py" financial_data_handler "000001.SZ"
# 返回: 近12期财务指标、估值统计

# 步骤4：获取股东数据
bash python "E:\\AI\\SKILLS\\company-research\\scripts\\stock_data.py" holder_data_handler "000001.SZ"
# 返回: 股东数量变化、十大股东

# 步骤5：搜索新闻
bash python "E:\\AI\\SKILLS\\company-research\\scripts\\stock_data.py" news_handler "平安银行"
# 返回: 近期新闻简报

# 步骤6：深度分析 (可选)
bash python "E:\\AI\\SKILLS\\company-research\\scripts\\ollama_searcher.py" "平安银行 近期动态"
# 返回: 深度分析摘要

# 步骤7：基于以上数据，使用 one_pager_template.md 生成报告
```

## 报告生成原则

### 基于实际数据，避免幻觉
所有分析必须基于工具脚本实际获取的数据，不猜测无法验证的信息。

### 实际可获取的数据类型
1. **确定可获取的数据**:
   - 股票代码/名称、行业分类、概念板块
   - 近12期财务指标、近一年估值统计
   - 股东数量变化、十大股东明细
   - 公司相关新闻和公告
   - 风险提示信息（如有）

2. **无法直接获取但可推断的数据**:
   - 财务趋势分析（基于历史数据）
   - 估值位置判断（基于历史分位数）
   - 股东结构变化趋势
   - 新闻事件的影响分析

3. **需要避免猜测的内容**:
   - 公司成立时间、核心团队等基本信息
   - 具体的业务模式细节
   - 未在新闻中出现的重大事件
   - 无法验证的竞争优势

## 注意事项

1. **数据验证**: 交叉验证不同来源的数据
2. **时效性**: 关注最新财务数据和新闻
3. **全面性**: 覆盖业务、财务、风险等多个维度
4. **客观性**: 保持分析的中立和客观
5. **API限制**: Tushare有访问频率限制，建议合理控制调用频率
6. **数据更新**: 财务数据更新存在延迟，通常在财报发布后1-2周内更新

## 报告输出格式

本技能支持生成Markdown格式的研究报告：

### Markdown格式
- **默认输出**: 使用 `assets/one_pager_template.md` 模板生成结构化Markdown报告
- **优势**: 便于编辑、版本控制和在线查看
- **文件扩展名**: `.md`

## 参考文档

本技能的详细分析方法和工具说明请参考以下文档：

| 文档 | 说明 |
|-----|------|
| `references/python_tools.md` | Python脚本工具详细使用指南和调用示例 |
| `references/financial_analysis.md` | 财务数据分析方法论、指标分析和风险评估 |
| `references/industry_research.md` | 行业分析框架、竞争分析和趋势判断 |
| `scripts/README.md` | 脚本详细安装和配置说明 |
| `requirements.txt` | Python依赖包清单 |
| `assets/one_pager_template.md` | ONE PAGER报告模板 |