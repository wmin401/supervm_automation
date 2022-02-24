from __common__.__parameter__ import *
from __common__.__module__ import *

def initResult():
    makeFolder(RESULT_PATH)
    makeFolder(RESULT_PATH + '/tmp')
    makeFolder(RESULT_PATH+'/log')

    with open(RESULT_PATH+'/'+RESULT_FILE,'w',encoding='utf-8') as file:
        file.write('Category' + DELIM + 'Test' + DELIM + 'Result' + DELIM + 'Message\n')

    with open(RESULT_PATH+'/tmp/'+TMP_RESULT_FILE,'w',encoding='utf-8') as tmpFile:
        tmpFile.write('Category' + DELIM + 'Test' + DELIM + 'Result' + DELIM + 'Message\n')

def saveRealTimeResult(res):
    with open(RESULT_PATH+'/tmp/'+TMP_RESULT_FILE,'a',encoding='utf-8') as tmpFile:
        tmpFile.write(res + '\n')

def saveTotalResult(lst):
    with open(RESULT_PATH+'/'+RESULT_FILE,'a',encoding='utf-8') as file:
        for i in lst:
            file.write(i[0] + '\n')