#!/bin/bash

echo "=========================================="
echo "WASKO Health AI Model Downloader"
echo "=========================================="

mkdir -p models

MODEL="models/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf"

if [ -f "$MODEL" ]; then
    echo ""
    echo "TinyLlama model already exists."
    echo "$MODEL"
    exit 0
fi

echo ""
echo "Downloading TinyLlama..."

curl -L \
https://huggingface.co/TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF/resolve/main/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf \
-o "$MODEL"

if [ $? -eq 0 ]; then
    echo ""
    echo "Download completed successfully."
else
    echo ""
    echo "Download failed."
    exit 1
fi
