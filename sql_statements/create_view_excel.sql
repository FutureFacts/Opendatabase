SELECT
    combination.Gemeentenaam as Gemeente,
    combination.MMR_indeling AS `CBS Wijk`,
    'TBD' as MMR_Wijk,
    combination.Codering as Code,
    0.0 as Factor,

#    -- Inwoners naar leeftijd
    combination.AantalInwoners as Inwoners_totaal,
    IFNULL(CAST(combination.pop0tm17 AS DECIMAL)/ NULLIF(combination.pop_totaal,0),0) as Kind_0_17,
    IFNULL(CAST(combination.pop18tm65 AS DECIMAL)/ NULLIF(combination.AantalInwoners,0),0) as Volwassene_18_65,
    IFNULL(CAST(combination.pop66tm74 AS DECIMAL)/ NULLIF(combination.AantalInwoners,0),0) as Oudere_66_74,
    IFNULL(CAST(combination.pop75tm84 AS DECIMAL)/ NULLIF(combination.AantalInwoners,0),0) as Oudere_75_84,
    IFNULL(CAST(combination.pop85enOuder AS DECIMAL)/ NULLIF(combination.AantalInwoners,0),0) as Oudere_85plus,
    IFNULL(CAST(combination.pop66tm74 + combination.pop75tm84 + combination.pop85enOuder AS DECIMAL) / NULLIF(combination.pop20tm65,0),0) AS `Grijze druk`,

 #   -- Jeugdhulpclienten per 1000 jeugdigen
    1000 * IFNULL(CAST(combination.Totaal_jeugdhulp AS DECIMAL)/ NULLIF(combination.pop0tm17,0),0) AS Jeugdhulpclienten_totaal,
    1000 * IFNULL(CAST(combination.Totaal_jeugdhulp_zonder_verblijf AS DECIMAL) / NULLIF(combination.pop0tm17,0),0) AS Jeugdhulpclienten_zonder_verblijf,
    1000 * IFNULL(CAST(combination.Jeugdhulp_met_verblijf AS DECIMAL) / NULLIF(combination.pop0tm17,0),0) AS Jeugdhulpclienten_met_verblijf,
    1000 * IFNULL(CAST(combination.Jeugdbescherming AS DECIMAL) / NULLIF(combination.pop0tm17,0),0) AS Jeugdhulpclienten_Jeugdbescherming,
    1000 * IFNULL(CAST(combination.Jeugdreclassering AS DECIMAL) / NULLIF(combination.pop0tm17,0),0) AS Jeugdhulpclienten_Jeugdreclassering,
    NULL AS `Jeugdhulpdiensten 18-22 totaal`,

#    -- WMO clienten per 1000 volwassenen
    1000 * CAST(combination.WmoTotaal AS DECIMAL) / (NULLIF(combination.AantalInwoners - combination.pop0tm17,0)) AS Totaal_WMO_clienten,
    1000 * CAST(combination.`Uitsluitend_Zorg_in_Natura_(ZIN)` AS DECIMAL) / (NULLIF(combination.AantalInwoners - combination.pop0tm17,0)) AS Alleen_ZIN,
    1000 * CAST(combination.`Uitsluitend_PersoonsGebondenBudget_(PGB)` AS DECIMAL) / (NULLIF(combination.AantalInwoners - combination.pop0tm17,0)) AS Alleen_PGB,
    1000 * CAST(combination.`Zowel_PGB_als_ZIN` AS DECIMAL) / (NULLIF(combination.AantalInwoners - combination.pop0tm17,0)) AS ZIN_en_PGB,

#    -- Dagbesteding etc
    'TBD' AS Huishoudelijke_Hulp,
    'TBD' AS Begeleiding,
    'TBD' AS Dagbesteding,
    
#     -- Huishoudens
    combination.HuishoudenTotaal AS Totaal_aantal_huishoudens,
    CAST(combination.Eenpersoonshuishoudens AS DECIMAL) / NULLIF(combination.HuishoudenTotaal,0) AS Eenpersoonshuishoudens,
    CAST(combination.HuishoudensZonderKinderen AS DECIMAL) / NULLIF(combination.HuishoudenTotaal,0) AS Huishoudens_zonder_kinderen,
    CAST(combination.HuishoudensMetKinderen AS DECIMAL) / NULLIF(combination.HuishoudenTotaal,0) AS Huishoudens_met_kinderen,

#    -- Etniciteit
    CAST(combination.NietWestersTotaal AS DECIMAL)/NULLIF(combination.AantalInwoners,0) As NietWesterse_Allochtonen,
    CAST(combination.WestersTotaal AS DECIMAL)/NULLIF(combination.AantalInwoners,0) As Westerse_Allochtonen,
    #--CAST(combination.WestersTotaal_17 + combination.NietWestersTotaal_18 AS DECIMAL)/NULLIF(combination.AantalInwoners_5,0) AS Allochtoon,
    1 - CAST(combination.WestersTotaal + combination.NietWestersTotaal AS DECIMAL)/NULLIF(combination.AantalInwoners,0) AS Autochtoon,

 #   -- Burgerlijke staat
    CAST(combination.Ongehuwd AS DECIMAL) / NULLIF(combination.AantalInwoners,0) AS Ongehuwd,
    CAST(combination.Gehuwd AS DECIMAL) / NULLIF(combination.AantalInwoners,0) AS Gehuwd,
    CAST(combination.Gescheiden AS DECIMAL) / NULLIF(combination.AantalInwoners,0) AS Gescheiden,
    CAST(combination.Verweduwd AS DECIMAL) / NULLIF(combination.AantalInwoners,0) AS Verweduwd,

#    -- Omgeving
    combination.AfstandTotHuisartsenpraktijk AS Afstand_tot_huisartsenpraktijk,
    combination.AfstandTotGroteSupermarkt AS Afstand_tot_grote_supermarkt,
    combination.AfstandTotKinderdagverblijf AS Afstand_tot_kinderdagverblijf,
    combination.AfstandTotSchool AS Afstand_tot_school,
    combination.ScholenBinnen3Km AS Aantal_scholen_binnen_3km,

#    -- Woonomstandigheden
    combination.PercentageKoopwoningen  AS Koopwoningen,
    combination.PercentageInBezitWoningcorporatie / 100 AS `Huurwoning woningcorporatie`,
    combination.`PercentageInBezitOverigeVerhuurders` / 100 AS `Huurwoningen Particulier`,
    combination.GemiddeldeWoningwaarde * 1000 AS Gemiddelde_Woningwaarde,

#    -- Inkomen
    combination.Actieven1575Jaar / 100 AS Aantal_participerenden_1575,
    1000 * CAST(combination.AantalInkomensontvangers AS DECIMAL) / NULLIF(combination.AantalInwoners,0) AS Aantal_inkomensontvangers_per_1000,
    combination.GemiddeldInkomenPerInkomensontvanger * 1000 AS Gemiddeld_inkomen_per_inkomensontvanger,
    combination.GemiddeldInkomenPerInwoner * 1000 AS Gemiddeld_inkomen_per_inwoner,
    combination.Huishoudens_met_laag_inkomen_percentage / 100 AS Huishoudens_met_een_laag_inkomen,
    combination.HuishoudensOnderOfRondSociaalminimum_percentage / 100 AS Huishouden_onder_of_rond_sociaal_minimum,

#    -- Uitkeringen
    1000 * CAST(combination.PersonenPerSoortUitkeringBijstand AS DECIMAL) / NULLIF(combination.pop18tm65,0) AS Bijstandsuitkering,
    1000 * CAST(combination.PersonenPerSoortUitkeringAO AS DECIMAL) / NULLIF(combination.pop18tm65,0) AS AO_Uitkering,
    1000 * CAST(combination.PersonenPerSoortUitkeringWW AS DECIMAL) / NULLIF(combination.`pop15tm75`,0) AS WW_Uitkering,
    combination.PersonenPerSoortUitkeringAOW AS AOW_Uitkering,

#    -- Jeugdhulp verwijzers
    IFNULL(combination.GemeentelijkeToegang,0) / NULLIF((IFNULL(combination.GemeentelijkeToegang,0) +
        IFNULL(combination.Huisarts,0) + IFNULL(combination.Jeugdarts,0) +
        IFNULL(combination.GecertificeerdeInstelling,0) + IFNULL(combination.MedischSpecialist,0) +
        IFNULL(combination.RechterOfficierVanJustitie,0) + IFNULL(combination.GeenVerwijzer,0) +
        IFNULL(combination.VerwijzerOnbekend,0)),0)
    AS Gemeentelijke_toegang,
    IFNULL(combination.Huisarts,0) / NULLIF((IFNULL(combination.GemeentelijkeToegang,0) +
        IFNULL(combination.Huisarts,0) + IFNULL(combination.Jeugdarts,0) +
        IFNULL(combination.GecertificeerdeInstelling,0) + IFNULL(combination.MedischSpecialist,0) +
        IFNULL(combination.RechterOfficierVanJustitie,0) + IFNULL(combination.GeenVerwijzer,0) +
        IFNULL(combination.VerwijzerOnbekend,0)),0)
        AS Huisarts,
    IFNULL(combination.Jeugdarts,0) / NULLIF((IFNULL(combination.GemeentelijkeToegang,0) +
        IFNULL(combination.Huisarts,0) + IFNULL(combination.Jeugdarts,0) +
        IFNULL(combination.GecertificeerdeInstelling,0) + IFNULL(combination.MedischSpecialist,0) +
        IFNULL(combination.RechterOfficierVanJustitie,0) + IFNULL(combination.GeenVerwijzer,0) +
        IFNULL(combination.VerwijzerOnbekend,0)),0)
    AS Jeugdarts,
    IFNULL(combination.GecertificeerdeInstelling,0) / NULLIF((IFNULL(combination.GemeentelijkeToegang,0) +
        IFNULL(combination.Huisarts,0) + IFNULL(combination.Jeugdarts,0) +
        IFNULL(combination.GecertificeerdeInstelling,0) + IFNULL(combination.MedischSpecialist,0) +
        IFNULL(combination.RechterOfficierVanJustitie,0) + IFNULL(combination.GeenVerwijzer,0) +
        IFNULL(combination.VerwijzerOnbekend,0)),0)
    AS Gecertificeerde_instelling,
    IFNULL(combination.MedischSpecialist,0) / NULLIF((IFNULL(combination.GemeentelijkeToegang,0) +
        IFNULL(combination.Huisarts,0) + IFNULL(combination.Jeugdarts,0) +
        IFNULL(combination.GecertificeerdeInstelling,0) + IFNULL(combination.MedischSpecialist,0) +
        IFNULL(combination.RechterOfficierVanJustitie,0) + IFNULL(combination.GeenVerwijzer,0) +
        IFNULL(combination.VerwijzerOnbekend,0)) ,0)
    AS Medisch_specialist,
    (IFNULL(combination.VerwijzerOnbekend,0) + IFNULL(combination.GeenVerwijzer,0) + IFNULL(combination.RechterOfficierVanJustitie,0)) /
        NULLIF((IFNULL(combination.GemeentelijkeToegang,0) +
        IFNULL(combination.Huisarts,0) + IFNULL(combination.Jeugdarts,0) +
        IFNULL(combination.GecertificeerdeInstelling,0) + IFNULL(combination.MedischSpecialist,0) +
        IFNULL(combination.RechterOfficierVanJustitie,0) + IFNULL(combination.GeenVerwijzer,0) +
        IFNULL(combination.VerwijzerOnbekend,0)),0)
    AS `Verwijzer_onbekend/Geen verwijzer`

 #   -- Jaartal
    # !!!! STILL TO ADD combination.Perioden AS Jaar
FROM CBS.combination 
WHERE soort_regio_nieuwe_indeling ='Wijk'

       
