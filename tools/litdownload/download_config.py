import os
from dataclasses import dataclass
from typing import Optional

import requests

# litsearch.search_config 在 import 时自动调用 _load_env()，触发 .env 加载
import litsearch.search_config  # noqa: F401

USER_AGENT = "ResearchProtocol/2.0 (paper-download)"
CONNECT_TIMEOUT = 5
READ_TIMEOUT = 15
REQUEST_TIMEOUT = (CONNECT_TIMEOUT, READ_TIMEOUT)

ARXIV_HTML_BASE = "https://arxiv.org/html"
ARXIV_EPRINT_BASE = "https://arxiv.org/e-print"
ARXIV_PDF_BASE = "https://arxiv.org/pdf"
UNPAYWALL_API_BASE = "https://api.unpaywall.org/v2"

BLOCKED_DOMAINS = {"ieeexplore.ieee.org"}


@dataclass
class DownloadResult:
    success: bool
    method: str = ""
    content_file: str = ""
    content_type: str = ""
    content_quality: str = "good"
