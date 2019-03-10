workflow "merge_and_cleanup" {
  resolves = ["When tests pass, merge and cleanup"]
  on = "check_run"
}

action "When tests pass, merge and cleanup" {
  uses = "./.github/auto_merge_branch"
  secrets = ["GITHUB_TOKEN"]
}
