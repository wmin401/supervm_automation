## 설치
#### PowerShell 또는 CMD 창에서 아래 명령어 입력
1) Selenium 설치
```
python -m pip install selenium
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

4) 해당 폴더 들어가서 파이썬 코드 실행(직접 파이썬 코드 빌드 가능)
```
cd supervm_automation
python main.py
```

## TestLink 연동
* TestLink
  1) 테스트링크 접속(http://192.168.105.140:8081/testlink/index.php)
  2) 자동화 테스트 플랜(automation)에 자동화 테스트케이스 추가
  3) 추가한 테스트 케이스의 Custom Field(SuperVM_Automation)값 추가
  4) 추가한 테스트 케이스의 Execution Type을 Manual -> Automated 로 수정
* 소스코드
  1) testlink 클래스 생성
    ```
    from __common__.__testlink__ import *
    ...
    self.tl = testlink()
    ```
  2) junitBuilder 함수 작성
    ```
    self.tl.junitBuilder('{Custom Field 값}', 결과값, 메세지)
    ```
  3) Jenkins에서 빌드시 junit_'{Custom Field 값}''xml 파일이 생성됨
    ```
    <testsuite>
    <?xml version='1.0' encoding='utf-8'?>
        <testcase classname="{Custom Field 값}" name="{Custom Field 값}" status="결과값(소문자+ed)" />
    </testsuite>
    ```
  4) 테스트링크 Custom Field와 xml 파일의 classname이 일치하면 결과 업데이트
  
## SSH 명령어 전달
1) ssh 클래스 선언
  * ` ssh_connection ` 클래스 사용
  * 매개변수 : ` 호스트 IP, 호스트 PORT, 호스트 ID, 호스트 PW `
  ```
  ssh = ssh_connection('192.168.17.161', 22, 'root', 'asdf')
  ```
2) ssh 연결 활성화
  * ` activate ` 함수 사용
  * 매개변수 없음  
  ```
  ssh.activate()
  ```
3) 명령어 입력
  * ` commandExec ` 함수 사용  
  * 매개변수 : ` 명령어, timeout 시간 `
  ```
  ssh.commandExec('dnf -y install wget', timeout=15) # timeout은 입력해도되고 안해도됨
  ```
4) ssh 연결 비활성화
  * ` deactivate ` 함수 사용  
  * 매개변수 없음
  ```
  ssh.deactivate()
  ```
* 사용 방법
  1) 코드 상단에 ` from __common__.__ssh__ import * ` 추가
  2) 원하는 위치에 ` ssh_connection ` 클래스 선언 및 ` activate() 실행 `
  3) 명령어 입력 후 출력으로 분석
  4) 테스트 결과 반영 후 ` deactivate `

## 설치 자동화
##### Jenkins에서 설치시 윈도우 노드 hosts에 내용 추가하는 것이 필요(수동)
### 실행 순서
1) parameter 값 변경 후 ` __install__.py ` 실행
2) ovirt 설치 -> nfs/ceph 구성 -> ` answers.conf ` 파일 생성 -> Deploy

  

## 코드 작성 주의사항
### 명명규칙
* 함수명 : `lowerCamelCase`
* 변수명 : `_lowerCamelCase`
* 전역상수 : `UPPER`
* 소스코드 폴더명 : `__lower__`
* 소스코드 파일명 : `__lower__.py`
* Custom Field명 : ``UPPER_TEST_NAME``