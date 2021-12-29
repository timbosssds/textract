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


# Works - as in reads and prints JSON
# =============================================================================
# # https://stackoverflow.com/questions/20199126/reading-json-from-a-file
# with open("analyzeDocResponse.json") as json_file:
#     json_data = json.load(json_file)
#     print(json_data)
# =============================================================================
    

with open("analyzeDocResponse.json") as json_file:
    json_data = json.load(json_file)
    #print(json_data)
    doc = json_data

#print(doc)

# Needed for downstream processing (pre-processing)
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
            
            
import pandas as pd

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
print('Len of dataframe', len(dataframes))
#print(dataframes)

# Build  from this...
# =============================================================================
# for df in dataframes:
#     if df.shape[0]>2:
#         print('yes')
#     else:
#         print('no')
# 
# =============================================================================

# This leaves just the df, build on this
# =============================================================================
# clean_list = []
# for df in dataframes:
#     if df.shape[0]>2:
#         #print('yes')
#         clean_list.append(df)
#     else:
#         print('no')
# print(len(clean_list))
# print(clean_list)
# =============================================================================

# Proves you can't treat this data like a list
#https://appdividend.com/2020/01/21/python-list-contains-how-to-check-if-item-exists-in-list/
# =============================================================================
# print(clean_list)
# if 'Dark' in clean_list:
#     print("Yes, 'S Eductation' found in List : ", listA)
# else:
#     print("Nope, 'Dark' not found in the list")
# =============================================================================

# I came up with this... seems useful, build on it
# =============================================================================
# for df in dataframes:
#     if df.shape[0]>2:
#         print(df.columns)
#     else:
#         print('no')
# =============================================================================

# Progress point
# =============================================================================
# for df in dataframes:
#     if 'Start date' in df.columns:
#         print('Yipee')
#     else:
#         print('no')
# =============================================================================

# Might not needs all below, but keep hacking till result, then refine
want = []
for df in dataframes:
    if 'Start date' in df.columns:
        want.append(df)
        print('remove')
    else:
        print('remove')

#print('... want...', want)    


for df in want:
    #print(df.shape[1])
    print(df.columns)
    


############################## ----------- Fixing the column header issue

# ------------------ want headers from above for below
print('..........   gap   ..........')

import numpy as np
new_want = []
for df in want:
    if 'Start date' in df.columns:
        new_want.append(df)
        #print('Yipee')
    else:
        print('no')
print(new_want)        
df1 = pd.DataFrame(np.concatenate(new_want))
df1.columns = df.columns
df1.to_csv('out.csv')
print('... df1 ...', df1)
