#!/bin/bash
cd /home/kali/projects/sabio
source bin/activate &>/dev/null
if [[ $1 == "voz" ]]; then
  python coquiTTS.py 
elif [[ $1 == "chat" ]]; then
  python rastreador.py
elif [[ $1 == "token" ]]; then
  echo $2 > "./api_token.txt"
fi
