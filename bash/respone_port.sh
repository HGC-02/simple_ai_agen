cd ..
PORT=$(jq -r '.[] | select(.id == "2") | .settings.port_for_tell' file.json)
cd bash
PORT=(20000)
python -m http.server "$PORT"
