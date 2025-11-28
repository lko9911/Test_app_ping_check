# 📡 Ping Test & Visualization Tool

로컬 디바이스의 **IPv4 주소를 자동으로 감지**하고, 해당 IP를 대상으로 **Ping 테스트를 수행한 후 Plotly 그래프로 시각화**하는 네트워크 진단 프로그램입니다.

> ⚠ **주의:** 본 프로그램은 *로컬 디바이스에서 직접 실행*해야 합니다.  
> Docker, WSL, VM 등의 가상 환경에서는 가상 인터페이스의 IP가 반환되어 정확한 Ping 테스트가 불가능합니다.

---
<br>

## 🚀 주요 기능

- 로컬 IPv4 주소 자동 탐지
- Ping 테스트 자동 실행 (`ping3`)
- RTT(Round Trip Time) 계산
- Ping 성공/실패 로그 출력
- Plotly 기반 인터랙티브 그래프 시각화
- 평균 RTT를 그래프에 점선으로 표시<br>

---

## 📦 필요 패키지

- **ping3**
- **pandas**
- **plotly**

설치 방법은 아래 requirements.txt 사용법을 참고하세요.<br>

---

## ▶️ 실행 방법

### 1. 레포지토리 클론

```bash
git clone https://github.com/해당 주소
```

### 2. 의존성 설치
```bash
pip install -r requirements.txt
```
### 3. 프로그램 실행
```bash
python Ping_Check_test.py
```
<br>

## 📁 파일 구조
<pre><code>ping_test.py         # 메인 실행 파일
requirements.txt     # 패키지 목록
README.md            # 프로젝트 설명 파일</code></pre>
<br>
## 📊 결과 예시

<img width="1505" height="902" alt="스크린샷 2025-11-28 102025" src="https://github.com/user-attachments/assets/cac35afd-2be4-451a-9720-230ac560e42e" /><br>

## 📬 문의

버그 제보 또는 기능 개선 요청은 GitHub Issues나 메일에 남겨주세요 !



