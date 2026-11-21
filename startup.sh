#!/usr/bin/env bash
set -e
exec python -m streamlit run app.py --server.address 0.0.0.0 --server.port 8000 --server.headless true
