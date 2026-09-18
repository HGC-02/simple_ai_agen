output=$(python3 -c "import sys; sys.path.append('..');import setting_funtion as i; print(i.web.port("port_listen"))")

echo "Captured: $output"

#python -m http.server "$PORT"
