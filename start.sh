#!/bin/bash
# Script de inicialização para VPS
source production.env
streamlit run main.py --server.port $STREAMLIT_SERVER_PORT --server.address $STREAMLIT_SERVER_ADDRESS
