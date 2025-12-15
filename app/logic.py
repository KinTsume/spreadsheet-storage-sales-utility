import pandas as pd
import unicodedata
import datetime
import config

basePath = config.getBaseFolder()

def generateFinalDataframe(storagePath, salesPath, templatePath):
    [storageDf, salesDf, templateDf] = loadDataframes(storagePath, salesPath, templatePath)

    size = getDataframeSize(templateDf)
    devices = getDevicesNames(templateDf)

    filledDataframe = getEmptyFinalDataframe(templateDf)

    for row in range(0, size[0]):
        companyName = templateDf.iat[row, 0]

        for column in range(1, size[1]):
            deviceName = devices[column - 1]

            filteredStorageDF = getFilteredDataframeByCompanyAndDevice(storageDf, companyName, deviceName, 'Nome Empresa', 'Descrição Produto')
            filteredSalesDF = getFilteredDataframeByCompanyAndDevice(salesDf, companyName, deviceName, 'NOME_FANTASIA', 'DESCRICAO')

            convertedStorageInt = filteredStorageDF['Saldo'].astype(int)
            storageSum = convertedStorageInt.sum()

            salesCount = filteredSalesDF['NOME_FANTASIA'].count()

            filledDataframe.at[row, (deviceName, 'estoque')] = storageSum
            filledDataframe.at[row, (deviceName, 'vendas')] = salesCount

    filledDataframe.to_csv(basePath + '/report-' + str(datetime.date.today()) + '.csv', index=False)
    return ('Relatório criado e salvo como: ' + 'report-' + str(datetime.date.today()) + '.csv')

def loadDataframes(storagePath, salesPath, templatePath):
    storageDf = pd.read_csv(storagePath, sep=';', encoding='latin1', low_memory=False)
    salesDf = pd.read_csv(salesPath, sep=';', encoding='utf-8', low_memory=False)
    templateDf = pd.read_csv(templatePath, sep=',', encoding='utf-8', low_memory=False)

    print(storageDf)

    storageDf['Nome Empresa'] = storageDf['Nome Empresa'].apply(remove_accents)
    salesDf['NOME_FANTASIA'] = salesDf['NOME_FANTASIA'].apply(remove_accents)
    templateDf['Lojas'] = templateDf['Lojas'].apply(remove_accents)

    return [storageDf, salesDf, templateDf]

def getDataframeSize(dataframe):
  targetRowsCount = dataframe.iloc[:, 0].count()
  targetColumnsCount = len(list(dataframe.columns))
  return [targetRowsCount, targetColumnsCount]

def getDevicesNames(targetDf):
  devices = []
  headers = list(targetDf.columns.get_level_values(0))
  headers.pop(0) #Remove the first column

  for header in headers:
    devices.append(header)

  return devices

def getEmptyFinalDataframe(targetDf):
  data = []
  columnTuples = [('Lojas', '-')]

  size = getDataframeSize(targetDf)
  devices = getDevicesNames(targetDf)

  for column in range(1, size[1]):
      deviceName = devices[column - 1]

      columnTuples.append((deviceName, 'estoque'))
      columnTuples.append((deviceName, 'vendas'))


  for row in range(0, size[0]):
    companyName = targetDf.iat[row, 0]

    rowData = [companyName]

    for column in range(1, size[1]):
      deviceName = devices[column - 1]

      rowData.append(0)
      rowData.append(0)

    data.append(rowData)

  multiLevelColumns = pd.MultiIndex.from_tuples(columnTuples)
  print(columnTuples)

  finalDataframe = pd.DataFrame(data, columns=multiLevelColumns)

  return finalDataframe

def getFilteredDataframeByCompanyAndDevice(dataframe, companyName, deviceName, companyFieldName, deviceFieldName):
  filtered = dataframe[(dataframe[companyFieldName].str.contains(companyName, case=False) & dataframe[deviceFieldName].str.contains(deviceName, case=False))]
  
  return filtered

def remove_accents(input_str):
  nfkd_form = unicodedata.normalize('NFKD', input_str)
  return ''.join([c for c in nfkd_form if not unicodedata.combining(c)])