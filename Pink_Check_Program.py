import socket
import ping3
import pandas as pd              
import plotly.express as px      
import time
import sys

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


def plotly_ping_and_graph(host, count=15):
    
    data_list = [] 
    
    # 'use_global_sock' 옵션을 완전히 제거 - 고려사항
    ping_options = {'timeout': 2} 
    
    print(f"\n[{host}] (로컬 디바이스)에 핑 테스트를 {count}회 시도합니다...")
    
    for i in range(1, count + 1):
        delay = ping3.ping(host, **ping_options) 
        
        status_text = f"시도 {i}/{count}: "
        
        if isinstance(delay, float):
            rtt_ms = delay * 1000 
            
            data_list.append({'시도 횟수': i, '지연 시간 (ms)': rtt_ms, '성공 여부': '성공'})
            print(status_text + f"응답 성공! RTT: {rtt_ms:.5f} ms")
        else:
            fail_reason = "타임아웃" if delay is None else "응답 실패"
            data_list.append({'시도 횟수': i, '지연 시간 (ms)': None, '성공 여부': fail_reason})
            
            if delay == "NeedRootPrivilege":
                print(f"\n\n❌ 치명적 오류: {fail_reason} - Raw Socket 권한이 필요합니다. 'ping3'를 최신 버전으로 업데이트하거나, 시스템 관리자에게 문의해야 합니다.")
                return False
            print(status_text + f"{fail_reason}")
        
        time.sleep(0.5) 
        
    df = pd.DataFrame(data_list)
    successful_pings = df[df['성공 여부'] == '성공']['지연 시간 (ms)']
    
    if successful_pings.empty:
        print(f"\n❌ [{host}] 모든 핑 시도 실패.")
        return False

    avg_rtt = successful_pings.mean()
    
    fig = px.line(
        df.dropna(subset=['지연 시간 (ms)']), 
        x='시도 횟수', 
        y='지연 시간 (ms)', 
        title=f"로컬 디바이스 Ping 지연 시간 분석: {host}",
        markers=True, 
        color_discrete_sequence=['#1E90FF'] 
    )

    
    fig.update_layout(
        xaxis=dict(tickmode='linear', dtick=1, range=[0.5, count + 0.5]),
        yaxis_title="지연 시간 (ms)",
        hovermode="x unified",
        template="plotly_dark",
        
        
        title={
            'text': f"로컬 디바이스 Ping 지연 시간 분석: {host}", 
            'y': 0.95, # Y 위치 (0.95는 상단에 가깝게)
            'x': 0.5, # X 위치 (0.5는 중앙)
            'xanchor': 'center', # 텍스트의 앵커 포인트를 중앙으로 설정
            'yanchor': 'top', # 텍스트의 앵커 포인트를 상단으로 설정
            'font': {
                'size': 24, # 💡 크기를 살짝 키움 (기본값보다 크게)
                # 'family': 'Courier New, monospace', # 💡 글꼴 변경 시도 (CSS 호환 폰트만 가능)
                'color': 'white'
            }
        },
        
        font={
            'family': 'Arial, sans-serif', # Plotly에서 안정적인 sans-serif 계열 사용
            'color': 'white'
        }
    )

    fig.update_traces(
        hovertemplate="시도: %{x}<br>지연 시간: %{y:.5f} ms<extra></extra>",
        line=dict(shape='spline', smoothing=1) # 'spline'으로 부드러운 곡선, smoothing 값으로 곡률 조절
    )

    fig.add_hline(
        y=avg_rtt, 
        line_dash="dash", 
        line_color="#FF4500", 
        annotation_text=f"평균 RTT: {avg_rtt:.5f} ms", 
        annotation_position="top right"
    )

    # 💡 업데이트 사항 2: 배경을 어둡게 (dark template)
    fig.update_layout(
        xaxis=dict(tickmode='linear', dtick=1, range=[0.5, count + 0.5]),
        yaxis_title="지연 시간 (ms)",
        hovermode="x unified",
        template="plotly_dark", # 'plotly_dark' 템플릿 사용
        # 배경색을 더 어둡게 하고 싶다면 paper_bgcolor, plot_bgcolor 설정 가능
        # paper_bgcolor='rgba(0,0,0,1)',  # 전체 배경색
        # plot_bgcolor='rgba(0,0,0,1)'   # 그래프 영역 배경색
    )
    
    fig.show()

    return True

# --- 프로그램 실행 부분 ---
if __name__ == "__main__":
    
    local_ip_address = get_local_ip()
    
    print("--- 로컬 디바이스 정보 ---")
    print(f"자동 감지된 로컬 IP 주소: **{local_ip_address}**")
    print("----------------------------\n")
    
    plotly_ping_and_graph(local_ip_address, count=15)