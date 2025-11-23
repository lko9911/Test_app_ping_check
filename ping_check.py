import streamlit as st
import subprocess
import platform
import socket

# -------------------
# 로컬 IP 감지 함수
# -------------------
def get_local_ip():
    s = None
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))  # 실제 데이터는 보내지 않음
        local_ip = s.getsockname()[0]
        return local_ip
    except Exception:
        try:
            return socket.gethostbyname(socket.gethostname())
        except:
            return "127.0.0.1"
    finally:
        if s:
            s.close()

# -------------------
# 핑 함수
# -------------------
def ping_host(host, count=4):
    current_os = platform.system().lower()

    if current_os == "windows":
        command = ['ping', '-n', str(count), host]
    else:
        command = ['ping', '-c', str(count), host]

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=10,
            check=False
        )
    except Exception as e:
        return f"오류 발생: {e}"

    if result.returncode == 0:
        return f"✅ [{host}] 핑 성공!\n\n{result.stdout}"
    else:
        return f"❌ [{host}] 핑 실패!\n\n{result.stdout}"

# -------------------
# Streamlit UI
# -------------------
st.title("웹 Ping 확인 프로그램")

# 자동 감지된 로컬 IP
local_ip_address = get_local_ip()
st.subheader("로컬 디바이스 정보")
st.text(f"운영체제: {platform.system()}")
st.text(f"자동 감지된 로컬 IP: {local_ip_address}")

if local_ip_address == "127.0.0.1":
    st.warning("네트워크 연결이 없거나 IP를 찾을 수 없어 루프백 주소(127.0.0.1)를 사용합니다.")

# 사용자가 핑할 호스트 입력
host = st.text_input("Ping 할 호스트 입력", "google.com")
count = st.number_input("Ping 횟수", min_value=1, max_value=10, value=4)

if st.button("Ping 실행"):
    output = ping_host(host, count)
    st.text_area("Ping 결과", output, height=200)
