SuperVM 자동화 프로젝트

## 설치
#### PowerShell 또는 CMD 창에서 아래 명령어 입력
1) Selenium 설치
```
python -m pip install -r selenium
```

2) git 설정 (git 멤버일 경우 본인것으로 작성)
```
git init
git config --global user.name "dongill_lee" 
git config --global user.name "dongill_lee@tmax.co.kr" 
```

3) git clone
```
git clone http://192.168.105.140/cloudqa/supervm_automation.git
```

4) 해당 폴더 들어가서 파이썬 코드 실행
```
cd supervm_automation
python main.py
```
## 코드 작성 주의사항

### 명명규칙
* 함수명 : `lowerCamelCase`
* 변수명 : `_lowerCamelCase`
* 전역상수 : `UPPER`
* 소스코드 폴더명 : `__lower__`
* 소스코드 파일명 : `__lower__.py`