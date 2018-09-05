import pandas as pd
def combine(original,older,source = {}):
    wanted_columns = list(original.columns)
    if len(source) == 0:
        source = {x:original['Perioden'].iloc[0] for x in original.columns}


    unchanged = original[original['IndelingswijzigingWijkenEnBuurten'] == '1'].copy()
    changed = original[original['IndelingswijzigingWijkenEnBuurten'] != '1'].copy()

    unchanged_trans = {x: x + 'recent' for x in unchanged.columns} 
    older_trans = {x: x + 'older' for x in older.columns} 
    unchanged.rename(columns = unchanged_trans,inplace = True)
    older.rename(columns = older_trans,inplace = True)

    merged = unchanged.merge(
        older,
        #how = 'left',
        left_index=True,
        right_index=True,
        suffixes = ('recent','older')
    )
    for column in list(wanted_columns):
        if False in merged[column+'recent'].isnull().value_counts():
            merged[column] = merged[column+'recent']
            source[column] = merged['Periodenrecent'].iloc[0]
        else:
            try:
                merged[column] = merged[column+'older'] 
                source[column] = merged['Periodenolder'].iloc[0]
            except:
                print(column, "doensn't exist in the older source")
    merged = merged[wanted_columns]
    merged = merged.append(changed)

    return merged.copy(),source

def list_combine(to_combine):
    names = sorted(to_combine.keys())[::-1]
    updated = to_combine[names[0]]
    source = {}
    for name in names[1:]:
        df = to_combine[name]
        updated,source = combine(updated,df,source)
    source = pd.DataFrame.from_dict({1:source},orient='index', dtype=None)
    return updated,source
