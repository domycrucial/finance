#!/usr/bin/env bash
set -euo pipefail

SCOPE="${1:-workspace}"
WORKSPACE_PATH="${2:-$(pwd)}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SOURCE_SKILLS="$SCRIPT_DIR/.agents/skills"

if [ "$SCOPE" = "global" ] || [ "$SCOPE" = "--global" ]; then
  TARGET_DIR="$HOME/.gemini/config/skills"
else
  TARGET_DIR="$WORKSPACE_PATH/.agents/skills"
fi

mkdir -p "$TARGET_DIR"
for skill in "$SOURCE_SKILLS"/*/; do
  name="$(basename "$skill")"
  rm -rf "$TARGET_DIR/$name"
  cp -R "$skill" "$TARGET_DIR/$name"
  echo "Installed skill: $name -> $TARGET_DIR/$name"
done

echo "Done! Verify with: python3 scripts/validate-skills.py "$TARGET_DIR""
