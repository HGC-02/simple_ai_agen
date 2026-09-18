name=$(python3 -c "import json; print(json.load(open('../setting.json'))[1][settings])")

echo "$name"
#python -m http.server "$PORT"
