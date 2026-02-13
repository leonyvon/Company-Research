# 公司深度调研技能 (Company Research Skill)

一个基于Claude Code的上市公司深度调研工具，整合Python脚本进行全方位公司分析，生成结构化的ONE PAGER研究报告。

## 功能特性

- 📊 **财务数据分析**: 获取近12期财务指标、估值统计
- 👥 **股东结构分析**: 查看股东数量变化、十大股东明细
- 📰 **新闻动态跟踪**: 搜索公司相关新闻和公告
- 🧠 **智能搜索分析**: 集成Ollama进行深度分析和摘要生成
- 📈 **行业研究分析**: 行业定位、竞争分析、趋势判断
- 📝 **结构化报告**: 生成标准的ONE PAGER研究报告（Markdown格式）

## 项目结构

```
company-research/
├── SKILL.md                          # Claude Code技能定义文件
├── requirements.txt                  # Python依赖包
├── scripts/                          # Python工具脚本
│   ├── ollama_searcher.py           # 智能搜索工具
│   ├── stock_inform.py              # 股票基本信息查询
│   ├── stock_data.py                # 财务数据获取
│   └── README.md                    # 脚本使用说明
├── references/                      # 参考文档
│   ├── python_tools.md              # 工具使用指南
│   ├── financial_analysis.md        # 财务分析框架
│   └── industry_research.md         # 行业研究方法
└── assets/
    └── one_pager_template.md        # 报告模板
```

## 安装

### 前置要求

- Python 3.8+
- Claude Code

### 安装步骤

1. 克隆本仓库
```bash
git clone https://github.com/你的用户名/company-research.git
cd company-research
```

2. 安装依赖包
```bash
pip install -r requirements.txt
```

3. 配置 Tushare API Token

在 `scripts/stock_inform.py` 和 `scripts/stock_data.py` 中，将 `TUSHARE_TOKEN` 替换为您自己的 Token。

获取 Token: https://tushare.pro/register

4. 配置 Ollama (可选，用于智能搜索功能)

访问 [Ollama官网](https://ollama.ai) 下载安装，然后启动服务：
```bash
ollama serve
```

详细安装说明请参考 [scripts/README.md](scripts/README.md)

## 使用方法

### 在Claude Code中使用

将本技能目录放置到Claude Code的skills目录，然后使用Bash工具调用脚本：

```python
# 股票代码/名称转换
bash python "scripts/stock_inform.py" code_name_transformer "平安银行"

# 查询股票信息
bash python "scripts/stock_inform.py" query_stock_info "000001.SZ"

# 获取财务数据
bash python "scripts/stock_data.py" financial_data_handler "000001.SZ"

# 获取股东数据
bash python "scripts/stock_data.py" holder_data_handler "000001.SZ"

# 搜索新闻
bash python "scripts/stock_data.py" news_handler "平安银行"

# Ollama智能搜索
bash python "scripts/ollama_searcher.py "贵州茅台 基本信息"
```

### 调研流程

1. **基本信息收集**: 获取股票代码、行业分类、概念板块
2. **财务数据分析**: 分析近12期财务指标和估值水平
3. **股东结构分析**: 查看股东变化和机构持股
4. **新闻动态跟踪**: 搜索相关新闻和公告
5. **综合分析报告**: 使用模板生成结构化报告

详细使用说明请参考 [SKILL.md](SKILL.md) 和 [references/python_tools.md](references/python_tools.md)

## 文档

- [SKILL.md](SKILL.md) - 技能定义和使用流程
- [scripts/README.md](scripts/README.md) - 脚本详细安装说明
- [references/python_tools.md](references/python_tools.md) - 工具使用指南
- [references/financial_analysis.md](references/financial_analysis.md) - 财务分析框架
- [references/industry_research.md](references/industry_research.md) - 行业研究方法

## 数据源

本工具使用以下数据源：
- **Tushare**: 中国股市数据（需要免费注册获取Token）
- **Adata**: 财务数据增强
- **Akshare**: 新闻资讯
- **Ollama**: 智能搜索（可选）

## 免责声明

本工具仅供学习和研究使用，所有分析基于公开信息生成。投资者应独立判断，谨慎决策，投资有风险，入市需谨慎。

## 许可证

[MIT License](LICENSE)

## 贡献

欢迎提交Issue和Pull Request！

## 致谢

- [Claude Code](https://claude.com/claude-code)
- [Tushare](https://tushare.pro)
- [Akshare](https://akshare.akfamily.xyz/)
- [Adata](https://adata.30006124.xyz/)
- [Ollama](https://ollama.ai)

## 联系方式

如有问题或建议，请提交Issue。

---

**注意**: 本技能需要Claude Code环境才能正常使用。如需了解Claude Code，请访问 https://claude.com/claude-code