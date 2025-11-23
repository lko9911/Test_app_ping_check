import subprocess
import platform
import socket

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


def ping_host(host, count=4):
    """
    지정된 호스트로 핑을 보내고 결과를 반환합니다. (이전 코드와 동일)
    """
    current_os = platform.system().lower()

    if current_os == "windows":
        command = ['ping', '-n', str(count), host]
    else:
        command = ['ping', '-c', str(count), host]

    print(f"[{host}]에 핑 시도 중...")

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=10,
            check=False
        )
    except Exception as e:
        print(f"오류 발생: {e}")
        return False

    if result.returncode == 0:
        print(f"✅ [{host}] 핑 성공! (응답 있음)")
        return True
    else:
        print(f"❌ [{host}] 핑 실패. (응답 없음 또는 호스트를 찾을 수 없음)")
        return False

# --- 프로그램 실행 부분 ---
if __name__ == "__main__":
    # 1. 로컬 IP 주소 자동 가져오기
    local_ip_address = get_local_ip()
    
    print("--- 로컬 디바이스 정보 ---")
    print(f"현재 운영체제: {platform.system()}")
    print(f"자동 감지된 로컬 IP 주소: **{local_ip_address}**")
    print("----------------------------\n")
    
    if local_ip_address == "127.0.0.1":
        print("경고: 네트워크 연결이 없거나 IP를 찾을 수 없어 루프백 주소(127.0.0.1)를 사용합니다.")
    
    # 2. 로컬 IP 주소로 핑 테스트 실행
    # 로컬 IP에 핑을 보내는 것은 일반적으로 항상 성공합니다.
    # 이는 시스템이 자체적으로 응답하기 때문입니다.
    ping_success = ping_host(local_ip_address, count=2)
    
    print(f"\n최종 결과: {'성공' if ping_success else '실패'}")