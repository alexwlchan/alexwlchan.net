workflow "merge_and_cleanup" {
  resolves = ["On PR pass, merge and cleanup"]
  on = "check_run"
}

action "On PR pass, merge and cleanup" {
  uses = "./.github/auto_merge_branch"
  secrets = ["GITHUB_TOKEN"]
}
