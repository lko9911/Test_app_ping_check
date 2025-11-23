import streamlit as st
import subprocess
import platform
import socket

# --- 헬퍼 함수 1: 로컬 IP 가져오기 (선택 사항) ---
def get_local_ip():
    """현재 로컬 디바이스의 IP 주소를 가져옵니다."""
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


# --- 헬퍼 함수 2: 핑 실행 로직 ---
def run_ping(host, count=4):
    """
    지정된 호스트로 핑을 보내고 결과를 문자열로 반환합니다.
    """
    current_os = platform.system().lower()

    if current_os == "windows":
        # 윈도우: -n 옵션으로 핑 횟수 지정
        command = ['ping', '-n', str(count), host]
    else:
        # 리눅스/macOS (Unix 계열): -c 옵션으로 핑 횟수 지정
        command = ['ping', '-c', str(count), host]

    # Streamlit에서 결과를 보기 좋게 출력하기 위해 stdout과 stderr을 모두 반환
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=10, 
            check=False
        )
    except Exception as e:
        return False, f"**오류 발생:** `ping` 명령을 실행할 수 없습니다. ({e})"

    # returncode 0이면 성공, 그 외는 실패
    success = result.returncode == 0
    
    # stdout을 보여주고, 에러가 있다면 stderr도 추가로 보여줍니다.
    output_text = result.stdout
    if result.stderr:
        output_text += f"\n\n**stderr (오류 출력):**\n{result.stderr}"

    return success, output_text


# --- Streamlit 메인 앱 구성 ---
def main():
    st.set_page_config(page_title="간단 핑 체커", layout="wide")
    st.title("🌐 간단 네트워크 핑(Ping) 확인기")
    st.markdown("---")

    # 1. 사이드바에 로컬 IP 정보 표시 (선택 사항)
    local_ip = get_local_ip()
    st.sidebar.info(f"💡 현재 로컬 IP: **{local_ip}**")
    st.sidebar.markdown("이 앱은 Streamlit과 `subprocess` 모듈을 사용합니다.")

    # 2. 사용자 입력 위젯
    # 기본값으로 구글 DNS를 미리 넣어둡니다.
    target_host = st.text_input(
        "핑을 확인할 호스트 이름 또는 IP 주소를 입력하세요:",
        value="8.8.8.8"
    )

    # 3. 핑 횟수 선택
    ping_count = st.slider(
        "핑 테스트 횟수 선택:",
        min_value=1, 
        max_value=10, 
        value=4
    )
    
    # 4. 실행 버튼
    # 버튼이 눌렸을 때만 핑 테스트를 실행합니다.
    if st.button("핑 테스트 실행", type="primary"):
        if not target_host:
            st.error("호스트 주소를 입력해주세요.")
            return

        # 결과 출력을 위한 컨테이너 (스피너가 돌아가게 만듭니다.)
        with st.spinner(f"**{target_host}**로 핑 테스트를 실행 중입니다... (총 {ping_count}회)"):
            ping_success, ping_output = run_ping(target_host, count=ping_count)

        # 핑 결과 출력
        st.markdown("### 📋 핑 테스트 결과")
        
        if ping_success:
            st.success(f"✅ **{target_host}** 핑 성공! (응답 있음)")
        else:
            st.error(f"❌ **{target_host}** 핑 실패. (응답 없음 또는 호스트를 찾을 수 없음)")
            
        # 상세 출력 (ping 명령어의 원본 출력을 코드 블록으로 표시)
        st.subheader("상세 출력")
        st.code(ping_output, language='text')

if __name__ == "__main__":
    main()