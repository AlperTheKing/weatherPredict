#!/usr/bin/env zsh
set -euo pipefail

REPO_ROOT="/Users/alper/Projects/weatherPredict"
LABEL="com.alper.weatherpredict.cankaya"
SOURCE_PLIST="$REPO_ROOT/automation/$LABEL.plist"
TARGET_PLIST="$HOME/Library/LaunchAgents/$LABEL.plist"
DOMAIN="gui/$(id -u)"

mkdir -p "$REPO_ROOT/reports/automation/logs"
mkdir -p "$HOME/Library/LaunchAgents"
cp "$SOURCE_PLIST" "$TARGET_PLIST"

launchctl bootout "$DOMAIN" "$TARGET_PLIST" >/dev/null 2>&1 || true
launchctl bootstrap "$DOMAIN" "$TARGET_PLIST"
launchctl kickstart -k "$DOMAIN/$LABEL"
launchctl print "$DOMAIN/$LABEL"
