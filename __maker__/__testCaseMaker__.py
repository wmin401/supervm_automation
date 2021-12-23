## Test Case Maker ##
# Selenium IDE를 사용하여 녹화된 테스트 케이스를 현재 SuperVM 자동화 코드에 맞게 변환 시켜주는 코드
# side -> python

'''
1. Selenium IDE 프로젝트 생성
 * 파일명 규칙 : camelCase, 테스트+테스트이름 ex. vmCreate, qosCreate
2. 녹화 시작
3. *.side 파일을 __maker__/side에 저장
4. 이 파일 빌드
5. side파일명.py 로 code 폴더에 생성됨
6. 기존 테스트 코드에 복사/붙여넣기
7. 변환된 코드를 수정(각 테스트에 맞게)
  * 시간이 오래걸리면 time.sleep를 넣어줌
  * sendKeys는 직접 입력해줘야함
  * 필요없는 코드는 삭제
8. 필요한 코드는 직접 추가
'''

import re, os
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

        try:
            sideObjects = self.readSide('side/%s.side'%fileName)
            fileNameSnakeCase = self.snake_case(fileName)
            fileNameSnakeList = fileNameSnakeCase.split('_')
            

            pyCode = '''
### Copy below function to your class ###


    def %s(self):    
        printLog(printSquare('%s'))
        result = FAIL
        msg = ''

        try:%s'''%(fileName,\
                   " ".join(str(i).capitalize() for i in fileNameSnakeList),\
                   '\n')

            for i in sideObjects:    
                if i[0] == 'click' or i[0] == 'linkText':
                    _type, target = i[1].split('=')            
                    _type = self.changeFullName(_type)
                    pyCode += '\n            # %s'%i[0]
                    pyCode += self.wait(_type, target)
                    pyCode += "            self.webDriver.findElement('%s', '%s', True)\n"%(_type, target)
                    #print(c)
                elif i[0] == 'type':
                    _type, target = i[1].split('=')       
                    _type = self.changeFullName(_type)
                    pyCode += '\n            # %s'%i[0]
                    pyCode += self.wait(_type, target)
                    pyCode += "            self.webDriver.findElement('%s', '%s', False)\n"%(_type, target)
                    pyCode += "            self.webDriver.sendKeys('%s') # You have to change this you want to write\n"%('')

            pyCode += '''   
        except Exception as e:   
            result = FAIL
            msg = str(e).replace("\\n",'')
            msg = msg[:msg.find('Element <')]
            printLog("[%s] " + msg)
            printLog("[%s] RESULT : " + result)

        self._%sResult.append(['%s' + DELIM + '%s' + DELIM + result + DELIM + msg])        
        self.tl.junitBuilder('%s',result, msg)'''%(" ".join(str(i).upper() for i in fileNameSnakeList),\
                                                   " ".join(str(i).upper() for i in fileNameSnakeList),\
                                                   fileNameSnakeList[0].lower(),\
                                                   fileNameSnakeList[0].lower(),\
                                                   " ".join(str(fileNameSnakeList[i]).lower() for i in range(1,len(fileNameSnakeList))),\
                                                   fileNameSnakeCase.upper())
        

            # 파일 만들기
            if not os.path.isdir('side/code'):
                os.makedirs('side/code')

            pyFile = open('side/code/%s.py'%fileName, 'w', encoding='utf-8')
            pyFile.write(pyCode)
            pyFile.close()

            if os.path.isfile('side/code/%s.py'%fileName):
                print("Succesfully side/code/%s.py was created !!!"%fileName)
            else:
                print("Failed to create side/code/%s.py file :("%fileName)
        except Exception as e:
            print("Exception occured : %s"%(str(e)))
aaa = TCMaker()
 
path_dir = r'./side'
 
file_list = os.listdir(path_dir)
file_list_side = [file for file in file_list if file.endswith(".side")]
print(file_list_side)

for i in file_list_side:
    fileName = i.replace('.side','')
    aaa.convert(fileName)