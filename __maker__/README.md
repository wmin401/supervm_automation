## Test Case Maker ##
#### Selenium IDE를 사용하여 녹화된 테스트 케이스를 현재 SuperVM 자동화 코드에 맞게 변환 시켜주는 코드

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