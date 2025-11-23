import streamlit as st
import subprocess
import platform
import socket
import netifaces  # pip install netifaces

# -----------------------------
# 로컬 IP 가져오기 (Windows 기준)
# -----------------------------
def get_local_ip():
    """
    Windows 환경에서 활성화된 IPv4 주소 가져오기.
    루프백(127.0.0.1) 제외.
    """
    try:
        for iface in netifaces.interfaces():
            addrs = netifaces.ifaddresses(iface)
            if netifaces.AF_INET in addrs:
                for addr in addrs[netifaces.AF_INET]:
                    ip = addr['addr']
                    if not ip.startswith("127."):
                        return ip
        return "127.0.0.1"
    except Exception as e:
        return "127.0.0.1"

# -----------------------------
# 핑 함수
# -----------------------------
def ping_host(host, count=4):
    """
    지정된 호스트로 핑을 보내고 결과를 반환
    """
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
        st.error(f"오류 발생: {e}")
        return False, ""

    if result.returncode == 0:
        return True, result.stdout
    else:
        return False, result.stdout

# -----------------------------
# Streamlit UI
# -----------------------------
st.title("웹 Ping 확인 프로그램")

# 호스트와 핑 횟수 입력
host = st.text_input("Ping 할 호스트 입력", "google.com")
count = st.number_input("Ping 횟수", min_value=1, max_value=10, value=4)

# 로컬 IP 자동 감지
local_ip_address = get_local_ip()
st.subheader("로컬 디바이스 정보")
st.write(f"현재 운영체제: {platform.system()}")
st.write(f"자동 감지된 로컬 IP 주소: **{local_ip_address}**")

if local_ip_address == "127.0.0.1":
    st.warning("경고: 네트워크 연결이 없거나 IP를 찾을 수 없어 루프백 주소(127.0.0.1)를 사용합니다.")

# 핑 버튼
if st.button("Ping 실행"):
    st.info(f"[{host}]에 {count}회 핑 시도 중...")
    success, output = ping_host(host, count)
    if success:
        st.success(f"[{host}] 핑 성공! ✅")
        st.text(output)
    else:
        st.error(f"[{host}] 핑 실패 ❌")
        st.text(output)
