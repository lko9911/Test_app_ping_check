import ping3
import streamlit as st
import socket
import sys

# --- 헬퍼 함수 1: 로컬 IP 가져오기 (이전 코드와 동일) ---
def get_local_ip():
    """
    현재 실행 중인 로컬 디바이스의 IP 주소를 가져옵니다.
    외부 연결 시도를 통해 가장 효율적인 로컬 IP를 얻는 방법입니다.
    """
    s = None
    try:
        # 실제 외부 통신을 수행하지 않고 연결만 시도하여
        # 해당 소켓이 사용할 로컬 IP 주소를 얻어냅니다.
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # 구글 DNS 서버에 연결(Connect)을 시도합니다.
        # 실제 데이터는 보내지 않으므로 안전하며, NAT 환경에서 정확한 내부 IP를 얻을 수 있습니다.
        s.connect(('8.8.8.8', 80)) 
        local_ip = s.getsockname()[0]
        return local_ip
    except Exception:
        # 연결 실패 시(예: 네트워크 연결 없음), 호스트 이름으로 시도해봅니다.
        # 이는 127.0.0.1 (루프백)을 반환할 가능성이 높습니다.
        try:
            return socket.gethostbyname(socket.gethostname())
        except:
            return "127.0.0.1" # 최후의 수단
    finally:
        if s:
            s.close()

# --- 수정된 헬퍼 함수 2: ping3 실행 로직 ---
def run_ping3(host, count=4):
    """
    ping3 라이브러리를 사용하여 지정된 호스트로 핑을 보냅니다.
    """
    results = []
    
    st.info(f"**{host}**로 ICMP Echo Request 패킷을 {count}회 보냅니다.")
    
    # ⚠️ 수정된 부분: NeedRootPrivilege 관련 코드를 제거합니다.
    # if sys.platform != "win32" and ping3.EXCEPTIONS['NeedRootPrivilege']: <--- 이 부분이 오류를 발생시켰습니다.
    #     st.warning("⚠️ Linux/macOS 사용자 경고...")
    
    # 새로운 Streamlit 경고: ping3가 관리자 권한을 요구할 수 있음을 간단히 안내
    #if sys.platform != "win32":
    #    st.warning("⚠️ **참고:** Linux/macOS 환경에서는 `ping3` 실행에 관리자 권한(root/sudo)이 필요할 수 있습니다.")


    for i in range(1, count + 1):
        # ping3.ping() 함수는 응답 시간을 초 단위로 반환합니다.
        # 실패 시 False (패킷 손실), None (타임아웃), 또는 문자열 에러 메시지 반환
        delay = ping3.ping(host, timeout=2) 
        
        status_text = f"시도 {i}/{count}: "
        
        if isinstance(delay, float):
            # 성공적으로 응답을 받은 경우
            rtt_ms = delay * 1000 # 초 단위를 밀리초(ms)로 변환
            results.append(rtt_ms)
            status_text += f"응답 성공! RTT: **{rtt_ms:.2f} ms**"
            st.text(status_text)
        elif delay is False:
            # TTL 만료, 패킷 손실 등 (정상적인 실패)
            status_text += "응답 실패 (패킷 손실/TTL 만료)"
            st.warning(status_text)
        elif delay is None:
            # 타임아웃
            status_text += "타임아웃 (응답 없음)"
            st.error(status_text)
        elif isinstance(delay, str):
            # 호스트를 찾을 수 없는 등의 에러
            status_text += f"오류 발생: {delay}"
            st.error(status_text)
            
    return results

# --- Streamlit 메인 앱 구성 ---
def main():
    st.set_page_config(page_title="Ping3 핑 체커", layout="wide")
    st.title("📡 `ping3` 라이브러리를 사용한 네트워크 핑 확인기")
    st.markdown("---")

    # 1. 사이드바에 로컬 IP 정보 표시
    local_ip = get_local_ip()
    st.sidebar.info(f"💡 현재 로컬 IP: **{local_ip}**")

    # 2. 사용자 입력 및 설정
    target_host = st.text_input(
        "핑을 확인할 호스트 이름 또는 IP 주소를 입력하세요:",
        value="8.8.8.8"
    )

    ping_count = st.slider(
        "핑 테스트 횟수 선택:",
        min_value=1, 
        max_value=10, 
        value=5
    )
    
    # 3. 실행 버튼
    if st.button("핑 테스트 실행", type="primary"):
        if not target_host:
            st.error("호스트 주소를 입력해주세요.")
            return

        st.markdown("### 📋 핑 테스트 진행")
        
        # 4. 핑 테스트 실행
        results = run_ping3(target_host, count=ping_count)

        # 5. 최종 결과 분석 및 출력
        st.markdown("### 📊 최종 결과 요약")
        
        if not results:
            st.error(f"**{target_host}**로의 모든 핑 시도가 실패했습니다.")
        else:
            success_count = len(results)
            loss_count = ping_count - success_count
            loss_rate = (loss_count / ping_count) * 100
            
            # 통계 계산
            min_rtt = min(results)
            max_rtt = max(results)
            avg_rtt = sum(results) / success_count
            
            st.success(f"✅ **{target_host}** 테스트 완료!")
            st.metric(
                label="패킷 손실률",
                value=f"{loss_count}/{ping_count} ({loss_rate:.1f}%)",
                delta=f"-{success_count} 성공"
            )

            col1, col2, col3 = st.columns(3)
            col1.metric("최소 응답 시간 (Min RTT)", f"{min_rtt:.2f} ms")
            col2.metric("최대 응답 시간 (Max RTT)", f"{max_rtt:.2f} ms")
            col3.metric("평균 응답 시간 (Avg RTT)", f"{avg_rtt:.2f} ms")


if __name__ == "__main__":
    main()