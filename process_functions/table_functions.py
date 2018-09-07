import pandas as pd
import cbsodata

def translator(string):
    exceptions = ['Appartement','VrijstaandeWoning','TweeOnderEenKapWoning',
                 'Hoekwoning','Tussenwoning','Huurwoning','EigenWoning',
                 'ClientenMetVoorzieningen','HuishoudensMetVoorzieningen']
    for x in exceptions:
        if x in string:
            return string
    split = string.split('_')
    if len(string.split('_')) == 1:
        return split[0]
    else:
        return '_'.join(split[:-1])

def process_data_buurten(CBS_codering,name):
    data = cbsodata.get_data(CBS_codering)
    collecting = {}
    year = int(''.join([x for x in name if x.isdigit()]))
    for row in reversed(data):
        collecting[int('1'+ row['Codering_3'][2:])] = row
        row['Perioden'] = year
        row['Gemeentenaam_1'] = row['Gemeentenaam_1'].strip()
        row['SoortRegio_2'] = row['SoortRegio_2'].strip()
    df = pd.DataFrame.from_dict(collecting, orient='index', dtype=None)
    df.rename(columns = translator,inplace = True) 
    return df

def process_data_jongeren(CBS_codering,name):
    data = cbsodata.get_data(CBS_codering)
    collecting = {}
    for row in data:
        if len(row['Perioden']) != 4:
            continue
        identifier = int('1'+row['Codering_3'][2:])
        if 'VormenVanJeugdzorg' in row.keys():
            TypeJeugdzorg = row['VormenVanJeugdzorg']
        else:
            TypeJeugdzorg = row['TypeJeugdzorg']
            
        if identifier in collecting:
            result = collecting[identifier]
            result[TypeJeugdzorg] = row['TotaalJongerenMetJeugdzorg_5']
        else:
            row[TypeJeugdzorg] = row['TotaalJongerenMetJeugdzorg_5']
            row['Gemeentenaam_1'] = row['Gemeentenaam_1'].strip()
            row['Wijken'] = row['Wijken'].strip()
            collecting[identifier] = row            
    df = pd.DataFrame.from_dict(collecting, orient='index', dtype=None)
    df.rename(columns = translator,inplace = True)
    return df    

def process_data_wmo(CBS_codering,name):
    data = cbsodata.get_data(CBS_codering)
    collecting = {}
    for row in reversed(data):
        if len(row['Perioden']) != 4 or len(row['Codering_3'].rstrip()) == 0:
            continue
        identifier = int('1' + row['Codering_3'][2:])
        Financieringsvorm = row['Financieringsvorm']
        if identifier in collecting:
            result = collecting[identifier]
            result[Financieringsvorm] = row['WmoClienten_5']
            result[Financieringsvorm + ' per100Inwoners_6'] = row['WmoClientenPer1000Inwoners_6']
        else:
            row[Financieringsvorm] = row['WmoClienten_5']
            row[Financieringsvorm + ' per100Inwoners_6'] = row['WmoClientenPer1000Inwoners_6']
            collecting[identifier] = row
    df = pd.DataFrame.from_dict(collecting, orient='index', dtype=None)
    df.rename(columns = translator,inplace = True)
    return df

def process_data_sociale_voorzieningen(CBS_codering,name):
    data = cbsodata.get_data(CBS_codering)
    collecting = {}
    for row in reversed(data):
        if len(row['Perioden']) != 4 or len(row['Codering_3'].rstrip()) == 0:
                continue
        identifier = int('1' + row['Codering_3'][2:])
        collecting[identifier] = row
    df = pd.DataFrame.from_dict(collecting, orient='index', dtype=None)
    df.rename(columns = translator,inplace = True)
    return df

def process_data_gezondheidsmonitor(CBS_codering,name):
    data = cbsodata.get_data(CBS_codering)
    buurten2016 = cbsodata.get_data('83487NED')
    translate2016 = {}
    for row in buurten2016:
        if row['SoortRegio_2'].rstrip() == 'Gemeente':
            translate2016[row['WijkenEnBuurten']] = row['Codering_3']
            
    collecting = {}
    for row in data:
        try:
            identifier = int('1' + translate2016[row['RegioS']][2:])
            collecting[identifier] = row
        except:
            pass
    df = pd.DataFrame.from_dict(collecting, orient='index', dtype=None)
    df.rename(columns = translator,inplace = True)
    return df
