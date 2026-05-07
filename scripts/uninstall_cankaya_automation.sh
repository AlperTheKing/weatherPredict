#!/usr/bin/env zsh
set -euo pipefail

LABEL="com.alper.weatherpredict.cankaya"
TARGET_PLIST="$HOME/Library/LaunchAgents/$LABEL.plist"
DOMAIN="gui/$(id -u)"

launchctl bootout "$DOMAIN" "$TARGET_PLIST" >/dev/null 2>&1 || true
rm -f "$TARGET_PLIST"
