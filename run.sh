#!/usr/bin/env sh
set -e
set -a
source .env
set +a

# use cloudflare gateway root cert
CERT_PATH="./cert.pem"
if [ -f "$CERT_PATH" ]; then
  export REQUESTS_CA_BUNDLE="$CERT_PATH"
  export CF_CA_BUNDLE="$CERT_PATH"
  export SSL_CERT_FILE="$CERT_PATH"
  export CURL_CA_BUNDLE="$CERT_PATH"
	echo "Using CA bundle at $CERT_PATH for SSL verification"
else
  echo "Warning: CA bundle not found at $CERT_PATH — SSL verification may fail"
fi

.venv/bin/python3 run.py
