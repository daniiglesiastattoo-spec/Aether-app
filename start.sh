#!/bin/bash
echo "Arrancando AETHER..."
pkill -f llama-server 2>/dev/null
pkill -f aether_final 2>/dev/null
sleep 2
~/bin/llama-server -m ~/models/phi3-mini.gguf --threads 2 --ctx-size 1024 --port 8080 --log-disable &
echo "Esperando modelo..."
sleep 35
echo "Arrancando interfaz..."
python ~/aether/aether_stream.py
