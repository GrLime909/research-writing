#!/usr/bin/env python3
"""Journal Monitor (WOS Edition) — WOS API-first approach.

Search WOS journals by keyword + time range via the internal runQuerySearch API,
parse structured NDJSON responses, deduplicate against existing Excel, translate,
and save new papers.

The actual API call is executed by Codex in the browser JS context and the
NDJSON response is fed back to this script via --api-result.
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional, List

from excel_manager import PaperRecord, ExcelManager

# -- Constants --------------------------------------------------------

DEFAULT_JOURNALS_FILE = Path(__file__).resolve().parent.parent / "wos-journals.txt"
COLUMNS = [
    "论文名", "作者", "发表时间", "期刊",
    "DOI", "URL", "摘要",
    "论文中文名", "摘要中文翻译", "入库时间"
]


# -- CLI -------------------------------------------------------------

def parse_args():
    p = argparse.ArgumentParser(description="Journal Monitor — WOS API search")
    p.add_argument("--journals", default=None,
                   help="Journal names file (default: wos-journals.txt). "
                        "Use --journals '' to search without journal filter.")
    p.add_argument("--keywords", required=True,
                   help="Keywords. Semicolon=OR, space=AND within group. "
                        "E.g. 'urban resilience;climate adaptation'")
    p.add_argument("--since", default=None,
                   help="Start year (e.g. 2026). Default: no filter.")
    p.add_argument("--until", default=None,
                   help="End year (e.g. 2026). Default: same as --since.")
    p.add_argument("--output", required=True, help="Path to output Excel (.xlsx)")
    p.add_argument("--database", default="WOSCC",
                   choices=["WOSCC"])
    p.add_argument("--editions", default=None,
                   help="WoS editions, comma-separated (SCI,SSCI). Default: all.")
    p.add_argument("--sort", default="date-descending",
                   choices=["relevance", "times-cited-descending",
                            "date-descending", "date-ascending"])
    p.add_argument("--doc-types", default=None,
                   help="Filter by document types, comma-separated (Article,Review). Default: no filter.")
    p.add_argument("--limit", type=int, default=100,
                   help="Max new papers per run (default 100)")
    p.add_argument("--translate", action="store_true",
                   help="Translate titles/abstracts to Chinese")
    p.add_argument("--api-result", default=None,
                   help="[Internal] NDJSON result from WOS API call. "
                        "Used by Codex to feed API responses back.")
    p.add_argument("--journal-index", type=int, default=None,
                   help="[Internal] Current journal being processed.")
    p.add_argument("--phase", default=None,
                   choices=["build-queries", "process-results", "translate", "export"],
                   help="[Internal] Execution phase.")
    return p.parse_args()


# -- Journal Loading --------------------------------------------------

def load_journals(raw: Optional[str]) -> List[str]:
    """Load journal names from file or return empty list."""
    if raw is None or raw.strip() == "":
        path = DEFAULT_JOURNALS_FILE
    else:
        path = Path(raw)
    if not path.exists():
        print(f"[WARN] Journal file not found: {path}")
        return []
    lines = path.read_text(encoding="utf-8").strip().split("\n")
    journals = []
    for line in lines:
        line = line.strip()
        if line and not line.startswith("#"):
            journals.append(line)
    return journals


# -- Keyword Parsing --------------------------------------------------

def parse_keywords(raw: str) -> list[list[str]]:
    """Parse keywords: semicolon=OR, space=AND within group."""
    groups = []
    for group in raw.split(";"):
        terms = [t.strip() for t in group.split() if t.strip()]
        if terms:
            groups.append(terms)
    return groups


# -- Time Parsing -----------------------------------------------------

def parse_time(since: Optional[str], until: Optional[str]) -> Optional[str]:
    """Parse time filter. Returns year string or None."""
    if since is None and until is None:
        return None
    year = since or until
    m = re.search(r"(\d{4})", str(year))
    if m:
        return m.group(1)
    return None


# -- Query Building ---------------------------------------------------

def build_wos_query(journal: str, keyword_groups: list[list[str]],
                    year: Optional[str], editions: Optional[List[str]],
                    database: str, sort: str) -> dict:
    """Build a WOS runQuerySearch API request body."""
    query_rows = []

    # Journal filter
    if journal:
        query_rows.append({"rowField": "SO", "rowText": journal})

    # Keyword filter (TS = topic search)
    ts_clauses = []
    for group in keyword_groups:
        ts_clauses.append(" ".join(group))
    if ts_clauses:
        ts_text = " OR ".join(ts_clauses) if len(ts_clauses) > 1 else ts_clauses[0]
        row = {"rowField": "TS", "rowText": ts_text}
        if query_rows:
            row["rowBoolean"] = "AND"
        query_rows.append(row)

    # Year filter
    if year:
        query_rows.append({"rowBoolean": "AND", "rowField": "PY", "rowText": year})

    body = {
        "product": database,
        "searchMode": "general",
        "viewType": "search",
        "serviceMode": "summary",
        "search": {
            "mode": "general",
            "database": database,
            "query": query_rows,
        },
        "retrieve": {
            "first": 1,
            "count": 50,
            "history": True,
            "jcr": True,
            "sort": sort,
            "analyzes": [],
            "locale": "en"
        },
        "eventMode": None
    }

    if editions:
        body["search"]["editions"] = editions

    return body


def build_all_queries(journals: List[str], keyword_groups: list[list[str]],
                      year: Optional[str], editions: Optional[List[str]],
                      database: str, sort: str) -> list[dict]:
    """Build API queries for all journals (or one if no journal filter)."""
    targets = journals if journals else [""]  # "" = no journal filter
    queries = []
    for j in targets:
        queries.append(build_wos_query(j, keyword_groups, year, editions, database, sort))
    return queries


# -- NDJSON Parsing ---------------------------------------------------

def parse_ndjson_records(ndjson_text: str) -> List[dict]:
    """Parse NDJSON API response into paper records."""
    records = []
    for line in ndjson_text.strip().split("\n"):
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue
        if obj.get("key") == "records":
            payload = obj.get("payload", {})
            for idx, rec in payload.items():
                title = ""
                titles = rec.get("titles", {})
                if "item" in titles:
                    items = titles["item"]
                    # item might be a dict keyed by language
                    if isinstance(items, dict):
                        for lang_data in items.values():
                            if isinstance(lang_data, list) and lang_data:
                                title = lang_data[0].get("title", "")
                                break
                    elif isinstance(items, list) and items:
                        title = items[0].get("title", "")

                # Authors
                authors = ""
                names = rec.get("names", {})
                author_list = names.get("author", {})
                if isinstance(author_list, dict):
                    for lang_data in author_list.values():
                        auth_names = []
                        for a in lang_data:
                        
                            if a and a.get("wos_standard"):
                                auth_names.append(a["wos_standard"])
                        if auth_names:
                            authors = "; ".join(auth_names)
                            break

                # Source
                source = ""
                src_titles = titles.get("source", {})
                if isinstance(src_titles, dict):
                    for lang_data in src_titles.values():
                        if isinstance(lang_data, list) and lang_data:
                            source = lang_data[0].get("title", "")
                            break

                # Year and pub date
                pub_info = rec.get("pub_info", {})
                pubyear = str(pub_info.get("pubyear", ""))
                pubdate = pub_info.get("pubdate", "")
                pub_date = pubdate or pubyear

                # DOI
                doi = rec.get("doi", "")

                # WOS URL
                colluid = rec.get("colluid", "")
                url = f"https://www.webofscience.com/wos/woscc/full-record/{colluid}" if colluid else ""

                # Abstract
                abstract = ""
                abs_data = rec.get("abstract", {})
                if "basic" in abs_data:
                    for lang_data in abs_data["basic"].values():
                        if isinstance(lang_data, dict) and "abstract" in lang_data:
                            abstract = re.sub(r"<[^>]*>", "", lang_data["abstract"])
                            break

                # Citations
                counts = rec.get("citation_related", {}).get("counts", {})
                citations = counts.get("WOSCC", 0)


                # Document type
                doctypes = rec.get("doctypes", [])
                doc_type = doctypes[0] if doctypes else ""


                records.append({
                    "title": title,
                    "authors": authors,
                    "pub_date": pub_date,
                    "journal": source,
                    "doi": doi,
                    "url": url,
                    "abstract": abstract,


                    "citations": citations,
                    "wos_id": colluid,
                    "doc_type": doc_type,
                })
    return records


def parse_search_info(ndjson_text: str) -> Optional[dict]:
    """Extract searchInfo from NDJSON."""
    for line in ndjson_text.strip().split("\n"):
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue
        if obj.get("key") == "searchInfo":
            return obj.get("payload", {})
    return None


# -- Paper Conversion -------------------------------------------------

def api_record_to_paper(rec: dict) -> PaperRecord:
    return PaperRecord(
        title=rec.get("title", ""),
        authors=rec.get("authors", ""),
        pub_date=rec.get("pub_date", ""),
        journal=rec.get("journal", ""),
        doi=rec.get("doi", ""),
        url=rec.get("url", ""),
        abstract=rec.get("abstract", ""),
    )


# -- Display Helpers --------------------------------------------------

def print_query_summary(queries: list[dict], journals: List[str], year: Optional[str]):
    """Print a summary of queries to be executed."""
    print(f"\n{'='*60}")
    print(f"Queries to execute: {len(queries)}")
    print(f"Journals: {len(journals)}")
    print(f"Year filter: {year or 'none'}")
    print(f"{'='*60}\n")
    for i, q in enumerate(queries):
        query_rows = q["search"]["query"]
        desc = " AND ".join(
            f'{r.get("rowField","")}=("{r.get("rowText","")}")'
            for r in query_rows
        )
        print(f"[{i+1}/{len(queries)}] {desc}")


# -- Main -------------------------------------------------------------

def main():
    args = parse_args()

    # Phase: build queries only
    if args.phase == "build-queries" or args.phase is None:
        journals = load_journals(args.journals)
        keyword_groups = parse_keywords(args.keywords)
        year = parse_time(args.since, args.until)
        editions = [e.strip() for e in args.editions.split(",")] if args.editions else None

        queries = build_all_queries(journals, keyword_groups, year,
                                    editions, args.database, args.sort)
        print_query_summary(queries, journals, year)

        # Output the first query as JSON for Codex to execute
        print("\n=== FIRST_QUERY_JSON ===")
        print(json.dumps(queries[0], indent=2, ensure_ascii=False))
        print("=== END_FIRST_QUERY ===")

        # Output all queries as a JSON array
        print("\n=== ALL_QUERIES_JSON ===")
        print(json.dumps(queries, indent=2, ensure_ascii=False))
        print("=== END_ALL_QUERIES ===")

        return

    # Phase: process API results
    if args.phase == "process-results":
        if not args.api_result:
            print("ERROR: --api-result required for process-results phase")
            sys.exit(1)

        # Load existing Excel for dedup
        excel = ExcelManager(args.output)
        excel.load_existing_keys()

        # Parse NDJSON
        ndjson_text = args.api_result
        if Path(args.api_result).exists():
            ndjson_text = Path(args.api_result).read_text(encoding="utf-8")

        records = parse_ndjson_records(ndjson_text)
        search_info = parse_search_info(ndjson_text)

        total = search_info.get("RecordsFound", len(records)) if search_info else len(records)
        print(f"Total found by WOS: {total}")
        print(f"Records parsed: {len(records)}")


        # Filter by document type
        if args.doc_types:
            allowed_types = [t.strip() for t in args.doc_types.split(",")]
            before = len(records)
            records = [r for r in records if r.get("doc_type", "") in allowed_types]
            print(f"Doc-type filter ({args.doc_types}): {before} -> {len(records)}")


        # Convert to PaperRecord
        papers = [api_record_to_paper(r) for r in records]

        # Deduplicate
        new_papers, duplicates = excel.deduplicate_batch(papers)
        print(f"Already in Excel: {len(duplicates)}")
        print(f"New papers: {len(new_papers)}")

        # Apply limit
        if args.limit and len(new_papers) > args.limit:
            new_papers = new_papers[:args.limit]
            print(f"Limited to {args.limit} new papers")

        # Save new papers (without translation yet)
        if new_papers:
            excel.append(new_papers)
            print(f"Saved {len(new_papers)} new papers to {args.output}")

        # Print new papers for inspection
        print("\n=== NEW_PAPERS ===")
        for i, p in enumerate(new_papers):
            print(f"[{i+1}] {p.title[:80]}")
            print(f"    {p.authors[:60]}")
            print(f"    {p.journal}, {p.pub_date}")
            print(f"    DOI: {p.doi}")
            print()

        return

    # Default: build queries phase
    journals = load_journals(args.journals)
    keyword_groups = parse_keywords(args.keywords)
    year = parse_time(args.since, args.until)
    editions = [e.strip() for e in args.editions.split(",")] if args.editions else None

    queries = build_all_queries(journals, keyword_groups, year,
                                editions, args.database, args.sort)
    print_query_summary(queries, journals, year)

    print("\n=== FIRST_QUERY_JSON ===")
    print(json.dumps(queries[0], indent=2, ensure_ascii=False))
    print("=== END_FIRST_QUERY ===")


if __name__ == "__main__":
    main()
