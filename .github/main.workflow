workflow "on pull request merge, delete the branch" {
  on = "pull_request"
  resolves = ["branch cleanup"]
}

action "branch cleanup" {
  uses = "jessfraz/branch-cleanup-action@master"
  secrets = ["GITHUB_TOKEN"]
}

workflow "on pull request pass, merge the branch" {
  resolves = ["Auto-merge pull requests"]
  on = "check_run"
}

action "Auto-merge pull requests" {
  uses = "./.github/auto_merge_branch"
  secrets = ["GITHUB_TOKEN"]
}
