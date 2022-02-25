import pandas as pd
import fnmatch
import openpyxl
import datetime
import win32com.client


datestring = str(datetime.datetime.now())
datestring = datestring.replace(':', '')
datestring = datestring.replace('.', '')
datestring = datestring.replace('-', '')
datestring = datestring.replace(' ', '')


enum = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
dfN = pd.read_csv(r'I:\PWOps\Lab\Wet Chem Instrumentation\BenchTemplates\comm\temp_dfN.csv')

xfile = openpyxl.load_workbook(r'I:\PWOps\Lab\Wet Chem Instrumentation\PrintTemplates\NO3 PRINT.xlsm', keep_vba = True)

temp = dfN.loc[dfN['Analysis'] == 'NO3-353.2']

printdfN = pd.DataFrame(temp, columns = ['LabNumber','SampleName', 'Sampled', 'Analyzed', 'InitialResult', 'InitialUnits', 'Batch'])

pt = xfile['PrintTemplate']

for letter in enumerate(enum):
    
    cell = letter[1] + '2'
    cName = pt[cell].value
    

    for indexrow, data in enumerate(printdfN[cName], start = 3):
    
        cell = letter[1] + str(indexrow)
        
        if printdfN[cName].name == 'Sampled':
            temp = data.split()[0]
            
            tlist = temp.split('-')
            temp = tlist[2] + '/' + tlist[1] + '/' + tlist[0]
            finaldate = temp + ' ' + data.split()[1]
            pt[cell].value = finaldate

        else:
            pt[cell].value = data
        

xfile.save(r'I:\PWOps\Lab\Wet Chem Instrumentation\print\NO3 Results' + datestring + '.xlsm')      
xfile.close()
o = win32com.client.Dispatch('Excel.Application')
o.visible = False
thwb = o.Workbooks.open(r'I:\PWOps\Lab\Wet Chem Instrumentation\print\NO3 Results' + datestring + '.xlsm')
thws = thwb.Worksheets([1])
thws.printout()

thwb.close()