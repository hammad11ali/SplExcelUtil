import re
from dataclasses import dataclass
from typing import List, Dict
from utils import log

verbose = False

@dataclass
class QueryResult:
    query: str
    headers: List[str]
    data: List[List[str]]
    row_count: int
    has_results: bool = True
    table_name: str = ""


def parse_query_result_block(block: str) -> tuple[list[str], list[list[str]]]:
    log('Parser', f"Parsing block:\n{block}", verbose)
    lines = [line.strip() for line in block.split('\n') if line.strip()]
    headers = []
    data_rows = []
    header_columns = 0
    current_header = []
    i = 0
    isPrevNonDased=False
    log('Parser', f"Lines found: {len(lines)}", verbose)
    log('Parser', f"Finding header columns", verbose)
    while i < len(lines):
        if all(c == '-' for c in lines[i].replace(';', '')):
            if i > 0:
                current_header.extend(lines[i-1].split(';'))
            i += 1
            isPrevNonDased=False
        else:
            if isPrevNonDased:
                break
            i += 1
            isPrevNonDased=True
            continue
            
  
    headers = [h.strip() for h in current_header]
    header_columns = len(headers)
    log('Parser', f"Header columns found: {header_columns}", verbose)
    i=i-1
    current_row = []
    log('Parser', f"Parsing data rows", verbose)
    for line in lines[i:]:
        if 'rows selected' in line or 'row selected' in line:
            break
        fields = [f.strip() for f in line.split(';')]
        current_row.extend(fields)
        
        if len(current_row) >= header_columns:
            data_rows.append(current_row[:header_columns])
            current_row = []
    log('Parser', f"Data rows found: {len(data_rows)}", verbose)
    return headers, data_rows

def find_table_name(block: str) -> str:
    log('Parser', f"Finding table name in block:\n{block}", verbose)
    table_name = ""
    if '**' in block:
        log('Parser', f"Block contains '**'. Attempting to find table name.", verbose)
        lines = block.split('\n')
        for line in lines:
            if 'select' in line.lower():
                break
            if '*' in line:
                start = line.find('*') + 1
                while start < len(line) and line[start] == '*':
                    start += 1
                end = line.find('*', start)
                if end == -1:
                    end = len(line)
                table_name = line[start:end].strip()
                break
    return table_name

def parse_spl_file(file_path: str, verbose_flag:bool) -> List[QueryResult]:
    global verbose
    verbose = verbose_flag
    log('Parser', f"Parsing file: {file_path}", verbose)
    with open(file_path, 'r') as f:
        content = f.read()

    # Split file into query blocks (separated by SQL> PROMPT)
    blocks = re.split(r'(?i)sql>\s*prompt', content)
    log('Parser', f"Found {len(blocks)} blocks in {file_path}.", verbose)
    results = []
    for block in blocks:
        if not block.strip() or not block.strip().replace('\n', ''):
            log('Parser', f"Skipping empty block. {block}", verbose)
            continue
        
        # Try to extract table name from PROMPT line
        table_name = find_table_name(block)
         
        # Extract query
        query_match = re.search(r'SELECT.*?(?=\n\n)', block, re.DOTALL | re.IGNORECASE)
        if not query_match:
            log('Parser', f"Skipping block without a valid query. {block}", verbose)
            continue
            
        query = query_match.group().strip()
        
        # Extract result data
        data_section = block[query_match.end():].strip()
        log('Parser', f"Data section found:\n{data_section}", verbose)
        if 'no rows selected' in data_section:
            results.append(QueryResult(
                query=query,
                headers=[],
                data=[],
                row_count=0,
                has_results=False,  # Mark as no results
                table_name=table_name
            ))
            log('Parser', f"No rows selected for query: {query}", verbose)
            continue
        
        log('Parser', f"Parsing data section:\n{data_section}", verbose)
        headers, data_rows = parse_query_result_block(data_section)
        log('Parser', f"Parsed headers: {headers}", verbose)
        log('Parser', f"Parsed data rows: {data_rows}", verbose)
        results.append(QueryResult(
            query=query,
            headers=headers,
            data=data_rows,
            row_count=len(data_rows),
            has_results=len(data_rows) > 0,
            table_name=table_name
        ))
    
    return results