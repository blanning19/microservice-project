#!/usr/bin/env bash
set -euo pipefail

# Start SSH
/usr/sbin/sshd

# Start your app if provided; otherwise keep container alive
if [[ -n "${APP_CMD:-}" ]]; then
  echo "Starting app: ${APP_CMD}"
  exec bash -lc "$APP_CMD"
else
  echo "No APP_CMD set. SSH is up; container will stay running."
  exec tail -f /dev/null
fi