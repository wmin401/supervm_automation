from __common__.__parameter__ import *
from __common__.__module__ import *

# 처음 실행시 결과 폴더 생성
# 결과 파일 생성(단, 매개변수가 False이면 결과 파일은 생성하지 않음)
def initResult(csvSave=False):
    makeFolder(RESULT_PATH)
    makeFolder(RESULT_PATH + '/tmp')
    makeFolder(RESULT_PATH+'/log')

    if csvSave == True:
        with open(RESULT_PATH+'/'+RESULT_FILE,'w',encoding='utf-8') as file:
            file.write('Category' + DELIM + 'Test' + DELIM + 'Result' + DELIM + 'Message\n')

        with open(RESULT_PATH+'/tmp/'+TMP_RESULT_FILE,'w',encoding='utf-8') as tmpFile:
            tmpFile.write('Category' + DELIM + 'Test' + DELIM + 'Result' + DELIM + 'Message\n')

# 하나의 모듈 테스트가 끝나면 해당 결과를 저장해주는 함수
def saveRealTimeResult(res):
    with open(RESULT_PATH+'/tmp/'+TMP_RESULT_FILE,'a',encoding='utf-8') as tmpFile:
        tmpFile.write(res + '\n')

# 전체결과를 저장하기 위한 함수
def saveTotalResult(lst):
    with open(RESULT_PATH+'/'+RESULT_FILE,'a',encoding='utf-8') as file:
        for i in lst:
            file.write(i[0] + '\n')