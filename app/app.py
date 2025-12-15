from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import logic
import logs
import config

initialDirectory = config.getBaseFolder()

storageButtonMessage = 'Escolha um arquivo com os dados de estoque'
salesButtonMessage = 'Escolha o arquivo com os dados de vendas'
templateButtonMessage = 'Escolha um arquivo de base para o relatório'

storageFilePath= ''
salesFilePath = ''
templateFilePath = ''

storageFileName= storageButtonMessage
salesFileName = salesButtonMessage
templateFileName = templateButtonMessage

feedbackText = ''
feedbackColor = ''

def feedbackSuccess():
    return 'green'

def feedbackAttention():
    return 'orange'

def feedbackFail():
    return 'red'

def selectStorageFile():
    global storageFilePath
    global storageFileName
    global feedbackText
    global feedbackColor

    storageFilePath = filedialog.askopenfilename(
        title='Selecione o arquivo de dados de estoque',
        initialdir=initialDirectory,
        filetypes=(('CSV files', '*.csv'), ('All files', '*.*'))
    )

    if not storageFilePath:
        return

    print(storageFilePath)
    fileName = storageFilePath.split('/')[-1]
    if(fileName.__contains__('.csv')):
        storageFileName = fileName
        feedbackText = ''
        return
    
    feedbackColor = feedbackAttention()
    feedbackText = 'Arquivo de estoque deve estar no formato .csv'

def selectSalesFile():
    global salesFileName
    global salesFilePath
    global feedbackText
    global feedbackColor

    salesFilePath = filedialog.askopenfilename(
        title='Selecione o arquivo de dados de vendas',
        initialdir=initialDirectory,
        filetypes=(('CSV files', '*.csv'), ('All files', '*.*'))
    )

    if not salesFilePath:
        return

    fileName = salesFilePath.split('/')[-1]

    if(fileName.__contains__('.csv')):
        salesFileName = fileName
        feedbackText = ''
        return
    
    feedbackColor = feedbackAttention()
    feedbackText = 'Arquivo de vendas deve estar no formato .csv'

def selectTemplateFile():
    global templateFileName
    global templateFilePath
    global feedbackText
    global feedbackColor

    templateFilePath = filedialog.askopenfilename(
        title='Selecione o arquivo de base',
        initialdir=initialDirectory,
        filetypes=(('CSV files', '*.csv'), ('All files', '*.*'))
    )

    if not templateFilePath:
        return

    fileName = templateFilePath.split('/')[-1]

    if(fileName.__contains__('.csv')):
        templateFileName = fileName
        feedbackText = ''
        return
    
    feedbackColor = feedbackAttention()
    feedbackText = 'Arquivo base do relatório deve estar no formato .csv'

def generateReport():
    global feedbackText
    global feedbackColor

    if(storageFileName == storageButtonMessage or 
       salesFileName == salesButtonMessage or 
       templateFileName == templateButtonMessage ):
        feedbackColor = feedbackAttention()
        feedbackText = 'Selecione todos os arquivos primeiro'
        return

    try:
        feedbackColor = feedbackSuccess()
        feedbackText = logic.generateFinalDataframe(storageFilePath, salesFilePath, templateFilePath)
    except Exception as e:
        feedbackColor = feedbackFail()
        feedbackText = f"Erro inesperado. Tente novamente ou contate o desenvolvedor. Detalhes do erro salvos na pasta logs"
        logs.SaveErrorLog(e)

def selectBaseFolder():
    global initialDirectory

    baseFolderPath = filedialog.askdirectory(
        title='Selecione a pasta base'
    )

    config.setBaseFolder(baseFolderPath)
    initialDirectory = baseFolderPath
    

root = Tk()
root.title('Controle de estoque')
root.geometry('1000x250')
root.grid_columnconfigure(0, weight=2)

frame = ttk.Frame(root, padding=10)
frame.grid(row=0, column=0, sticky='nsew')
frame.grid_columnconfigure(0, weight=1)

ttk.Label(frame, text='Bem vindo(a)').grid(column=0, row=0, padx=10)

fileFrame = ttk.Frame(frame)
fileFrame.grid(column=0, row=1, padx=10, pady=10, sticky='nsew')
fileFrame.grid_columnconfigure(0, weight=1)
fileFrame.grid_columnconfigure(1, weight=1)
fileFrame.grid_columnconfigure(2, weight=1)

ttk.Button(fileFrame, text='Abrir arquivo de estoque', command=selectStorageFile).grid(column=0, row=0)
storageLabel = ttk.Label(fileFrame, text=storageFileName)
storageLabel.grid(column=0, row=1, padx=10, pady=10)

ttk.Button(fileFrame, text='Abrir arquivo de vendas', command=selectSalesFile).grid(column=1, row=0)
salesLabel = ttk.Label(fileFrame, text=salesFileName)
salesLabel.grid(column=1, row=1, padx=10, pady=10)

ttk.Button(fileFrame, text='Abrir arquivo de base', command=selectTemplateFile).grid(column=2, row=0)
templateLabel = ttk.Label(fileFrame, text=templateFileName)
templateLabel.grid(column=2, row=1, padx=10, pady=10)

ttk.Button(fileFrame, text='Gerar relatório', command=generateReport).grid(column=1, row=2)
feedbackLabel = ttk.Label(fileFrame, text=feedbackText, foreground='red', wraplength=500)
feedbackLabel.grid(column=1, row=3)

optionsFrame = ttk.Frame(frame)
optionsFrame.grid(column=0, row=2, padx=10, pady=10, sticky='nsew')
optionsFrame.grid_columnconfigure(0, weight=1)
optionsFrame.grid_columnconfigure(1, weight=1)

ttk.Button(optionsFrame, text='Quit', command=root.destroy).grid(column=0, row=0)
ttk.Button(optionsFrame, text='Pasta base', command=selectBaseFolder ).grid(column=1, row=0)

def updateLabels():
    storageLabel['text'] = storageFileName
    salesLabel['text'] = salesFileName
    templateLabel['text'] = templateFileName
    feedbackLabel['text'] = feedbackText

    feedbackLabel['foreground'] = feedbackColor

    root.after(1000, updateLabels)

root.after(1, updateLabels)
root.mainloop()