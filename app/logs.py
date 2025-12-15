import datetime
import traceback

def SaveErrorLog(error: Exception):
    fileName = './logs/error-log-' + str(datetime.datetime.today()) + '.txt'
    with open(fileName, 'w') as file:
        file.write(str(error) + f'\n{traceback.format_exc()}')