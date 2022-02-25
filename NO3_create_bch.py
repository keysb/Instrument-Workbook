import pandas as pd
import datetime
import xlsxwriter

dfN = pd.read_csv(r'I:\PWOps\Lab\Wet Chem Instrumentation\BenchTemplates\comm\temp_dfN.csv')

datestring = str(datetime.datetime.now())
datestring = datestring.replace(':', '')
datestring = datestring.replace('.', '')
no3workbook = xlsxwriter.Workbook(r'M:\BENCH\Data_Entry_and_Review\NO3_Results' + datestring + '.xls')
detable = no3workbook.add_worksheet('DeTable')

row = 1
col = 0
for name in dfN:
    detable.write(0, col, name)
    col += 1
col = 0
for indexrow, data in enumerate(dfN.Analysis, start = 0):
    if data == 'NO3-353.2':
        for column in dfN:
            if column == 'Sampled':
                tstring = dfN.loc[indexrow,column]
                temp = tstring.split()[0]
                tlist = temp.split('-')
                temp = tlist[2] + '/' + tlist[1] + '/' + tlist[0]
                finaldate = temp + ' ' + tstring.split()[1]
                
                detable.write(row,col,finaldate)
                #temptime = dfN.loc[indexrow, column].strftime("%m/%d/%Y %H:%M")
                #detable.write(row, col, temptime)
            else:
                try:
                    detable.write(row, col, dfN.loc[indexrow, column])
                except:
                    pass
            
            col += 1
    
    
no3workbook.close()