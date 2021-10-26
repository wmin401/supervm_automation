import os
## 시작시간과 종료시간을 입력받으면 시, 분, 초로 보여주는 함수
def secToHms(start, end): # 시작시간, 끝나는 시간
    sec = end - start
    m, s = divmod(sec, 60)
    h, m = divmod(m, 60)
    return h,m,s

## 메세지 리스트 처리하는 부분
def mergeMsg(msg):
    ## 에러 최대 두번째 줄까지만 추가
    merge = ''
    if len(msg) < 1:
        merge = ''
    elif len(msg) == 1:
        merge = msg[0]
    else:
        merge = ''
        for i in range(0,2):
            msg[i] = msg[i].replace("\n",' ')
            msg[i] = msg[i].replace(";",'')
            merge += msg[i]
    return merge

def makeUpMsg(msg_list):
    ## 입력받은 메시지 리스트에서 \n과 , 삭제
    returnMsg = []
    for i in msg_list:
        i = i.replace('\n','')
        #i = i.replace(',', ' ')
        returnMsg.append(i)
    return returnMsg

## 해당 경로에있는 파일을 읽어오고, 테스트 진행시 파일에 있는 내용은 테스트를 실행하지 않고 넘어감
def getListinFile(list_path_):
    #No stop daemon    
    _LIST = open(list_path_, 'r', encoding='utf-8').read()
    _LIST = [v for v in _LIST.split('\n') if v]
    return _LIST

## 원하는 경로에 폴더를 생성해줌
## 하위 경로 입력시, 폴더가 존재하지 않으면 같이 생성
def makeFolder(path_):
    if os.path.isdir(path_):
        print("* " + path_ + ' folder is already existed!')
        return
    else:
        print("* " + path_ + ' folder made!')
        os.makedirs(path_)


def printLine():
    print('---------------------------------------------------------')