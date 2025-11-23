import streamlit as st
import subprocess
import pandas as pd
import time

st.title("간단 Ping 확인 프로그램")

host = st.text_input("Ping 할 호스트 입력", "google.com")
count = st.number_input("Ping 횟수", min_value=1, max_value=10, value=4)

if st.button("Ping 실행"):
    results = []
    for i in range(int(count)):
        try:
            output = subprocess.check_output(
                ["ping", "-c", "1", host],  # Windows는 "-n", Linux/Mac "-c"
                universal_newlines=True
            )
            # 출력에서 시간 추출
            latency = float(output.split("time=")[1].split(" ms")[0])
            results.append(latency)
            st.write(f"{i+1}번째 ping: {latency} ms")
        except Exception as e:
            st.write(f"{i+1}번째 ping 실패: {e}")
        time.sleep(1)

    if results:
        df = pd.DataFrame(results, columns=["Latency (ms)"])
        st.line_chart(df)
