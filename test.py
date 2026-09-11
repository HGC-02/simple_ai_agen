import setting_funtion as v
s=v.chat
st=v.web
print(s.model_name())
print(s.url_api())
print(st.ip())
print(st.port("port_web"))
print(st.port(1))
print(st.port(2))