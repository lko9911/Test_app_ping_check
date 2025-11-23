import subprocess
import platform
import socket
import streamlit as st

# --- IP 가져오기 함수 ---
def get_local_ip():
    s = None
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
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

# --- Ping 함수 ---
def ping_host(host, count=4):
    current_os = platform.system().lower()
    if current_os == "windows":
        command = ['ping', '-n', str(count), host]
    else:
        command = ['ping', '-c', str(count), host]

    st.write(f"[{host}]에 핑 시도 중...")
    
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=10,
            check=False
        )
    except Exception as e:
        st.error(f"오류 발생: {e}")
        return False

    if result.returncode == 0:
        st.success(f"[{host}] 핑 성공! ✅")
        st.text(result.stdout)
        return True
    else:
        st.error(f"[{host}] 핑 실패 ❌")
        st.text(result.stdout)
        return False

# --- Streamlit UI ---
st.title("웹 Ping 확인 프로그램")

host = st.text_input("Ping 할 호스트 입력", "google.com")
count = st.number_input("Ping 횟수", min_value=1, max_value=10, value=4)

if st.button("Ping 실행"):
    st.subheader("--- 로컬 디바이스 정보 ---")
    local_ip_address = get_local_ip()
    st.write(f"현재 운영체제: {platform.system()}")
    st.write(f"자동 감지된 로컬 IP 주소: {local_ip_address}")
    
    if local_ip_address == "127.0.0.1":
        st.warning("네트워크 연결이 없거나 IP를 찾을 수 없어 루프백 주소(127.0.0.1)를 사용합니다.")
    
    # 1. 로컬 IP 핑 테스트
    st.write("\n### 로컬 IP 핑 테스트")
    ping_host(local_ip_address, count=2)
    
    # 2. 사용자가 입력한 호스트 핑 테스트
    st.write("\n### 입력한 호스트 핑 테스트")
    ping_host(host, count=count)
