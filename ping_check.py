import streamlit as st
from ping3 import ping
import pandas as pd
import time

st.title("웹 Ping 확인 프로그램")

host = st.text_input("Ping 할 호스트 입력", "google.com")
count = st.number_input("Ping 횟수", min_value=1, max_value=10, value=4)

if st.button("Ping 실행"):
    results = []
    for i in range(int(count)):
        try:
            latency = ping(host, unit='ms')  # ms 단위 반환
            if latency is None:
                st.write(f"{i+1}번째 ping 실패")
            else:
                st.write(f"{i+1}번째 ping: {latency:.2f} ms")
                results.append(latency)
        except Exception as e:
            st.write(f"{i+1}번째 ping 실패: {e}")
        time.sleep(1)
    
    if results:
        df = pd.DataFrame(results, columns=["Latency (ms)"])
        st.line_chart(df)

