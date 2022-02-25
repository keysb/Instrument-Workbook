import sys
import qUERIES as sq
import pandas as pd
import pyodbc
import datetime
import xlsxwriter
import csv


srvr = "ch-dbss4"
db = "CHW_Element"
userid = "CHW_Element_ReportUser"
pwd = "boise15!"


Nbatches = sq.NO3_Batches(sys.argv[1])

conn = pyodbc.connect("Driver={SQL Server};Server=" + srvr + ";Database=" + db + ";uid=" + userid + ";pwd=" + pwd + ";")
cursor = conn.cursor()

df = pd.read_sql(Nbatches, conn)

Narray = [] 
                                #initialize array for NOx NO2 batches
for ind, item in enumerate(df.Analysis, start=0):
    if item != 'NO3-353.2':
        Narray.append(df.loc[ind,"Batch"])
    else:
        NO3LIMSBatch = df.loc[ind,"Batch"]
        Narray.append(df.loc[ind, "Batch"])

dfNO3 = pd.read_sql(sq.NO3_LIMS(NO3LIMSBatch), conn)
print(dfNO3.to_string())

Ndata = sq.NO3_calcdata(Narray[0], Narray[1], Narray[2], dfNO3.loc[0,'LIMSID'])
dfN = pd.read_sql(Ndata, conn)

with open('I:\PWOps\Lab\Wet Chem Instrumentation\BenchTemplates\comm\errorlog.txt', 'w') as f:
	f.write(dfNO3.to_string())

for index, analysis in enumerate(dfN.Analysis, start = 0):
	if analysis == 'NO3-353.2':
		
		noxvalue = dfN.loc[(dfN.LabNumber == dfN.loc[index,'LabNumber']) & (dfN.Analysis == 'NOx-353.2 (W)'),'InitialResult'].values[0]
		noxtime = dfN.loc[(dfN.LabNumber == dfN.loc[index,'LabNumber']) & (dfN.Analysis == 'NOx-353.2 (W)'),'Analyzed'].values[0]        

		noxtime = pd.to_datetime(str(noxtime))
		no2 = dfN.loc[(dfN.SampleName == dfN.loc[index, 'SampleName']) & (dfN.Analysis == 'NO2-353.2'),'InitialResult'].values[0]

		no3 = noxvalue - no2
		noxtime = noxtime.strftime("%m/%d/%Y %H:%M")
		dfN.loc[index,'InitialResult'] = no3
		dfN.loc[index,'Analyzed'] = noxtime

 

        
        
cursor.close()
conn.close()

dfNTransfer = dfN[['LabNumber', 'SampleName', 'InitialResult', 'Analysis', 'Batch', ]]
dfNTransfer.to_csv(r'I:\PWOps\Lab\Wet Chem Instrumentation\BenchTemplates\comm\pycomm.csv')
