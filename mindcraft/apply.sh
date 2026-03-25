#!/usr/bin/env bash
set -euo pipefail

DIR="$(cd "$(dirname "$0")" && pwd)"
OVERLAY="$DIR/overlay"
TARGET="$DIR/repo"

if [ ! -d "$OVERLAY" ]; then
  echo "Error: overlay/ not found" >&2
  exit 1
fi

# Initialize submodule if needed
if [ ! -f "$TARGET/.git" ] && [ ! -d "$TARGET/.git" ]; then
  echo "Initializing mindcraft submodule..."
  git -C "$DIR/.." submodule update --init mindcraft/repo
fi

echo "Copying overlay into repo/..."
cp -r "$OVERLAY"/* "$TARGET/"
# Copy dotfiles individually (glob .* matches . and .., so avoid it)
for f in "$OVERLAY"/.[!.]*; do
  [ -e "$f" ] && cp -r "$f" "$TARGET/"
done

echo ""
echo "Done. Next steps:"
echo "  cd mindcraft/repo"
echo "  ast configure       # set BOT_NAME, ANTHROPIC_API_KEY, etc."
echo "  ast dev             # start the bot — mindserver UI at http://localhost:8080"
