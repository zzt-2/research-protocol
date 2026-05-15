# 常量、环境变量加载、API key 解析

import os
from pathlib import Path
from typing import Optional


def _load_env() -> dict[str, str]:
    """从项目 .env 文件加载环境变量，不覆盖已有值"""
    env_path = Path(__file__).resolve().parent.parent.parent / ".env"
    env_vars: dict[str, str] = {}
    if not env_path.exists():
        return env_vars
    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" in line:
            key, _, value = line.partition("=")
            key, value = key.strip(), value.strip()
            if key and key not in os.environ:
                os.environ[key] = value
            env_vars[key] = os.environ.get(key, value)
    return env_vars


_load_env()


def _resolve_keys(cli_value: Optional[str], env_name: str) -> list[str]:
    """解析 API key：CLI 参数 > 环境变量。支持逗号分隔的多个 key。"""
    raw = cli_value or os.environ.get(env_name, "")
    return [k.strip() for k in raw.split(",") if k.strip()]


S2_SEARCH_URL = "https://api.semanticscholar.org/graph/v1/paper/search"
S2_FIELDS = "title,authors,abstract,externalIds,year,venue,citationCount,isOpenAccess,openAccessPdf"

OPENALEX_WORKS_URL = "https://api.openalex.org/works"

ARXIV_SEARCH_URL = "http://export.arxiv.org/api/query"
ARXIV_NS = {"atom": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/atom"}

FIRECRAWL_API_BASE = "https://api.firecrawl.dev/v1"
EXA_API_BASE = "https://api.exa.ai"

USER_AGENT = "ResearchProtocol/2.0 (literature-search)"
REQUEST_TIMEOUT = 30

MODE_SOURCES = {
    "academic": ["s2", "openalex", "arxiv", "serpapi", "exa"],
    "chinese":  ["serpapi", "exa", "firecrawl"],
    "standard": ["firecrawl", "exa", "serpapi", "tavily"],
    "broad":    ["s2", "openalex", "arxiv", "serpapi", "tavily", "firecrawl", "exa"],
}

SOURCE_WEIGHTS = {
    "semantic_scholar": 1.0,
    "serpapi_scholar":  0.9,
    "exa":              0.85,
    "arxiv":            0.8,
    "openalex":         0.6,
    "firecrawl":        0.6,
    "tavily":           0.5,
    "serpapi_web":      0.9,
}

DOC_TYPE_SOURCE_MAP = {
    "journal":          ["exa", "firecrawl"],
    "conference":       ["exa", "firecrawl"],
    "preprint":         ["exa", "firecrawl"],
    "standard":         ["firecrawl", "exa"],
    "patent":           ["firecrawl", "exa"],
    "policy":           ["firecrawl", "exa"],
    "financial":        ["exa", "firecrawl"],
    "industry_report":  ["firecrawl", "exa"],
    "whitepaper":       ["firecrawl", "exa"],
    "code":             ["exa"],
    "dataset":          ["exa"],
    "news":             ["exa"],
    "blog":             ["firecrawl", "exa"],
    "book":             ["exa", "firecrawl"],
    "chinese_journal":  ["exa"],
    "cnki":             ["serpapi_web"],
    "thesis":           ["openalex"],
}

VALID_DOC_TYPES = list(DOC_TYPE_SOURCE_MAP.keys())

DOC_TYPE_QUERY_MODIFIERS = {
    "preprint":         "site:arxiv.org",
    "standard":         "3GPP ETSI specification",
    "industry_report":  "Gartner McKinsey report",
    "whitepaper":       "technical report",
    "cnki":             "site:cnki.net",
}

EXA_CATEGORY_MAP = {
    "code":     "github",
    "news":     "news",
    "journal":  "research paper",
    "preprint": "research paper",
}

DOC_TYPE_LABELS = {
    "journal": "期刊", "conference": "会议", "preprint": "预印本",
    "standard": "标准", "patent": "专利", "policy": "政策",
    "financial": "金融", "industry_report": "行业报告", "whitepaper": "白皮书",
    "code": "代码", "dataset": "数据集", "news": "新闻",
    "blog": "博客", "book": "书籍", "chinese_journal": "中文期刊",
    "thesis": "学位论文", "cnki": "CNKI知网",
}

PRESET_STRATEGIES = {
    "scenario-method": {"mode": "academic", "split_query": True},
    "problem-driven": {"mode": "broad"},
    "comparison": {"mode": "academic", "append_terms": ["survey", "review", "comparison", "benchmark"]},
    "implementation": {"mode": "standard", "append_terms": ["github", "code", "implementation"]},
}

STANDARD_KEYWORDS = [
    "ITU-R", "3GPP", "IEEE 802", "standard", "implementation",
    "specification", "RFC", "IETF", "ISO", "ETSI",
]

# 非学术域名黑名单 — 直接过滤，不出现在结果中
DOMAIN_BLACKLIST = {
    # 百度系
    "baike.baidu.com", "wenku.baidu.com", "wk.baidu.com",
    "xueshu.baidu.com", "zhihu.com",
    # 文档分享/论文售卖平台
    "docin.com", "doc88.com", "book118.com", "renrenwenku.com",
    "ishare.iask.sina.com.cn", "zxtw168.com", "csdn.net",
    "xueshu.baidu.com", "xw.importantmc.com", "importantmc.com",
    "reference-report.com", "shangxueba.com", "xuexi111.com",
    "xueshu56.com", "xueshu123.com", "xuewenshe.com",
    # 内容农场/低质聚合
    "360doc.com", "oh100.com", "51test.net", "edu.iqiang.com",
    # 培训机构
    "morningChinese.com", "hahaku.com",
}

# 域名降权列表 — 保留但在综合排序中降权
DOMAIN_GREYLIST = {
    "weibo.com", "mp.weixin.qq.com", "toutiao.com",
    "sohu.com", "sina.com.cn", "163.com", "qq.com",
}
