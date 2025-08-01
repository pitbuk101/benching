#!/bin/sh

# # Check if force_deploy.py exists
# if [ ! -f /app/src/force_deploy.py ]; then
#   echo "Error: /app/src/force_deploy.py not found!" >&2
#   exit 1
# fi

# python /app/src/force_deploy.py
# if [ $? -ne 0 ]; then
#   echo "Error: force_deploy.py failed to execute successfully!" >&2
#   exit 1
# fi

# Check if __main__.py exists
if [ ! -f src/__main__.py ]; then
  echo "Error: /app/src/__main__.py not found!" >&2
  exit 1
fi
uvicorn src.__main__:app --host 0.0.0.0 --port 8009

if [ $? -ne 0 ]; then
  echo "Error: uvicorn failed to start!" >&2
  exit 1
fi
