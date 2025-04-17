#!/bin/bash
mkdir -p .streamlit
echo "[general]" > .streamlit/secrets.toml
echo "OPENAI_API_KEY = \"$OPENAI_API_KEY\"" >> .streamlit/secrets.toml
