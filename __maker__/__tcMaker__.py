import re, os

## SeleniumConverter ##
'''
1. Selenium IDE를 사용해서 TC 녹화
2. 저장 후 side 파일을 현재 내 코드에 맞도록 변환
3. side파일명이 함수명

# 세부 사항
1. 각 object의 target 내용을 읽어옴
ex) "target": "id=asdasdasd",
2. 처음부분이 findElement에서 첫번째 매개변수로, 두번째 부분이 path로 사용될듯
'''
# 가져온 문자열 정리

class TCMaker:

    def readSide(self,sideFile):
        def arrangeStr(_str):
            _str = _str.replace('\n','')
            _arranged = _str.strip() # 빈칸 제거
            _arranged = ''.join(x for x in _arranged if x not in ',"') # 쌍따옴표 제거
            return _arranged

        sf = open(sideFile, 'r', encoding='utf-8')

        sideLst = []

        for i in sf:
            if '"command"' in i :
                i = i.split(":")
                com = arrangeStr(i[1])

            elif '"target"' in i:
                i = i.split(":")
                tar = arrangeStr(i[1])
                sideLst.append([com, tar])
        # for i in sideLst:
        #     print(i)
        return sideLst

    def camelCase(self,st):
        output = ''.join(x for x in st.title() if x.isalnum())
        return output[0].lower() + output[1:]
        
    def snake_case(self,st):
        st = re.sub(r'(?<!^)(?=[A-Z])', '_', st).lower()
        return st

    def wait(self,_type, _path):
        waitCode = '\n'
        waitCode +="            self.webDriver.explicitlyWait(10, By.%s, '%s')\n"%(_type.upper(),_path)

        return waitCode

    def changeFullName(self, name):
        if name == 'css':
            name = 'css_selector'
        elif name == 'linkText':
            name = self.snake_case(name)
        return name

    def convert(self,fileName):

        sideAction = self.readSide('side/%s.side'%fileName)

        # 필요한 액션
        # 클릭, 입력 2개면 되나?

        fileNameSnakeCase = self.snake_case(fileName)


        pyCode = '''    def %s(self):    
        printLog(printSquare('%s'))
        result = FAIL
        msg = ''

        try:%s'''%(fileName, fileNameSnakeCase.split('_')[0].capitalize() + ' ' + fileNameSnakeCase.split('_')[1].capitalize(),'\n')

        for i in sideAction:    
            if i[0] == 'click':
                _type, path = i[1].split('=')            
                _type = self.changeFullName(_type)
                pyCode += self.wait(_type, path)
                pyCode += "            self.webDriver.findElement('%s', '%s', True)\n"%(_type, path)
                #print(c)
            elif i[0] == 'type':
                _type, path = i[1].split('=')       
                _type = self.changeFullName(_type)
                pyCode += self.wait(_type, path)
                pyCode += "            self.webDriver.findElement('%s', '%s', False)\n"%(_type, path)
                pyCode += "            self.webDriver.sendKeys('%s') # You have to change this you want to write\n"%('')
            elif i[0] == 'linkText':
                _type, path = i[1].split('=')       
                _type = self.changeFullName(_type)
                pyCode += "            self.webDriver.findElement('%s', '%s', True)\n"%(_type, path)
        pyCode += '''   
        except Exception as e:   
            result = FAIL
            msg = str(e).replace("\\n",'')
            msg = msg[:msg.find('Element <')]
            printLog("[%s] " + msg)
            printLog("[%s] RESULT : " + result)

        self._%sResult.append(['%s' + DELIM + '%s' + DELIM + result + DELIM + msg])        
        self.tl.junitBuilder('%s',result, msg)'''%(fileNameSnakeCase.split('_')[0].upper() + ' ' + fileNameSnakeCase.split('_')[1].upper(),\
                                                fileNameSnakeCase.split('_')[0].upper() + ' ' + fileNameSnakeCase.split('_')[1].upper(),\
                                                fileNameSnakeCase.split('_')[0].lower(),\
                                                fileNameSnakeCase.split('_')[0].lower(),\
                                                fileNameSnakeCase.split('_')[1].lower(), fileNameSnakeCase.upper())
        print(pyCode)

        # 파일 만들기
        
        pyFile = open('side/code/%s.py'%fileName, 'w', encoding='utf-8')
        pyFile.write(pyCode)
        pyFile.close()

aaa = TCMaker()
 
path_dir = r'./side'
 
file_list = os.listdir(path_dir)
file_list_side = [file for file in file_list if file.endswith(".side")]
print(file_list_side)

for i in file_list_side:
    fileName = i.replace('.side','')
    aaa.convert(fileName)