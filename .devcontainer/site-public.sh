#!/usr/bin/env bash
# Run by postAttachCommand (devcontainer.json).
#
# Serves ONLY the site/ folder on port 8000 and makes port 8000 public, so an
# agent-built page is live at https://<codespace>-8000.app.github.dev with no
# clicks. The server's --directory is site/, never the repository root: a server
# started in the root would also publish mine/ (your own documents).
#
# If your GitHub organization does not allow public ports, the port stays
# private: the site then opens only for you, from the Ports tab.
#
# Never fails the attach: every problem is logged to ~/.agentic-classroom-site.log.

root="$(cd "$(dirname "$0")/.." && pwd)"
site="$root/site"
log="$HOME/.agentic-classroom-site.log"
say() { printf '%s %s\n' "$(date -u +%H:%M:%S)" "$*" >>"$log"; }

mkdir -p "$site"
if [ ! -e "$site/index.html" ]; then
  cat >"$site/index.html" <<'EOF'
<!doctype html>
<meta charset="utf-8">
<title>Your site</title>
<!-- This folder is PUBLIC on the internet while the Codespace runs, and it is
     already being served. Do not start a web server. Never put keys, tokens,
     student data or anything private here.
     Check with: python3 .devcontainer/site-check.py -->
<h1>Your site will appear here</h1>
<p>Ask the agent to build files in the site/ folder, then refresh this page.</p>
EOF
fi

if ! curl -s -o /dev/null --max-time 2 http://127.0.0.1:8000/; then
  setsid nohup python3 -m http.server 8000 --bind 0.0.0.0 --directory "$site" \
    >>"$log" 2>&1 </dev/null &
  say "server started for $site"
fi
for i in $(seq 1 20); do
  curl -s -o /dev/null --max-time 2 http://127.0.0.1:8000/ && break
  sleep 0.5
done

if [ -z "${CODESPACE_NAME:-}" ]; then
  say "not a Codespace; left private"
  exit 0
fi
if ! command -v gh >/dev/null 2>&1; then
  say "gh not installed; left private"
  exit 0
fi

# The port is registered a moment after the server starts; retry for ~1 min.
for i in $(seq 1 12); do
  if gh codespace ports visibility 8000:public -c "$CODESPACE_NAME" >>"$log" 2>&1; then
    url="https://$CODESPACE_NAME-8000.${GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN:-app.github.dev}"
    printf '%s\n' "$url" >"$HOME/.agentic-classroom-site-url"
    say "public: $url"
    exit 0
  fi
  say "visibility attempt $i failed"
  sleep 5
done
say "could not make port 8000 public"
exit 0
