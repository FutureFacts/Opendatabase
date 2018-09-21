import cbsodata
from collections import defaultdict
import pandas as pd


def add_population(data,codering,CBS_code,population,age):
    data[codering]['Codering'] = CBS_code
    data[codering]['totaal'] += population
    if age < 18:
        data[codering]['0tm17'] += population
    elif age < 66:
        data[codering]['18tm65'] += population
    elif age < 75:
        data[codering]['66tm74'] += population
    elif age < 85:
        data[codering]['75tm84'] += population
    else:
        data[codering]['85'] += population
    if age < 76 and age > 14:
        data[codering]['15tm75'] += population
    if age < 66 and age > 19:
        data[codering]['20tm65'] += population
    return data

def read_population_data_asc(source,name):
    buurten = defaultdict(lambda:defaultdict(int))
    with open(source,'r',encoding='latin1') as bevolking_data:
        for regels in bevolking_data:
            code = regels[120:128]
            #print(code)
            codering = '1' + code
            buurtcode = 'BU' + code
            wijkcode = 'WK' + code[0:6]
            gemeentecode = 'GM' + code[0:4]
            gemeentenaam = regels[60:120].strip()
            if gemeentenaam == 'Onbekend':
                continue
            leeftijd = int(regels[189:191])
            aantal_bewoners = int(regels[191:197])
            buurten = add_population(buurten,int(codering),buurtcode,aantal_bewoners,leeftijd)
            buurten = add_population(buurten,int(codering[0:7]),wijkcode,aantal_bewoners,leeftijd)
            buurten = add_population(buurten,int(codering[0:5]),gemeentecode,aantal_bewoners,leeftijd)
            buurten = add_population(buurten,100,'NL00',aantal_bewoners,leeftijd)
    bevolkingsdata = pd.DataFrame.from_dict(buurten, orient='index', dtype=None)
    return bevolkingsdata

source_translator = {2015:'83220NED',
                     2016:'83487NED',
                     2017:'83765NED'
                     }


def read_population_data_xlsx(source,name):
    wijken = defaultdict(str)
    codering = defaultdict(str)
    year = int(''.join([x for x in name if x.isdigit()]))
    cbs_bron = source_translator[year]
    data_buurtenwijken = cbsodata.get_data(cbs_bron)
    for x in data_buurtenwijken:
        wijk = x['WijkenEnBuurten'].strip()
        gemeente = x['Gemeentenaam_1'].strip()
        if x['Codering'][0:2] == 'WK':
            wijken[(gemeente,wijk)] = x['Codering']
            codering[x['Codering']] = (gemeente,wijk)

    ##HIER LADEN WE DE BEWONERSDATA 2018 IN DE DATABASE, NOG IN SQL SERVER ZETTEN
    ## This file needs the document  "kale bron 2015.xlsx" to be in the same folder to run.

    population_data = pd.read_excel(source)
    population_data['Codering'] = population_data.apply(lambda x: wijken[(x['GemeenteGBA'],x['GWBnaam'+str(year)].strip())],axis =1)
    population_data['0tm17'] = 0
    population_data['18tm65'] = 0
    population_data['66tm74'] = 0
    population_data['75tm84'] = 0
    population_data['85'] = 0
    population_data['totaal'] = 0
    population_data['20tm65'] = 0
    population_data['15tm75'] = 0
    def optellen(wijk):
        if year == 2015:
            leeftijd = wijk['Leeftijd']
        else:
            leeftijd = wijk['jaren']
        aantal_bewoners = wijk['Aantal']
        wijk['totaal'] += aantal_bewoners
        if leeftijd < 18:    
            wijk['0tm17'] += aantal_bewoners
        elif leeftijd < 66:    
            wijk['18tm65'] += aantal_bewoners
        elif leeftijd < 75:    
            wijk['66tm74'] += aantal_bewoners
        elif leeftijd < 85:    
            wijk['75tm84'] += aantal_bewoners
        else:   
            wijk['85'] += aantal_bewoners
        if leeftijd < 66 and leeftijd > 19:
            wijk['20tm65'] += aantal_bewoners
        if leeftijd < 76 and leeftijd > 14:
            wijk['15tm75'] += aantal_bewoners
        return wijk

    population_data = population_data.apply(optellen, axis =1)
    population_data = population_data[['totaal','0tm17','18tm65','66tm74','75tm84','85','20tm65','15tm75','Codering_3']].groupby(['Codering_3']).sum()
    population_data['Codering'] = population_data.index
    population_data = population_data.reset_index(drop=True)
    population_data = population_data[1:]
    population_data['Gemeentecode'] = population_data['Codering'].apply(lambda x:'GM'+  x[2:6])
    NL = population_data.sum()
    NL['Codering'] = 'NL00'
    NL['Gemeentecode'] = 'NL00'
    GM = population_data.groupby('Gemeentecode').sum()
    GM['Codering'] = GM.index
    GM = GM.reset_index(drop=True)
    result = pd.concat([population_data,GM],ignore_index = True)
    result = result.append(NL,ignore_index = True)
    result.index = result['Codering'].map(lambda x: int('1' + x[2:]))
    result = result.rename_axis('codering')
    return result
