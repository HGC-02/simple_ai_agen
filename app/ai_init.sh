#only need to use at first

mkdir -p ai_notes ai_calendar

echo "need to install ollama for you? y/n:"

read ans

if [ "$ans" -eq "y" ]; then
    curl -fsSL https://ollama.com/install.sh | sh
elif [ "$ans" -eq "Y" ]; then
    curl -fsSL https://ollama.com/install.sh | sh
else
    echo"ok"
fi 

echo "need to install py requests for you? y/n:"

read ans

if [ "$ans" -eq "y" ]; then
    python -m pip install requests
elif [ "$ans" -eq "Y" ]; then
    python -m pip install requests
else
    echo"ok"
fi 


