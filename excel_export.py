import pandas as pd
from parser import QueryResult
from typing import List

from utils import create_file, create_folder, log

verbose = False
def save_to_sheet(writer, df, sheet_name: str, query: str,):
    """
    Save a DataFrame to an Excel sheet with the query as a comment.
    """
    df.to_excel(writer, sheet_name=sheet_name, index=False, startrow=1)
    worksheet = writer.sheets[sheet_name]
    worksheet['A1']=query
    log('Excel Export', f"Saved {sheet_name} with query: {query}", verbose=verbose)

def save_to_file(df, file_name: str, sheet_name: str, query: str):
    """
    Save a DataFrame to an Excel file.
    """
    log('Excel Export', f"Saving file {file_name} with sheet {sheet_name}...", verbose=verbose)
    with pd.ExcelWriter(file_name+'.xlsx', engine='openpyxl') as writer:
        save_to_sheet(writer, df, sheet_name, query)
        

def export_to_excel(results: List[QueryResult], destination: str, separate: bool = False, verbose_flag: bool = False, showstats: bool = False):
    global verbose
    verbose = verbose_flag
    log('Excel Export', f"Exporting {len(results)} results to {destination}...", verbose)
    sheets = []
    # Create a summary sheet if requested
    if showstats:
        log('Excel Export', "Creating summary stats...", verbose)
        summary_data = {
            'Query Number': range(1, len(results) + 1),
            'Query': [result.query for result in results],
            'Row Count': [result.row_count for result in results]
        }
        df_summary = pd.DataFrame(summary_data)
        sheets.append((df_summary, "Summary", "List of queries and their row counts"))
        log('Excel Export', "Summary stats created.", verbose)
    
    # First create a sheet for queries with no results
    no_result_queries = [result.query for result in results if not result.has_results]
    if no_result_queries:
        log('Excel Export', f"Seggregating queries with no results...", verbose)
        df_no_results = pd.DataFrame({
            'Query Number': range(1, len(no_result_queries) + 1),
            'Query': no_result_queries
        })
        sheets.append((df_no_results, "No Results", "Queries with no results"))
        log('Excel Export', "No results queries created.", verbose)
        log('Excel Export', f"Found {len(no_result_queries)} queries with no results.", verbose, mandatory=True)

    # Create sheets for queries with results
    log('Excel Export', f"Creating sheets for queries with results...", verbose)
    sheet_num = 1
    for result in results:
        if result.has_results:
            if result.table_name:
                sheet_name = result.table_name
            else:
                sheet_name = f"Query_{sheet_num}"
            df = pd.DataFrame(result.data, columns=result.headers)
            sheets.append((df, sheet_name, result.query))
            sheet_num += 1
    log('Excel Export', f"Found {len(sheets)} queries with results.", verbose, mandatory=True)
        

    if separate:
        # In this case, destination is a folder
        destination = create_folder(destination)
        log("Export", f"Creating folder: {destination}", verbose, mandatory=True)
        for df, sheet_name, query in sheets:
            file_name = f"{destination}/{sheet_name}.xlsx"
            save_to_file(df, file_name,  sheet_name, query)
    else:
        # In this case, destination is a file
        log('Excel Export', f"Creating file: {destination}", verbose, mandatory=True)
        destination=create_file(destination)
        with pd.ExcelWriter(destination, engine='openpyxl') as writer:
            for df, sheet_name, query in sheets:
                save_to_sheet(writer, df, sheet_name, query)
    