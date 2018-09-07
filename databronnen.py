from process_functions.table_functions import (process_data_buurten,
                             process_data_jongeren, 
                             process_data_wmo,
                             process_data_sociale_voorzieningen,
                             process_data_gezondheidsmonitor)
from process_functions.age_functions import (read_population_data_asc,
                                             read_population_data_xlsx
                                            )


cijfers_buurten_en_wijken = {'leeftijd_2015':('./age_data/age_data_2015.xlsx',
                                               read_population_data_xlsx
                                             ),
                             'leeftijd_2016':('./age_data/age_data_2016.xlsx',
                                               read_population_data_xlsx
                                             ),
                             'leeftijd_2017':('./age_data/age_data_2017.xlsx',
                                               read_population_data_xlsx
                                             ),
                             'Leeftijd_2018':('./age_data/age_data_2018.asc',
                                               read_population_data_asc
                                             ),
                             'BuurtenenWijken2015':('83220NED',process_data_buurten),
                             'BuurtenenWijken2016':('83487NED',process_data_buurten),
                             'BuurtenenWijken2017':('83765NED',process_data_buurten),
                             'BuurtenenWijken2018':('84286NED',process_data_buurten),
                             'jongeren2015':('82964NED',process_data_jongeren),
                             'jongeren2016':('83563NED',process_data_jongeren),
                             'jongeren2017':('83782NED',process_data_jongeren),
                             'wmo2015':('83267NED',process_data_wmo),
                             'wmo2016':('83620NED',process_data_wmo),
                             'wmo2017':('83818NED',process_data_wmo),
                             'sociale_voorzieningen_2015':('83265NED',process_data_sociale_voorzieningen),
                             'sociale_voorzieningen_2016':('83619NED',process_data_sociale_voorzieningen),
                             'sociale_voorzieningen_2017':('83817NED',process_data_sociale_voorzieningen),
                             'gezondheids_monitor_2016':('83674NED',process_data_gezondheidsmonitor)}
