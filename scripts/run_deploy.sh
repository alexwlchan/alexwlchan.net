#!/usr/bin/env bash
# run_deploy.sh is a script that be run any time you want to kick off
# a deployment of the website.
#
# It deliberately doesn't print much and instead directs output to a file
# which can be inspected later.

set -o errexit
set -o nounset

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
cd "$SCRIPT_DIR/.."

source .venv/bin/activate

NOW=$(date +'%Y-%m-%dT%H-%M-%S')
LOG_NAME="deploy.$NOW.log"
LOG_PATH="$TMPDIR/$LOG_NAME"

echo "Deploying alexwlchan.net..."
echo "Follow logs: tail -f \$TMPDIR/$LOG_NAME"

if bash "$SCRIPT_DIR/deploy.sh" > $LOG_PATH 2>&1; then
  print_success "Deployment succeeded!"
else
  print_error "Deployment failed failed!"
  cp "$LOG_PATH" ~/Desktop/alexwlchan.net.deploy.$NOW.failed.log
  print_error "See logs: cat ~/Desktop/alexwlchan.net.deploy.$NOW.failed.log"
  exit 1
fi
