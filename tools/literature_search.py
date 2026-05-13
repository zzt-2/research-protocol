# CLI 入口：argparse + 主流程编排

import argparse
import concurrent.futures
import json
import os
import sys
from pathlib import Path

from litsearch.search_pipeline import (
    _apply_preset,
    _auto_save,
    _compute_relevance,
    _detect_mode,
    _filter_by_domain,
    _filter_by_relevance,
    _resolve_sources,
    _resolve_sources_with_doctypes,
    _split_scenario_method,
    assign_ids,
    assign_publication_status,
    deduplicate,
    enrich_abstracts,
    filter_results,
    sort_results,
)
from litsearch.search_output import (
    print_summary,
    to_brief,
    to_json,
    to_markdown,
    to_markdown_table,
)
from litsearch.search_sources import (
    _resolve_s2_paper_id,
    _search_source,
    _apply_query_modifier,
    exa_find_similar,
    get_s2_citations,
    get_s2_references,
    openalex_citations,
    openalex_trend,
)
from litsearch.search_config import EXA_CATEGORY_MAP, VALID_DOC_TYPES


def main():
    parser = argparse.ArgumentParser(
        description="文献搜索工具 v2 - 多源聚合搜索 + 智能模式检测 + 文档类型路由",
    )
    parser.add_argument("query", nargs="?", default=None, help="搜索关键词（支持中英文、多词组合）")

    parser.add_argument(
        "--mode", default=None,
        choices=["academic", "chinese", "standard", "broad"],
        help="搜索模式: academic(默认)/chinese/standard/broad（不指定则自动检测）",
    )
    parser.add_argument(
        "--sources", nargs="+", default=None,
        choices=["s2", "openalex", "arxiv", "serpapi", "serpapi_web", "tavily", "firecrawl", "exa"],
        help="手动指定搜索源（覆盖 --mode）",
    )
    parser.add_argument(
        "--doc-types", nargs="+", default=None,
        choices=VALID_DOC_TYPES,
        help="文档类型过滤，自动路由到最优源",
    )

    parser.add_argument(
        "--preset", default=None,
        choices=["scenario-method", "problem-driven", "comparison", "implementation"],
        help="搜索预设策略",
    )

    parser.add_argument("--merge", type=Path, default=None, help="合并历史搜索结果文件")
    parser.add_argument("--refs", type=int, default=0, help="展开前 N 条结果的引用链 (默认: 0)")

    parser.add_argument("--max-per-source", type=int, default=20, help="每个源的最大结果数 (默认: 20)")
    parser.add_argument("--top", type=int, default=30, help="最终输出前 N 条 (默认: 30)")
    parser.add_argument("--year-from", type=int, default=None, help="起始年份")
    parser.add_argument("--year-to", type=int, default=None, help="截止年份")
    parser.add_argument("--min-citations", type=int, default=0, help="最低引用数 (默认: 0)")
    parser.add_argument(
        "--sort", default="composite",
        choices=["citations", "year", "relevance", "composite"],
        help="排序方式 (默认: composite 综合排序)",
    )

    parser.add_argument("--start-id", type=int, default=1, help="起始编号 (默认: 1)")
    parser.add_argument("--output", "-o", type=Path, default=None, help="输出文件路径")
    parser.add_argument(
        "--format", dest="out_format", default="json",
        choices=["json", "markdown", "brief"],
        help="输出格式: json/markdown/brief (默认: json)",
    )

    parser.add_argument("--s2-api-key", default=None, help="Semantic Scholar API key")
    parser.add_argument("--openalex-email", default=None, help="OpenAlex 邮箱")
    parser.add_argument("--serpapi-key", default=None, help="SerpAPI key")
    parser.add_argument("--tavily-key", default=None, help="Tavily key")
    parser.add_argument("--firecrawl-key", default=None, help="Firecrawl API key")
    parser.add_argument("--exa-key", default=None, help="Exa API key")
    parser.add_argument(
        "--exa-mode", default="auto",
        choices=["keyword", "neural", "auto"],
        help="Exa 搜索模式 (默认: auto=keyword+neural 并跑)",
    )

    parser.add_argument("--find-similar", type=str, metavar="URL",
                        help="查找与指定 URL 相似的文献 (Exa)")
    parser.add_argument("--citations", type=str, metavar="DOI",
                        help="查看指定 DOI 的引用图谱 (OpenAlex)")
    parser.add_argument("--trend", action="store_true",
                        help="查看查询关键词的发文趋势 (OpenAlex)")
    parser.add_argument("--citations-direction", default="forward",
                        choices=["forward", "backward"],
                        help="引用方向: forward(谁引用了)/backward(引用了谁)")
    parser.add_argument("--citations-depth", type=int, default=1,
                        help="引用扩展深度 (默认: 1)")
    parser.add_argument("--trend-years", type=int, default=5,
                        help="趋势分析年数 (默认: 5)")

    parser.add_argument("--include-web", action="store_true", help=argparse.SUPPRESS)

    args = parser.parse_args()

    if args.output:
        args.output = args.output.resolve()

    # ---- 独立命令路径 ----
    if args.find_similar:
        results = exa_find_similar(args.find_similar, api_key=args.exa_key)
        results = assign_ids(results, args.start_id)
        results = assign_publication_status(results)
        print_summary(results)
        _output_results(results, args, ["exa_similar"])
        _auto_save(results, args.find_similar, ["exa_similar"])
        return

    if args.citations:
        results = openalex_citations(
            args.citations,
            direction=args.citations_direction,
            depth=args.citations_depth,
            email=args.openalex_email,
        )
        results = assign_ids(results, args.start_id)
        results = assign_publication_status(results)
        print_summary(results)
        _output_results(results, args, ["openalex_citations"])
        _auto_save(results, args.citations, ["openalex_citations"])
        return

    if args.trend:
        if not args.query:
            parser.error("--trend 需要 query 参数")
        results = openalex_trend(args.query, years=args.trend_years, email=args.openalex_email)
        print(f"\n{'='*50}")
        print(f"  趋势: {args.query} (近 {args.trend_years} 年)")
        print(f"{'='*50}")
        for r in results:
            bar = "#" * (r["count"] // 10)
            print(f"  {r['year']}: {r['count']:>5}  {bar}")
        return

    if not args.query:
        parser.error("需要 query 参数（或使用 --find-similar/--citations）")

    # ---- 模式与源选择 ----
    if args.mode is None and args.sources is None:
        args.mode = _detect_mode(args.query)
        print(f"[模式] 自动检测: {args.mode}")
    elif args.mode is None:
        args.mode = "custom"

    active_sources = _resolve_sources_with_doctypes(args.mode, args.doc_types, args.sources)
    if args.include_web and "tavily" not in active_sources:
        active_sources.append("tavily")
    print(f"[源] {', '.join(active_sources)}")

    # ---- Exa category from doc_types ----
    # 只在单一 doc_type 且有 category 映射时设置
    if args.doc_types and len(args.doc_types) == 1:
        dt = args.doc_types[0]
        if dt in EXA_CATEGORY_MAP:
            args._exa_category = EXA_CATEGORY_MAP[dt]

    # ---- 预设策略 ----
    queries = [args.query]
    if args.preset:
        modified_query, strategy = _apply_preset(args.query, args.preset)
        if args.preset == "scenario-method":
            queries = _split_scenario_method(args.query)
            print(f"[预设] scenario-method: 拆分为 {len(queries)} 个子查询")
            for i, sq in enumerate(queries):
                print(f"  子查询 {i+1}: {sq}")
        else:
            queries = [modified_query]
            append_terms = strategy.get("append_terms", [])
            if append_terms:
                print(f"[预设] {args.preset}: 追加关键词 {append_terms}")
            if strategy.get("mode") and args.sources is None:
                active_sources = _resolve_sources(strategy["mode"], None)
                print(f"[预设] 源切换为: {', '.join(active_sources)}")

    # ---- 搜索（并行）----
    all_results: list[dict] = []

    search_tasks: list[tuple[str, str]] = []
    for q in queries:
        modified_q = q
        if args.doc_types:
            for dt in args.doc_types:
                modified_q = _apply_query_modifier(modified_q, dt)
                if modified_q != q:
                    break
        for source in active_sources:
            search_tasks.append((source, modified_q))

    if search_tasks:
        print(f"[搜索] {len(search_tasks)} 个任务并行执行...", file=sys.stderr)
        with concurrent.futures.ThreadPoolExecutor(
            max_workers=min(len(search_tasks), 10)
        ) as executor:
            future_to_task = {
                executor.submit(_search_source, src, q, args): (src, q)
                for src, q in search_tasks
            }
            for future in concurrent.futures.as_completed(future_to_task):
                src, q = future_to_task[future]
                try:
                    results = future.result()
                    all_results.extend(results)
                except Exception as e:
                    print(f"  [ERROR] {src} 搜索失败: {e}", file=sys.stderr)

    # ---- 合并历史结果 ----
    if args.merge:
        merge_path = args.merge.resolve()
        if merge_path.exists():
            prev_data = json.loads(merge_path.read_text(encoding="utf-8"))
            prev_results = prev_data.get("results", [])
            print(f"[合并] 加载 {len(prev_results)} 条历史结果")
            all_results.extend(prev_results)
        else:
            print(f"[警告] 合并文件不存在: {merge_path}", file=sys.stderr)

    # ---- 后处理 ----
    print(f"\n[汇总] 原始结果: {len(all_results)} 条")
    all_results = deduplicate(all_results)
    print(f"[汇总] 去重后: {len(all_results)} 条")

    s2_key = args.s2_api_key or os.environ.get("S2_API_KEY")
    all_results = enrich_abstracts(all_results, api_key=s2_key)

    all_results = _compute_relevance(all_results, args.query)
    all_results = _filter_by_relevance(all_results)
    all_results = _filter_by_domain(all_results)

    all_results = filter_results(
        all_results,
        min_citations=args.min_citations,
        year_from=args.year_from,
        year_to=args.year_to,
    )
    all_results = sort_results(all_results, args.sort, args.query)

    # ---- 引用链展开 ----
    if args.refs and all_results:
        s2_key = args.s2_api_key or os.environ.get("S2_API_KEY")
        expanded = []
        for r in all_results[:args.refs]:
            paper_id = _resolve_s2_paper_id(r)
            if not paper_id:
                continue
            title_short = r.get("title", "")[:40]
            print(f"[引用] 展开: {title_short}...")
            expanded.extend(get_s2_references(paper_id, api_key=s2_key))
            expanded.extend(get_s2_citations(paper_id, api_key=s2_key))
        if expanded:
            print(f"[引用] 展开得到 {len(expanded)} 条额外结果")
            all_results.extend(expanded)
            all_results = deduplicate(all_results)
            all_results = enrich_abstracts(all_results, api_key=s2_key)
            all_results = _compute_relevance(all_results, args.query)
            all_results = _filter_by_relevance(all_results)
            all_results = _filter_by_domain(all_results)
            all_results = filter_results(
                all_results,
                min_citations=args.min_citations,
                year_from=args.year_from,
                year_to=args.year_to,
            )
            all_results = sort_results(all_results, args.sort, args.query)

    if len(all_results) > args.top:
        all_results = all_results[:args.top]
        print(f"[截断] 保留前 {args.top} 条")

    all_results = assign_ids(all_results, args.start_id)
    all_results = assign_publication_status(all_results)

    # 终端摘要
    print_summary(all_results)

    _output_results(all_results, args, active_sources)
    _auto_save(all_results, args.query, active_sources)


def _output_results(results: list[dict], args, sources: list[str]) -> None:
    if args.out_format == "json":
        output_data = to_json(results, args.query or "", sources)
        content = json.dumps(output_data, ensure_ascii=False, indent=2)
    elif args.out_format == "markdown":
        content = to_markdown_table(results, args.query or "", sources)
    elif args.out_format == "brief":
        content = to_brief(results)
    else:
        content = to_markdown(results)

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(content, encoding="utf-8")
        print(f"[OK] 结果已保存到: {args.output}")
    else:
        print(content)


if __name__ == "__main__":
    main()
