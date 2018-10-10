import pandas as pd
pd.set_option('use_inf_as_null', True)

def absolute_values_BeW(data):
    data['Oppervlakte'] = data['AantalInwoners']/data['Bevolkingsdichtheid']
    data['Totale_Woningwaarde'] = data['Woningvoorraad'] * data['GemiddeldeWoningwaarde']

    percentages_woningvoorraad = ['PercentageEengezinswoning',
                                 'PercentageMeergezinswoning',
                                 'PercentageBewoond',
                                 'PercentageOnbewoond',
                                 'Koopwoningen',
                                 'HuurwoningenTotaal_41',
                                 'InBezitWoningcorporatie',
                                 'InBezitOverigeVerhuurders',
                                 'EigendomOnbekend',
                                 'BouwjaarVoor2000',
                                 'BouwjaarVanaf2000',
                                ]


    data['Eengezinswoningen_Totaal'] = data['PercentageEengezinswoning'] * data['Woningvoorraad'] / 100
    data['Meergezinswoning_Totaal'] = data['PercentageMeergezinswoning'] * data['Woningvoorraad'] / 100
    data['Bewoond_Totaal'] = data['PercentageBewoond'] * data['Woningvoorraad'] / 100
    data['Onbewoond_Totaal'] = data['PercentageOnbewoond'] * data['Woningvoorraad'] / 100
    data['Koopwoningen_Totaal'] = data['Koopwoningen'] * data['Woningvoorraad'] / 100
    data['Huurwoningen_Totaal'] = data['HuurwoningenTotaal_41'] * data['Woningvoorraad'] / 100
    data['InBezitWoningcorporatie_Totaal'] = data['InBezitWoningcorporatie'] * data['Woningvoorraad'] / 100
    data['InBezitOverigeVerhuurders_Totaal'] = data['InBezitOverigeVerhuurders'] * data['Woningvoorraad'] / 100
    data['EigendomOnbekend_Totaal'] = data['EigendomOnbekend'] * data['Woningvoorraad'] / 100
    data['BouwjaarVoor2000_Totaal'] = data['BouwjaarVoor2000'] * data['Woningvoorraad'] / 100
    data['BouwjaarVanaf2000_Totaal'] = data['BouwjaarVanaf2000'] * data['Woningvoorraad'] / 100


    ## Energy_usage, is dropped for now
    energy_usage = [ 'GemiddeldElektriciteitsverbruikTotaal',
                     'Appartement_48',
                     'Tussenwoning_49',
                     'Hoekwoning_50',
                     'TweeOnderEenKapWoning_51',
                     'VrijstaandeWoning_52',
                     'Huurwoning_53',
                     #'Koopwoning',
                     'GemiddeldAardgasverbruikTotaal',
                     'Appartement_56',
                     'Tussenwoning_57',
                     'Hoekwoning_58',
                     'TweeOnderEenKapWoning_59',
                     'VrijstaandeWoning_60',
                     'Huurwoning_61',
                     #'Koopwoning',
                     'PercentageWoningenMetStadsverwarming',
                    ]

    ## Inkomen
    inkomen_relatief = ['GemiddeldInkomenPerInkomensontvanger',
                         'GemiddeldInkomenPerInwoner',
                         'k_40PersonenMetLaagsteInkomen',
                         'k_20PersonenMetHoogsteInkomen',
                         'k_40HuishoudensMetLaagsteInkomen',
                         'k_20HuishoudensMetHoogsteInkomen',
                         'HuishoudensMetEenLaagInkomen',
                         'HuishOnderOfRondSociaalMinimum']

    data['inkomen_totaal'] = data['GemiddeldInkomenPerInkomensontvanger'] * data['AantalInkomensontvangers'] / 100
    data['Laagste_inkomen_k40_totaal'] = data['k_40PersonenMetLaagsteInkomen'] * data['AantalInkomensontvangers'] / 100
    data['Hoogste_inkomen_k20_totaal'] = data['k_20PersonenMetHoogsteInkomen'] * data['AantalInkomensontvangers'] / 100
    data['Hoogste_inkomen_k20_totaal_huishoudens'] = data['k_20HuishoudensMetHoogsteInkomen'] * data['HuishoudensTotaal'] / 100
    data['Laagste_inkomen_k20_totaal_huishoudens'] = data['k_40HuishoudensMetLaagsteInkomen'] * data['HuishoudensTotaal'] / 100
    data['Huishoudens_met_laag_inkomen_totaal'] = data['HuishoudensMetEenLaagInkomen'] * data['HuishoudensTotaal'] / 100
    data['HuishoudensOnderOfRondSociaalminimum_totaal'] = data['HuishOnderOfRondSociaalMinimum'] * data['HuishoudensTotaal'] / 100


    ## Personen_autos
    personen_autos = ['PersonenautoSPerHuishouden',
                     'PersonenautoSNaarOppervlakte']

    data['Personenautos_totaal'] = data['PersonenautoSPerHuishouden'] * data['HuishoudensTotaal']


    #Afstanden voorzieningen
    afstanden_voorzieningen = [ 'AfstandTotHuisartsenpraktijk',
                                 'AfstandTotGroteSupermarkt',
                                 'AfstandTotKinderdagverblijf',
                                 'AfstandTotSchool',
                                 'ScholenBinnen3Km']


    data['AfstandTotHuisartsenpraktijk_totaal'] = data['AfstandTotHuisartsenpraktijk'] * data['AantalInwoners']
    data['AfstandTotGroteSupermarkt_totaal'] = data['AfstandTotGroteSupermarkt'] * data['AantalInwoners']
    data['AfstandTotKinderdagverblijf_totaal'] = data['AfstandTotKinderdagverblijf'] * data['AantalInwoners']
    data['AfstandTotSchool_totaal'] = data['AfstandTotSchool'] * data['AantalInwoners']
    data['ScholenBinnen3Km_totaal'] = data['ScholenBinnen3Km'] * data['AantalInwoners']



    #data['PercentageEengezinswoning'].iloc[1] * data['Woningvoorraad'].iloc[1] / 100
    data = data.drop(['SterfteRelatief','GemiddeldeHuishoudensgrootte','Bevolkingsdichtheid',
                  'Bevolkingsdichtheid','GemiddeldeWoningwaarde',] + 
                  percentages_woningvoorraad + 
                  energy_usage +
                  inkomen_relatief +
                  personen_autos + 
                  afstanden_voorzieningen,
                  axis = 1)

    columns_not_in_both = ['GeboorteRelatief','Koopwoning','Koopwoning','EigenWoning_54',
                           'EigenWoning_62', 'Dekkingspercentage','MateVanStedelijkheid',
                           'Omgevingsadressendichtheid' , 'MeestVoorkomendePostcode']

    for column in columns_not_in_both:
        if column in data.columns:
            data.drop([column], axis = 1,inplace = True)
    return data
