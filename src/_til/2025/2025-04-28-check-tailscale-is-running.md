---
layout: til
title: How to check if Tailscale is running
summary:
  Use `tailscale status` and look for the `BackendState` key.
date: 2025-04-28 11:38:50 +0100
tags:
  - tailscale
---
I have some scripts that talk to nodes in my Tailscale network, but they can only connect if Tailscale is running on my Mac.
I wanted a way for my scripts to check if Tailscale is running, and prompt me to start it if not.

You can get the state of Tailscale using the CLI, for example:

```console
$ /Applications/Tailscale.app/Contents/MacOS/Tailscale status --json
{
  "Version": "1.82.5-tdec88625e-gec2eb9730",
  "TUN": true,
  "BackendState": "Running",
  …
}
```

The `BackendState` key can return [seven different states](https://github.com/tailscale/tailscale/blob/189e03e741acfcd3476343bf01a9fd8c02f3760d/ipn/backend.go#L24-L32), but in practice I only ever see `Running` and `Stopped`.

By inspecting this value, I can check whether Tailscale is running.

## A wrapper script

I've wrapped this in a script `ensure_tailscale_running.sh` which I can call from my other scripts, and will exit with a non-zero error code if Tailscale isn't running.

Because I write all my scripts with `set -o errexit`, this means the other scripts will fail if I'm not connected to Tailscale.

```bash
#!/usr/bin/env bash
# Check if Tailscale is running, and prompt you to start it if not.

set -o errexit
set -o nounset



# Print a message in blue to stdout
print_info() {
    echo -e "\033[34m$1\033[0m"
}

# Print an error in red to stderr
print_error() {
    echo -e "\033[31m$1\033[0m" >&2
}

# Print a warning in yellow to stdout
print_warning() {
    echo -e "\033[33m$1\033[0m"
}



print_info "Checking if Tailscale is running…"

# Call the Tailscale CLI to check if Tailscale is running
#
# This usually returns one of two statuses: "Stopped" or "Running"
backend_state=$(
  /Applications/Tailscale.app/Contents/MacOS/Tailscale status --json \
    | jq -r .BackendState
)

if [[ "$backend_state" = "Running" ]]
then
  print_info "Tailscale is running!"
  exit 0
elif [[ "$backend_state" = "Stopped" ]]
then
  print_error "You need to start Tailscale!"
  exit 1
else
  print_warning "Unexpected BackendState from Tailscale CLI: $backend_state"
  exit 2
fi
```
