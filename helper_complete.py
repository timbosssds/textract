# succesfully extracted the df i wanted to csv

# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import os as os 
#print(os.getcwd)
#analyzeDocResponse

import json
import numpy as np
import pandas as pd

# Works - as in reads and prints JSON
# =============================================================================
# # https://stackoverflow.com/questions/20199126/reading-json-from-a-file
# with open("analyzeDocResponse.json") as json_file:
#     json_data = json.load(json_file)
#     print(json_data)
# =============================================================================
    
""" Read JSON """
with open("analyzeDocResponse.json") as json_file:
    json_data = json.load(json_file)
    #print(json_data)
    doc = json_data
#print(doc)


""" Pre-processing """
#https://maxhalford.github.io/blog/textract-table-to-pandas/
def map_blocks(blocks, block_type):
    return {
        block['Id']: block
        for block in blocks
        if block['BlockType'] == block_type
    }

blocks = doc['Blocks']
tables = map_blocks(blocks, 'TABLE')
cells = map_blocks(blocks, 'CELL')
words = map_blocks(blocks, 'WORD')
selections = map_blocks(blocks, 'SELECTION_ELEMENT')

def get_children_ids(block):
    for rels in block.get('Relationships', []):
        if rels['Type'] == 'CHILD':
            yield from rels['Ids']


""" Process JSON to create dataframes """
dataframes = []
for table in tables.values():

    # Determine all the cells that belong to this table
    table_cells = [cells[cell_id] for cell_id in get_children_ids(table)]

    # Determine the table's number of rows and columns
    n_rows = max(cell['RowIndex'] for cell in table_cells)
    n_cols = max(cell['ColumnIndex'] for cell in table_cells)
    content = [[None for _ in range(n_cols)] for _ in range(n_rows)]

    # Fill in each cell
    for cell in table_cells:
        cell_contents = [
            words[child_id]['Text']
            if child_id in words
            else selections[child_id]['SelectionStatus']
            for child_id in get_children_ids(cell)
        ]
        i = cell['RowIndex'] - 1
        j = cell['ColumnIndex'] - 1
        content[i][j] = ' '.join(cell_contents)

    # We assume that the first row corresponds to the column names
    dataframe = pd.DataFrame(content[1:], columns=content[0])
    dataframes.append(dataframe)            


""" Remove unwanted data """
stage = []
for df in dataframes:
    if 'Start date' in df.columns:
        stage.append(df)


""" Process for output """
out = []
for df in stage:
    if 'Start date' in df.columns:
        out.append(df)
        #print('Yipee')
    else:
        print('no')
#print(out)        
df1 = pd.DataFrame(np.concatenate(out))
df1.columns = df.columns
df1.to_csv('out.csv',index=False)
print('... df1 ...', df1)

