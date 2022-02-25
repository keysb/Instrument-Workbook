# -*- coding: utf-8 -*-
"""
Created on Mon Jan  4 18:19:43 2021

@author: bkeys
"""

def getBatchesforDate(thedate, theanalysis ,theanalysis2 = "", theanalysis3 = ""):
    
   
    if theanalysis2 and not theanalysis3:
        sqlcondition = "(dbo.SAMPLEEXTRACTION.Analysis = '" + theanalysis + "' OR dbo.SAMPLEEXTRACTION.Analysis = '" + theanalysis2 + "') \
            AND dbo.SAMPLEEXTRACTION.Extracted BETWEEN '" + thedate +  " 00:01' AND '" + thedate +  " 23:59'"
    elif theanalysis3:
        sqlcondition = "(dbo.SAMPLEEXTRACTION.Analysis = '" + theanalysis + "' OR dbo.SAMPLEEXTRACTION.Analysis = '" + theanalysis2 + "' \
        OR dbo.SAMPLEEXTRACTION.Analysis = '" + theanalysis3 + "') AND dbo.SAMPLEEXTRACTION.Extracted BETWEEN '" + thedate +  " 00:01' AND '" + thedate +  " 23:59'"
    else:
        sqlcondition = "dbo.SAMPLEEXTRACTION.Analysis = '" + theanalysis + "' AND dbo.SAMPLEEXTRACTION.Extracted BETWEEN '" + thedate +  " 00:01' AND '" + thedate +  " 23:59'"
    sqlcf1 = "SELECT DISTINCT dbo.SAMPLEEXTRACTION.Batch, dbo.SAMPLEEXTRACTION.Analysis FROM dbo.SAMPLEEXTRACTION WHERE " + sqlcondition
                
    return sqlcf1

def NO3_LIMS(batch):
    sqlcf1 = "SELECT DISTINCT dbo.SAMPLEEXTRACTION.Wrk + '-' + dbo.SAMPLEEXTRACTION.Sample AS 'LIMSID' FROM dbo.SAMPLEEXTRACTION \
        WHERE dbo.SAMPLEEXTRACTION.Batch = '" + batch + "'"
    return sqlcf1

def NO3_Batches(thedate):
    return getBatchesforDate(thedate, 'NOx-353.2 (W)', 'NO2-353.2', 'NO3-353.2')

def NO3_calcdata(batch1, batch2, batch3, LIMS):
    

    sqlcondition = "(dbo.SAMPLEEXTRACTION.Batch = '" + batch1 + "' OR dbo.SAMPLEEXTRACTION.Batch = '" + batch2 + "' OR dbo.SAMPLEEXTRACTION.Batch = '" + batch3 + "') \
        AND dbo.SAMPLEEXTRACTION.Wrk + '-' + dbo.SAMPLEEXTRACTION.Sample = '" + LIMS + "'"


    sqlcf1 = "SELECT DISTINCT dbo.SAMPLEEXTRACTION.Wrk + '-' + dbo.SAMPLEEXTRACTION.Sample as 'LabNumber', dbo.WRKSAMPLE.SampleName, dbo.WRKSAMPLE.Sampled, \
        null as 'SourceID', dbo.SAMPLEANALYSIS.Analysis, dbo.SAMPLEANALYSIS.Analyte, dbo.SAMPLEANALYSIS.Analyzed as 'Analyzed', dbo.SAMPLEANALYSIS.Result as 'InitialResult', \
        '' as 'mdl', '' as 'mrl', 'mg/L' as 'InitialUnits', '1' as 'dilution', \
        dbo.SAMPLEANALYSIS.Analyst, 'FIA 5' as 'instrument', 'InstrumentWorkbook' as 'fileID', dbo.SAMPLEEXTRACTION.Batch, Null as 'client', \
        Null as 'qctype', null as 'Initial', null as 'Final' FROM dbo.SAMPLEEXTRACTION INNER JOIN dbo.WRKSAMPLE ON \
        dbo.SAMPLEEXTRACTION.Wrk = dbo.WRKSAMPLE.Wrk AND dbo.SAMPLEEXTRACTION.Sample = dbo.WRKSAMPLE.Sample INNER JOIN dbo.SAMPLEANALYSIS ON \
        dbo.SAMPLEANALYSIS.Wrk = dbo.SAMPLEEXTRACTION.Wrk AND dbo.SAMPLEANALYSIS.Sample = dbo.SAMPLEEXTRACTION.Sample AND \
        dbo.SAMPLEANALYSIS.Analysis = dbo.SAMPLEEXTRACTION.Analysis WHERE " + sqlcondition 
    return sqlcf1