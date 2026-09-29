sudo apt update
sudo apt install -y curl
curl -fsSL https://ollama.com/install.sh | sh
sudo systemctl enable --now ollama
ollama run 

