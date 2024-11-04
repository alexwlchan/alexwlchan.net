---
layout: page
title: Changelog
---

## October 2024

*   I moved the site from being hosted on Netlify, to being hosted on a Linux VPS using Caddy.
    I wrote [an article](/2024/netlify-to-caddy/) explaining the motivation behind this change.
*   Don't show the background texture when you print the page.

## September 2024

September-ish: redesign TIL, articles

*   Make sure Python console sessions get syntax highlighting in TIL post.

## August 2024

*   Remove Twitter from my contact page.
*   Fix an invalid value in my [`X-Frame-Options` header](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Frame-Options).
    I was returning `ALLOW`, but I should have been returning `ALLOWALL`.

## June 2024

*   Add syntax highlighting [for Python console sessions](/til/2024/how-to-highlight-python-console-in-jekyll/).
*   Add a `utm_source` parameter to links in the RSS feed, so I can track how many people are reading via RSS.
*   Allow serving the site in an `<iframe>` by changing the X-Frame-Options header from `DENY` to `ALLOW`.
*   De-duplicate styles for inline SVGs, to reduce page weight.
*   Fix a bug where embedded YouTube videos were appearing too wide on mobile devices.
*   Fix a bug where inline SVGs had empty `<defs>` tags.
*   Remove all uses of `polyfill.io` because of a supply chain attack, and serve the JavaScript directly from this domain only. (This only affected a single page.)

April 2013:

*   f5f96e9db17d277e7ee52b6865c1d37b53fa57e8 / switch the defualt font from Georgia to Charter

{% raw %}
---

commit 0e1d1c0b9881e3b67ea2cce4885e1c7ec07558e8
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Apr 11 18:41:06 2024 +0100

    Add a new TIL: "How to embed an inline SVG in a CSS rule"

commit fc55e0d5ea9b3fcd246c12a2c24c91209dc885f7
Merge: 28eac86e 539aa0c7
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Apr 11 18:41:40 2024 +0100

    Merge pull request #782 from alexwlchan/no-install-in-plugin-tests

    Maybe I can use Nokogiri from Bundler?

commit 539aa0c7962f32f0af2ed6853e208a187ab3a34a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Apr 11 10:39:05 2024 +0100

    Plugin tests YAML needs to run the plugin tests!

commit ce7d9af0d47c122fd24f52b5208691dace80b880
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Apr 11 10:34:37 2024 +0100

    Maybe I can use Nokogiri from Bundler?

commit 28eac86eb16bc24cab6c184c6186be25d82788b3
Merge: e1464921 6fe4a681
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Apr 11 04:12:14 2024 +0100

    Merge pull request #781 from alexwlchan/put-more-gems-in-bundle

    What if I rely on Nokogiri from Bundler?

commit 6fe4a681a62e01b039891bb27d109e661ca364ca
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Apr 11 04:07:25 2024 +0100

    Can I get html-proofer from bundle also?

commit 20e5a5f576956f7afc63b280edcf587077899c07
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Apr 11 04:03:09 2024 +0100

    Can I get json-schema from bundle also?

commit c4c87796acb19a81758c3fa4e990fcebc9154e29
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Apr 11 03:59:27 2024 +0100

    What if I rely on Nokogiri from Bundler?





commit 09d74ec2991f50576a6827bd4884cd7904837cc1
Author: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>
Date:   Thu Apr 11 01:21:16 2024 +0000

    Bump nokogiri from 1.16.3 to 1.16.4

    Bumps [nokogiri](https://github.com/sparklemotion/nokogiri) from 1.16.3 to 1.16.4.
    - [Release notes](https://github.com/sparklemotion/nokogiri/releases)
    - [Changelog](https://github.com/sparklemotion/nokogiri/blob/main/CHANGELOG.md)
    - [Commits](https://github.com/sparklemotion/nokogiri/compare/v1.16.3...v1.16.4)

    ---
    updated-dependencies:
    - dependency-name: nokogiri
      dependency-type: direct:development
      update-type: version-update:semver-patch
    ...

    Signed-off-by: dependabot[bot] <support@github.com>

commit 76b0b8722f1a71098a67ad01f050a3ecf1ce3e99
Author: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>
Date:   Thu Apr 11 01:20:56 2024 +0000

    Bump rubocop from 1.63.0 to 1.63.1

    Bumps [rubocop](https://github.com/rubocop/rubocop) from 1.63.0 to 1.63.1.
    - [Release notes](https://github.com/rubocop/rubocop/releases)
    - [Changelog](https://github.com/rubocop/rubocop/blob/master/CHANGELOG.md)
    - [Commits](https://github.com/rubocop/rubocop/compare/v1.63.0...v1.63.1)

    ---
    updated-dependencies:
    - dependency-name: rubocop
      dependency-type: direct:development
      update-type: version-update:semver-patch
    ...

    Signed-off-by: dependabot[bot] <support@github.com>

commit 18b10e653814721d9724375d5a789b0dd5d661eb
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Apr 10 23:53:55 2024 +0100

    Log the name of the bad colour profile

    [skip ci]

commit a8ced4ae2990df2fe02bd07b5dfbb7dda045086f
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Apr 10 23:52:48 2024 +0100

    Add a missing f-string prefix

commit 727c47b9827a500c0c5c8dad8ecbc4367aad9bd6
Merge: 8a7de012 a5822f63
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Apr 9 08:59:17 2024 +0100

    Merge pull request #777 from alexwlchan/dependabot/bundler/rubocop-1.63.0

    Rejig a bunch of the Ruby handling in CI [Was: Bump rubocop from 1.62.1 to 1.63.0]

commit a5822f633f4c1467e99331726e25115357c44b2f
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Apr 9 08:49:47 2024 +0100

    Fix two issues flagged by the newest RuboCop

commit 2f9a3676144132be1999f576d3a473c8927b319a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Apr 9 08:49:40 2024 +0100

    Maybe I don't need these gems after all?

commit 371ee15e1bb8cf49055f26ff7c054087746b0157
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Apr 9 08:47:52 2024 +0100

    Add the `.bundle` file to `.gitignore`

commit 842b043a09c8c8232ae583d8ddeaeefa9da8a6c4
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Apr 9 08:47:19 2024 +0100

    Actually run RuboCop

commit 2c027c5fa0ffd2e05112de4a03312d1ba1a6f712
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Apr 9 08:44:34 2024 +0100

    Try rejigging this bit of RuboCop config

commit a755fba626068f2199d54ba185131e772474eb65
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Apr 9 08:43:58 2024 +0100

    What is RuboCop trying to lint?

commit 3ec436fcaa9b6ddcba0c47588395c9071a671214
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Apr 9 08:33:58 2024 +0100

    Try to avoid RuboCop taking forever in GitHub Actions

commit d622ea27791fa233afc3e8589d2f6036471c9a96
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Apr 9 08:31:55 2024 +0100

    Don't bother running the 'merge PR' workflow if it won't merge

commit fef7202726b4c5c4bbd599a80a7763d125392bf7
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Apr 9 08:19:52 2024 +0100

    Continue rejigging the lock files

commit 065f94dfd7ea3ce4c148e51976b4080b55a1b3e7
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Apr 9 08:12:39 2024 +0100

    Continue fiddling with GitHub Actions

commit f8a81cf2d85ba85152d20f34663d8b2ab14e9f25
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Apr 9 08:07:47 2024 +0100

    Try installing all the dependencies

commit e90e0e1616204bf666dafa2f080c77b19a1356e9
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Apr 9 08:02:30 2024 +0100

    Add the missing dependency; add Gemfile groups

commit 2fcf321be3266a1e953bd35eb250ecaa4152113c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Apr 9 07:54:47 2024 +0100

    Plugin tests should also run for Gemfile changes

commit d750a3be6469aca4c4f1c7050ffbf81c202a5af5
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Apr 9 07:54:24 2024 +0100

    Trigger the RuboCop workflow on more changes

commit 499b20f31e20ce9da710f26fd8bfe1e13bc5448a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Apr 9 07:51:36 2024 +0100

    Try installing rubocop from bundler

commit e06757db0e5f01c9eef25d118583af498e23782e
Author: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>
Date:   Tue Apr 9 01:19:59 2024 +0000

    Bump rubocop from 1.62.1 to 1.63.0

    Bumps [rubocop](https://github.com/rubocop/rubocop) from 1.62.1 to 1.63.0.
    - [Release notes](https://github.com/rubocop/rubocop/releases)
    - [Changelog](https://github.com/rubocop/rubocop/blob/master/CHANGELOG.md)
    - [Commits](https://github.com/rubocop/rubocop/compare/v1.62.1...v1.63.0)

    ---
    updated-dependencies:
    - dependency-name: rubocop
      dependency-type: direct:production
      update-type: version-update:semver-minor
    ...

    Signed-off-by: dependabot[bot] <support@github.com>

commit 8a7de0126478858e2c9618e6996f17fbc8c65e30
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Apr 8 15:16:40 2024 +0100

    Add a couple of missing redirects

commit 48b4b5bc37c70692c68b1ea8e829c355cf68e2e0
Merge: 88b98f24 4af24ce7
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Apr 8 13:25:02 2024 +0100

    Merge pull request #776 from alexwlchan/port-all-tils

    Bring across all the existing TIL files

commit 4af24ce79cfa216d1df1fe4b92201bf64e4927bf
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Apr 8 13:19:50 2024 +0100

    Fix all the TIL-related stuff

commit 3aadea3722883b78e8faaedc9ffc7cc53f69add8
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Apr 8 13:05:04 2024 +0100

    FIx a bug where some list items were stacking horizontally

commit ead47d53a6f205f549019ff72dafd639e68efa90
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Apr 8 13:04:46 2024 +0100

    We don't need to repeat the path here

commit 2cb9468a01a4dd51b65c5f9a99f8f64969580e10
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Apr 8 13:04:34 2024 +0100

    Bring across all the TILs from the old repo

commit 88b98f24073969a9085632ff01a1547cefac0c1c
Merge: 0df0b67c 24b0c192
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Apr 8 09:09:51 2024 +0100

    Merge pull request #775 from alexwlchan/use-css-for-hr

    Push my custom <hr/> styles into custom CSS, out of Jekyll

commit 24b0c1921398f5ea7c746c91974d59d439f3cc8b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Apr 8 09:04:02 2024 +0100

    Also use CSS with an <hr> for the separator on the homepage

commit 92eb53f31740c5e0a3b8850efec0f478e1c55438
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Apr 8 07:59:37 2024 +0100

    Push my custom <hr/> styles into custom CSS, out of Jekyll

commit 0df0b67c957e02c0b38cadeb242e3be519fa69e9
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Apr 8 08:03:47 2024 +0100

    Fix a bug in this error message

commit 8e41ba045d03bd868758094c790e7a7a2878fe84
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Apr 8 01:49:55 2024 +0100

    tweak this line

commit 5964a7d5514923e30aebc8b1d018927df88dee98
Merge: f9b580e0 41999e61
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Apr 8 01:49:27 2024 +0100

    Merge pull request #774 from alexwlchan/remove-projects

    Remove the projects page; tighten up the homepage

commit 41999e6123360533d69e771f1958c0fe8bfab908
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Apr 8 01:40:32 2024 +0100

    Remove the projects page; tighten up the homepage

commit f9b580e01d9c99c192a5d9ee420819e883d731f2
Merge: 65de9a06 f533a876
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Apr 8 00:45:20 2024 +0100

    Merge pull request #771 from alexwlchan/shuffle-tils

    Shuffle a couple of old notes into the TIL section

commit f533a87630653df577a8190376a27c0006ee0407
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Apr 8 00:41:19 2024 +0100

    Fix some broken redirects

commit de65288b0c043cdb33ca5650b24ec9b9d8d3bd0e
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Apr 7 22:03:21 2024 +0100

    Shuffle a couple of old notes into the TIL section

commit 65de9a0607aabc711e592a9111f11c81f16d5980
Merge: 7cb0d5d8 9a456aa4
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Apr 8 00:33:24 2024 +0100

    Merge pull request #773 from alexwlchan/fix-jekyll-issues

    Fix a few lingering issues in the new Jekyll process

commit 9a456aa40ce90147d0b5920f0e3236ee896d5a00
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Apr 8 00:14:50 2024 +0100

    What if I run the linter through bundle?

commit 40bcd5a8b8f0c7142a28fb00606cb01eb93eae81
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Apr 8 00:03:13 2024 +0100

    Fix a few more issues detected running Jekyll on a new Mac

commit 7cb0d5d841b426a4abba426e5987423ae7888958
Merge: 795b97e2 57cd37ca
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Apr 8 00:27:45 2024 +0100

    Merge pull request #772 from alexwlchan/til-more-flexible

    Make the TIL templates a bit more flexible

commit 57cd37ca848dbda192160b219db66258e2c9a181
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Apr 7 22:03:21 2024 +0100

    Support TILs that don't have tags

commit 8147bb34fa57a81acbd81a3662df7e9cb5b8b5e4
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Apr 7 22:03:21 2024 +0100

    Remove the TIL: prefix from TIL titles

commit 1ccd8206b454c9d7d4e3c124fa987c87c0b5373c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Apr 7 22:03:21 2024 +0100

    Allow skipping the summary on TILs

commit 795b97e23e4e8cbc16ca4db13e9950fc31f136cb
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Apr 8 00:15:30 2024 +0100

    Fix the branch name in the README

commit 28b19bce6b07fb012c47e322937ae174c2924e3a
Merge: 112b4dc2 5845aada
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Apr 7 22:03:10 2024 +0100

    Merge pull request #770 from alexwlchan/remove-maths-page

    Remove the top-level /exams/ page; make it a hidden post

commit 5845aadafeddad363d1b22e344c8fdac495efc5d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Apr 7 21:57:16 2024 +0100

    Remove the top-level /exams/ page; make it a hidden post

commit 112b4dc27f33df8d2bd736017dca69735f6313b8
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Apr 7 21:47:31 2024 +0100

    Tidy up a few styles

commit 6171ebb7a51d91ad315a0d2b8554296fcb85ef5a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Apr 7 21:43:15 2024 +0100

    Remove an unnecessary console.log() debug statement

commit e169349510870d86b9eb22fb1dc3b5b55143a483
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Apr 7 21:42:46 2024 +0100

    Remove an unnecessary bit of config

commit 037712290b4934a566d7a2f2dd66274eac542d42
Merge: bcbb23c2 f17a2e4a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Apr 7 20:28:04 2024 +0100

    Merge pull request #769 from alexwlchan/bump-nokogiri

    Bump to the newest version of Nokogiri

commit f17a2e4a989edfd461d9bffd55936291af47499f
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Apr 7 20:18:29 2024 +0100

    Bump to the newest version of Nokogiri

commit bcbb23c21efe1f3e5bca39b8b81fa0ab2d73c7ed
Merge: e1bdeac8 7c0c1a1a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Apr 7 20:12:33 2024 +0100

    Merge pull request #767 from alexwlchan/faster-image-builds

    Speed up the initial build when the image cache is cold

commit 7c0c1a1abb4accde933695c9a3fc8f2c9e19156b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Apr 7 20:01:06 2024 +0100

    Speed up the initial build when the image cache is cold

    This takes the cold build from ~50s to ~7s.

commit e1bdeac83930fd35e46a4714e60bd99df089f1d9
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Apr 7 20:05:44 2024 +0100

    Add Dependabot alerts for Python

commit 827087e6c234744f48124c96d3e97b45a0196a59
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Apr 7 20:04:02 2024 +0100

    The article layout is gone; this rule is redundant

commit d6b6ed36f69fda61da722a0daa8ac3c9c09bcb8b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Apr 7 20:03:20 2024 +0100

    Create dependabot.yml

    For #759

commit e4ea3314c191a2849be4a2e9c765778416660b08
Merge: 3296de45 d33a3777
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Apr 7 19:53:48 2024 +0100

    Merge pull request #766 from alexwlchan/misc-changes

    A couple of stray tidy-up changes

commit 3296de451cf32385b1583a0766c254c864ee8699
Merge: a5376e20 b2611f93
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Apr 7 19:50:07 2024 +0100

    Merge pull request #765 from alexwlchan/posts-not-articles

    Use the posts collection, not articles

commit b2611f936c8b7fa618978c9ebaad162f2207f667
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Apr 7 19:45:46 2024 +0100

    Fix a couple of issues flagged by the linter

commit d33a3777d62067341f8eeab3fbb4d97a428f0083
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Apr 7 19:42:39 2024 +0100

    Add caching to another text processing filter

commit 0693b376aee2aa5b50a1124a4222069fb132bc48
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Apr 7 19:42:31 2024 +0100

    Remove the unused eggbox component

commit 3a03ed82f879db638f01221991a9d75566596cf7
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Apr 7 19:41:56 2024 +0100

    Add another section to my `_config.yml`

commit 1f6a3de1f198edba9543a5f1c79d5f890fa622a3
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Apr 7 19:40:17 2024 +0100

    Switch back to using the posts collection, not articles

commit 4cfacd67229a9a9c3fe13504d3676ab232900038
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Apr 7 19:34:05 2024 +0100

    Remove the articles collection from _config.yml

commit a5376e202bab4d022a5104032c36748fc4334de8
Merge: 51f33226 556e4701
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Apr 7 19:29:19 2024 +0100

    Merge pull request #760 from alexwlchan/run-in-macos-jekyll

    Allow running in macOS Ruby rather than Docker

commit 556e4701dc6db80e6fb01810bd384680c0054937
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Apr 7 19:22:16 2024 +0100

    Re-enable the "merge pull request" action

commit 057bf89de1ec9b5ffc173af6b5714b43c26c8193
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Apr 7 19:20:23 2024 +0100

    Tidy up a few things in the plugin tests GitHub Action

commit 6e8153c668d5da319ec466d01e216b3da202aa0e
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Apr 7 18:58:59 2024 +0100

    Re-enable RuboCop and plugin tests

commit 9e041f58f096d7cb3a38cab0ac5a4726585fb4aa
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Apr 7 18:58:37 2024 +0100

    Remove a bunch of references to Docker

commit 297b14ffda6bdb8cdbdbeae2578c0ff0f27574dc
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Apr 7 18:50:09 2024 +0100

    Also supply the publish-dir setting

commit af04a219bfe9231101c14069bffbd88acfa851c3
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Apr 7 18:45:54 2024 +0100

    Add my Netlify site ID

commit c86a2fdfdffbfd0d1e9bbff1f3b913c4559e3314
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Apr 7 18:41:37 2024 +0100

    Try deploying to Netlify from GitHub Actions

commit 046b0ae549c124829059449d16cbdbc1c7bc91eb
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Apr 7 18:35:25 2024 +0100

    Try installing HTML-Proofer manually

commit 71f9ebb5904019c7e209fdce8b1cc0a6dbf93576
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Apr 7 18:31:59 2024 +0100

    Maybe `bundle` will install HTML-Proofer now?

commit dfc516c85a066b1d76196006b133bd33219b9f99
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Apr 7 18:31:07 2024 +0100

    Upgrade to HTML-Proofer 5; fix linting issues

commit 6f4bcb0e8a00a3c6b167d1899a58b5c4c38cf7c8
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Apr 7 17:15:26 2024 +0100

    try swapping the installation order

commit 9812ff4aa5e29e68182a5bd4c794fdcfc3ec91e9
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Apr 7 17:13:55 2024 +0100

    Pin the version of html-proofer used in CI

commit c2faa3e7044d596019a3742bae965d47de67680f
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Apr 7 17:10:39 2024 +0100

    Remove more Docker-related commands

commit 2b79c4da70693ebe5984d0696ea99d30821d98fd
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Apr 7 17:10:17 2024 +0100

    Try installing json-schema manually also

commit fd56331e08d8a7f41b645d9f758bd2321b5a0688
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Apr 7 17:06:40 2024 +0100

    Switch back to Ubuntu latest

    The check out and cache actions are way slower on macOS!

commit 7457f0d2144d66d60020149f5532a7e95388f868
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Apr 7 17:02:50 2024 +0100

    Okay, let's actually build the site

commit b1626f73da4831bd6fba79bb0403ac436bfc566b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Apr 7 16:58:37 2024 +0100

    Okay, now let's get the plugin tests working

commit da73772ffb056fbb62499308817876bd2e73eb55
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Apr 7 16:57:24 2024 +0100

    Don't install rubocop with bundle

commit 2ad1d84d82d46fa92a3babb87329f0545b4f93eb
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Apr 7 16:56:13 2024 +0100

    Comment out the other CI runs for now

commit 428bf14580964b5ea2760fbe219e510f270466bf
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Apr 7 16:50:51 2024 +0100

    Remove some of the Docker pieces

commit 26a057f80ce2152f432dbf92ed04d022e008159a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Apr 7 16:50:29 2024 +0100

    Remove another now-unused .gitignore line

commit f09b360fc981304284b3ad2b5434e446545ee905
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Apr 7 16:49:45 2024 +0100

    Try installing these gems manually

commit 3195c359b9542c3f0eb1ca0e9a45550694f2ebf0
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Apr 7 16:49:29 2024 +0100

    Fix the plugin tests

commit 3faddc7eabd89a81a409a6337b79596e47686cc3
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Apr 7 16:46:01 2024 +0100

    Restore the RuboCop check

commit 1d6a3f0727d7745f1b379fcecdb569df27c24377
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Apr 7 16:40:45 2024 +0100

    Fix all the linting issues

commit 7a67dd2f2cda798d29eca371b74d153d1580ec5f
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Apr 7 16:25:33 2024 +0100

    Ignore .DS_Store when getting colour profiles

commit d390555d4e8bdf87a5d272f27a26b39bc3440c83
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Apr 7 16:24:44 2024 +0100

    Ignore a README that was throwing off the linter

commit 81303c17909caacc103773d403fc924095525159
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Apr 7 16:23:57 2024 +0100

    Make HTML-Proofer happy

commit 6dcc217cc0c90779c8f07d474401ac7688de84dd
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Apr 7 16:18:04 2024 +0100

    Continue fiddling with the macOS build

commit 74725587b5e7067647ad673cfcb48596f56b6796
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Apr 7 16:02:03 2024 +0100

    Try building the site in GitHub Actions

commit 9fccf5de5772e550111f01aacb31005204f5d2c5
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Apr 7 15:49:59 2024 +0100

    Fix the color profile tests by removing the exiftool dependency

commit 7aac7ac05897702cef86b8d7abad371700f0b80c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Apr 7 15:37:42 2024 +0100

    Install Nokogiri in a separate step

commit 889fbeb20cb54b8c2426e82f295e966e07063f69
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Apr 7 15:30:10 2024 +0100

    Let's get a new Gem cache

commit 7dfc8d710ab0915ac07a377a7c8dbea2f3478b5c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Apr 7 15:27:29 2024 +0100

    Try running on macOS, not Ubuntu

commit 7d4c7537af7c453dfc4b38e75f455582c80f905c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Apr 7 15:25:17 2024 +0100

    Is Nokogiri available at all in GitHub Actions?

commit e48e5d7ce66bf884c4b78dfc5b4cdc2353aff518
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Apr 7 14:15:57 2024 +0100

    Run the GitHub Actions tests in Ruby

commit 90627cba1d4ba911d4471d98f6a38bca736715f0
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Apr 7 14:10:49 2024 +0100

    Run RuboCop to format everything

commit eb44b7e66d8f340ea99821a29427a23280caee28
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Apr 7 14:04:20 2024 +0100

    Swap out for a cached filter for more speed

commit eb59959e604153767fccbe27ae487d9572dd1bfd
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Apr 7 14:03:31 2024 +0100

    Remove an unused CSS class

commit 3b39aba36482108a3e8c6077c01996f415de6542
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Apr 7 14:02:34 2024 +0100

    We can do away with the old Docker machinery

commit 0319b0d66a00a370ae9567325a2efdaa3488d08e
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Apr 7 14:01:53 2024 +0100

    Add another layer of caching, we can skip globbing

commit 363cea846f8a63ed633e9ae5fcc2d7cd1c105a3f
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Apr 7 14:00:42 2024 +0100

    Add caching to speed up getting image info

commit 815c81e898a93e2ab838c36b3fa876848f06f827
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Apr 7 13:57:07 2024 +0100

    Get the build working with Pillow

commit 3cd75612eabdb890cb6702bb95da3e99e1902f92
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Apr 7 13:50:21 2024 +0100

    Fiddle with scripts to get things working

commit b0876d57bbcb69f2f4de483c2248ed9d1077cbc9
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Apr 7 13:46:14 2024 +0100

    And convert a use of images in the twitter plugin

commit ad0f6102cf6b8a7c2fcbd8188ba2bc2bed9485f6
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Apr 7 13:38:35 2024 +0100

    Convert the picture tag to use Pillow

commit 5db99fb30137717e23a7dc9a295989e13f7ad796
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Apr 7 13:33:11 2024 +0100

    Remove 'rszr' from the linter script

commit 32e2f0c42f6b1cca1c7e7af23b415deda774ddac
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Apr 7 13:13:43 2024 +0100

    Replace rszr with my first Pillow script

commit 240c857b8b1a67cff05c5089d7a95baee046f130
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Apr 7 13:13:35 2024 +0100

    Remove rszr as a dependency

commit d59c57dbe5d6cfedee38509bd993223ab7182951
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Apr 7 12:55:08 2024 +0100

    Build a Docker image that includes Python

commit 51f33226eda8f4a62c6250e629ae7854c50fffab
Merge: 4e1c321f b681c39b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Apr 7 10:06:01 2024 +0100

    Merge pull request #758 from alexwlchan/create-articles-page

    Rejig the articles to make them easier to deal with

commit b681c39b92f0d016d801eef5556f486f3b3ba4d2
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Apr 7 09:59:49 2024 +0100

    Add featured articles to the articles page

commit 6db1cff69b2749e07499db1ea6322a743349fee8
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Apr 7 09:36:18 2024 +0100

    Fix a bug in the article code

commit e6a52b3a43358fbd41e44862a7ee510e643bfdd2
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Apr 7 09:29:11 2024 +0100

    Let's tighten up all the spaces around titles

commit 0df99e19bfa9203128368157f44796fa1e283872
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Apr 7 09:27:19 2024 +0100

    We don't need styles for excluded posts

commit 72a68d06f31cf5091055b133ec6bee3f6dace197
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Apr 7 09:25:32 2024 +0100

    We don't need the path prefix here

    This saves another ~10KB from the /articles/ page!

commit befb94455f41eb288a10c4a95234703d6399cdb3
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Apr 7 09:23:39 2024 +0100

    Card images don't need to be larger than 2x

commit 53fc1190303ead871454b7d2936cbfc2ce3155b5
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Apr 7 09:19:37 2024 +0100

    Continue to trim the size of the article cards

    Looking at /articles/ in particular:

    Before: 365,315 bytes
    After:  345,804 bytes

commit 1c6f38204ec2615a410ef99813ffde38413e87f2
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Apr 7 09:11:54 2024 +0100

    Tidy up a few more bits of CSS

commit e23770f59306ff458c0a9082b64a5067ea7d07d9
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Apr 7 09:06:28 2024 +0100

    Hide a couple more posts from the archives

commit 9ee95c025811118da2a0d0afb8fb252613837cbe
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Apr 7 09:01:43 2024 +0100

    We can consolidate these two styles

commit 3c4f32e038f39ff404d40f6b4e306e1c1a6e39e4
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Apr 7 09:01:37 2024 +0100

    We don't need to wrap this in a <p>

commit 2387042d93c2e5a1df913464e22081e0ba4e086d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Apr 7 08:54:40 2024 +0100

    Use variables for card styles instead of inline CSS rules

    This cuts the size of the /articles/ page from 400,638 bytes to 372,554.

commit 9f209c2ce4e213f039e4a556f7794ce8128bbe8f
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Apr 7 08:48:55 2024 +0100

    We don't need to re-include variables.scss for every bit of custom CSS

    This repeats the CSS variables for every custom block, which balloons
    the size of the custom CSS. Yikes!

    On the all posts page, this cuts the size from 648,242 bytes to
    411,494 bytes.

commit f1c043600402f6165faffc9de39200dbd1202b64
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Apr 7 08:33:56 2024 +0100

    WIP homepage

commit 4e1c321f6fdbcba206c9d585b8e3e8278a6dba0b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Apr 7 08:26:06 2024 +0100

    Add a missing field to the front matter

commit 959849ae1f38389e44a0f899a9af740cbdf1223d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Apr 7 08:24:15 2024 +0100

    Remove a few posts from the index; remove a few posts entirely

commit a2b28c23b34ae32e98e8cb67ff898ca1d27902ca
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Apr 7 08:13:46 2024 +0100

    Add three TILs, including shuffling an array in Jekyll

commit a1581c936b9282c88d5448843f148032ab657f17
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Apr 7 08:13:11 2024 +0100

    Introduce the notion of a "featured" article, more prose

commit 663255cd664dbf30e9da7343e88e0d5c6ee53f2f
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Apr 7 07:51:43 2024 +0100

    Continue fiddling with contact info on the homepage

commit f290d2df295c67b7a4ae5ed1390ab4b514150207
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Apr 7 07:50:58 2024 +0100

    Fix the list of recent articles on the homepage

commit 10bdd48d694ce005cf1f598415f25dccfb10bfa8
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Apr 7 07:35:52 2024 +0100

    Let's make the "Say thanks" page be a bit more standalone

commit c732cb4461eb1f21bd3c2aed64ce83c4d574ad4c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Apr 6 16:45:26 2024 +0100

    Stop saying the word 'blog'

commit 9784c1fa2b33fe26f54be7ba6b2471e7f1db01c6
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Apr 6 16:44:40 2024 +0100

    Tidy up a few of the error pages

commit 8f260fd813b4002d7d3310757695756c527e7195
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Apr 6 16:37:00 2024 +0100

    Put the privacy page in the contact nav section

commit 7e97f9da62731538e40006e1171f04d75bb20a80
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Apr 6 16:35:24 2024 +0100

    Bin the /all-posts/ page

commit 0ed412b723670c4323b649d7ad4f416d48a20596
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Apr 6 15:19:38 2024 +0100

    Add a new `/articles/` page, with my new tag filters et al

commit 939987c4818e79c00f841608adfe90a4f92f981a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Apr 6 15:14:32 2024 +0100

    Remove two Harry Potter articles from the index

commit 2da7a47ee58bb8ae60a1d6b5c58fa68053f47f3d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Apr 6 12:18:10 2024 +0100

    WIP Start building an articles page

commit 6cd584e436b295e37f940aad60807ef0653c4a5b
Merge: a0fc4990 c83ae002
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Apr 6 14:12:39 2024 +0100

    Merge pull request #757 from alexwlchan/ditch-post-url

    Replace the {% post_url %} tag with hard-coded URLs

commit c83ae0026fb4d3265e3823800b8efb9c369910f4
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Apr 6 13:37:43 2024 +0100

    Replace the {% post_url %} tag with hard-coded URLs

    This will make things easier when I move my posts into a new 'articles'
    collection, and the `{% post_url %}` tag stops working.  Also, this URL
    structure doesn't change very often, so this is a bit more portable.

commit a0fc499051802e997ae3b748b569b14b5c722963
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Apr 6 12:19:18 2024 +0100

    Remove an unused variable

commit 671d9a288a147daea44c9f451309aab5b947008f
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Apr 6 12:02:35 2024 +0100

    Add an extra comment to the `markdownify_oneline` plugin

commit 42542c499b33d951c8c7bce8df4c802682a274d2
Merge: 733deb7b 3058e032
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Apr 6 10:44:03 2024 +0100

    Merge pull request #756 from alexwlchan/remove-per-year-indexes

    Remove the per-year indexes; redirect all to /all-posts/

commit 3058e0326144b1326d95876e247e32170e97c2d7
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Apr 6 10:31:11 2024 +0100

    Remove all the per-year archives, dump all to /all-posts/

commit 3eb964f823def505bd63f304cfb7e14071eb3b35
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Apr 6 10:21:17 2024 +0100

    Add a lint for "hackable" URLs

commit 14e29ccbfa16ae441e5e5230fbb831ef6172a3c8
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Apr 6 10:17:33 2024 +0100

    Remove the style sample

commit 733deb7b817a850e22a69f9255577e867d719731
Merge: e1700443 0335426e
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Apr 5 23:18:12 2024 +0100

    Merge pull request #755 from alexwlchan/port-tils

    Bring across some more TILs from the old site

commit 0335426e6c755335451b8ee9a0f3fc6f12d574de
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Apr 5 23:14:31 2024 +0100

    Fix a broken redirect

commit 81e04e0f637deca868c2e0d6c3303120ca6f3795
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Apr 5 23:11:03 2024 +0100

    Remove a broken link

commit c02427d72b691a39495d212d30e306d076491ea6
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Apr 5 23:07:54 2024 +0100

    I need to look for a space here also

commit 101a00d66b48b10d401b53444360fc10808fcf9a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Apr 5 23:04:56 2024 +0100

    Try to fix an issue with LaTeX rendering

commit fe566f422166e3236dd623c9b5ecfd381ea61ef7
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Apr 5 22:58:54 2024 +0100

    Bring across a few more TIL posts

commit cbad0491256a3e99b19b00cc5c4a802d185842e2
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Apr 5 22:57:59 2024 +0100

    Remove a couple of unnecessary filters for perf wins

commit e86b4591a8146be89eb542333a168c3d0fba3640
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Apr 5 22:54:40 2024 +0100

    Convert a post from 2013 into a TIL

commit e17004431cfe85dbc928af66b19b419988b1141c
Merge: c508a844 9b02df3c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Apr 5 22:20:52 2024 +0100

    Merge pull request #754 from alexwlchan/lets-add-tils

    Let's add the beginning of a TIL section

commit 9b02df3c3b28798c1bf528da9998686e9379ed1f
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Apr 5 22:14:54 2024 +0100

    Remember to run rubocop

commit 5567ab538e519dd7535214a22a7a9d7f7a676d75
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Apr 5 22:13:17 2024 +0100

    Continue fiddling to make the linter logic correct

commit 204ef6911d5951b387ed4eb1894f5b8781c524e2
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Apr 5 22:08:54 2024 +0100

    Fix this linting rule

commit 1ae9c6308d7a4f23bb061816e0c7a1f4fcae2fa7
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Apr 5 22:05:36 2024 +0100

    Fix a broken bit of Ruby

commit 7afc87dc5c11ec32a18aedaa38fed1329e7bd30d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Apr 5 22:02:33 2024 +0100

    Tweak some rules around the linting for TIL

commit cffad955f573a32a141f6bb667eca752d7e2b04b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Apr 5 21:55:30 2024 +0100

    Fix a styling bug on Firefox

    For some reason the `a:hover` selector removes the styles from `a[selected], a:hover`.
    Separating them fixes it.

commit 8b52bc6b9973d270fa9ebd42104ec33dab37b8a6
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Apr 5 21:54:05 2024 +0100

    Fix the width bug, but properly this time

commit f66a2f3cb3cb19923db63e6e2bb7506b258883b2
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Apr 5 21:51:38 2024 +0100

    Restore the border radius to pre/blockquote

commit eb8124c7b04ae9c79335cdbff5532d913afd5273
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Apr 5 21:51:30 2024 +0100

    Try to fix the layout bug where the page is too wide

commit 5c6149eb04c776d859f7b1de483c78c69ea7a98d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Apr 5 21:49:55 2024 +0100

    Fix a bug in TIL titles

commit c66664b34ee663f3d06e418e6f21e4aaea52aa33
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Apr 5 21:49:19 2024 +0100

    Fix a bug in the spacing of the nav

commit a6b2fd8d0188fd11ca5b40dd880f10025a47f0db
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Apr 5 21:45:57 2024 +0100

    make this more conversational

commit cf952e8172782f18d3efd4e2c14c64288cb200a9
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Apr 5 21:45:36 2024 +0100

    Add an RSS feed for my TIL

commit 01122eea6787e13a5861ff648bc0260021db3b0f
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Apr 5 21:37:48 2024 +0100

    This nav component shouldn't be cached

commit 4fe4a4a4c6beb6b3c1111f847eaffc07362117c4
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Apr 5 21:37:41 2024 +0100

    Start adding the TIL section

commit c508a8449cba3c25577456608385c966870300c1
Merge: 4b1b72eb e038c0c5
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Apr 5 21:27:35 2024 +0100

    Merge pull request #753 from alexwlchan/rejig-the-rss

    Create a basic template for RSS feeds

commit e038c0c53f0e7dc0e69353e4bf649c3e4f77fbd4
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Apr 5 21:23:19 2024 +0100

    Create a basic template for RSS feeds

commit 4b1b72eb5a19cc683b550df98d8cfeb525bb592a
Merge: 32d9bc85 297c0c09
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Apr 5 21:04:22 2024 +0100

    Merge pull request #752 from alexwlchan/better-nav

    Start improving the top nav and the contact page

commit 297c0c0991ce4fc86504ec8ce27166ea4a485eee
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Apr 5 21:00:43 2024 +0100

    Add the new nav_section field to the front matter

commit a3dd5c9fad04174cb681e53e529044d7b1cebe98
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Apr 5 20:56:07 2024 +0100

    Continue tweaking link styles in the nav

commit fb705ba29e9a211a4692253eda0e6778987eb026
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Apr 5 20:55:30 2024 +0100

    Hovering a nav link gets an underline, not a background

commit 1c35ede71f3519a03f9c484689ff5d3292e72e11
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Apr 5 20:51:12 2024 +0100

    The title of pages/posts don't need to be linked

    Plus, ditch the `novisited` link class, which was mentioned in a comment
    but no longer working.

commit 2495c29143b3668523d7210d053b0a86aadf2199
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Apr 5 20:49:54 2024 +0100

    Add a small gap between link underlines and the text

commit c6c69b0c08e9c85531b1d90a5c60abeaa459858b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Apr 5 20:48:15 2024 +0100

    Bring across the new, simpler contact page

commit 32d9bc8576fddfb0250290765426be83683e10e4
Merge: 7a3afa87 56f7cc5a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Apr 5 20:43:16 2024 +0100

    Merge pull request #751 from alexwlchan/better-footer

    Bring across the improved footer from the redesign

commit 56f7cc5a027acb86df33ecc183f85162ff75e425
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Apr 5 20:36:47 2024 +0100

    Bring across the improved footer from the redesign

commit 7a3afa8795906c8a8b5416dad781edfe331dc92b
Merge: 313add6c 4c3f8541
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Apr 5 20:24:55 2024 +0100

    Merge pull request #750 from alexwlchan/tidy-up-css

    Continue tidying up the Sass files

commit 4c3f85414f697b14d50565ddf42744aa4b052a7d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Apr 5 19:20:41 2024 +0100

    Get the styles for embedded tweets out of the global stylesheet

    Maybe 5% of my posts have embedded tweets, and this is ~25% of the main
    stylesheet.  Let's load it on-demand instead!

commit 926083f1aa14827801a59eb513521ffc4154687f
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Apr 5 19:19:01 2024 +0100

    Continue tidying up some of the styles

commit 9ba823e7c410ce37dcfceb3805c858cb37ae1fe4
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Apr 5 19:16:08 2024 +0100

    Do away with an unnecessary #nav_inner div

commit b6ea387f38b1dab2c732aa88bb2b307b03b4337d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Apr 5 19:10:42 2024 +0100

    Consolidate a couple of styles out of `_main.scss`

commit a136d4b1361756786a7d35f0ad777a5d1a7909d3
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Apr 5 19:08:31 2024 +0100

    Remove a now-unused `_settings.scss` file

commit 428e7acf158ac6dcd63c988eda346074e229e312
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Apr 5 19:07:55 2024 +0100

    Move the syntax highlighting styles into the components folder

commit 313add6cecb6b402d799c29bd602feb4afbcde18
Merge: 4c61ecbf b70c3b50
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Apr 5 19:03:17 2024 +0100

    Merge pull request #748 from alexwlchan/more-theming-bits

    Continue to refactor the theme-related code

commit 4c61ecbf4646af68a24b31a517243e01cd615fe9
Merge: ed34c5f3 5d0ef1b9
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Apr 5 18:59:03 2024 +0100

    Merge pull request #749 from alexwlchan/remove-subscribe

    Remove everything related to the "subscribe" component

commit b70c3b5091a27e2161b94da2a552fd46b68aa19c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Apr 5 18:56:11 2024 +0100

    Fix the name of a method for rubocop

commit 5d0ef1b95a19e7505852534f1c6110834e35c2c0
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Apr 5 18:55:05 2024 +0100

    Remove everything related to the "subscribe" component

    This is a dead-end I never went down, so at least for now I'm going to
    remove all the associated code -- I can always come back to it later.

commit 820386e6f4387980a7746ecdd2e56f1c3339d6d3
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Apr 5 18:45:05 2024 +0100

    Slightly tidy up some of the code in the <head> for tint colors

commit e430f2ac946d251bd504d5e201df3b694095842d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Apr 5 18:43:08 2024 +0100

    Fix a couple of linting issues

commit f14b1f3089f2e5998dcac2f6087dc6768f4f6119
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Apr 5 18:41:43 2024 +0100

    Create the headers and favicons for new tint colors

commit 81c64ab32e72701092044e25703ab20fca7f324b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Apr 5 16:52:38 2024 +0100

    Create a new utils file

commit 590a5a04ac4c3cf5f02add4d0ace2aee2e8f95da
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Apr 5 16:51:34 2024 +0100

    Add a function for getting CSS colors

commit ed34c5f32ae8a736abcd35931c84ae6c37d9f34d
Merge: 77e16179 acf8ae12
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Apr 5 14:19:19 2024 +0100

    Merge pull request #747 from alexwlchan/css-colour-variables

    Keep rejigging the plugins I use for custom tint colors

commit acf8ae123d4bc261de752ea774767549b9f1e2b6
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Apr 5 14:12:41 2024 +0100

    Finish breaking up the vague `css.rb` plugin, create one for tint colors

commit dc1b384c70a878fcf2479f7574f58d081128819c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Apr 5 14:05:09 2024 +0100

    Start writing a new plugin for tint colors

commit 77e16179af240c93b0652862e1b3caa0cb406ffb
Merge: 4e6c3c3b 513c290b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Apr 5 13:46:45 2024 +0100

    Merge pull request #746 from alexwlchan/color-variables

    Continue improving the CSS handling

commit 513c290ba00c8be2fadb275ff0f425de881aac67
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Apr 5 13:43:07 2024 +0100

    Fix some broken Ruby syntax

commit 0842e53a4fed3a3d56d43bce030cbfaadd28085f
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Apr 5 13:41:33 2024 +0100

    Run rubocop to fix the linting issues

commit 55d36ab0f21b03cdf57117bff87e29762a18532c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Apr 5 13:29:53 2024 +0100

    Create a new plugin for setting the CSS fingerprint

commit 4866a440d7c631076cdf1e7fb8380024a4a6345a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Apr 5 13:24:53 2024 +0100

    Push all the tint colours into CSS variables

commit 4e6c3c3b7e9d1e8c3712748fa7382908e3774c8e
Merge: 155f52ba 35c3551e
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Apr 5 08:33:46 2024 +0100

    Merge pull request #745 from alexwlchan/more-variables

    Move all the Sass layout variables into CSS

commit 35c3551e9ad61f501efa9cb27f7e46f36cac6a1b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Apr 5 08:30:09 2024 +0100

    Add a comment about the Sass config in the _config.yml

commit 0e69999af1a84c7bac7ddc2c94d6d9ab8d154994
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Apr 5 08:28:46 2024 +0100

    Make a nicer heading here

commit 602aeb47df9149751693e2798af7eccbd0d0ea3d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Apr 5 08:27:09 2024 +0100

    No more Sass layout variables, only CSS variables

commit a9a5ed0f99d2df26f9c1723115ca28e2db23ec0a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Apr 5 08:24:06 2024 +0100

    Collapse down a few more variables into CSS

commit 1ba0517abcc503866a4e0d88ef5fe482d81d1e44
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Apr 5 08:22:25 2024 +0100

    Push a couple more values into CSS variables

commit 155f52ba30b96de45a47b25a06ab9ed7d02541f1
Merge: e2cb90d2 70c8ed7a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Apr 5 08:16:53 2024 +0100

    Merge pull request #744 from alexwlchan/more-css-variables

    Continue leaning on CSS variables

commit 70c8ed7aacab07ad0f1a8a0c81184661148dd461
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Apr 5 08:13:06 2024 +0100

    Add a linebreak for readability

commit c1e7ff1677129f7d9e44c6bb7a63624e3ab935a7
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Apr 5 08:11:52 2024 +0100

    Continue leaning on CSS variables

commit 280de584b639cb119fb9be72749f5e22ae9d394b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Apr 5 08:09:14 2024 +0100

    Also use a CSS variable for max-width

commit 0dc5effa0cf4733d360c2704df027df996a3fe95
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Apr 5 08:06:24 2024 +0100

    Continue leaning on CSS variables over Sass

commit e2cb90d2aadf4d680403cabe2df0bc475d15e2e3
Merge: 97332786 c5cc1a96
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Apr 5 07:55:55 2024 +0100

    Merge pull request #743 from alexwlchan/use-css-variables

    Start using CSS variables in place of Sass

commit c5cc1a96ccf0bc9f6ca52936bef70ab72911f39e
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Apr 5 07:46:19 2024 +0100

    Remove a bunch of duplicate keys from `_settings.scss`

commit af97dde880859e4ffce0a62b5b0e9d729bb9934b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Apr 5 07:44:37 2024 +0100

    Remove a few more duplicate variables

commit f5d50e5454999830400fb647191ad58bf6168d4c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Apr 5 07:44:08 2024 +0100

    Fix a long-standing bug in the CSS on this post

commit f0b7019f555ad974e94f7a98bdd98893a7d6e50d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Apr 5 07:37:56 2024 +0100

    Consolidate on a single variable for grid-gap

commit 36c4cca1c1ac5de43a5b0669cda901753c895b6b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Apr 5 07:37:41 2024 +0100

    Remove a couple of unused variables

commit 842e3b46cee9d5e56082fce9a32f48aff2906ca2
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Apr 5 07:35:38 2024 +0100

    Replace more colours from `variables.scss` with CSS variables

commit 043c7e8d472a262d98c389f41aa1aca978147439
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Apr 5 07:29:06 2024 +0100

    Start using CSS variables for dark mode

commit 973327863b40d844a24419e74b01b195cf877d6d
Merge: 6eeaba01 89774da6
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Apr 5 07:24:25 2024 +0100

    Merge pull request #742 from alexwlchan/tidy-up-config

    Tidy up my _config.yml configuration file

commit 89774da69a9178cf37e75257d2217fc1aab2df4c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Apr 5 07:16:19 2024 +0100

    Pull out a couple of template variables

    As part of this I've removed the `smartify` filter, which turns out to
    have a noticeable impact on performance -- from ~11s to ~8s on my MBA!
    This filter is really quite slow, and irrelevant for a site title that
    doesn't have anything in need of SmartyPants.

commit 4fead652a4a71b272c4f16b04b1846c0a87dcac2
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Apr 5 07:12:27 2024 +0100

    Don't repeat the author key in `_config.yml`

commit f7ab3c32a18cda5da376bb17819ebd1125bfa027
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Apr 5 07:12:11 2024 +0100

    Don't repeat my email address in the config file

commit f2a6f0d50e99674e727c77ccddcb85422b7b08ba
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Apr 5 06:45:33 2024 +0100

    Actually `strict_variables` isn't what I want here

commit e2619b7732e1be1a1ea3a36bc5b6d7eb0a44ad58
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Apr 3 13:18:56 2024 +0100

    Remove a dead email address

commit 511d95b55542e0a02bf51ce7978a5690d86d1e59
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Apr 3 13:18:56 2024 +0100

    Add some headings and comments to `_config.yml`

commit 6eeaba014d239e9b388c517f9b4b25f7cd7f874d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Apr 2 19:32:03 2024 +0100

    I don't need to delete these images every time

commit 166f6d9eb5f9c6b0557767bd373bfb5b0ee61a65
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Apr 2 18:45:57 2024 +0100

    Fix the width of some of these images

commit 578afb913845c2914795b24124ae7addae5dd5e8
Author: GitHub Actions on behalf of Alex Chan <githubactions@alexwlchan.net>
Date:   Tue Apr 2 15:40:35 2024 +0000

    Publish new post commons-explorer.md

commit fdf9b440832bcd398d9c3057539d436bd3034f1a
Merge: 949f432f feb18a78
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Apr 2 16:37:32 2024 +0100

    Merge pull request #739 from alexwlchan/commons-explorer

    Add a quick post about the Commons Explorer

commit feb18a78f263b975306198ad0be2ba62d90675a0
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Apr 2 16:29:46 2024 +0100

    Add a quick pointer to the new Commons Explorer

commit e9891e3e8057d9ffe2165898fae172d30f4c0435
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Apr 2 16:06:30 2024 +0100

    Tweak the posts highlighted in my eggbox

commit 949f432f9078c44e7b4a552fedaacb4fb5993f82
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Mar 18 20:53:59 2024 +0000

    Clarify Linode/Netlify

commit 27e527868b035e7dff5c5035a88fb6c00b3b5f96
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Mar 18 20:46:32 2024 +0000

    Remember to bump the updated date!

commit 456e71598ace0388a021d4b3101b66febdda1e33
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Mar 18 20:46:20 2024 +0000

    Tidy up the privacy policy a bit

commit 3dc4c1b974e09df108ec5f639d19b06cdc786612
Merge: 0e0145a0 54f9d0c4
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Mar 17 09:52:43 2024 +0000

    Merge pull request #738 from alexwlchan/remove-unnecessary-data

    Remove unnecessary data from the saved tweets

commit 54f9d0c409fb1221e37b6b3c1aca0aef1290acc1
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Mar 17 09:48:27 2024 +0000

    Finish stripping out the tweet metadata

commit 99c33d720e3645dc61c151361b0d791202132705
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Mar 17 09:46:37 2024 +0000

    Tidy up the doc comment

commit ff230a362d2720c7e8fb8e787202277506456ce5
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Mar 17 09:46:03 2024 +0000

    Strip out a bunch of fields that aren't being used

commit 0607221b90e54dd937fbf41c31206119f46088e7
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Mar 17 09:36:13 2024 +0000

    Don't duplicate the `id` metadata on tweets

commit 8522849303e494aa0008f7913b19cbab8f902b9b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Mar 17 09:30:34 2024 +0000

    Remove the `in_reply_to` metadata

commit 0e0145a07fd9b8c608579fbe71b3dc2aa0c37e8b
Merge: 5d43beb4 a7dd5374
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Mar 17 09:23:14 2024 +0000

    Merge pull request #737 from alexwlchan/more-tweet-schema

    Simplify the user and entity metadata on tweets

commit a7dd53747189fe92875d02cfc55e897ad8c1e9a5
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Mar 17 09:17:15 2024 +0000

    Simplify the media metadata for tweets

commit c5a3da8759ed3df8caa47e7b0b602a0439451312
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Mar 17 08:58:32 2024 +0000

    Merge the `extended_entities` and `entities` fields

commit c45a3673b6b6028af95248b2458fa19676ec7406
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Mar 17 08:44:33 2024 +0000

    Simplify the user metadata for tweets

commit 5d43beb48b131fb52405e89c4856919effaf240b
Merge: 1d52b6c4 68d914b6
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Mar 17 08:33:48 2024 +0000

    Merge pull request #736 from alexwlchan/expand-the-schema

    Simplify the metadata schema for tweet text and entities

commit 68d914b6ee470e1d8271eeb2e63b2dddfa85e03a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Mar 17 08:27:26 2024 +0000

    Start building out the schema for media

commit 2d938f58858997a46feece87a81a8e9c76528e20
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Mar 17 08:25:55 2024 +0000

    Remove the unused symbols field from the tweet metadata

commit ef6cd41e79228ea1eebd7467678def0434817db2
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Mar 17 08:23:01 2024 +0000

    Simplify the tweet metadata for hashtags

commit 1513fa2a868a26a55eaa76cab3426523b272c209
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Mar 17 08:18:19 2024 +0000

    Simplify the tweet metadata for user_mentions

commit e571f7f7df710fc0cebadc1ad8b93bd958a0d150
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Mar 17 08:11:37 2024 +0000

    Simplify the tweet metadata for urls

    * We don't need an empty JSON list if there aren't any
    * We don't need to keep the indices, a simple replace() is enough

commit e1c21ee05d3c0516cb21b54cb4c2387100b52719
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Mar 17 08:02:21 2024 +0000

    Simplify the "text" field in the tweet data

    Previously tweets were a mix of `full_text` and `text`, based on changes
    in the Twitter API when the number of characters increased from 140 to
    280 and the API responses changed.

    Now we just use the `text` field and can simplify the rendering code.

commit 1d52b6c41782a4306d5b54b30a7e1eef9b8c8a88
Merge: f7eeab76 c21247e3
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Mar 17 07:34:35 2024 +0000

    Merge pull request #735 from alexwlchan/start-tidying-up-tweet-data

    Refactor and tidy up the TwitterTag class

commit c21247e394f1378c6fe0023819451115d70b8cc6
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Mar 17 07:24:14 2024 +0000

    We can use `begin … end` here for nicer error handling

commit 27aa26a6cf24f6739f5648323e5a417301a46359
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Mar 17 07:16:49 2024 +0000

    Improve the way we extract the tweet URL/screen name/ID

commit 9a50cb60b6aa43681b438692b77327758931e85b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Mar 17 07:12:53 2024 +0000

    Remove another now-unused method

commit 64c3b47cb0cb22b2279992523d969f920b508265
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Mar 17 07:12:12 2024 +0000

    Add a comment to `cache_file`; rename it to `metadata_file_path`

commit b62bf49da0e802ac0b93ecd5d6af88ab0945b083
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Mar 17 07:07:35 2024 +0000

    Remove a now-unused method

commit 9b005497e2b519b2df51578818888e6bae3339de
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Mar 17 07:06:09 2024 +0000

    Get all the metadata inside a single method

    This adds a minimal schema that can be used to validate the format of
    the metadata, so I can gradually add types to this schema.

commit f7eeab768f65087ab74792c1aa8fc8fe1d128598
Merge: dd500c7d 3746d086
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Mar 17 06:56:09 2024 +0000

    Merge pull request #734 from alexwlchan/remove-old-script

    Remove a now-dead script for saving tweets

commit 3746d086c2806616e4dd6efed610c1469e037abb
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Mar 17 00:04:39 2024 +0000

    Remove a now-dead script for saving tweets

commit dd500c7ded5f51f260511312143542cdafb5a1e2
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Mar 16 23:58:23 2024 +0000

    Update 2024-03-15-step-step-step.md

commit b67d88254120c8f1e537084dfe9f9a96a8a70fe2
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Mar 16 22:22:04 2024 +0000

    Add lazy loading to a bunch of these images

commit 6d15da7cd8747203d10c7ee124459e8cac4bffed
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Mar 15 16:33:09 2024 +0000

    Update 2024-03-15-step-step-step.md

commit 1bbcb2d1e4100efbd5048fe9433921e1a256b604
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Mar 15 13:32:50 2024 +0000

    Update 2024-03-15-step-step-step.md

commit d3e6f97b78c5544e9c038b1eabd932de86782b44
Author: GitHub Actions on behalf of Alex Chan <githubactions@alexwlchan.net>
Date:   Fri Mar 15 12:56:47 2024 +0000

    Publish new post step-step-step.md

commit 4328ad790e88a6f3946d5099fbc51f012d64fd3f
Merge: 4f03967f 5c63b2e3
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Mar 15 12:53:42 2024 +0000

    Merge pull request #732 from alexwlchan/monki-gras-2024

    Add the notes from my Monki Gras talk

commit 5c63b2e3482d95103a9b4ff3a32ada120a5dd203
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Mar 15 12:42:36 2024 +0000

    a few final tweaks

commit 6d795f92b345a7300946dae837ac3e18c636346c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Mar 15 12:34:32 2024 +0000

    make this a 2:1 aspect ratio

commit 3b4069067e25ca04b9227e185c76b679f01f0402
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Mar 15 12:23:28 2024 +0000

    Add some better alt text

commit ee1bedbe1f73abecc33cbcb3c86facccd1542564
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Mar 15 11:48:40 2024 +0000

    Make some final tidy-ups

commit 8c4bea9817ad16962973bd24880b16a02129c287
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Mar 15 11:19:32 2024 +0000

    Tidy up the colours and theme

commit 652c3b2b61cf4d717678cbf1f648d0cbc4de5676
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Mar 15 11:09:02 2024 +0000

    Add some missing alt text

commit 13f5d14f4d830ccc2b0ff14f977624f6d0ce928d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Mar 15 11:00:54 2024 +0000

    It's yesterday, not today

commit db3fbd95db00bdcb22780bab487109e056c7a6c3
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Mar 15 11:00:44 2024 +0000

    Add the initial draft of my Monki Gras post

commit 4f03967f0cbd9f2cc308817205c2e70de1d30792
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Feb 28 08:51:53 2024 +0000

    Add a simple ASCII art diagram

commit 612d45f9a273cbb3510e70885955d80def254a13
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Feb 16 23:34:49 2024 +0000

    Update 2024-01-21-ian-flemingo.md

commit bf610adaff706ef132b607e7e3a84f6cf8d884c3
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Feb 15 08:04:44 2024 +0000

    Fix another issue with the YouTube API

commit 3bde60f8c106be01a532643888a09e50cbc44f60
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Feb 15 07:53:27 2024 +0000

    Remember to unpack the `expiry` parameter

commit 049e1f3968b93c5cda88d4c23ec77b35a32cc65f
Author: GitHub Actions on behalf of Alex Chan <githubactions@alexwlchan.net>
Date:   Sun Feb 11 23:04:31 2024 +0000

    Publish new post moving-youtube-likes.md

commit c2926c94cb55884632779f39f40a0fb80b61cfba
Merge: baeba47c 38d53aad
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Feb 11 23:02:01 2024 +0000

    Merge pull request #726 from alexwlchan/migrating-youtube-likes

    Moving my YouTube Likes from one account to another

commit 38d53aad21a850597cb2e373c8455688646155a1
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Feb 11 22:57:33 2024 +0000

    remember to use that sRGB colour profile!

commit ca9a437b39dbfc6627892c2c64560becc062e879
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Feb 11 22:53:09 2024 +0000

    add a link to the original photo

commit b3caf8789af3e4dcfc26ca4c07cd92a9d5411ede
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Feb 11 22:51:02 2024 +0000

    editing markups

commit dccd30ed5b7f975eec51ce5a18dfa87f8777edfd
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Feb 11 22:32:50 2024 +0000

    first draft of the YouTube post

commit c24cdc04bf222f47beac885a92131cc35058aca9
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Feb 11 17:21:38 2024 +0000

    Add the outline and the post card

commit baeba47cef5a724ccd8b94c82d7a2f368f37ef19
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Feb 7 08:08:47 2024 +0000

    2022, not 2024

commit 5deade5ed9d0089940330e771b0856a179199519
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Feb 7 08:06:01 2024 +0000

    Link to my shortcut

commit 7a2f0a26abac84bc680902f701d77f168bfab550
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Feb 6 20:56:43 2024 +0000

    Add a note about Time Machine

commit 59205514e2ae5c558f4148d5bafed86d9bfe0717
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Feb 4 21:15:50 2024 +0000

    Bump the versions of all the GitHub Actions workflows

commit 07e8074689df70c744c2e54b5239344d1652f6ea
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jan 26 20:15:13 2024 +0000

    Remove a few unnecessary chunks from the RSS template

commit d23cd1248fcf7a7fef61fd19bd5b620106783c5d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Feb 4 19:50:21 2024 +0000

    Lazy load the two big images

commit 7d734a23c6147f010aaad81c3843fa41015b1af1
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Feb 1 06:32:29 2024 +0000

    Update 2024-01-31-big-pdf.md

commit 3a041f8fe311031406fa830c1b8b94ca5ab41b5c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Feb 1 06:29:04 2024 +0000

    Update 2024-01-31-big-pdf.md

commit 77db88495ce4b7cece427c2326b180e9aba3b185
Author: GitHub Actions on behalf of Alex Chan <githubactions@alexwlchan.net>
Date:   Wed Jan 31 21:32:45 2024 +0000

    Publish new post big-pdf.md

commit c2af58df75211b33733ab03a9a24aac1af2013dc
Merge: c7847346 f3555088
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Jan 31 21:29:50 2024 +0000

    Merge pull request #724 from alexwlchan/big-pdf

    New post: Making a PDF that’s larger than Germany

commit f3555088e440fba5337f38e56813320566ce0407
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Jan 31 21:25:48 2024 +0000

    Add some alt text

commit cf6824e873f652f37d9230c1c3332864490cd13f
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Jan 31 21:21:51 2024 +0000

    sort out the card issues

commit 54e8129b42bcbb0079dbaaa23f5f67600d78c085
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Jan 31 19:53:06 2024 +0000

    Add a card for the big pdf post

commit 81cfcb5f06af6c7bef2556092909f02b8af76bc0
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Jan 31 19:37:47 2024 +0000

    make some big PDF markups

commit cd535ef79e4c902179d71d7abf233edd56d3ed90
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Jan 31 07:11:47 2024 +0000

    Make one very small tweak

commit 31904f95a6fcaa539e8385e9e4a853d499db3717
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Jan 30 23:17:25 2024 +0000

    add the post card

commit 63de9016e445e1aae43a1d53700c1da598a11a9d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Jan 30 23:08:23 2024 +0000

    Add all the bits for the PDF post

commit ebda60e29edb4d9661c04ba12a6525aecb631d5a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Jan 30 19:04:15 2024 +0000

    Make the PDF layout be dark-aware

commit 1c03b80fdc139f5423184fc8bd096d86a279eb56
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Jan 30 18:57:44 2024 +0000

    Start the post about big PDFs

commit c7847346524a78b7748f7b4001ac8021320c40a7
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Jan 24 23:11:07 2024 +0000

    Add a couple of comments about headers

commit a3a7f5e3d13d02e693011becafafab3eaaed6e26
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Jan 22 23:21:19 2024 +0000

    Pass along the cookies

commit 343b58a203e22da85dbd159eba8831a2893f95fb
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Jan 22 23:20:36 2024 +0000

    Revert "Add the 'is_me' parameter to the analytics snippet"

    e8fe7b5d697993e59d78e7a00f764ddd996c2bb2

commit e8fe7b5d697993e59d78e7a00f764ddd996c2bb2
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Jan 22 23:14:03 2024 +0000

    Add the 'is_me' parameter to the analytics snippet

commit e6abff886d06d9a997abfd66215320baacfa0af1
Author: GitHub Actions on behalf of Alex Chan <githubactions@alexwlchan.net>
Date:   Sun Jan 21 11:24:05 2024 +0000

    Publish new post ian-flemingo.md

commit 8a502f4f01ce10eaf5a9dd25361f740d9c4e5165
Merge: 929730d0 72285d53
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jan 21 11:20:51 2024 +0000

    Merge pull request #723 from alexwlchan/ian-flemingo

    Add my Ian Flemingo post

commit 72285d53beca58df140bc31f6ff51585e89df6ce
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jan 21 11:15:46 2024 +0000

    Fx the sRGB colour profiles

commit 4a57bb5de743bd14a7df9d7b705623d5bcaf7b44
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jan 21 11:10:05 2024 +0000

    Finish the Ian Flemingo post

commit 5f63005341340179f673af5ccc10284577bbb021
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jan 21 11:01:16 2024 +0000

    Exclude this post from the index

commit e8ae1dfc4dc5e8d2df8e471fba3097e09ba04a39
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jan 21 11:01:07 2024 +0000

    More Ian Flemingo bits

commit d25f3eeeecb23695e47c785924de3e968b5c8c55
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jan 21 10:19:31 2024 +0000

    Add Flemingo's author photo

commit d07c960c4e5f19564d631e9aa5c9273e9f1142e1
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jan 21 10:16:15 2024 +0000

    more flemingo bits

commit 929730d01ddbb444e147b530681baaa0a4e7b761
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jan 21 08:55:51 2024 +0000

    Update privacy.md

commit 2a18b391bb8e649a1fed2736254e5777d7c8d9b7
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jan 21 08:55:37 2024 +0000

    Update privacy.md

commit 7d1d26108a140ab970022ad2f87d5b9c58b2859b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jan 21 08:54:43 2024 +0000

    Update privacy.md

commit 980e720d135d64b5ff2711eb1054a84af97fb602
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jan 21 00:38:35 2024 +0000

    add the new CSP header in the right place

commit 5fa043d596e633a600d8a859555772582c541cfa
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jan 21 00:32:41 2024 +0000

    connect-src, not content-src

commit 92bccb513390859d991f9c013ea7b29e091aeee4
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jan 21 00:29:18 2024 +0000

    Add the analytics site to the CSP

commit 380332524c10f1c23c69ae0f54670f4245fe785e
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jan 21 00:24:37 2024 +0000

    Add a tracking pixel and privacy policy

commit d4490afaf13b1d7d63335a3562c6cbe9f70515ed
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Jan 20 22:08:10 2024 +0000

    Start doing the Ian Flemingo post

commit 6da4fcee8ccaee29d9e50b3d78489e769cf96d90
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Jan 20 20:45:42 2024 +0000

    Add a first draft of the Ian Flemingo post

commit ea8c3338b49ec6e1f4f97da8f0d57fb7a14dca69
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Jan 9 21:28:56 2024 +0000

    Now these SVG files are flushed from the cache; we don't need to keep deleting them

    Closes #720

commit 77b9096eed7f10bec5d7365e761a8d979db18d85
Merge: ed793a25 52a84253
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jan 7 22:38:14 2024 +0000

    Merge pull request #721 from alexwlchan/tidy-up-svg

    Load all SVGs using inline_svg; don't copy an SVG to _site unless it's actually linked to

commit 52a84253686de3efc34e128b67532a927fda2d51
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jan 7 22:35:02 2024 +0000

    Make RuboCop happy

commit b70d6f39478216d3f8d74aa9bd3d686a11e8bd97
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jan 7 22:31:21 2024 +0000

    Purge any cached SVG files from GitHub's cache

commit 9500af7366b741f00127b49faedad58df0ce46f0
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jan 7 22:30:47 2024 +0000

    Don't minify the SVG files as part of the static file generator plugin

commit 36d24179737754941f8ee3e289525ea1c051fdc8
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jan 7 22:30:36 2024 +0000

    Switch the remaining SVG files to use inline_svg

commit 6ee1bf389087748b46cb2c1ab1e6b84999dadd1a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jan 7 22:24:57 2024 +0000

    Cut the size of some SVG files; add 'link_to_original' to the inline SVG plugin

commit ed793a25fa24a21712fa4ed4560ca7140cb5b550
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jan 7 21:32:01 2024 +0000

    Add a card for the best age picker post

commit 7da2837babfc7b6d5b12999fe369be1097e23412
Author: GitHub Actions on behalf of Alex Chan <githubactions@alexwlchan.net>
Date:   Sun Jan 7 21:11:32 2024 +0000

    Publish new post best-age-picker.md

commit 5724e7df13642fe39e11a7a7c8a05976b697d480
Merge: c8b09ad7 2bbb5f8c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jan 7 21:08:03 2024 +0000

    Merge pull request #719 from alexwlchan/birthday-cake

    Add a post about age pickers

commit 2bbb5f8c015742b2480cf9b42285d1e0d15f1b15
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jan 7 21:04:27 2024 +0000

    Link to the SVG file

commit 85dfbd35da26bc8658d993303951a070fa40ae83
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jan 7 21:03:00 2024 +0000

    Markups on the age picker post

commit a86428e01b5f13a480e4f14b5ea4b97427670013
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jan 7 20:47:15 2024 +0000

    Make sure you indent this example

commit 437f5ab67759edda01cf614d47ebba59628df5a2
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jan 7 18:17:47 2024 +0000

    First draft of the SVG post

commit 3b96b49efddf02ffcda292be62a3d0bfe25a6ec9
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jan 7 12:45:46 2024 +0000

    Get the CSS working for the age picker

commit c8b09ad73cd4d89242a5b15568473a8590041cd4
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Jan 6 10:03:43 2024 +0000

    Pin the version of this image for now

commit 96719fa9785b5c018f425d9d553009027641c485
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Jan 6 09:21:39 2024 +0000

    Fix a broken HTML entity

commit 0898d6e5c283d560bd08efbe0281bea5dddbc8f0
Author: GitHub Actions on behalf of Alex Chan <githubactions@alexwlchan.net>
Date:   Tue Jan 2 19:10:51 2024 +0000

    Publish new post dog-or-bat.md

commit 35a0b5a28a946c93fff0df551ab950c336eff8a2
Merge: 399f218f 08ab22fa
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Jan 2 19:07:32 2024 +0000

    Merge pull request #718 from alexwlchan/dog-or-bat

    Add a quick 'dog or bat' post

commit 08ab22fa13baae2c7315c783454e9659b8d3c364
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Jan 2 19:03:16 2024 +0000

    Add a quick 'dog or bat' post

commit 399f218fdfc898c36e9eb0c69e3a6fd64ff88695
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Dec 31 17:43:55 2023 +0000

    Remove some invalid YAML syntax

commit 39064988cfd4a2a1e8184049e43d2700d6a89a59
Merge: 9f3d3a5c 333784ee
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Dec 31 17:42:32 2023 +0000

    Merge pull request #717 from alexwlchan/check-for-color-profile-in-src

    Continue converting existing images to sRGB

commit 333784ee1f567fcf7d877a88d74c47f0b52faf12
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Dec 31 17:36:42 2023 +0000

    Continue converting existing images to sRGB

commit 9f3d3a5cb6a4dabd80a35ae55ebe75fc16642512
Merge: dffdf1d3 1daf6e40
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Dec 31 15:59:50 2023 +0000

    Merge pull request #716 from alexwlchan/check-for-color-profile-in-src

    Fix the check for non-sRGB colour profiles

commit 1daf6e406d344673a8f19654a18fb96e723e9459
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Dec 31 15:58:06 2023 +0000

    Convert a bunch more images to have sRGB colour profiles

commit e7b4f47ae430a0b48bfe0c768e95b77c92ed8506
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Dec 31 15:51:58 2023 +0000

    Fix the syntax for a Ruby set

commit d7a0d1f3323fa0c18a501eb9244394e3510c1b00
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Dec 31 08:34:17 2023 +0000

    Make RuboCop happy

commit 24873661b331e4b650c4ef4ed34539a45b603d91
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Dec 31 08:32:34 2023 +0000

    Add a list of approved profiles

commit a36fa0c26e509b344a6f1bf5e1891b253766700d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Dec 31 08:31:46 2023 +0000

    Use the new profile checking function in linter.rb

commit 22cda74bcbe09a4a5b5bd7359be6cd6d449e4c8b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Dec 31 08:27:52 2023 +0000

    Test the function for finding colour profiles

commit 2c705bc4ea824c62b6d032cf839df51d9f941a0b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Dec 31 00:37:07 2023 +0000

    Keep adding sRGB profiles to images

commit b6dadcedb65e163ad3e97a68d6470dfe762869d2
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Dec 31 00:30:09 2023 +0000

    Remove some old debugging code

commit 880fc3977ad6d68ff49ca7f963682621010af7ad
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Dec 31 00:22:12 2023 +0000

    Replace the '2023 in reading' card

commit d67a195a472d96f4e48641a85dfbd4f7f1cf51cc
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Dec 31 00:21:44 2023 +0000

    Remember to check all the images in the folder

commit dffdf1d3546e74de440ef8fa15ecb13402074ac1
Merge: dbb8b74d d3aab6f1
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Dec 31 00:20:12 2023 +0000

    Merge pull request #715 from alexwlchan/more-merge-logic

    Continue fiddling with the auto-merge logic

commit d3aab6f130e9d54599329a5b3ff8bd225fdffa4c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Dec 31 00:17:37 2023 +0000

    Remember to skip itself

commit 131d4d994447b129f2d81db0932f6031e386361f
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Dec 31 00:13:39 2023 +0000

    Use an API token to get higher rate limits

commit cfd36c142bfb3ba8aa1d40261e9a943357c0c85c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Dec 31 00:09:37 2023 +0000

    Highlight errors; make rubocop happy

commit 6f7a8fe4110544f12a3c4d56559046483e5ff413
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Dec 31 00:07:33 2023 +0000

    Fix this variable name

commit f4f33deed06b3dae2032a3bb73a006757ce10b6a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Dec 31 00:05:53 2023 +0000

    This should be a list, not a set

commit 8e80a6135e72c45358c64f0fb5e46f918e02fc29
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Dec 31 00:03:46 2023 +0000

    We can abort as soon as a check run fails

commit 11dab76869794387a318da2c12b52d7671edce98
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Dec 30 23:59:30 2023 +0000

    Don't look for the Git commit until check runs are done

commit 4c0108e9a6e467e6c1fce39699704a687bc9d6a2
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Dec 30 23:59:04 2023 +0000

    Add another rubocop failure to catch

commit f9987b1197e72646ebfa52e03eeca962f37f3aa3
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Dec 30 23:57:29 2023 +0000

    Log the name of the succeeded checks

commit f49dcb92cc54324df01f441bf8c5682637f7fb55
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Dec 30 23:56:59 2023 +0000

    You do need to pass the branch name here

commit dbb8b74d361486f8b2651b5cf8bd106aa3a67580
Merge: 11c99503 4c45f3a5
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Dec 30 23:54:31 2023 +0000

    Merge pull request #714 from alexwlchan/tidy-up-merge-logic

    Continue fiddling with "auto-merge PR" logic

commit 4c45f3a55739dace3f0394d0a9cb1444e2f16692
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Dec 30 23:54:21 2023 +0000

    We can fail immediately if another check fails

commit 7266d151d5180f72826b58c15cd0b67d61a7af1b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Dec 30 23:52:43 2023 +0000

    Split merging the pull requests into a separate action

commit 18dacd335054ce0fd8715011138fe14808ddf9fd
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Dec 30 23:48:14 2023 +0000

    Print to sys.stderr rather than sys.exit

    This ensures messages appear in the right order, hopefully

commit ec31c48d1e00f01beae7bb3d239825d5b0eea240
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Dec 30 23:44:07 2023 +0000

    Uncomment the rest of this workflow

commit 1215bc21334b464b4b7aa71f1097d7b3591e37a9
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Dec 30 23:43:52 2023 +0000

    Tidy up the script with black and linting

commit 95641b9d5be24f357db746cf01757456a9b2775a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Dec 30 23:40:45 2023 +0000

    This is a plural, not a singular

commit 308e5c7c816f10e495fd7efe663a92b04c2016dd
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Dec 30 23:39:26 2023 +0000

    Look in the right place for this

commit 64d1ffab8407e614ce6d1db0a1f628f5c861b56e
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Dec 30 23:35:48 2023 +0000

    Okay, I know what I want now

commit 83ca576913f20276ac76ee348a33845395dc6a60
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Dec 30 23:34:04 2023 +0000

    I want HEAD not HEAD^1

commit cf37a999b3fcee02ce9e17053308e68f65bb0a51
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Dec 30 23:32:36 2023 +0000

    Fix this variable name

commit 0a276ed6640ac253fa24992058fd7ddd14881743
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Dec 30 23:31:30 2023 +0000

    just log everything

commit d626a080a146122ed9222de15b4eb243f2ad43f1
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Dec 30 23:29:30 2023 +0000

    What if we go back a commit?

commit 02b7821ccb20b9230043d10e09a41319394bc4d2
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Dec 30 23:27:02 2023 +0000

    Actually log the right commit ID

commit 08403042e72b45429a30b81fd713f3c5063013bf
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Dec 30 23:25:11 2023 +0000

    Get the repr of these two values

commit 8d1617ec7bf3ee0126a4c63bba20aa29a2ead0bd
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Dec 30 23:23:25 2023 +0000

    This should be an f-string

commit 5ca873aba63a37d0cfc5ffdfe50ca1456a6add9f
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Dec 30 23:21:54 2023 +0000

    What commit is currently running?

commit de8a3369eebc598af23774bc24729e72b66acab1
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Dec 30 23:16:02 2023 +0000

    Add another error to upset rubocop

commit b0f2fbafbd0899e85db9f7d9f83f59bae16cec69
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Dec 30 23:15:27 2023 +0000

    Now check for other check runs

commit bd77ec74d1a9a439431175407ed98c8a12c8c35c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Dec 30 23:09:58 2023 +0000

    Another new commit to trigger builds in quick succession

commit 6f64e8fa7d724b7b8bdcdd84034cb377bd1ac37f
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Dec 30 23:09:31 2023 +0000

    This should be check_output

commit 4c29a39fd222f60b4ede98d7e81b2066d8794896
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Dec 30 23:08:17 2023 +0000

    Trigger a new build by dropping this f-string

commit 9bdfaeb5fa9e99743f481bc154ce88f04dab309b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Dec 30 23:07:58 2023 +0000

    Retrieve the current branch name and commit ID

commit 0d68d7b2221f72fe744abc023fb7f696a402b8d1
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Dec 30 23:02:05 2023 +0000

    We do need to check out the repo

commit 23dc61b5f8d989a64418a839163ebd4bbba2ef9b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Dec 30 23:00:49 2023 +0000

    Is the file there??

commit 68f17025acbbe28c39a800be4530baf6ecaa15ca
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Dec 30 22:59:20 2023 +0000

    Revert "These don't run unless Ruby/plugin code changes, so always run them"

    c08dc42cd910b9133d409fea13bf876298c6b15c

commit 86714dfebca73fc6044389b6dc248dd06a8f9119
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Dec 30 22:59:11 2023 +0000

    Start rewriting the merging logic in Python

commit 11c995031dd406c31a596c869ba4ef88e7967c38
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Dec 30 22:56:41 2023 +0000

    Revert "Deliberately introduce an error that will upset rubocop"

    eef6e0fb58b6c291e2aafa315a8757d4057de2da

commit 8cf9f72573a625f1f95c21485f8c6ce917228ebe
Merge: 52626f23 c08dc42c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Dec 30 22:55:43 2023 +0000

    Merge pull request #713 from alexwlchan/dont-merge-unless-everything-passing

    Deliberately introduce an error that will upset rubocop

commit c08dc42cd910b9133d409fea13bf876298c6b15c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Dec 30 22:53:56 2023 +0000

    These don't run unless Ruby/plugin code changes, so always run them

commit eef6e0fb58b6c291e2aafa315a8757d4057de2da
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Dec 30 22:50:52 2023 +0000

    Deliberately introduce an error that will upset rubocop

commit 52626f23f3b2ce6c39203780eaa2a9705e3886e9
Author: GitHub Actions on behalf of Alex Chan <githubactions@alexwlchan.net>
Date:   Sat Dec 30 17:10:51 2023 +0000

    Publish new post 2023-in-reading.md

commit 7e12d5b12904cb33fd92f9c080d41e5256e56d0f
Merge: d0a5d1a9 13f1ad45
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Dec 30 17:08:48 2023 +0000

    Merge pull request #712 from alexwlchan/2023-in-reading

    Add my favourite books from 2023 post

commit 13f1ad45221b126999337ab2bd77cf3d6af33d5a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Dec 30 17:06:23 2023 +0000

    Finish my 2023 in reading post

commit 5d8d40b648b38d7b43176647f7f4a4bf0f82eb44
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Dec 30 15:01:50 2023 +0000

    Tidy up the markup in this post

commit 968f04d1ec2df96f0d52ac09534f21b9876b1a02
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Dec 30 13:04:51 2023 +0000

    Finish the first draft of "2023 in reading"

commit 36337bdb049d42aaeba2b33e9e72241e18b8b10a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Dec 30 10:36:35 2023 +0000

    Start fleshing out the reviews

commit fb98ddf1821347136d5d3f6714d87d45501d78d3
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Dec 30 10:10:58 2023 +0000

    Align all the styles

commit 6d75dcddd6ca39288f0ce109042b40802f3f456b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Dec 30 09:51:55 2023 +0000

    Set out the skeleton of my "2023 in reading" post

commit d0a5d1a943cbe1d76482ad24b73a65ed6cfd5eda
Merge: afb7c3bd 3236cd8e
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Dec 30 14:04:50 2023 +0000

    Merge pull request #710 from alexwlchan/bounding-box

    Allow specifying the `height` of a picture

commit 3236cd8e01952e88fc533aa4e1e84a37e517472c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Dec 30 14:04:43 2023 +0000

    Fix some RuboCop offences

commit dd9d097e178d57683c19830965eb554117516b06
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Dec 30 14:02:15 2023 +0000

    Allow specifying the `height` of a picture

commit afb7c3bdf5baf3fc10150c51bb1bced56d32d4b6
Merge: 6af99cb8 e1d7fe7a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Dec 30 13:51:42 2023 +0000

    Merge pull request #709 from alexwlchan/no-px-on-width

    Remove the 'px' suffix from the 'width' parameter on pictures

commit e1d7fe7a06ffb870ed09393bf006ccf3c3385b53
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Dec 30 13:49:06 2023 +0000

    Remove the 'px' suffix from the 'width' parameter on pictures

commit 6af99cb87d694215be3c708ca002960b8697e3c3
Merge: d6afe449 ddda7914
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Dec 30 13:47:52 2023 +0000

    Merge pull request #708 from alexwlchan/tidy-up-book-posts

    Tidy up the HTML in my end of year book posts

commit ddda791433c64e7804ed5bb47a3683d4fd919d5a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Dec 30 13:44:13 2023 +0000

    We can also do away with the <div class="book_cover"> wrapper

commit 53853cc6a19c435f56a8cc5ffd593f3acd4c60aa
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Dec 30 13:40:33 2023 +0000

    We can strip away the <div class="heading">

commit 0a4aa07f34ab600f4897365d3592a7034386961a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Dec 30 13:37:57 2023 +0000

    I can write the reviews in Markdown, not HTML

commit f0529860f35e66c9523576d77e0b85b89f8dd9f7
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Dec 30 13:29:52 2023 +0000

    Tidy up the CSS at the top of this post

commit d6afe449f2f3a1f4ddb76892ecf42e9cb169a61a
Author: GitHub Actions on behalf of Alex Chan <githubactions@alexwlchan.net>
Date:   Fri Dec 29 07:46:34 2023 +0000

    Publish new post obsidian-open-note.md

commit 5bd6cddb5175e107b7196cca6075defed37b2ae1
Merge: ee86cbfc 30e3c1e4
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Dec 29 07:44:19 2023 +0000

    Merge pull request #706 from alexwlchan/obsidian-get-frontmost-window

    Getting the path to the note I have open in Obsidian

commit 30e3c1e4c87d378fdbd065b1b4c0239d28eb7cd9
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Dec 29 07:39:37 2023 +0000

    Make a couple of tweaks

commit 8a27ae13dad5b67db432041836c5311f07d76527
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Dec 29 00:09:04 2023 +0000

    Make this error message more useful

commit b58619dedf3f4c018d1584067958b3de09f31a62
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Dec 29 00:08:54 2023 +0000

    Add the first draft of the Obsidian post

commit ee86cbfc25f98703885661aeb0cb5c7548f6c290
Author: GitHub Actions on behalf of Alex Chan <githubactions@alexwlchan.net>
Date:   Tue Dec 19 10:33:36 2023 +0000

    Publish new post fish-venv.md

commit 6e3ef6c515bfce6207348b31026a1909b7931354
Merge: 696e163c 8420246c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Dec 19 10:27:59 2023 +0000

    Merge pull request #705 from alexwlchan/fish-venv

    New post: "Setting up Fish to make virtualenv easier"

commit 8420246cab8041aae4008b1d3967f99a7b92f405
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Dec 19 10:25:45 2023 +0000

    Pin the version of rubocop to avoid lint issues

commit 67f9b115f84f9477a797d1b10a1b94ecf9f11e47
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Dec 19 09:47:55 2023 +0000

    Add some .inspect markers

commit 9f553757425e0af85f9155a376e8c6f2026d6ec0
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Dec 19 09:44:48 2023 +0000

    Add more debugging

commit 810128df44dddd8cc55639fd54f36fe0cd73fd82
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Dec 19 09:42:26 2023 +0000

    Log what the actual layout is in this lint error

commit 1e8c948a23864e48a59a5d058afaffd049c06e89
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Dec 19 09:24:01 2023 +0000

    Add imagemagick-webp

commit 82e0870b151842a06fbdcb0733eb66d292e9dce9
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Dec 19 09:19:33 2023 +0000

    Apparently we need to install imagemagick-jpeg as a separate plugin

commit 0537ceeb871467212226001784dbf099a354379d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Dec 19 09:01:34 2023 +0000

    Log the ImageMagick version here

commit 1870e7a349d2562f4268ee067baa713032f86d3b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Dec 19 08:03:00 2023 +0000

    Make sure this Shell.execute call succeeded

commit d5e17eac2b8ebd427f82f491a277f2ad8a43064f
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Dec 19 07:27:15 2023 +0000

    Fix some issues flagged by the newest rubocop version

commit d3d69516e15c705cfb4c629b13d99cd377f66690
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Dec 19 07:07:57 2023 +0000

    few more edits

commit e06dca3db07ab4b9680bf04d962e324c1746c817
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Dec 19 07:01:34 2023 +0000

    Continue tweaking the Fish venv code

commit 764716b73ea24628667933c09ab02dfe5300778a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Dec 18 22:59:46 2023 +0000

    First draft of fish-venv

commit bb489436469b4f8847c5eb1c97c8c30a3e05a0c2
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Dec 18 22:59:40 2023 +0000

    Add a crude mechanism for adding attribution to card images

commit 696e163c1043af54266113531c6ff64cc87323af
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Dec 19 07:40:21 2023 +0000

    Remove a probably-redundant check for transparent pixels

commit c194ce7d6ecb3966ee0fa167b92d2a409aa74a2f
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Dec 14 11:28:40 2023 +0000

    Make sure <main> fills the width

commit 0312d7ffd9df02919ca558d084a207e9f0a19b56
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Dec 12 14:38:34 2023 +0000

    Make the footer appear at a consistent place across pages

commit 752e0bffd8d9fb17b3dcba8e418c635e8d4d9b4e
Author: GitHub Actions on behalf of Alex Chan <githubactions@alexwlchan.net>
Date:   Thu Dec 7 20:53:09 2023 +0000

    Publish new post mechanize-ssl.md

commit a6c991cc49d7830e1500939a4e57ba36b26b496e
Merge: 044852ab b17d184e
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Dec 7 20:50:55 2023 +0000

    Merge pull request #704 from alexwlchan/mechanize-and-ssl

    Add a quick post about mechanize and SSL

commit b17d184e9c8b6f32de8b41da3171dc24cf356989
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Dec 7 20:48:35 2023 +0000

    Add a quick post about mechanize and SSL

commit 044852abc0abe13e327b6528f3d2a8d1732fe00d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Nov 19 03:20:13 2023 -0300

    Rearrange the `assets` directory

    [skip ci]

commit 563fe77d2dfbbbc222e542693ee59e703bdc9a9f
Author: GitHub Actions on behalf of Alex Chan <githubactions@alexwlchan.net>
Date:   Fri Oct 20 23:08:51 2023 +0000

    Publish new post forgetful-fish.md

commit 26325cc120dddde88d2588325908886b34596b92
Merge: b9769ef0 283e5d0d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Oct 21 00:06:04 2023 +0100

    Merge pull request #702 from alexwlchan/forgetful-fish

    New post: Making the fish shell more forgetful

commit 283e5d0d0597be91fed2100c8c476335dcbabeca
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Oct 21 00:02:58 2023 +0100

    Fix a bug in the picture plugin

commit b396eda1d2b1114b53361122d6f8f9ca31d88784
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Oct 21 00:02:52 2023 +0100

    Add alt text

commit 2209dfa2d4669b48219eb0dd5b6e6cea8a2e5743
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Oct 20 23:55:30 2023 +0100

    Add my fish forgetfulness post

commit b9769ef053f1b18da7c475987d9f456084850c33
Author: GitHub Actions on behalf of Alex Chan <githubactions@alexwlchan.net>
Date:   Fri Oct 20 09:16:16 2023 +0000

    Publish new post hyperfocus-and-hobbies.md

commit 74eca896380cd992a7eb0011c93ec457bb4298e0
Merge: ce0a183e a434f090
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Oct 20 10:12:57 2023 +0100

    Merge pull request #701 from alexwlchan/hyperfocus-and-hobbies

    Link to the hyperfocus and hobbies story

commit beccde3c1d691deae8f062bc4be29b462640f3ad
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Oct 19 22:47:01 2023 +0100

    skeleton of the forgetful fish post

commit 4876d8f5635f01930e623d615c7b10d8b753a53c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Oct 19 22:46:51 2023 +0100

    Fix my 'search tags' script for YAML front matter

commit a434f09032bd81be067bbdd5e623f317dc932f26
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Oct 19 22:20:25 2023 +0100

    Link to the hyperfocus and hobbies story

commit 51440183f104d048181fb19aff9680ad502951f3
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Oct 19 22:20:09 2023 +0100

    Tweak the eggbox posts

commit ce0a183ea26675485bdb1975350b1b330671b4ad
Author: GitHub Actions on behalf of Alex Chan <githubactions@alexwlchan.net>
Date:   Sun Oct 15 16:12:21 2023 +0000

    Publish new post finding-big-photos.md

commit f12f0eebab688806856e56cd598a71ea603b7fda
Merge: 5388b5d1 d9376f55
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Oct 15 17:09:41 2023 +0100

    Merge pull request #700 from alexwlchan/photo-sizes

    Add a quick post about finding big photos

commit d9376f555a668c63942b73835f1eafde199493e8
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Oct 15 17:06:23 2023 +0100

    Add a quick post about finding big photos

commit 5388b5d113a8256ac8151e95ef06ebde1b7d06a7
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Oct 15 11:09:19 2023 +0100

    Switch to main as the main branch

commit 4ef93c8de47ca7a77edd7cdfdb6bdcc9eb09712a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Oct 15 10:58:52 2023 +0100

    Update 2023-05-25-managing-albums-in-photos.md

commit 30df9f98afa97b986eefebf07e8efb49f2bf785e
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Oct 15 10:48:06 2023 +0100

    Fix the capitalisation of 'Fastmail'

commit e70a7253b09b3597e6602db665cdb7e15d3b725b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Oct 10 23:34:18 2023 +0100

    make the homepage less obviously out-of-date

commit d84d63f3443d829eec52583adfa4159b364b4419
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Oct 6 15:37:41 2023 +0100

    Add a Slovenia road sign for testing stuff

commit a852fd296c9510b8f3d7c4bbf429072c9670f1b3
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Sep 28 08:42:19 2023 +0100

    Fix the <img> tag in the README

    Make sure it actually renders on GitHub!

commit b23d27742c3b4bd1e13148501aa434d5d2e41de5
Merge: 581fd263 e344098c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Sep 28 03:23:30 2023 +0200

    Merge pull request #698 from alexwlchan/add-time-element

    Use the <time> element for timestamps on posts

commit 581fd26335d4dea9e71aa9a940d47c6b3528113c
Author: GitHub Actions on behalf of Alex Chan <githubactions@alexwlchan.net>
Date:   Thu Sep 28 01:21:06 2023 +0000

    Publish new post spotting-spam-in-our-cloudfront-logs.md

commit e344098cd7b19efb2721bb4ec5a51bf393d382fd
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Sep 28 02:19:34 2023 +0100

    Use the <time> element for timestamps on posts

    According to the MDN documentation, the "24 September 2023" format I'm
    using as the child text content isn't a valid date format (all the valid
    formats are numeric, so maybe it's to do with internationalisation?).

    I suspect search engines already know how to parse this, but it seems
    semantically nice to provide the date in a machine-readable format here.

commit 664903b892fc2df748aa3208e41819948ff73aca
Merge: 161b91f3 87713e9d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Sep 28 03:18:15 2023 +0200

    Merge pull request #697 from alexwlchan/spam-detection

    Add a post about spam analysis in CloudFront

commit 87713e9dfba79de3992abce2f97e78f13ddffe72
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Sep 28 02:14:42 2023 +0100

    Markups on the spam post

commit fb1ee5b8fe1504ef698256a953d4eb3040261e00
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Sep 27 13:47:17 2023 +0100

    Add the first post about CloudFront

commit 161b91f3d50ba057be52a4950b9b1727bc591cba
Author: GitHub Actions on behalf of Alex Chan <githubactions@alexwlchan.net>
Date:   Sun Sep 24 16:31:02 2023 +0000

    Publish new post adding-watch-locations.md

commit e37bae3e037acff070e4d7cebcd517a166b51a42
Merge: 8dd62243 185b0698
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Sep 24 18:27:18 2023 +0200

    Merge pull request #695 from alexwlchan/watch-locations

    Adding locations to my photos from my Apple Watch workouts

commit 185b0698bf59249e3c3a4d206778be357cb8e0c3
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Sep 24 17:23:54 2023 +0100

    fix the tag front matter

commit 6002ddf0387c717c7f7197fccc36e247d66d1355
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Sep 24 17:20:00 2023 +0100

    A couple of markups on the photo post

commit e510bd86b56273591594127ca24c2ae122549ee7
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Sep 24 15:50:55 2023 +0100

    couple of edits

commit b5261e8b253b6c3973ef5a102418fb29215740b7
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Sep 24 15:48:36 2023 +0100

    add alt text

commit 87468db1da63a4478e1b553e86157787732f5e60
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Sep 24 15:46:09 2023 +0100

    more watch location stuff

commit 25d8a19b62190d81c9e9752c4c78ad4fb403f5c0
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Sep 24 10:25:27 2023 +0100

    more watch location stuff

commit 8dd622430c0f9d491c16fda5a7040826fb2726ac
Merge: 435d7d6e baf196c8
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Sep 23 21:45:13 2023 +0200

    Merge pull request #694 from alexwlchan/tags-as-a-list

    Convert to using YAML lists for tags

commit 435d7d6eeb4016d7feaba7db9918334009892d54
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Sep 23 20:41:45 2023 +0100

    remove some trailing whitespace for rubocop

commit baf196c8fac3aa0137a9ab4f01d5c50a4acf4883
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Sep 23 20:40:44 2023 +0100

    Convert to using YAML lists for tags

    Jekyll will do the right thing with a space-delimited list, but this is
    the syntax I think of when I imagine lists in YAML, and it's how I do it
    on books.alexwlchan.net -- this makes the two sites more consistent.

commit 4f11fab11cf4dc2a90f37c9d99386efa374e9d56
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Sep 23 20:36:07 2023 +0100

    Fix another issue flagged by rubocop

commit 440c8666c60669b0195f9a128982833cb33ae96a
Merge: 8999d0be 1e6bc37f
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Sep 23 21:33:52 2023 +0200

    Merge pull request #693 from alexwlchan/more-consistent

    Copy across a couple of pieces from books.alexwlchan.net

commit 1e6bc37f797d7e13a1a0b71318c1a89d7162e2b9
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Sep 23 20:32:33 2023 +0100

    Fix an error flagged by rubocop

commit e484dfeffb85b3fd31ff4bfc1eea22e27a2c4e80
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Sep 23 20:29:40 2023 +0100

    Pull out a helpful named variable in the theming code

commit c2d48e26c1f41d46d152fe5e76ca69c7e84aacf0
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Sep 23 20:29:28 2023 +0100

    Remove an unused bit of the Makefile

commit 92f57df0b4b5b32ac2de2375a95e334f8f5e4589
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Sep 23 20:29:22 2023 +0100

    Make the server port a variable in the Makefile

commit d397a06ef2164039ea936a70d742f9a59d55618c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Sep 23 20:29:07 2023 +0100

    Add the skeleton of the post

commit 8999d0beb81bce0ac49217e467968fd5c4e6b266
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Sep 21 13:26:11 2023 +0100

    remove some now-dead redirects

commit 31bd1ba674405471da5701e2b5c2a8041237be2a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Sep 21 12:26:19 2023 +0100

    make this card actually have a 2:1 aspect ratio

commit 42d7bcab1f33e6e9d0cc4e24901880c6efe4353d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Sep 21 11:23:38 2023 +0100

    trigger a new build

commit 444e5658698a49e049059aaea51ce9e1ec8ec717
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Sep 20 08:23:27 2023 +0100

    change up this card

commit 5c46516c75a043fcb415e3c532a116915e4e03ca
Author: GitHub Actions on behalf of Alex Chan <githubactions@alexwlchan.net>
Date:   Wed Sep 20 07:12:55 2023 +0000

    Publish new post fare-wellcome-collection.md

commit 4018f0d8389e204ef00479613c796cae8a9a8962
Merge: 10f96a28 12ea1c85
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Sep 20 09:08:31 2023 +0200

    Merge pull request #692 from alexwlchan/leaving-wellcome

    Add my "leaving Wellcome" blog post

commit 12ea1c85dca5f54f12627d8c059c3e4fbbfac085
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Sep 20 08:04:39 2023 +0100

    this should be sRGB, not P3

commit a93a7bde2ebee39e1b2a3860561bc0a63293d65d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Sep 20 07:52:09 2023 +0100

    fix the aspect ratio on the card

commit cc8f7912675bfddac7649711ad090c902abc1f5d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Sep 20 07:46:29 2023 +0100

    Add my "leaving Wellcome" blog post

commit 10f96a28510da6a82f2c56126e144baa0cfc345b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Sep 19 22:43:37 2023 +0100

    Clarify that both vaults have the same folders

commit e623eedf08666fd5f4b21a3e8c4c5849c348302b
Author: GitHub Actions on behalf of Alex Chan <githubactions@alexwlchan.net>
Date:   Tue Sep 19 21:31:00 2023 +0000

    Publish new post obsidian-setup.md

commit da6ccfc5decd92fdb485085b15c08f8268e04d6b
Merge: 993e2a93 79dc26b0
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Sep 19 23:28:23 2023 +0200

    Merge pull request #691 from alexwlchan/obsidian

    Add a post about my Obsidian vault setup

commit 79dc26b047a7cf5dc4254025a0ece6f48e1c1db1
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Sep 19 22:25:43 2023 +0100

    fix the front matter format

commit e5aaea0296e66bd792cb6cae9fd89388984374b5
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Sep 19 22:03:01 2023 +0100

    Remember to add a missing image

commit 1d82b44f01ee635ddfe223f9bb8b4193d5619e02
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Sep 19 21:45:07 2023 +0100

    Add a post about my Obsidian vault setup

commit 993e2a93cad93658ac642480a0f0130e0f2605d6
Merge: 72c7ce25 34199252
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Sep 10 18:45:44 2023 +0100

    Merge pull request #690 from alexwlchan/use-new-picture-plugin

    Replace remaining uses of `srcset` with the `{% picture %}` plugin

commit 3419925239f45885c3829b25d3a1c530ac010aa9
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Sep 10 18:26:49 2023 +0100

    Replace remaining uses of `srcset` with the `{% picture %}` plugin

    Before I created my custom <picture> plugin [1], I had a script that
    would create 1x/2x variants of an image and insert an HTML snippet
    with the `srcset` attribute.

    This patch replaces all remaining uses of `srcset` for images with
    the new plugin, which makes everything more consistent and gets the
    nice benefits of modern image formats and smaller file sizes.

    [1]: https://alexwlchan.net/2023/picture-plugin/

commit 72c7ce2561c48f92fc1ad2ca1ad9d5a2507a8d23
Merge: 269738f0 eb745349
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Sep 10 18:35:44 2023 +0100

    Merge pull request #689 from alexwlchan/use-setlength

    Use \setlength instead of \renewcommand to set \ULdepth

commit eb745349f0f2bb62eb7dbf039c849e39cfb649cf
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Sep 10 18:32:33 2023 +0100

    Use \setlength instead of \renewcommand to set \ULdepth

    I've changed this in both the source code embedded in the post, and in
    the standalone zip file that contains all the source files.

    I've tested it by regenerating all the source files using the examples
    in that zip.

commit 269738f0d8151e7c7416a8d712547714a9e15d16
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Sep 4 19:51:04 2023 +0100

    Update 2023-07-28-cloudfront-logs.md

commit 4d2b7d42c707da95da64eb8798ec7c3d77528124
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Aug 26 14:46:25 2023 +0100

    link to my mastodon from /contact

commit 62f5f54cf499adc0b759e740c129181a3f1c8169
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Aug 26 13:21:55 2023 +0100

    stick mastodon in the footer

commit 739bdf38120a3034bfb9601166162145b1a88380
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Aug 26 13:10:05 2023 +0100

    update the footer link

commit baa417302d021e3cb12f8eed488e497872412d34
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Aug 26 12:32:47 2023 +0100

    skip the social.alexwlchan.net redirects in the linter

commit 6d57cc4577740003d807b6a7fe6a1acf2cf946b1
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Aug 26 12:28:34 2023 +0100

    Add some Masto.host redirects

commit 877857f01658c73c01364621e98631c08d4ad05d
Author: GitHub Actions on behalf of Alex Chan <githubactions@alexwlchan.net>
Date:   Sat Aug 26 09:22:24 2023 +0000

    Publish new post iam-keys.md

commit 1b8e155e2e975f0311867d5bf0600419e146c72d
Merge: 21419c56 92b0334b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Aug 26 10:19:20 2023 +0100

    Merge pull request #688 from alexwlchan/add-iam-keys-post

    Add a quick post about IAM keys

commit 92b0334b3f5ffc55814e1ce38ec2d908a53f8609
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Aug 26 10:16:10 2023 +0100

    Add a quick post about IAM keys

commit 21419c56bb1e78cff0503b1e5e28a07dbea3e38d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Aug 19 11:26:26 2023 +0100

    Add a link to my LRUG talk

commit 1b7bd7aa17fdb2e2405fef90dc0b169fc0a2973d
Author: GitHub Actions on behalf of Alex Chan <githubactions@alexwlchan.net>
Date:   Sat Aug 19 07:14:32 2023 +0000

    Publish new post hester.md

commit 33cc2ad966ebdc1df0e01f832ef769cd2dec7406
Merge: 3151ed64 9d45cf30
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Aug 19 08:11:44 2023 +0100

    Merge pull request #687 from alexwlchan/hester

    A plaque for Hester

commit 9d45cf30015a8fea38cd59e879b27485c02ed416
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Aug 19 08:08:05 2023 +0100

    no mailing list… for now

commit 76d8ba0b8405c5278c15b1d46a44c00583887f01
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Aug 18 21:51:35 2023 +0100

    get the hester post done

commit f7ab61bd2ec66442db7c720a0033fd25f9ececa4
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Aug 18 21:24:58 2023 +0100

    add a basic mailing list form

commit 8686e9cbd6e1bab1f3d70ffcb13c4f90c1a600df
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Aug 18 09:04:39 2023 +0100

    Revert "get an instagram story embed working, kinda"

    07b8f51b75c6f102f825ac3aca00fb8da7ee84a8

commit 0018013559da48292e617652ff83efaa2a95645b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jul 21 19:24:10 2023 +0100

    get an instagram story embed working, kinda

commit 2b261c625bfdeee09987ee86891efa8f66e43ad2
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Jul 19 20:49:28 2023 +0100

    tweaks

commit 6c9d5d78329213037f516f32d690de132077257a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Jul 19 20:44:55 2023 +0100

    start the hester post

commit 3151ed6419d0aff7202bad7bc3d50dc52d0227bb
Author: GitHub Actions on behalf of Alex Chan <githubactions@alexwlchan.net>
Date:   Fri Aug 18 08:04:31 2023 +0000

    Publish new post tag-iac-resources.md

commit 784723b1aa04b983bd91a3d8ebbd6dffee3b7420
Merge: 699750bd 224f931e
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Aug 18 09:00:52 2023 +0100

    Merge pull request #685 from alexwlchan/tag-terraform-resources

    Tag your infrastructure-as-code resources with a link to their definitions

commit 224f931e6dbc1b6a3a0037225e14bea2dd29a800
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Aug 18 08:57:13 2023 +0100

    tweak the wording a little

commit 33b59316b18fe6e4e2f7548b79f1809a97013ca7
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Aug 18 08:54:48 2023 +0100

    remove this post from the archives

commit fc125c7c7b6342ff2ddb08e987875d50d6efc825
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Aug 18 08:54:43 2023 +0100

    Add a post about tagging IaC resources

commit 699750bd7dd4ec1fbd05fe33f8a456079e36110b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Aug 11 21:55:15 2023 +0100

    fix a couple of redirects

commit 7516d7c932662a088e26678c27110abec1a2116c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Aug 9 22:29:34 2023 +0100

    add a couple more fields

commit a990e39d2a8ec964c8b56288d8d21293f9f8e733
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Aug 9 22:29:29 2023 +0100

    remove the wellcome email address

commit 03124262cba8010c10de0483edfd0f7507464348
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Aug 2 12:01:17 2023 +0100

    add a missing 'it'

commit 37e92e6346cb8e00442f205e3672f64ebf70e4e4
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Aug 1 19:09:02 2023 +0100

    fix a couple of small mistakes

commit 9388a587a3a3a9bcc38edc268cd8a381d0501704
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jul 28 22:05:48 2023 +0100

    add the screenshot styles, use new images

commit 45e15190e83d96c498dad9f39b8ec4a702f13e21
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jul 28 21:56:48 2023 +0100

    add a v old asset

commit a325886bbe54c699f647a6727bb4ec8e9f8ef1ae
Author: GitHub Actions on behalf of Alex Chan <githubactions@alexwlchan.net>
Date:   Fri Jul 28 05:13:02 2023 +0000

    Publish new post cloudfront-logs.md

commit b5185aa65661474cfc33ee2c95ac09b8f7695ade
Merge: e0a9c98c 2c73bc23
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jul 28 06:10:29 2023 +0100

    Merge pull request #684 from alexwlchan/cloudfront

    Add a post about CloudFront logs

commit 2c73bc234dbe58a1c07d3dfc0b53a90e49236f12
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jul 28 06:07:08 2023 +0100

    tweak

commit 3b38fa05d454daa7346082319cadabaeef6b941a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jul 28 06:06:43 2023 +0100

    more edits on the CloudFront logs

commit 0011e436d3743d369a68af2d5910ffc28b1213b6
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Jul 27 23:00:09 2023 +0100

    keep tweaking the cf stuff

commit 0f9f5dca2bab1c8f4ea325edda9a6028dfb1aef8
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Jul 27 08:29:36 2023 +0100

    keep going on cf logs

commit 860ba7179bb1d8fe88cbddf14ca59c3f2385e55d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Jul 26 16:59:04 2023 +0100

    more cf stuff

commit 2ca87f3ec33e01ce78f4b1ed0d577cfe9201533c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Jul 25 23:43:40 2023 +0100

    add the code

commit 581b4fa948dea4c8046b34b33c638822e0bde30c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Jul 25 23:43:31 2023 +0100

    start the cf logs post

commit e0a9c98ca950ffe47af06e7265e951f1d5232580
Author: GitHub Actions on behalf of Alex Chan <githubactions@alexwlchan.net>
Date:   Wed Jul 26 16:07:14 2023 +0000

    Publish new post snake-walker.md

commit 4a51462fbcbabde6821ef64bc384be2b1ff797a6
Merge: 9d583a34 4435f39c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Jul 26 17:03:12 2023 +0100

    Merge pull request #683 from alexwlchan/walking

    Add a quick 'snake walker' post

commit 4435f39c952d4101efa6e16f0e5f3d111176b425
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Jul 26 16:59:13 2023 +0100

    Add a quick 'snake walker' post

commit 9d583a34c1ae0ec5407da61ae388151d95ca00de
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Jul 25 10:50:05 2023 +0100

    xml_escape, not escape

commit 48ea7da625a0820d2d106f8eb1003fcd25f885a1
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Jul 25 10:49:19 2023 +0100

    Revert "fix an escaping issue in the front matter"

    6de4b7c70b32b98e9c369e64ff1803e4e2afdc17

commit 2b709860b90933270a2f735336202a1675a1f9b7
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Jul 25 08:26:31 2023 +0100

    actually put that back

commit 98ec1ba47fd094da54a4bc0aaad3a9929c63fa02
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Jul 25 08:26:09 2023 +0100

    slightly adjust the eggboxes

commit f921a2ed56f09776a20db9f3df8f8ffdaac59589
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jul 21 07:54:36 2023 +0100

    add a quick note about lazy loading

commit 6de4b7c70b32b98e9c369e64ff1803e4e2afdc17
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Jul 18 13:45:33 2023 +0100

    fix an escaping issue in the front matter

commit affdd402ce9cd2ae1ea7874620ed82a6b7ee7a4a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Jul 18 07:14:10 2023 +0100

    convert another image to the new picture plugin

commit 1abb94ff8a7ab266ed3f397bea8051b30a345a56
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Jul 17 20:45:30 2023 +0100

    convert another post to the new picture plugin

commit 828948a46189678b0bbbcc2537fcccd32255844b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Jul 17 20:12:11 2023 +0100

    switch another post to the picture plugin

commit e0175c2ed32a4a825d2ca6225f7c2ce27087ab3b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Jul 17 12:24:42 2023 +0100

    fix some rubocop errors

commit 09c206f32b066107c60af6baf4877d91f476f636
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Jul 17 12:21:47 2023 +0100

    add a log for creating images

commit 959471d5c470382207df6a7246fd2179d97948a5
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Jul 17 12:19:54 2023 +0100

    let's add another picture tag

commit 35df651957550c7066c9834e5003850186589ffb
Merge: 4160ada5 74fd4f16
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Jul 17 07:50:55 2023 +0100

    Merge pull request #681 from alexwlchan/more-picture-plugin

    Convert a bunch of uses of Markdown image syntax to the picture plugin

commit 4160ada523f7d93f71a21c9325f76ed50abb0892
Merge: 80557cfc 9392fd95
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Jul 17 07:49:01 2023 +0100

    Merge pull request #682 from alexwlchan/update-projects-page

    Use the new picture plugin and card styles on the projects page

commit 74fd4f162e8e46f6808b61f01af4d207d537227d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Jul 17 07:48:00 2023 +0100

    fix more quoting issues

commit 064dc2e500ffae5f1f71bf4287c17e88b14f7090
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Jul 17 07:44:24 2023 +0100

    and some more

commit e7f4e3482ed772d712430f77a0e1576f9072c4ee
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Jul 17 07:43:54 2023 +0100

    fix some more quoting issues

commit 9392fd9514216519bd40b05cec3d26f394478e3c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Jul 17 07:43:05 2023 +0100

    finish converting the projects page to the picture tag

commit 204a477c605ca2c4465493b439aa77f04d87fd6f
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Jul 17 07:33:44 2023 +0100

    fix a quoting issue

commit ade86dee50171abc785cfe26c48efae8cd873fe3
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Jul 17 06:12:40 2023 +0100

    convert all the md image syntax to the picture plugin

commit f7068a6549555468d45375ec82518e9d3871e669
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Jul 17 05:41:42 2023 +0100

    switch a few more posts to the new picture plugin

commit df484769690d5ac50c58bc100b1105ddb767c2bc
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Jul 17 06:01:41 2023 +0100

    more to picture plugin

commit 0421732304a64eb80ca571629ab275a68d9f6696
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Jul 17 05:41:42 2023 +0100

    switch a few more posts to the new picture plugin

commit 26750a6740a919b99a06a0be7cf9e79da3d9afab
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Jul 17 03:49:14 2023 +0100

    this should be min, not fixed

commit 0b485fee3d9be82eddc39bed6d1e0c4b06537e8f
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Jul 17 03:45:37 2023 +0100

    convert book tracker also

commit e8459acdfe79500c505d85712b3026020e05e673
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Jul 17 03:43:35 2023 +0100

    tumblr is next

commit c7e31636b52a6f80a2e424a9cf74765d36c9cf6e
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Jul 17 03:04:49 2023 +0100

    tweak borders, add a catalogue search picture

commit e8785e8e05113efcbb847b41d7cfb0796b4690ed
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Jul 17 02:49:12 2023 +0100

    fix the border-radius on hover

commit 6a3dbc564abb8cbce890049f80d52f636643b5e4
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Jul 17 02:42:43 2023 +0100

    change the appearance of the 'fun' images

commit 80557cfca4f26b1953ef66c8e234ae1b4e00bd3b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Jul 17 03:32:25 2023 +0100

    fix the <picture> syntax

commit f37fead497a8de78d098c3f46fdf892ecb0a37fe
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Jul 17 03:29:11 2023 +0100

    I don't need the extra widths any more

commit 33e0f1a35a3a032346b671f85795c8e631d1027e
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Jul 17 03:32:29 2023 +0100

    Revert "Revert "Revert "delete in github also"""

    113618fb43ef339de1e1965997b44ad6b099befe

commit 113618fb43ef339de1e1965997b44ad6b099befe
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Jul 17 03:07:55 2023 +0100

    Revert "Revert "delete in github also""

    dbe24e2f5470072980f4f45ab830a140ec5e8071

commit e433ffb07eed6feb9232d74d10b89cf00e6949e3
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Jul 17 03:07:36 2023 +0100

    make sure we create at the right widths

commit 41fd2f8db0102270f374e111a3696d513a05d073
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jul 16 14:40:53 2023 +0100

    we can move these variables out of the enumerator

commit 50de3909b63a4717221b5b5324012e285c929016
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jul 16 13:25:44 2023 +0100

    tweak the social icons so they look good without css

commit 8ae9ad75a220072699a276dc0da4a9e28bd99a8d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jul 16 07:50:29 2023 +0100

    Fix twemoji images in the RSS feed

commit 2dfaa374c3c9e3c396ba64f1b7a1936e03ce626c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jul 16 07:48:50 2023 +0100

    remove trailing whitespace

commit 5e5d48bc4aa6758cf1dfc09b1e19e9767649ab3e
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jul 16 07:37:01 2023 +0100

    Add a comment about twemoji styles

commit 93a33f9eeb81efb6bb0c59e16977203cbb3db2d1
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jul 16 07:35:32 2023 +0100

    fix a couple of warnings from rubocop

commit 521cf29be2bbd1df26f5004309c752598f307c1b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jul 16 07:29:56 2023 +0100

    Add width/height attributes to twemoji images

commit 69586029b7a9b1ac4f87f80a3ba9a9eb7be64b62
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Jul 15 16:33:58 2023 +0100

    Update 2023-07-15-picture-plugin.md

commit d948136e0414b5c78baf77fa21cdc9633094eb4b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Jul 15 16:28:25 2023 +0100

    fix a bunch of lint errors in the twitter plugin

commit aac7ac2d8f67728d859a4542700022d31fc891c5
Author: GitHub Actions on behalf of Alex Chan <githubactions@alexwlchan.net>
Date:   Sat Jul 15 06:46:13 2023 +0000

    Publish new post picture-plugin.md

commit 8b9280a76422c3a3ebe48b2c56bddfba284fb907
Merge: be7056b0 619f33b9
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Jul 15 07:43:49 2023 +0100

    Merge pull request #680 from alexwlchan/picture-plugin-post

    Publish a post about my picture plugin

commit 619f33b9d5243aabe912f71b71e042e2e6da201d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Jul 15 07:37:39 2023 +0100

    add a proper conclusion

commit ed369edcbce431134563c941c5840b94997403dc
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jul 14 07:56:03 2023 +0100

    add a summary

commit 6e900f95be6018e0017a57134b5d8aeb45c39045
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Jul 13 23:03:08 2023 +0100

    add the picture plugin keynote file

commit cc292a1c657e14bf5821455c465f72abb27fcde5
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Jul 13 23:01:54 2023 +0100

    start writing the picture plugin post

commit abd4199e7d6a660cf92930dc3e9008e151f16906
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Jul 13 20:01:41 2023 +0100

    start writing my picture plugin post

commit be7056b065b50a88cf1ab14cdddd69347e542ce7
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jul 14 07:56:48 2023 +0100

    exclude another bot url

commit 62127926e9b75272b6b714aff42cfbd1b400d2df
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jul 14 07:56:15 2023 +0100

    add some missing redirects

commit 58892ae1f933fcf20b1b68a1a824585fb54e3854
Merge: 25c211cf d78e8b72
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Jul 13 20:23:33 2023 +0100

    Merge pull request #679 from alexwlchan/inline-tweet-pictures

    Just inline tweet avatars, don't serve a separate request

commit d78e8b72924fb7e3df72bde3d988a7fb4875dfb9
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Jul 13 20:19:55 2023 +0100

    Just inline tweet avatars, don't serve a separate request

commit 25c211cffc61f6f537cf333c6c4af9b91a4a0778
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Jul 13 13:13:10 2023 +0100

    Revert "bin all the avif images, rebuild"

    b00b750e4f2014d96f5cf2b66622e496a3f801db

commit dbe24e2f5470072980f4f45ab830a140ec5e8071
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Jul 13 13:13:09 2023 +0100

    Revert "delete in github also"

    2cac1cae5fddd3b3a0259ffe7b65e99ac75b68d3

commit 2cac1cae5fddd3b3a0259ffe7b65e99ac75b68d3
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Jul 13 12:31:18 2023 +0100

    delete in github also

commit b00b750e4f2014d96f5cf2b66622e496a3f801db
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Jul 13 12:23:55 2023 +0100

    bin all the avif images, rebuild

commit 1902e7ffdcdba6cc94ef2f452da91f891908279c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Jul 13 12:23:33 2023 +0100

    fix all the issues flagged by rubocop

commit 296d49e465afc3227cb257f7412d952149f7fb90
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Jul 13 12:22:37 2023 +0100

    check for missing transparent pixels

commit df1e333785e1f0a38ad17ef7cb3c9ea2c3e534f1
Merge: 5cd88f9a e6fa4b91
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Jul 13 12:17:30 2023 +0100

    Merge pull request #678 from alexwlchan/fix-avif

    Fix the AVIF support by running ImageMagick in a separate container

commit e6fa4b919ff4f0a42e65ac7ac9b67fec22f73f9b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Jul 13 12:17:02 2023 +0100

    remove some unwanted export lines

commit 53c1d71ac83457fa508262502abb75e2c862d0a6
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Jul 13 12:14:20 2023 +0100

    break out image creation as a separate process

commit 3de9584a82ac05f548d38cf0740bfe155aab88f7
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Jul 13 08:59:13 2023 +0100

    don't install imagemagick in the container

commit 01d0c9542e113008c5172dfcbce22a5b7b9917e4
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Jul 13 08:58:44 2023 +0100

    imagemagick container kinda works

commit 5ddbf020cc92e0000e925bfb302f08952699ce7d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Jul 13 08:34:16 2023 +0100

    Add a basic ImageMagick container

commit 5cd88f9a34c5197f7d41b21dda3e8c81dc00d9b9
Merge: 0638ec60 6ce6e2df
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Jul 8 17:27:08 2023 +0100

    Merge pull request #676 from alexwlchan/spy-for-spy

    Spy for spy

commit 6ce6e2dfd2df96d6a530a02aa89298005f2edaa1
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Jul 8 17:24:30 2023 +0100

    Update 2023-07-08-spy-for-spy.md

commit 1a379feb9b3b1303743de3419cfa3a4add77be92
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Jul 8 17:23:11 2023 +0100

    Update 2023-07-08-spy-for-spy.md

commit 7c5a922fc72d2314f00ee461b2b1e3f6bc5da350
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Jul 8 16:57:49 2023 +0100

    keep twiddling

commit 8e0a57ae9fdaa3cfdf58098a8c3316266c75d3ae
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Jul 8 16:28:27 2023 +0100

    keep fiddling with spy for spy

commit 0c6b4ac63f8e7345f86e1b50e0cb4b0c9aac8f63
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Jul 8 16:05:14 2023 +0100

    keep twiddling with the Spy for Spy post

commit 0638ec60e7732851f93f5d93de7f30971ae3d1da
Author: GitHub Actions on behalf of Alex Chan <githubactions@alexwlchan.net>
Date:   Mon Jul 3 13:43:20 2023 +0000

    Publish new post bedtime-for-ecs.md

commit 1b7b13cf1a00674461d0a9dd96f2c9afa6b0b318
Merge: bed5f680 ff0d0146
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Jul 3 14:39:37 2023 +0100

    Merge pull request #675 from alexwlchan/eventbridge-schedules

    Add a post about turning off ECS tasks overnight

commit ff0d0146f0c1c6ecdc63716e7b93b4c8417f011d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Jul 3 13:41:28 2023 +0100

    Add a post about turning off ECS tasks overnight

commit bed5f6802f1d907c04f57e0288e3008e330d6e93
Author: GitHub Actions on behalf of Alex Chan <githubactions@alexwlchan.net>
Date:   Wed Jun 28 16:38:26 2023 +0000

    Publish new post preserved-dates.md

commit 44e5e853d0d4a0d28c92bcd40f75494f25ac6bd2
Merge: 514ff1df a849eda5
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Jun 28 17:35:46 2023 +0100

    Merge pull request #674 from alexwlchan/preserved-dates

    Preserving Dates during JSON serialisation with vanilla JS

commit a849eda5736c0e9c2a35dd8f7971ee3f57e27bfc
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Jun 28 17:31:56 2023 +0100

    make a couple of markups, fix indentation

commit 41b6ba5b2a2f5b81237a152a21f3f4fd4de9a4e1
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Jun 28 17:00:06 2023 +0100

    Add a first draft of "Preserved Dates"

commit 514ff1df92ac52d272c1365aec24ec1412ec7531
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jun 18 21:03:16 2023 +0100

    add a picture of the set

commit 83ba839ae9668fdba789dde20db33b2b151ce621
Author: GitHub Actions on behalf of Alex Chan <githubactions@alexwlchan.net>
Date:   Sun Jun 18 10:19:04 2023 +0000

    Publish new post blink.md

commit f5c38b915d87237a28d4b8206ae4a65f7c54b8ce
Merge: fcce6e4f 1a0b7235
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jun 18 11:16:32 2023 +0100

    Merge pull request #673 from alexwlchan/blink

    add a qucik post about blink

commit 1a0b7235b40c28cf8acc602637c55f46a8911ad6
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jun 18 11:13:16 2023 +0100

    fix an image colour profile

commit 6c7fae8d1848210071975a4ac6ec5e076834011f
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jun 18 10:41:49 2023 +0100

    tweak the conclusion

commit 50934737ca2fbee0e174d5ad2571a3f9afac5d57
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jun 18 10:40:21 2023 +0100

    Add a post about Blink

commit fcce6e4fa17746ea530c4b69eb2d48da574557b4
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Jun 17 08:00:45 2023 +0100

    keep tweaking

commit cb1998dc312c0cdc7db0534e27b63ea58004a1fa
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Jun 17 07:42:11 2023 +0100

    remember the word sapphic

commit 788c134ec8b9f11176493e742fff866540a5a8f9
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Jun 17 07:41:24 2023 +0100

    toss in a picture

commit 3bccd6d910476019924e38246d2da165bee1af49
Author: GitHub Actions on behalf of Alex Chan <githubactions@alexwlchan.net>
Date:   Sat Jun 17 06:35:17 2023 +0000

    Publish new post spy-for-spy.md

commit e2053b772934ff25fee6d2b8e577a7f48b0622b1
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Jun 17 07:32:32 2023 +0100

    Add an entry for "Spy for Spy"

commit 6a4ca46913ab335e6cb06bb85daebf6d8c9166b8
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Jun 14 23:29:27 2023 +0100

    this is still a 410

commit 34c12d35091e544a1dbd7da7349cbe89631918a6
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Jun 14 22:42:36 2023 +0100

    Update 2023-06-05-now.md

commit 24a631899af56221f612a564474d5a334520de92
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Jun 13 22:07:49 2023 +0100

    remove the kindle de-drm post

commit fbe88a6027f2cc7f4654f93ad5f799aa70ba0c31
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Jun 7 23:52:48 2023 +0100

    fix a few more grid issues on mobile

commit e9d92674b74b0b232166f5f02794d05c7929fcd7
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Jun 7 23:36:17 2023 +0100

    fix a grid display issue on small screens

commit 0a2f31a042cc4fb0dee80a616349253bd445646e
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Jun 6 17:12:09 2023 +0100

    Update 2023-06-05-now.md

commit 7e6bd50f61591aa80b09097b30a681005d0bb7a1
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Jun 5 21:28:01 2023 +0100

    Create 2023-06-05-now.md

commit 84ce76de53bb39a13cf38ac30b25352dc4f2ebba
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Jun 5 21:20:43 2023 +0100

    Add files via upload

commit abd59e9c831c8c62f8831c899904fc7a4c9653ca
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Jun 3 08:48:59 2023 +0100

    let's not link to elon musk's hate speech soapbox

commit 59a295c524c264400cf5db010713d92651b3f458
Author: GitHub Actions on behalf of Alex Chan <githubactions@alexwlchan.net>
Date:   Tue May 30 19:41:49 2023 +0000

    Publish new post docker-on-demand.md

commit 30a5d4fcd79922f4a34b8bb7a59121dbf208fa23
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue May 30 20:38:58 2023 +0100

    add the new text-wrap: balance; property

commit 09d14ac277f7ad6e26df16276ae3fc0bfcebcf72
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue May 30 20:38:48 2023 +0100

    scribble a quick post about docker on demand

commit 6c7cf37ec9818c0765b263d38bf236f7664dfd6e
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun May 28 07:30:34 2023 +0100

    fix a couple of issues flagged by rubocop

commit f8cfbbc76136ba5d3310dd71e0a774b832ee3669
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun May 28 05:50:38 2023 +0100

    add the drawing-things tag

commit bc099575635d8fe781dcc1528872e06d0c3d7a62
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Feb 7 20:59:59 2023 +0000

    tweak the twitter plugin

commit 61b64c772f23a766f322705295925cf9eaab28ef
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun May 28 05:26:29 2023 +0100

    Check in all my card assets separately

    This is a precursor to removing an old file called `codesamples.key`,
    which contained all these cards in a single file.  It was getting very
    large and clogging the Git history, because every new card would cause
    the entire file to be re-committed.  I'm breaking it into smaller files,
    then I'm going to remove all versions of the single file from history.

commit 7d205d7c0bb2a99604873f880434ff50de843951
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri May 26 00:00:18 2023 +0100

    fix a bunch of broken links

commit 7b93dc2a576cea70fd29d27186316f75e252b17e
Author: GitHub Actions on behalf of Alex Chan <githubactions@alexwlchan.net>
Date:   Thu May 25 21:02:22 2023 +0000

    Publish new post managing-albums-in-photos.md

commit d09dc85fb8f8591d0ceda2b97d02e13916811c28
Merge: 294f6513 aed19105
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu May 25 21:59:05 2023 +0100

    Merge pull request #671 from alexwlchan/scripts-to-do-albums

    New post: Snippets to manage albums in Photos.app

commit aed191053b8f02ffbc557f2a0214f6180d27db1f
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu May 25 21:55:19 2023 +0100

    fix the photos card

commit fd71cb85f8a302555d9d1c08f105fd720f66bc7a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu May 25 21:52:58 2023 +0100

    a couple of edits on the photos post

commit 22b3598f7ec562ad97dfb89923fb2e9994c589ff
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu May 25 21:01:33 2023 +0100

    first draft of my photo albums post

commit 294f65133179d34cc1ce0e91dc897a3ec0c2e59b
Author: GitHub Actions on behalf of Alex Chan <githubactions@alexwlchan.net>
Date:   Wed May 17 17:20:28 2023 +0000

    Publish new post s3tree.md

commit b6aa3db834401c72ed4a991520bd6288970a7073
Merge: fb2c337f 62fb90cc
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed May 17 18:16:51 2023 +0100

    Merge pull request #670 from alexwlchan/s3tree

    write a post linking to my s3tree script

commit 62fb90cc6478ee1aa7a7319c590501c3decc800e
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed May 17 18:13:53 2023 +0100

    fix the colour profiles

commit fdecdb54169d129deb2668ec20e97d6f2c992877
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed May 17 18:03:58 2023 +0100

    add the card assets

commit 56f3cbdea51214de426dd5b152457d18b9733673
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed May 17 18:03:09 2023 +0100

    write a post linking to my s3tree script

commit fb2c337f853207faf1ed5dd3bef52e1bbcbed93f
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun May 14 23:08:55 2023 +0100

    don't build the site for changes in assets

commit 69ac2ed1b90dd7f8c6a5e2c4fb14aeedded496b2
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun May 14 23:08:32 2023 +0100

    tidy up a couple of tags

commit c7c6b1f805e3132c9539056a8cc67618ea16ad2f
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun May 14 23:08:16 2023 +0100

    add the keynote diagrams for my bedroom

commit 4f4a8c44b4f10145ae49a8023b59db52aab25c19
Author: GitHub Actions on behalf of Alex Chan <githubactions@alexwlchan.net>
Date:   Thu May 11 20:21:19 2023 +0000

    Publish new post redecorating-my-bedroom.md

commit 012a54bee7d1f39cdd89d5ce9caf5bbd3048925d
Merge: acb00591 666bcb6f
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu May 11 21:16:53 2023 +0100

    Merge pull request #669 from alexwlchan/bedroom

    add a post about redecorating my bedroom

commit 666bcb6ff6b7117d06505eef31f68ee057a0760d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu May 11 21:11:55 2023 +0100

    more markups on the bedroom post

commit 9dfc4d345609c0c619a30c7ef14949042431269f
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu May 11 18:46:49 2023 +0100

    more edits on the bedroom post

commit 3f9c3ac3a2e4cf58d1c5fe102777d7b824244946
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu May 11 12:01:40 2023 +0100

    first draft of the bedroom

commit acb0059191c9e0e6bc5370c37f77f6c72e11deb2
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Apr 30 08:42:28 2023 +0100

    record a couple of resource sources

commit 2d81e73c30871e9f3ef868813d06c828ddcdb0f0
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Apr 25 14:51:14 2023 +0100

    remove the whitespace

commit d9cd10f102fa9bdcab03da5585f9f53a8cba1ebb
Author: GitHub Actions on behalf of Alex Chan <githubactions@alexwlchan.net>
Date:   Tue Apr 25 13:40:02 2023 +0000

    Publish new post erratic-ecs-events.md

commit 29949409987afe6f115412b4c213a83e364fb327
Merge: cb2e9c92 4097f3db
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Apr 25 14:37:48 2023 +0100

    Merge pull request #666 from alexwlchan/erratic-ecs-events

    New post: "Getting alerts about flaky ECS tasks in Slack"

commit 4097f3db35ea88ad4c71f17d77f0a40d265fe01b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Apr 10 20:17:01 2023 +0100

    fix a couple more colour profiles

commit 74d7fb6f04782ab36718e4ce532a78cf385cb583
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Apr 10 20:16:18 2023 +0100

    fix a couple of colour profiles

commit 4377e7413183d9a060d04a8fc9fa77ea6684d7ed
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Apr 10 19:18:42 2023 +0100

    Finish the post about erratic ECS events

commit f937cc4f32d77998a124e40b085f89b364cdc77b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Apr 6 11:35:33 2023 +0100

    start writing the ECS events post

commit cb2e9c92873ba303ebf38980a9bf85070fb253fc
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Apr 21 16:57:37 2023 +0100

    Update 2023-04-21-terraform-template-docs.md

commit 4af8e8d898126bcd0d7051a5456babe959e4274e
Author: GitHub Actions on behalf of Alex Chan <githubactions@alexwlchan.net>
Date:   Fri Apr 21 15:40:26 2023 +0000

    Publish new post terraform-template-docs.md

commit 1650e19e1f8e66a727f3eb00bce1e280c5d81517
Merge: 3dd3a170 ba2be7da
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Apr 21 16:38:01 2023 +0100

    Merge pull request #668 from alexwlchan/tf-template-docs

    Add a post about Terraform template docs

commit ba2be7da0dccc4884351496c967785db0ca0371e
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Apr 21 16:35:23 2023 +0100

    Add a post about Terraform template docs

commit 3dd3a17025b92f459ca1a388ecf144bb8ddc041f
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Apr 20 08:03:56 2023 +0100

    add a couple of missing redirects

commit 5e5066124442c7823213a73ccf43559393291576
Author: GitHub Actions on behalf of Alex Chan <githubactions@alexwlchan.net>
Date:   Sun Apr 16 18:37:04 2023 +0000

    Publish new post my-sns-firehose.md

commit 1c8442e3ea5ff82bc992ed93640a6e876da76239
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Apr 16 19:34:12 2023 +0100

    Add a post about my SNS publishing script

commit 8aa60d9e4fba65af7e1ca7b76c9cf3e8e9e88b22
Author: GitHub Actions on behalf of Alex Chan <githubactions@alexwlchan.net>
Date:   Tue Apr 11 21:04:12 2023 +0000

    Publish new post working-with-jq-and-tags-in-the-aws-cli.md

commit 586541e6b5b35c9fe8d0e2ff7e1ce925c90da009
Merge: 0f5ed8bb 3b72a666
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Apr 11 21:58:32 2023 +0100

    Merge pull request #667 from alexwlchan/jq-tags

    add a post about jq and tags in the AWS CLI

commit 3b72a6661a91c53878a51d858393305ee6e741a3
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Apr 11 21:56:08 2023 +0100

    fix a colour profile

commit c8ed36e9a9d069bf863782697b68b50b85189ff6
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Apr 11 21:50:07 2023 +0100

    this card image is playing silly games

commit b3db1b358a3ff45f33d58b980b4b60f24f20aba6
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Apr 11 20:42:56 2023 +0100

    fix the card aspect ratio

commit ce06ebdfb27371b88194d07dbdd383e1d120cec3
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Apr 11 17:50:35 2023 +0100

    add a missing image

commit f9d70ef12d635bb424005e79da31028694b45af2
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Mar 11 09:21:21 2023 +0000

    add a post about jq and tags in the AWS CLI

commit 0f5ed8bba7e94bca5f99f2426f90c3fd5334b6f2
Merge: a6dd1d16 3b0711ec
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Apr 1 17:25:33 2023 +0100

    Merge pull request #665 from alexwlchan/multi-architecture-builds

    Use `docker buildx` to publish multi-architecture images

commit 3b0711ec20848474fb39d21c85a093247c405f77
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Apr 1 17:21:55 2023 +0100

    Use `docker buildx` to publish multi-architecture images

commit a6dd1d16cc10c886f50932b8499434a69eb404fe
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Mar 20 19:02:30 2023 +0000

    add a card image for the coloured icons

commit 7a1bfbe770fd4bec168f504e66328a1b8ae0589d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Mar 16 10:49:36 2023 +0000

    Update 2019-11-27-my-scanning-setup.md

commit a2b93d0cf1e8f1822f32b4d853a9996068ce1536
Merge: bff954e7 cb6ef469
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Mar 14 21:13:35 2023 +0000

    Merge pull request #664 from alexwlchan/use-ghcr

    Move the image used for builds into GitHub Container Registry

commit cb6ef469703bcd69788da38709eef1b75904ba0a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Mar 14 21:07:47 2023 +0000

    Move the image used for builds into GitHub Container Registry

    Docker is doing… something with their free plan, I don't really know what?
    There's nothing keeping me on Docker Hub, so this publishes the image
    into GitHub Container Registry instead.

commit bff954e7906873a939c29eaf56ef90c92f8b0ec5
Author: GitHub Actions on behalf of Alex Chan <githubactions@alexwlchan.net>
Date:   Mon Mar 13 13:24:58 2023 +0000

    Publish new post cats-cross-stitch-and-copyright.md

commit 5752cd2e8145812ce4d161d048059f3ddb787221
Merge: 393563be a5177c07
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Mar 13 13:21:32 2023 +0000

    Merge pull request #663 from alexwlchan/cheetah

    Cats, cross-stitch, and copyright

commit a5177c07f862ffd06a51ede82cb9aa870b2292f1
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Mar 13 13:18:42 2023 +0000

    make all the images be sRGB, not Display P3

commit 9a71057806bb60e489d763294c2fc6a997f524e7
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Mar 13 13:17:00 2023 +0000

    remove a missing lint

commit f18bff35fcf614dc95fd8ffe7d6a0930b310d86a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Mar 13 13:12:52 2023 +0000

    final edits

commit 568e901ef00e7afdd0f62f7a0e7b230be714e7b3
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Mar 13 11:59:32 2023 +0000

    tweak some wording

commit 0ee753172a4847d8331f543a193297cab9fcf1c2
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Mar 12 22:35:43 2023 +0000

    s/a/in

commit ad41f6bece5624ac43f177372097c8bde31024d6
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Mar 12 22:35:24 2023 +0000

    Add a post about my cheetah cross-stitch

commit 393563beeadc2d35e329a75ba37126fd3ae60d99
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Mar 8 11:32:59 2023 +0000

    Add a card image for "what does \d match"

commit f2c49959ad3f9cffed08ce3c0aefdc8d8e16a8d9
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Mar 6 22:47:14 2023 +0000

    Update 2022-08-03-no-cute.md

commit 9c8f594a050afbd92a77237411435a90e9a6bd33
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Mar 5 20:19:41 2023 +0000

    sort out a couple more redirects

commit ea9197644352de97ba3ccd28bf4170822135e0e5
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Mar 5 18:19:14 2023 +0000

    don't forget the redirects!

commit d8a7a6b8317d157adf884fca3a8a5f2103169d4e
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Mar 5 18:09:18 2023 +0000

    Replace a couple of these images with shiny hi-res and WebP versions

commit bc4dd21494f4f0774ae3a648fa27acd2c54c6230
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Mar 5 13:19:49 2023 +0000

    Update socials.html

commit 40ae1a590d163a7d806f6b937d9ad2d15494a3a9
Author: GitHub Actions on behalf of Alex Chan <githubactions@alexwlchan.net>
Date:   Sun Mar 5 12:33:07 2023 +0000

    Publish new post filtering-netlify-analytics.md

commit ea52075b3295b446549e0754c5d40323aca5f9f7
Merge: c45abe90 dd7b1be5
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Mar 5 12:30:50 2023 +0000

    Merge pull request #661 from alexwlchan/remove-bogus-requests

    Filtering out bogus requests from Netlify Analytics

commit dd7b1be595845861b9103882b30df397503a95f7
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Mar 5 12:28:19 2023 +0000

    convert these images to an sRGB profile

commit d3c2ce05e4f410c050d7f66d5373aeb0d28421c5
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Mar 5 10:15:33 2023 +0000

    couple of edits

commit eb6b65c9ffa34b0076d309704f03f0c9e7a4c3cf
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Mar 5 10:11:22 2023 +0000

    tidy up some of the wording

commit 50b83b4d3c83e996650305ccdf44b3273c980e94
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Mar 5 10:09:20 2023 +0000

    actually add the netlify analytics draft

commit 81308b69981c7f3467d8d09665fd7f934478f466
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Mar 5 10:09:15 2023 +0000

    tweak the links on the homepage

commit 0d5582318d429502149515ed49357ca17f8a509b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Mar 5 10:07:32 2023 +0000

    Add a post about filtering Netlify Analytics

commit bac0100b6deefbdaea2aebaa57e8d8eceff654ad
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Mar 5 10:07:23 2023 +0000

    Dark aware images don't need to be desaturated

commit 527d70e895c426b196cd73b0d6380063d5bc224c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Mar 5 10:06:59 2023 +0000

    Don't include the HTML comment in the 400 page

commit c45abe90c3d5f93fa32673ea7863279f2fa6c646
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Mar 5 08:02:24 2023 +0000

    even more wordpress redirects

commit a528ffde16f09a74ffc65ef34b799e11302bc3ab
Merge: 51a25a97 4c342a5a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Mar 5 07:59:34 2023 +0000

    Merge pull request #660 from alexwlchan/reduce-perceived-complexity

    Refactor the Netlify redirect handling to reduce the PerceivedComplexity metric

commit 4c342a5abb55c5857177e97d6befc4df62ee7d7c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Mar 5 07:55:02 2023 +0000

    Refactor the Netlify redirect handling to reduce the PerceivedComplexity metric

commit 51a25a9767030dc8537440eb485027dc48f22358
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Mar 4 21:05:19 2023 +0000

    this should be .colors

commit 471d5fbd0a951c5a94c4ab6c5478ab03989af708
Merge: 8c340f5d ff2d44df
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Mar 4 21:00:03 2023 +0000

    Merge pull request #659 from alexwlchan/fix-rubocop

    Reduce the rubocop PerceivedComplexity metric in css.rb

commit ff2d44df95d4c0c1f207f8212293c852c91a3026
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Mar 4 20:56:00 2023 +0000

    Reduce the rubocop PerceivedComplexity metric in css.rb

commit 8c340f5df7af2a675cecc02eae9776bf3e71263b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Mar 4 20:48:00 2023 +0000

    add a redirect for a v popular 404'ing image

commit 41a84742677cd9999949b5d16dbc27f0794c869c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Mar 4 17:10:52 2023 +0000

    fix the failing plugin tests

commit cf7fb3bd7aa6b0e01595f7ad564df87c64c143df
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Mar 4 17:01:27 2023 +0000

    ensure pages actually have content!

commit 94b318584195b7fbed68ed08b7020c9183dc9c2a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Mar 4 17:00:11 2023 +0000

    add the missing bits to default.html

commit 13cff5b64f8c998b812d0e1c2fe1873025983eda
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Mar 4 17:00:00 2023 +0000

    satisfy rubocop 1.47

commit 8ca493485898334aebbc0ad39ebfa60d4f31cd75
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Mar 4 16:51:28 2023 +0000

    fix a couple of rubocop issues

commit 85bbc3f9416f8dfddbe75a7efffdf87ad9252d6a
Merge: 833df3a3 9c540945
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Mar 4 16:28:37 2023 +0000

    Merge pull request #658 from alexwlchan/speed-up-jekyll

    Try to speed up Jekyll a little bit

commit 9c540945b3f60d1995f175e24bf1c6bf31aef348
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Mar 4 16:26:35 2023 +0000

    Move a couple more shared bits out of head.html

commit 34860328037be6873fc8a5a0fe51939741e8cacb
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Mar 4 16:25:37 2023 +0000

    We only need to parse the HTML once for inline styles, not twice

    I was hoping this might improve the build time, but I guess not.

commit fb5ef269695f5d92941ab0533756c229216fa2d6
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Mar 4 16:24:50 2023 +0000

    Remove an unnecessary empty line

commit 833df3a348d115211d4655b04e6169d78c08983e
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Mar 2 19:49:21 2023 +0000

    add a redirect for an especially popular image

commit 84b7ef5d7ae8a765b23631daff5c8d3f36946b89
Author: GitHub Actions on behalf of Alex Chan <githubactions@alexwlchan.net>
Date:   Thu Mar 2 15:51:48 2023 +0000

    Publish new post dictionaries-and-userdict.md

commit b5c5f2615abc368ed072ea0b3f27264aa625eefb
Merge: 6f99a9f0 8d2b25f5
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Mar 2 15:49:28 2023 +0000

    Merge pull request #657 from alexwlchan/normalised-dictionaries

    Add a post about dictionaries and UserDict

commit 8d2b25f5be9b59f3436a0623e2e3b590926914d1
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Mar 2 15:48:32 2023 +0000

    put the card image in the right place

commit 664f9d516facf059ba8259774a45328d2baa9d78
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Mar 2 15:46:27 2023 +0000

    Add a post about dictionaries and UserDict

commit 6f99a9f0bc04094585f5604e6a54d18e31aed093
Author: GitHub Actions on behalf of Alex Chan <githubactions@alexwlchan.net>
Date:   Thu Mar 2 14:03:08 2023 +0000

    Publish new post balancing-act.md

commit 3d791caa511d707a767ddfdbfac833a63e8b0172
Merge: 73aeb548 3939e86d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Mar 2 13:59:52 2023 +0000

    Merge pull request #656 from alexwlchan/classroom-sizes

    Add a quick post about classroom sizes

commit 3939e86d32eea43765ccc99c2603674aa7710b73
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Mar 2 13:57:24 2023 +0000

    it should be colors

commit eb84e06e287aaedd78de96e0140d5ef399fb3e5b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Mar 2 13:38:14 2023 +0000

    add a note about google

commit 601e836ede7650a578e87158c37d2ff9346e6410
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Mar 2 13:35:53 2023 +0000

    a brief markup, but good enough

commit 93e9eebe71eaa34d5e571ce86a5de87bba266fa7
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Mar 2 13:33:14 2023 +0000

    first draft ob the balancing post

commit 782b62653c41d1fc227e36bf7fda969c7b8b61fa
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Mar 2 12:59:58 2023 +0000

    Add a first draft of the balancing groups post

commit 73aeb548fe808497aa50e3260664f80105f2ce31
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Mar 2 08:37:48 2023 +0000

    try to fix slowness on the tag filters page

commit a4e55c08f57b4864f032e9381c7775e90c62a2d3
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Feb 22 22:43:04 2023 +0000

    toss in a linkedin link to my contact page

commit a9e7054551765af3cfa6ddc40087aa213313c2d3
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Feb 20 19:20:40 2023 +0000

    add a card image for 'testing JS without a framework'

commit 8ed1145e4188cd3f37b84ae361461d16920fe1bb
Author: GitHub Actions on behalf of Alex Chan <githubactions@alexwlchan.net>
Date:   Mon Feb 20 08:28:17 2023 +0000

    Publish new post testing-javascript-without-a-framework.md

commit fd4098903434167e85f159ae204b850dac408adb
Merge: 65ead281 62bccf4b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Feb 20 08:24:42 2023 +0000

    Merge pull request #654 from alexwlchan/testing-javascript-no-framework

    Testing JavaScript without a (third-party) framework

commit 62bccf4bcada61412093e5da203edd77fa5866b8
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Feb 20 08:22:10 2023 +0000

    Make the linter happy with my example HTML file

commit 65ead281db84143783be7003c59a34a7a3dde4a1
Merge: 4ae0bf5f 6dbb0996
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Feb 20 08:18:32 2023 +0000

    Merge pull request #655 from alexwlchan/rubocop-repeated-blocks

    Fix some Rubocop warnings about multiline block chains

commit 6dbb0996abb36ddca012a020618e478ca33cc2b5
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Feb 20 08:15:50 2023 +0000

    Fix some Rubocop warnings about multiline block chains

commit 593d91019c68ca3c3cca88a94385ea5b885116d2
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Feb 20 08:09:57 2023 +0000

    markups on my javascript post

commit 4ae0bf5f530830ead8b57bb25e83f54192e17224
Merge: 668d946e 241dbdf7
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Feb 20 07:46:50 2023 +0000

    Merge pull request #653 from alexwlchan/no-more-best-of

    remove the best_of metadata; I never use it

commit 241dbdf73a1ddb2ab8da55023c2c6f7253d653b5
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Feb 20 07:43:59 2023 +0000

    remove the best_of metadata; I never use it

commit dc2d74c47c5efd9c07e86fc7143337cba5df674c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Feb 20 07:42:37 2023 +0000

    clarify this line

commit e699c5ada71a3284b09e7aa9eff31f73b7e2a7ef
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Feb 20 07:40:15 2023 +0000

    first draft of this post

commit 668d946ef83bc0d2cf5130d505bfaff17a06e65b
Merge: 3508c29b d5e36d9c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Feb 18 08:28:16 2023 +0000

    Merge pull request #652 from alexwlchan/fix-rubocop

    Fix more rubocop stuff

commit d5e36d9c159d586f6fed0eb349f6ba1d737922c2
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Feb 18 08:24:47 2023 +0000

    fix a rubocop warning about long parameter lists

commit 1a287da4f91159787d70cbe90b630ec1f0168cca
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Feb 18 08:24:25 2023 +0000

    fix static file generator

commit fdaeb1560d03650ca78ce78dc09e3df0e3a4d2a8
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Feb 18 08:21:50 2023 +0000

    Fix a rubocop warning about perceived complexity

commit 026d42ca03911ae6f87bf92b8adab5208e7fa13a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Feb 18 08:15:54 2023 +0000

    Remove a couple of unused vars flagged by rubocop

commit 3508c29bd1929ffee9b56efefa27cd2507981678
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Feb 18 07:58:07 2023 +0000

    Fix a few issues with CSS in the local dev environment

commit bab597fc80c3c46d556f5b262fe7a00e2f705da2
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Feb 16 20:03:06 2023 +0000

    render markdown in the post descriptions

commit b8b61ff8525aa90fa75da5170fc52995ad3ffb74
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Feb 16 19:58:55 2023 +0000

    fix the styles for emails on the homepage

commit db8bf2b2be3fd0333f5a6a222dd7d05355a0fbee
Merge: f6ca0b69 041f670f
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Feb 16 17:01:44 2023 +0000

    Merge pull request #651 from alexwlchan/social-contact-links

    add some new contact methods

commit 041f670f05f309f6acbfcbb055668dc7d6270053
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Feb 16 16:58:49 2023 +0000

    add some new contact methods

commit f6ca0b698c0a861d7111be1d65ed3914c2ac645f
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Feb 16 11:00:19 2023 +0000

    Update 2023-02-16-css-formatting-in-the-console.md

commit 09e1f4cc5e2822de23456cf79cd2fdfe30a7af01
Author: GitHub Actions on behalf of Alex Chan <githubactions@alexwlchan.net>
Date:   Thu Feb 16 10:58:10 2023 +0000

    Publish new post css-formatting-in-the-console.md

commit aa751f91776c6c312d8c6edf04d0386f95781b64
Merge: 963ebbcc 5a631088
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Feb 16 10:55:54 2023 +0000

    Merge pull request #650 from alexwlchan/formatting-in-the-console

    Add a post about CSS formatting in the console

commit 5a631088be37119ef7b699c0c12c621caa8e8c09
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Feb 16 10:53:03 2023 +0000

    change slightly less!

commit cd2d554eebd63abec7bd3dcf103cbe399cac1dab
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Feb 16 10:48:38 2023 +0000

    fix all my attributes

commit 109d3ba5001bd92e7b8c78e7442b27af61c1a5ce
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Feb 16 10:45:06 2023 +0000

    add some tests for attribute parsing

commit 5bb5d9e961f68b54d138bbee56c965c1bcf27d0f
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Feb 16 09:13:30 2023 +0000

    that should be backticked also

commit 59e36f1fc06c087d91add76b0e81771f43092112
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Feb 16 09:13:22 2023 +0000

    Add a post about CSS formatting in the console

commit 963ebbccc80adf96c5a96e819dc58ae3d1f8ecbc
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Feb 15 22:26:19 2023 +0000

    Make sure not to set the `alt` attribute on inline SVG; use a <title>

commit c1379fce0ba75e043a75732592833daed518d796
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Feb 16 07:51:29 2023 +0000

    Update 2023-02-15-school-stuff.md

commit c9edde5c7c6aa1f9c5de16eff622d33f01e345bb
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Feb 15 23:19:13 2023 +0000

    add a caption and some text

commit 9c6f4b059ab973f9ea5fe28d89d67d3a48ca5d72
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Feb 15 23:13:30 2023 +0000

    fix a bunch of attribute escaping issues

commit 5e739fd7c200d4d14d0aa72a3f1a9c10b2614d84
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Feb 15 22:40:52 2023 +0000

    fix a spacing issue in tweets

commit 5f42d01ac03f0d42c82724480ea45657809c38a4
Author: GitHub Actions on behalf of Alex Chan <githubactions@alexwlchan.net>
Date:   Wed Feb 15 07:37:34 2023 +0000

    Publish new post school-stuff.md

commit c86a56923aeb31b05b20a9a3e31504047ffb39a4
Merge: d09a9b2e 6cecc526
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Feb 15 07:34:48 2023 +0000

    Merge pull request #649 from alexwlchan/school-stuff

    School stuff

commit 6cecc526ed693e54ff32661b071f83e6dc32b403
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Feb 15 07:31:52 2023 +0000

    add alt text and edits

commit 8e23cb8c850c65498738f52af58af429d90fa9e6
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Feb 15 07:08:32 2023 +0000

    edits

commit 9dca6af2ef695f4b9e08b9356249c18054d2bce4
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Feb 15 07:01:44 2023 +0000

    first draft of school stuff

commit d09a9b2e563b45571b6b49ad2f9015856831ca0d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Feb 13 16:25:21 2023 +0000

    let's call this page 'writing'

commit 6c76de314b9cc97867b7a7e90e49e4ebec0a4071
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Feb 13 08:37:15 2023 +0000

    Update index.md

commit 56bab94b7adcdefdfb3c534ad1569c45f8b10163
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Feb 13 08:02:13 2023 +0000

    Only push commits if GitHub Actions has changed something

    If I push several commits straight to live, GitHub can complain because
    it's not allowed to push, even though it had nothing to push!  This should
    silence those spurious warnings.

commit efa6146556798424b47a8c15ad2aeb4db830b07a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Feb 13 07:35:11 2023 +0000

    more colour tweaking

commit 6bfe384597b7569448fb456b5be1e617883c5862
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Feb 13 07:34:07 2023 +0000

    make this a brighter colour

commit 921132e19db8b52f2b66da896ab06bc2e314f3fa
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Feb 13 07:32:54 2023 +0000

    add the screenshot class to this image

commit 495bb4a422a5b2bc4721d80ce586836f66bea076
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Feb 13 07:32:46 2023 +0000

    make the social buttons look better in dark mode

commit 1507f8cb896b1064c6d23e24e4f2d5564143883f
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Feb 13 07:29:39 2023 +0000

    make this page a bit nicer in dark mode

commit 1d57da49433ceb1370c07e64591485ee3dc69b94
Author: GitHub Actions on behalf of Alex Chan <githubactions@alexwlchan.net>
Date:   Mon Feb 13 07:28:37 2023 +0000

    Publish new post s3-bucket-inventory.md

commit c76b56e9f5ac1f598ee95ae99a5bc0cc7d63b235
Merge: 419ee7c3 dc1504d9
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Feb 13 07:25:32 2023 +0000

    Merge pull request #648 from alexwlchan/bucket-inventory

    add an entry about my S3 bucket inventory

commit dc1504d96e1ecec12920ff70996aa4c798b6c944
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Feb 13 07:24:57 2023 +0000

    fix rubocop warnings

commit c79b87cc6d088d51afeb92d7c601b27c3ebec91b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Feb 13 07:22:41 2023 +0000

    add an entry about my S3 bucket inventory

commit 419ee7c3a3ba8b6c1121f99960d5d9cc69dfe9e7
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Feb 12 20:43:33 2023 +0000

    Update index.md

commit 93ed9a6a79fbec687baaabfe81aedca3acba58d4
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Feb 12 20:42:59 2023 +0000

    Update index.md

commit e7a6aadef89cd79aa53fc0756508c4b754b6b8cd
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Feb 12 20:28:41 2023 +0000

    move contact info to the bottom

commit 069d9c649167cfeb10c61305400e58918dccfd5d
Merge: eca16c36 988ac17d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Feb 12 20:07:14 2023 +0000

    Merge pull request #647 from alexwlchan/redesign-2023

    soup up the new-reader experience for the posts

commit 988ac17d63bf569481f3ff00e5522c4dac1b4fc3
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Feb 12 20:04:11 2023 +0000

    bin the old "new archive" post

commit 709d47b37ebc4e89a06d971868323c252fc99d9f
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Feb 12 19:56:43 2023 +0000

    fix a few broken links

commit ddb80fe105fde582866728373c9f76172e133b5e
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Feb 12 19:55:48 2023 +0000

    fix a bunch of rubocop warnings

commit 7e291231a5b7808395d2d4cf6e89a2f4239d28a0
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Feb 12 19:47:26 2023 +0000

    revamp some of the social links

commit df0ee473ce4417d3f943dc158d3d7ded05764984
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Feb 12 19:20:13 2023 +0000

    sort out the homepage

commit 6c385f7ee8b9b634d7ea55b2975b3d2228887617
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Feb 12 19:15:26 2023 +0000

    Tidy up some of the copy

commit 20bf26846586d003c4ff1b63eb9ac6c4a7dcd8da
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Feb 12 19:12:57 2023 +0000

    Add an eggbox + a page of major themes and topics

commit eca16c3632c2add37ebf68013fd5aa568c662561
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Feb 12 17:31:21 2023 +0000

    Add a Mastodon link to the footer

commit a6919ed5d3fd14d696af90206c33a70ffea087a0
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Feb 12 17:17:35 2023 +0000

    Put the Twitter link back in the footer

commit 3856568d38b89a29aa01d3609f0bff541f12b968
Merge: 403693dd 70ea844f
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Feb 12 08:34:19 2023 +0000

    Merge pull request #645 from alexwlchan/permalink-accessibility

    make permalink read properly for screen readers

commit 70ea844f3948846bfe044ef8692ddb393d0b6b16
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Feb 12 08:31:57 2023 +0000

    make permalink read properly for screen readers

commit 403693ddcf9b796d00cc6525ee57c75f1ca66151
Author: GitHub Actions on behalf of Alex Chan <githubactions@alexwlchan.net>
Date:   Sun Feb 12 08:29:25 2023 +0000

    Publish new post moving-to-the-cloud.md

commit baf37429070f60500e69426c5f90637d0679444e
Merge: 237c61c0 13c81405
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Feb 12 08:26:41 2023 +0000

    Merge pull request #644 from alexwlchan/intro-post

    link to my "moving to the cloud" post

commit 13c81405880191d0b89e089d22ce2b4706ca579b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Feb 12 08:24:11 2023 +0000

    link to my "moving to the cloud" post

commit 01c1e9b6c5a81b8e37f5101bd4ebaf8d2f470c75
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Feb 12 07:58:40 2023 +0000

    Add an entry for "How moving to the cloud took our digital collections to new heights"

commit 237c61c052460cc18814ea33c7f6f8d742104906
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Feb 7 21:05:41 2023 +0000

    fix the hover bg colour of cards on the homepage

    previously hovering a default red card gave you green, now you get the
    correct red hover

commit 4d17e537c7faf9733b1b69af134c3bd1b459157d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Feb 5 09:32:35 2023 +0000

    add a rainbow flag

commit 47eda3ddc2e0d00ca60871adfe4f47dc1eb34090
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Feb 5 09:24:30 2023 +0000

    add the word 'queer'

commit 2f7ad296cf6fdd34464a7ad4e43b98f8a7c936d3
Merge: 32d7576f 17f32192
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Feb 1 06:17:46 2023 +0000

    Merge pull request #643 from alexwlchan/refactor-linting

    Improve some aspects of the popular "How to underline text in LaTeX" post

commit 17f321926c432a21758ffc7c27e2d25b4a3d87e1
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Feb 1 06:13:36 2023 +0000

    Make my pretty-looking LaTeX more accessible to screen readers

    I've also removed the Jekyll caches for cleanup_text and smartify; the
    performance gain is marginal, and they make it harder to debug this sort
    of thing because you might be getting a cached value.

commit 9b9b4557199d83383bee0943293efba5098591a3
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Feb 1 06:00:46 2023 +0000

    Make sure we don't include unescaped HTML in a <title>

    This fixes a bug in a fairly popular post about LaTeX underlines (among
    others), where the "helpful" HTML substitutions meant this was getting
    a title like

        <title>Four ways to underline text in &lt;span class="latex"&gt;L&lt;sup&gt;a&lt;/sup&gt;T&lt;sub&gt;e&lt;/sub&gt;X&lt;/span&gt; – alexwlchan</title>

    which looks ugly in a browser.

commit 03c25f5f5566d316113ebacc722f85e27cf88976
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Feb 1 05:43:20 2023 +0000

    Add another frozen string literal

commit 445b4888e13c0b5988cc3b5b2b4ca695826738a3
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Feb 1 05:42:34 2023 +0000

    Only parse the HTML documents with Nokogiri once

commit 4518ef4e26a667fe88c87102ff058686046f2b52
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Feb 1 05:38:41 2023 +0000

    Fix a couple of newly-broken redirects

commit 32d7576fb700d181b0ff94bc8c50b630b1c89a0e
Merge: 9022eab1 4c6e76bc
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Feb 1 05:30:32 2023 +0000

    Merge pull request #642 from alexwlchan/no-combinable-loops

    Fix a rubocop warning about combinable loops

commit 4c6e76bc0cf40153dbec6a850d90122c3430e926
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Feb 1 05:27:29 2023 +0000

    And another frozen string literal comment

commit ac04599c2bd3e7c9d3a42b046fb454cb65435a92
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Feb 1 05:27:10 2023 +0000

    Fix a rubocop warning about combinable loops

commit 9022eab12747071f1067b22457467800887aeeff
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Jan 28 23:56:46 2023 +0000

    bin the explicit width attributes on the svgs

commit 2ad1fe92de59e7a2e6ca3f8fef2bcd7cd1b78fa0
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Jan 28 23:55:46 2023 +0000

    add a stroke outline to this image

commit 9b2a7d128e55bb89a0178efeb908b120c574032a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Jan 28 23:49:57 2023 +0000

    you need these <figure> wrappers for iOS

commit ad59f760e191a4a40a822e41ef4b0418d9ac9e99
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Jan 28 23:42:49 2023 +0000

    Revert "Add dark-aware diagrams to "inner/outer strokes""

    This reverts commit f242310de0b31eead3417422021a15bc36b65500.

commit 81fcbf14dd866106db0f66acb3e9d935db19aeb6
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Jan 28 23:39:16 2023 +0000

    Add dark-aware diagrams to "inner/outer strokes"

    This post is featured on my homepage, so let's make sure it looks good
    in dark mode, and test some patterns for dark-aware SVGs.

commit 032601114efb3dbf762a19858911932fb2d94d29
Merge: a47144c6 b15f7c82
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Jan 28 23:13:49 2023 +0000

    Merge pull request #641 from alexwlchan/fix-rss-issues

    Check a few issues with the Atom feed plugin; add tests and fix some rubocop lints

commit b15f7c820e3d94f4c5a12c86f4a558651be49f21
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Jan 28 23:10:59 2023 +0000

    Replace this repetitive code with a loop

commit 801b9e9baebf66088cb2da614130b8d8c7d3ba02
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Jan 28 23:07:22 2023 +0000

    fix a few more rubocop warnings

commit 4b220376696b8248e1c97ddb63028c39cc9c3847
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Jan 28 20:39:19 2023 +0000

    Add some tests for the atom feed filters

commit 4357937ddfef4452934a593c23134f2ca36734b9
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Jan 28 20:23:48 2023 +0000

    Add some tests for the atom feed filters

commit 581cf4fd229f2c52f12ed55f830e83dd561e3d11
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Jan 28 20:13:17 2023 +0000

    Fix the rubocop lints around string concatenation

commit a47144c68b40445f998e7c432213928884fd8889
Author: GitHub Actions on behalf of Alex Chan <githubactions@alexwlchan.net>
Date:   Sat Jan 28 10:30:50 2023 +0000

    Publish new post responsive-image-bookmarklet.md

commit 2babba6cf89631aebc2ddde8f4d6b4c05e8b81d3
Merge: 2066b933 b461dd30
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Jan 28 10:28:45 2023 +0000

    Merge pull request #640 from alexwlchan/responsive-images

    Responsive images

commit b461dd304a3725f2877f30bed90d1b0bd483ebd7
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Jan 28 10:26:03 2023 +0000

    Add missing alt text

commit e4b6ce226b049f4398cd1a73de17071bf570c0ab
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Jan 28 09:58:38 2023 +0000

    fix a couple of rubocop issues

commit ec2c9e01d20cb541af48f397670b4fc08863ed7b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Jan 28 09:57:37 2023 +0000

    add a post about my responsive image bookmarklet

commit 5c03dd0a8ebacc356663854e5578efd937816cad
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Jan 28 09:27:29 2023 +0000

    make the "maths is about facing ambiguity" post dark-aware

commit 2066b93311ed6a215079947a1e25a2ec6a513a27
Merge: 642bc628 bda3f92e
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Jan 26 22:32:06 2023 +0000

    Merge pull request #639 from alexwlchan/fix-more-plugin-stuff

    Fix more plugin stuff

commit bda3f92e480b16cd8f5d048cfaf6009257cc4382
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Jan 26 22:22:18 2023 +0000

    Fix a rubocop lint about parameter names

commit ebc7c6db2accba0197c90e787030ddf6c4340f32
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Jan 26 22:26:54 2023 +0000

    Delete some apparently unnecessary code

    That `puts` method never gets called, I'm not sure `data` exists if it
    was, and the site builds fine without it.

commit 642bc62875e054b20c2a01395fcf670bc0bbaa21
Merge: bc1829ff 66037cfd
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Jan 26 22:24:54 2023 +0000

    Merge pull request #638 from alexwlchan/better-images

    Improve a couple of plugin things

commit 66037cfd440f9fd16d70a48375ae561ab2d88455
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Jan 26 22:20:43 2023 +0000

    Add some tests for filter_cleanup_text; fix a bug

commit a8a25c0d7aa3c0f7e76c4ce3686499a7040a8e3a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Jan 26 22:16:08 2023 +0000

    Fix a rubocop lint about HereDocIndentation

commit e18b7d0a9824e3d37c11c82d9b2a6311a5e1085e
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Jan 26 22:14:42 2023 +0000

    remove unnecessary double parens

commit 16495f2233bf19760d42914d34a73a0de9acc021
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Jan 26 22:13:17 2023 +0000

    Add some extra widths to the image on the homepage

    It's one of the most popular pages, and the image is just quite big --
    nearly a megabyte on my iPhone (!).  Smaller sizes should reduce the
    bandwidth on this page.

commit 0bf113cfa97ebd75a5025608e1a76ccb3a71805a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Jan 26 22:12:36 2023 +0000

    Fix some Rubocop warnings about Style/AndOr

commit 26bd97eba206edf7e28ec87a62e1045038c6662f
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Jan 26 22:08:36 2023 +0000

    Fix a rubocop warning about Metrics/BlockLength

commit 40cd97d026c7dca0c2135e65c182aec0a92bb325
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Jan 26 22:05:27 2023 +0000

    Use width/sizes in the picture tag, not pixel density

commit bc1829ff1fb3aee6f175acc1ea46d6ccee599167
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Jan 24 06:46:29 2023 +0000

    fix another few images

commit bda0a40445cb4860ca7ce54aafb72d3562387c40
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Jan 24 06:39:19 2023 +0000

    delicious bird seed!

commit 72fd8cbc834e01a2dd84312a23677e470e8d3fcb
Merge: f5e7185e 7e92a8c1
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Jan 24 06:29:16 2023 +0000

    Merge pull request #637 from alexwlchan/run-plugin-tests

    Add a Make task and GitHub action for the plugin tests

commit 7e92a8c1ae0cd97bf7200a98bd947eba931372c5
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Jan 24 06:24:45 2023 +0000

    fix some issues flagged by rubocop

commit da0c5b4e4c00125df074c06548a6549e4f275019
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Jan 24 06:23:48 2023 +0000

    Add some proper tests for the inline style plugin

commit 8fcc98cf8e3e58a7021f4889b93c2302cdae2fee
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Jan 24 06:08:38 2023 +0000

    Add a Make task and GitHub action for the plugin tests

commit f5e7185eb92d6fc18ad8b6d1862aa10e34bc95a5
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Jan 24 05:55:33 2023 +0000

    use Ruby's neat 'clamp' method

commit 97cac8b00223a3009d6ca0ba86a25aff9d0048c3
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Jan 24 05:50:04 2023 +0000

    ditch the wrapping <center> element, it's invalid HTML

commit db06b950de484a046a8362ef2ba773589485a3ea
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Jan 24 05:45:07 2023 +0000

    Maybe a void <source> tag is fine after all?

commit 0708ac03594dca9a78bb3c969b7354a0dfa07e0f
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Jan 24 05:35:00 2023 +0000

    this is now available as a zip download

commit 60d6e9efe1f4d3ec66ba391138ebb074a8569063
Author: GitHub Actions on behalf of Alex Chan <githubactions@alexwlchan.net>
Date:   Sun Jan 22 21:22:16 2023 +0000

    Publish new post changing-the-bulb-in-a-meridian-lighting-cir100b-ceiling-light.md

commit e273ffbcb481046596e2304d43b3f9db9ad7ec2e
Merge: ddd26ea9 20a1cce6
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jan 22 21:19:42 2023 +0000

    Merge pull request #636 from alexwlchan/light-bulbs

    add a quick post about my ceiling light

commit 20a1cce663dfa47231aebdf4879fc7248ba50612
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jan 22 21:02:30 2023 +0000

    add a quick post about my ceiling light

commit ddd26ea97fc297cd05801fbd04a2cd50f65783a2
Merge: 733b5c25 2bc97c93
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jan 22 14:29:05 2023 +0000

    Merge pull request #635 from alexwlchan/delete-misc

    move everything in 'misc' into the files folder

commit 2bc97c9320260e30a7d800a14f8ec7417efa7cde
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jan 22 14:25:27 2023 +0000

    move everything in 'misc' into the files folder

commit 733b5c25b70b68f6c16b8d401cf7fe48adb34af8
Merge: 24b9bf69 5c9dfd05
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jan 22 09:19:29 2023 +0000

    Merge pull request #634 from alexwlchan/fix-broken-html

    Fix a couple of bits of broken HTML

commit 5c9dfd05adab50ab114cc39eb7851a71f8355cef
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jan 22 09:16:52 2023 +0000

    Fix some broken HTML syntax in the t.co URL post

commit eee87c8ab9357e2d089dbe0591df637b056d55ae
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jan 22 09:13:05 2023 +0000

    Remove an extra closing </figure> tag

    This was being rendered with an empty paragraph above and a visible
    </figure> below.  I have no idea what the difference is or why this
    whitespace change fixes it, but it seems to work now.

commit 24b9bf696156e17b13cf88d958f4c0f122b9b264
Merge: 43b26961 72b86e18
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Jan 21 08:32:49 2023 +0000

    Merge pull request #627 from alexwlchan/more-css

    Implement a first version of dark mode

commit 72b86e18b2967ad94dfe8335d09ab7da771cbb89
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Jan 21 08:30:50 2023 +0000

    move some variables around

commit beb4c370e7549ea3fdd599f74fc957f000adcc68
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Jan 21 08:28:06 2023 +0000

    bin the old stylesheet docs

commit ad506a55ac7e6f8810bde03d87f425e16f82e1b4
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Jan 21 08:27:16 2023 +0000

    remove an unused variable/hook

commit 36213ebbc0a4cbb2cfed5cbbb4d11cd6b39f6169
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Jan 21 08:26:30 2023 +0000

    remove a stray empty line

commit 84e0923e7d188cea3374350b27232cdd5d5aa6e1
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jan 20 21:42:09 2023 +0000

    remove some old redirects

commit d3fe5b3c83968cf157c954194a6dbe31ced3764e
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jan 20 21:41:13 2023 +0000

    fix a couple of issues from merge conflicts

commit 228d33b4d9b5bf5d515b78f043ac97b53a5d5f7b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Jan 19 21:42:32 2023 +0000

    more colours

commit f12f05ce4af6b506cf776a98c91aeebcbb729893
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Jan 19 20:14:37 2023 +0000

    more colours

commit cfe26c1ebcc323395ed95c3e920c23bc8be40c7e
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Jan 19 20:00:12 2023 +0000

    keep fiddling with colours

commit 3bca2e5c0113ad860da4d6b12d55c3281a6beb2c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Jan 19 19:47:24 2023 +0000

    continue updating colours

commit b6fd9a3bf2061813f6f0c2d9ab7313b3ac7367f3
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Jan 19 15:02:26 2023 +0000

    continue sorting out the palette

commit 0d510e939de104024dae768fc1c38b2a86a76a23
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Jan 19 15:02:26 2023 +0000

    continue sorting out the palette

commit ea5aeba0a2306fc5ddee90456005841bce39340e
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Jan 19 09:12:20 2023 +0000

    start rolling out a new colour palette

commit 2eaa5f798b55c5cb8e47e56ac91e04d3953ffda6
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Jan 18 21:19:19 2023 +0000

    remove some unused lines

commit bcf11606f6fb9107eff09e37b0a6d62122013f40
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Jan 18 21:08:13 2023 +0000

    the theme colour css is small enough to inline

commit 88e560e0c0cbb720047518b649c1706b65de81a5
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Jan 18 21:06:02 2023 +0000

    make rubocop happier

commit 7ae0bacd545b78e32d072933087aa0f692207ef7
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Jan 18 21:05:03 2023 +0000

    make rubocop happier

commit 7cdee0e99ed96357a9e6969d719df3d681b582a9
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Jan 18 21:04:54 2023 +0000

    cut some more CSS; remove the twitter footer link

commit 6ccbe3e0465c3414ac9af21ff460f7719d2f1d2c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Jan 18 20:46:14 2023 +0000

    get dark mode working (kinda)

commit 095bf380e96f8143a71f719fabbf3e450d544375
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Jan 18 18:54:35 2023 +0000

    finish fiddling with dark mode

commit 0e0b85b72de2c1ef559ab6aa562528839ad8ce8f
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Jan 18 18:28:20 2023 +0000

    continue fiddling with pygments

commit 15df6b77f6ff249418f11978298004b8a354174f
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Jan 18 18:27:05 2023 +0000

    keep plugging away at dark mode

commit 2075c05f037c72614b4bbf98790182083225f37c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Jan 18 17:49:27 2023 +0000

    start properly implementing dark mode

commit 20622ecd6286361b5d20b1db6e2226f2cf1413e9
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Jan 18 17:37:44 2023 +0000

    inline

commit f90ed579d5e67f1ac26d8e5cc8be44612156edcf
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Jan 18 17:37:34 2023 +0000

    this doesn't need to be a variable

commit 7cae143a99930231657b98c83a353d89bddad55f
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Jan 18 17:34:28 2023 +0000

    remove some unused variables and files

commit 43b269612c9cdc81f591f593ee030635b8404e92
Merge: be7b7432 ba49cd6a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jan 20 21:11:09 2023 +0000

    Merge pull request #633 from alexwlchan/fix-html-validator

    Continue fiddling with inline styles, HTML validation, rip out the old approach and put in the new one

commit ba49cd6a6af4dd41c8682c0ebe9c8890bce13180
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jan 20 20:40:38 2023 +0000

    split the GitHub Actions caches

commit 51499ecf55191dd8c06a7854b3fdd518fcecf28d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jan 20 20:39:37 2023 +0000

    fix the pretty hr

commit d11f17904c044fff4d74d64b1c2a422d6ddde3b4
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jan 20 20:38:49 2023 +0000

    WIP get inline styles working

commit be7b7432b377dd9f9d8653eb3c2daf96b49c738e
Merge: 20fac7d1 26b001db
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jan 20 18:47:30 2023 +0000

    Merge pull request #632 from alexwlchan/fix-html-validator

    Fix a couple of issues flagged by the W3C HTML validator

commit 26b001db0f6bf580ec7d21ef5fab8a2ce784ec32
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jan 20 17:56:23 2023 +0000

    move the finatra example into the site

commit e3325c7e07c2864cb643d35d123996b78d70dcd5
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jan 20 17:48:37 2023 +0000

    add some new cards

commit 888ff5a47c0b263fab78edc0790a1f6fdef6f8ca
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jan 20 10:39:48 2023 +0000

    Move the 'skip to main content' link inside the <body>

commit 636f32699be3b7bf3fcc389d9ef92eac324f1b35
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jan 20 10:39:40 2023 +0000

    Remove some trailing slashes on void elements

commit 20fac7d161aebcc1132e5f4045b8b4a833b31ed5
Merge: 54ce83be a172f4bf
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jan 20 08:59:33 2023 +0000

    Merge pull request #631 from alexwlchan/tidy-front-matter

    Tidy up a bit of the front matter

commit a172f4bfa98813c76c0ff05eb0b0759d331cf3c6
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jan 20 08:57:08 2023 +0000

    whoops, those quotes were important

commit 1f5b3ee21b96b5845c1a8a383f7321e45b49f9c2
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jan 20 08:46:44 2023 +0000

    A bit more front matter tidying

commit 17baf1acd55dd8669c9573e45e1338b470f9842c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jan 20 08:45:51 2023 +0000

    Start organising YAML front matter into a consistent order

commit 54ce83be39aa500a1eba884854cc31d7dd57aba1
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jan 20 08:39:47 2023 +0000

    Remove the custom apple-touch-icon files

    Nice idea, never used in practice.

commit 86ec09daf37f628406e51b48b71d03905df5ea0f
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jan 20 00:28:22 2023 +0000

    convert a few images to RGB to shut up ImageMagick

    see https://github.com/ImageMagick/ImageMagick/issues/5987

commit ab82eb1e020db0a1faec69b43e8d3451cde4cba0
Merge: cf7f5fc8 902b727f
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Jan 19 23:07:47 2023 +0000

    Merge pull request #630 from alexwlchan/jekyll-cache-api

    Use the "new" Jekyll Cache API

commit 902b727f26f94ec12c20486eeb67fa803a1dc432
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Jan 19 23:01:47 2023 +0000

    cache the <details> tag also

commit 9e3b568ccd24c2793ef0a388fc8fae7fcdc518bd
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Jan 19 23:01:41 2023 +0000

    make rubocop happy

commit 3c299277967d01e305d312f626b63dc727c1a56c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Jan 19 23:00:28 2023 +0000

    Fix soem Rubocop violations

commit e3ec6305611cea60ab35f390c3a4a7247d67ddd5
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Jan 19 22:57:58 2023 +0000

    Use the Jekyll Cache API for faster builds

commit 3b30287225df37eff46006b04f8f0a1682d48353
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Jan 19 22:50:33 2023 +0000

    the :: is unnecessary here

commit cf7f5fc8d61283f48b09b6e26ae2cfc7e5f0b5db
Merge: d36618d7 9194b1d1
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Jan 19 22:49:53 2023 +0000

    Merge pull request #629 from alexwlchan/go-faster

    Make a few optimisations to improve the site build time

commit 9194b1d14458a4aefe32c2e483cb77f19899482f
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Jan 19 22:48:15 2023 +0000

    empty line after magic comments

commit 001c181787a78b659a802ec2012b37cf7f9acdb8
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Jan 19 22:46:43 2023 +0000

    unless, not if false

commit 86271c0e9e0e8b64a17e558aecc7a2887916eb11
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Jan 19 22:46:36 2023 +0000

    remove some dead code

commit 05ce3c971b909392882bc593fb8f69e2d00f033d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Jan 19 22:37:24 2023 +0000

    optimise the text cleanup regexes - less expensive loops

commit d72aa93024677e59e1b7f6991e0322b27acec215
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Jan 19 22:32:28 2023 +0000

    let's try freezing this string, making it a constant

commit 517ddb8bd976b7f641b6ee097d5341e6252982d1
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Jan 19 22:28:45 2023 +0000

    The entire site is in English; don't look it up every time

commit 3013cdc8e89aeb20655d6a7c198cfdbbdb8fcfca
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Jan 19 22:28:27 2023 +0000

    Cache the nav and footer; they're the same on every page

commit 41b750e356fd4a44cf2976c9f80eee81f08792ee
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Jan 19 22:11:21 2023 +0000

    Remove an unused `post__title` class

    There are no CSS styles that target this class, so it can be safely removed.

commit e3a78f92969ef3d0b527a12747dda458adfa4b37
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Jan 19 22:10:27 2023 +0000

    Cache the result of markdownify_oneline

commit bd8b3d458885c6b9752e58afbd7f975ff4fe41e7
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Jan 19 22:10:05 2023 +0000

    Cache a result in all_posts_generator

commit dbebc9d4773be451a0256d8fb0766a1bc6467d1d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Jan 19 22:08:12 2023 +0000

    Remove a now-unused layout

commit d36618d7a62a29d2295f6cb308207c75263af5f5
Merge: 0c3e6c1a ffa54df9
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Jan 19 21:53:34 2023 +0000

    Merge pull request #628 from alexwlchan/convert-more-images-2

    Swap out some more images to the new plugin

commit ffa54df92c1fee2e1976f22d83abf924cadb5e1d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Jan 19 15:02:26 2023 +0000

    Swap out some more images to the new plugin

commit 0c3e6c1a22b5c2af82ea13a1143cc63403de3a73
Merge: e2fe86af d1b514fe
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Jan 18 17:27:04 2023 +0000

    Merge pull request #626 from alexwlchan/refactor-elsewhere

    continue refactoring the CSS

commit d1b514fe52bc50f481ee3fba6b15e469b5984ac3
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Jan 18 17:23:10 2023 +0000

    tweets are unaffected by palette

commit c60d5bbddfb1f7ebc0a3a14e13d29b5bd6717699
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Jan 18 17:21:32 2023 +0000

    and move around some more styles

commit 520b97480e5e0c7a64d231c919d562e546c5e5a3
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Jan 18 17:10:51 2023 +0000

    consolidate some meta-y styles

commit 8665d00d38033f0b86631e35970b8fba285cec77
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Jan 18 17:05:02 2023 +0000

    move images wide into the base stylesheet

commit 9847bdbfa72ebc6cce074f52a457bd0f4994fe7e
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Jan 18 17:04:17 2023 +0000

    split the download styles

commit 3808a410a5bc7fa49d6e8f2b777789b9eed899b5
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Jan 18 16:55:01 2023 +0000

    remove an unused variable

commit 138528ed68b1100683cf45a7cf01699bca613f1e
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Jan 18 16:54:55 2023 +0000

    We don't need to replace <hr> in the RSS any more

commit e2fe86af4e5c22cb1b0bf865ebb505a0c04a6ede
Merge: 8cd8e7b4 fb825dd3
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Jan 18 16:49:00 2023 +0000

    Merge pull request #625 from alexwlchan/dark-mode-css

    Start refactoring the CSS ahead of dark mode

commit fb825dd3ace45e4d31f88ed1dcad30343c5758ff
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Jan 18 16:46:39 2023 +0000

    filter out some xml headers

commit fce1584902eac543b7dea5e8c812861b18b67b36
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Jan 18 16:45:23 2023 +0000

    we don't need this at all

commit 24fbc9d60997adbe1f7291515475003e254c9732
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Jan 18 16:44:40 2023 +0000

    fix some rubocop issues

commit d6a78127dc4acb02dc67d317e986c3ba97d06e00
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Jan 18 16:44:04 2023 +0000

    move some more stylesheets around

commit db3ec3f8bbd19a598f5736e8601f9462eadc5a15
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Jan 16 18:22:49 2023 +0000

    tweak tweet styles a bit more

commit fc07dcf0ba42c2239740dc9703cf86243eb83260
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Jan 16 18:01:36 2023 +0000

    Add the dark mode styles for Twitter

commit 24fe689aa242269fb162bda2964711c695f2c876
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Jan 18 16:38:22 2023 +0000

    port one tweet change

commit b7268e745445b6d9e2f29eac76da1857ee2a83b5
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Jan 18 16:36:57 2023 +0000

    move more stuff into the base stylesheet

commit 54ab0d926258260c33c54ef0441b3aa161c7f63b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Jan 18 14:50:38 2023 +0000

    start pulling out the palette-independent css

commit 620d63d60cbe29660294758a1844e31a87d16f3e
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Jan 18 13:04:31 2023 +0000

    consolidate a few more styles

commit 82012f8b5adff9104a79de17f49679de610a254e
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Jan 18 13:02:35 2023 +0000

    remove some more unused styles

commit 903dd21f0a3fcb58be976c3a819e6ba7b84a66ea
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Jan 18 12:03:18 2023 +0000

    continue tweaking styles

commit 51bc5792678008e3f04f185310b7fa7b57413481
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Jan 18 10:09:00 2023 +0000

    remove some now-redundant overrides

commit 3d22bc203c85a52674dcf1d84520dca5781289db
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Jan 18 09:57:39 2023 +0000

    consolidate some existing CSS

commit e5c58192aaec0707fa95adb4aad0899f6ad4a6d0
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Jan 18 09:33:50 2023 +0000

    continue fiddling with the homepage separator

commit 73cbeb9e7257821c9a4cb13614b002566aa36d44
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Jan 18 09:31:14 2023 +0000

    remove an unused icon

commit efefd7b80f0b4c99e09979586ef25ec3d68f41bb
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Jan 18 09:31:09 2023 +0000

    remove the now-unused text_separator tag

commit ac539c5c4727295db56ca6ceb6c7822e3b46592f
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Jan 18 09:30:47 2023 +0000

    Replace all the uses of custom separators with simple squares

commit 8cd8e7b4935e850cc14ce0a042c2ab98feafd2f5
Merge: 67c269a8 b39150e0
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Jan 18 16:26:56 2023 +0000

    Merge pull request #624 from alexwlchan/combine-talks-and-elsewhere

    Combine talks and elsewhere

commit b39150e0cc118401795111d9efee5c6bbf06c952
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Jan 18 16:24:49 2023 +0000

    add a comment

commit 8e46f902713ece4896fa3dd5a66eddc6170939ac
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Jan 18 16:24:10 2023 +0000

    ignore url fragments when linting

commit 721dc8a4b0752e1dcbff56650b3a60b4906c5446
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Jan 17 18:51:03 2023 +0000

    Consolidate the info on talks into elsewhere

commit 147003ed7e2a0e33e8bfea2cf07eca54491e4c6e
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Jan 17 18:44:59 2023 +0000

    remove a redundant bit of template logic

commit 399e133b81b0980106f955dce108bbad6ef30a9c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Jan 17 18:44:53 2023 +0000

    Move my speaking photo to the "projects" page

commit 67c269a8154bdcec2d997c00efa26b3385529cee
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Jan 17 22:44:11 2023 +0000

    another post to the new picture plugin

commit 1b306b6a1c4db6cb0eb16d13e9aa94983c494311
Author: GitHub Actions on behalf of Alex Chan <githubactions@alexwlchan.net>
Date:   Sun Jan 15 21:46:18 2023 +0000

    Publish new post check-for-transparency.md

commit 1222b9db16e1c471c5d2e3a8f423aed55a12e5ba
Merge: 61982480 2ce52fc7
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jan 15 21:44:06 2023 +0000

    Merge pull request #622 from alexwlchan/check-for-transparency

    scribble a quick post about IM6 and AVIF transparency

commit 2ce52fc7fc98be2696ed0baa2a6579988331f902
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jan 15 21:43:12 2023 +0000

    remove an unnecessary variable

commit edbe83102502bce067bca02765307a65b5602119
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jan 15 21:41:33 2023 +0000

    scribble a quick post about IM6 and AVIF transparency

commit 61982480eae4b351397fc6dad29539c8475c9565
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jan 15 13:57:17 2023 +0000

    flush the images so that old images are reloaded

commit ed21708917cda0761e58386fce00ed3d215a8148
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jan 15 13:15:21 2023 +0000

    and now rebuild them with the new image

commit b69b456e403dada6bd639993667f45f6cf3a90ff
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jan 15 11:59:27 2023 +0000

    just blat them all

commit 8c3d7936ecb16ff718b789d8d797ea2b19bf9a1d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jan 15 11:57:40 2023 +0000

    add a missing newline strip

commit 1dbfa5ea60dca81a2fc582d336952506368e97b1
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jan 15 11:54:10 2023 +0000

    flush all the AVIF images from the cache

commit 7685ecb2a68ba3110ea680fabd5a61342bc5f2a8
Merge: 829437e9 8ea1455e
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jan 15 11:50:54 2023 +0000

    Merge pull request #621 from alexwlchan/check-for-transparency

    Fix an issue where AVIF images are getting black background, not transparent

commit 8ea1455e4f1fb77c3d43fa5130ec83d42de03da2
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jan 15 11:45:18 2023 +0000

    Compile a new version of ImageMagick 7 from source

commit 0eba87f87dd8b048d204c6317975b485c7a8c709
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jan 15 11:39:42 2023 +0000

    Add a lint to detect when transparent pictures are de-transparented

commit 829437e9315e421abba1c369bfb4049e055942f8
Author: GitHub Actions on behalf of Alex Chan <githubactions@alexwlchan.net>
Date:   Fri Jan 13 15:23:18 2023 +0000

    Publish new post upward-assignment.md

commit b25641aa3f3c1a87dcb98153ffced6ea0f8e630e
Merge: 713dc462 7af34dd8
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jan 13 15:10:09 2023 +0000

    Merge pull request #620 from alexwlchan/vertical-assignment

    Upward assignment in Ruby

commit 7af34dd8b5d6330b6b218940456c39e255c32f5d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jan 13 15:07:11 2023 +0000

    add some missing alt text

commit 3e4675183e17f1861198bd534dc0df28983ef042
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jan 13 15:04:00 2023 +0000

    fix some formatting + blockquote stuff

commit 87f93a7f0c1cbd525d3ce159b15b43599c35a49b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jan 13 15:03:42 2023 +0000

    fix a URL

commit f2868f765412cd1f783b83249c0ecd689f61dc29
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jan 13 13:49:42 2023 +0000

    add the full code to the post

commit f9f5d7761f0b2670320c3c638599f0eee9373056
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jan 13 13:17:56 2023 +0000

    final batch of edits

commit cc6cd37c12b534f34a83c3badfcd01e42575a61b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jan 13 12:23:14 2023 +0000

    more markups on upward assignment

commit 5ea35d4e43dc3d8cee1b83d960edcd69027d6b0b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jan 13 08:38:23 2023 +0000

    edit the first section

commit 33f47e14cab39db55462d6620bc13351f21b4d75
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Jan 12 22:11:09 2023 +0000

    add a conclusion to the post

commit b2b5b16561aec07572e563503418c0adca99f7b4
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Jan 12 20:00:44 2023 +0000

    more upward assignment

commit 49a68cdfb30e1af860f83521604de415e278d896
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Jan 12 17:30:01 2023 +0000

    continue writing the post

commit 07642521f30156b1a96fe1d60cc319752b7489b9
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Jan 12 10:43:05 2023 +0000

    continue writing about upward assignment

commit 1a2610e6a1c9d8743b797b3a800384ee9ffd94ac
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Jan 11 20:35:05 2023 +0000

    continue writing about upward assignment

commit 8a7dfe3acd2d606316b2647b4f96ecc99b600179
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Jan 11 19:49:24 2023 +0000

    add the look up image

commit 003726a01961ae1dd6afd4ffd4d772a8e66a899e
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Jan 11 19:16:55 2023 +0000

    continue fiddling with upward assignment

commit 02f65849ba8f116be241a1a6acd54fcdeb75bcaa
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Jan 11 09:08:01 2023 +0000

    Start to write the vertical assignment post

commit 713dc4622c6a85ed52eddd8cf975c66d4673698f
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jan 13 07:59:17 2023 +0000

    make the footer icons look good when styles are disabled

commit 1c2dfbe7bf6efd88a9412b7e901e88caffb769e5
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Jan 12 22:56:48 2023 +0000

    make rubocop happy

commit b51ccaf978be4eccdada83103225093e12fb9e97
Merge: c6520d4f b026aba6
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Jan 12 22:56:07 2023 +0000

    Merge pull request #619 from alexwlchan/inline-svg-2

    improve the inline svg tag

commit b026aba682b9a4001e672f93234bf9ceac959e7c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Jan 12 22:52:54 2023 +0000

    now get rid of the old inline svg tag

commit 812fdfbfb5c7246de0d5ed3d3c6012eb2010bfe2
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Jan 12 22:50:20 2023 +0000

    fix a couple of bugs

commit f7248f94396749b4740e03079513facce90b6c03
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Jan 12 22:48:06 2023 +0000

    and fix one weird example

commit ec5d91d1a7fa2c31279447f568d2c8471afd7235
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Jan 12 22:47:00 2023 +0000

    convert a bunch more svgs to inline_svg2

commit 0fb34861a9a24ab5f479b1fa135903c75daac55d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Jan 12 22:45:06 2023 +0000

    convert all the generative art svgs

commit 7df08c3621f94b2d508cfbc412eca63626abc017
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Jan 12 22:42:07 2023 +0000

    migrate another example

commit b01a78e255a9ebc76a3683efe282ff6255bc263a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Jan 12 22:40:06 2023 +0000

    migrate another example to the new plugin

commit 9b4ac036a1151c7a1b6b8537f74c9674e0d640f5
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Jan 12 22:34:33 2023 +0000

    migrate a single example to the new plugin

commit 180ea2aff60281a8dec5db47521642cefda77bec
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Jan 12 22:33:22 2023 +0000

    start using the new inline_svg plugin

commit c6520d4f31605729e5f22f885ea2909be548e7d9
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Jan 12 21:49:19 2023 +0000

    and email also

commit 4327228b44f0e46f5aebf892015f56d2ca57f871
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Jan 12 21:49:19 2023 +0000

    remove a dead line of css

commit 5414dd3dad4bf7a499299ca63e7633f216cbc18b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Jan 12 21:49:14 2023 +0000

    fix a small visual incongruity in the rss icon

commit 22b41885d9c1b22db8b30833b9168a3b3eeb13d3
Merge: e3ce3dcd 936771b8
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Jan 12 19:57:10 2023 +0000

    Merge pull request #618 from alexwlchan/colourful-footeer

    make the footer bright and colourful; tidy up icons

commit 936771b8792dabef52ba121e5e3ace7b63879b79
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Jan 12 19:53:58 2023 +0000

    make the footer bright and colourful; tidy up icons

commit e3ce3dcdb24f2223fc8c4526a60de6e16e5a17ef
Merge: 39414d1e f15a8cd8
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Jan 12 19:17:57 2023 +0000

    Merge pull request #617 from alexwlchan/download-tag

    fix the download tag

commit f15a8cd8d8a755af7d9528a80b64eca79b171532
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Jan 12 19:16:13 2023 +0000

    make rubocop happy

commit bc172a0d512a952ff306ae95e0fc5f386fdf9486
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Jan 12 19:15:03 2023 +0000

    use the new picture tag in this post

commit b20ffeed78537507977968370f0975f460a64652
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Jan 12 19:10:36 2023 +0000

    bring the download tag into line with my other plugins

    (and fix it!)

commit 39414d1e9b4f613daa16c1b01f510138eccdd5d8
Merge: b626d6c9 4e372051
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Jan 11 19:53:51 2023 +0000

    Merge pull request #616 from alexwlchan/align-inline-tag

    Make the plugin structure a bit more consistent

commit 4e372051e83df3c7fdf915d1caa1d28927700ebd
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Jan 11 19:46:56 2023 +0000

    fix a broken import

commit 3d81b513794e7be730c2be68ee52823c9c92e876
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Jan 11 09:08:09 2023 +0000

    Make it clear I don't care about these attributes

commit 3311b584391e3f0d513edd0507f8fd644b64106b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Jan 11 19:44:45 2023 +0000

    fix a couple of rubocop warnings

commit 61633ac9a4efe0b51e4680d8e3c852db6688f371
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Jan 11 19:43:12 2023 +0000

    more consistency in tag naming

commit 37977a70ce1459eda4d74b1999828ea651b8ca8e
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Jan 11 19:41:24 2023 +0000

    Tidy up the Markdown filter

commit e20342d43230acdb380c59fe4f8cc08867b0e417
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Jan 11 19:37:36 2023 +0000

    Rewrite the inline_code tag to be like picture

commit 1503e6959d717b5b086619c304f2d39de1bc9810
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Jan 11 19:28:24 2023 +0000

    Add a description to the cleanup_text filter

commit 463165435809ea2fed722e4559740f99be4ad3aa
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Jan 11 19:26:13 2023 +0000

    Pull out the smartify filter into its own file

commit da63148ffbc8b481956ee5f97f98f92965fa1fb3
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Jan 11 09:08:01 2023 +0000

    Start to write the vertical assignment post

commit e38c157ec853fc8e1bcb7db689d29c171dddc8b8
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Jan 11 19:19:20 2023 +0000

    Move some utility code into a utility folder

commit b626d6c9adf2251a190db32e97e7158c987b0dd3
Merge: 729fc50f 45f79d20
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jan 8 11:45:22 2023 +0000

    Merge pull request #614 from alexwlchan/no-more-per-month-posts

    Stop putting the month in post URLs

commit 45f79d207780b675e85d4eed6c6dc4358df33e9e
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jan 8 11:42:19 2023 +0000

    fix a couple of old redirects

commit af75bdd4a1e259f303af3344a691c73a3d816fa1
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jan 8 11:40:21 2023 +0000

    fix a few more post URLs

commit 47f6e02ded29f5f34302d0c21831074f894466bc
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jan 8 10:56:24 2023 +0000

    I can also remove per-month archives

commit 4f4522555ee5c762bf35d3ae2d1832767c8e1a06
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jan 8 10:53:52 2023 +0000

    Stop putting the month in post URLs

commit 3c87807569b509a62b4f97d2235bc6b9f19a23cd
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jan 8 11:27:50 2023 +0000

    Add a missing {% post_url %}

commit 729fc50f1f05977126fca784b0d33d0d5954f7cc
Merge: 14dbb7e8 1d2209ae
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jan 8 11:27:40 2023 +0000

    Merge pull request #615 from alexwlchan/use-post-url-jekyll

    Use Jekyll's built-in {% post_url %} tag

commit 1d2209ae72f14e2c3171aafa389fc44a8561fe2d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jan 8 11:24:06 2023 +0000

    Apply {% post_url %} everywhere in can find

commit affd95b321f99000c3182ed1b3e96200c7cf44eb
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jan 8 11:11:19 2023 +0000

    Convert another tag to the new {% post_url %} tag

commit ee378faac45ca81da5d68f0d16ce21fc811d4187
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jan 8 11:10:29 2023 +0000

    Fix the formatting in an old post

commit 2e30d18803a0a23ca035c2c4a565586ad792141d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jan 8 11:10:21 2023 +0000

    Start using Jekyll's {% post_url %} tag

commit 14dbb7e8d13f4d947ec6b43b86dc9ffe2d8f268d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Jan 7 18:50:19 2023 +0000

    Update 2022-10-05-snapped-elastic.md

commit 7d2834d8d69c2a1db9722e1e980c4d3b2a048b43
Merge: 7f644605 68d0aeca
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jan 6 15:03:44 2023 +0000

    Merge pull request #613 from alexwlchan/more-images

    flip a few more images to the new plugin

commit 68d0aeca6334b106c975d432804fd8a91ef97e65
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jan 6 14:59:10 2023 +0000

    flip a few more images to the new plugin

commit 7f6446055c2e1b39033828e34c444f71f4692b40
Merge: 72970b33 45f6c02f
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jan 6 10:31:23 2023 +0000

    Merge pull request #612 from alexwlchan/more-images

    fix a few more images

commit 45f6c02f23f34f269b401d9542a149773e67f1ee
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jan 6 10:28:28 2023 +0000

    fix a few more images

commit 72970b3352a26b36856466bd03dcf4fed4622556
Merge: bf7a8069 b4b93659
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jan 6 08:50:54 2023 +0000

    Merge pull request #611 from alexwlchan/more-rubocop

    continue fiddling with rubocop rules

commit b4b93659715abbd5abf27e28e7ce6d89eef54d26
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jan 6 08:46:59 2023 +0000

    remove some unused code

commit 17e37bfe65baedb790d36372bf047ca9960cb141
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jan 6 08:46:47 2023 +0000

    Set an explicit max line length

commit bf7a806987c4058fd4b790fb7c6f2f088e66b36a
Merge: 6d8050e2 17e9beac
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jan 6 08:43:00 2023 +0000

    Merge pull request #610 from alexwlchan/fix-images

    Convert some more images to the new picture plugin

commit 17e9beac99082ffd125e305a686348d58768c565
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jan 6 08:39:10 2023 +0000

    jobs, not queue

commit d870351c7e004ccd926beee1924512aaaee7e606
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jan 6 08:34:54 2023 +0000

    and another image

commit 40ba539748b0b2865f638d4002e50e6745e0b846
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jan 6 08:32:51 2023 +0000

    convert another batch of images across

commit ce2ade6c0f3c7fd0b198870fc1e70cbac8d039eb
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jan 6 08:28:34 2023 +0000

    flip another couple of posts to the new picture plugin

commit fa0e8d8dd46f88c479c62244fdbb69b29aaafbba
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jan 6 08:21:21 2023 +0000

    fix a few issues on the crossness post

commit 4b0ea3e3830e7c58a551591ade82279bbab11447
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jan 6 08:18:59 2023 +0000

    Log the number of images being created

commit 6d8050e28795a3a2928e976786644b12178be9a9
Merge: 5743c7a5 48689feb
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jan 6 02:53:19 2023 +0000

    Merge pull request #608 from alexwlchan/more-images

    convert some more images to the new plugin

commit 48689feb9607fedbb76a01d6155d5e96e400c294
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jan 6 02:50:35 2023 +0000

    use single-quoted strings

commit 97400bc757c2a82aaabebcd2d168c3aeb39c3553
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jan 6 02:48:23 2023 +0000

    convert some more images to the new plugin

commit 5743c7a519cbf9ca72da2345a6654bb779806776
Merge: 3eaec71f ec04dfd3
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jan 6 02:28:53 2023 +0000

    Merge pull request #607 from alexwlchan/increase-rubocop-level

    Increase rubocop level

commit ec04dfd326c41a3df6ad8d735fbd9b9e5b910b2a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jan 6 02:26:40 2023 +0000

    just run rubocop on the defaults

commit c16c62f541d2baccc298c00bd7c216e4e028328c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jan 6 02:25:58 2023 +0000

    continue making rubocop happy

commit 684075fafbc7d3aa50daebda0717dbba9f2aa49a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jan 6 02:24:18 2023 +0000

    fix a bunch more rubocop suggestions

commit 889e7d546cf7c42a33e6f3eba8126022929aebb0
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jan 6 02:06:05 2023 +0000

    fix some issues flagged by rubocop

commit f61c8765dc73a5f47d9edb78bfa52b70ce2bb077
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jan 6 02:03:30 2023 +0000

    exclude some rubocop checks

commit 24b722c4f9f4182f9269fc065606ed17d978e46a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jan 6 01:51:38 2023 +0000

    Run rubocop --level C --autocorrect

commit bbf8b192f09ed19bb1c816dfd5bdbd09e475184b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jan 6 01:46:44 2023 +0000

    increase the rubocop level to WARN

commit 37bdd41c9a00db52c0256a491e4e2b39419d8285
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jan 6 01:46:34 2023 +0000

    rename the rubocop workflow

commit 3eaec71fd6ed72ab82ef9362f40f60d473bc6132
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jan 6 02:06:41 2023 +0000

    these are now 1x ignores

commit 683c93bd342e976cbfc2e876a8d9b2c0128009ad
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jan 6 01:55:38 2023 +0000

    fix a couple of build issues

commit 5e2449ee4a17736ca666749c2269aec5afedec4e
Merge: 117a19a4 d5edfc18
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jan 6 01:46:40 2023 +0000

    Merge pull request #605 from alexwlchan/tweets-with-pictures

    Use the new picture plugin for tweets; use a proper grid layout and not tables

commit 117a19a48503bde97a58cfdeb7fe1f76a81513c7
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jan 6 01:45:47 2023 +0000

    uncomment the build site workflow

commit fb710490b4d3618e4f670d2c17efb7f3fcc49daa
Merge: 1e913e01 6e10c01a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jan 6 01:45:25 2023 +0000

    Merge pull request #606 from alexwlchan/ruby-linting

    Add a workflow to lint Ruby code

commit d5edfc18ec9533f14b215a92c0c327e544ea8cc5
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Jan 5 23:06:04 2023 +0000

    add alt text to tweets properly

commit e15dae810ff0cb21cb187fa0fe85040bfb088537
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Jan 5 22:38:52 2023 +0000

    use the new picture tag to render images in tweets

commit 6e10c01a02b762fcf189fbc1d79c0e47cb20f380
Merge: fdb48ec2 1e913e01
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jan 6 01:40:45 2023 +0000

    Merge branch 'live' into ruby-linting

commit 1e913e01568068aa4a52a8b3f2630e3542c7684a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jan 6 01:36:59 2023 +0000

    10 to 5

commit 11b249fd3e41986c147de85ab54964a38d91dd5d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jan 6 01:33:02 2023 +0000

    Revert "get it working for now"

    bd6bf56e95a28e445e10f0254f2ba85099852274

commit 38b97dbbef8650ae50eacc0e90e8b6bb10e8993f
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jan 6 01:32:54 2023 +0000

    Revert "Revert "and there go two more posts""

    1f8f3b0b669eef5acf2d0ea08ed3278afeb87a29

commit fdb48ec2b646ff2f06cfebd3a89d582c41bf8e1c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jan 6 01:16:12 2023 +0000

    don't print messages below the current level

commit e2fe93d1d22b1c71879d8e1d6f4d45cc4daf006b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jan 6 01:13:14 2023 +0000

    Fix a bunch of issues flagged by rubocop

commit f099cdefd7f083ed0eed6f6b2d590b951e8f49b6
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jan 6 01:00:16 2023 +0000

    only fail rubocop on errors

commit 8b7e4ca30ac568e95e644d37979429d635dce5c9
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jan 6 00:37:37 2023 +0000

    fix the name of the workflow

commit dada839c345efc9ff48ab6900810a343bf5d4e7b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jan 6 00:34:59 2023 +0000

    specify a ruby version

commit f17fcf3376a49699de013255d3378837113dca68
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jan 6 00:33:53 2023 +0000

    actually run rubocop

commit ebd7f5ca1d429beba829635f69d102e8afd95890
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jan 6 00:32:20 2023 +0000

    Add a stub workflow to lint Ruby code

commit 32b1e1c735a83d07d4cb9eae35ac50af191d3067
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jan 6 01:17:41 2023 +0000

    and exclude from front-matter linting too

commit a4e277d9945be179b0f5ed715f138024b11d30a0
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jan 6 01:05:26 2023 +0000

    fix this variable once more

commit 9d5bf339cddad66b1b782bbc7df4e81ee1542879
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jan 6 00:46:41 2023 +0000

    Revert "and there go two more posts"

    d25605a825cded0c963b6118e6f59242e90f956b

    Revert "some more posts go to the new picture plugin"

    2489b8e136e5253c8ea72ddafec844649245935b

    Revert "convert the ICNS colour post to the new picture tag"

    d116af48a50b53e79aedb55d12afd54cf4294241

    Revert "fix the aberdulais waterfall photos"

    281fc81e287a386d561a83532c108a2bbd4e0e43

commit d0ad215f68e6b8f842cfaca3a3e8b99840b800ee
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jan 6 00:46:21 2023 +0000

    add the html_path variable

commit 1ff4d68dd156fbc3425209921a597353b715f11e
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jan 6 00:33:08 2023 +0000

    fix a missing variable in linter.rb

commit c97959703764ce212cbc774b52a9a643bce054e5
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jan 6 00:25:15 2023 +0000

    fix a linting issue on /400/

commit 1dfb24917c406b428960606174c891ec689c19d2
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Jan 5 23:31:00 2023 +0000

    get it working for now

commit 43e3c5d176a471a73f6a8157fc99933d25cc2dc8
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Jan 5 23:47:22 2023 +0000

    fix a missing variable

commit ce66ea94f96286c7a879745f03603f86c4ddb2f1
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Jan 5 22:17:12 2023 +0000

    and there go two more posts

commit fc4055797afc0be3b92f4d80c53c56d307b6d7b3
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Jan 5 22:08:21 2023 +0000

    some more posts go to the new picture plugin

commit d4ce003c46de9bff67bfced76ee96db70e7faadc
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Jan 5 21:47:51 2023 +0000

    convert the ICNS colour post to the new picture tag

commit f557b6cae934b93602c396a8f3b5184b24203937
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Jan 5 21:42:00 2023 +0000

    fix the aberdulais waterfall photos

    don't use this dastardly image layout, also one of the images is repeated!

commit cf29857ae55d8004b47259acc228372fe6f3800d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Jan 5 21:33:38 2023 +0000

    add another missing redirect

commit 66efdbe986e2f029165354645b66a2f7ccab451d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Jan 5 21:33:33 2023 +0000

    better error for missing image

commit a7d7b2f290194c24e388017201a54d970185e18c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Jan 5 21:33:27 2023 +0000

    reduce the size of the crossness post

    * images are now loaded with the new plugin
    * the video doesn't load until it starts to play

commit dcf56222871a229339afd3e36f46f024cbdcc2a4
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Jan 5 21:31:24 2023 +0000

    Don't waste bandwidth on the 400 page

commit c5ae85a6b7f63a3237d017582fd3acfde0f4d770
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Jan 3 22:25:31 2023 +0000

    sort out a couple more redirects

commit 9d188ad3dfb1f79db30263d8cceeca8651414eac
Merge: b1708fdc 3c305fe0
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Jan 3 18:51:51 2023 +0000

    Merge pull request #603 from alexwlchan/experimental

    keep fiddling with styles

commit 3c305fe0fbeb2f57ae8fae7e9090d44cc092c6aa
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Jan 3 18:48:56 2023 +0000

    add some colour to code/pre

commit 9315c52b719fc89cfa6ab513ba97e21ddaf3ce3f
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Jan 3 18:40:12 2023 +0000

    experiment with a more radical change to code styles

commit b1708fdc793092278a13a22e76209fde66fd6440
Merge: 0896c9e7 95349bbf
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Jan 3 18:42:16 2023 +0000

    Merge pull request #602 from alexwlchan/css-fixes

    tweak a couple of css things

commit 95349bbfc8a147eb4aeb020f1aff6883c12602fa
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Jan 3 18:35:26 2023 +0000

    tidy up the way link styles on code work

commit 6c02cfb1d232647edf7b6391a985797c017fec50
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Jan 3 18:26:53 2023 +0000

    add curved corners to <code>

commit b5ec1c79921858e2504bc00cd69bd2bc88c55964
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Jan 3 18:17:57 2023 +0000

    add a default background to download links

commit 251b4917a5d3d9d7c5de06679de04b1d9377282a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Jan 3 18:16:28 2023 +0000

    use another variable here

commit eef6c7b16bd58e20600ad03ced66cb5686352e38
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Jan 3 18:16:20 2023 +0000

    move the link styles into _links.css

commit 6be971053e3d177e1386afe98c129577240a4ca7
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Jan 3 18:16:08 2023 +0000

    new image plugin, formatting

commit 0896c9e7fd1a8ca6d2bbc1c03bd593dd7ea7186c
Merge: 4b4875f2 814306e9
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Jan 3 16:36:29 2023 +0000

    Merge pull request #601 from alexwlchan/css-tweaking

    Rejig how the CSS is handled

commit 814306e96e0de91092bce1089d44bee23d26367e
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Jan 3 16:33:21 2023 +0000

    Rejig how the CSS is handled

    *   Each page now gets a single file with all its CSS, which is
        concatenated from the base CSS and per-post CSS
    *   Each CSS file is now tagged with its own MD5 hash, rather than
        a fingerprint for the overall CSS, which should improve cache rates

commit 5f95f47aea53c9b31d53c6593a098e33876202ed
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Jan 3 12:57:21 2023 +0000

    swap out some images on the twitter card post

commit 4b4875f2889abe908d9bc5252a57f76c32523a7b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Jan 3 11:14:09 2023 +0000

    add a todo note

commit bd64733e61344d1e962fb59970d92641aecfc14f
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Jan 3 11:13:17 2023 +0000

    fix an issue with aspect ratio

commit 4fb7d94e276d0ee8d50f0efb63f394e650fc966e
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Jan 3 09:44:18 2023 +0000

    heck yeah, drop shadows

commit 74ce44f9af4819d2adf5805cce7f1dd963e00a44
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Jan 3 09:44:13 2023 +0000

    remove some trailing whitespace

commit c403eea15a16b3cbae2eed4630d7f4e34153be8a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Jan 3 09:44:09 2023 +0000

    flip another few images over to the new picture plugin

commit 2f53abb63c7b6cc142c77ea07fd05b8909c3f83d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Jan 2 20:15:36 2023 +0000

    convert another two posts to the new picture plugin

commit 0c7360b35b7a754440bb34176d14507e86182ce4
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Jan 2 15:23:25 2023 +0000

    new picture plugin in the maths sampler

commit 8d7a5d6cb25cc3bf887bd7239df47e3cae6058af
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Jan 2 15:22:34 2023 +0000

    remove an unused image

commit d7c300e64acc8a53b4d8a13024e7c559f60f67bc
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Jan 2 15:21:54 2023 +0000

    convert another image to the new plugin; make it work in 3x

commit fa72fe7aebe9f95fec7ecf19dbf9d6817b07859d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Jan 2 13:42:10 2023 +0000

    flush all requests for /wp-content/*

commit 933192951aac6005f008d0d936231ae85c1286ff
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Jan 2 10:02:22 2023 +0000

    clean up some more redirects

commit 80802624b0846e04541f2c6fe983eb3538171d5a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Jan 2 01:22:21 2023 +0000

    remove a typo

commit fe9ac3784725f6c83d553ba1b92aa5facc00daae
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Jan 2 01:10:37 2023 +0000

    this should be .jpeg

commit 69f75221feacd8aa6b2c046f1354dd3c5d3d522c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Jan 2 01:10:03 2023 +0000

    add a bunch of missing redirects

commit e784a9263180d7ba891a0cc01bba836ca88198a6
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Jan 2 01:03:28 2023 +0000

    Add a missing closing quote

commit dae4f0f17821c13bb55fb4518dc908e864b68548
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Jan 2 01:02:34 2023 +0000

    tidy up images on the old veil post

commit b8b673290b4096ae37b36785221f456d4bfc8b2c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Jan 2 01:01:03 2023 +0000

    Add a lint rule for Netlify redirects; organise them better

commit 8316687686102c4a6350dd31bf9c67bb431bc27c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Jan 2 00:35:28 2023 +0000

    fix a couple of years

commit fb83ba48e97b4cb0e94e69d02b009b086e56180d
Merge: 06381412 a014ec8d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Jan 2 00:27:44 2023 +0000

    Merge pull request #595 from alexwlchan/sans-alpine-jekyll

    Improve a bunch of build image stuff

commit a014ec8dc360ab28e95489ed2469aefe17d380e9
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Jan 2 00:25:14 2023 +0000

    Fix a bunch of straggling build issues

commit 594e83fae4080e4df5882f7d1c9361f50edb9ffa
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Jan 2 00:10:38 2023 +0000

    add a bunch of missing redirects

commit 305b65c52f60408c603852873b35e64e5219f5b7
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jan 1 23:51:46 2023 +0000

    fix the Docker image tag

commit 48403213b649effd10a8c4b43bc34ec86b908630
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jan 1 23:48:25 2023 +0000

    this shouldn't be a backticked string now

commit 460ef85c07b3e49445ded8798bc9d700bea3bc4f
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jan 1 23:48:05 2023 +0000

    Remember to remove the old ICO code

commit 2c65eba6b843c5918937b91dc582aa959b1aef8a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jan 1 23:47:49 2023 +0000

    Remove Perl from the image also

commit 5f66c11c90efc1486eb48ee83e36c6376e532846
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jan 1 23:09:47 2023 +0000

    Get a Docker image building with a Debian base

commit 3fd695bcf14000040fb9e6844b9bcb10ffbaac93
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jan 1 22:38:09 2023 +0000

    Fix some warnings flagged by the CSS checker

commit b7da79c1f8eb484c71cafade6b35242a8bb9da85
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jan 1 22:36:43 2023 +0000

    Fix a couple of warnings from the new version of Sass

commit f8fa42ee5034ec23a7cab30db6d857057f50073e
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jan 1 22:33:15 2023 +0000

    Add some notes on some Sass warnings

commit 29447f81b512108b78b039be845df2bc18030d5d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jan 1 22:07:34 2023 +0000

    start fixing sass deprecations

commit 179626e3e92d57ee4d7a8ffd66e664230920dabb
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jan 1 22:02:48 2023 +0000

    note some extra commands to run

commit 0cc3a37a20635fe7e5e725ee6ec38454ac7245df
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jan 1 22:01:57 2023 +0000

    Get a working(-ish) build with Ruby 3.2 and Jekyll 4.3

commit 39b97cb1a9c036df32cf934195ff039763003c74
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jan 1 21:49:23 2023 +0000

    Bump the version of Jekyll in the Makefile

commit d493677f84e29b21116ecbf08901225806402113
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jan 1 21:48:09 2023 +0000

    Bump the version of Jekyll in Gemfile.lock

commit 0638141244ca8b445234e383dcae9e411ef62254
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jan 1 21:12:55 2023 +0000

    fix a couple of broken links

commit e9843dd0a330765c1ce1564af8845e1b42f91ab3
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jan 1 20:31:39 2023 +0000

    Flip a couple more images to the new plugin

commit 9d6a609b33edc7c748fa7fc58d05917d52d4e222
Merge: 52cbabee 79007bb7
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jan 1 20:22:07 2023 +0000

    Merge pull request #592 from alexwlchan/fix-grayscale-image

    Fix a warning about grayscale PNG profiles

commit 79007bb7d638b0e54742f27e47c63709110cedc7
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jan 1 20:19:54 2023 +0000

    fix the warning about a colour profile on an image

    closes #590

commit 73468b060ad4fbb4e05e0ca84ae6c5e345206564
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jan 1 20:19:33 2023 +0000

    Check all the _output_ images, not the source

commit 52cbabeef3b88180d0906911c544e617b5a83ef9
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jan 1 07:57:08 2023 +0000

    fix images in the Egyptian mixtape post

commit 40e6d1864f1cd9fc750cd606c6d10cfb6b530399
Merge: 5ea43bbc 3038afb0
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jan 1 07:48:21 2023 +0000

    Merge pull request #591 from alexwlchan/fix-what-year-is-it

    Fix a few issues in the 2021 "What year is it?" post

commit 3038afb02e512c5d46990f20fce919d9e837e465
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jan 1 07:46:33 2023 +0000

    fix the title of the post!

commit be689d0b157915aacad209f4c0241bba2335e202
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jan 1 07:45:48 2023 +0000

    use the separator plugin; remove unused styles; expand spacing a bit

commit fb40272f8d33fb80525ea6f2c0cb9b93aae61dd5
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jan 1 07:41:41 2023 +0000

    Fix the slug on the post: 'is it', not 'it it'

commit 5ea43bbc366fba0c13baf11ce27ed3a143e014d1
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jan 1 07:37:38 2023 +0000

    this is a jpeg, not a png

commit 0821c4b853e49dd0a480dd354cb859a23195a418
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Dec 31 23:11:02 2022 +0000

    smaller images in the artichoke post

commit c3328655a4843e6f986026c1c26c453b5a821363
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Dec 31 23:07:11 2022 +0000

    tidy up a couple of styles

commit 4463f46821752b44681033f909ee678d10f8fcb8
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Dec 31 22:05:24 2022 +0000

    srgb-ify again

commit 8eecde25c958f934784a2713a63faf82a5479917
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Dec 31 19:20:14 2022 +0000

    fix the front matter

commit 45e43ecf4abc82e76d2f1431f75ceee4ecee44b5
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Dec 31 19:18:18 2022 +0000

    better summary for 2021

commit 6138e681c8ee4016e7846012671c0fbe8140bf7b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Dec 31 19:01:45 2022 +0000

    this needs to be srgb

commit 1d5f6c03fcbc8b3671d35c057d08fc8365e91a9f
Author: GitHub Actions on behalf of Alex Chan <githubactions@alexwlchan.net>
Date:   Sat Dec 31 18:47:55 2022 +0000

    Publish new post 2022-in-reading.md

commit 9be52f358bb22e06146fdc2eae24783c826beefd
Merge: 9783a53e 5ed8ddf2
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Dec 31 18:45:11 2022 +0000

    Merge pull request #589 from alexwlchan/2022-in-reading

    2022 in reading

commit 5ed8ddf219c3817c1291ac17e7de42ca83408e59
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Dec 31 18:42:59 2022 +0000

    markups on my 2022 reading post

commit 804fb4be99f3b713f52d8dfc59d699acf11af62c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Dec 31 18:37:42 2022 +0000

    add some semantic headings

commit 8da788414035af16fe405258d9a8e5d6c3b8b4b3
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Dec 31 18:31:44 2022 +0000

    add a missing separator

commit 822aac07e97c9a84f97447c854ecc4297c1c0193
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Dec 31 18:27:57 2022 +0000

    use my nice new HTML include

commit 7b314659f90dba0f88938d666cc92976a719eeb2
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Dec 31 18:23:05 2022 +0000

    Add an entry for "2022 in Reading"

commit 9783a53ee2f8cda7ca97ffdaf12f185e3b08feb3
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Dec 31 16:22:24 2022 +0000

    Add a better error message to create_post.rb if no arguments

commit 215453debbdd57e3af461fd4fd1879dc73075c51
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Dec 31 16:19:29 2022 +0000

    Add a mechanism for injecting extra style sheets

commit 46fddb5253df6815c0789eb938bb250423d08067
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Dec 31 15:28:32 2022 +0000

    there go some more images

commit 211665bd0df84bd367630fa1034443f3eb95f59d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Dec 31 15:20:36 2022 +0000

    Revert "Tweak the way `srcset` attributes are created for smaller images, maybe?"

    41b6575fe0491137082742377babc7a6e8c72743

commit 1e5e594ab48750c4d279631e4af4dca511cfb2ef
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Dec 31 14:47:25 2022 +0000

    add a missing parameter

commit 5211c8f4f6191381420973f27ef93adb21a1977d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Dec 31 14:47:06 2022 +0000

    Remove some unused CSS

commit c86387d2862cab804c54ada56aef092945bae274
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Dec 31 14:47:02 2022 +0000

    Tweak the way `srcset` attributes are created for smaller images, maybe?

commit ff6cecc4a14847efaeb84cd63532d4453efd7b02
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Dec 31 14:32:01 2022 +0000

    Add the width/aspect-ratio attributes to optimise CLS

commit 14bca3b0549c5024c288e378e0d2669019638961
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Dec 31 14:30:18 2022 +0000

    trim a bunch of whitespace

    [skip ci]

commit f55c87857b39aab5473fee4450b7e1383eecfb96
Author: GitHub Actions on behalf of Alex Chan <githubactions@alexwlchan.net>
Date:   Sat Dec 31 12:42:13 2022 +0000

    Publish new post live-text-script.md

commit 1caecd33a8b9c812b324ebcb859ae198b2af379e
Merge: febc6ea7 09a96a7e
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Dec 31 12:40:00 2022 +0000

    Merge pull request #588 from alexwlchan/live-text

    Add a quick link to my Live Text scripts

commit 09a96a7e64f98ba21db7c81217d7e5622ba89897
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Dec 31 12:37:28 2022 +0000

    Add a quick link to my Live Text scripts

commit febc6ea7a69f6c9c5cdad6f1490652b358d0437e
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Dec 30 11:46:02 2022 +0000

    big titles for everyone!

commit 1dd9282df72b54bdbdd1ce0d12bd4ccf0c2fd16a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Dec 30 11:13:16 2022 +0000

    red, not yellow

commit 1018f1be8cfd41b44d960d7a673d0234f6f8b418
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Dec 30 11:02:28 2022 +0000

    make last year's book post prettier!

commit 4cc2a9493db8473752d8476bb8416c1795f0cafd
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Dec 30 00:17:22 2022 +0000

    make the new footer accessible, better line height, ko-fi link

commit aab3a4ea678243d853656de366473d3f64c89c8d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Dec 29 23:57:49 2022 +0000

    don't blow up the footer when styles are disabled

commit a6f58f37a49835f5043ecdef3f8bfabe577b0ab3
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Dec 29 23:55:43 2022 +0000

    update the licence pointer in the footer

commit 95138a1b38e4396eba3c988dccd234dc2dbce6d1
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Dec 29 23:47:36 2022 +0000

    remove an unused import

commit 073cae11bac3aae40118f7162eac1e784c9a98cf
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Dec 29 23:46:22 2022 +0000

    fix alignment of footer icons

commit 84e7b6e2c7adee0051c0a7bd394d9404822360ba
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Dec 29 21:29:18 2022 +0000

    Update _footer.scss

commit 1e0ab116f082557e3c06475834faed61a6ced917
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Dec 29 21:22:33 2022 +0000

    add some cool social logos to the footer

commit 8ac79dd341a9ac415ed8bdf499c4f427fea45c8f
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Dec 29 07:52:05 2022 +0000

    add another 410 for a wpinclude

commit bbd138e72951d120e246a31c5e168a3fec83d2f1
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Dec 29 07:50:16 2022 +0000

    don't solicit tweets here

commit e7becd6d2b6f863d2b9bd4ba47b03f0b60ae22ab
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Dec 29 07:43:11 2022 +0000

    tidy up a bunch of redirects

commit d02469a727208eea82d5cffc7367d0cf2d16b896
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Dec 29 07:36:49 2022 +0000

    add an empty robots.txt file

    It's the top entry in my list of 404s and everything is crawlable

commit 8b177c8cec2eee80b103dffcdd3c51902d20e185
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Dec 29 07:32:38 2022 +0000

    and a few more popular posts to new-style pictures

commit 1ac333056ee8bb55f36372c6f0ddd8351ca1a61e
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Dec 29 07:28:52 2022 +0000

    Convert the 'downloading SQS queues' post to new-style images

commit 8e40bec5646fd960a1d5225ea298b09c68a77f68
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Dec 29 07:28:29 2022 +0000

    Add a better error message if images aren't wide enough

commit b22f3f66b65c1096747eb35509745059f81b05bd
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Dec 29 07:24:48 2022 +0000

    Use new-style images in my post about LaTeX underlines

    It cuts page weight by ~60% and improves the alt text.

commit 09dd02345bf5ec7870435f4094a83d8ae72e9f94
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Dec 28 21:51:38 2022 +0000

    flip another two posts to the new picture plugin

commit 7e6cb0229181f6849ff754d5f911db86c8c0767a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Dec 28 18:12:02 2022 +0000

    only run the "create images" job if new images needed

commit 1b59b2bbb2342cb65c1209b94f4bc2c012054f4b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Dec 28 18:11:48 2022 +0000

    Flip a few more images to the new plugin

commit 5b17128c14ae73d03242151a9819ec5f079a015e
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Dec 28 10:23:59 2022 +0000

    fix a broken link

commit 25114f1e59c920f83c9493fc48e3c33647b76337
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Dec 28 09:10:28 2022 +0000

    remember to create the out directory first

commit 1556cacb902ee0b466c1030f2ea287f60c1263d0
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Dec 28 09:07:30 2022 +0000

    Bump the Docker image to version 30

commit 7369167f59b75219d37311d80a1cc74b7a2f72f0
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Dec 28 09:07:01 2022 +0000

    Revert "build a new docker image"

    8509b5d8fd3b0a5e60082999ef10475ec116d7af

commit 39b324a43ae499c6c841bc6849d3eee3dc4ed49e
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Dec 27 13:20:40 2022 +0000

    build a new docker image

commit 582f7d762fe44e0ed98dd45b98754dbe6cb4efea
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Dec 28 08:58:00 2022 +0000

    Switch to using ImageMagick for AVIF and WebP

commit e3b9baff3a293ac5ee58c1450d1340002a3b32fc
Merge: 41a74311 1dcfa263
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Dec 27 17:42:36 2022 +0000

    Merge pull request #585 from alexwlchan/fix-source-in-rss

    Fix the URLs in <source> tags in the RSS feed; more image optimisations

commit 1dcfa263576fbdbd7fe84e1fe1c9ea3a5e7e60e6
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Dec 27 17:35:07 2022 +0000

    tidy up the images in the aberdulais post

commit 954e4373dc404a5646bcaadf4d6bbf3097d12c79
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Dec 27 17:11:47 2022 +0000

    Fix paths in the <source> tag in the RSS feed

commit 41a74311b4daacd483f42f7735b192c0e5aa6e9b
Merge: fb1cb8be 36309a92
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Dec 27 15:20:48 2022 +0000

    Merge pull request #582 from alexwlchan/use-images-for-cards

    Use the new image logic for cards

commit 36309a92e9df9dfacaa9e08edb9ad31ec64c9900
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Dec 27 15:12:34 2022 +0000

    move over the remaining cards

commit da957d40f84dd8d232fcb0b7ca97038535953d44
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Dec 27 15:10:43 2022 +0000

    remove some unused metadata

commit cddb439a3695b2e0598f9812362c66a107e2c51f
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Dec 27 15:08:21 2022 +0000

    Revert "build a new docker image"

    43b4734a1292cb885fc8297273af67d1895bca7d

commit 6dec7733b2b5971805e4e3458b472b002cb12475
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Dec 27 13:20:40 2022 +0000

    build a new docker image

commit 828e1a6028b75b14a5784b01ec0d2ba75967c248
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Dec 27 13:20:20 2022 +0000

    We don't need ImageMagick any more

commit 4511157e7b08d12cfc38343c9420fac460ce98dc
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Dec 27 13:18:39 2022 +0000

    make sure we always create social images

commit 2e69b78e72d57543abf269c68dd571bf3152845b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Dec 27 13:15:45 2022 +0000

    flip a bunch of images in the "Our Place in Space" post

commit 2a9b8cd57cb2be274dfb1e41e4d79e8e5bc316a3
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Dec 27 13:03:18 2022 +0000

    we need to pick up hyphenated attribute names

commit 4d5cb1db0809bbda5ed725f300bf24cbdb11c0bb
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Dec 27 13:01:22 2022 +0000

    this should be * not +

    so that empty values (e.g. empty `alt`) still appear

commit ffd80a3a861b331995c23a283c2d13e10378f6e1
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Dec 27 12:34:32 2022 +0000

    remove an unused script

commit 2aa38845eb55924ad2dfbf3a2491f57ded3cdd1f
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Dec 27 12:31:31 2022 +0000

    And also serve the social cards this way

commit c61f57a8296cc8ab36ff1b6c57a566a0921ca0af
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Dec 27 12:17:19 2022 +0000

    use the new picture tag for cards on the index page

commit a18050e22692012b9c1dd7cbcd24f604060e0644
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Dec 27 11:52:56 2022 +0000

    remember to delete the right file here

commit fb1cb8beacf530069a9c3c16d760669cf83fa5fd
Merge: 225905bf 6247be76
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Dec 27 11:27:48 2022 +0000

    Merge pull request #581 from alexwlchan/tweak-picture-tag

    Continue tweaking and improving the picture tag

commit 6247be76638babd59f863c9de29f061ee01326e4
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Dec 27 10:58:51 2022 +0000

    use the new picture tag on the Forth Bridge post

commit 2d396ab27419a1f794bbc1d0d5b2ea84c2d61e54
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Dec 27 10:46:02 2022 +0000

    allow creating non-sharded images in the picture tag

commit c6e0e1100b606f779a9aa65c4cba150ed2e75469
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Dec 27 10:45:51 2022 +0000

    remove a filter that's not being used

commit 225905bf3301d8537b3249540a3936429ae0f854
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Dec 27 10:35:18 2022 +0000

    tidy up a few redirects

commit 370b8b0cc89f155db008131b70e7811f2feedb71
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Dec 27 10:35:09 2022 +0000

    add a missing 'screenshot' class

commit 31ff28bd77db34cef16dddbb3d8c853a99091aef
Merge: fd9b3d38 00de2d19
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Dec 27 10:34:21 2022 +0000

    Merge pull request #580 from alexwlchan/skeletor

    put the skeletor files in per-year /files/ paths

commit 00de2d190e9adfbde23ace05298e4f5d4e8346f7
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Dec 27 10:32:18 2022 +0000

    remove a dead .gitignore

commit c2e424460274c46762b8e61d5e0dca69ea44c38c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Dec 27 10:30:24 2022 +0000

    tidy up the spacing

commit 612894fe1601238d664fc4094a2615d25d3aba40
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Dec 27 10:29:20 2022 +0000

    put the skeletor files in per-year /files/ paths

commit fd9b3d38a2b4027d9ac31f21b10140b52f6dbf91
Merge: f5d24e6e dfca2d15
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Dec 27 10:21:54 2022 +0000

    Merge pull request #579 from alexwlchan/tidy-up-files

    Tidy up the 'files' and 'talks' directories

commit dfca2d15099f7fca935d9949f5503ab77466b27f
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Dec 27 10:19:48 2022 +0000

    fix links to some talks

commit cfe980818c21b3c87bbe7a56922d147f1e223aea
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Dec 27 09:59:32 2022 +0000

    and move some images to per-year directories also

commit 06bad85358cdde4bf69a410d1595359e290e72dc
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Dec 27 09:57:28 2022 +0000

    remove a few more old images

commit b13df21a01ab7cd297b251d8a7f117ebc6613e7e
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Dec 27 09:56:01 2022 +0000

    finish removing stuff from the /talks/ namespace

commit 62e3c6f3f2404ecf45571667fc562c5ed9872538
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Dec 27 09:50:59 2022 +0000

    remove some more old files

commit 9c3591f99784d75ffd582927749ee2f25d5979f4
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Dec 27 09:50:04 2022 +0000

    another file into /files/$year

commit 4929a41c4e2f16e34bfa2f3a420fb7702cf5716f
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Dec 27 09:48:36 2022 +0000

    remove some unused files

commit a0bb1e3d92dc37d53bd503556e0cf9b8b4e37704
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Dec 27 09:37:46 2022 +0000

    make some indentation consistent

commit fd4a5657646c682087c189c5bf964eae85bd267e
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Dec 27 09:37:40 2022 +0000

    move a talk file out of /talks

commit 99eee4cbe928b9a04f2348da590b27b2539a2841
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Dec 27 09:36:18 2022 +0000

    we can now remove the old 'slides' directory

commit 8d9ec9645183177315e9673dd5c88b4122eea2c4
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Dec 27 09:35:26 2022 +0000

    rearrange the 'files' folder into per-year subdirectories

commit f5d24e6e62033a17f91b2b3883e752126e55447d
Merge: 9036b45b 906019a9
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Dec 27 09:19:51 2022 +0000

    Merge pull request #573 from alexwlchan/more-images

    keep fiddling with images and caches

commit 906019a945b569f8b6144bc65ab793026fd586d6
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Dec 27 09:16:26 2022 +0000

    I don't need to know what's in the cache

commit eee53af274423a3a919ee1a43d43fa020c8a4612
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Dec 27 09:13:37 2022 +0000

    get rid of the _slides directory

commit fb9c93ac0fe56a676103b2169ff0755e54b4c999
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Dec 27 09:05:14 2022 +0000

    remove some unused code

commit f7bb46fbe9e3d1ee874a244428a78370fec2272c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Dec 27 09:04:46 2022 +0000

    fix a file extension

commit 754c52060ccd0d0c92d126854ee2902a3d53e1c5
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Dec 27 02:44:39 2022 +0000

    use the .jpg suffix consistently

commit 672764ea227178d2971730e6bb9db4fb487ae0e0
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Dec 27 02:32:26 2022 +0000

    and remove some more old plugin code

commit 5b9777099b20d27b1d6f66f39d761af732b536a7
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Dec 27 02:31:12 2022 +0000

    keep removing the old plugin

commit b04f6e4f206e66b5b331c9678943f20cb9b5091d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Dec 27 02:30:59 2022 +0000

    rename the slide tag

commit bf5c3d4114237241e58d98a5461ee8360962f40e
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Dec 27 02:30:50 2022 +0000

    ditch the old slide plugin

commit 57cd5f5b78c3aeca48bd54607c09f5e90f226a8e
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Dec 27 02:28:32 2022 +0000

    move across the final old slides

commit 3c1d3ae477f1c8b9ebd0a6c01c2aa9d7d96210e0
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Dec 27 02:11:59 2022 +0000

    there go some more images

commit 204e91483e3021f3ef3a9c4369995d263eaefa16
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Dec 27 01:34:19 2022 +0000

    fix an alt text attribute

commit 754d2b18d5e2c06a6a91927c32ee48216ba86af4
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Dec 27 01:30:53 2022 +0000

    convert "inclusion can't be an afterthought" to the new slide plugin

commit fdfd75c2ad8eb72810378fac6e06d20c438f6f99
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Dec 27 01:19:25 2022 +0000

    flip another batch of slides

commit 8b625a16c95127de3f0c03d84bc203f23246cd69
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Dec 27 01:07:48 2022 +0000

    does this use the cache key I want?

commit acfb9be60dca3c55a8ad91fd1c25c744c9c796be
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Dec 27 00:52:22 2022 +0000

    fix a couple of markup issues

commit b2b8e6efaea037e0a76d79d31f7969163ed1cc25
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Dec 27 00:44:24 2022 +0000

    maybe I need an env here?

commit 994f47dffa578da352a711c4aacd037ee2411c91
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Dec 27 00:37:04 2022 +0000

    try fixing the github actions caching

commit c4cedcf3a47ca2c7d857b391705ab8b3a293e70a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Dec 27 00:36:57 2022 +0000

    move the docopt and OLS slides into picture tag

commit 9036b45b46065745b23d16600a3af61ae98e1236
Merge: cda9cc34 1b5c6e2a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Dec 27 00:19:37 2022 +0000

    Merge pull request #572 from alexwlchan/delete-slide-plugin

    Switch up the image rebuilding a bit

commit 1b5c6e2a63b128491344a8d6a772e0e69a460fe6
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Dec 27 00:15:50 2022 +0000

    sort the cache

commit 1472f4f89b297970b46fb536bdc273b984907495
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Dec 27 00:12:31 2022 +0000

    what's in the cache?

commit d5a55be22b5b9906f81924b0ab5bf66d3df8588a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Dec 27 00:07:03 2022 +0000

    just check for a missing resized image

commit 51b22374c520463a953d57ee4d001a12547ce996
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Dec 27 00:04:36 2022 +0000

    bump the docker image tag

commit 317ddf077c30855ce01fc515e3b1190ff143df44
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Dec 27 00:04:23 2022 +0000

    Revert "build a new docker image"

    e067a5677d535cc1e76cca9e341d7ad27f4edff7

commit 6a3072f02a1b7126bd0a4268999bd88957cfd520
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Dec 27 00:04:21 2022 +0000

    Revert "go faster"

    b3870bc7e2ac4af84ecbf618c9b1e0abf52d326d

commit 176d32251f7651b1209d0d064c7024fb22ac156e
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Dec 27 00:01:50 2022 +0000

    go faster

commit f75965e88ee71fd916135e2aa557362d00d0b28d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Dec 27 00:00:01 2022 +0000

    build a new docker image

commit dd4c269891b9524d6b5fb5436fe4bb6ede660b3b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Dec 26 23:58:21 2022 +0000

    remove a stray hash

commit 1f2270876169881f8a0439d74db92e5bdfbf6c1a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Dec 26 23:57:20 2022 +0000

    switch to pillow for images

commit 728a86ea11cc648adef0adaad33c21c8c3581496
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Dec 26 23:17:32 2022 +0000

    we don't need to create for a magical, as-yet non-existent 4x device

commit 381621dd78040c483e6d4366878ea017a94798ff
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Dec 26 23:12:24 2022 +0000

    add a daily rebuild to keep the cache fresh

commit 96f29ed3368cb615d25d156dff4b7c7f5e1ea2c1
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Dec 26 23:03:58 2022 +0000

    add a todo note

commit 4dbfb147f8bc84c0ed35d247254a6dd8b8ae0b92
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Dec 26 23:03:52 2022 +0000

    use rszr instead of ImageMagick where possible

commit be32eaf608326f9f7dcecf2ed7542863d9313f01
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Dec 26 22:53:13 2022 +0000

    And switch to the new slide tag for Curb Cut Effect

commit cda9cc347af60120c3dac980124a423bd05d178d
Merge: 22171eb1 fa2368a3
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Dec 26 22:50:50 2022 +0000

    Merge pull request #571 from alexwlchan/delete-slide-plugin

    Use the new picture logic for slides

commit fa2368a3c51db97e3942356e7ab2ae65f50eaf38
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Dec 26 21:51:14 2022 +0000

    convert sans I/O programming to the new tag

commit 224356d6d3fd480134c5a67deee3d5544f1efb7e
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Dec 26 21:29:38 2022 +0000

    add a missing newline

commit b2a656a938467f8df8e4d397fd030efd13b9ac24
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Dec 26 21:28:44 2022 +0000

    don't load a template I'm not using

commit cd687de47bf37efc34fcb41e3730287e09578b75
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Dec 26 21:27:54 2022 +0000

    fix the name of the tag

commit 971fd6a5a01dd1c2e651d8203b9b6117b8285e3d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Dec 26 20:57:39 2022 +0000

    Create a new slide tag with improved picture handling

commit e344783e5a658149a95dc8a88196b0e855f0a638
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Dec 26 20:00:31 2022 +0000

    Start pulling out some common Jekyll tag code

commit 22171eb127daad4bb40e0c85e5512b3f6a1f32c1
Merge: ce526aae 53f8fee3
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Dec 26 19:33:40 2022 +0000

    Merge pull request #569 from alexwlchan/more-image-logic

    A bold and terrifying new image pipeline is upon me

commit 53f8fee379dfd1b5faeb0190471d87bc9871d28a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Dec 26 18:47:21 2022 +0000

    that should be src, not filename

commit 21c32a8d19c70f82e598612ced99d00e48221201
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Dec 26 18:16:55 2022 +0000

    fix another attribute

commit d665422c7707968d74006e861d7a1169861bbf2b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Dec 26 18:08:56 2022 +0000

    filename, not src

commit 9938e6de4e020d2674a8989c14b0751da170032a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Dec 26 17:59:15 2022 +0000

    add a missing quote to a post

commit d51d68148e31295f6e9c9ec7790748bc2a6b8e29
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Dec 26 17:55:31 2022 +0000

    continue replacing some old images

commit ee7d2980039ac1e7a06074317f8b782eb78762ce
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Dec 26 17:52:53 2022 +0000

    convert another instance of the old <picture> tag

commit 41d0899c0cf632be9c8c3022bd957e6a171d693d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Dec 26 17:50:23 2022 +0000

    replace a few more images with the new {% picture %} tag

commit 7e1ef32b3f0b8944e0e5f43d921d00b0d8aa0b05
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Dec 26 17:46:17 2022 +0000

    Toss in AVIF, what the heck

commit a61c896c4d1413c386a39362cd37eb55f8f312b7
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Dec 26 17:19:56 2022 +0000

    let's make all of these images lazy loading

commit e05fc7ed42f375262855269a81af7687c13def51
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Dec 26 17:17:51 2022 +0000

    remember to pass extra attributes

commit 296b0efa0c5f5b976b288a554a6a09f8e4180cce
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Dec 25 23:57:09 2022 +0000

    Use rszr to speed up getting image width

commit 9beed78c1e9affcc632c191856fb5c2924c82e9e
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Dec 25 23:52:27 2022 +0000

    identify the slow bit

    [skip ci]

commit 442d728ea3805b08bd8bb76fcca6430d51785319
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Dec 25 23:06:08 2022 +0000

    remove more images

commit d97310e89b11a59a7bff5f4241513bd1dfd0b49c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Dec 25 21:54:42 2022 +0000

    start to push image generation logic into a plugin

commit ce526aae7bd587218c1d94eabac6aabf5a20dc3d
Merge: 13335f04 135490cd
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Dec 26 13:05:19 2022 +0000

    Merge pull request #570 from alexwlchan/dont-auto-merge-draft-prs

    Only merge the PR if it's not a draft

commit 135490cd569f35c25e9ac72bc2b06899dc8cedb4
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Dec 26 13:02:45 2022 +0000

    Only merge the PR if it's not a draft

commit 13335f04cc02d771180c53f6245a2b501a53eda1
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Dec 25 23:06:47 2022 +0000

    Revert "start to push image generation logic into a plugin"

    0980a43eef1b2a3b14146cfec1084acd7a009e13

commit 5949329e46dd2ed4f4632888f997fe8291f97c25
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Dec 25 23:06:44 2022 +0000

    Revert "remove more images"

    bec75f1de8b1018f7efafb87e5114886ac131789

commit a875bf64caafab71d1327db7f398317a386a6650
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Dec 25 23:06:08 2022 +0000

    remove more images

commit 435415ecec0aa45c93b7c47a6d02ae8af687032a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Dec 25 21:54:42 2022 +0000

    start to push image generation logic into a plugin

commit 7ec74056596789f5fdea5d8efbbdf2a92ef56070
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Dec 25 13:39:38 2022 +0000

    fix a typo in some alt text

commit 42c1d4bcdf056a29f8d532234d2349c8641f6f2f
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Dec 25 13:37:18 2022 +0000

    remove a couple of unused images

commit 4e5e2fe83e14098ec433d3ee41a153e098670204
Merge: 37a8c077 b757a151
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Dec 25 09:33:38 2022 +0000

    Merge pull request #567 from alexwlchan/remove-unused-filter

    Remove a plugin I'm no longer using

commit b757a15144a082bfd2bc6416d457a574a5f47c72
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Dec 25 09:31:13 2022 +0000

    Remove a plugin I'm no longer using

commit 37a8c077190e9333d9ade44dd884e60e3fb4b66c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Dec 25 08:41:17 2022 +0000

    remove an old var; trigger a new build

commit 89209d8a25771914558b80065eec2e1ab0ca56f9
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Dec 25 08:27:18 2022 +0000

    Add a comment explaining how card_images works

commit 0e66714ec6928cfd9e01aaf115f196449857a863
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Dec 25 08:27:09 2022 +0000

    remember to cache the right path!

commit c071e363742505fdc22eb2ff1bbee6f1b36eabd9
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Dec 25 08:22:21 2022 +0000

    spaces, not tabs

commit adbb6d016189931cea8588a2eb92d653b59d3acf
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Dec 25 08:17:51 2022 +0000

    try caching the site output for faster builds

commit 36cdf206766ac378fbcde203e4f7654be8a7981f
Author: GitHub Actions on behalf of Alex Chan <githubactions@alexwlchan.net>
Date:   Wed Dec 21 20:33:41 2022 +0000

    Publish new post cursor-confirmed.md

commit 8bfdeb787808e97171cbeac181e14f98bee997be
Merge: 33629ecf 20afcfda
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Dec 21 20:29:26 2022 +0000

    Merge pull request #566 from alexwlchan/checkmarks

    Getting an Important Internet Checkmark to follow your cursor

commit 20afcfdaded2b395019367b8ea0311729a893cc7
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Dec 21 20:25:41 2022 +0000

    fix the link to cohost unverified

commit a828f607fd9d6c20d7f7338360aad8891384b5f1
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Dec 21 20:18:13 2022 +0000

    more colourful!

commit a45a24ac90e0f9d4b502e1aff676f8cd22eb9c07
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Dec 21 20:05:20 2022 +0000

    make it more colourful!

commit 18f8bc9f996ec090c847cc9ade64265e01e2fac7
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Dec 21 19:58:18 2022 +0000

    add my kofi link again

commit 33629ecf9e0b9a76a79aeaa9e3a8bd51a5e4d5bb
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Dec 20 08:47:13 2022 +0000

    call it the eggbox

commit f1cf15a533a58e4d0e32d0d6319eeec7fdd1d05b
Author: GitHub Actions on behalf of Alex Chan <githubactions@alexwlchan.net>
Date:   Tue Dec 20 08:31:16 2022 +0000

    Publish new post prismic-validation.md

commit b8a7c11180419e86ebdffb0565f41e4d245a8a36
Merge: bee370c0 11a6f02b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Dec 20 08:27:48 2022 +0000

    Merge pull request #565 from alexwlchan/prismic

    How we do bulk analysis of our Prismic content

commit 11a6f02b9c3c267e939c417c36163dc7a4080d05
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Dec 20 08:24:09 2022 +0000

    shave off two pixels, fix the aspect ratio

commit 25393cb7a31a1dd4ba47c582fe01f18b1a2f0e98
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Dec 20 08:14:43 2022 +0000

    add some final markups and fixes

commit 5d7bee8fe779c219f8f730dd1816072fe9bc9a76
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Dec 20 08:11:24 2022 +0000

    Revert "fix a bug on the index page"

    684592198abb09219efca02df9bc885c26e17116

commit ced83d8646f8136ad81b5e92c9d96b08832d22b4
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Dec 14 14:27:46 2022 +0000

    tweak the prismic validation post

commit c6e21030a421965f24ef36abd8bf35bc79c68fd8
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Dec 12 21:51:42 2022 +0000

    First draft of a post about Prismic

commit bee370c021698cb01b2ee82e62301313f0516f0c
Merge: 517df377 cc03a6d2
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Dec 19 22:45:12 2022 +0000

    Merge pull request #564 from alexwlchan/revise-cards

    Create WebP and resized versions of cards

commit cc03a6d25813d32892bd9f2ee782e6b9d5c13481
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Dec 19 22:28:07 2022 +0000

    fix the card linting code

commit 6dae5d3f2cc51e3ecbb270f1d13f3bf3c65b5fb1
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Dec 19 22:12:23 2022 +0000

    fix a couple more cards, check OG cards also

commit 89c2d9253c275cb0cf6641a3027e893103688918
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Dec 19 21:30:31 2022 +0000

    add a missing image

commit 34c677be5a86df306880e6aa91d625c271a4290c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Dec 19 21:28:41 2022 +0000

    fix some aspect ratios

commit d790cb41bc400e50b583590ba949a8b6d61c6641
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Dec 19 21:17:24 2022 +0000

    add another missing image

commit 0436e722ff8d45b7abc1f43d812620831d4f65a6
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Dec 19 21:17:03 2022 +0000

    add a missing image

commit ca1815510e19fc90fb554a87df25722fd7c2d94c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Dec 19 21:15:54 2022 +0000

    fix a bug on the index page

commit d19cc4d8644e801ad8e2bf4075d53bad98f62f19
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Dec 19 21:11:34 2022 +0000

    continue tidying up some of the images

commit 221605f4e8e707efd73219422a1e08269c50c1fe
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Dec 19 20:53:40 2022 +0000

    migrate another card

commit e07a4f6a977aac43b7a6bc84a75d60ead67db260
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Dec 19 16:06:41 2022 +0000

    continue moving around some of the cards

commit a04851861d4556b82460b8dc7063c32c1eea8130
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Dec 19 13:56:03 2022 +0000

    continue migrating across cards

commit 71608e1722c208260180e49c119ce0ea1ba7fd73
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Dec 19 13:29:28 2022 +0000

    continue moving around cards

commit 08f361c9adf2a9b9c2cc8b787d3abd052297ad86
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Dec 19 13:14:40 2022 +0000

    move all the existing 'theme' cards into the cards directory

commit cd6aa0268c9fb5c2d71ab6306861293b0079a777
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Dec 19 09:16:54 2022 +0000

    Create multiple sizes of card image

commit f42cff9490519f5718577fc8e952a8c2a1983103
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Dec 19 06:39:50 2022 +0000

    Add ImageMagick to the Docker image

commit 517df3779ac1849702a7074b8c6fdaf5889d473c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Dec 19 06:28:19 2022 +0000

    Add an aspect ratio to the homepage image

    This gets lazy loading for the card images.

commit 819f8b56d8be85ef1f60e0209fb4814ef39adc93
Merge: 1fe32e3f be55874b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Dec 19 06:28:08 2022 +0000

    Merge pull request #563 from alexwlchan/fix-twitter-avatar-resizing

    Fix resizing for Twitter avatars

commit be55874bc358b88bd7d83bec921dc18346936ca7
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Dec 19 06:21:09 2022 +0000

    Make this avatar a JPEG, not a PNG (26KB ~> 4KB)

commit 64e739cf7d954581ed3e0732f76ce22cd9f0207f
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Dec 19 06:19:38 2022 +0000

    Fix the way Twitter avatars get resized

    Because `image.resize` returns a new image rather than mutating the
    existing image in-place, I was discarding the resize.  Oops!  This fixes
    it so avatars do actually get resized.

    This lets me delete the "gets bigger when resized" code, because this no
    longer occurs when avatars are resized properly.

    Most avatars are now <4KB.

commit 1fe32e3fe632ea29f9303995a1a39fbb9bdd2d87
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Dec 19 04:10:56 2022 +0000

    Update index.md

commit 1cadedc52d4461651bb2c5781d1ba8d76c115c8d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Dec 19 00:43:18 2022 +0000

    Update index.md

commit c9954ef46a8e3a193422cb4f0b2a1fccbcc31e8c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Dec 18 23:31:46 2022 +0000

    try supplying some bounds on this image, maybe?

commit 6b047c45db51e037fbaadc64e354c556ef3d4bef
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Dec 18 23:29:23 2022 +0000

    link to contact page

commit 71d595dcc99847204a024d2984e4f4b99c143b37
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Dec 18 23:27:27 2022 +0000

    beef up the homepage; add an eggbox

commit bf71dcb2bf1db79543f376eb72f6de3663d0af2f
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Dec 17 12:26:42 2022 +0000

    Update _settings.scss

commit 2ac94f8947ee72548d395c613e2a795657751e0f
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Dec 17 12:26:32 2022 +0000

    Update _footer.scss

commit 70f529324b196c958ecaf977e2d3d24e6044bd2a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Dec 17 12:26:19 2022 +0000

    Update footer.html

commit a6e6cccbcd5fbde362f4f3002757899311f608a3
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Dec 17 12:26:08 2022 +0000

    Update say-thanks.md

commit b64c06a04e5bb9252d8cbe0cf21b0d933cbf5d9f
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Dec 17 12:25:28 2022 +0000

    Update index.md

commit 84ec1645b12ccda464bd24876e2548290569d846
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Dec 16 17:11:16 2022 +0000

    Update conclusion.md

commit df1675374adcb0ede35ab8c288852c10712a5e85
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Dec 16 15:05:34 2022 +0000

    and tweak the tint colour

commit c3ca195c2c68371cb8a309bf86c82e66caf2720d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Dec 16 15:02:21 2022 +0000

    better card for 2021 in reading

commit 6b30c52b3b713ca1bc98121229a55d44996dcd45
Author: GitHub Actions on behalf of Alex Chan <githubactions@alexwlchan.net>
Date:   Fri Dec 16 10:01:11 2022 +0000

    Publish new post marquee-rocket.md

commit 478c01bbdf500e0b644214e532fa67d9b1cfd84e
Merge: 3649e8af b711bd52
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Dec 16 09:59:09 2022 +0000

    Merge pull request #560 from alexwlchan/marquee

    MARQUEE MARQUEE MARQUEE

commit b711bd52b64dddec57f0cb161820b5871066b8d7
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Dec 16 09:57:04 2022 +0000

    add alt text!

commit 0ac846bebafb9e362450252f3def0b6961b77710
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Dec 16 09:52:30 2022 +0000

    let's call that the final marquee post

commit 460082b86396c659f43f986b0e1fb4d7d839c11d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Dec 16 09:13:38 2022 +0000

    more marquee markups

commit a91579b85ecefb6faaf55edf5e85e52469c8f08c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Dec 16 08:33:35 2022 +0000

    another round of marquee markups

commit 8bb5756cf6a8a87581351d3ffe1588e539c27a27
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Dec 15 21:57:48 2022 +0000

    more marquee markups

commit 85558bcf2e87bb5e264bfc33585b94994dcb5e6b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Dec 15 18:34:23 2022 +0000

    WIP marquee

commit 3649e8afe471b878cd472d5c9ffbea842429792a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Dec 14 14:28:19 2022 +0000

    remove twitter from the footer/nav

commit 40a27c35e7fe9cdfbce598d80577e7c8244fb073
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Dec 7 16:17:04 2022 +0000

    add a missing space

commit 29e947c8e636bb28edeb80534939fd1f6ad48aa2
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Dec 4 06:32:49 2022 +0000

    Update 2022-12-04-print-sbt.md

commit e267e7670b51171fd7698eccc01fd40a1d37b9ae
Author: GitHub Actions on behalf of Alex Chan <githubactions@alexwlchan.net>
Date:   Sun Dec 4 01:16:55 2022 +0000

    Publish new post print-sbt.md

commit 09d3743e05f627effcf4d1d4dde235340d5eadbe
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Dec 4 01:14:33 2022 +0000

    add a quick post about sbt base directory

commit 61a8d3c961588ede9179259d749c5b37200c0411
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Nov 30 09:05:51 2022 +0000

    be consistent about image border-radius

commit 70bbd9308c7f22e9cd22d4c3cace4024fcd27dab
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Nov 30 08:06:28 2022 +0000

    make this image display properly

commit f56653e60e0b77dedce48b5864039801904a0c03
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Nov 30 00:34:45 2022 +0000

    Update index.md

commit ecbeb15246dddcc485ca7c8ba8bd55a315d34863
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Nov 29 23:42:34 2022 +0000

    fix typo: working

commit 4bef8169784df0d20d59ecf755476d7bc492276f
Author: GitHub Actions on behalf of Alex Chan <githubactions@alexwlchan.net>
Date:   Tue Nov 29 23:39:12 2022 +0000

    Publish new post koa-logger-redactions.md

commit 5834594b08133db5f5a6cfb550cb4ec4831cc547
Merge: a5c753b9 3cec9685
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Nov 29 23:37:16 2022 +0000

    Merge pull request #559 from alexwlchan/koa-logging

    Redacting sensitive query parameters with koa and koa-logger

commit 3cec9685b296b2d2271211b281c5b6375fe7eb67
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Nov 29 23:34:35 2022 +0000

    Add a post about koa-logger redactions

commit 939bf90ab48ce86abbb02d2538aaf524dd4f0b68
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Nov 28 21:34:31 2022 +0000

    let's webp up this cover image also

commit a5c753b9a5557ce620884f0579b6854864bedf23
Author: GitHub Actions on behalf of Alex Chan <githubactions@alexwlchan.net>
Date:   Mon Nov 28 19:57:52 2022 +0000

    Publish new post bure-valley.md

commit b073d1e5e0bc6ace4664373b7432a2c4e4a8743f
Merge: 1816d1d7 129a9c1a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Nov 28 19:55:52 2022 +0000

    Merge pull request #558 from alexwlchan/bure-valley

    A day out at the Bure Valley Railway

commit 129a9c1a42957cd5b1e921db30a8b1d0b6d748d6
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Nov 28 19:51:11 2022 +0000

    tweak the title

commit b9f6312d80118fc504e8f926ef503a424a3a6433
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Nov 28 19:49:48 2022 +0000

    finish bure valley markups

commit 9037d7efad7be3896f02f708d25dab6e1632b60f
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Nov 28 19:18:38 2022 +0000

    add all the alt text

commit 1a2b0b764f49d0ac55c57b63356a01dc1f571466
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Nov 28 19:10:00 2022 +0000

    add more alt text

commit 05c6dd4e414499f1adde6a2bc824ea71c3b1e7dd
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Nov 28 18:59:57 2022 +0000

    tweak the bure valley markup

commit 66074fcf42a0af1e0230b45d6f6785e5b0c3d089
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Nov 28 18:07:12 2022 +0000

    explain what this script does

commit 8654e42c47dcb191269ca8105f78015fbc30f44b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Nov 28 18:05:47 2022 +0000

    more bure valley stuff

commit 781a4a471c8a3410102dcc013c9ddea56c3a0148
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Nov 28 12:36:32 2022 +0000

    continue fiddling with the bure valley post

commit 53580789ece735208b09a7c9f0fda63d723ff292
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Nov 28 08:19:42 2022 +0000

    first draft of the bure valley post

commit 1816d1d7c66134e02f653aa6d0cfb649c468d162
Merge: f67d0070 ee43e11d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Nov 27 14:15:58 2022 +0000

    Merge pull request #557 from alexwlchan/detect-bad-colour-profiles

    Use a vanilla sRGB colour profile for all images

commit ee43e11d95c4d701b2d853c7d3590b37f05beaab
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Nov 27 14:13:38 2022 +0000

    convert the remaining images to sRGB

commit 699628456f01201d3b9077b6535625fe5b724c83
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Nov 27 14:09:45 2022 +0000

    convert more images to sRGB

commit d90923fd5933a9fcac9a0ad2070a14376200bc29
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Nov 27 13:01:11 2022 +0000

    convert more images to sRGB

commit 1e47fbd9dc0958fb437ce6ac413e01637a3822ac
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Nov 27 12:53:52 2022 +0000

    convert more images to sRGB

commit bce09bcc53578cd3160f1498630fb3d61754d2d1
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Nov 27 12:43:28 2022 +0000

    convert yet more images to sRGB

commit adba7aa0c51da5dadad167e2099bdc61d9e8cfb1
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Nov 27 11:13:22 2022 +0000

    continue converting images to sRGB

commit f09b68bb13153b9a037b6eba287c241d15f9c2ab
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Nov 27 10:08:18 2022 +0000

    continue converting images to sRGB

commit 53dd762698e66c3f8b7e1f4d6f5ac7fcb993655b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Nov 27 09:17:59 2022 +0000

    continue flipping colour profiles to sRGB

commit c7e53c27ffdbd404cca001e5a62d2167d773a528
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Nov 27 09:13:50 2022 +0000

    convert a few more images to sRGB

commit 51132812dadd92a8844e78193b955d00cf097475
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Nov 26 22:06:01 2022 +0000

    convert more images to sRGB

commit 6394086f2c7836cb3e4b06464cb4aad9ac444eea
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Nov 26 22:05:04 2022 +0000

    Use the newest version of the checkout action

    This fixes a warning about using Node 12 actions

commit 3393a37b6349f08ff6ed96222b8a5c28e2c8eada
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Nov 26 21:40:11 2022 +0000

    Check images use an sRGB colour profile; start converting

commit 3ff97b1b9be826c4ce79076c49aa8175f0465a8d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Nov 26 16:32:15 2022 +0000

    Add exiftool to the Docker image

commit f67d007086c28d9a2e59d4de300c27e4692981c8
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Nov 26 09:54:20 2022 +0000

    Optimise the 10-of-cards.jpg; use an SRGB colour profile

commit 03d8269389b5a5fc3d447352a52f565533559dba
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Nov 26 09:00:41 2022 +0000

    add some CSS for the editing toolbar

commit e0988f64339ce9474b17c0bb89435eba6bfc1c54
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Nov 25 23:45:08 2022 +0000

    Update all-posts.md

commit 7e577702f69172609df7da05d9e71e8ba070aa40
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Nov 25 23:29:26 2022 +0000

    add a bit about using applescript

commit cf364583504f2160116b2d275c79e1dade175035
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Nov 23 04:36:31 2022 +0000

    Update 2022-08-01-screenshots-go-gangbusters.md

commit 1c4f369a75226444bd5bb17b7d88c4c5b9d3b40e
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Nov 19 22:17:37 2022 +0000

    Revert "tweak the twitter card for "all posts""

    c8017a10cdb84b2e16faa4dfdf60dfd18c98f2a0

commit bbddfae3bdf64ebe3f8e471e5de6686301dc2d0b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Nov 19 22:09:04 2022 +0000

    Revert "tweak the twitter card for "all posts""

    c8017a10cdb84b2e16faa4dfdf60dfd18c98f2a0

commit 0c0fc48bd372888356129d6e408bf2b77d6de734
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Nov 19 21:58:13 2022 +0000

    tweak the twitter card for "all posts"

commit 1bddfe964ebe865109a1b1c4afb617ae7b4ec653
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Nov 17 23:02:24 2022 +0000

    Update 2022-11-17-changing-the-macos-accent-colour.md

commit e632cb1f59332f65edb551d36284be1dd769301b
Author: GitHub Actions on behalf of Alex Chan <githubactions@alexwlchan.net>
Date:   Thu Nov 17 22:38:39 2022 +0000

    Publish new post changing-the-macos-accent-colour.md

commit 4cd188f16225f1ccf88faa84332171658c01e02c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Nov 17 22:36:51 2022 +0000

    add a missing card

commit 02e25cdf45cf740eefac23a5e495a2f2297ec606
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Nov 17 22:34:26 2022 +0000

    Add a quick post about setting accent colours

commit 3325314cd793c43f375b921e1ac7b463995d8a5f
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Nov 16 22:24:59 2022 +0000

    add the screenshot style

commit 8d966c6c2bf30fd637441df5042ab18502f38aa6
Author: GitHub Actions on behalf of Alex Chan <githubactions@alexwlchan.net>
Date:   Sat Nov 12 07:13:03 2022 +0000

    Publish new post tin-anniversary.md

commit 15c3b1f247571d90362c5f9ba9cb95a19da111ac
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Nov 12 07:11:36 2022 +0000

    again

commit 819fe83ecf60839217d08d3e40b5cf51b59a53a7
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Nov 12 07:11:25 2022 +0000

    explain a bit more

commit 0ee0d82072bdeebe2986906800fe9dc15673237b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Nov 12 07:10:46 2022 +0000

    tweak word

commit 9e9ce712995637af00ab4494fd12acc519e74408
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Nov 12 07:10:24 2022 +0000

    tweak wording

commit 36184fe2110683d6676249704b3aab4850652ead
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Nov 12 07:09:14 2022 +0000

    add a post to mark 10 years

commit a2fa889d888a03c9fd29cf1294b80b9746ce3d03
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Nov 12 07:09:00 2022 +0000

    is this really generative art?

commit 5186cce72b3f9de96b94dfabb675b3f13d60fb1d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Nov 12 07:08:53 2022 +0000

    fix the moomin headache

commit 81f3c6998a44759f9128e098aeba10a49721f3cf
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Nov 6 12:22:58 2022 +0000

    Update save_tweets_by_id.py

commit 783d91beb16146606e5e3473dc616b3eca12adf5
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Nov 6 10:48:03 2022 +0000

    put a bit more whitespace on the blue bird card

commit d087b9feec21355dfb8dbeb84d951369df5a7ad5
Author: GitHub Actions on behalf of Alex Chan <githubactions@alexwlchan.net>
Date:   Sun Nov 6 10:39:43 2022 +0000

    Publish new post tweet-alt-text.md

commit cac83de85bcaa9aee3423484d5501a82c9f9b796
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Nov 6 10:37:50 2022 +0000

    tweak the description

commit d34e43890ce5a64dfe95e29550b3e5ad8e3b0c2a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Nov 6 10:36:41 2022 +0000

    toss up a quick post about alt text

commit d441ead3deec368682cdc9be3c56ef98adb1ea37
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Nov 5 09:29:24 2022 +0000

    Update 2022-11-04-obsidian-plugin.md

commit 96609d55a828165d2a19868b08b41ae62fe76f7e
Author: GitHub Actions on behalf of Alex Chan <githubactions@alexwlchan.net>
Date:   Fri Nov 4 22:27:36 2022 +0000

    Publish new post obsidian-plugin.md

commit 2bd44f48b0c4ac7184ed7272477a897b169c9a16
Merge: ceb2488c 3238f5ad
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Nov 4 22:26:12 2022 +0000

    Merge pull request #556 from alexwlchan/obsidian-plugin

    add a quick post about my new obsidian plugin

commit 3238f5ad7e26bf92aafb1e14b29327d4f6b01655
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Nov 4 22:24:41 2022 +0000

    add the concepts screenshot

commit bb4eef9060368e1a43475af159d421b03a63706f
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Nov 4 22:16:11 2022 +0000

    add a quick post about my new obsidian plugin

commit ceb2488cd04682131df298dae1d8baf5819fc654
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Oct 27 16:59:47 2022 +0100

    aria-braillelabel

commit a8e27fd45bd9b8856f94147bc310423dadc13691
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Oct 27 16:50:18 2022 +0100

    delist this post

commit ca994dd72ea2b525c82839eb5e77ee099c454ca3
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Oct 26 22:23:06 2022 +0100

    Update 2022-10-26-accessibility-fixes.md

commit d33d49fc705f81b46e6f93849fd6ad8cdf2a9d1b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Oct 26 20:05:45 2022 +0100

    Update 2022-10-26-accessibility-fixes.md

commit e438ac1a0bcd054d54a5dd51f039e66eb8dbcd29
Author: GitHub Actions on behalf of Alex Chan <githubactions@alexwlchan.net>
Date:   Wed Oct 26 18:58:54 2022 +0000

    Publish new post accessibility-fixes.md

commit 4762fd3ee600c0a608bd446e3cf7504659cb9714
Merge: a608bdbd 538ee581
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Oct 26 19:56:06 2022 +0100

    Merge pull request #554 from alexwlchan/accessibility-fixes

    Accessibility fixes

commit 538ee5813bf5832eebf5795d5000b206bd89f6f4
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Oct 26 19:55:25 2022 +0100

    Update accessibility-fixes.md

commit 640724b44267ddb57c39a5d4275aacf37680750c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Oct 26 19:54:27 2022 +0100

    Update accessibility-fixes.md

commit 7dc05737a18d27bf8123f9981c23ffb9f71f9e1e
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Oct 26 19:47:38 2022 +0100

    sort out the accessibility fixes

commit 3de5ed1073d8059c22ae8c41bb3253862dc182df
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Oct 26 11:23:52 2022 +0100

    kick off the accessibility post

commit a608bdbd2b5b53b2178bf629458ea943c65d8507
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Oct 25 23:29:06 2022 +0100

    tell VoiceOver to read this as continuous blocks

    see https://tinytip.co/tips/a11y-voiceover-text-role/

commit 2f442325d662fbf2614fb4b59c9364e37b047a81
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Oct 25 23:19:21 2022 +0100

    Add some more missing aria-labels

commit 70327e0ec72830b3e619f78ca37bdb60bee0262d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Oct 25 22:51:55 2022 +0100

    Add an aria-label so this gets read correctly

commit c42e38e32e6504b9523a8913eba75aeb27c25f9f
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Oct 25 22:51:24 2022 +0100

    Remember to add aria-hidden=true to all separators

commit c7f555f91f59b38790193d0fbf1a39df69cbe29e
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Oct 25 12:27:55 2022 +0100

    Update 2022-10-25-iterative-project-management.md

commit 0d1500a9d7bcf79e13278ef78a8c97e56f2907ec
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Oct 25 12:07:20 2022 +0100

    finish a version of iterative product management

commit 0f2e2292241b6f450ad28b6b43c18926dc8e72cc
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Oct 25 10:43:12 2022 +0100

    continue tweaking iterative project management

commit 69c7d93e3c040e77933cce3461e9d71bf7ed1cb8
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Oct 25 09:57:10 2022 +0100

    fix the post slug for the bit.ly link

commit 70e562da0b5c463ff3a6e3076f08c0e6dcec4ac7
Author: GitHub Actions on behalf of Alex Chan <githubactions@alexwlchan.net>
Date:   Tue Oct 25 08:07:13 2022 +0000

    Publish new post agile-and-iterative-project-management.md

commit f086202741f0c9042f6f618238f6f8f830332b37
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Oct 25 09:05:21 2022 +0100

    helps to link to the slides

commit b86186cdb53239edbf3a65229dafcc7a41b7641c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Oct 25 09:05:04 2022 +0100

    Add the most basic version of the OLS-6 post

commit 7e47f34c6367a8e181c9083f63c2ea116b7e126a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Oct 18 12:29:36 2022 +0100

    Delete 2022-10-15-medicine-man.md

commit 65f4f249c4334fe1fd7cd4712b3ff122f06cb88e
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Oct 18 12:26:03 2022 +0100

    Update 2022-10-15-medicine-man.md

commit 8b41e94b1b23165bf57ff9453123f4c3b37d3215
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Oct 18 10:56:53 2022 +0100

    Update 2022-10-15-medicine-man.md

commit 9a0277192747ddbe8b01a684a00631f7229f0e9f
Author: GitHub Actions on behalf of Alex Chan <githubactions@alexwlchan.net>
Date:   Sat Oct 15 22:27:05 2022 +0000

    Publish new post medicine-man.md

commit 0954428607b24b39153a0d005faf90ef16577ee0
Merge: 509c79af 1c54893b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Oct 15 23:25:28 2022 +0100

    Merge pull request #553 from alexwlchan/queer-medicine-man

    Looking for queer energy in Medicine Man

commit 1c54893bcb2fc10201a993af40e7fe84e1e6037a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Oct 15 23:23:45 2022 +0100

    couple of markups

commit abcfd5f8c9d86ddda933940784b2b8ceac9af916
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Oct 15 23:12:35 2022 +0100

    tweak the medicine man post

commit 7ea55f0efa0e396566e03fd003efcf5128663aff
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Oct 15 14:30:28 2022 +0100

    Update medicine-man.md

commit 4782cd66a62cf4dc48fe4191fee43d1d4e480469
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Oct 15 14:22:30 2022 +0100

    Update medicine-man.md

commit f356cc3aff4996e045e419ebff5aa5a390b11761
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Oct 15 14:05:46 2022 +0100

    start writing the Medicine Man post

commit 509c79af7279d9b4d7a73e332b0fdb0e6902d328
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Oct 13 00:59:39 2022 +0100

    remove a now-unused pagination component

commit 986336e79a35c4ee1682961e93cf2a3620ff5e98
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Oct 13 00:56:40 2022 +0100

    the top bar should be a <nav> not an <aside>

commit 228dad30dc6d3c6e4e9cb719cd363b2b5e9dbb35
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Oct 13 00:29:17 2022 +0100

    Add a 'skip to main content' for VoiceOver users

commit 948d81d6e0c47fa045285ce91703913c91ca971f
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Oct 11 15:22:39 2022 +0100

    reduce the size of the bodleian image

commit 6902b218708ccfdea9ff90c5b508dbeb8cd8a2a5
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Oct 10 20:53:07 2022 +0100

    Update 2022-05-17-carbon-monoxide.md

commit da990c8fa7f848b7333f212085f441b175c05bae
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Oct 10 20:52:58 2022 +0100

    Update 2022-08-28-blink-diffs.md

commit 4f172ff483e51119d77d89ea680c91501b2229c2
Author: GitHub Actions on behalf of Alex Chan <githubactions@alexwlchan.net>
Date:   Mon Oct 10 19:47:43 2022 +0000

    Publish new post library-lookup.md

commit 7b634c18f0ad88a4d4dc00a0815cd86ad0b8fe4c
Merge: ab9e52e8 24094fb3
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Oct 10 20:46:12 2022 +0100

    Merge pull request #552 from alexwlchan/library-lookup

    Finding books in nearby library branches

commit 24094fb370f586dea5da64748580cca01dda75df
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Oct 10 20:44:01 2022 +0100

    toss in a cover image

commit 9cecdca17dabe1fcac1e3412c21ef534f5ee7e37
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Oct 10 20:40:11 2022 +0100

    tidy up the images and alt text

commit ab9e52e8e1b98e4a2b2c96bf42b898cb4a547776
Merge: 36cc409a 215a78bd
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Oct 10 20:30:20 2022 +0100

    Merge pull request #551 from alexwlchan/find-localhost-links

    Add a linting rule to look for stray localhost links

commit 83efe7b968091ae1bb08e31f3a1dca017efd7e3b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Oct 10 20:22:01 2022 +0100

    continue fiddling with the library post

commit c8785700d2f36ef6cf5cc492f0aa71ffea5e8306
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Sep 28 07:55:04 2022 +0100

    first draft of library lookup

commit 215a78bde2d318569f236e17f04c9d48a276cf68
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Oct 10 20:28:47 2022 +0100

    Add a linting rule to look for stray localhost links

commit 36cc409ad8e57a269c30577e4ffe15fd72d441dd
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Oct 9 14:51:46 2022 +0100

    Remove localhost link

commit af56bbfce89b3db37e0f4d2d43464f62a773d499
Author: GitHub Actions on behalf of Alex Chan <githubactions@alexwlchan.net>
Date:   Wed Oct 5 22:35:11 2022 +0000

    Publish new post circle-experiments.md

commit 3967c86fd67588358fb3a95c39d0eb223eae56e0
Merge: e2c4feb1 11f95499
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Oct 5 23:33:52 2022 +0100

    Merge pull request #549 from alexwlchan/circle-headers

    Add a quick post "Some experiments with circle-based art"

commit 11f95499733dd45e28ec8ae81220a09a2b507ed7
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Oct 5 23:31:31 2022 +0100

    run the png images through an optimiser

commit 75de1154be9ad2482b4699d8cfea925b2baac7b0
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Oct 5 23:27:17 2022 +0100

    Add a missing full stop in the footer

commit e2c4feb1180d8262f0eaef5bfe620ff8ea55fd4d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Oct 5 20:09:48 2022 +0100

    Update 2022-09-23-moomin-mathematics.md

commit 62a508d6e4cb4793713658701b0610a183489d20
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Oct 5 19:19:46 2022 +0100

    remove some extra braces

commit e72e2aa37c5261c6a065a75dc2a2f7176357672a
Author: GitHub Actions on behalf of Alex Chan <githubactions@alexwlchan.net>
Date:   Wed Oct 5 07:50:53 2022 +0000

    Publish new post snapped-elastic.md

commit 259b2fd20952f6e4d5103f7adf0b4ea5d659e8df
Merge: bbc2d90b d1226ff3
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Oct 5 08:49:38 2022 +0100

    Merge pull request #548 from alexwlchan/debugging

    Post: "Finding a tricky bug in Elasticsearch 8.4.2"

commit d1226ff36ea49bc8dea7ff23d3a2c80f5ca8ed12
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Oct 5 08:45:13 2022 +0100

    add two missing images

commit 23a128014b2062f02563502bea0984949f52e38d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Oct 5 08:41:05 2022 +0100

    tweak the cover image

commit 7d76c6e0717c636c5cbd5ec06a572468b1d81a3d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Oct 5 08:23:59 2022 +0100

    Markusp on the Elastic post

commit 2e8143ee4523d4db9e3b7f48616b7133448e42b9
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Oct 4 23:34:56 2022 +0100

    second draft of debugging

commit 1ca4783deae596cf27e87549669584141a81fb03
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Oct 4 21:22:57 2022 +0100

    redo the first section

commit 6b4c2f7d957c4cd1682ab6afd6b21da50039d0a7
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Oct 4 20:09:06 2022 +0100

    more elastic stuff

commit 20155459dcb7065e5253c5c17b801725d906b0ca
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Oct 1 08:51:04 2022 +0100

    first pass at the elastic debugging

commit bbc2d90bc363dff5aa13746fcf0168c93f6e1428
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Sep 28 07:55:18 2022 +0100

    tweak the homepage

commit dca5e76737e2afca85a9521804b04b773dd378a3
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Sep 25 22:32:13 2022 +0100

    better semantics, remove unused classes

commit c52c96b95634674c1dfe10006eeaaa1011e15ea9
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Sep 25 22:28:10 2022 +0100

    The word 'posted' is implicit

commit 041637d5d9c5302082a96129ca38a51f31e94d5d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Sep 25 22:25:02 2022 +0100

    Add a 'web-development' tag

commit c99391553971b69a6284cc719af1ed4d4a153384
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Sep 25 21:43:34 2022 +0100

    add a subtle background to cards

commit 6a3da829f9d6120dfb6b11b744555aae558f240a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Sep 25 21:22:58 2022 +0100

    Add the post date to cards

commit 34859bfc34ad6cf77ee4a2fd0f14e30081706730
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Sep 25 14:13:44 2022 +0100

    Rearrange the footer links slightly

commit 04fb39575e774638b615f13d7dd89390704a9cfa
Author: GitHub Actions on behalf of Alex Chan <githubactions@alexwlchan.net>
Date:   Sun Sep 25 10:55:25 2022 +0000

    Publish new post rust-1-64.md

commit 3751ad4bc9a1666de21454d7f9fce40d910c1a2b
Merge: 05705c9c 1173140b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Sep 25 11:54:01 2022 +0100

    Merge pull request #547 from alexwlchan/rust-1.64

    Add a post about Rust 1.64

commit 1173140b2cd64583e89add557ecb4ab0cd0021eb
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Sep 25 11:52:34 2022 +0100

    Update rust-1-64.md

commit 8c78d577d0d1fea2f095b7420b4f8e441d0eca86
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Sep 25 11:42:53 2022 +0100

    Add a post about Rust 1.64

commit 05705c9c004c89c925de93d1723ea610c8add78c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Sep 23 06:44:36 2022 +0100

    better title

commit 6a1accb42062ca11cd68c138cc953ffe3ac3287a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Sep 23 06:43:53 2022 +0100

    tweak the homepage card

commit 69aa6b08e4ae188aff86b2247c053682df861284
Author: GitHub Actions on behalf of Alex Chan <githubactions@alexwlchan.net>
Date:   Fri Sep 23 05:42:28 2022 +0000

    Publish new post moomin-mathematics.md

commit f1976d58da269be660446c5f05328b4bcb298025
Merge: 18d67625 63e2af1a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Sep 23 06:40:44 2022 +0100

    Merge pull request #546 from alexwlchan/moomin-maths

    Breaking the rules of division

commit 63e2af1ad869b6254b5f9a5b0b8b988ac9b4e936
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Sep 23 06:39:17 2022 +0100

    less harsh here

commit 5973b176a5ce9f69741e95f6d0dc581280928c04
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Sep 23 06:38:40 2022 +0100

    better final line

commit 681a8279c811ef8861be4b01ac26f580e311491b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Sep 23 06:37:29 2022 +0100

    add a post about Moomin maths

commit 18d67625ba1e847a5e9b5a21b05d833440ab6aaf
Author: GitHub Actions on behalf of Alex Chan <githubactions@alexwlchan.net>
Date:   Thu Sep 22 21:32:14 2022 +0000

    Publish new post maths-cross-stitch.md

commit c22a30a7c223df2e95d2e2bee5430f13f0b6f7dc
Merge: 0d8d66b3 ae184f0c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Sep 22 22:30:47 2022 +0100

    Merge pull request #545 from alexwlchan/maths-sampler

    Add a post about my maths sampler

commit ae184f0ca1eaed9a8ad923ed720f1b83d6b32200
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Sep 22 22:28:25 2022 +0100

    Add a post about my maths sampler

commit 9a8d2cf3450a1a8c23371dba659b56cc7062456c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Sep 20 08:51:09 2022 +0100

    Initial draft of the maths sampler post

commit 0d8d66b38b7029f379ef813c77bca5bc1eb2b650
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Sep 16 22:11:37 2022 +0100

    fix the 2:1 aspect ratio

commit 86ccb225e21ff5d1578ab8935f79e32f49a88f73
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Sep 16 22:08:58 2022 +0100

    add a card for the "all posts" page

commit 63160e2a324ecf4846f023285eb7ca4dcb01d8f5
Merge: 437c3451 d756f380
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Sep 16 09:02:15 2022 +0100

    Merge pull request #544 from alexwlchan/more-tag-fixes

    Tidy up a bunch of stuff for tag filtering

commit d756f38011f8c719a0adc2a7fc2eabadf5d70484
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Sep 16 09:00:29 2022 +0100

    remove an errant newline

commit c5a0e594f51ae9aab16759d34986e9d18d19406c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Sep 16 09:00:24 2022 +0100

    Throw a less cryptic error for a missing twitter:image attribute

    Previously this gave the less-than-specific output:

        Checking Twitter card metadata...
        jekyll 4.2.2 | Error:  bad argument (expected URI object or URI string)

    which is because the value being passed to the `URI` is `nil`.

commit 6889fb709d88b49772a28547a92ff1c21006ac0f
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Sep 16 08:47:59 2022 +0100

    update a bunch of tags on old posts

commit 2fbf205577feba2698732200f1573e1274c313ee
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Sep 16 08:47:21 2022 +0100

    remove tag saving

commit f0e96728d913f8726788ad854d9d9e0ddd584115
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Sep 16 08:46:59 2022 +0100

    okay, but actually filter the tags

commit 126644651b5522607959aae89791537bb35091fc
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Sep 16 08:15:26 2022 +0100

    don't send users to /all-posts/?tag=_nofilter_

commit abdd90a908f3258f17ffd0cfe7f438afbcb4b6f5
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Sep 16 08:15:12 2022 +0100

    dump a copy of all the tags to a file

commit ef1eb9933bbcd97683e04bef6fdc60c293e3778a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Sep 16 08:15:01 2022 +0100

    do tag filtering in the plugin

commit d38ccde3adbd513780e3ab16461cc85b522714dc
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Sep 16 07:53:23 2022 +0100

    use underscore case

commit 9664aa76116ee03e7037a4ea0bb579459f9bd4b3
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Sep 16 07:50:26 2022 +0100

    tweak the appearance of the tag filter on mobile

commit 437c34518811e67be94c0dfa0baf2a245baf827e
Merge: c2121c6e 0c7c600e
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Sep 15 23:15:51 2022 +0100

    Merge pull request #543 from alexwlchan/post-pruning

    Improve the way tagging works

commit 0c7c600e99f2908c5fd7b3a3345e8583cb13b12f
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Sep 15 23:14:21 2022 +0100

    fix a couple of broken links

commit a7c15de13f80c83a165943d09f5204439c3ba079
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Sep 15 23:00:11 2022 +0100

    tidy up some tags

commit 1b6cb556890994926c29fdf9a3f06b0f148bdd8c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Sep 15 22:58:41 2022 +0100

    remove the 'bash' tag

commit c29904b8286aa9e877bca6fe17c7fecce86bad91
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Sep 15 22:57:00 2022 +0100

    remove the old 'all posts by tag' code

commit c87c9c914fd1a883f4b8b2b43be19325bfc3d9d9
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Sep 15 22:54:40 2022 +0100

    do funky stuff with URLs

commit d99067bd62dae634b2a54ea6203a2637bb9c474c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Sep 15 22:54:32 2022 +0100

    link to visible tags on pages

commit 042090d0b5c6903e2f01eac1a9de336eaa33a5f4
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Sep 15 22:42:10 2022 +0100

    add a style for 'novisited' links

commit bf650be8efcbc0c84c6700d689ade854c728b70d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Sep 15 22:39:24 2022 +0100

    continue twiddling with tag filtering

commit 3a03ec3fca8d52b300e346e880648c8b48ee3ea4
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Sep 15 22:31:24 2022 +0100

    get post tag filtering working!

commit c62c550506e4306a19ec249ed7e237910b31727b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Sep 15 21:35:58 2022 +0100

    Add the year and tags to a card

commit ca6c3da52b638a3c6a11814434c8652543c1f298
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Sep 15 21:33:14 2022 +0100

    exclude a couple more posts

commit cc4a46574fa9319904499925377573bbac13d683
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Sep 15 21:31:53 2022 +0100

    Put cards on the per-year/per-month indexes

commit b89e68bccd38c8e604a2afea1fda41609fa40ef9
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Sep 15 21:27:03 2022 +0100

    Remove an unused plugin filter

commit cfedeef9221868f4ee009e08437193882c8aee87
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Sep 15 21:23:25 2022 +0100

    Remove tags from unlisted posts

commit c2121c6e737af0cf141e575c82a1cc36744e867f
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Sep 15 08:03:41 2022 +0100

    fix the 2:1 aspect ratio on the card

commit 29c7a2c9604febce06b3373c917c3a4c9897b3c7
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Sep 15 08:00:11 2022 +0100

    add a DynamoDB calculator card

commit 66baa67384647854eb10ce4314f658854f27f499
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Sep 15 07:40:52 2022 +0100

    fix the 2:1 aspect ratio on this card

commit 3edab3a3d393787f011c65897dec3e21a5673d18
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Sep 15 00:48:02 2022 +0100

    change the Lorenz Wheels card

commit 6cef6e93ab3db8c66be118bb99ffcd4a70256c91
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Sep 15 00:45:42 2022 +0100

    tweak the Route 53 card

commit 290ac5447e79b8a9a38e94393e135410f7b27b15
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Sep 15 00:43:23 2022 +0100

    add another comment about article cards

commit 7f2cf91f373b031e46bcd8a983fb569815fc48d7
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Sep 15 00:40:41 2022 +0100

    tweak the tint colour for "what year is it"

commit faa5ffebc1b1ebaa4ded8e4d6876f1e1c959090e
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Sep 15 00:40:32 2022 +0100

    add a default card for every post

commit de0fd9bb7fc55884649e7157995a81080f1bed9e
Merge: a1531a63 0b0c95e6
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Sep 15 00:22:05 2022 +0100

    Merge pull request #542 from alexwlchan/fix-cards

    Make a couple of improvements to cards

commit 0b0c95e6a1179554fcc6574530d85f089d43783a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Sep 15 00:19:41 2022 +0100

    add a card for non-commuting strings

commit 443a55630e693f7b18a03364456f9580745f5bd2
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Sep 15 00:16:02 2022 +0100

    exclude another post from the index

commit 11a38b1e48f11815da90a74e54513d197d9c1b9d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Sep 14 23:59:21 2022 +0100

    Improve the display of cards when there's only one in a set

    This isn't very useful now, but may be useful when I start adding some
    changes for tagging.

commit a1531a63e8c8cd01e7d4a137a259c999943c62bc
Author: GitHub Actions on behalf of Alex Chan <githubactions@alexwlchan.net>
Date:   Tue Sep 13 18:31:41 2022 +0000

    Publish new post graph-generative-art.md

commit 613f24867495a805182d24a9e2f7f7ef67f745e7
Merge: 5d108bb3 b93cf58a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Sep 13 19:29:48 2022 +0100

    Merge pull request #541 from alexwlchan/gena-rt

    Post: "Generating art from lattice graphs"

commit b93cf58a9acd3b278679a2503a2839ae40f8a4f1
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Sep 13 19:27:43 2022 +0100

    fix relative/absolute links

commit 6e7140800006dc8eed72507f426ec0b3c627cec6
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Sep 13 19:16:23 2022 +0100

    one more markup

commit a1ac8f92559a6221e3e3032748da1aa121d7e662
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Sep 13 19:13:55 2022 +0100

    sort out the generative art post

commit 96b7c3e30c286e8e273c7a55f3475f6bda842c5b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Sep 13 18:27:48 2022 +0100

    add cards, continue tweaking

commit b7c37ad9d9c4f56c322da2c67bcefe30d8906f5e
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Sep 13 17:52:54 2022 +0100

    get all the graphs into svg

commit 4775d328204bc46a96b5f1f9c3bc1056d549c5e5
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Sep 13 07:38:04 2022 +0100

    remember to inline the class attributes; continue to svg-ify

commit ba7284eb3ed80bb8634726b0bd0d898aebef89bf
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Sep 12 21:25:10 2022 +0100

    rip out the section on graph theory

commit e3c0a1e17a6949152de4cdb1f878b8cd7a0dd8a4
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Sep 12 20:58:46 2022 +0100

    start adding the inline svgs

commit 4da760da1e5bb7e5d89ca727de38c6fcfc09bc40
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Sep 12 18:59:36 2022 +0100

    add the initial post

commit 5d108bb3e10ec12808238176d3917b2a38d807eb
Author: GitHub Actions on behalf of Alex Chan <githubactions@alexwlchan.net>
Date:   Sat Sep 10 17:04:32 2022 +0000

    Publish new post nextjs-props.md

commit 49b1221dd5253f12a835b2d9ae23afe71c17223d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Sep 10 18:02:17 2022 +0100

    Add a quick post about Next.js props

commit 0265271ec2c24b99f6a9ceaf24c357bb489146e7
Author: GitHub Actions on behalf of Alex Chan <githubactions@alexwlchan.net>
Date:   Sun Aug 28 16:49:37 2022 +0000

    Publish new post blink-diffs.md

commit 75473923a71e89e8c96bc7e456bd772abb226199
Merge: 2772fa38 ff4077e0
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Aug 28 17:47:14 2022 +0100

    Merge pull request #540 from alexwlchan/blink-diffs

    add a quick post about blink diffs and Darkroom

commit ff4077e0e4d5395106e08842cfecc1d5c281bfe1
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Aug 28 17:45:03 2022 +0100

    this should have a 2:1 aspect ratio

commit 315e07509a5d1af17a894321e8507814287d6fd0
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Aug 28 17:41:50 2022 +0100

    add a pair of missing images

commit 26d84ef488d5a95854aaa0876c6698c351071d2c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Aug 28 17:38:38 2022 +0100

    add a quick post about blink diffs and Darkroom

commit 2772fa3892f74c6ffea655a41460bddbfa63d126
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Aug 21 16:22:03 2022 +0100

    Add a couple of new cards

commit 742ff3de042fe60027928379f0e48a45d9f29bfc
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Aug 19 22:51:09 2022 +0100

    add a card for my os-sep post

commit 018336906a5617e16764a27d3c9b3b641daaa4b2
Author: GitHub Actions on behalf of Alex Chan <githubactions@alexwlchan.net>
Date:   Thu Aug 18 07:22:45 2022 +0000

    Publish new post strict-jinja.md

commit c66db0a6b4737e3a8e2fcf0979d27001ee5bdb3a
Merge: f9c457a9 ec0458ab
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Aug 18 08:20:47 2022 +0100

    Merge pull request #537 from alexwlchan/jinja2

    Post: "I always want StrictUndefined in Jinja"

commit ec0458ab8055454bfda60d46db6fdf6292bd4108
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Aug 18 08:18:33 2022 +0100

    jinja2, not Jinja

commit 9595f6dc98942b87646282bd615e64b92c0f4691
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Aug 18 08:18:08 2022 +0100

    Add a quick post about undefined in Jinja

commit f9c457a9429524f4e5754be33098fbaf8ad1dff6
Author: GitHub Actions on behalf of Alex Chan <githubactions@alexwlchan.net>
Date:   Tue Aug 16 06:46:19 2022 +0000

    Publish new post egyptian-mixtape.md

commit 412e8046fb194aa7eba31f490f861d8fe73e479d
Merge: 3b6e1241 0767d525
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Aug 16 07:44:25 2022 +0100

    Merge pull request #536 from alexwlchan/egyptian-mixtape

    An Egyptian 'mixtape' of embroidered material

commit 0767d5258822a14f4f36a194c38f15912be2b6c7
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Aug 16 07:41:15 2022 +0100

    small wording tweaks

commit d677483141b5aabf498ce138dc319274eae49589
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Aug 16 07:40:14 2022 +0100

    Add a quick post about my 'Egyptian mixtape' cross-stitch

commit 3b6e12411b81156a88ae3268282adb7aacfebab2
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Aug 16 01:33:30 2022 +0100

    continue filling out the cards

commit b490124befb04337785c820db576af9b9ca9ab71
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Aug 16 01:31:40 2022 +0100

    Add a card image for Voice Control and AppleScript

commit 2a0df2e1baa1a24e9630663ac5a2a8769e0b8517
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Aug 16 01:27:12 2022 +0100

    add a couple more post cards

commit 205274f065c94824dc97cbdde3f4ac83c7c644c1
Merge: df47288a f1653d47
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Aug 16 01:13:44 2022 +0100

    Merge pull request #535 from alexwlchan/new-index

    tighten up the words on the homepage

commit f1653d47aaf3e5ac2897f669288aa726a0aa3aad
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Aug 16 01:11:28 2022 +0100

    tighten up the words

commit 0061011f6fe949695161de50e020f67d232d39e6
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Aug 16 01:10:53 2022 +0100

    Tidy up the index page

commit df47288aa97feadd61ff1d4804160e43e75bd82f
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Aug 10 23:15:25 2022 +0100

    Update 2022-08-10-circle-party.md

commit 761f32e652ddb4f2bfcd7f2118ae169ebb1709c0
Author: GitHub Actions on behalf of Alex Chan <githubactions@alexwlchan.net>
Date:   Wed Aug 10 22:10:43 2022 +0000

    Publish new post circle-party.md

commit 6c83f011b2ec83d3c7c6396861983ccea34d6f65
Merge: 27e19f72 903b50a4
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Aug 10 23:08:45 2022 +0100

    Merge pull request #534 from alexwlchan/add-svg-arcs

    add a quick post about circle diagrams

commit 903b50a4ab551d26ac8e03f3a2ed0defa96b1f48
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Aug 10 23:06:28 2022 +0100

    add a quick post about circle diagrams

commit 27e19f72cca85993486ef1b46eb95ac4c8c2dcc7
Author: GitHub Actions on behalf of Alex Chan <githubactions@alexwlchan.net>
Date:   Mon Aug 8 07:49:40 2022 +0000

    Publish new post buildkite-deployments.md

commit 3b51d1765abb44d6a6fe11b3c26c57c0cfb6fee5
Merge: 6325c3d1 286fcfc3
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Aug 8 08:47:25 2022 +0100

    Merge pull request #533 from alexwlchan/buildkite-deployments

    Quick post: "How to customise the title of Buildkite builds triggered from GitHub deployments"

commit 286fcfc3ef4db256cfafdfe10ea95c52dcac4832
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Aug 8 08:40:51 2022 +0100

    Tint cards on the homepage red if no explicit colour

commit 4862a515d1dfe80004a3853f8d8a1bdc4ffca92c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Aug 8 08:40:41 2022 +0100

    Add a quick post about Buildkite deployment titles

commit 6325c3d19ec01c476bb1fc1c19b96f10665057cb
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Aug 8 08:37:58 2022 +0100

    make sure the "our place" card is 2:1

commit 6818bbd7a85905ea34140701275da085c014c5c1
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Aug 8 08:05:50 2022 +0100

    reduce the size of the 'our place in space' card

commit a59cd0bfb0d39aa4c98417b4c08d5cd05fe9fdbd
Author: GitHub Actions on behalf of Alex Chan <githubactions@alexwlchan.net>
Date:   Sun Aug 7 21:47:27 2022 +0000

    Publish new post spaaaaaace.md

commit 265ccae935841ffed1d34185de99a4984a2af920
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Aug 7 22:45:13 2022 +0100

    Update README.md

commit ebb077150ca4f1813b066241c0e3725937133191
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Aug 7 22:43:13 2022 +0100

    Update README.md

    [skip ci]

commit 155b25c1550920b654b0b4c4ba8f53554c7e4c4a
Merge: d48893b5 aa14552b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Aug 7 22:42:20 2022 +0100

    Merge pull request #532 from alexwlchan/our-place-in-space

    Add a quick post for "Our Place in Space"

commit aa14552bc1f1b7a1aeeb620355d03b54f8d65c16
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Aug 7 22:38:52 2022 +0100

    quick markups

commit e531fd03df6086bd5c07d3a4dd8ba8ea425f8f88
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Aug 7 22:37:27 2022 +0100

    Add a quick post for "Our Place in Space"

commit d48893b5d274e01a08c91d447a4bcea3aa00ef2b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Aug 3 20:44:07 2022 +0100

    Update 2022-08-03-no-cute.md

commit ba06c2edf0d8b7c6cd09dfa5f58bd66394351abe
Author: GitHub Actions on behalf of Alex Chan <githubactions@alexwlchan.net>
Date:   Wed Aug 3 19:36:17 2022 +0000

    Publish new post no-cute.md

commit 6a64a49b8fa3cc1abfd1737c41faaf135741685a
Merge: 4fc268ca dd8e75de
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Aug 3 20:34:25 2022 +0100

    Merge pull request #531 from alexwlchan/no-cute-errors

    Post: "Cut out the cutesy errors"

commit dd8e75de3af4a043c44a2b105473c80685e22f1b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Aug 3 20:31:39 2022 +0100

    add some tags

commit f702c4f0d869e018a7c7cb1fac6d84dbaa974926
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Aug 3 20:23:27 2022 +0100

    add missing alt text

commit bdc22a748fdf632ecde9304a2e234a0c6b1e1009
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Aug 3 20:19:28 2022 +0100

    scribble a post about cutesy errors

commit 4fc268caea87d4214ea2abb0bf19aadd4bf36f3b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Aug 3 08:31:33 2022 +0100

    Update 2020-10-12-the-importance-of-good-error-messages.md

commit 61730446d0dc394fb9d5d99cdaf1caad8d95e02e
Author: GitHub Actions on behalf of Alex Chan <githubactions@alexwlchan.net>
Date:   Mon Aug 1 08:21:03 2022 +0000

    Publish new post screenshots-go-gangbusters.md

commit c8756f49d05af9e11b5a07c410961c15a8d48b65
Merge: a451401d 07cdebcc
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Aug 1 09:19:19 2022 +0100

    Merge pull request #530 from alexwlchan/surprise

    Post: "A surprise smattering of stardom"

commit 07cdebcc5de1b77c059c9db8a03f94f2b0c4d98b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Aug 1 09:17:04 2022 +0100

    Remember to check in the images

commit 4cd52ea3fcef8174fae67fb4ff8699d135ccb92e
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Aug 1 09:11:43 2022 +0100

    Quick markups on the surprise post

commit da58093f9a85b017b549183de0e18dfc60da3566
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Aug 1 08:33:13 2022 +0100

    First draft: "A surprise smattering of stardom"

commit eebe621028631b184b38c5f7c52270a3603be706
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Aug 1 08:33:05 2022 +0100

    Ignore the favicon README when searching tags

commit a451401d8b5829671655b2bf1f4cac897637263f
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Jul 26 12:27:40 2022 +0100

    Clarify that I'm no longer involved with PyCon UK

commit 693383a87945cf91541212bb45d83cf9bcd60343
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Jul 25 07:45:17 2022 +0100

    add multiple image resolutions

commit d04632134c406479e8f631a8ba801c037cb47d9f
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Jul 25 07:36:53 2022 +0100

    Make this image smaller, holy bandwidth batman

commit 51e476be8c556905b784eff7c494f7c8b9e36300
Author: GitHub Actions on behalf of Alex Chan <githubactions@alexwlchan.net>
Date:   Sat Jul 23 08:45:43 2022 +0000

    Publish new post screenshots.md

commit 495df2b42a3003995835312f56893df555d40375
Merge: 02728f11 ed419193
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Jul 23 09:44:01 2022 +0100

    Merge pull request #529 from alexwlchan/screenshots

    Post: "You should take more screenshots"

commit ed4191931f0643ceeff6b55a5a43be3e705dc09e
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Jul 23 09:42:14 2022 +0100

    Fix the aspect ratio on the card

commit 95a88736815805b407e47a27bba5de26caf04691
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Jul 23 09:16:28 2022 +0100

    Markups on the screenshots post

commit a4fbb01a47af9a1a6fc09441fd26ba475ea7adba
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Jul 23 08:56:27 2022 +0100

    Another pass at the screenshots post

commit 3657c167185c5026173e394f6556e1fa82d22c56
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Jul 23 08:24:28 2022 +0100

    Add some extra text cleanup filters

commit 722161592e66ba4b7b4700b3010b104e8b3875ae
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jul 22 22:14:17 2022 +0100

    another pass on the screenshots post

commit ce6495461c88cc85cba2698cb364fa073f229949
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jul 22 21:23:30 2022 +0100

    Initial draft of my screenshot post

commit 02728f11ef93f715f71d7879158b4bc82ceb0369
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jul 22 21:44:11 2022 +0100

    fix the aspect ratio

commit a579b4d5142574546eb98ca6c73dace10c5b6bef
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jul 22 21:40:43 2022 +0100

    Add a card for non-breaking spaces

commit dce9c0f943be99b4febcf702d1c4247090c7ba25
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jul 10 20:58:16 2022 +0100

    nope

commit a66862cf979ef14f1ccf2d2335cbea0eea04e247
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jul 10 20:53:32 2022 +0100

    moar cache bust

commit 9c8b7052f8424e5fc80580263c9a7d5a6255ef71
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jul 10 20:45:24 2022 +0100

    fix the date on the plaque

commit deea7583038c9256c4bf4d6473704afa18ae9621
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jul 10 19:45:29 2022 +0100

    time for cache busting

commit af9d7c35e366bf3259d32e78964a6e64c6ce1e06
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jul 10 19:45:14 2022 +0100

    I can guess about when they land

commit d328b5dbce12975b7aa145f63a476dcc107483fd
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jul 10 18:13:19 2022 +0100

    tweak the summary text

commit c0ba6f387699090f0130efc35e1e7d431df7a959
Author: GitHub Actions on behalf of Alex Chan <githubactions@alexwlchan.net>
Date:   Sun Jul 10 17:09:12 2022 +0000

    Publish new post martian-plaque.md

commit e473ca134bb6d6edd305eefa117c4f9cf1c3f642
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jul 10 18:06:54 2022 +0100

    add some tags

commit 2903c2d7f9707096fecb4b98a69d6508115d4286
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jul 10 18:04:18 2022 +0100

    Add an image of my Martian plaque

commit dd6ac90ada1f662c1e0f83636c619abe670df311
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jul 10 17:58:57 2022 +0100

    Markups on the Martian plaque post

commit 2040a9f79a43eabc58100d236362149840266c66
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jul 10 17:37:58 2022 +0100

    Add an initial draft of the Martian plaque post

commit 44e559ac07ad33bf2b26b2c463bb790264c7116a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jul 10 13:56:39 2022 +0100

    bin the ko-fi

commit 1d72992f09cca996d0fdaf701e8e5f1526fc165c
Merge: a96a0eb3 80336825
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jul 3 19:20:03 2022 +0100

    Merge pull request #528 from alexwlchan/full-width-images

    Allow marking images as full-width on narrow screens

commit 8033682570423b248e0df6f01ad571b19190d84a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jul 3 19:16:18 2022 +0100

    Allow marking images as full-width on narrow screens

commit a96a0eb3d2adae7499fe9ab2a5d80f00e29d36aa
Merge: 3aa1f931 03380594
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jul 3 19:08:10 2022 +0100

    Merge pull request #527 from alexwlchan/tidy-css

    Tidy up the CSS and styling a bit

commit 03380594e9023e1659d454733cbe1b79ebedac24
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jul 3 19:03:07 2022 +0100

    Make these values align nicely

commit bb29568ae77651a8175c1b26b8242e913cb50c83
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jul 3 08:49:47 2022 +0100

    Inline all the one-off CSS

commit 71dddcec5027ec392e6dd02b960e2c0fd92b69ab
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jul 3 08:46:54 2022 +0100

    Remove a bunch of unused CSS variables

commit 69ed6f7a78dd06ff9391766ae6bc239e76d70a27
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jul 3 08:43:30 2022 +0100

    Restructure the Sass slightly

commit 3aa1f93166b29cf772874d7e3b2106154392c005
Merge: 4e74c095 6568dcd7
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jul 3 06:37:48 2022 +0100

    Merge pull request #526 from alexwlchan/favicons-in-chunky-png

    Create favicons in Ruby rather than shelling out to imagemagick

commit 6568dcd7cfccf3b16ff05988a7b83eef0f9bc904
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jul 3 06:36:02 2022 +0100

    Exclude the new README from linting

commit 79085ae3c577e68094c9764211194f673254a2b2
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jul 3 06:31:51 2022 +0100

    remember to set the fill colour

commit 7bfe5e0b0c4dc6ae676354aa0c57a42fa5e582e1
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jul 3 06:28:15 2022 +0100

    these should be png, not svg

commit dc688d342b59af28bb5a110a59f351e119626c7c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jul 3 06:18:48 2022 +0100

    Add the new favicon templates

commit 97f1ecd4b7f9d8cc88fafe339aafddb18229e27d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jul 3 06:18:33 2022 +0100

    Create favicons in Ruby rather than shelling out to imagemagick

commit 4e74c09517ede3bf3e5a57edd311631148340c77
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jul 3 04:38:15 2022 +0100

    Update 2022-06-26-alfred-to-github.md

commit db53beeb545e33dbd7521a9f1df94b8bd26984de
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jul 3 04:37:58 2022 +0100

    Update 2022-06-26-alfred-to-github.md

commit 7ca69aaff9ad75378ff4bb15a0c6f3e5d2d026c6
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jul 3 04:31:40 2022 +0100

    Update 2022-06-26-alfred-to-github.md

commit 26872c66c79eafdb8e595103ee9916efb1017dea
Author: GitHub Actions on behalf of Alex Chan <githubactions@alexwlchan.net>
Date:   Sat Jul 2 10:17:47 2022 +0000

    Publish new post saturn-v.md

commit 89f2be5992e18c4735363a0406b8fe39ab0a7234
Merge: 4d535a71 39b7ee7a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Jul 2 11:15:38 2022 +0100

    Merge pull request #525 from alexwlchan/saturn-v-stitch

    Post: "One small stitch for yarn, one giant leap for yarn-kind"

commit 39b7ee7af10433088ba6fd0a40ad0dd9ee71a883
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Jul 2 11:13:48 2022 +0100

    Remember to set alt text when it comes from Twitter

commit 7049d67280216f5ee1574a7dd75548526b760127
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Jul 2 11:01:58 2022 +0100

    Flip the title and the summary

commit 60669492ce7418a9cd431d0a50e05ff558e24873
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Jul 2 11:01:09 2022 +0100

    Markups on my Saturn V post

commit 67185b8a72a87009c30b5d3e9025e961376b5e49
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Jul 2 10:50:21 2022 +0100

    Initial draft of the Saturn V post

commit 4d535a717643776a322ec5906778938e82ecc176
Merge: b800b4a5 5c4ca95d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Jul 2 10:13:38 2022 +0100

    Merge pull request #524 from alexwlchan/tweet-plugin-improvements

    Support twemoji in embedded tweets

commit 5c4ca95ddd8eff2f41a64394e6a4046b8e5d7963
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Jul 2 10:05:32 2022 +0100

    Style sheets should always be regenerated

commit d8ec978bbb5c53bf0f57f3855caa83e01b641453
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Jul 2 10:05:25 2022 +0100

    Add support for inline twemoji

commit 4f546433b64549d6e5a81ee401d3843f3e3b832c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Jul 2 09:31:23 2022 +0100

    Move avatars into a dedicated subdirectory

commit 7379a69b00f9f1eff9ad47e073116e432b1ff621
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Jul 2 09:30:05 2022 +0100

    Move posts into a dedicated subdirectory

commit b800b4a5064cbaeccf88a33383142450f27bf62f
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jul 1 20:16:27 2022 +0100

    This should continue the loop, not exit the function

    It's a holdover from when the `create_shelf()` code was a standalone
    function, called once per colour.  It's wrong now that code has been
    inlined.

commit 54fbb38d73cef0e12c504c394decd9599e62a691
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Jun 27 22:54:32 2022 +0100

    Update 2022-06-26-imaginary-numbers.md

commit 5bf4cb10b3f9d80da490f5fed4ef27e068cdc3e4
Merge: c3910dda b5789acd
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Jun 27 22:51:57 2022 +0100

    Merge pull request #523 from alexwlchan/generated-header-images

    Generate the header images programatically

commit c3910dda06a78184b5ff6ec4ce991bb69f2d7a43
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Jun 27 22:50:54 2022 +0100

    Update stylesheets.md

commit b5789acdae8b0724e0032a8fc62a01aa2d0c0486
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Jun 27 22:49:30 2022 +0100

    Generate the header images programatically

commit c04155f5b8ced2935e4612e16df87896af5d9608
Merge: 26d6118a 78d33833
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Jun 27 22:09:51 2022 +0100

    Merge pull request #522 from alexwlchan/cache-generated-theme-assets

    Push generated theme assets into dedicated directories

commit 78d33833696aa3efa57d1c32335f527ce4109c26
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Jun 27 22:07:26 2022 +0100

    Add a missing slash here

commit 7c2fdb378ac575f11f82bf87ca599ce000ac5980
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Jun 27 22:06:39 2022 +0100

    Push generated theme assets into dedicated directories

    This means I can put the entire directory in the `keep_files` setting,
    rather than wildcards which don't seem to work -- and then we can skip
    regenerating the assets on subsequent builds.

    This isn't much of an issue for the CSS/favicons, but it's more of a
    concern for the header images, which are substantially larger.

commit 26d6118a84b9b0afdaca742035d5db79ed8c5c6f
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Jun 27 17:48:41 2022 +0100

    Update 2022-06-26-imaginary-numbers.md

commit d2d2e78a79bdd39b147f3e6737de8bec6289a825
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Jun 27 17:42:08 2022 +0100

    Update 2022-06-26-imaginary-numbers.md

commit dd14e9f83288506f6e5c081423ddd8d6bddffe6b
Author: GitHub Actions on behalf of Alex Chan <githubactions@alexwlchan.net>
Date:   Sun Jun 26 23:04:52 2022 +0000

    Publish new post imaginary-numbers.md

commit 58631a62589e4ef6bf2910a47d3f6e094a7106e1
Merge: e486bd36 aa80b589
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Jun 27 00:03:14 2022 +0100

    Merge pull request #521 from alexwlchan/phone-number

    Post: "Fictional phone numbers in For All Mankind"

commit aa80b589a3c3a0d46dfaf10e610fc1d2fb8529d9
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Jun 27 00:01:29 2022 +0100

    Update imaginary-numbers.md

commit 31aa04ff21b689006c306570df11208cee0f9489
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jun 26 23:51:02 2022 +0100

    couple of markups on the FAM post

commit 30bdbabfb7869134d153f10c837daf5db4ecc352
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jun 26 23:44:07 2022 +0100

    First draft of a post about imaginary numbers

commit e486bd367b6fa914fbaea440aa529e631451e3cd
Author: GitHub Actions on behalf of Alex Chan <githubactions@alexwlchan.net>
Date:   Sun Jun 26 20:53:04 2022 +0000

    Publish new post alfred-to-github.md

commit a984075837c1ef912606112c4d21c4bb9f3fbeb1
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jun 26 21:51:06 2022 +0100

    Try fixing it in the GitHub Actions workflow

commit 9b7a5cf3a1f1cb574ead1b24c5cb78c23bc6aab2
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jun 26 21:50:33 2022 +0100

    Revert "try fixing the 'publish drafts' plugin"

    abea6fc14c428c0dd7fe2c8f61cd5a5102f775aa

commit c597dc659351e02d81d8d629107f93b819179708
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jun 26 21:40:39 2022 +0100

    try fixing the 'publish drafts' plugin

commit e5befa3b2a619eb71342c2c2cb9ba1daca6f2b0c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jun 26 21:34:50 2022 +0100

    hard-code the jekyll version for now

commit 995e80ed45667f68ba7b4f05d22260750251f174
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jun 26 21:28:59 2022 +0100

    Extract the Jekyll version number automagically in the Makefile

commit 8d2dae7c7eba0c9555c8f8bf9f7e5e22b0131c31
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jun 26 21:20:40 2022 +0100

    Make sure we don't display an empty dash on the index page title

commit e772f4796773684ba510533ed256b8cbe00decf1
Merge: 080eac33 97780e24
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jun 26 21:17:37 2022 +0100

    Merge pull request #511 from alexwlchan/updates

    Post: "Creating an Alfred Workflow to open GitHub repos"

commit 97780e24b41bbdd1fe38118f3f500f9dd13b6f3b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jun 26 21:15:29 2022 +0100

    fix the jekyll syntax here

commit fcb93bbb4b3f014632fa853ebae4be91acc17dc4
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jun 26 21:14:57 2022 +0100

    We want 'layout: post' for a draft

commit d3f3bbe7bf1d1f693439b7b28e91fc75b41c57e2
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jun 26 21:11:01 2022 +0100

    Add a missing card image

commit 49b5caee11dc98067bbc6b42422fe54a377e31ea
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jun 26 21:08:15 2022 +0100

    don't use .docs here

commit 23d1c05c294b6fd6482a53764394893494b8b95e
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jun 26 21:05:32 2022 +0100

    move the .docs method to the right place

commit b363f20291bb0bcb4da58d91ac14e355378c69fb
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jun 26 20:30:20 2022 +0100

    remember to fetch colours for pages

commit 4916e8d8d3e77824c1b45ffd60f75c84b2c3c0e4
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jun 24 08:48:27 2022 +0100

    Add alt text and post markups

commit f06f1d6c95d754b054606e903986afedc604d0c6
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jun 24 00:11:58 2022 +0100

    Various bits + draft Alfred post

commit 59276b24f4529b24f417a23fcb774fe09ba849cf
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Jun 23 23:24:18 2022 +0100

    Go for a leafy green home page

commit 080eac3371c98451699b26f9da3e742af7f43bce
Merge: 29ecde83 28456e14
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jun 26 19:29:02 2022 +0100

    Merge pull request #519 from alexwlchan/generate-favicons-at-build-time

    Generate favicons at build time

commit 28456e14819263136545aa79e57b0fd2cec266bc
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jun 26 19:26:52 2022 +0100

    Generate favicons in a Jekyll plugin

    This means they're now consistent, and they can be generated for an
    arbitrary theme colour on a page, rather than the handful I'd made
    previously by hand.

commit 44b91ee4e656f4f347fd80df756446daa816f8fa
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jun 26 16:08:26 2022 +0100

    Add ImageMagick to the Docker image

commit 29ecde836ba6327ad20a448f4522b5502e4fe7dd
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jun 26 15:53:41 2022 +0100

    Tweak how post cards are handled

    * Set an aspect ratio in CSS, so browsers that support that don't have
      to keep re-drawing the page as images get loaded
    * Add the `loading="lazy"` attribute so browsers don't load all the
      images at once, only as they become visible

commit efaa14ecac06d149de49dd14a7719a5ccfa4b5fa
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jun 26 15:25:43 2022 +0100

    Add a missing variable

commit 123bd87a74164ff7f9562005e3e7ad91d121f9ee
Merge: 07437cdf cf3aac13
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jun 26 15:14:03 2022 +0100

    Merge pull request #517 from alexwlchan/generate-scss-at-build-time

    Generate the per-colour SCSS files at build time

commit cf3aac136140e039eb20ba7c86086585f3cf3cf7
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jun 26 15:13:28 2022 +0100

    Remove the commented-out code in the theming plugin

commit 8845105f247f3f69df98fe9a34f221a2b649fd6d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jun 26 15:12:19 2022 +0100

    Fix a warning about excerpt separators

commit 9d3660ac53a0d99ae36a26972db030fd7efdbf56
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jun 26 15:12:06 2022 +0100

    Generate the per-colour SCSS files at build time

    Previously these files had to be generated and checked in, but they're
    automatically generated derivatives.  It's easier to generate them at
    build time and dump them straight in the `_site` directory than have them
    cluttering up `src`.

commit 07437cdf5a4dd1e843b86ce4beaa3de4a06b3b19
Merge: 84cd6a0f bd34aa4d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jun 26 08:39:12 2022 +0100

    Merge pull request #514 from alexwlchan/check-layout-type

    Check that layout types are correct

commit bd34aa4d954397b4b0a7dc49b331a264cdece19e
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jun 26 08:36:44 2022 +0100

    Check that layout types are correct

commit 84cd6a0fe227294738077c476b60f9f0cc779c40
Merge: 25a63fd0 d714d7f5
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jun 26 08:24:58 2022 +0100

    Merge pull request #513 from alexwlchan/json-schema-linting

    Add a JSON Schema for my Markdown front matter

commit d714d7f5b42743e9e83d46b867a02271adee3811
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jun 26 08:23:22 2022 +0100

    Remove the notes index page

commit ea9e72bea06592fd4926c2058e8a17c6964d80b3
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jun 26 08:22:23 2022 +0100

    this is just linting, no HTML involved

commit 8a117ffbccc3685c29e1e2a1eaa00f1a91433c91
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jun 26 08:18:41 2022 +0100

    fix an instruction in the README

commit 2304f006f393cc052b379b9fbc28bde3449d10bc
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jun 26 08:18:04 2022 +0100

    Re-enable the other linting commands

commit 25e86355471cad7d4c26695b1a1b9f4ba38cf8d1
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jun 26 08:15:01 2022 +0100

    Add some docs for front matter validation

commit 7d51bfddbfb9760894aba3f8b70fb0228669087a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jun 26 08:07:37 2022 +0100

    Finish describing the front matter in the schema

commit a8d5055c48ae5d7798332f451830bc2749856b54
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jun 26 08:02:52 2022 +0100

    Consolidate the field for 'last updated'

commit 636b78f0ac6767601a2407c01c6f7d6be799270a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jun 26 08:00:44 2022 +0100

    Remove a bunch of unwanted front-matter fields

commit 0e024d40435c7955520636f0ff741aa3fd510652
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Jun 25 23:28:50 2022 +0100

    Continue removing unused keys and tidying up front matter

commit ed4073e53143d7caf4741dbe9bfc01db56260859
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Jun 25 23:09:36 2022 +0100

    Remove a now-unused `archive_variant` front matter key

commit 8f519da6fbc5e1ee9773bb5cbd089ac57b8f6228
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Jun 25 23:03:07 2022 +0100

    Remove the now-unused `date_added` field

commit 342f60bda3577b39e2f941725b0ce70164c9166e
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Jun 25 23:02:29 2022 +0100

    Move the two posts about boiler clocks to /posts/

    Although these posts get a fair amount of traffic, there's nothing else
    in the /notes/ path and they're not worth special-casing.

    This also moves the `date_added` field to `date`, because currently that
    info isn't surfaced anywhere.

commit b3cc37d63a5ee1f97fac6274172256f976c8275d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Jun 25 22:55:41 2022 +0100

    Remove another post from the index as not of long-term value

commit 60fce603e65dc6613be4d16e4456b2c47962ad05
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Jun 25 22:55:29 2022 +0100

    Remove the 'slug' variable from the YAML front matter

    This is set by default as a Jekyll variable, and I'm not setting i to
    an interesting value in these examples.

    See https://jekyllrb.com/docs/permalinks/#placeholders

commit c24c1a1f17787822eef3bf2548d381213780316e
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Jun 25 22:52:24 2022 +0100

    Check in the initial front matter

commit 1e57b0d42c88c164267a13f9f89b6592500ab9ae
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Jun 25 22:51:50 2022 +0100

    Remove some now-unused front matter fields

commit 43a281c5f520173b67e6e598ba9820464bb7422d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Jun 25 22:51:32 2022 +0100

    Add a plugin for linting using a JSON schema

commit b97a03f684a76cb6e59213083a0ac8b46aa28da7
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Jun 25 20:24:03 2022 +0100

    Mount the linting plugin in the right place in the container

commit b1cbafeaffbfbf55a0b072b1065849bb8329be7e
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Jun 25 20:20:39 2022 +0100

    Add the JSON-schema gem to the Docker image

commit 25a63fd052a61dfa65986ce1d7ed1bb1b397d586
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Jun 20 06:47:10 2022 +0100

    better tint colour for this card

commit 300f1fdf254b22bcbeb6e7a62cf0a0871087fcc7
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Jun 20 06:45:34 2022 +0100

    weed another post from the index

commit f378b4e9bc673d9b0ac8c3042f847f1f00c47cc5
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Jun 20 06:44:05 2022 +0100

    link to all posts by default

commit c273022ac035a5dc15c5fba8bddab1a3b90450b3
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Jun 20 06:42:21 2022 +0100

    continue fiddling with cards to make the index shorter

commit 5124af04d83fed27d3fd4ed9a0ea7410d4b8bc62
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Jun 20 06:42:02 2022 +0100

    add the card assets

commit 2223ba408c32fa5b268985c5abdee46265b82e94
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Jun 9 08:01:37 2022 +0100

    fix the card type

commit ac13c5e455c1d7c7df1748c59eb0e217e97b96c2
Author: GitHub Actions on behalf of Alex Chan <githubactions@alexwlchan.net>
Date:   Thu Jun 9 06:40:49 2022 +0000

    Publish new post forgotten-secrets.md

commit d7c6a30b8f31203a38b96d3e9a95e42bb3cd52b8
Merge: e906ac2d 4633f006
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Jun 9 07:38:58 2022 +0100

    Merge pull request #509 from alexwlchan/jq-and-secrets

    Post: "Experimenting with jq as a tool for filtering JSON"

commit 4633f006e7176ab11cbf7f8813988ebf813aae2d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Jun 9 07:37:02 2022 +0100

    Improve the title of the jq post

commit 5f85e806ee0ada401ec66749cceff00ccbe07942
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Jun 9 07:36:52 2022 +0100

    Add an image used in the secrets post

commit cd67be16e1cfa81ccf3359df899ee9af440d3293
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Jun 9 07:36:47 2022 +0100

    Add print styles for code

commit bd1a8874f368aa33e6b2a6c679820ebc2c6dd26e
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Jun 9 07:34:35 2022 +0100

    Add some cards

commit 9d7a1404d5e1f2d8af6374b1511b4eeb0a0375d3
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Jun 9 07:26:45 2022 +0100

    Markups on my post about jq and Secrets Manager

commit 585df6f76eb4c484c1ae15c32cefd6caad9057bd
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Jun 8 21:55:21 2022 +0100

    Add a post about jq and secrets

commit e906ac2d07ef0b27c86b48347ba48aee9ac62154
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Jun 7 21:04:42 2022 +0100

    Add another card; tidy the index more

commit a5277e4e48c526ba0f5f29397d5391586268cbb9
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Jun 7 19:32:08 2022 +0100

    add two more cards

commit 0ef3819fd95da09be57e1f02e0e61fc6de6d36fe
Merge: e5174f95 5ff89017
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Jun 6 11:54:06 2022 +0100

    Merge pull request #506 from alexwlchan/all-posts-have-cards

    Use cards throughout the "all posts" page

commit 5ff890172c86dd8070cab8fa539ef858ca1f4953
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Jun 6 11:49:57 2022 +0100

    continue shrinking cards slightly

commit 57de0846e88b6f63705c6d9c403d167031f2ea8f
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Jun 6 11:28:42 2022 +0100

    reduce some card sizes

commit 916304584138664c5fa216d5c4611d97400c64a2
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Jun 6 11:23:02 2022 +0100

    Continue backfilling cards

commit 154289e5a68522a96b5a5bf1b243a0b324819195
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Jun 6 09:07:14 2022 +0100

    more backlog pruning

commit a5d77cb9b52312b38fe460b40ef817ed3516f748
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Jun 6 08:30:43 2022 +0100

    continue fiddling with cards

commit b9141989bdd4e60a06e17de6bf6e7ff26997735b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jun 5 21:57:15 2022 +0100

    continue fiddling with cards and the archive

commit 229cb05a7d6a53177d5aca5a84ba82f70e3b9976
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jun 5 20:51:56 2022 +0100

    keep tidying the index and the cards

commit 1ae811cc641dd972c04abf8e90c741c723fdf300
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jun 5 19:59:30 2022 +0100

    more fiddling with cards

commit 638165fba4a101212def080e6eea1020c17f5a08
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jun 5 19:29:16 2022 +0100

    Continue backfilling the post cards

commit a55844ca74c81a6c72d3193550d4f9e962105566
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jun 5 18:14:02 2022 +0100

    Get some more cards sorted

commit 2debee1aa30c0fe1bb525721b02f0edf8c7ee7e1
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jun 5 17:48:20 2022 +0100

    tweak what gets linked from the homepage

commit bcd86c1a2e20f4286e768c957ef37835ce5c8cea
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jun 5 17:42:14 2022 +0100

    Continue adding cards to posts

commit fa262989fbd5734150ec830245e36006ef74d9ed
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jun 5 17:23:40 2022 +0100

    Continue backfilling cards on old posts

commit a5b56c9639d08209a87c00dfb76284feb27667c8
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jun 5 14:29:00 2022 +0100

    tweak the 2022 cards

commit 96baba20545a8c852b993858c91dd9b8e4457a45
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jun 5 14:18:44 2022 +0100

    Make cards for all my 2022 posts

commit 5f4838e0d8d0653faa878b68dcb26968fa504084
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jun 5 13:36:48 2022 +0100

    Keep fiddling with article cards for 2022

commit e5a456c8facb3db30ae10966e208ac0f55e34bbd
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jun 5 12:27:35 2022 +0100

    keep playing with colours and themes

commit 34303bf66511486a5a82f3a153bb2d60223ebe8a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jun 5 12:22:45 2022 +0100

    Start rendering the 'all posts' page as cards

commit e5174f95ccaef4470d7684a172980fbfd7a61abf
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jun 5 13:03:52 2022 +0100

    Don't link to a now-defunct stylesheet

commit f372ea96be1e3181aa922ad67de5ea1b66105330
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jun 5 13:01:05 2022 +0100

    move post cards into the main css file

commit 817c3f29987bb0dcaa48cf8737a1f929c88aeaf8
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jun 5 10:44:18 2022 +0100

    Add the styles for inline SVG

commit bc9cc28e011f36efefb62c7a677b63a74b4cc0db
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jun 5 12:46:37 2022 +0100

    Add a query param for cache busting

commit f4a958349f05f4269911965f691ad9e9a3c6044e
Merge: 2bcdf79f 46405148
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jun 5 12:23:42 2022 +0100

    Merge pull request #503 from alexwlchan/inline-svg

    Inline SVGs on post cards

commit 464051481ffdac507f9ac1af36b8e1858fa5c77b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jun 5 10:42:00 2022 +0100

    Inline SVGs on post cards

    This reduces the number of round trips required to load an archive page

commit 2bcdf79fa4ed0405cf052a239adc858dd0200242
Author: GitHub Actions on behalf of Alex Chan <githubactions@alexwlchan.net>
Date:   Fri Jun 3 12:29:47 2022 +0000

    Publish new post new-archive.md

commit 0914539d386c5dba013c123a1ebc22e37a1b284c
Merge: 36528730 62acaa79
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jun 3 13:28:13 2022 +0100

    Merge pull request #502 from alexwlchan/about-the-new-archive

    Post: "Redesigning my archive pages"

commit 62acaa7951b1807c50091e82359a48aff747521e
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jun 3 13:26:01 2022 +0100

    Add the card image for the new archive post

commit 0b522b65e665a58c923eb65e3a7a35bbc43358d0
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jun 3 13:19:35 2022 +0100

    put a pretty card on the best of page too

commit 055cd0df4421b85804761b1d0e5765c7995978bc
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jun 3 13:18:23 2022 +0100

    one final tweak

commit 663b92d8e7e01ec4ad2633086accf428a85e86d5
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jun 3 13:14:41 2022 +0100

    keep tweaking

commit 38f3eb00bab04a52e56b17a399cec3aee3e06139
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jun 3 13:06:57 2022 +0100

    Continue fiddling with the new archive post

commit eee2d4b8fbe33763eae60388d2df4cb87c7cf819
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jun 3 13:00:27 2022 +0100

    continue tweaking this post

commit 13ec0287f694f2917c9b2f53a42d6ecc6202e009
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jun 3 12:27:17 2022 +0100

    final markups on the post about my new archive

commit df0b2bfbabdd99987900c6bf2842e61d5a90f211
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jun 3 11:53:39 2022 +0100

    Only define the globe image in the strokes card once

    From 111KB ~> 29KB.

commit bd5441001affb9ea993bdaa310df6f8c58b3a40a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jun 3 11:46:24 2022 +0100

    fix the card for the svg clip/mask post

commit 423c1c66b7992f91da75fb2db140b2249abcc27a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jun 3 11:00:14 2022 +0100

    Make a list of Noun Project icons

commit 47a3071b55682740a032850f3e22245c86597549
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jun 3 10:47:41 2022 +0100

    Mention the cards on the "about the site" page

commit 37a164ecaa48a4578465e1469042035038757a81
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jun 3 10:37:39 2022 +0100

    Add a first draft of the "about the new archive" page

commit f1a5dab93c13829a0c10141e3590e232c671af58
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jun 3 09:18:22 2022 +0100

    add curvy corners to the projects page

commit 2bb065f4e7502dca727b38ba8b761856cdecac72
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jun 3 09:18:12 2022 +0100

    first draft of my new archive pages

commit e57ea6e21d00d5848024930d76e15ba4cb0d1520
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jun 3 07:52:27 2022 +0100

    Tweak the homepage wording

commit a106ec9a18f77cadff8f30d8fa006310b092126c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jun 3 07:51:59 2022 +0100

    Move some one-off CSS into the post itself

commit 2425a7ed501ed4a7af0cc823a96d86fb8bf92122
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jun 3 07:37:06 2022 +0100

    Add <meta description> to the all/best of post pages

commit 365287302fe9303e036845e584507275abe4b55f
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jun 3 13:25:34 2022 +0100

    more license shenanigans

    [skip ci]

commit 563c963b39dadbf7b6d470c6fc989d22be3910db
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jun 3 09:01:50 2022 +0100

    monetary

commit 017b516656333554137788bb325330db083ae5c0
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jun 3 09:01:32 2022 +0100

    'reach out' blech

commit 60c691f063ee184095ab1941e2de820543d86d1d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jun 3 09:01:13 2022 +0100

    pepper some ko-fi links around

commit 1f992eeee5941017776c056ec2d879dd8021d8bc
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jun 3 08:53:20 2022 +0100

    Link to the Noun Project from the 'about' page

commit 6b2117562344d6f264e771045f61a47c9d1a9870
Merge: 83fce04a 52516f89
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jun 3 01:08:34 2022 +0100

    Merge pull request #501 from alexwlchan/fix-auto-merge

    Use a personal token so GitHub builds automerge commits

commit 52516f89c2c0cd3b14fe4e6166af97a04b9618d7
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jun 3 01:06:47 2022 +0100

    Use a personal token so GitHub builds automerge commits

commit 83fce04a2f98ff751ae24ab4ec4fb8062720e8c2
Merge: 85a34de4 65daca27
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jun 3 01:02:50 2022 +0100

    Merge pull request #500 from alexwlchan/alexwlchan-patch-1

    Update README.md

commit 65daca279a0a9b37ac6ae0411d564b257bd4a3f8
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jun 3 01:02:42 2022 +0100

    Update README.md

commit 85a34de4700f2da11d694ee9b48b5d2a7443ec08
Merge: e30f8836 6366ea87
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Thu Jun 2 23:51:26 2022 +0000

    Merge pull request #499 from alexwlchan/blog-backlog

    Redesign the "best of" page with cards

commit 6366ea87a0c2fab0ddec77eb89c526e8d7d41753
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jun 3 00:48:42 2022 +0100

    optimise a few cards

commit 48b02378c5701c5fd7174f34c35edf0ea46e9fd6
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jun 3 00:41:36 2022 +0100

    add cards to the homepage

commit a8b2ddc95a1ef5a410d2baa1137dcf6875a94759
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jun 3 00:21:12 2022 +0100

    more card improvements, fix lints

commit 8cb6fadfb7fb4dbb5a2983dd8ebe86839809ed0d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jun 3 00:15:06 2022 +0100

    continue twiddling with posts

commit 3b9eba51067d6f1630c92f1ca742c7369cefaa70
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jun 3 00:12:19 2022 +0100

    finish adding cards

commit 02041e207dcff94f1b12788ca977b9cdeb836150
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Jun 2 23:51:17 2022 +0100

    Add a bunch more cards

commit e30f8836a5cfd17f8b1836d165b4f5f6671d2b12
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Jun 2 23:42:30 2022 +0100

    transparent backgrounds here

commit d69f00af4c02698270eddeee9536b55cb42b054b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Jun 2 12:49:03 2022 +0100

    Continue fiddling with cards

commit b87e16bb6148181f20fab1710c412d49560e3ee9
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Jun 2 09:34:31 2022 +0100

    continue to fiddle with card information

commit b121e590e4452f302f2f4318b505e9ccd6e1d63f
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Jun 2 07:25:24 2022 +0100

    Start to flesh out the cards page

commit 0275d36511ff1ae792e5e5648585cba133df123c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Jun 1 17:39:01 2022 +0100

    Start fleshing out the /posts/ page

commit 69ac064984ca519ee4fa1e80d56f8af58102b2eb
Merge: f4d743ed cd35c4af
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Sun May 29 08:29:13 2022 +0000

    Merge pull request #498 from alexwlchan/more-elsewhere

    Add a script for saving elsewhere writing; add storage articles

commit cd35c4af69a9459345adbe4edb5eba9270630b49
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun May 29 09:27:17 2022 +0100

    Add a script for saving elsewhere writing; add storage articles

commit f4d743ede264cb4fbdb95cb3267dc5cd7215f536
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed May 25 21:04:42 2022 +0100

    remove the test post

commit 93134fee4f2a34309f9169021cdd3a3739e77d41
Author: GitHub Actions on behalf of Alex Chan <githubactions@alexwlchan.net>
Date:   Wed May 25 20:02:23 2022 +0000

    Publish new post this-is-a-test.md

commit b6bafb754be05f28c9d53b92d3d3a16c5bc89b33
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed May 25 21:00:44 2022 +0100

    add some more git config

commit fab1c51b73c71150737a2692b06f64ca44712c8a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed May 25 20:57:21 2022 +0100

    create the ~/.gitconfig file

commit 5b2c59be97f07b84a9e9d6b9fa52340e48d6962d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed May 25 20:54:14 2022 +0100

    test the auto-publishing

commit cae2fb28a1a12d5dbe26a05653dfc3524c60a436
Merge: 2fe2b19c 08e73cac
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Wed May 25 19:52:12 2022 +0000

    Merge pull request #497 from alexwlchan/explain-github-actions

    Continue fiddling with GitHub Actions and auto-merging

commit 08e73cac0b09ef6ad8d63424043021015760274b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed May 25 20:51:01 2022 +0100

    this should be a PUT, not a GET

commit 578eee46c35c41917118c64cd872ce57496a9596
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed May 25 20:49:00 2022 +0100

    is this the right syntax?

commit 67b23f4ccbc6aaedc101de48933c0798aaf2b40e
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed May 25 20:44:51 2022 +0100

    fix the bash comparison

commit 91394028c028f38c06c60002499ca96fdb289e0b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed May 25 20:43:37 2022 +0100

    try auto-merging myself again

commit 154c4fca82f4f104b726826e18fdfd45556cb682
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed May 25 20:32:10 2022 +0100

    use a prebuilt action

commit afdbfb0a18a0f8b0565270c2fade007a2720686a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed May 25 20:30:19 2022 +0100

    twiddle with auto-merging

commit 423912812f8ccf5c05542cc94ed437a406f8e1f8
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed May 25 20:25:14 2022 +0100

    run, not steps

commit a3f25dc199c7cf56a83c6956fd871486ced7cc78
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed May 25 20:24:45 2022 +0100

    fiddle with auto-merging logic

commit 69965ed4d8462b6658ebba340d8d0759bffe72b7
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed May 25 20:20:03 2022 +0100

    fix the syntax, maybe

commit 7ffc0afd1fd3d8637aefd51b75cb1bbec83fcba4
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed May 25 20:18:53 2022 +0100

    Try merging in the PR Action

commit 11cf931783cd735cd33da1a685200454ebcd7e16
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed May 25 20:15:38 2022 +0100

    Delete the old Azure Pipelines config

commit 01fcd507f4aeb7c89659e6c3b5c2c123b0c0ff4a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed May 25 20:11:12 2022 +0100

    Update the site notes to explain it's deployed by GitHub Actions

commit 2fe2b19cdeb243362b391554b65dc036d63c9f38
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed May 25 20:04:45 2022 +0100

    Pass the NETLIFY_AUTH_TOKEN variable

commit a04d0458ea35181d16a49dde7b71e89125e62e2f
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed May 25 18:18:38 2022 +0100

    restore the merge and cleanup action

commit 6f308d60a6e3ba6de4d6200eb9e7a9ef5607225c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed May 25 18:16:26 2022 +0100

    this should be a 'run' block

commit 2886ae2a3f47c3dd6e34793da9b56663278f748b
Merge: 693df723 22d17528
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed May 25 18:15:44 2022 +0100

    Merge pull request #495 from alexwlchan/github-actions-ci

    Do everything in a GitHub Action

commit 22d175280f46a0a3440925627bb34e0eb9b86f92
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed May 25 18:14:28 2022 +0100

    Do everything in a GitHub Action

commit 693df7238e6fde4634e655762dab3a30e8dbafa8
Merge: b8a87d06 a9aafae6
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Wed May 25 17:13:03 2022 +0000

    Merge pull request #494 from alexwlchan/github-actions-ci

    Add a GitHub Action to build the site

commit a9aafae6cb26839a0bc3a178ea578f0342b61677
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed May 25 18:09:54 2022 +0100

    Build the site and run linting

commit f0c64b7dc83014ade6fb9159c3ebdb68c9f352af
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed May 25 18:07:57 2022 +0100

    okay but actually build the site

commit bfde450b0f61341ba0d1435f643d9db9254292a6
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed May 25 18:07:28 2022 +0100

    Remove the unused GitHub Action for now

commit dfe2444c7fba61deff3f2613965316b8ff534ed2
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed May 25 18:06:55 2022 +0100

    Add a GitHub Action to build the site

commit b8a87d069f7354c773fb8adb834f4ac82c5d7038
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue May 24 10:22:21 2022 +0100

    Sort the source files for the CSS fingerprint

    For #493

commit 6fcc48adcb35ceb46b162eb4430bd716177ba29e
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue May 24 08:35:08 2022 +0100

    Add a Slack emoji for the Elizabeth line

commit c98025c06c5787a9658086d8e481e2179eb23e90
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.net>
Date:   Tue May 17 07:25:06 2022 +0000

    Publish new post carbon-monoxide.md

commit a589183758fbd7633fe749a192a075807aecfe2c
Merge: 0b9befc1 c36ad479
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Tue May 17 07:22:28 2022 +0000

    Merge pull request #492 from alexwlchan/carbon-monoxide

    Post: "Changing my carbon monoxide detectors"

commit c36ad479894569584fe450a978602175421d1afb
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue May 17 08:18:28 2022 +0100

    "nothing else"

commit bed199663c0050ba946e7e9de1cbcd293db58728
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue May 17 08:18:06 2022 +0100

    Add a quick post about carbon monoxide detectors

commit 0b9befc10954c5a53e9c109d24af052d355fcfcd
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon May 16 22:39:48 2022 +0100

    fix the busted video tags

commit 3f91143abca3573669d4a1d5adb7cafcc79c3399
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon May 16 22:31:04 2022 +0100

    Try closing my video tags

commit c58ec49952ce7b6fa344f39f3c184b8813edbe78
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue May 10 06:23:34 2022 +0100

    Update footer.html

commit c2553e80ba7000cc54b511ed79dfe35ac4df480a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon May 9 10:24:34 2022 +0100

    Update footer.html

commit 9eea04732f7bb058cc1e52bae9275633419826bd
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon May 9 10:24:07 2022 +0100

    Update footer.html

commit c12ba4ab8302db4081e8a015d50c8f1ade389deb
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.net>
Date:   Sat May 7 19:28:32 2022 +0000

    Publish new post dominant-web-colours.md

commit dc96ad720d680b6a958232b39255112c6a3e5ff7
Merge: da6ccee5 eee5725c
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Sat May 7 19:26:26 2022 +0000

    Merge pull request #491 from alexwlchan/webapp-dominant

    Add a post about dominant colours on the web

commit eee5725cbd2ab06a5a6f83a297f79a8efaa7eb45
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat May 7 20:23:02 2022 +0100

    Add a post about dominant colours on the web

commit da6ccee5c076d514797d2f596312a1c29083a33c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat May 7 10:39:17 2022 +0100

    Stick this screenshot into Netlify

commit 7198089381a21a8d6f1d881e4d68967d05b01459
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.net>
Date:   Thu May 5 14:01:57 2022 +0000

    Publish new post rust-on-glitch.md

commit 2138ab2b923010cf08beea82617b70fbe96c8e30
Merge: 8acb954e f1ce05b2
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Thu May 5 13:59:13 2022 +0000

    Merge pull request #489 from alexwlchan/rust-on-glitch

    Add a quick post about Rust on Glitch

commit f1ce05b2da0878720d631a153fdafb64f9b36a61
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu May 5 14:54:07 2022 +0100

    Add a quick post about Rust on Glitch

commit 8acb954ef28fc63b76eff4e25978412954987758
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun May 1 22:17:53 2022 +0100

    Update about-the-site.md

commit afd10f58ac8ac7147d4e650c98336d463910ad58
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun May 1 19:56:03 2022 +0100

    Make sure my "search tags" script always works

commit 26b1fd9f1400991f943ec9d17e726a3f98196128
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.net>
Date:   Mon Apr 25 21:10:40 2022 +0000

    Publish new post lorenz-wheels.md

commit 4d5984746a3b5346be11e870bc025a5dfe051f70
Merge: a3808d45 174e8942
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Mon Apr 25 21:08:36 2022 +0000

    Merge pull request #487 from alexwlchan/lorenz-wheels

    Post: "Illustrating the cipher wheels of a Lorenz machine"

commit 174e89428a20375e1d4e6cd46adbbb680a455c8d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Apr 25 22:05:06 2022 +0100

    tweak the aspect ratio of this image

commit a3808d45fcddecb1b0b8cac4f4937985f731c8d7
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Apr 25 22:00:36 2022 +0100

    Update projects.md

commit fdff91595232a47348e57f3aaf6a895b84d6958f
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Apr 25 21:55:41 2022 +0100

    these are cams, not pins

commit 0b364011ee398bd9d7619a32b79ef0a7234d8477
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Apr 25 21:55:23 2022 +0100

    Add a quick post about my Lorenz wheel code

commit c4d15a11a403d8c9620770eb5e0ea3dcab06e014
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Apr 25 20:50:03 2022 +0100

    Add a tool for searching tags

commit f70d9c04d660d80c5e6001c45f2a5f609ef10db0
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Apr 24 08:19:10 2022 +0100

    Convert my "publish Docker image" script to Ruby

commit 7272340f2b25563bb7eb75ffb7d0a53c72660826
Merge: f42668a1 d3c10d2d
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Sat Apr 23 23:35:44 2022 +0000

    Merge pull request #486 from alexwlchan/deterministic-email-obfuscation

    Make email obfuscation more deterministic

commit d3c10d2dd56b7fbcdcb61a8caa78265f94e47f5d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Apr 24 00:32:23 2022 +0100

    Make email obfuscation more deterministic

commit f42668a1ae3e8e79479f5db7bff6c2be58517eee
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Apr 24 00:18:51 2022 +0100

    Don't run these steps if previous steps failed

commit 4953e1ecd35845eaeb12d2cccc3f4be76caeefb5
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Apr 24 00:14:57 2022 +0100

    png, not jpg

commit 150a9a9788284d86042e1cec63b7c98c036745e8
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Apr 24 00:11:42 2022 +0100

    add the twitter card image

commit 3bd41841048943514167132f8bc1e476ce72dc17
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.net>
Date:   Sat Apr 23 23:03:47 2022 +0000

    Publish new post supposedly-simple-image-layout.md

commit a68d93540b0ba2603e54dfbabc5099814b0e9864
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Apr 24 00:00:39 2022 +0100

    Add some nice card metadata

commit 2d21ebf6e256b47b288108c6f9749339a4fc3950
Merge: d343509a 3078dfd0
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Sat Apr 23 23:00:37 2022 +0000

    Merge pull request #484 from alexwlchan/simple-layouts

    New post: "Creating a “simple” three-up image layout in CSS"

commit 3078dfd0b5785bcb70f298820d11a548f5b6e745
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Apr 23 23:56:33 2022 +0100

    final final markups

commit 55c32fa819b7196cdb35584d3595e276afa55ba3
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Apr 23 23:53:19 2022 +0100

    Final markups on "simple image layouts"

commit ca236ce92055818ca961bfd6bb142e2b0561a831
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Apr 23 22:01:10 2022 +0100

    More edits on "image layouts"

commit a8c9b80b23d18cc06b9a3b3b7bc6e498ac679d8b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Apr 22 13:47:30 2022 +0100

    more image layout stuff

commit 6cd5a5911bb66976ea8ce50a20db9f428da89028
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Apr 20 21:31:43 2022 +0100

    continue fiddling with CSS Grid layouts

commit dc8bf751f246f0905fbe0089a35d1a97e279d555
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Apr 19 20:15:56 2022 +0100

    Start writing a post about image layouts

commit d343509a0f981b54f4a2cea69789adc74f44a203
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Apr 20 21:01:55 2022 +0100

    Add the NASA images I'm using for CSS Grid examples

commit 3e9ed408c2bca11fc9227c60d737658b8ba9be46
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Apr 3 11:02:32 2022 +0100

    Update 2022-04-02-checking-with-curl.md

commit 1af864d621009c359c74d2f83a69cba0ad9bb6db
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.net>
Date:   Sat Apr 2 08:44:30 2022 +0000

    Publish new post checking-with-curl.md

commit 62d14fd513b228e0eecd33ba90e6c0e7c48cbe03
Merge: 0d019c8f 81bc1a6c
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Sat Apr 2 08:42:08 2022 +0000

    Merge pull request #482 from alexwlchan/blunt-url-checking-with-curl

    Add a quick post about checking lots of URLs with curl

commit 81bc1a6cb9540757e3dae5f718a5b88a69f3c46a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Apr 2 09:33:38 2022 +0100

    Add a quick post about checking lots of URLs with curl

commit 0d019c8f2c719f7e91b06108cc0674b7c8595e31
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Mar 24 08:36:39 2022 +0000

    Fix a typo (thanks Steve Summit!)

commit d38cf87f752bbe32bf8055e7bd17767af4e9e294
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Mar 11 07:47:26 2022 +0000

    Update about-the-site.md

commit 6d3f61284a596cc466560ed5d4d5be7e9933881a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Mar 11 07:47:10 2022 +0000

    Update README.md

commit 99566ed676df54480bad29a043a333a2a02cc115
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Mar 5 13:14:57 2022 +0000

    Update the comment about CSP headers

commit 5ddc9bb964a53b26a4360ae491d6da62fa28e34e
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Mar 5 13:14:33 2022 +0000

    Move the unsafe CSP headers to a single page

commit 36ea3ac969d60695af10d77a9ad725c482e59201
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Mar 5 09:48:33 2022 +0000

    Try to fix the Permission-Policy header

    Using the first example from https://www.w3.org/TR/permissions-policy-1/

commit 326735e82c7458ffd0469f8c00dc3b2efea3a12d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Mar 5 09:45:55 2022 +0000

    Split out HTML and script linting

    My shell scripts change very infrequently; putting them on the hot path
    of deploying the site is unnecessary.

commit 290227385c49592ac396bbb0eae44a5824c2a7c4
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Mar 5 09:42:00 2022 +0000

    Skip publishing drafts in Azure if there aren't any

commit 36f72ed7348e1436d7e6016ad65ed8ba2be89b5d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Mar 5 09:40:13 2022 +0000

    Update the name of the feature-policy header

commit d7f0658df6e911bb8005457ffc003eb916b7b7e2
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Mar 5 09:32:41 2022 +0000

    Add a note on where I test security headers

commit 7e0929985c83add6e76d428a22adc4022b25e0ac
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Mar 5 09:29:49 2022 +0000

    Remove an errant semicolon

commit ad71f79e2b556ee91361387f0d6ae6e950d3e850
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Mar 5 09:29:41 2022 +0000

    Add an explanation for long-lived caching headers

    [skip ci]

commit 3e79d1ffe2e20e4dab2a1e14333bb5252761ba39
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Mar 5 09:25:38 2022 +0000

    Add some HTTP security headers

    These are the headers I was setting on my old nginx server, which I need
    to reconfigure for Netlify.

commit 73e372e028a4cf3b8778639ec4c345dafe59ef26
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Mar 4 16:29:38 2022 +0000

    Hide my _files directory from GitHub language analysis

    See https://stackoverflow.com/q/19052834/1558022

commit 4209e0a6e0fea691b71a253cd26e03ce918af3f4
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Mar 1 23:25:35 2022 +0000

    Use the new link to the costs report

commit 2c42274740b193bab420e1237c7c2ae7dfa56735
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.net>
Date:   Mon Feb 28 10:23:15 2022 +0000

    Publish new post no-cause-for-alarm.md

commit 2a8187714d7f9762d0a2651914ef61f1671dbfb6
Merge: e75d9f88 0f91db83
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Mon Feb 28 10:21:03 2022 +0000

    Merge pull request #480 from alexwlchan/sqs-autoscaling

    New post: "Beware delays in SQS metric delivery"

commit 0f91db8301bac39d259fb524d5a457ed3077d0b1
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Feb 28 10:16:26 2022 +0000

    Add a good Twitter card

commit 5d8e98e9612206825afb22483d586832aa4ce6a9
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Feb 28 10:03:38 2022 +0000

    Markups on "no cause for alarm"

commit 9ac6bd4e408e090e2ee3c18f2ba7417f24e36682
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Feb 28 09:16:09 2022 +0000

    Remove some unused Makefile keys

commit 32118978ff8136b466bdd309b40d1a4c58b0c134
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Feb 27 01:58:28 2022 +0000

    First draft of the SQS scaling bug post

commit 9aa6710af8e1fa25b1e9a286f3a2889f1fdf4e11
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Feb 22 08:49:52 2022 +0000

    Start adding an SQS autoscaling diagram

commit e75d9f889fc34cda7fe7e831f96416d0f6b0c41c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Feb 19 13:16:22 2022 +0000

    Fix the proxy URL

commit 7666096f1636ba8c4c0dd712e1e80bdb6ec53b33
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Feb 19 13:10:50 2022 +0000

    Add a proxy to the inclusive events site

commit 642e7292b23f72a1ee925d9dd13ee2b64aadb73d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Feb 19 12:46:41 2022 +0000

    remember to rebuild after we publish drafts

commit 65df6371eed1a19842f39c04ed3317090b8367b1
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.net>
Date:   Sat Feb 19 12:45:20 2022 +0000

    Publish new post two-twitter-cards.md

commit 9ae527cf7af43a40dfbf824e1f1fcc4fcb7c05f1
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Feb 19 12:44:03 2022 +0000

    continue fiddling with directories

commit c3e89084eb563b1e2d416b5796b02d11b145828c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Feb 19 12:40:48 2022 +0000

    try rejigging some more

commit 73ffee6b5645c5362815b651b37eea2c4e25b2ff
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Feb 19 12:40:02 2022 +0000

    close up those newlines

commit 4c5ced17ef5309e6c406189471721715eeb2efa0
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Feb 19 12:38:28 2022 +0000

    Set up Git config before we deploy to Netlify

commit 6dc559337435497f7546c1f91836656eb17a6cef
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Feb 19 12:34:13 2022 +0000

    What if I just use the downloaded path directly?

commit e8d901c0431b289eb61e41d9db7cd8c479fb4e6e
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Feb 19 12:31:37 2022 +0000

    what's already in ~/.ssh?

commit 053e91e3d082b1166e891b25902fb40515d81ca6
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Feb 19 12:29:37 2022 +0000

    try to debug pushing to github

commit c00d833c2613fd5933ecf2e1bf1da5c36f1e34a0
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Feb 19 09:19:33 2022 +0000

    Remember to publish drafts!

commit 1fa50b1820ef7c7830d2609eeea900d3c7cde8a8
Merge: 964901ad bc191a9a
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Fri Feb 18 18:00:38 2022 +0000

    Merge pull request #479 from alexwlchan/two-twitter-cards

    New post: "A tale of two Twitter cards"

commit bc191a9af2cdec39349e608d08a3e47b26538a0f
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Feb 18 17:53:33 2022 +0000

    More writing about Twitter cards

commit 273e244e0ce190e8c2bac7be3a20d54c5179aba7
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Feb 18 17:13:09 2022 +0000

    Add a post about Twitter cards

commit 58eb3976aaa0823054d2bb97fc0d65889dea8a5c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Feb 17 22:51:45 2022 +0000

    First draft of my "two Twitter cards" post

commit 964901ad35f601d1a5bdd358a8a2a73a9ce0e339
Merge: 27cd5dbb 5a5f1a90
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Fri Feb 18 14:04:10 2022 +0000

    Merge pull request #478 from alexwlchan/fix-twitter-cards

    Add linting that checks for 2:1 aspect ratio on Twitter cards

commit 5a5f1a90269fdf1536c8c1f609bda79583677dd3
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Feb 18 13:40:21 2022 +0000

    Fix all the remaining Twitter cards

commit c5e21e7057618e42c4a1adca64b0b3cd4af7d6f2
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Feb 17 23:06:17 2022 +0000

    Improve the error reporting on bad Twitter cards

commit e18889ae2c8e72c8193a312472a4e3b6ec4d5434
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Feb 17 22:51:45 2022 +0000

    Add linting that checks for 2:1 aspect ratio on Twitter cards

commit 27cd5dbb50501fb8dcfda5e3fe15b7148085d8fc
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Feb 18 12:47:32 2022 +0000

    s/mediocre/basic

commit 2c803627066390ade36995aaa5e42016ef4665ca
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Feb 17 21:33:20 2022 +0000

    Update the "about the site" page to talk about Netlify

commit 99f4edbce9af01863fcd8e814ff292ad93f50a0c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Feb 17 20:20:48 2022 +0000

    I don't actually care about staging builds

commit 3d05d1235fc7c306660ef36cd5ebd70d1be8b9a1
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Feb 17 20:13:41 2022 +0000

    fix the azure pipelines syntax

commit 3a261ce0e802d7a624d814c4d13c05a66355d05b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Feb 17 20:09:24 2022 +0000

    try doing a shallow clone

commit 2578bcd5cb4350df4d33e31484621bd7dd22654e
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Feb 17 20:09:08 2022 +0000

    don't do a stage deploy on main

commit 338e6cadc43c6ac2e1715868f43fcb76501818ac
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Feb 17 20:03:41 2022 +0000

    Add Netlify-based redirects

commit 6264b2c2d8d1069fd634374d9eb2e881f683154a
Merge: c6248b12 6c1579cb
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Thu Feb 17 18:28:21 2022 +0000

    Merge pull request #477 from alexwlchan/keep-twiddling

    Another attempt at exposing the Netlify token

commit 6c1579cbc2a1976cf103be123cbd9952a6f7acb8
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Feb 17 18:23:43 2022 +0000

    helps if I use the right env var

commit 039f03d7063d83785f33f13d4d468e80962db44f
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Feb 17 18:19:31 2022 +0000

    Another attempt at exposing the Netlify token

commit c6248b12340dcc5301905b0fafb435c2670fcecb
Merge: 25cdc619 da24b903
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Thu Feb 17 18:17:06 2022 +0000

    Merge pull request #476 from alexwlchan/netlify

    Can we make this work with Netlify?

commit da24b90328174124699b8c17f4b2462cb6beea76
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Feb 17 18:07:26 2022 +0000

    surely this doesn't make a difference

commit 635b433564633e6070859583072bb129fb1abf79
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Feb 17 18:00:44 2022 +0000

    this should only run on live

commit 9f70d31be152d8a702939f69b16185b49b5d18c0
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Feb 17 17:55:11 2022 +0000

    fiddle with env vars in Make

commit 54c531bb80fb0f1035f83e9cedf40b3e8d70094b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Feb 17 17:49:53 2022 +0000

    We don't need a second build

commit fc77818a203966619890d675eadb6c79e5ea49b4
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Feb 17 17:45:15 2022 +0000

    Can we make this work with Netlify?

commit 25cdc619f68eb4b9e6ae96b4706b866b35afa770
Merge: 4118c19b 9f68172d
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Thu Feb 17 13:25:59 2022 +0000

    Merge pull request #475 from alexwlchan/check-twitter-card-images

    Add a lint that my Twitter/OpenGraph cards point at real images

commit 9f68172d678a10e6763c8145c2fa3a4ca9decc59
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Feb 17 13:22:20 2022 +0000

    Fix OpenGraph card linting

commit df6ceaeef9cb860627f2d9c888789075bc578a5e
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Feb 17 13:12:08 2022 +0000

    Add a lint that my Twitter/OpenGraph cards point at real images

commit 4118c19b14b561fafc6a7df434dd659b4436c59f
Merge: fa669c87 aee37642
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Wed Feb 16 22:23:34 2022 +0000

    Merge pull request #474 from alexwlchan/new-profile-photo

    Time for a new profile photo

commit aee3764262e2824e8cd4e115334f1793e2c08828
Author: Alex Chan <a.chan@wellcome.org>
Date:   Wed Feb 16 22:19:56 2022 +0000

    Time for a new profile photo

commit fa669c87c3c4186ee894b85056621a82160db3d4
Merge: df906555 0215a01b
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Wed Feb 16 20:19:01 2022 +0000

    Merge pull request #473 from alexwlchan/bin-sitemap

    Remove jekyll-sitemap, which I don't actually want

commit 0215a01b0ea4c6f4301a9556e0d30d250b94873f
Author: Alex Chan <a.chan@wellcome.org>
Date:   Wed Feb 16 20:13:08 2022 +0000

    Remove jekyll-sitemap, which I don't actually want

commit df90655546cdaa3c63389b1e4f8bfd521da15189
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Feb 15 22:22:45 2022 +0000

    remove a robots.txt file that I'm not using

commit 46858a898081b469e56158bda73b67b70d23b2a4
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.net>
Date:   Tue Feb 15 20:54:35 2022 +0000

    Publish new post safari-tabs.md

commit 0e9efeff23efce0500b15044f51cc942f12af7e1
Merge: b1408faf f40be0a0
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Tue Feb 15 20:52:31 2022 +0000

    Merge pull request #472 from alexwlchan/safari-tabs-jxa

    New post: "Closing lots of Safari tabs with JXA"

commit f40be0a0580d0e391db685c1bbb7fa13a9504251
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Feb 15 20:48:58 2022 +0000

    fix a couple of plugins

commit 294f35573c81884f033faac78cdba291078441bd
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Feb 15 20:43:53 2022 +0000

    fix var name

commit 9035d2da5db26867a9a8014cda67ff9ee5317844
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Feb 15 20:43:06 2022 +0000

    markups on the JXA post

commit dc177ae2876d6eb5f55b5ef01f7965473ebd9361
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Feb 15 20:30:20 2022 +0000

    Initial post about closing Safari tabs

commit b1408faff223e4a08f0737e941f5bf557c95f400
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Feb 13 11:49:53 2022 +0000

    Add a substitution for Route 53

commit 4f25763e8f2ced2b180d051240da242c9bbbdf5c
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.net>
Date:   Sat Feb 12 17:27:21 2022 +0000

    Publish new post route53.md

commit 92fd1dc6ebc9e65e612d4ab5cac3ad7a48646922
Merge: bf859976 6f7137e7
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Sat Feb 12 17:25:08 2022 +0000

    Merge pull request #471 from alexwlchan/route53

    Add a quick post about Route 53 naming

commit 6f7137e727517a71b729b3d118f08e3072890201
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Feb 12 17:21:56 2022 +0000

    Add a quick post about Route 53 naming

commit bf859976c9f5b4e0d6e24ae997ff5716c07096e2
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Jan 29 11:02:01 2022 +0000

    Fix a few bits

commit e27f6717b29948898079427f6f2359a5e5a4b099
Merge: ad83ce68 55181a43
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Sat Jan 29 10:55:32 2022 +0000

    Merge pull request #469 from alexwlchan/speed-up-jekyll

    Try to make the Jekyll build go a bit faster

commit 55181a43243293a7fda0cdb29d5bc227fbbd8695
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Jan 29 10:52:10 2022 +0000

    Inline a few config values

commit 8ee7b1779def9a57b86cd22511054e8ab8e97130
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Jan 29 10:49:14 2022 +0000

    Inline a Nokogiri 'require' so we only load it when needed

commit 5953342cd4ef4f00b715abbc4f3e2fd5282fd60b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Jan 29 10:45:06 2022 +0000

    Also cache the cleanup_text filter

commit b39b04334028e74e3e654dd6ea60089cee3ab732
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Jan 29 10:42:07 2022 +0000

    Cache calls to the smartify() filter

commit 126d5d1ac228e97f21e151e393d8d8c4ad878a03
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Jan 29 10:15:54 2022 +0000

    Remove a trailing newline

commit 32c9ca73c014566df4b5742e5ef408a26e7ca9a4
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Jan 29 10:14:47 2022 +0000

    Remove all the code around <!-- summary -->

    This is a feature from a very different design of the site, and I don't
    need it, so let's get rid of it.

commit 821d2bbff7745cf27fb05ccabc6560e68e1dea8d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Jan 29 10:09:38 2022 +0000

    Inline the 'post_content.html' include in 'post.html'

    It's the only place where it's used.

commit ad83ce682376339374daf435e9763601a80b2f39
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.net>
Date:   Fri Jan 14 10:58:15 2022 +0000

    Publish new post animated-artichokes.md

commit 811ce6706ec362fc59a9c121adb423e1fd85ec3d
Merge: 46bf8652 77568e43
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Fri Jan 14 10:56:16 2022 +0000

    Merge pull request #468 from alexwlchan/animated-artichoke

    Add a post about animated GIFs and artichokes

commit 77568e431f53df8657430a23192ca785940b601d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jan 14 10:52:34 2022 +0000

    get an internal ref that works

commit afb0cf69ac9d92a24a8f3df136178b7f21b67095
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jan 14 10:36:41 2022 +0000

    Add some missing alt text

commit df8cd8cf21c523bed0c78b9b52473d2d0946e7d0
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jan 14 10:30:20 2022 +0000

    Improve the conclusion

commit 0c7d5c038e55cafed76396badc1145d319ba9357
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jan 14 10:28:18 2022 +0000

    Add a bit more to the artichoke post

commit 23794ff15c8d67985f62fb5482d917a90a596333
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jan 14 10:22:33 2022 +0000

    First draft of the artichoke post

commit 46bf8652a11c2e147c3544c00503753b9a287a48
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Jan 12 08:24:52 2022 +0000

    Update 2021-06-08-s3-deprecates-bittorrent.md

commit afa315d5539f519d3a58a31ca8fb4f1a1844a92b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jan 7 09:20:34 2022 +0000

    Update 2022-01-07-rusty-shelves.md

commit e101abf30a2b9a159e8e3e5797797025aec3f39b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jan 7 09:10:22 2022 +0000

    Remember to lint before publishing!

commit 6e07c1736d6b45c0760ca1829c641d46c84e2bc0
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jan 7 09:05:59 2022 +0000

    Publish new post rusty-shelves.md

commit 44a4703412444a91ed06e7defbfdef8e8f6a6e95
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jan 7 09:05:46 2022 +0000

    Final markups on my rusty shelves post

commit 7fc588903da3bb95e30342e4a40d33990a72eea3
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jan 7 08:08:26 2022 +0000

    Markups on the "rusty shelves" post

commit b3eb49680b529a2d6bf50f22772ea8613bf3d8fe
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Jan 5 23:12:34 2022 +0000

    Add a complete first draft of my bookshelves post

commit 5fb067e4f7cfe8196a705dec555ba3ef8c5ba9f7
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Jan 4 22:27:13 2022 +0000

    Add the first draft of the Rusty shelves post

commit 33a5810e1e2d4ca4cf7882004335112335dabdd0
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Jan 4 08:18:43 2022 +0000

    remove the indentation

commit a5800ba87d9d8640f9e4a85f70b2db72f7cb06be
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Jan 4 08:17:34 2022 +0000

    Point to the concurrently repo in the concurrent.futures post

commit 30e4684bc20fcf0dadd661d6e881d50a6ed661bf
Merge: 6a038aab 65987dd3
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Fri Dec 31 20:50:33 2021 +0000

    Merge pull request #467 from alexwlchan/bumped-html-proofer

    Bump the version of HTML-Proofer

commit 65987dd3ddc897058be8c538a621ca884d7c3dc5
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Dec 31 20:47:21 2021 +0000

    Fix the mount point for the custom commands

commit 07d7506c63c6e0b219ac4448b048733739fde8c6
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Dec 31 20:41:48 2021 +0000

    Fix the email address in the deploy script

commit 50b4eb8885e2b20ad08e6e2052988d3897d50c32
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Dec 31 20:41:37 2021 +0000

    Bump the version of HTML-Proofer and other gems

commit 2989cdef343e1f0cfc3e6e8a46ae4e68b73c7f2f
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Dec 31 20:35:12 2021 +0000

    Remove a now-completed TODO comment

commit 6a038aabc206cee4a7ea3bcd072d0fea57f423e2
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Dec 31 12:21:46 2021 +0000

    clarify that this is reading order

commit c0b64e1c81579fd5e6d4eec757964d4a2bf2f486
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Dec 31 12:19:46 2021 +0000

    remember to centre book images on phone screens

commit 5f2dd0bf7b1fba7a8ff0f1dbb5af5ae08449ff87
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.fastmail.co.uk>
Date:   Fri Dec 31 11:52:34 2021 +0000

    Publish new post 2021-in-reading.md

commit 21a06e314fcccc5095d058625d45e4289ea2a19d
Merge: b1fae61e 5df2fd95
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Fri Dec 31 11:50:31 2021 +0000

    Merge pull request #465 from alexwlchan/2021-books

    Add a list of my favourite books from 2021

commit 5df2fd95a2db60df0babc4eb87bf84102698efa4
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Dec 31 11:46:34 2021 +0000

    final markups on "2021 in reading"

commit d252910eb6b9af0b57ab8dee5620208edfbd03c6
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Dec 31 09:18:51 2021 +0000

    Add the missing alt text

commit 3e249d89dff352b8a6a63bca613a62cd1c8f1931
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Dec 31 09:12:04 2021 +0000

    continue editing my "in reading" post

commit 4b1bc190b50345b7e3891261c679ecb69ccf3952
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Dec 31 00:05:47 2021 +0000

    First draft of my 2021 books post

commit b1fae61eb079111765f1f43deb5380c229721508
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.fastmail.co.uk>
Date:   Fri Dec 24 09:09:39 2021 +0000

    Publish new post os-sep.md

commit 9d68ecca2bddffa0ff119ca1eac99a1f9ea4a737
Merge: a96a5088 78a263a5
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Fri Dec 24 09:07:39 2021 +0000

    Merge pull request #463 from alexwlchan/os.sep

    Add a quick post about os.sep

commit 78a263a56d6babdbae769ac710dbe0f34e2bf0d5
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Dec 24 09:03:51 2021 +0000

    Add a quick post about os.sep

commit a96a5088c36b5ad0fd7fffba58828adedb3dd3ab
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.fastmail.co.uk>
Date:   Fri Dec 10 21:36:56 2021 +0000

    Publish new post rust-errors.md

commit 0ec6e18de87bc07d06c941daa183dfc40b75fb36
Merge: a9dc21e2 39c5ee26
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Fri Dec 10 21:34:52 2021 +0000

    Merge pull request #462 from alexwlchan/rust-errors

    Add a quick post about Rust's error output

commit 39c5ee266b418e1307f695ce809eb33f96fc2903
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Dec 10 21:30:58 2021 +0000

    Add a quick post about Rust's error output

commit a9dc21e229be154cbd2c36ba648d45b1434aee58
Merge: b23f922d 834d8945
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Fri Dec 10 09:59:13 2021 +0000

    Merge pull request #461 from alexwlchan/css-fingerprint

    Fix the CSS cache busting

commit 834d8945c981a4433fe235f403ef88a204f35a1a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Dec 10 09:55:19 2021 +0000

    Fix the CSS cache busting

    It turns out iOS 15 ignores query parameters that aren't a key/value pair,
    so my cache-busting isn't actually working.  This switches to a k/v pair
    and embeds the MD5 fingerprint in the URL, so it should only bust the
    cache when the CSS actually changes.

commit b23f922dfba30aecb7c36d48515e5a7a94099a1e
Merge: f0ca447d 774be585
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Fri Dec 10 09:02:12 2021 +0000

    Merge pull request #460 from alexwlchan/new-styles

    Add some styles for modern Apple browsers

commit 774be585340c251287bd80c0b6fa01c43583dbeb
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Dec 10 08:58:07 2021 +0000

    Extend into the notch area when in landscape on iPhones

commit dc0487bcbd64383cab5b9a94a896d8a0f9521a06
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Dec 7 23:13:52 2021 +0000

    Add the theme-color meta tag for Safari 15

commit f0ca447da3c6c0ee97dbb307e1f5985a070a0244
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Dec 2 22:30:58 2021 +0000

    /s/different/difference

commit bad4367789ca69d0333d924a6aceea0cff438820
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.fastmail.co.uk>
Date:   Wed Dec 1 14:33:14 2021 +0000

    Publish new post slashes.md

commit 1b102ac0a736cf24dfc5f8b9123753d9926d902d
Merge: ea10e575 0b16a78b
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Wed Dec 1 14:30:40 2021 +0000

    Merge pull request #459 from alexwlchan/slashes

    Add a post about slashes in path separators

commit 0b16a78b86084433a08053e00a0c4826658e2612
Author: Alex Chan <a.chan@wellcome.org>
Date:   Wed Dec 1 14:25:19 2021 +0000

    Markups on my path separator post

commit e9a5504b9bae1e2b764f7dcbf887678a51dfbbdb
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Dec 1 09:07:33 2021 +0000

    Add a post about slashes in path separators

commit ea10e57501f69abd15c07830f2c36a76eb48e186
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Dec 1 11:47:00 2021 +0000

    Fix find/replace error: scripture ~> scroll

    https://twitter.com/shamblepop/status/1466010357051404294

commit 80495a64de905a0541b0248f4bad55d8d37b79e3
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.fastmail.co.uk>
Date:   Tue Nov 30 09:30:01 2021 +0000

    Publish new post dominant-colours.md

commit 36d7a66898bab2b70d591fcdb52c6abb6f52aa86
Merge: 34b0375c b32a29d6
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Tue Nov 30 09:27:50 2021 +0000

    Merge pull request #458 from alexwlchan/dominant-colours

    Add a post about dominant_colours

commit b32a29d65829adce0c0c11247a2481e6e87deaea
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Nov 30 09:24:03 2021 +0000

    Link to dominant_colours from my projects page

commit ee3419523a666dc16947ae71372b1b7493f06982
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Nov 30 09:22:07 2021 +0000

    finish copy-editing my dominant colours post

commit c864e5c11d854b2d76d46e2182b7014d20e5945d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Nov 30 09:12:08 2021 +0000

    Continue tidying the dominant-colours post

commit d39461ffe40936eda0b9ce4a6cf93cd15ff1e3b6
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Nov 30 07:48:00 2021 +0000

    Add some more benchmark data

commit 546062d1f3507ade1816cc9b1172d967a959bcb2
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Nov 28 22:27:09 2021 +0000

    Add an initial draft of my "dominant colours" post

commit 34b0375c19090cdfc03d3815e53177cbf63e517f
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Nov 20 22:11:35 2021 +0000

    Add <marquee> rocket to my projects page

commit 0d1ebece84c82b3aba04af9a13cda29ba2522ec6
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Nov 12 14:17:12 2021 +0000

    Update 3-context-from-commits.md

commit 0bd79f4f09f4f25f6d6dcfbfe37c3446fdca072f
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Oct 28 16:34:29 2021 +0100

    Update 2019-10-06-rough-edges-of-filecmp.md

commit 4420b0eecc98264c9c8395a6f2e9b701f5fa1476
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Oct 23 14:16:46 2021 +0100

    Add a missing apostrophe

commit 7b18f7f52b5b5e9ec93d3b54fc2dec9c68204cbe
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.fastmail.co.uk>
Date:   Tue Oct 19 19:11:46 2021 +0000

    Publish new post original-photos-filename.md

commit b336f7dbc2d0db95e1a521be8f9ec14e0fd0927c
Merge: b79c155e be2bab27
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Tue Oct 19 19:09:43 2021 +0000

    Merge pull request #457 from alexwlchan/finding-original-photos

    Add a quick post about Photos

commit be2bab2781c06c71c659f2bc3f280071b37006a6
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Oct 19 19:56:05 2021 +0100

    Add a quick post about Photos

commit b79c155e36249d97d1690cf1990092007fc00862
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.fastmail.co.uk>
Date:   Sat Oct 16 16:40:17 2021 +0000

    Publish new post oboe-of-optozorax.md

commit bc3ffd31b2937556037a1cf4917bc7a787875211
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Oct 16 17:38:14 2021 +0100

    Add a link to the AO3 version

commit dab0618d605df3b910610dbfd199c7af15790bd0
Merge: f84d3cfe 5ce5e99b
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Sat Oct 16 16:37:19 2021 +0000

    Merge pull request #456 from alexwlchan/oboe

    Add my "Oboe of Optozorax" fiction notes

commit 5ce5e99bb09ddb1e045d7eff841da599db189631
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Oct 16 17:33:17 2021 +0100

    Add my "Oboe of Optozorax" fiction notes

commit f84d3cfeb6d6825a70cf1c5c4e44e8085827fbc1
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.fastmail.co.uk>
Date:   Thu Oct 14 18:09:09 2021 +0000

    Publish new post console-copying.md

commit 0d8239708970b979b26388af54dcbc911d9eddb6
Merge: 0cc0c890 3fd3f297
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Oct 14 19:06:38 2021 +0100

    Merge pull request #455 from alexwlchan/accidental-copying

    Add a quick post about copying the prompt character

commit 3fd3f29700cb919f9b1254b4b34b962a019a6115
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Oct 14 19:01:28 2021 +0100

    Add a quick post about copying the prompt character

commit 0cc0c8904b22054bff95dbc1736c1ff46ee09a30
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.fastmail.co.uk>
Date:   Wed Oct 6 21:39:30 2021 +0000

    Publish new post readmes-for-open-science.md

commit 689df7bba2e90ac24ce6529ccdcf7ad9a8055101
Merge: b76f3264 30d78c25
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Oct 6 22:37:26 2021 +0100

    Merge pull request #453 from alexwlchan/readmes-for-open-science

    :pen: READMES for Open Science

commit 30d78c25153080f07037f22fc5c7212b2005aff5
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Oct 6 22:34:43 2021 +0100

    lowercase the 'f'

commit 59034dfd9f38de870de4084e39676bbe647838e1
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Oct 6 22:31:26 2021 +0100

    fix the link to the slides

commit 2011ddda354af4d2368c15fbab290a19cf1cee01
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Oct 6 22:28:10 2021 +0100

    sort out the banners

commit 6fa775cc15e0c3d6485701bf359a93e6adac0c46
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Oct 6 22:23:42 2021 +0100

    Tidy up tagging and notes a bit

commit 77979af9e50b6af9555449e72c9bd18f698c4c77
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Oct 6 22:23:34 2021 +0100

    Add some very quick notes on OLS + READMEs

commit d0620b36b8e1f2c1bbf28160b3f0e24465faf110
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Oct 6 17:22:59 2021 +0100

    Add the first post about READMEs for Open Science

commit b76f3264faf1999973c38cff41d690fd811dcbc8
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.fastmail.co.uk>
Date:   Mon Oct 4 14:48:37 2021 +0000

    Publish new post redacting-pdfs.md

commit 16966a4954e0e421d56624f60880e894589a15d8
Merge: cf59422c 7f7ac30e
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Mon Oct 4 14:46:27 2021 +0000

    Merge pull request #452 from alexwlchan/redaction

    :pen: Beware of incomplete PDF redactions

commit 7f7ac30e8cf458e9cc7052e5692ce662117be252
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Oct 4 14:57:58 2021 +0100

    Add a cover image and some alt text

commit 3aae45530aeb85f2fa55a3db2c81462baf2e45d9
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Oct 4 14:57:48 2021 +0100

    Keep tweaking the redacted PDFs stuff

commit ba543985326a440477d91966e56094aa8df9c3b2
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Oct 4 08:44:12 2021 +0100

    More stuff on PDF redactions

commit 758e2f4a5fff99aef88879db6aa06a8762e82448
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Oct 4 07:28:12 2021 +0100

    Initial draft of "Beware the incomplete PDF redaction"

commit cf59422c8b6b07e5688f33ddc6ae36034959f718
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Oct 1 16:29:19 2021 +0100

    don't say "technical jargon"

commit e25c9d0239e9152094624ef75c3effcbfb2ad545
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.fastmail.co.uk>
Date:   Fri Oct 1 15:18:28 2021 +0000

    Publish new post how-do-you-work-with-non-engineers.md

commit 493dcd3e6db3c9f64a6e422028ff8437ed32f9a6
Merge: 4d89accc 1a02831c
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Fri Oct 1 15:16:04 2021 +0000

    Merge pull request #451 from alexwlchan/work-with-non-engineers

    :pen: How do you work with non-engineers?

commit 1a02831c496971e3f7452cdb56aaf04c9e072324
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Oct 1 16:07:53 2021 +0100

    finish editing "how do you work with non-engineers"

commit 80eae2bae9773f8280e9654a979b392346f8c05d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Oct 1 12:30:07 2021 +0100

    continue tweaking the "non-engineers" post

commit 4f3e9a80e6d0edb343d966c014c75619b940d466
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Oct 1 12:26:55 2021 +0100

    More edits on the "non-engineers" post

commit 3688b226a92dcfcee1c7a0915d79b488dc08ef30
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Oct 1 07:53:23 2021 +0100

    Add a draft of "How do you work with non-engineers?"

commit 4d89accc52620242bca53522da1a4a38d78185c9
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Sep 29 23:02:28 2021 +0100

    Clarify why some of these S3 keys are forbidden

commit 040c2467baa5a01093fb84fc9daab1ba7fe2e19b
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.fastmail.co.uk>
Date:   Wed Sep 29 20:23:05 2021 +0000

    Publish new post septembrse.md

commit 17c24fb9ac3fc17d485a68699b46dc8e72c63b72
Merge: 2b894887 7788b3ba
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Wed Sep 29 20:20:54 2021 +0000

    Merge pull request #450 from alexwlchan/septembrse

    Add some very rough notes from SeptembRSE

commit 7788b3ba0f41281a5b91e29907b463dc2a49b412
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Sep 29 21:16:59 2021 +0100

    add a note to my list of talks

commit 4c93cbfbcca536d198b2d3aaf0bb2b5c52906072
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Sep 29 21:15:12 2021 +0100

    Add some quick notes on SeptembRSE

commit 2b894887ecbdd4763fbd30a5525f40502c3f2e5a
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.fastmail.co.uk>
Date:   Tue Sep 28 19:23:40 2021 +0000

    Publish new post editing-toolbar.md

commit 8d83fc8eee48f0f8b19c714cb7702308e5b36f81
Merge: 1fde1bba 0d1dd0ae
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Tue Sep 28 19:21:25 2021 +0000

    Merge pull request #449 from alexwlchan/bookmarklet

    Add a quick post about my editing toolbar

commit 0d1dd0ae92be6e93db6d6fe7226782e121fb1567
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Sep 28 20:17:30 2021 +0100

    Add a quick post about my editing toolbar

commit 1fde1bba93ceb4f6cc65859a51e8134daab2c445
Merge: 36636668 44255abd
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Sun Sep 26 09:03:30 2021 +0000

    Merge pull request #447 from alexwlchan/favicons

    Get 32x32 favicons on pages that use the default theme colour

commit 44255abd81209c666a6363c332d46b6553f59d42
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Sep 26 09:59:20 2021 +0100

    Get a 32x32 favicon for pages using the default theme

commit af0c95e4f5231e037ee935c5f6caa6542a834ea2
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Sep 26 09:40:52 2021 +0100

    start getting a new favicon pipeline working

commit 8057e8428e0e8553a8581f91676003080200c008
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Sep 26 09:22:27 2021 +0100

    Add the old favicon assets

commit 366366689eb578cc95d34a14b9fcff185a759d9e
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.fastmail.co.uk>
Date:   Sat Sep 25 15:41:45 2021 +0000

    Publish new post cloud-costs-report.md

commit 62411d5ade8581b7872c59892691133c8046f5d9
Merge: fd8a027f eed5dd95
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Sat Sep 25 15:39:26 2021 +0000

    Merge pull request #444 from alexwlchan/costs-report

    Add a post about our cloud costs report

commit eed5dd95b89a94bf17ccd6ab1ee3f18c3652cee3
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Sep 25 16:35:44 2021 +0100

    put the report in the card

commit d8320dd7adf4432b71072b55746c507facc70f61
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Sep 25 16:34:15 2021 +0100

    and one more tweak

commit dfce8abade316a1fba36d77c119383c1e972ad1d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Sep 25 16:33:12 2021 +0100

    a few copy edits on the costs report post

commit ad060a6fc3ce3c1c47fce7edf2fa661a476ad2d1
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Sep 25 14:51:28 2021 +0100

    Add a tag for AWS billing stuff

commit 9e1d31eda257a792db98c6d4c55be32fce2df633
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Sep 25 14:51:19 2021 +0100

    Add a first draft of the "costs report" post

commit 03d486c3ed4c9f4367ed592467685ffa9d0d4a92
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Sep 25 14:51:07 2021 +0100

    Move the "create post" script to the scripts folder

commit fd8a027f0235d9ca9d6b1c836a6e44ec86caa3e9
Merge: 8bb6be81 199c8d35
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Sat Sep 25 08:02:24 2021 +0000

    Merge pull request #443 from alexwlchan/fix-html-proofer-failures

    Fix more issues flagged by HTML-Proofer

commit 199c8d35c3e743a203a9bd056dd7a4c3a8b77613
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Sep 25 08:58:23 2021 +0100

    Fix a few issues with invalid HTML when compressing

commit 34917094769f8dd49f5dff384992e50e00fc1e05
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Sep 24 23:48:27 2021 +0100

    add opengraph checking

commit c69840624e41d56f2c4ada55f4a7b26ef955c181
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Sep 24 23:46:28 2021 +0100

    fix all the HTML linting issues flagged by html-proofer

commit b046b61cb3366ba1fd66ddeddffac5d23e7654a2
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Sep 24 23:44:04 2021 +0100

    escape a few more attributes

commit 85a79956ec65c3717c9f86d07744e4b3e34fcc87
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Sep 24 23:43:57 2021 +0100

    Remove some <xml> declarations from inline SVGs

commit 67ddc1e3ea183373bd9bd7e238f7b92c6099f758
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Sep 24 23:36:12 2021 +0100

    Remember to escape HTML attributes

    This avoids cases where double quotes end up in the attribute value and
    render the entire attribute unmanageable.

commit 35b4c1ffd7e6752fb1a86dd564098a2e16895f24
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Sep 24 23:35:50 2021 +0100

    Enable validation of HTML in html-proofer

commit 8bb6be817124631326ac9cf8ee9b28a5d10ee02a
Merge: 9909b00d 2e4ae47e
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Fri Sep 24 22:27:02 2021 +0000

    Merge pull request #442 from alexwlchan/bin-minipost

    remove the notion of a "minipost"

commit 2e4ae47e45d97d1f7edd55eb0da170ea94d9233b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Sep 24 23:23:36 2021 +0100

    remove the notion of a "minipost"

commit 9909b00da142e252148d4aa79fd1047dd076db8a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Sep 24 23:17:57 2021 +0100

    tweak the line height of <h2>

commit aace4778e9bec877a8d9793dc89544204673892c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Sep 24 20:17:58 2021 +0100

    put the source-path in the page instead

commit 502b26bb68addbb4d03e4893f8387ebb157b2ab7
Merge: 897048b7 a06bf894
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Fri Sep 24 19:13:45 2021 +0000

    Merge pull request #441 from alexwlchan/css-tidying

    Rearrange some CSS: reduce the size by ~1.5%

commit a06bf894ebe387a342d040c1aaa49f08624725a4
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Sep 24 20:10:07 2021 +0100

    Rearrange some CSS: reduce the size by ~1.5%

commit 897048b7fa73b981b1368888e6065c31da35a686
Merge: c3434cfc cfd51d4e
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Fri Sep 24 18:57:21 2021 +0000

    Merge pull request #440 from alexwlchan/switch-to-rszr

    Switch to the rszr gem for creating thumbnails of Twitter avatars

commit c3434cfcb6869913f5332d57edc3e76ea4e0794f
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Sep 24 19:53:25 2021 +0100

    Fix the path to this script

commit cfd51d4e15c29c890abb386ded346986da5dd185
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Sep 24 19:51:15 2021 +0100

    Switch to the rszr gem for creating thumbnails of Twitter avatars

    This reduces the size of the base Docker image by about 25% -- from 400MB
    to 298MB.  Wow!

commit 796c4ccdd61417abccc787f8a43f2529e28a80fd
Merge: 626a6523 5c16bd97
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Fri Sep 24 18:31:13 2021 +0000

    Merge pull request #439 from alexwlchan/build-tidies

    Toss a whole bunch of stuff from the main Docker image

commit 5c16bd97c85aa7c2958372a784672a510a1f4583
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Sep 24 19:27:40 2021 +0100

    remove an errant --volume from this 'docker run' command

commit c038d02a55df10016e85a0264cfedf1ffc46a1c8
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Sep 24 19:23:31 2021 +0100

    fix the name of this method

commit 656c621adb70c96829cc7211848bef68293db00e
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Sep 24 19:19:49 2021 +0100

    Fix the path used by certain gems

commit 8b41e4213e9adc5ecf40b4e42e70dcddd8edbd4e
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Sep 24 19:17:12 2021 +0100

    Remove an unused "require"

commit 8f1c9097027398be5b1b5ed2a38eb79709761253
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Sep 24 19:10:08 2021 +0100

    Bump the version of the Docker image

commit bd064f0066a1c52c3870c4f9153948cdc7cb09a3
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Sep 24 19:05:40 2021 +0100

    This is already installed by install_jekyll.sh, don't reinstall it

commit 167ee8573f4875bfa6f9d5e845d0aa60f24dbb5a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Sep 24 19:05:15 2021 +0100

    Remove some now-redundant .gitignore entries

commit ff2cef6b2261249e7cbd2ccc83cf83448dcdb7af
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Sep 24 19:05:06 2021 +0100

    Move all of the Twitter stuff out of the main Docker image

    This should reduce the size of the Docker image and means I don't have
    credentials in plaintext lying around on my disk.

commit 07eb0e37c08f592081c65eb5cebaa389c80ddc9a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Sep 24 18:38:20 2021 +0100

    Move the creation of Specktre banners into a separate process

commit e3b329589fa55c5194b462b11d66a102d26f0f53
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Sep 24 18:37:57 2021 +0100

    Move the "archive_elsewhere" into the 'scripts' folder

commit 79bcc6d3389a8cde69c3565084dafcbac89bb86e
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Sep 24 18:13:09 2021 +0100

    Put the deploy script in the scripts folder; add script linting

commit eb1883d8f1008696c8af284e091a4d57428b67e3
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Sep 24 18:10:24 2021 +0100

    Move the "publish Docker image" script into the scripts directory

commit 3f279e098acf7d3312fb76de9927eb3dbf78cfb4
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Sep 24 18:07:29 2021 +0100

    Remove a couple of gems I don't think I'm using

commit adcb3aea87c6626a4be87e2ad05fa6e4b1f3f41e
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Sep 24 18:06:55 2021 +0100

    Move the install scripts into the "scripts" folder

commit 626a652355cf7884cfeb84b15d88a1481ccec9c9
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Sep 24 08:44:02 2021 +0100

    put the word "ligature" in the post

commit 2b3bd2d437ecb891a1474df08309be5837fd120c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Sep 23 15:11:27 2021 +0100

    Use a meta tag for the link to the page source

commit 2dc035a385a99c126c844b09842ebe6444e210b9
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Sep 22 10:06:18 2021 +0100

    Update 2021-09-22-non-commuting-strings.md

commit e5d2204a7486dd4bbd194a2e2ff9b6dd13ec9b47
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.fastmail.co.uk>
Date:   Wed Sep 22 07:56:05 2021 +0000

    Publish new post non-commuting-strings.md

commit 0318c33b5df104064dd06e891ce7e27490830252
Merge: 647017c4 e7692abf
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Wed Sep 22 07:53:16 2021 +0000

    Merge pull request #438 from alexwlchan/non-commuting-strings

    Add a post about non-commuting string operations

commit e7692abfbb57ca831f5ed1fcedc734e0d2867b86
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Sep 22 08:46:38 2021 +0100

    copy edits on "non commuting strings"

commit 6b02b88228546e22a02cddcc71acc417b20eea6c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Sep 22 08:37:37 2021 +0100

    Add a quick post about non-commuting string operations

commit 647017c4fc0f9ff8a93d28957a6bdc392510cf93
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.fastmail.co.uk>
Date:   Tue Sep 21 21:50:31 2021 +0000

    Publish new post safari-15-favicons.md

commit 5c7441fd6a681303d9ed5e4d015e5590195cf607
Merge: e406b8f1 6c7c9d8b
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Tue Sep 21 21:48:07 2021 +0000

    Merge pull request #437 from alexwlchan/safari-15-favicons

    Add a quick post about Safari 15 favicons

commit 6c7c9d8b97abf1051e9048b65219bdc116045091
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Sep 21 22:40:50 2021 +0100

    Add a quick post about Safari 15 favicons

commit e406b8f1e2fe27bf6cf38633a35140cb0dca8462
Merge: 4683926d be6c6923
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Sun Sep 19 21:49:54 2021 +0000

    Merge pull request #436 from alexwlchan/add-canonical-url

    Make /all-posts/ the canonical page for the post archive

commit be6c6923eebe31b232ad3895624c36865f18436b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Sep 19 22:46:16 2021 +0100

    Make /all-posts/ the canonical page for the post archive

    While searching in DuckDuckGo, I noticed that it's indexed the per-month
    and per-year archive pages, which are really specific views of the overall
    archive page.  They shouldn't be surfaced in search, only for people
    fiddling with URLs.

    This patch uses <link rel="canonical"> to redirect search engines to the
    overall archive page, and away from the per-month/per-year pages.

commit 4683926d0fcc133e830221afde5cc99ac8bfcc45
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.fastmail.co.uk>
Date:   Tue Sep 14 20:40:27 2021 +0000

    Publish new post debugging-eventbridge-cron.md

commit b5c473ce4214bece9ad7212f087b543c489ee77b
Merge: 0e394bb3 137f0294
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Tue Sep 14 20:37:45 2021 +0000

    Merge pull request #435 from alexwlchan/debugging-eventbridge-rules

    Add a quick post about a handy EventBridge feature

commit 137f0294ab4bff2dbe96a06d2981f56e3b59a9ea
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Sep 14 21:33:30 2021 +0100

    Add a quick post about a handy EventBridge feature

commit 0e394bb3613936d1ca9bc7a56a71651d66e5becd
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.fastmail.co.uk>
Date:   Mon Sep 6 05:49:10 2021 +0000

    Publish new post perfect-planks.md

commit 7dc2a8c28801b70d09a13958aa40171ee623dcf9
Merge: 2ec74faf 89238787
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Mon Sep 6 05:46:31 2021 +0000

    Merge pull request #434 from alexwlchan/perfect-planks

    Picking perfect planks with Python

commit 89238787997791c00f07cc7b381517530fcb3e3c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Sep 6 06:39:50 2021 +0100

    Copy-editing on the plank post

commit 7fa3b2a50584999d7cf368cb916c54065d7e0dc6
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Sep 5 22:25:07 2021 +0100

    Remove a paragraph break here

commit fe40cd7e736dd2995f54fbfa18736ebbda2906d1
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Sep 5 20:10:26 2021 +0100

    initial draft of a post about perfect planks

commit 2ec74faf47d56be963325f1dd132c1afaa02cb2e
Merge: 8006b7d9 66c6d6df
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Sun Sep 5 18:41:52 2021 +0000

    Merge pull request #433 from alexwlchan/better-twitter-icon

    Don't display an enormous Twitter icon when CSS is disabled

commit 66c6d6df0aaa3848883ce98d02a112d298602ff0
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Sep 5 19:36:43 2021 +0100

    Don't display an enormous Twitter icon when CSS is disabled

    If CSS is disabled, the SVG for the blue Twitter icon on tweets will render
    at full-width, because there are no width/height constraints.  This PR swaps
    out the inline data+svg image for one that's loaded from a file at render time
    (so it's a bit easier to edit), and adds width/height attributes so it
    stays small even when CSS is disabled.

commit 8006b7d95a1a1f61757f3e1568deb5162b2158f9
Merge: 68f400ec 4850de00
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Wed Sep 1 22:38:22 2021 +0000

    Merge pull request #432 from alexwlchan/remove-unused-plugins

    Remove a now-unused "random" plugin

commit 68f400ecdaa9348cdc77b3e5e3bd6a4643933e99
Merge: eb346a51 f22fb74f
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Wed Sep 1 22:34:20 2021 +0000

    Merge pull request #431 from alexwlchan/link-to-other-writing

    Link to writing that isn't for LWIA/Stacks

commit 4850de00b66840ee65bf812e7693fb621c7a9b86
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Sep 1 23:32:07 2021 +0100

    Remove a now-unused "random" plugin

commit f22fb74f9019fe8b3d7d92b24abd41696b27a2f6
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Sep 1 23:30:02 2021 +0100

    Remove a block of commented-out code

commit 341bd19e36a4d39c4299ca02adb767627c89f4c5
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Sep 1 23:28:04 2021 +0100

    Include my Hypothesis article in the list of writing

commit eb346a517b703332edcf11a1704a1359822574cd
Merge: c0e1532a 8e9c1046
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Mon Aug 30 12:15:40 2021 +0000

    Merge pull request #430 from alexwlchan/archive-elsewhere

    Ensure I'm archiving all my "elsewhere" articles; add a lint check for that

commit 8e9c10461d56b595806861cb980242561f528407
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Aug 30 13:10:08 2021 +0100

    Add a few notes on how I archive my work

commit 50b1bdf2c81c036890a0c3ec1b91712040ff6bfc
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Aug 30 13:01:31 2021 +0100

    archive all the existing paths

commit f12a4ceff202ed7517700c35f027058b88c2cc90
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Aug 30 13:01:02 2021 +0100

    check writing has been archived when linting

commit 37597736df79bc0b4d3d18b783ca5caa38047192
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Aug 30 12:49:14 2021 +0100

    keep fiddling with archive elsewhere

commit 4f4cc8042a583127f08d160f586aa1c9bcdb2c16
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Aug 30 12:29:16 2021 +0100

    Add the initial "elsewhere" script

commit c0e1532add5699ea8c8ff4b3a197ff0176892b06
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Aug 30 12:01:00 2021 +0100

    Spruce up the README

commit 97f6bbd167bc13d72a4361092c6dd2f77848cca5
Merge: 303f359b ee0c6f52
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Sun Aug 29 12:58:11 2021 +0000

    Merge pull request #428 from alexwlchan/add-elsewhere

    Add a list of projects and things I've done

commit ee0c6f52921175a8ac1d926132315a7fd8e6f173
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Aug 29 13:54:37 2021 +0100

    remove a merge conflict

commit 7916a8baf5d6c1353926d304353ba972bf43989e
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Aug 29 13:53:08 2021 +0100

    get enough of the front page working for now

commit ac3afd0bf225877a0988b7bf31cfbfda3014e3f5
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Aug 29 13:48:15 2021 +0100

    that should be alt text, oops

commit fed37c9b6f713238a9658b28777a820721afd8b1
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Aug 29 13:47:41 2021 +0100

    actually check for image alt text

commit c89fe3bf254213809e145f2417b1f7b8d19611dd
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Aug 29 13:47:35 2021 +0100

    keep tweaking the projects + index pages

commit ed77f8b3dae5ffdd341351296250d42364858559
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Aug 29 08:23:45 2021 +0100

    Check in the CamPUG slides so the link checker is happy

commit a3afce6b33047dfc4b9701bec0f5a56dea254bee
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Aug 29 08:18:27 2021 +0100

    keep tweaking the project page

commit 948f5f6fa09e3ff6c677167fb30e121d7ad906a1
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Aug 24 21:10:46 2021 +0100

    keep fiddling with the project page

commit 79524b992251c3b25522a308ceeebeebcc7047a3
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Aug 22 23:18:16 2021 +0100

    add more stuff to the projects page

commit 4e7f4b741a4599346dd3dcf2708c56bd3999d478
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Aug 21 20:28:45 2021 +0100

    Add some images to the projects page

commit 2f262e7dad1c2609184f575e0684cc183ec630b1
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Aug 21 10:16:36 2021 +0100

    start fleshing out the project page

commit bd60963973060e8aa38324b490595b57df82ae75
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Aug 15 18:27:40 2021 +0100

    tweak headings and separators

commit 980d9395e8abe60d99efa0dd2d4abb085609a737
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Aug 8 11:08:47 2021 +0100

    sort out the per-year/month archives

commit 7aba8853c44bc3d5b52cf652d7e9dfa98b9412bc
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Aug 8 11:01:35 2021 +0100

    Make the "all posts" list more consistent

commit 6f6a22ddd0d846e826a9d1345857623ced7149ac
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Aug 8 10:54:22 2021 +0100

    only fiddle with the dot list in the talks archive

commit f3cb8a71e354dc6200d1173e0bcb74d639172ff9
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Aug 8 10:51:01 2021 +0100

    link to "elsewhere" in the header

commit 3331026369742ac1e36f6b30da3b8ca6d026cd79
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Aug 8 10:50:44 2021 +0100

    Add a proper page for my "elsewhere" stuff

commit 303f359bdc98326708fa6b6cbd07b749caeaaf74
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.fastmail.co.uk>
Date:   Sat Aug 28 17:43:17 2021 +0000

    Publish new post ignore-lots-of-folders-in-spotlight.md

commit af67e5c97ece3c157fe7323cdb96a049234cbf70
Merge: 1b007b88 457b445b
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Sat Aug 28 17:40:39 2021 +0000

    Merge pull request #427 from alexwlchan/ignore-lots-of-folders-in-spotlight

    How to ignore lots of folders in Spotlight

commit 457b445bd058ee2291c87d863a9ea0164f50792d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Aug 28 18:36:35 2021 +0100

    make the title more "me"

commit 4cb31cefcbf0b05f1b0abcb7a5c3bac92e15f3c5
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Aug 28 18:35:40 2021 +0100

    continue to tighten word

commit fec8e22963ca5e6b65bf7939a3d454ce3c118a19
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Aug 28 18:27:37 2021 +0100

    continuing to edit and tighten wording

commit aede3b1386dc906d330b667707774d146e581c38
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Aug 28 18:22:01 2021 +0100

    tweak the post a bit more

commit e181a346126247768a38d23475255ea5344d7559
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Aug 28 18:19:39 2021 +0100

    Add a script for ignoring lots of folders in Spotlight

commit 1b007b88da451db833cd99a0a8044014f9ec2bd8
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.fastmail.co.uk>
Date:   Wed Aug 25 16:13:24 2021 +0000

    Publish new post markdown-image-syntax.md

commit 65ce9105026132be36f8f1fff21ae4c34f5e2697
Merge: b5dbb18e ade73eff
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Wed Aug 25 16:11:01 2021 +0000

    Merge pull request #426 from alexwlchan/markdown-images

    Markdown’s gentle encouragement towards accessible images

commit ade73eff6fde4fd8e95c2048a8bf1dad5b65d912
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Aug 25 17:07:02 2021 +0100

    vrbs

commit 1cda75ed117a75b18d5ad5682ed313ebcd9a749e
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Aug 25 17:06:49 2021 +0100

    keep tweaking the conclusion

commit 2f0cff2e171bc0290b39d2ad560aaa29d2b5aaed
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Aug 25 17:04:27 2021 +0100

    finish the markdown p[ost

commit ec93de3957dcef643dd9124737f2f382fb9b82fb
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Aug 25 17:01:56 2021 +0100

    tweak a couple of print styles

commit 043821c3ec823aee325e6b657a62c85369a2c71c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Aug 25 16:56:12 2021 +0100

    Initial draft of a post about Markdown image syntax

commit b5dbb18e0d0a577622e3574c862c8ddb961ce05f
Merge: 8e40b309 63197da7
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Sun Aug 22 15:55:05 2021 +0000

    Merge pull request #425 from alexwlchan/tweak-say-thanks

    tidy up "say thanks", remove analytics

commit 63197da7b64cd8342cf6c1e3538007c3bf44fb6c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Aug 22 16:51:04 2021 +0100

    let's bin all the analytics

commit f64d8c531b5084d675d8374b3dac26bcd4a0027b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Aug 22 16:50:23 2021 +0100

    drastically trim back the say thanks page

commit 8e40b30981daf3269ec75550487a9e5e3029a906
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.fastmail.co.uk>
Date:   Sun Aug 22 07:40:24 2021 +0000

    Publish new post finding-misconfigured-or-dangling-cloudwatch-alarms.md

commit 6743c4a4c90637b4cd3e2aa19fbd107a322dc380
Merge: 0d1351ed 6c7743fd
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Sun Aug 22 07:37:35 2021 +0000

    Merge pull request #424 from alexwlchan/dangling-cloudwatch-alarms

    Add a quick post about dangling CloudWatch alarms

commit 6c7743fdf370df7adf70b40fbbcf5ca0de759816
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Aug 22 08:33:56 2021 +0100

    Run black over the CloudWatch Alarms script

commit 8b2767708bb5b7215bb5ec834d16f118d1b4d49b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Aug 22 08:33:13 2021 +0100

    Add a quick post about dangling CloudWatch alarms

commit 0d1351ed173d818546e1ec0867560031bee6b4a4
Merge: 1d134007 73339f52
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Sun Aug 15 18:59:32 2021 +0000

    Merge pull request #423 from alexwlchan/bin-image-plugin

    Replace the image plugin with a vanilla <img> tag

commit 73339f52c004e3856e51a8f5d91c02591a023bb4
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Aug 15 19:55:58 2021 +0100

    remove two scripts I no longer use

commit 14e66909fd2d93a76423167b73ca0275f26e2ef4
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Aug 15 19:52:16 2021 +0100

    Remove a reference to word-count.csv

commit efb7de0822b924585b15aeb033ed17b7f0001f8b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Aug 15 19:51:55 2021 +0100

    Replace the image plugin with a vanilla <img> tag

commit 1d1340071a9e2a1fdfd4f4f80cd69378871af6d5
Merge: 0bbf046d 102bbfd3
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Sun Aug 15 18:20:05 2021 +0000

    Merge pull request #422 from alexwlchan/keep-trimming

    Keep throwing stuff away that I don't need

commit 102bbfd30eb34968ba2bf8308a5738010593e543
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Aug 15 19:13:39 2021 +0100

    consolidate the footnote fixer into the text cleanups

commit ae96cde341d993daaa63add07b5df1cfbadc7fd9
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Aug 15 19:11:51 2021 +0100

    use the link styles mixin

commit ece442c3c42ad6116283c052dc2f915653e3df12
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Aug 15 19:11:46 2021 +0100

    remove the word counter, which nobody cares about

commit 0bbf046dd9735415ca1285b5e27973bd93a1bbff
Merge: 78892753 b9997310
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Sun Aug 15 18:04:10 2021 +0000

    Merge pull request #421 from alexwlchan/clean-up-css

    Clean up the CSS a bit

commit b99973100a6632690d6e885b671692f3b1319def
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Aug 15 19:00:31 2021 +0100

    remove the ko-fi brand colour

commit 5111c81e73a36ebf41209b59546f67d1f22ce4d9
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Aug 15 18:59:37 2021 +0100

    remove the special-case logic for content warnings

commit fb3cca9c56cca082acbfddea26101f96242afe4f
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Aug 15 18:55:56 2021 +0100

    this p.cite selector is never used

commit 5b00758828ac91eeec1ce821d2813343ef47fdcd
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Aug 15 18:54:21 2021 +0100

    remove this style; defer to .title

commit 30d954539a07201de4ad3edb3dc2496ad326e322
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Aug 15 18:50:47 2021 +0100

    I no longer link to Ko-fi in the footer

commit 43cf2fd826ce633db0e4b05367f5b26f1df131d2
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Aug 15 18:49:22 2021 +0100

    These pagination selectors aren't used any more

commit b4bd8ec537b790ed4c4d2c92bd4bf0fe71a92319
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Aug 15 18:46:11 2021 +0100

    Make <h2> bigger and more colourful

commit 2ba39650947a1adf851a452e15d11f66bb04a5fa
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Aug 15 18:46:05 2021 +0100

    Remove two unused templates

commit 34b54846401a7c8d0b7a422e0c507dadfb76cb01
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Aug 15 18:45:59 2021 +0100

    Consolidate on a single approach to separators

commit d7d246a213d4f2fdd8a4d950cfb2e54e02cd0c74
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Aug 15 18:32:11 2021 +0100

    All headings are normal weight now

commit 2448577c72190b3c190609328f7080b322df7c71
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Aug 15 18:25:32 2021 +0100

    Remove a now-unused CSS rule for .continue_reading

commit 78892753a10abfaaca5d25a06b086f5ab1ac0a54
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Aug 5 19:02:25 2021 +0100

    Remove an errant comma

commit 871312b548385a32dc4fd4e38463cdaceeaef691
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jul 16 23:52:57 2021 +0100

    fix the formatting of code in an old post

commit cf1c3fdae5b630179a5c6c67dfec019cb38aa6e3
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.fastmail.co.uk>
Date:   Fri Jul 9 06:27:58 2021 +0000

    Publish new post useful-github-searches.md

commit a169446a7076dc78f51c24f0439d09cf60e2aa20
Merge: 6c702035 1b6d7285
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Fri Jul 9 06:25:37 2021 +0000

    Merge pull request #420 from alexwlchan/github-searches

    Add a quick post about useful GitHub searches

commit 1b6d728505cf7fa5ac922f7f2519ee5a62660c3c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jul 9 07:15:39 2021 +0100

    Add a quick post about useful GitHub searches

commit 2e446420bf8783cae8f6132e2d031852176ca2bc
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jul 9 07:15:17 2021 +0100

    Make "listing deleted secrets" a best of

commit 6c7020354c0d2cbd9db3485c85ece576ff6287ab
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Jul 5 12:54:53 2021 +0100

    Update 2021-07-05-listing-deleted-secrets.md

commit e4845c733f491f96938dc7fd1f59add595831e29
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Jul 5 12:52:56 2021 +0100

    Update 2021-07-05-listing-deleted-secrets.md

commit 963456aec4db8373930486fad47858ceea9322c3
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.fastmail.co.uk>
Date:   Mon Jul 5 11:46:24 2021 +0000

    Publish new post listing-deleted-secrets.md

commit 16b04fdefc59c791787b92e6b0c83ac8600ddb9b
Merge: e5af22bb 318fcc12
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Mon Jul 5 11:43:12 2021 +0000

    Merge pull request #419 from alexwlchan/list-deleted-secrets

    Add a post about listing deleted secrets

commit 318fcc126ce4de046f1a8b13f356dd9fcc07370a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Jul 5 12:37:22 2021 +0100

    Final markups on the "list deleted secrets" post

commit 773d70fe98be529b6669657fc5d0219e5977e1ae
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Jul 5 11:40:48 2021 +0100

    Edits on the Secrets Manager post

commit 69dd333fbdb51ef6021da25755a073cf6d4cad6f
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jul 4 23:15:03 2021 +0100

    First draft of a post about Secrets Manager + deleted secrets

commit e5af22bb9e1566fc4ef22943c5dfe003e53e9c76
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.fastmail.co.uk>
Date:   Sun Jul 4 12:24:36 2021 +0000

    Publish new post a-wise-choice-of-test-strings.md

commit 57b2c2161960f271483dfbac746048e12e207781
Merge: 520e7122 d9c7410b
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Sun Jul 4 12:22:04 2021 +0000

    Merge pull request #418 from alexwlchan/wise-choice-of-test-strings

    Add a quick post about a wise choice of test strings

commit d9c7410b0440ec02a9c382c0efb79a4d69389543
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jul 4 13:14:31 2021 +0100

    Add a note about it starting on Twitter

commit 2d2c1df18ce6687fc08d6a366cdb2ea962d4041c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jul 4 13:12:16 2021 +0100

    Add a quick post about a wise choice of test strings

commit 520e712265c401ee5bec4d126c2dca33fe757e38
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Jun 8 10:35:40 2021 +0100

    Update 2021-06-08-s3-deprecates-bittorrent.md

commit 4c77402ef094b414e8f1a01cd359a12a8cf761af
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Jun 8 10:33:29 2021 +0100

    Update 2021-06-08-s3-deprecates-bittorrent.md

commit a56ad40feab4d146a043df0d320f626db3d26c8e
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Jun 8 10:29:32 2021 +0100

    tweak the title to clarify this is a feature, not a protocol

commit a950f21d5dc66d49a0ac158e21a0d8fc41438376
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.fastmail.co.uk>
Date:   Tue Jun 8 06:21:15 2021 +0000

    Publish new post s3-deprecates-bittorrent.md

commit ad2caa4164fb0a24f50126281551571f249014e0
Merge: 38cb4fd8 53671397
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Jun 8 07:19:01 2021 +0100

    Merge pull request #417 from alexwlchan/s3-deprecates-bittorrent

    Add a quick post about S3 deprecating BitTorrent

commit 536713973f196bb86c99ee7cfe4409fc4ff946d3
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Jun 8 07:15:59 2021 +0100

    Add a link to my tweet

commit 9a1a6af6c89de7b7a07c9edd3a286d80bc30297b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Jun 8 07:13:26 2021 +0100

    Add a quick post about S3 deprecating BitTorrent

commit 38cb4fd8614a342b2b03ee8afad977e320594d09
Merge: 13e9375c b29149c0
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Thu Jun 3 09:55:35 2021 +0000

    Merge pull request #416 from alexwlchan/migrate-to-ubuntu-latest

    Upgrade to a supported version of Ubuntu in Azure CI

commit b29149c0d62eee8728fd58082f45c38bd5947fa5
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Jun 3 10:49:51 2021 +0100

    Upgrade to a supported version of Ubuntu in Azure CI

commit 13e9375c4544cb523089e6eeed3094d2c4d44f33
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.fastmail.co.uk>
Date:   Thu Jun 3 09:46:46 2021 +0000

    Publish new post visualising-journal.md

commit f20c44c07fdd1a432e06b64e0db3cb78ba06cc57
Merge: aabd257a 39c3a1a8
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Thu Jun 3 09:44:06 2021 +0000

    Merge pull request #415 from alexwlchan/tracking-my-journal-progress

    Add a quick post about visualising my journal progress

commit 39c3a1a814b40b8255db69d4e732e38f9604151d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Jun 3 10:40:24 2021 +0100

    Ignore empty alt tags

commit e2574504ec98a9ba280858481d9ac1f078fc7f31
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Jun 3 09:53:13 2021 +0100

    Finish editing my journal post

commit 39d257c7426a24fde8432ebb065765a4297e8de4
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Jun 3 09:28:17 2021 +0100

    A couple of edits on the journal post

commit 546d6436e56dff8b34f62835c452bd9fa0d20cce
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Jun 3 09:24:01 2021 +0100

    Initial draft of a post about visualising my journal

commit aabd257a7aa005e73d30496b4daf0dacdf0863ce
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun May 2 10:36:19 2021 +0100

    Fix a typo; update the link styles on the demo button

commit 32a7b59f95b588364c3f1ced13b52cb92b5f3d28
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Apr 30 23:15:16 2021 +0100

    Don’t fail if there’s no href on the a tag

commit d3b9e9c07c47c49b9f8ce8d46e726cb51b72acbb
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Apr 30 23:10:14 2021 +0100

    Don’t jump around the page in the S3 progress bars demo

commit ef5228738d8eaa384caed102e9ae4071f8590a79
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.fastmail.co.uk>
Date:   Fri Apr 30 18:28:27 2021 +0000

    Publish new post s3-progress-bars.md

commit dc96139aafafe6fc1f5c9eccb98d6530a8355262
Merge: 711d473e 3237def5
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Fri Apr 30 18:25:44 2021 +0000

    Merge pull request #414 from alexwlchan/progress-bars

    Add a quick post about progress bars

commit 3237def5786c82e58387a8e7b1db0c638215ba91
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Apr 30 19:19:54 2021 +0100

    Make a quick tweak to the post

commit 111c7cc9da165122ad9c0ebe7f5dd954436638ad
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Apr 30 19:06:45 2021 +0100

    Initial draft of a blog post about S3 progress bars

commit 711d473e9264ccc65bc4dfd44ecef9c6cde08bdd
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.fastmail.co.uk>
Date:   Thu Apr 29 09:02:12 2021 +0000

    Publish new post coloured-squares.md

commit 1b31ad07fe4826f44a4321c8c0c727661804e457
Merge: 634a28d5 97ffcdf9
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Thu Apr 29 08:59:33 2021 +0000

    Merge pull request #413 from alexwlchan/print-coloured-squares

    Add a post about coloured text in the terminal

commit 97ffcdf99e6e4a4ff9e455aa5061430a9c3374f8
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Apr 29 09:55:18 2021 +0100

    Remove an empty image

commit f560bf2417719764b20ac39267073e5989b828a0
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Apr 29 09:54:33 2021 +0100

    A few quick markups on the coloured squares post

commit 4c50831e1b7a246275fec03e9f7e9461983df64d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Apr 29 08:58:53 2021 +0100

    Add an initial draft of a post about coloured squares

commit 634a28d5cc8e7019fac0df1c59b82cc05031b055
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.fastmail.co.uk>
Date:   Tue Apr 27 20:05:02 2021 +0000

    Publish new post unified-search.md

commit bedff651887194f2c703f51279aa3c95a779abd6
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Apr 27 21:01:47 2021 +0100

    "or fun"

commit e7fde83c3bf40006d0648208c182b5cd4bbf20da
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Apr 27 21:01:43 2021 +0100

    Link to my post about unified catalogue search

commit 9c796ade5ef0c979fce76eaad08498d72b2a7a2a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Apr 25 14:09:23 2021 +0100

    Use a more compelling example for bad tuple unpacking

commit 9736411ff76d7bbad763f257c7da2bbfab0427bb
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.fastmail.co.uk>
Date:   Sun Apr 18 12:35:58 2021 +0000

    Publish new post detect-private-browsing.md

commit 72d9e53fe0b4a73fe8319d1f1b087666b6b9da84
Merge: 7321952f 6f7e7575
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Sun Apr 18 12:33:29 2021 +0000

    Merge pull request #412 from alexwlchan/detect-private-browsing

    Add a quick post about detecting Private Browsing

commit 6f7e75758cf6df7e0f8658592dac95cac14a8530
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Apr 18 13:29:19 2021 +0100

    Quick markups on the private browsing post

commit 06ab1b486d74d73d24cf7f561961377d73363073
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Apr 18 11:59:33 2021 +0100

    Add the macOS tag to last year's post

commit ef1d74559c4ed3ad03bab80c3b0df2791b02041c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Apr 18 11:59:27 2021 +0100

    Add a post about opening Private Browsing tabs

commit 7321952f3ff283251367285e36979b15cae40838
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Apr 17 23:14:07 2021 +0100

    Don't remove all the whitespace in the RSS feed

    It breaks <code> blocks, among other things.

commit b24cbabc0b61b257cf4863c64b7634b9b255d17e
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.fastmail.co.uk>
Date:   Mon Apr 5 07:25:21 2021 +0000

    Publish new post secure-input.md

commit 5997c4928c936a58ce87177a0b4a0ca31b7191af
Merge: 2feb1939 1322ce70
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Mon Apr 5 07:22:37 2021 +0000

    Merge pull request #411 from alexwlchan/secure-input

    Add a post about Secure Input

commit 1322ce701235bb713dc0240401c0d9d0b05a0490
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Apr 5 08:18:24 2021 +0100

    A few more edits on Secure Input

commit a9f57480012524654b0bb39e5e9cda5ff5a5da58
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Apr 4 20:56:58 2021 +0100

    Tweak the draft of the Secure Input post

commit 5628806166bfcfbdbfdf6e8314da01e6e8833ba0
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Apr 4 20:37:07 2021 +0100

    Add a post about finding apps using Secure Input

commit 2feb193982f4832e74f0bc5959515164c174bd15
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Mar 21 07:37:39 2021 +0000

    Ensure the scissors are always rendered as text, not emoji

commit a9c7c191bd9a2d61fc05fe5ef8122e3551697ba1
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.fastmail.co.uk>
Date:   Fri Mar 12 14:04:59 2021 +0000

    Publish new post inner-outer-strokes-svg.md

commit fa81ce28807766e86dc0365686f5b695e21dd47d
Merge: 1dc43a36 c5820fa1
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Fri Mar 12 14:02:03 2021 +0000

    Merge pull request #410 from alexwlchan/inside-outside-stroke

    Add a post about inner/outer strokes

commit c5820fa1b86d8a55a3aa495c4f8fe1a974686ba7
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Mar 12 13:53:22 2021 +0000

    Edits on the SVG post

commit 2ef391cfcf3618c48424dae1ba32df68bb1f566c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Mar 12 11:19:05 2021 +0000

    Add the S3 tag to the large S3 objects post

commit 945a9064baae1a963ca006bca74298db0210d754
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Mar 12 09:36:59 2021 +0000

    Add the stroke mockups from OmniGraffle

commit ab52d703e124dafbed9acdb0a178d55d7c1c8724
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Mar 12 09:36:47 2021 +0000

    Print post meta properly

commit 68a8eeaf33d66e1232d93c8bb398c28c5a93b029
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Mar 11 21:53:27 2021 +0000

    Add more separators, but don't print them

commit 5a258895336a726112baf2f559aaf6bfe1c8f064
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Mar 11 21:47:55 2021 +0000

    Centralise the definition of separator icons

commit a510dc5382efdfe259195c443b448c28521553e9
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Mar 11 21:40:06 2021 +0000

    Create absolute URLs that occur inside standalone SVG images

commit 494577f197601d92e7c28aef1c9e5c25e7a16648
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Mar 11 20:42:21 2021 +0000

    Remove trailing whitespace

commit 4494ca3de7a6450f47ab4bcceee515d70f808b76
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Mar 11 20:41:40 2021 +0000

    Images in inline SVGs become absolute URLs in the Atom feed

commit 1ccacd66a0ffec8a388c060a6f4cec495199ad36
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Mar 11 20:35:53 2021 +0000

    Keep editing the SVG post

commit 831444432d7d151b9770111c3391d13a179782f2
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Mar 11 14:16:59 2021 +0000

    Keep editing and tweaking the diagrams in the SVG post

commit 367620e8629845f1c00de9abf160f5335b6c7942
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Mar 11 08:52:38 2021 +0000

    Convert more of the post to SVG

commit 89a117875c772cadf210716d4646582ec74eda33
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Mar 10 21:50:43 2021 +0000

    First draft; start to tidy up the SVG post

commit ba8479ac20f3a1081312edd3d13b823f5e5a2241
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Mar 10 08:35:38 2021 +0000

    Explain how to draw an inside stroke with clipping

commit 8267ecf875be5e9501ab69629a6ce42c31d27c38
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Mar 10 00:00:21 2021 +0000

    Start to write the post about inner/outer stroke

commit 1dc43a3647b46b4f3285ce0939de864a98937c68
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.fastmail.co.uk>
Date:   Sun Mar 7 10:53:24 2021 +0000

    Publish new post rainbow-hearts.md

commit b4f2bdbdaaafee12f539b49e6cbff88f84ae3371
Merge: 6db2102a 28e7002f
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Sun Mar 7 10:50:42 2021 +0000

    Merge pull request #409 from alexwlchan/rainbow-hearts

    Link to my rainbow hearts post

commit 28e7002f71a580cf1e4e7f83363fe7af3ccf79fb
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Mar 7 09:19:31 2021 +0000

    A couple of touch-ups on the rainbow hearts post

commit 3ec1a2b0ad30ad02b77e68c750da21bddff2964e
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Mar 6 21:52:33 2021 +0000

    Add a post about rainbow hearts

commit 3206440743003a08f8b2307cf12fb719bb519cfb
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Mar 6 21:52:20 2021 +0000

    Add a "generative-art" tag

commit 6db2102adff9117f44f9598a092fd94ab1d057d2
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.fastmail.co.uk>
Date:   Tue Mar 2 13:17:55 2021 +0000

    Publish new post an-applescript-to-toggle-voice-control.md

commit 31d2b37cea3625c34da663a8660c610ff4f1e788
Merge: c589b1b2 05d5394f
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Tue Mar 2 13:15:12 2021 +0000

    Merge pull request #408 from alexwlchan/voice-control-applescript

    Add a post about Voice Control and AppleScript

commit 05d5394f58274f54b45402f4d344f8e50162b8ac
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Mar 2 08:39:43 2021 +0000

    Remove a stray "just"

commit 239c06e7c44d5dd9f7a7f7a382189451794e7f3e
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Mar 2 08:38:21 2021 +0000

    Write another draft of my Voice Control post

commit 3d4e3127e0b626afb77fc708fdf7223db684bcaf
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Mar 1 20:57:35 2021 +0000

    Add an initial post about Alfred + Voice Control

commit c589b1b207f19a2658957d818ea05433723ff789
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.fastmail.co.uk>
Date:   Mon Feb 15 20:12:06 2021 +0000

    Publish new post digital-verification.md

commit 34b48e9d9649d2857bb230da00a6a46c39037055
Merge: ee686560 926d42ef
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Mon Feb 15 20:08:13 2021 +0000

    Merge pull request #407 from alexwlchan/link-stuff

    Add a couple of link posts

commit 926d42efa5e57579a0588c133cf3985bd8c7e14f
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Feb 15 20:02:59 2021 +0000

    Link to my post about digital verification

commit 7dd9faa2cc20e0614eed6f7c2a8239807890c2ed
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Feb 15 19:31:25 2021 +0000

    Link to my "Screaming in the Cloud" episode

commit ee6865608fb7091b2c8405d1cd4f1de2afc48fc8
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.fastmail.co.uk>
Date:   Sun Jan 31 12:25:07 2021 +0000

    Publish new post kempisbot.md

commit 670049112dd961739b75b2f8f5b3af44c3194ae8
Merge: cdbeec8d c2ced20a
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Sun Jan 31 12:22:29 2021 +0000

    Merge pull request #406 from alexwlchan/kempisbot

    Add a post about how KempisBot works

commit c2ced20a74a39a9033ba590c110cc35902505aa0
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jan 31 12:17:48 2021 +0000

    Final markups and alt text

commit c984d5217f13ddfd6faaf06c4280214b7cac151c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jan 31 12:04:41 2021 +0000

    Add a script for generating the Twitter auth file

commit cb073e0802d4f0e720c805cb45c5c47895b62ce7
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jan 31 12:03:09 2021 +0000

    Further drafts of the kempisbot post

commit c3ea7f5ee019bf1bef861e08303d197018bd43a1
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jan 31 10:54:40 2021 +0000

    Initial draft of a post about KempisBot

commit cdbeec8dfe006d829ed730e09b15f13405a6eca9
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Jan 21 14:51:33 2021 +0000

    Remove images

commit 56e97163fb06a4cad744a8cdf9c762862022ad13
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jan 10 19:40:25 2021 +0000

    Redrive SQS messages one-by-one

    So messages will never be deleted before they're read from the queue.

commit a48d56113ed679227220fc5faf9c8abcd983fbc3
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Jan 7 05:06:57 2021 +0000

    Remove mention of MSW

commit 5168c4b7630c91eb61a68c21cfb6c3cb1cee30d9
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jan 1 18:43:49 2021 +0000

    Add a note about visiting the original post

commit 233cc3d69d771140ca6d813409b96b02b3f0e16e
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jan 1 18:39:30 2021 +0000

    Add pretty printing of the XML in the Atom feed

    This should make debugging it easier, and leave less vast swathes of
    whitespace in the file.

commit 41c1d4e8061c71e79fe49a88e5df43dc78aef561
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jan 1 18:34:20 2021 +0000

    Use a CDATA block to embed literal HTML in the RSS feed, easier to debug

commit 55124e984bbbe2a87f52c43dabd8f6db0ec8d8bb
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jan 1 18:28:34 2021 +0000

    Properly replace custom post separators

commit 062c290f5b3f29167a6e19659bc251ef3e96f9c8
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jan 1 11:17:53 2021 +0000

    make the obvious reference

commit 003c6ddbd0dcc969671d1342b3c41458bbbe4346
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.fastmail.co.uk>
Date:   Fri Jan 1 11:11:48 2021 +0000

    Publish new post what-year-it-it.md

commit 9d569803a38247436592236d6397cbb3aab9ced4
Merge: d67de845 08a9bad1
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jan 1 11:08:45 2021 +0000

    Merge pull request #405 from alexwlchan/iso-week-dates

    Add a post about ISO week dates

commit 08a9bad1215122385628ad4dad07273469410fab
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jan 1 11:04:16 2021 +0000

    Fix permalinks in the RSS feed

commit b184b32cede7844e21ff45cfea3a709a620ca358
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jan 1 11:04:04 2021 +0000

    Ditch custom icons in the RSS feed

commit 5b91fb7a337632c1bfbcc5a20b53347ad0086160
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jan 1 10:55:24 2021 +0000

    Link to the original thread

commit 40770b43b0a72010fc4be8942b722dc34d2689ee
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jan 1 10:51:34 2021 +0000

    Add an example usage for the inline_svg plugin

commit 5c7b3f51252377b2fa568a861d4936ce2a7e9dce
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jan 1 10:51:24 2021 +0000

    Add a post about ISO week dates

commit d67de8451949ce7f302bbc09eb389eaac5425af6
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Dec 2 20:32:46 2020 +0000

    History only occurs once

commit 55d48e9b04a45824a80f6689ba2ca68c1ddf91f3
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.fastmail.co.uk>
Date:   Tue Dec 1 21:19:16 2020 +0000

    Publish new post creating-short-lived-temporary-roles-for-experimenting-with-aws-iam-policy-documents.md

commit 28ad632468d792a1da0044dc814b821f32b849ff
Merge: 6e404d66 66cb87c4
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Dec 1 21:16:26 2020 +0000

    Merge pull request #404 from alexwlchan/iam-policy-document-test

    Link to my code for creating short-lived IAM policy documents

commit 66cb87c4b51a3480cb235330756d0dca1c29c3c1
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Dec 1 21:04:22 2020 +0000

    Link to my code for creating short-lived IAM policy documents

commit 6e404d66a8859a06b5a5c253435736526ccbcd23
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.fastmail.co.uk>
Date:   Tue Nov 24 11:53:35 2020 +0000

    Publish new post non-technical-users.md

commit 97817ebb5f5bee7c484646345caddc5187d2c58d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Nov 24 11:50:17 2020 +0000

    Add a post about the phrase "non-technical users"

commit 70d190a5de7b0a2438fcc281421e26d4758417f4
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Nov 23 00:28:06 2020 +0000

    Add a couple of missing AWS tags

commit 9b2da6005b1522580a5cc6feaa36015de1113a1a
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.fastmail.co.uk>
Date:   Wed Nov 18 09:41:33 2020 +0000

    Publish new post copying-images-from-docker-hub-to-amazon-ecr.md

commit c385d45bbebaefed598a83a24950f9dc608d787a
Merge: 3f53350b 47f7fd68
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Wed Nov 18 09:38:53 2020 +0000

    Merge pull request #403 from alexwlchan/docker-hub-ecr-script

    A script to copy images from Docker Hub to Amazon ECR

commit 47f7fd687f1d983ae84fa8c2094a6d7805af4462
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Nov 18 09:34:30 2020 +0000

    Final markups on the Docker Hub/ECR post

commit 86f3ac77181b8d0d2f7d850a17da25704870ec68
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Nov 18 08:20:49 2020 +0000

    Edits on the Docker Hub ~> ECR post

commit cedc1a50455ff154ace4923d4d2f08132f46e878
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Nov 18 08:08:46 2020 +0000

    First draft of a link post about Docker ~> ECR script

commit 3f53350bc4fc31315852f9a2daaa3c9e5dbc2980
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.fastmail.co.uk>
Date:   Mon Nov 16 09:16:48 2020 +0000

    Publish new post how-i-read-non-fiction-books.md

commit b304bce45d90942530a927c707861b68caf02eff
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Nov 16 09:13:47 2020 +0000

    Edits on my post about reading books

commit b72f47d027ea01d67929e78ed92859841756a514
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Nov 16 08:53:43 2020 +0000

    Markups on "how I read non-fiction books"

commit aa54effae615ad718da216b715ff86941051c2e3
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Nov 16 08:35:17 2020 +0000

    Initial draft of "how I read non-fiction books"

commit 6571961e74bac65b711758bcaf63f075ee7f2389
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.fastmail.co.uk>
Date:   Sun Nov 15 10:08:33 2020 +0000

    Publish new post maths-is-about-facing-ambiguity-not-avoiding-it.md

commit 74a56a021b5e4cc8451a7bc66d4698f6b47e406c
Merge: f5b6d2e4 bd7788c4
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Sun Nov 15 10:05:51 2020 +0000

    Merge pull request #402 from alexwlchan/maths-ambiguity

    Maths is about facing ambiguity, not avoiding it

commit bd7788c4efbf4c9e839617ab133de2dd2a7dd32d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Nov 15 10:01:49 2020 +0000

    Add a link to the original Twitter thread

commit 0e6a2653e2e2ac86f125a19a0d77d1f2a3867f82
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Nov 15 00:05:36 2020 +0000

    Add a post about dealing with ambiguous problems

commit f5b6d2e4ba82b71c5def71977b29c617bf7b73f7
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Nov 6 15:29:06 2020 +0000

    Don't be clever with characters in the summary

commit fdb22beee0413f46ca4d74bb11cf10610e50e1f2
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Nov 6 15:27:03 2020 +0000

    Add a note about progressive enhancement

commit 07786ce4320261ce3bb24f02de0b20ec677466f1
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.fastmail.co.uk>
Date:   Fri Nov 6 15:20:01 2020 +0000

    Publish new post remembering-if-a-details-element-was-opened.md

commit 6b69ef8e8aa782e404a2a69acd9b71c1cba42f35
Merge: 12ed0742 996257a7
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Fri Nov 6 15:16:11 2020 +0000

    Merge pull request #401 from alexwlchan/remember-the-details

    Post about remembering the state of <details>

commit 996257a7614efaf633875ab861ce03a502762710
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Nov 6 15:11:20 2020 +0000

    Add a post summary

commit be207db81c094d6cf4465227ed81706873a3af0a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Nov 6 15:09:08 2020 +0000

    Edits on the <details> post

commit bfb9661f622bd7f273d75549ba32f6d7c655b80e
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Nov 5 21:54:16 2020 +0000

    Initial draft of a post about remembering the state of <details>

commit 12ed07422b857789004943e9690e810bb6090cda
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.fastmail.co.uk>
Date:   Sun Nov 1 09:13:27 2020 +0000

    Publish new post a-python-function-to-ignore-a-path-with-git-info-exclude.md

commit a07939506ac4f5484bb49d7abc63452c7cd97b6e
Merge: 531e4565 2814b460
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Sun Nov 1 09:11:01 2020 +0000

    Merge pull request #400 from alexwlchan/git-info-exclude

    A Python function to ignore a path with .git/info/exclude

commit 2814b4604fec674f1b96f9b41d7f4174e63d0315
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Nov 1 09:06:49 2020 +0000

    Even better title and URL slug

commit 41348d649fb0d0ba3276a1eb94a6fd2d5311ed69
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Nov 1 09:06:25 2020 +0000

    Better title for the post

commit b659b84d83d5673101f73da474a1979265f78eb8
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Nov 1 09:03:06 2020 +0000

    Markups on my Python + .git/info/exclude post

commit 715a828214d44cff57c47d4a627cf529f37772b1
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Nov 1 08:53:23 2020 +0000

    First draft of post about Python + .git/info/exclude

commit a8fcd9c568eb242fc440e1f8d5d8079ce8af093a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Oct 31 19:12:41 2020 +0000

    Don't exclude miniposts from the front page

commit 531e45657d72d643c03cd1f14e87dc030224d91a
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.fastmail.co.uk>
Date:   Fri Oct 30 18:25:23 2020 +0000

    Publish new post til-using-git-check-ignore-to-debug-your-gitignore.md

commit 92c79abfe1c97a4aed2b8c7828dd0b0b42592f71
Merge: 92e06f96 9dfdc1eb
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Fri Oct 30 18:23:01 2020 +0000

    Merge pull request #399 from alexwlchan/git-check-ignore

    Add a quick post about git check-ignore

commit 9dfdc1eb37f58c7640b0c22d4089190bcab359dc
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Oct 30 18:18:29 2020 +0000

    Add a quick post about git check-ignore

commit beb36032cebace32dae3c2818677ed57936a69d3
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Oct 30 17:59:03 2020 +0000

    Escape the title when writing YAML front matter in a new post

    This means that titles with colons (e.g. "TIL: A new fact!") don't cause
    the YAML parser to be sad when you built the site.

commit 92e06f96b1e4fcfad47d8729aa712e03e42a840c
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.fastmail.co.uk>
Date:   Sat Oct 17 16:58:19 2020 +0000

    Publish new post how-do-i-use-my-iphone-cameras.md

commit 91cf420b63f134f6eca2a428cb2842807bbb280f
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Oct 17 17:55:33 2020 +0100

    Run optipng over a couple of images

commit 6684362d5423853b7e503ec6c135c8e039218c22
Merge: 3d5b1989 8ad2df1a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Oct 17 17:53:40 2020 +0100

    Merge pull request #398 from alexwlchan/exif-lenses

    Add a post about finding out how often I use my iPhone cameras

commit 8ad2df1a0f21153b579cc7f52e74034aef9c612b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Oct 17 17:49:52 2020 +0100

    Add some alt text to the info screenshot

commit 7eee5287b68f4f3306af19e5c468d6cc8810cf45
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Oct 17 17:49:01 2020 +0100

    More markups on my EXIF post

commit 11a1c447c04d8b0f1f7fe767e5572002197eb458
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Oct 17 17:25:18 2020 +0100

    Markups on how I use my iPhone cameras

commit 6039ad741e5330505b6ae977dc15840e4f97e7e6
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Oct 17 16:00:42 2020 +0100

    First draft of a post about EXIF metadata

commit 3d5b1989a8f2af9c0ab8e1a6875ea8fd832c658a
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.fastmail.co.uk>
Date:   Mon Oct 12 18:02:19 2020 +0000

    Publish new post the-importance-of-good-error-messages.md

commit 1b374c865a7021d645e057182b2f2790bfaff25f
Merge: fdbec393 4ed360eb
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Mon Oct 12 17:59:40 2020 +0000

    Merge pull request #397 from alexwlchan/error-handling

    Add a post about Excel error messages

commit 4ed360eb64c44b61a5dc179aa45f4b26678cb412
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Oct 12 18:55:20 2020 +0100

    Markups on my post about Excel error messages

commit eed99d5a9e9ab37cb5afea71fcd2addc3bd41e59
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Oct 12 17:48:27 2020 +0100

    Add a post about Excel error messages

commit a62d3468884334b633c186e46016d6e5896ee6b8
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Oct 12 17:45:48 2020 +0100

    Put tags on new posts, not categories

commit fdbec393ee3b007bf7490174a88563b8de03de79
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.fastmail.co.uk>
Date:   Mon Oct 12 06:52:55 2020 +0000

    Publish new post a-new-readme-for-docstore.md

commit a688f24830b6eadd6464edc585c367297ae6fc10
Merge: 9ed247a3 5435a1cc
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Mon Oct 12 06:50:05 2020 +0000

    Merge pull request #396 from alexwlchan/docstore-readme

    Link to my new docstore README

commit 5435a1cc05eb6f2ab4a6e605fb587aeb4290463c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Oct 12 07:45:08 2020 +0100

    Couple of clarifications on Monday morning

commit 8f430956450749a299e8ce061a07a7ccce7249a9
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Oct 11 21:35:58 2020 +0100

    Since the image is 500px wide, we can go to 3x

commit e55f1d46d83bf42d633cfb2cc0e3bfc37b82229a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Oct 11 21:33:47 2020 +0100

    Link to my new docstore README

commit e5d5404f8f88321e23087fd34f8a831c05fd9121
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Oct 11 21:27:52 2020 +0100

    Don't put a double space in the arrow on link post titles

commit 9ed247a39b6243221c71999b84d6cc4bc58c42ff
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Oct 10 09:23:40 2020 +0100

    Fix the images in the sign post post

commit 68f1bf7dd53dbbce77bcdbbb831a3769a3cc1c8b
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.fastmail.co.uk>
Date:   Fri Oct 9 11:37:48 2020 +0000

    Publish new post a-sprinkling-of-azure.md

commit f8c0f24d4bc51420ac90f96415ccb2ef59296472
Merge: 146ec987 e4354a9d
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Fri Oct 9 11:35:09 2020 +0000

    Merge pull request #395 from alexwlchan/azure-link-post

    Link to my post about Azure replication

commit e4354a9d2db95cb1145460e7909c6d0a68f86fc5
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Oct 8 20:12:28 2020 +0100

    Link to my post about Azure replication

commit 146ec987b03ca5997a9ec9bf31a55d2e9f1ed6b9
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.fastmail.co.uk>
Date:   Sat Sep 26 10:14:58 2020 +0000

    Publish new post using-qlmanage-to-create-thumbnails-on-macos.md

commit 16e69f9982300c8352daba16de17fe993665f3da
Merge: c324dfe0 9f1d335c
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Sat Sep 26 10:12:40 2020 +0000

    Merge pull request #394 from alexwlchan/thumbnailing-with-qlmanage

    Using qlmanage to create thumbnails on macOS

commit 9f1d335c76959591212a13d77227cfddc416de75
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Sep 26 11:08:47 2020 +0100

    Add the images for the Quick Look post

commit e0db5e2813925ec410d446b4805022a6c7880783
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Sep 26 09:42:23 2020 +0100

    Don't show tags if there aren't any

commit b08247f1daaa76d4086ee583943bb987f1baeaa8
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Sep 26 09:42:00 2020 +0100

    Add a quick post about using qlmanage to create thumbnails

commit c324dfe0346bae83a065769dd661392930ccde76
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.fastmail.co.uk>
Date:   Tue Sep 8 07:06:07 2020 +0000

    Publish new post two-python-functions-for-getting-cloudtrail-events.md

commit be7c6955302846deb3ed5285afed19eeb54e5ad3
Merge: 42e5075a f7476a16
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Tue Sep 8 07:03:21 2020 +0000

    Merge pull request #393 from alexwlchan/cloudtrail-functions

    A quick post about two CloudTrail functions

commit f7476a16d78d56c07fc6f933ec99ffbe34b34c4b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Sep 8 07:58:52 2020 +0100

    A couple of small markups and clarifications

commit a9a2d078afaf82c47653eac62fe3aa4279d6cd89
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Sep 8 07:52:32 2020 +0100

    First draft of my post about CloudTrail events

commit 42e5075a4b62d3b9fa27315820d018d06277abd6
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Sep 7 08:14:24 2020 +0100

    I now have a shiny new wellcome.org email address

    See https://wellcome.ac.uk/news/why-were-changing-wellcome-org

commit 314d678a98eb49176fbc4c52d2daacf4acb6c563
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Aug 20 07:59:06 2020 +0100

    Add a summary to the S3 prefix post

commit 0771d9d3b45a04ed366161ecec39286b7d429c3e
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.fastmail.co.uk>
Date:   Thu Aug 20 06:50:04 2020 +0000

    Publish new post s3-prefixes-are-not-directories.md

commit 4941912e67723146205e71ad6c39eb76fb38818c
Merge: e44dfa4e ab265c2a
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Thu Aug 20 06:47:04 2020 +0000

    Merge pull request #392 from alexwlchan/s3-prefixes-are-not-folders

    S3 prefixes are not directories

commit ab265c2a93eb5eefc3131afe331077cf6203349a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Aug 20 07:40:46 2020 +0100

    More markups on S3 prefixes are not directories

commit 8f6bf53e8749f1c2904cf4476ff4a2666e1e1669
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Aug 20 07:13:33 2020 +0100

    Add some markups on S3 prefixes are not directories

commit d21947a0eafe33c5a52cdf4894ce648591529d27
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Aug 20 06:23:26 2020 +0100

    First draft of "S3 prefixes are not directories"

commit e44dfa4e76ce167c59f68fb125d1ae82036ea7a5
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Aug 18 17:11:29 2020 +0100

    More stuff about S3 keys and file paths

commit 7f3673a905421e1b700140971a8db4a89a7a8e85
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Aug 18 17:11:17 2020 +0100

    Add "Large things living in cold places" to the best of list

commit f9d6ab85ac4699c635a468163f03986d0710b6d1
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Aug 18 17:11:08 2020 +0100

    HTTP error messages should also get non-breaking spaces

commit 637ec47f36c9366c80ab4d5064e65d765692d6d4
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Aug 18 17:10:52 2020 +0100

    Run optipng over this S3 screenshot

commit eaf6c4c62b3634280918f25fd7158049ceba6501
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.fastmail.co.uk>
Date:   Tue Aug 18 15:19:21 2020 +0000

    Publish new post s3-keys-are-not-file-paths.md

commit aa8488bd745535e0ed070209eb017d8bfeba5c2e
Merge: a144f2d0 aff2a896
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Tue Aug 18 15:16:17 2020 +0000

    Merge pull request #391 from alexwlchan/s3-keys-are-not-paths

    S3 keys are not file paths

commit aff2a8963bdeeac0f89689e38f2d4becf10a10bd
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Aug 18 16:11:48 2020 +0100

    Finish editing the post about S3 keys and paths

commit 0d90f6fb6c35a085c5dfc531044c4552b94a0845
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Aug 18 15:48:34 2020 +0100

    More edits on the post about S3 keys

commit 52d6f852aa3dff5599ebec59b0a6cd05c2a83f6c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Aug 18 14:55:06 2020 +0100

    First round of edits on my post about S3 keys

commit a421968bfe13d529410a46972114428aecac6ef0
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Aug 18 14:22:57 2020 +0100

    Initial draft of "S3 keys are not file paths"

commit a144f2d0397ebb7f923b279629ba31d8c3ea9be2
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Aug 16 16:56:54 2020 +0100

    Update 2019-07-08-creating-preview-thumbnails-of-pdf-documents.md

commit f75d8e5228711f20c9b1e983edcaa497aae90a21
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Aug 15 14:36:21 2020 +0100

    Oops, that flag should be -jpeg, not -jpg

commit 1218781ff4110ffa7b5a2eee4ce35b19c367a836
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.fastmail.co.uk>
Date:   Thu Aug 6 11:14:20 2020 +0000

    Publish new post using-fuzzy-string-matching-to-find-duplicate-tags.md

commit 0fdeebe40c52eb6ca9de03aca47b40a83bfe2d1e
Merge: 4666d189 de7ae1a4
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Thu Aug 6 11:11:50 2020 +0000

    Merge pull request #390 from alexwlchan/finding-similar-tags

    Using fuzzy string matching to find duplicate tags

commit de7ae1a4d0ddf7e5b24d0816ca755606752b2020
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Aug 6 12:06:34 2020 +0100

    Final markups on the "similar tags" post

commit 9cab81b1f9e1ddc793146fe4ea26befa48292052
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Aug 6 10:47:54 2020 +0100

    Some markups on the fuzzy string matching post

commit f3237d503ab0583f0418b5c2e23a16c3b6dbc83b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Aug 6 08:55:52 2020 +0100

    Initial draft of FuzzyWuzzy post

commit 4666d189a776955331208bd931e965b8a5fe1e4e
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jul 31 19:41:01 2020 +0100

    "What does \d match in a regex": tighten it up, improve the ending

commit d6741ec6561451e7a7443aa25e564e3cf708a4bb
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Jul 27 10:00:42 2020 +0100

    Shorten this line so it has nicer paragraph breaking

commit 328f2cc39bf6791d933b09e24591884a2adf599e
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.fastmail.co.uk>
Date:   Sun Jul 26 17:31:37 2020 +0000

    Publish new post getting-a-markdown-link-to-a-window-in-safari.md

commit 3ac9bcdb80aceb4283e0d7cb6fbca3e8c80400ea
Merge: 71b7b510 0b3eb673
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Sun Jul 26 17:29:06 2020 +0000

    Merge pull request #389 from alexwlchan/md-link

    Quick post about getting Markdown links from Safari windows

commit 0b3eb673ceccbacee20568446e2e75c8e773c5aa
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jul 26 18:24:17 2020 +0100

    Quick post about getting Markdown links from Safari windows

commit 71b7b510d7eeed2318fa4a809c49882ecdcca65b
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.fastmail.co.uk>
Date:   Wed Jul 22 14:18:15 2020 +0000

    Publish new post why-do-programming-languages-have-a-main-function.md

commit c3239ca648751e7db0421ef62d921c5c1b86fe92
Merge: 640ae0c8 64b665ef
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Wed Jul 22 14:15:49 2020 +0000

    Merge pull request #388 from alexwlchan/where-did-main-come-from

    Where did the main function come from?

commit 64b665ef37a72ae62bd05175bc5d6a079535c335
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Jul 22 15:11:14 2020 +0100

    Tweak the conclusion

commit ffe21b11ca0e794783afc706617aa4a22eb2a41e
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Jul 22 14:49:46 2020 +0100

    Finish marking up the "main function" post

commit 31275c3347893c575d0e505577124007f2dff1f5
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Jul 22 07:37:30 2020 +0100

    Initial draft of "Why do programming languages have a main() function?"

commit 640ae0c8b6fff6b0ec4f2fbf1ff555547f826c36
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Jul 21 21:34:41 2020 +0100

    Add tags, not a category

commit 631c23870e8912bd3188d254b7d08ce5832ec036
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.fastmail.co.uk>
Date:   Mon Jul 20 09:06:39 2020 +0000

    Publish new post running-concurrent-try-functions-in-scala.md

commit d84733498e3e8c794f36952894e162dc7fa97f35
Merge: 27a1d408 9d2b693d
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Mon Jul 20 09:00:15 2020 +0000

    Merge pull request #387 from alexwlchan/running-concurrent-try

    Add a quick post about concurrent Try functions in Scala

commit 9d2b693d0b3dd6bfcf1d93499f6039c7a340fa53
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Jul 20 09:54:55 2020 +0100

    Add a quick post about concurrent Try functions in Scala

commit 9124c66b416dbd30b374538458d79a71207aeb70
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Jul 20 09:54:41 2020 +0100

    Don't bother minifying the XML feed

    Very few people will be loading this directly; they'll be using an
    aggregator service like Feedly or Feedbin, and they have plenty of
    spare bandwidth.  It should fix the issue where <code> blocks don't
    lose all their newlines, maybe.

commit 27a1d40847c79992557bd3a914eb6141f4af6e18
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.fastmail.co.uk>
Date:   Mon Jul 13 22:20:07 2020 +0000

    Publish new post what-does-d-match-in-a-regex.md

commit 795ad64f0c1afda2b2f46459cc78e86cac9c23c7
Merge: 5833066e 914db596
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Mon Jul 13 22:17:24 2020 +0000

    Merge pull request #386 from alexwlchan/the-d-capturing-group

    Add a quick post about matching \d in a regex

commit 914db5960ec1e12397b02c1f7350a5161774e9db
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Jul 13 23:13:14 2020 +0100

    Add a quick post about matching \d in a regex

commit 5833066efbf4d9b691c3fb6f6439badbaabc03b9
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.fastmail.co.uk>
Date:   Sun Jul 12 07:34:45 2020 +0000

    Publish new post how-to-do-parallel-downloads-with-youtube-dl.md

commit f70050b775ad70ee30db31cf4b20e89d7ab180f9
Merge: 93d72a9c 73c2a982
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jul 12 08:32:10 2020 +0100

    Merge pull request #385 from alexwlchan/youtube-dl

    Add a quick post about parallel downloads with youtube-dl

commit 73c2a9827873bca5d58cfef0b5a569b62786a0a6
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jul 12 08:28:10 2020 +0100

    Add a quick post about parallel downloads with youtube-dl

commit 93d72a9cded200d1d14237f3cdc783013823eda4
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.fastmail.co.uk>
Date:   Mon Jul 6 21:31:33 2020 +0000

    Publish new post changing-the-accent-colour-of-icns-icons.md

commit 2c36fa6987701aa46cd83726e7ffd93c8ee3d453
Merge: 412a0f4d 5634093c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Jul 6 22:28:45 2020 +0100

    Merge pull request #384 from alexwlchan/icns-manipulation

    Write a post about changing the accent colour of ICNS files

commit 5634093c39dcef9111234c433a3f139f298a3e1a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Jul 6 22:25:08 2020 +0100

    Add missing alt text to images

commit cf579b71e91b1aa69229d4c46a0101d474d437de
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Jul 6 22:17:21 2020 +0100

    Final markup for line-breaking ness

commit 292ed572d0c0afa406bce6f09db7c72c11012a38
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Jul 6 22:10:13 2020 +0100

    Final markups and a preview image

commit 8c6b46078b5f368e207b264d1a8b8b0063e5bf32
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Jul 6 19:48:26 2020 +0100

    Include a link to the page source in the <head>

commit c716a806d5f3f2f54107d7a6b3e9c98f885842cd
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Jul 6 19:48:06 2020 +0100

    Add a tag for "python-pillow"

commit 7c98c82b00acd37d5de48d228f9a02712db832f5
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Jul 6 19:47:57 2020 +0100

    Add an initial draft of my "accent colour of ICNS files" post

commit 412a0f4d57b9c978df4dfb205be516cce92d8f31
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jul 5 19:33:17 2020 +0100

    Add a couple of missing tags to this post

commit 31af9219db4f62ed0e277b8c6178fca7d662683f
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jul 5 19:27:19 2020 +0100

    That Docker command only works if you supply the image

commit 70876075b79d90ef5dc0175330d8ff12c3770dc2
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Jul 4 22:49:26 2020 +0100

    Re-enable Twitter cards

commit 396b564ba5a59a48bee3cf486f9efb451082e0b5
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jul 3 09:41:53 2020 +0100

    Fix the name of `dynamo_client` in the DynamoDB scanning post

commit 1d3d66eb8cb1d4495fafc7cf67c013d7ad0b5b27
Merge: 37190192 8ce09d6c
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Sun Jun 28 08:33:54 2020 +0000

    Merge pull request #383 from alexwlchan/less-youtube-tracking

    Use youtube-nocookie.com to reduce tracking from YouTube embeds

commit 8ce09d6cfabaecda3afb35799fd510a744c232dc
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jun 28 09:30:04 2020 +0100

    Use youtube-nocookie.com to reduce tracking from YouTube embeds

    h/t Steve Troughton-Smith: https://twitter.com/stroughtonsmith/status/1276940666933821440

    > Today's protip: swap all your YouTube embeds for
    > "http://youtube-nocookie.com". You may not even know you have
    > tracking on your site, and Safari in macOS 11 will make it very clear

commit 371901926e48769c3da6eebfceb10924be5a473e
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.fastmail.co.uk>
Date:   Wed Jun 24 20:02:44 2020 +0000

    Publish new post using-applescript-to-open-a-url-in-private-browsing-in-safari.md

commit 084e3cc63a969e40c0390536c6598a58916f87a0
Merge: 00f1b3bf 1329d91b
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Wed Jun 24 20:00:14 2020 +0000

    Merge pull request #382 from alexwlchan/private-browsing

    Add a post about AppleScript and private browsing

commit 1329d91b09b1763d101db00d86a7063a3d3d39f6
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Jun 24 20:56:02 2020 +0100

    Add a post about AppleScript and private browsing

commit 00f1b3bfbdfebc5ff5bde9d9644d27c535fdfa64
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.fastmail.co.uk>
Date:   Sun Jun 21 10:44:14 2020 +0000

    Publish new post fat-shaming-in-the-good-place.md

commit 7ace61079fb4d8d4efd06422511ab46fdc9e650d
Merge: 1ce7bdbb 28a7ae74
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Sun Jun 21 10:41:56 2020 +0000

    Merge pull request #381 from alexwlchan/fat-shaming-is-the-bad-place

    Post: Fat shaming in “The Good Place”

commit 28a7ae744e42d63b453038ccdac7012e38fc7771
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jun 21 11:21:52 2020 +0100

    Tighter ending

commit ca8cb0ce2710d12c0f391426beced3d78807a9bb
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jun 21 11:17:59 2020 +0100

    Add a post about fat shaming in The Good Place

commit 1ce7bdbb8046da900780ff3db6f14282a6d26aba
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.fastmail.co.uk>
Date:   Sat Jun 20 08:36:40 2020 +0000

    Publish new post large-things-living-in-cold-places.md

commit 4bd330f1a4661993aaf7e96627d28e51eecf12e9
Merge: ea6f6f10 d1c05261
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Sat Jun 20 08:33:54 2020 +0000

    Merge pull request #380 from alexwlchan/cold-places

    Add a link to my post about Glacier + digital archives

commit d1c052619ac30fecbd81205fc0d34bd83c00fe32
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Jun 20 09:29:17 2020 +0100

    Add a link to my post about Glacier + digital archives

commit ea6f6f105fa582c641e248cb73930717e3248801
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.fastmail.co.uk>
Date:   Mon Jun 15 20:49:45 2020 +0000

    Publish new post always-read-your-contract.md

commit 7b29cd346380eae7bee9d28151b7f6f4b106546e
Merge: 0ebb23b0 2791a180
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Mon Jun 15 20:47:35 2020 +0000

    Merge pull request #379 from alexwlchan/always-read-your-contracts

    Add a post about always reading your contracts

commit 2791a180e723465e780318e885be498a75ea78d0
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Jun 15 21:43:12 2020 +0100

    Add a post about always reading your contracts

commit 0ebb23b0b54aec9e5ee5c7c7f652a14c759efdaa
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.fastmail.co.uk>
Date:   Mon Jun 15 06:57:52 2020 +0000

    Publish new post archive-monocultures-considered-harmful.md

commit f833a604f0e73a0a3308858b504a64571eb46c80
Merge: eafe1fd0 d3a5e64d
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Mon Jun 15 06:55:41 2020 +0000

    Merge pull request #378 from alexwlchan/archive-monocultures

    Add a post about archive monocultures

commit d3a5e64d23071ee0fd11606c3e093f2fa16f07ee
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Jun 15 07:51:29 2020 +0100

    Final edits before posting

commit 0c0115985b4d78bad4532cf0cef561f4ae6ea7a6
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Jun 15 07:33:29 2020 +0100

    Add a link to the Twitter thread

commit a21767412a549b13c8d6248345e11e9ac14945e4
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Jun 15 07:31:36 2020 +0100

    Edits and markups on Monday morning

commit a2f2d1a0729852de2cd7d8719f7f378a3c6cf9c6
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Jun 15 07:27:04 2020 +0100

    Markups and edits on Sunday night

commit e0a31deb3253a061072be14f34e50e7f0e33b49b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jun 14 23:04:23 2020 +0100

    Apply some fixes from dictation mistakes

commit 1dc69ecce107318bb73ac64173894481ea4c3b24
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jun 14 22:53:39 2020 +0100

    Second draft of archives post

commit 1e252ad290f7c8b7c1d34fe6cbfb164293cbc044
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jun 14 22:23:32 2020 +0100

    First draft of a post about archive monocultures

commit eafe1fd0d08c7c7199f9cc701613338610ede4bf
Merge: b9e6acc5 a539337b
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Mon Jun 8 00:21:02 2020 +0000

    Merge pull request #377 from alexwlchan/redo-archive-pages

    Redesign the "all posts" pages

commit a539337bed9146a58d6cd0a6730a5073bd5234e4
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Jun 8 01:05:43 2020 +0100

    The links in the all-posts page are anchors, not pages

commit 5a735086157ecd0ab2f8fca21b2b4951314b752b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Jun 8 00:59:40 2020 +0100

    Link to tag pages, not category pages

commit 443cb7c41261297049698918dd92fbed7d16b049
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Jun 8 00:19:46 2020 +0100

    CSS goes in the CSS file

commit 90bc80e90d6305f5257b459dc842b2788fa12d25
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Jun 8 00:18:49 2020 +0100

    Fix some more tagging things

commit b3cdbc2809af4831471f1210cc3df3ffa2ff878e
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Jun 8 00:18:38 2020 +0100

    Use logarithms to balance the tag cloud better

commit e463c62ff4ccb89fca77cf12b96a2c6cddfe716a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jun 7 17:10:54 2020 +0100

    Sort out tag browsing in the archive

commit 633e0754e2f7e79ba016989f7c1ce18007174987
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jun 7 15:25:52 2020 +0100

    Start to refactor/simplify the per-year logic

commit a479a534c3c25ef4e360df18e7a9234235e77a70
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jun 7 08:37:26 2020 +0100

    Add a page for browsing by tag

commit b9e6acc55fa9eb887df8397dde6516a850ccb3de
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.fastmail.co.uk>
Date:   Sat Jun 6 06:38:11 2020 +0000

    Publish new post finding-the-months-between-two-dates-in-python.md

commit e919026bf18a3525a14ce2b302104f7c6fb0d1b6
Merge: ed680391 a8a3f85a
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Sat Jun 6 06:36:08 2020 +0000

    Merge pull request #376 from alexwlchan/finding-months-between

    Finding the months between two dates in Python 📆 + 🐍

commit a8a3f85aabb105f4cacdb384ec04bb17dd41070f
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Jun 6 07:30:57 2020 +0100

    Post: Finding the months between two dates in Python

commit ed680391c3fc24deaa111bd6c1fbab1f8a2cfea5
Merge: 6a8e2f4e 47f0e667
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Fri Jun 5 14:43:35 2020 +0000

    Merge pull request #375 from alexwlchan/add-queerjs-slides

    Add my slides for QueerJS London

commit 47f0e6678e4ddb35676f268b246a92764dd3cbca
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jun 5 15:12:08 2020 +0100

    Add my slides for QueerJS London

commit 6a8e2f4e3b51514348af8a9780b165a0b20826b4
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed May 27 10:54:09 2020 +0100

    Remove a stray debugging line

commit dc17ad248d62f2748ae6ef669e880f494f6b5046
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.fastmail.co.uk>
Date:   Wed May 27 09:26:14 2020 +0000

    Publish new post getting-every-item-from-a-dynamodb-table-with-python.md

commit a4f0c701591b466d308d83045c734a9ec4b49519
Merge: bdbc5a44 ea959499
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Wed May 27 09:24:23 2020 +0000

    Merge pull request #373 from alexwlchan/dynamodb-tables

    Add a post about getting every item from a DynamoDB table

commit ea959499c9137273bee396caa0f4658ff201ae58
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed May 27 10:20:49 2020 +0100

    Add a post about getting every item from a DynamoDB table

commit bdbc5a4482c32757e3533cff9242df13dd918eb2
Merge: 4315a988 f912ecf3
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Wed May 27 05:53:25 2020 +0000

    Merge pull request #372 from alexwlchan/plugin-fixes

    Relative URLs in the RSS feed should be absolute

commit f912ecf3e765d890b62225290ed2b77684b70ef4
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed May 27 06:48:44 2020 +0100

    Relative URLs in the RSS feed should be absolute

commit 4315a9884d9449262d3aeb6327cda5a931adcea9
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.fastmail.co.uk>
Date:   Sun May 24 11:08:57 2020 +0000

    Publish new post human-friendly-dates-in-javascript.md

commit e6252b57f38fc1dc966a2e6e7f50584d5f8ac47a
Merge: fddc0635 db7f5c78
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun May 24 12:07:02 2020 +0100

    Merge pull request #371 from alexwlchan/human-friendly-dates

    Add a post "Showing human-friendly dates in JavaScript"

commit db7f5c78ac4f87ecc8c74e83fc37f504041004c0
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun May 24 12:04:10 2020 +0100

    Add a post "Showing human-friendly dates in JavaScript"

commit fddc063577a75df48e95d3de6f8c36d244920ae0
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.fastmail.co.uk>
Date:   Sun May 17 13:13:13 2020 +0000

    Publish new post sachsenhausen.md

commit 2b9859a82b6efb5a7416945524a347d9f6168373
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun May 17 14:10:59 2020 +0100

    Add a post about Sachsenhausen

commit e5e32c20c87a99313b16f2932b56804caffaa45f
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun May 17 08:32:58 2020 +0100

    Add an #id to update blocks

commit 95078b29fc23bd31e1a8862fb64fbe5d062ea3ea
Merge: aaaceaf2 06589263
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun May 17 08:28:05 2020 +0100

    Merge pull request #368 from alexwlchan/ao3-script-fixes

    Fix some bugs in my AO3 script

commit 06589263be742cd3f82c4e765fe461910de9fe4e
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun May 17 08:25:37 2020 +0100

    Make it brighter!

commit cf55f3e453a9496d314202e7513ac0c01cb99307
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun May 17 08:25:14 2020 +0100

    Tweak the update box for transparency and italics

commit ab0b6c5f51b9bd7c564c1e164134c77d1e0d9f51
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun May 17 08:23:40 2020 +0100

    Make some updates based on feedback

    * Selectively download by tag
    * Selectively download by format
    * Better error if that's not a Pinboard API token
    * Work around AO3's 500 error that isn't a 500

commit aaaceaf272ddad5eea1a974645eddde0b8586c3a
Merge: 9f7db549 34c47cd0
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Sat May 16 22:17:18 2020 +0000

    Merge pull request #367 from alexwlchan/scrub-tweet-icon-from-rss

    Scrub the blue bird from tweets from the RSS feed

commit 34c47cd0de3dd99e21e36f85d8674d4030b2e28e
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat May 16 23:13:49 2020 +0100

    Scrub the blue bird from tweets from the RSS feed

commit 9f7db549fb40fabac9d45c9500e73de1999963d7
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.fastmail.co.uk>
Date:   Sat May 16 09:43:01 2020 +0000

    Publish new post moving-messages-between-sqs-queues.md

commit 6e7f629c58170c259a6d626aad4d1d741d1ada6b
Merge: 88e61583 7e26dfbd
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Sat May 16 09:41:07 2020 +0000

    Merge pull request #365 from alexwlchan/add-sqs-redrive-script

    Post: "Moving messages between SQS queues"

commit 7e26dfbde43bbdad50cf4f6b11b32a69c0008f1c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat May 16 10:37:55 2020 +0100

    Post: "Moving messages between SQS queues"

commit 88e615830b84b9b59857b4173a9a499a08799550
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri May 15 20:00:14 2020 +0100

    Beware Liquid variable scoping!

    The `name` and `screen_name` variables would last outside the quoted
    block, and affect the URL to the tweet in the timestamp.

commit 3d71da7362044ae23738353380b943ca88341239
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.fastmail.co.uk>
Date:   Fri May 15 18:59:26 2020 +0000

    Publish new post downloading-the-ao3-fics-that-i-ve-saved-in-pinboard.md

commit 2e3211c78e436f68013ad4ed76e2f2e1d5985ade
Merge: d45c3aee 22a84077
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Fri May 15 18:57:37 2020 +0000

    Merge pull request #363 from alexwlchan/ao3-downloader

    Add a post about my AO3 downloader script

commit 22a8407741dbd12de07dcb731948d4f82e061c01
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri May 15 19:54:01 2020 +0100

    Finish my post about downloading AO3 fics from Pinboard

commit 2584e37eb9e0c951fc651ff815ff641fd77db4ef
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri May 15 19:16:35 2020 +0100

    Start writing about my AO3 script

commit eeaf97a19041aa71d350004f4e401565fda653d9
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri May 15 18:38:14 2020 +0100

    Add support for quote tweets in my Twitter plugin

commit d45c3aee8b8658f86143a4437610d6a794d41879
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.fastmail.co.uk>
Date:   Thu May 14 21:21:57 2020 +0000

    Publish new post letter-to-my-mp-about-liz-truss-and-medical-treatment-for-trans-youth.md

commit b34a9e10faf15ae5d4a64a56ae69e5fd96015b46
Merge: c26a895c 7a6a5175
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Thu May 14 21:20:01 2020 +0000

    Merge pull request #362 from alexwlchan/liz-truss

    Add the letter to my MP

commit 7a6a51753898515390b7367842c304a8698b6314
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu May 14 22:15:46 2020 +0100

    Add a note about address and phone number

commit 22b439e6b12d839196879937dd588f413a44e675
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu May 14 22:14:49 2020 +0100

    Add the letter to my MP

commit c26a895ceea06e3d8f41b8f14e6c1855193cc230
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.fastmail.co.uk>
Date:   Wed May 13 20:29:24 2020 +0000

    Publish new post social-media-as-a-growth-culture-for-opinions.md

commit f3c7ec5b9e2b6ff9833ab2f45f8b3e0189ddb69a
Merge: 36778001 870cab05
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Wed May 13 20:27:32 2020 +0000

    Merge pull request #361 from alexwlchan/social-media-opinions

    Social media as a growth culture for opinions

commit 870cab05d516633c5460bf2cec9452578e47c713
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed May 13 21:23:52 2020 +0100

    Final markups on the opinions post

commit 6b30b85f8b474649c08ad92cfc6231fe39edd082
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed May 13 21:10:16 2020 +0100

    Final markups on the social media post

commit a461d1bebe92164081828b236bef342c5d43c4e1
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed May 13 21:06:33 2020 +0100

    Cut, cut, cut.  200 words tighter on the social media + opinions post

commit b11db07a5782c152e9107e11d8859a7855c9f307
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed May 13 20:48:18 2020 +0100

    Initial draft of "social media + opinions"

commit 36778001da62b44747a5e853e234b0a2dbc4b0ba
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.fastmail.co.uk>
Date:   Tue May 12 06:57:54 2020 +0000

    Publish new post reflecting-on-bad-life-choices.md

commit 0f9157077dd14d8a48246f82aba7971ad09cd1b9
Merge: 8136fe87 6e842b5e
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Tue May 12 06:55:35 2020 +0000

    Merge pull request #360 from alexwlchan/reflection

    Add my post about terrible tuple unpacking

commit 6e842b5ec353af156c341fd0e740cc1fd54b2dd4
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue May 12 07:52:23 2020 +0100

    Remove some parentheses that were breaking link syntax

commit 5fcccf79cc87502ae7dc2885a4f6ca66608808ac
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue May 12 07:20:52 2020 +0100

    Finish markups on the reflections post

commit e2757fed82e7c0a2498c0f7ec7cbbf0237f1c42e
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue May 12 06:29:16 2020 +0100

    Make <pre> backgrounds transparent to let texture through

commit bdd278b7681d217ccccfcf370a85893a58beafe7
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue May 12 06:29:04 2020 +0100

    Add a "Truesday" date to the tuple unpacking post

commit fc1589254b0884b0d716ef568b3f156f11eb4bf1
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon May 11 19:13:32 2020 +0100

    bit more

commit 20c057463e99ea523b5f2cd0d2121dc94dfbf425
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon May 11 17:43:11 2020 +0100

    Add a couple of missing imports

commit 08054d576e6ff10df73bfce1891582cf68d96317
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon May 11 11:50:23 2020 +0100

    Add the image for the reflection post

commit add67b1c7d99a7a60b38bc59a7fc34de9f91be01
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun May 10 07:25:13 2020 +0100

    More markups on the reflection post

commit 303606a782742f161c24c3bbd4f75297f56e2a89
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat May 9 21:44:35 2020 +0100

    Finish another draft of the reflection post

commit 1e9eece222558efc53da28774977d32e2e26398f
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu May 7 07:32:42 2020 +0100

    Include the tweet metadata

commit 102ac1e80cddf2e05caee800b14699355c7494df
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu May 7 07:32:28 2020 +0100

    Include the photo link

commit ce02f66a3792d423b5bc8ac47e3f55b5d8102428
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu May 7 07:31:36 2020 +0100

    Start drafting the tuple unpacking post

commit 8136fe875d37ff7d2673d4494eb83844c51b7909
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.fastmail.co.uk>
Date:   Mon May 11 18:30:07 2020 +0000

    Publish new post the-friends-i-lost-along-the-way.md

commit 927c9502e8ada33c42a012fcb5cf906a4f518fec
Merge: a3e95d65 c2fe1889
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Mon May 11 18:28:01 2020 +0000

    Merge pull request #359 from alexwlchan/friends

    Post: "the friends I lost along the way"

commit c2fe1889d14bcf3e2e16f63184cbed2138019e84
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon May 11 19:24:17 2020 +0100

    A couple of markups

commit 8220111a947b889b978c2453d633e65048862193
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon May 11 19:19:50 2020 +0100

    First draft of "the friends I lost along the way"

commit a3e95d65f09a50b9d0a13ed45596dfad1fd960e7
Merge: 8399bd5e c9ea52fe
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Sun May 10 09:34:16 2020 +0000

    Merge pull request #358 from alexwlchan/remove-twitter-cards

    Remove Twitter cards from the site

commit c9ea52fe8083c3d5903b435669e40ec1986b734d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun May 10 10:30:46 2020 +0100

    Remove Twitter cards from the site

commit 8399bd5ebb0b6521634f03710434c9fb13c3841d
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.fastmail.co.uk>
Date:   Sun May 10 09:11:56 2020 +0000

    Publish new post make-it-safe-to-admit-mistakes.md

commit 8b6f37cd4a2b106d3f27d36ca663be55af9aa226
Merge: 7b76dbfa e74fd81c
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Sun May 10 09:10:03 2020 +0000

    Merge pull request #357 from alexwlchan/safe-apologies

    New post: "Make it safe to admit mistakes"

commit e74fd81cc220a9f3d61760a920397f16f621af86
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun May 10 10:06:48 2020 +0100

    Don't rely on the destination directory already existing

commit e3cf34b268e87b6b7a50a5a876dfcad7811378df
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun May 10 09:58:48 2020 +0100

    Markups on the mistakes post

commit 3addbf8d29cd433a380312e94a24e8a0df58d59e
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun May 10 08:33:59 2020 +0100

    Make it safe to admit mistakes

commit 7b76dbfaac02944daa418c32d61a6997c5d7200f
Merge: 6b3b654a ff32bfe6
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Sat May 2 19:33:48 2020 +0000

    Merge pull request #356 from alexwlchan/concurrent-futures-lists

    Explain how lists are special in the concurrent.futures post

commit ff32bfe60724a4af743bf6581e91cfac0c79632a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat May 2 20:29:56 2020 +0100

    Add an example of how to use the update plugin

commit bf41c9d7e91388d6767415e04dbcc677c999071c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat May 2 20:29:49 2020 +0100

    Add an update to the concurrent.futures post about lists

commit 6b3b654a9b363919ce95aa058b2bcc720c4528be
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat May 2 14:08:19 2020 +0100

    Tweak the display of the date on the stats page

    Omit the leading zero when displaying a single-digit day.

    Before: "As of 02 May 2020"
    After:  "As of 2 May 2020"

commit 4d4bf55a78f6f5c7fda047df3629c5a05ff58bb8
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.fastmail.co.uk>
Date:   Sat May 2 08:07:19 2020 +0000

    Publish new post how-long-is-my-data.md

commit 8ea2eb134310b0d617d8d0dd251ff0a8d08e59bb
Merge: df902225 477aa922
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Sat May 2 08:05:33 2020 +0000

    Merge pull request #355 from alexwlchan/how-long-is-my-data

    Add a link to my "How long is my data?" app

commit 477aa9227fb7f039217b5c282c7d5a4604d2978d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat May 2 08:36:14 2020 +0100

    Add alt text for Stuart's image

commit c4a056b61c1c3ef170a178ffff984765dff0eb41
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat May 2 08:34:28 2020 +0100

    Add an emoji floppy disk

commit eb7e95fc54b66dfb440b6f4a2e88823e6104c4d9
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat May 2 08:33:39 2020 +0100

    Add a link to my "How long is my data?" app

commit 942747f38bbb094a0bac2050bcf70781bae8e175
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat May 2 08:33:11 2020 +0100

    Fix a bug for saving images in the tweet plugin

commit df9022259afae277a57d7849c73229adf309027e
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.fastmail.co.uk>
Date:   Sat May 2 06:01:44 2020 +0000

    Publish new post give-your-audience-time-to-react.md

commit b4f9b35045761cb1893a2fd561a98cd9724a355e
Merge: 4aa4bb3c 0d9963a5
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Sat May 2 05:59:47 2020 +0000

    Merge pull request #354 from alexwlchan/let-your-audience-react

    Give your audience time to react

commit 0d9963a5229c76f67ef641f3386a1d29a9268667
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat May 2 06:56:20 2020 +0100

    Markups on the audience reaction post

commit 775a368e48345f7f5603bf21fe032c3a78ff183c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat May 2 06:53:57 2020 +0100

    First draft of running your rehearsal short

commit 4aa4bb3cdaea06274d39e3ce76df00e588578de0
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.fastmail.co.uk>
Date:   Fri May 1 15:56:05 2020 +0000

    Publish new post illustrating-lifecycle-transitions-in-amazon-s3.md

commit 3798097f4364d7f1169136ffc9d4ab2de4ce967e
Merge: 8a2e7696 fc9d34dc
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Fri May 1 15:54:16 2020 +0000

    Merge pull request #353 from alexwlchan/s3-lifecycle-transitions

    Add a post about illustrating things

commit fc9d34dc0b6847d67542451f2986813baafcd99b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri May 1 16:51:00 2020 +0100

    Move the footnote around to get a new commit

commit 137919899396c1b9938533297d2991e68d305c97
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri May 1 16:45:07 2020 +0100

    Tweak the line spacing in footnotes

commit bb559fb503dc830f148d4b3c83d7c3e7f520aa5b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri May 1 16:44:51 2020 +0100

    Add a post about illustrating bits of S3

commit 8a2e7696bf97e7dd0244b54584fbeac012f152ea
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.fastmail.co.uk>
Date:   Mon Apr 27 09:23:05 2020 +0000

    Publish new post using-dynamodb-as-a-calculator.md

commit a3eba77d82ae893912cb98c5321abef4eafec145
Merge: 222312eb 29e10089
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Apr 27 10:20:57 2020 +0100

    Merge pull request #352 from alexwlchan/dynamodb-wtf

    Pour fuel on the world fire with a DynamoDB-backed calculator

commit 29e10089ed2b5bfff08aa90f7a3d71c26a41985a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Apr 27 10:18:20 2020 +0100

    One more FAQ

commit 91571a8beabe4b1d58a352d389ed17a583af7dc1
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Apr 27 10:06:44 2020 +0100

    final markups

commit c09ec7e22338a214f89527f4b39d5df5e35e9335
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Apr 27 09:17:12 2020 +0100

    Tidy up the first draft

commit b6197218f443fecda626bb810b5d750bf183677f
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.fastmail.co.uk>
Date:   Sun Apr 26 17:53:54 2020 +0000

    First draft of my DynamoDB post

commit 222312eb8f1d642de4cab620c0cf3318456663b3
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.fastmail.co.uk>
Date:   Sun Apr 26 17:53:54 2020 +0000

    Publish new post exploring-an-unknown-sql-server.md

commit 11c3a14cd033d9944b0feb395e1b49e6d82043c0
Merge: 53732731 83b7ea82
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Sun Apr 26 17:52:07 2020 +0000

    Merge pull request #351 from alexwlchan/exploring-an-unknown-mysql-server

    Add a post about exploring an unknown SQL server

commit 83b7ea825ad63b059c511f5007ea710ce6918f23
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Apr 26 18:48:35 2020 +0100

    Add a post about exploring an unknown SQL server

commit 53732731bc4ea20e830c407350dc27fce388974c
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.fastmail.co.uk>
Date:   Wed Apr 22 18:19:41 2020 +0000

    Publish new post thinking-about-gender.md

commit b6471822257a9e3a0bfae44ba7d8f67d73adba7b
Merge: c8bdf28b 72f99f2c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Apr 22 19:17:58 2020 +0100

    Merge pull request #350 from alexwlchan/thinking-about-gender

    Add a post "Thinking about your gender"

commit 72f99f2cc8331dd97ebfe7f60962d3bb90a8a81a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Apr 22 19:15:25 2020 +0100

    Fix the link to last year's post

commit 4b94957ce2d771250feda0a4c0e5c94461c71894
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Apr 22 19:11:12 2020 +0100

    Link to the original thread

commit e869e714647dce77ab09de1cf7bdbbd33159f65a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Apr 22 19:10:31 2020 +0100

    Actually, revert to the old title

commit 067ffde086c80ba3f1fafac6f2ed4cf65d837c20
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Apr 22 19:08:54 2020 +0100

    Edit the post about thinking about gender

commit 2c415c70c9102982ff625d2fc0242279342825ef
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Apr 22 19:04:27 2020 +0100

    First draft of my post about gender

commit 482964d327f1c456de95ec62076fb13e5612035e
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Apr 21 18:22:00 2020 +0100

    add an outline for "thinking about gender"

commit c8bdf28b6609b50a4702c4b6400e12b56edf650b
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.fastmail.co.uk>
Date:   Sun Apr 19 18:32:48 2020 +0000

    Publish new post complex-failures.md

commit 627cc18215d05e2dfd9b36e7d66736b11a0dfd67
Merge: 430fff9c 043a2a12
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Sun Apr 19 18:30:57 2020 +0000

    Merge pull request #349 from alexwlchan/complex-failures

    Add a post about complex failures

commit 043a2a1284eeaa8a012373ec73c10ebabd64124e
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Apr 19 19:14:51 2020 +0100

    Add a post about complex failures

commit 430fff9c8285aba1b5954962e1afbea7ebebaf0a
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.fastmail.co.uk>
Date:   Sun Apr 19 12:43:44 2020 +0000

    Publish new post comparing-json-in-scala.md

commit cb1565414d96de0ae2a5bed0757a2cc479731a42
Merge: 86cf5cee 354c2e5f
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Sun Apr 19 12:41:57 2020 +0000

    Merge pull request #348 from alexwlchan/comparing-json-in-scala

    Add a post about comparing JSON in Scala

commit 354c2e5fcb042d03d2c6e31cd240d2de3ccc712a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Apr 19 13:38:42 2020 +0100

    Fix the title and description

commit 419d6b8c889b731be0ed039c15d0a79f23ff4e5b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Apr 19 13:36:38 2020 +0100

    Add a post about comparing JSON in Scala

commit 86cf5ceee939fb5082a96344bbf5b575807ff462
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.fastmail.co.uk>
Date:   Sat Apr 18 07:02:19 2020 +0000

    Publish new post survivors-guilt.md

commit 9c1db77e3191d609d492e7f8ee4870464bd15a5e
Merge: e0165d19 d9837dc2
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Sat Apr 18 07:00:27 2020 +0000

    Merge pull request #347 from alexwlchan/survivors-guilt

    Add a post about survivor's guilt

commit d9837dc21bf0afcc85946617241e54e00fb06a01
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Apr 18 07:57:10 2020 +0100

    Add a post about survivor's guilt

commit e0165d19c8d2f384cf1ffa299a536eecfa268fab
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.fastmail.co.uk>
Date:   Fri Apr 17 20:23:20 2020 +0000

    Publish new post getting-word-count-stats-for-my-blog.md

commit bb3d7e5550b0e7e37a7f8c4cc01145242eaa7eee
Merge: 8c0f57b3 d61b86b0
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Fri Apr 17 20:21:30 2020 +0000

    Merge pull request #346 from alexwlchan/word-counter-post

    Add a post about my new stats page

commit d61b86b0eb231372db6ce869218aa9bd118e6b6a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Apr 17 21:17:59 2020 +0100

    Add a post about my new stats page

commit 8c0f57b3f4e7d883e59a642a7ed7ebbf470b889e
Merge: 8ef8c979 1584844b
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Fri Apr 17 17:37:40 2020 +0000

    Merge pull request #345 from alexwlchan/blog-stats

    Add the total post count, the date, improve graph appearance

commit 1584844b371ff5e022e82d784d7e4a16ba5c35da
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Apr 17 15:58:07 2020 +0100

    Add the total post count, the date, improve graph appearance

commit 8ef8c979c8131521a45fb7cfc0df158d3e6035e1
Merge: 4e1763c3 4d1e0896
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Fri Apr 17 07:40:28 2020 +0000

    Merge pull request #344 from alexwlchan/word-counter

    Add all the pieces to display a word counter

commit 4d1e08961cb4c3e27673cd79403b2f0b757db1ef
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Apr 17 08:34:55 2020 +0100

    Add all the pieces to display a word counter

commit 4e1763c3b792220205ebeb7b3b8bce001a9d56e4
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.fastmail.co.uk>
Date:   Thu Apr 16 11:50:49 2020 +0000

    Publish new post adventures-in-embodiment.md

commit 36c541f4104745de03178b591215539d3eb2ecb8
Merge: f7fcf727 a6b73489
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Thu Apr 16 11:48:56 2020 +0000

    Merge pull request #343 from alexwlchan/embodiment

    Add a post about euphoria and embodiment

commit a6b73489a7c6ac9f997c33bd7d79829c430af3b9
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Apr 16 12:45:02 2020 +0100

    Add a post about euphoria and embodiment

commit f7fcf72780c2c8612e01689ec72d90a77a652f06
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Apr 16 07:09:48 2020 +0100

    Add a very subtle background texture

commit af5d79b4353ae3c429c05bbbbf1648c2baa556bc
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.fastmail.co.uk>
Date:   Wed Apr 15 18:54:03 2020 +0000

    Publish new post good-information-is-a-privilege.md

commit b48ec872fb4568fe45ed419b7a2a55b47221c94e
Merge: d919385d 2ea27864
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Wed Apr 15 18:52:16 2020 +0000

    Merge pull request #342 from alexwlchan/good-information

    Add post: "Access to information is a privilege"

commit 2ea27864a0c62d205cfb9475b16817a888bfd14b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Apr 15 19:48:23 2020 +0100

    Add post: "Access to information is a privilege"

commit d919385dc94a8aa3ad08494895125cf8c8e407ba
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.fastmail.co.uk>
Date:   Sun Apr 12 14:27:02 2020 +0000

    Publish new post downloading-files-with-python.md

commit 9e2922fb64f84dba23f2bc73fc483e251014ac6d
Merge: 56ed5727 de7c1df5
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Sun Apr 12 14:25:18 2020 +0000

    Merge pull request #341 from alexwlchan/downloading-files-with-python

    Add a post about downloading files with Python

commit de7c1df563c2ce3d2e4e1f2465f10b24fdbfff84
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Apr 12 15:21:40 2020 +0100

    Add a brief line about testing

commit ee93752853ebf44c8e00bc7e515b14b8e5dc6bd2
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Apr 12 15:19:35 2020 +0100

    Add a snippet for downloading files with Python

commit 56ed572741108e389e8abf306a7805b6ccfd537b
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.fastmail.co.uk>
Date:   Sun Apr 5 08:09:36 2020 +0000

    Publish new post storing-language-vocabulary-as-a-graph.md

commit 4b8349ed2df318e50d5b72379d61320632dcab53
Merge: 706f474a f8289aa0
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Sun Apr 5 08:07:50 2020 +0000

    Merge pull request #340 from alexwlchan/vocabulary-graphs

    Add a post about vocabulary graphs

commit f8289aa0a734812ab809396bad692393189f0cf2
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Apr 5 09:04:35 2020 +0100

    Put the alt text attribute on the right image

commit 1bea6703eefaaa02062fadbed7bbfc8b1b432014
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Apr 5 08:39:52 2020 +0100

    Add a post about storing language vocab as a graph

commit ce5941106a552cebf9e6960e110b699e9bd1e4d6
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Apr 4 23:03:43 2020 +0100

    Remove an unused CSS rule

commit 706f474aebfdcd06b90f096e350fb0f0210d17d7
Merge: bf9c073a 098e99e3
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Apr 4 18:39:45 2020 +0100

    Merge pull request #339 from alexwlchan/smaller-profile-image

    Optimise the size of this JPEG; save 30KB

commit 098e99e3f97337ece5df17b6e49ece071e37ba07
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Apr 4 18:32:19 2020 +0100

    Optimise the size of this JPEG; save 30KB

commit bf9c073a3fc3b151b527b5c1f34f7ce1f30e0728
Merge: 3f9e371a f3d8f7a2
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Sat Apr 4 17:32:12 2020 +0000

    Merge pull request #338 from alexwlchan/allow-inline-svg

    Allow inlining SVGs for performance, and with accessibility support too

commit f3d8f7a2699ffe0584b58e6a9d7d8bc2b6eb557c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Apr 4 18:28:39 2020 +0100

    When I made the font size bigger, I should have bumped the width

commit 83f419f1a1025c047854ef07be3ba390a9d328c1
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Apr 4 18:28:30 2020 +0100

    Add a plugin for inlining SVGs with a11y support

commit 3f9e371ad7efec42cbbebebac3ad09abdb6a9c84
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.fastmail.co.uk>
Date:   Wed Mar 25 13:03:11 2020 +0000

    Publish new post inclusion-cant-be-an-afterthought.md

commit 32f1f474f10c8cb06238a13e757bdd67b9a6c055
Merge: 2ef80554 5b7ea730
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Mar 25 13:01:16 2020 +0000

    Merge pull request #337 from alexwlchan/unconscious-bias

    Add notes for "inclusion can't be an afterthought"

commit 5b7ea7301625689f35062c42aabb6cf1737a2e2e
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Mar 25 12:57:57 2020 +0000

    Check in the slides as well!

commit 6cba458a09f127568b0d19d31d299305bfcdde19
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Mar 25 12:52:52 2020 +0000

    Add theme-appropriate favicons

commit c8cddf35cee61e24390f3a0865da7d80633fcfe3
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Mar 25 11:18:56 2020 +0000

    Add the pre-built Specktre assets

commit 63c96e8f09899be60f670c51d63f042dce7d998c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Mar 25 09:20:09 2020 +0000

    Add notes for "inclusion can't be an afterthought"

commit 2ef805548f9b2eb2c7d8f984bb938ec67c74014a
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.fastmail.co.uk>
Date:   Sun Mar 15 08:30:19 2020 +0000

    Publish new post rich-enough-to-make-bad-choices.md

commit 4235c9a1557200ffd083a6b26809858f9c997d60
Merge: b082ced8 c0fc27fb
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Sun Mar 15 08:28:32 2020 +0000

    Merge pull request #336 from alexwlchan/boot-making-startups

    Add a post "Rich enough to make bad choices"

commit c0fc27fbb2167d49e2737306a68311d1b609638a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Mar 15 08:25:26 2020 +0000

    Increasing the font size makes things better

commit 0b28eaf99062b32dcf2dbbca5ad2403347cfbf43
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Mar 15 08:25:05 2020 +0000

    Add a post "Rich enough to make bad choices"

commit b082ced846a018512274ba29455e578f383b6c34
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Mar 14 11:30:05 2020 +0000

    Use a less Voldemort-y title

commit d418e7c29f27ab29b2f2d83a889983798f4ef4f6
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Mar 14 10:15:06 2020 +0000

    Revert "Hack in something to make Twitter cards work"

    This reverts commit 33ceb94cf1edcc9e01c027af5b3753b4a708c77f.

commit be7ae0d847d44a93caf97ee501154e345ddda793
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Mar 14 10:14:59 2020 +0000

    Revert "Use liquid comments, not jinja2 comments"

    This reverts commit 813581b948f32f5d64bf8d53baf145a0080cee27.

commit b6eee11b72af7ebb8d68ca850aa0e5e80058f3ff
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Mar 14 10:10:45 2020 +0000

    Use liquid comments, not jinja2 comments

commit 9e5d3af92b58dcc465caf73196de82a26c875f65
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Mar 14 10:03:29 2020 +0000

    Hack in something to make Twitter cards work

commit b830d79ee5f38ce2dc1ce0c1c2d4c4fef15d6e6c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Mar 14 09:39:28 2020 +0000

    Completely new image URL

    Maybe Twitter's card logic is caching the 404 I returned for a while?

commit 2f2ea2fca72640d9fda506de5253715cf9d7f688
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Mar 14 09:36:17 2020 +0000

    try resizing the profile to 500x500, does this make twitter happy?

commit 587b390914baa6c52a8fe024063bb9ca73471523
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.fastmail.co.uk>
Date:   Sat Mar 14 09:27:10 2020 +0000

    Publish new post sick-leave.md

commit 460cfe8a7fc4efd52e2f8b97cfa33edeaccc753f
Merge: 5796059f 3b6aa363
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Sat Mar 14 09:25:24 2020 +0000

    Merge pull request #335 from alexwlchan/sick-leave

    Add a post about sick leave in a COVID-19 world

commit 3b6aa363e4dd307d25f0a0ef648d1cf3d0634f1c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Mar 14 09:21:56 2020 +0000

    Add a post about sick leave in a COVID-19 world

commit 5796059f4708e5cc326fab4dbe12f1eb65fa4d6b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Mar 14 07:48:38 2020 +0000

    Add a JPEG copy of my profile image

commit 7feac41cf8a6f331c8acf1fd4a0527671d78e9a4
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.fastmail.co.uk>
Date:   Sun Mar 8 10:13:19 2020 +0000

    Publish new post stripey-flag-wallpapers.md

commit ff28dba1466a05fb3c11007d9370aab0f86c0100
Merge: c2a5f7b3 3a1baa97
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Sun Mar 8 10:11:29 2020 +0000

    Merge pull request #334 from alexwlchan/horizontal-flags

    Add a post about my striped flag wallpapers

commit 3a1baa9722d6dfa880c8a075dc030266b366146c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Mar 8 10:07:50 2020 +0000

    Add a post about my striped flag wallpapers

commit c2a5f7b3ae8f927b68422a37c05100bb1b28a8ab
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.fastmail.co.uk>
Date:   Wed Mar 4 09:42:36 2020 +0000

    Publish new post adding-non-breaking-spaces-with-jekyll.md

commit 573180e2082010700e9021dccd23d07227e6b683
Merge: 6be6ab16 a0091027
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Wed Mar 4 09:40:42 2020 +0000

    Merge pull request #333 from alexwlchan/non-breaking-jekyll

    Add a post about non-breaking spaces in Jekyll

commit a0091027de84bc90c9147a5b4b7bfed29ad1bacf
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Mar 4 09:36:23 2020 +0000

    Add a post about non-breaking spaces in Jekyll

commit 9a3ffac570a6b95f490f770dd9660d3cfeb3978c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Mar 4 09:03:50 2020 +0000

    Add some more text about responsive design

commit f8bc18bff9e7bc13de7c31d1028a507123ad9abd
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Mar 4 09:00:05 2020 +0000

    Start a post about non-breaking spaces with Jekyll

commit 6be6ab163ba734bc7c6e1e7c5ed7b962d7fe8993
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.fastmail.co.uk>
Date:   Mon Mar 2 07:48:10 2020 +0000

    Publish new post finding-the-size-of-your-s3-buckets.md

commit 6628f3fb568bfe8c8f03a3893507a707c5d6803a
Merge: bbeb069d a3ff186e
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Mon Mar 2 07:46:25 2020 +0000

    Merge pull request #332 from alexwlchan/measuring-s3-bucket-size

    Link to my script for searching S3 buckets

commit a3ff186ec0e9e3f280a33450b6b7a788ff58497a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Mar 2 07:43:29 2020 +0000

    Add missing alt text for the cops-with-guns photo

commit 109c2e31dd6bc66ea66bf53687f23e16dffb235b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Mar 2 07:38:08 2020 +0000

    Better title on the S3 post

commit f689177adb1ae28a419a1356b40fc3176c8d712b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Mar 2 07:37:50 2020 +0000

    Link to my script about searching S3 buckets

commit bbeb069d1dbefb0a1c7fb8819ce9ad3ae5666f7b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Feb 28 11:29:53 2020 +0000

    Add a missing ? mark

commit aa8962aa5807766c9b07309183b30eada0a8bee8
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Feb 28 11:21:24 2020 +0000

    Fix display of single-image tweets

commit 348c5bf1cf79b00ecb112aaa4663f2e701ae2e6c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Feb 25 13:00:05 2020 +0000

    don't let a word trail onto the next line

commit 89a51649f7cda3495751fe504ef3bb737deb5915
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.fastmail.co.uk>
Date:   Tue Feb 25 12:13:12 2020 +0000

    Publish new post a-remote-controlled-oven-is-a-safety-nightmare.md

commit 94e9c3c7825982103d337f62a89b198c922215b2
Merge: a5cf28b0 228fb13b
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Tue Feb 25 12:11:25 2020 +0000

    Merge pull request #331 from alexwlchan/monzo-oven

    Write a bit about the Monzo oven

commit 228fb13b10c8ca64a579eacda272004a4488a7f7
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Feb 25 12:02:00 2020 +0000

    one more fix

commit 07a4a3091e8d0ee235d596ac27cc0c62c40dda06
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Feb 25 11:56:36 2020 +0000

    markups on the mozno post

commit ea91ff4d7b7592c145f547a6d91308743e3fc62d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Feb 25 11:38:44 2020 +0000

    markups on the monzo oven

commit 18086ff0f9d5d8333f076b1a8d4250a859fec8e7
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Feb 24 21:37:38 2020 +0000

    markups on the monzo oven thing

commit 5c07ce68d7967b771693076537161a68d1960470
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Feb 24 20:43:03 2020 +0000

    First draft of a post about the Monzo oven

commit a5cf28b04212d45dad748f1a4125a2d469dfe1b0
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.fastmail.co.uk>
Date:   Sun Feb 23 20:58:34 2020 +0000

    Publish new post adjusting-the-dominant-colour-of-an-image.md

commit ebde1771bfbf180dadac37d80a534219c7f53bcb
Merge: b71b810c 9cf59426
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Sun Feb 23 20:56:50 2020 +0000

    Merge pull request #330 from alexwlchan/hue-adjust

    [post] Adjusting the dominant colour of an image

commit 9cf59426119ef677d1416062a752cf158c31860a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Feb 23 20:53:16 2020 +0000

    [post] Adjusting the dominant colour of an image

commit b71b810ced92bba3b489e7c2e665294ac6a559bc
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Feb 21 15:04:13 2020 +0000

    Fix the link to the profile image

commit 7ea11450b608820d560030580d95d679e0d163df
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.fastmail.co.uk>
Date:   Tue Feb 18 08:09:37 2020 +0000

    Publish new post versioning-a-bagit-bag.md

commit 17eff6a50c39b65dfcf5af858f79b17124edc84d
Merge: ec0c3b0c cc8a7fd0
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Tue Feb 18 08:07:45 2020 +0000

    Merge pull request #329 from alexwlchan/bagit-versioning

    Link to my post about BagIt versioning

commit cc8a7fd0d66ebe86eb5b68cfb11aa4e27099dc98
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Feb 18 08:00:26 2020 +0000

    Link to my post about BagIt versioning

commit ec0c3b0cc7222737d1222e1aac17eb4501653b13
Merge: a0a97d8e c4601a55
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Tue Feb 18 07:51:08 2020 +0000

    Merge pull request #328 from alexwlchan/add-category-list

    List all the categories on the "all posts" page

commit c4601a555bc2e98efe3778713cd254cb8b7618a8
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Feb 18 07:47:40 2020 +0000

    Rename the "Wellcome Collection" category to "Digital Preservation"

commit 0655714d58fc63edcb11f9753ffa90e199ffb52c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Feb 18 07:47:28 2020 +0000

    Put a list of all the categories on the "all posts" page

commit a0a97d8eddd2d598aea015d5509a1d83e8a839e2
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Feb 16 07:11:23 2020 +0000

    Add a moment I'd forgotten about

commit bdb2812183c6c8bf0dc60cf9df50daf7d7d3cafc
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Feb 15 23:14:22 2020 +0000

    Remove an unwanted post

commit 873a64c36f43c2550f66bfddbeb60dac6b9f1806
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Feb 15 23:14:04 2020 +0000

    Add a new Skeletor clip loop

commit f8e3c0c53ec39c4f672341de68a3865b86ebc968
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Feb 9 22:54:00 2020 +0000

    Swap out my profile image

commit d22d27aeed2b46be47641a0ecf47e737395bdb6d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Feb 8 20:10:17 2020 +0000

    That should be a break, not a continue

commit 903a0c04b8ceb749b6ab69c31232048b6179044a
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.fastmail.co.uk>
Date:   Thu Feb 6 21:27:03 2020 +0000

    Publish new post archival-storage-service.md

commit e49858e07526bb336e48093f4d2b7e3489364763
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Feb 6 21:24:55 2020 +0000

    Link to my article about the archival storage service

commit 28a7b2447e12dfa118af662e41085073b38221e8
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Feb 3 17:03:14 2020 +0000

    Fix a typo in 2019-09-12-streaming-large-s3-objects

commit 762f4b232ca91c9f9545f526ec1b223073974810
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.fastmail.co.uk>
Date:   Wed Jan 29 09:44:49 2020 +0000

    Publish new post excluding-lots-of-folders-in-backblaze.md

commit 620bbbf77626144b3aedff412afbd86a495ea349
Merge: 1fd8bfbc 0f838c8a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Jan 29 10:42:51 2020 +0100

    Merge pull request #327 from alexwlchan/bulk-backblaze-exclusions

    Add a post about excluding folders in Backblaze

commit 0f838c8af5079735bb2e55fad0c53772069bf401
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Jan 29 09:39:59 2020 +0000

    Remember to check in the {% details %} plugin source

commit ceead795029eb05d30032a6355c0d2aacd702cd2
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Jan 29 09:29:07 2020 +0000

    Add a post about excluding folders in Backblaze

commit 1fd8bfbca31b1be3bd39ac64d634556c7a719fbb
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.fastmail.co.uk>
Date:   Wed Jan 22 08:23:51 2020 +0000

    Publish new post deletion-canary.md

commit 3288cf8ebf9b909f85d8fc604c6abba1b831f7dd
Merge: 7451836a 986ec3bc
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Jan 22 08:21:46 2020 +0000

    Merge pull request #326 from alexwlchan/deletion-canary

    Add a post about delete canaries

commit 986ec3bc563b9e6d4c3bbb1a274945080a47c279
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Jan 22 08:17:21 2020 +0000

    Add a post about delete canaries

commit 7451836a929ede3f904db0d75d41d2539cacf025
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.fastmail.co.uk>
Date:   Wed Jan 22 07:50:24 2020 +0000

    Publish new post uk-stations-map.md

commit 6253a3e70ea8c8c691c7855c3d4bc306e44d21ba
Merge: 6d1ec9af 433475fb
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Wed Jan 22 07:48:26 2020 +0000

    Merge pull request #325 from alexwlchan/uk-stations-map

    Link to my UK stations map fun app

commit 433475fbbcb5aa27aa770a022a77212aa9a251de
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Jan 22 07:40:56 2020 +0000

    Link to my UK stations map fun app

commit 6d1ec9afd3db72509e4bcf563b3d60d8322dc483
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.fastmail.co.uk>
Date:   Sun Jan 19 10:32:59 2020 +0000

    Publish new post tex-dockerfile.md

commit 3d3d832bc6610c8ec0a3f5f9134773e2c2e79b98
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jan 19 10:30:47 2020 +0000

    Link to my Docker image for running LaTeX

    + handle "TeX" as a special-cased appearance

commit e70d7094693b17e02c02351e5b4b0e874046d51c
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.fastmail.co.uk>
Date:   Thu Jan 16 22:56:51 2020 +0000

    Publish new post pride-valknuts.md

commit 2c2bc36246d45718c14ce6ff78f27daff3b313f1
Merge: 005ee949 07f870d3
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Thu Jan 16 22:54:58 2020 +0000

    Merge pull request #324 from alexwlchan/pride-valknuts

    Add a link to my Pride valknuts Glitch app

commit 07f870d389425cb5de1d4f24b245fa740baa5c9e
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Jan 16 22:51:02 2020 +0000

    Add a link to my Pride valknuts Glitch app

commit 005ee9490e2733fcc3e2110ac9686e1f56e5b59d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jan 10 20:18:06 2020 +0000

    Tweak this variable name to match the text

commit 756b89944b198b74bf87495d47a6316f5658ac57
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.fastmail.co.uk>
Date:   Sat Jan 4 10:03:53 2020 +0000

    Publish new post finding-the-bottlenecks-in-an-ecs-cluster.md

commit e61d7801a210496220bfda52821b2a6dbe2a4cd5
Merge: 146c6139 1720b227
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Sat Jan 4 10:01:57 2020 +0000

    Merge pull request #323 from alexwlchan/cluster-stats

    Add a post about finding CPU/memory bottlenecks in ECS

commit 1720b22710d9628401aed42621a787ea8ebc2861
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Jan 4 09:57:51 2020 +0000

    Finish this post, add alt text and final markups

commit cdec77f1a5283a305c75921825e87e6ec3908b17
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Jan 4 09:50:15 2020 +0000

    Copy edits for "finding bottlenecks in an ECS cluster"

commit e69ee7baeba30f9fb95dd930edea4b9e2e4cb515
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jan 3 21:26:20 2020 +0000

    First draft of the post about CPU/memory bottlenecks in ECS

commit 239577a1cd6e078b68af8163199bae7163e53d11
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jan 3 17:04:14 2020 +0000

    Start writing a post about finding the bottlenecks in an ECS cluster

commit 146c61391d93f817902ffd08fbdd4352ae2b811c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Dec 15 20:34:00 2019 +0000

    Add another charity to the list

commit 9c00320589f9439b1fd35bfc2127502f9b2d3cc5
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.fastmail.co.uk>
Date:   Wed Dec 11 08:52:40 2019 +0000

    Publish new post yaml-impossible.md

commit e4b2dc5105cd2e26a7ae951ab4c0a7ced06f38d7
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Dec 11 08:50:05 2019 +0000

    Ensure hearts always align to the top

commit 91a4d6060b4de207c3fb432814dd1395c37402dc
Merge: d939ae71 02581c3a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Dec 11 08:49:35 2019 +0000

    Merge pull request #322 from alexwlchan/self-destruct

    Add a post about self-destructing YAML

commit 02581c3a4a112345d28d71c4ea8f2a224873caab
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Dec 11 08:42:08 2019 +0000

    Use the tape recorder in social media previews

commit 56446c8b975e38e750d62f7f493d1c084cf0fb0c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Dec 11 08:38:50 2019 +0000

    Finish edits on "YAML impossible"

commit 3b3b71670a8e08f0f2dc40b907988c65b138b6dc
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Dec 11 08:19:38 2019 +0000

    Add a first draft of a post about self-exploding YAML

commit d939ae71e475a40fc1d408fdec6f0d632a665948
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Dec 9 19:15:58 2019 +0000

    Tweak the appearance of dates in a post list

commit a296751a130886c5ebcaf55520489904080cf83d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Dec 6 09:22:30 2019 +0000

    Revert "Revert "Use a profile picture that matches the site""

    f2373d7d4c19c498bdec1836eea01a7883c42d0d

commit 494046a3370555d2287e94ad928f47233ee144dc
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Dec 6 09:20:50 2019 +0000

    Revert "Use a profile picture that matches the site"

    4aff921318add6dbbd78e64c73e346fbad34ab6b

commit 207892114d9f9677b6a2a9836d6bda1dda78e9c7
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Dec 6 09:12:49 2019 +0000

    Add Twitter to the header bar

commit 87c8b7db9b3a9f62210f9f1c516452c5abf3f082
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Dec 6 09:11:53 2019 +0000

    Use a profile picture that matches the site

commit e27f7429739b46fa816147c65edfd7acce9bb84f
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.fastmail.co.uk>
Date:   Fri Dec 6 09:02:20 2019 +0000

    Publish new post spreadsheet-functions.md

commit 8f5976418b003eeea97cc3dc241d4898033d961c
Merge: b710a42f d3ce1612
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Dec 6 08:59:48 2019 +0000

    Merge pull request #321 from alexwlchan/spreadsheet-functions

    Add a post about spreadsheet functions

commit d3ce161217531582a95e2e297b3b4329b0d7c70b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Dec 6 08:43:31 2019 +0000

    Add a post about spreadsheet functions

commit b710a42fe5129109a65048b010984adf62d958ea
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Dec 3 08:33:49 2019 +0000

    Recategorise some posts; add some tools to do so

commit 59326fa9dd2bb3a9172ab763b784e9ad6d596288
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Dec 2 23:41:50 2019 +0000

    Add a missing date

commit 64b00a32c1b579ecc6b53a5c701e8c61653b0a4e
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Dec 3 08:27:18 2019 +0000

    Add a note about theme.minipost excluding from the front page

commit 3f4ae809a390bad182533190ff4cb952c0c774c8
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.fastmail.co.uk>
Date:   Mon Dec 2 23:21:41 2019 +0000

    Publish new post november-scripts.md

commit cb76fd6364c6dc9e341a41ed462de13f7d6ade1a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Dec 2 23:19:15 2019 +0000

    Clarify multi-pronoun

commit 2e98081b796fa02e1817ac7ea7b49c85403b8202
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Dec 2 23:17:50 2019 +0000

    Add a post of "November scripts"

commit ec2ab0f4dec3de34f1c34b7659b738fcb92348b3
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.fastmail.co.uk>
Date:   Wed Nov 27 12:43:44 2019 +0000

    Publish new post my-scanning-setup.md

commit 96cca40bee4a1552a2272a809c350ec31e50dd25
Merge: 4fd5630b 9d59890b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Nov 27 12:41:12 2019 +0000

    Merge pull request #320 from alexwlchan/scanning

    Add post about my scanning setup

commit 9d59890b0ee97fc9b14ca6313acdc39759133c11
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Nov 27 12:36:01 2019 +0000

    restore accidentally deleted image

commit 9a1a007f33ace511c7cd911322b05063c2d23133
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Nov 27 11:28:35 2019 +0000

    Finish drafting the scanning post

commit ba12852d8802c9b8b9ffe97e2aa542a3d51a243c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Nov 26 22:49:45 2019 +0000

    A complete rewrite to simplify the post

    In particular cutting a bunch of stuff about directories/hierarchies,
    and being more ruthless with editing/quotes.

commit cf4e97c0c7242f5f858a5bdfd8c68328a9c28fe9
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Nov 25 20:19:04 2019 +0000

    Tweak some of the wording

commit d1e19f415df15380923cdaf6a8445f591ab0301a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Nov 25 09:15:59 2019 +0000

    Some more notes on scanning

commit df6bf6a2d2ecfe218713db43490246756a0e81cd
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Nov 25 08:20:04 2019 +0000

    Add some screenshots from docstore

commit 5acbe240bc9205037983e29b4af66bbf3e3990f1
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Nov 24 23:44:21 2019 +0000

    Add some more about search/tagging

commit c3a407339503ac6fae4f2424f6a0e6be69809ee7
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Nov 24 21:05:53 2019 +0000

    Tighten up the first section

commit 2465581aab7b47bc8441210076686d5c2c541f67
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Nov 24 21:01:25 2019 +0000

    Turning paper into PDFs

commit 6405828ee7c3edb3912e5a4ceac35a024e332b49
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Nov 24 20:17:52 2019 +0000

    Add the initial outline of a scanning setup post

commit 4fd5630b2f98e987a2c9a5e87a063ff75ace4804
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.fastmail.co.uk>
Date:   Sun Nov 17 11:38:06 2019 +0000

    Publish new post saving-a-copy-of-a-tweet-by-typing-twurl.md

commit 61e4df14b1ae79b14dad6f6e9fab6706f4ffdec5
Merge: 6a431971 6bbcc43a
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Sun Nov 17 11:35:42 2019 +0000

    Merge pull request #318 from alexwlchan/markdown-tweets

    Add a post about saving tweets with ;twurl

commit 6bbcc43a3b3208d7c33dab6e10a35bf89ef83041
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Nov 17 11:20:49 2019 +0000

    Add a post about saving tweets with ;twurl

commit 6a4319719c9b56eae03c0d0420661e9824937a31
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Nov 8 08:32:50 2019 +0000

    Tweak the appearance of blockquotes to match code

commit 3f0851b8349c5c5495c35dc237b9076383dcf422
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.fastmail.co.uk>
Date:   Fri Nov 8 08:29:51 2019 +0000

    Publish new post fixing-terraform-module-sources.md

commit 0cda1345d520c5634e8d2daafbc3827fd15972d7
Merge: 3c6fcbe6 ca489d3d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Nov 8 08:27:19 2019 +0000

    Merge pull request #317 from alexwlchan/fixing-tf-paths

    Add a post about fixing TF module sources

commit ca489d3d67ff808d117b4655993aae0b83f7c348
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Nov 8 08:23:55 2019 +0000

    Add missing parenthetical

commit 83832b1ebadf086a7e787ab33cb152510bc73058
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Nov 8 08:23:04 2019 +0000

    Add a post about fixing TF module sources

commit 3c6fcbe6f7c51c25647618e15fe230f3690fcb0f
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.fastmail.co.uk>
Date:   Wed Nov 6 07:54:28 2019 +0000

    Publish new post aws-costs-graph.md

commit 87e8828215279536e5a2246bfacc7ba9bdf34d64
Merge: 72384105 d8202666
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Wed Nov 6 07:52:00 2019 +0000

    Merge pull request #316 from alexwlchan/aws-costs

    Add a quick post about my AWS costs graph

commit d8202666ed43a019ed4970b86687f476307d04fa
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Nov 6 07:47:40 2019 +0000

    Add a quick post about my AWS costs graph

commit 723841051b7a8501cb33e982bd96cf23684c2604
Merge: 2af45b18 d90edaf8
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Sun Nov 3 17:39:05 2019 +0000

    Merge pull request #315 from alexwlchan/better-categories

    Rejig a couple of categories

commit d90edaf83bad9f527f8bd75081b5fceb675c3c9a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Nov 3 17:32:28 2019 +0000

    Rejig a couple of categories

commit 2af45b1873ec9520293281d2915e1a555e570f69
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.fastmail.co.uk>
Date:   Tue Oct 22 22:00:14 2019 +0000

    Publish new post digital-preservation-at-wellcome-collection.md

commit 8f8b99b23908fc252c341cb42b73d3f8b5e6544a
Merge: 7cc92dec 8ec1ca79
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Tue Oct 22 21:57:47 2019 +0000

    Merge pull request #313 from alexwlchan/stacks-post

    Link to my digital preservation post; add more to my talks page

commit 8ec1ca79f74959da2aac4d0a09140e2780bd1ecd
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Oct 22 22:53:32 2019 +0100

    Make linting a distinct step in azure-pipelines

commit b2f1c8be4fc112fea90d3bc6ff6cbea39057f800
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Oct 22 22:53:23 2019 +0100

    Add alt text to pyconuk-speaking.jpg

commit d5550edf9add31b81dcd60e6165235ec955bd879
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Oct 22 22:29:44 2019 +0100

    Bulk up the talk page, add a photo

    (You can see my heels in this photo, it's gr8)

commit 514806cd33d68928972553e4c04d191891b12294
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Oct 22 22:25:34 2019 +0100

    Link to my digital preservation post

commit 7cc92dec15236fc5fd5108949904172535017d51
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Oct 21 09:50:02 2019 +0100

    Add slides for the GLAM Digital Lunch event

commit 53fd65353afcc2901e2088176cf4353e2d87a326
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.fastmail.co.uk>
Date:   Wed Oct 16 21:24:21 2019 +0000

    Publish new post adventures-with-concurrent-futures.md

commit 5b52bc33ad8312eb7487bec3a7fcd2f4da778940
Merge: 0a3d6286 0c35835a
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Wed Oct 16 21:21:57 2019 +0000

    Merge pull request #311 from alexwlchan/concurrent-futures

    Write up some of my notes on concurrent.futures

commit 0c35835ab15a395ba142b090fb1872b43a5a839d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Oct 16 22:14:57 2019 +0100

    Finish my concurrent.futures post

commit e7ff9811ca1e06534db545de01b70f8dc661fed6
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Oct 16 20:54:34 2019 +0100

    Finish the first draft of the concurrent.futures post

commit c67d1e9825b4e7099d9af16f42eb8561ec33c5b8
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Oct 16 08:49:27 2019 +0100

    Hey look, a diagram emerges!

commit 95323010eed93f7dda867116b1684d11da2caef8
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Oct 15 22:27:53 2019 +0100

    Start writing about concurrent.futures

commit 0a3d62861264e55c7b850e9950018bfe713de924
Merge: 592a8e35 e19e97b3
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Tue Oct 15 20:42:58 2019 +0000

    Merge pull request #310 from alexwlchan/highlight-talks

    Improve the text on the homepage

commit e19e97b310a10b37a18c35cbec3cbb67b1e7120a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Oct 15 21:18:34 2019 +0100

    Push the "say thanks" page a little harder

commit 5734b49367ffaa87f7e9c21cbbee823e8afbea19
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Oct 15 21:18:24 2019 +0100

    Tweak the homepage to link to my talks

commit 592a8e358f05db85715348d23f2eafc91fcefba5
Merge: ea2dd707 d0aa9ad0
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Tue Oct 15 20:08:25 2019 +0000

    Merge pull request #309 from alexwlchan/tidy-all-posts

    Tweak the appearance of the "all posts" page

commit d0aa9ad012dd2d66048c2566efd35b790207a9d0
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Oct 15 13:11:27 2019 +0100

    Tweak the appearance of the "all posts" page

    * The most recent 10 posts use DD/MM dates (1 Sep, 2 Oct, 3 Nov) rather
      then MM/YY (Sep 2019, Oct 2019)
    * There's a grey diamond between the most recent 10 and the category
      list

commit ea2dd7074a95c38dfbb47d6066f14b2c4f90b8fa
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Oct 14 20:00:10 2019 +0100

    Link to my notes for sans I/O programming

commit 28f330dbf0355579afbeb6cb919d3937c3a749b9
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.fastmail.co.uk>
Date:   Mon Oct 14 17:33:10 2019 +0000

    Publish new post sans-io-programming.md

commit 11da8291fe95b382bd3e89f48a7b301f37b2fed3
Merge: a48eeffa 92cc3e39
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Mon Oct 14 17:31:19 2019 +0000

    Merge pull request #308 from alexwlchan/sans-io

    Post my notes on sans I/O programming from PyCon UK

commit 92cc3e399afc48544802f0f48ad216837eb5e657
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Oct 14 18:27:53 2019 +0100

    Add two missing favicons

commit ca89f05d9c690be54f17d6000861fa918a23b3e0
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Oct 14 18:22:40 2019 +0100

    Tweak the URL slug for sans I/O programming

commit b75171c0ce816680a65f8cd7e42ae4e375a9cc84
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Oct 14 18:22:03 2019 +0100

    Add a summary to the sans I/O talk notes

commit 11ea59474983bc813c27d600f4d4e3f86b3f11ed
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Oct 14 18:15:17 2019 +0100

    Tidy up the sans I/O programming post a bit

commit 14792e4a511a6edf48e64ae75ed81ac5c1c6c60a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Oct 14 18:01:21 2019 +0100

    Add all the slides for sans-io programming

commit ade476857fe85e6ab81ed83a17cb79e88defaa0a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Oct 14 15:51:07 2019 +0100

    First draft of sans I/O programming, sans slides

commit 50598781872fa20a757e823b3df1ef2b7814c620
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Oct 14 10:07:10 2019 +0100

    Add a shortcut for opening the latest draft

commit 87b7aecfc8e4935ecffb0337d1f42f93dc61691e
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Oct 14 09:07:44 2019 +0100

    Start adding notes on sans I/O programming

commit a48eeffaa54cb40935d0eed34666469fe4c1ab0e
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.fastmail.co.uk>
Date:   Fri Oct 11 20:34:14 2019 +0000

    Publish new post religious-holidays.md

commit ff8a225eca18491e9e0ccad1491419329a49306c
Merge: 7378fd97 bfec6de1
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Fri Oct 11 20:32:25 2019 +0000

    Merge pull request #307 from alexwlchan/religious-holidays

    Add a quick post about religious holidays

commit bfec6de108628b97f3d00d41329959251d886b92
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Oct 11 21:29:00 2019 +0100

    Add a quick post about religious holidays

commit 7378fd97daef40ed4723947393c469743d523e23
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.fastmail.co.uk>
Date:   Sun Oct 6 17:32:56 2019 +0000

    Publish new post rough-edges-of-filecmp.md

commit bd1d068b21793d5164039c18ad3e608658b65e6e
Merge: b89254c5 c7c9db2d
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Sun Oct 6 17:30:35 2019 +0000

    Merge pull request #306 from alexwlchan/rough-edges-filecmp

    Add a post about the rough edges of filecmp

commit c7c9db2d755dc6fc506a22c23cf989a46163cc18
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Oct 6 18:26:17 2019 +0100

    Finish the "rough edges of filecmp" post

commit 32ae4e0062d7c696796257babe6184955835d324
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Oct 6 09:39:03 2019 +0100

    Start writing about the rough edges of filecmp

commit b89254c56778d40fa9dc7c7e3617ea28ff5f4484
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.fastmail.co.uk>
Date:   Sat Sep 28 19:26:40 2019 +0000

    Publish new post github-code-search-with-de-duplication.md

commit 59ed836a8ae65fd2de0394a97bc8131821b5b84d
Merge: 1a21b9e3 ef0790e4
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Sat Sep 28 19:24:18 2019 +0000

    Merge pull request #305 from alexwlchan/github-code-search

    Link to my GitHub code search page

commit ef0790e425d686174469e7906b932f7f511670fe
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Sep 28 20:20:02 2019 +0100

    Link to my GitHub code search page

commit 1a21b9e35f7e05cbfc227867aaefbf8b579b7a72
Merge: cb9fb868 54aefe5d
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Mon Sep 23 21:32:11 2019 +0000

    Merge pull request #304 from alexwlchan/gratitude

    Add a page with info on how to 'say thanks'

commit 54aefe5d7f28688e7b1a3bff09b320bd0c6da315
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Sep 23 21:28:03 2019 +0000

    Add alt text to the charity logos

commit 0007b751b5f58ef176ebe2a4a96a7f55c20ee54e
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Sep 23 21:21:55 2019 +0000

    Add a page with info on how to 'say thanks'

commit cb9fb8681fdb0271b822bb4205aaddcad35c1bad
Merge: 99670776 88c93f9f
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Mon Sep 23 19:48:36 2019 +0000

    Merge pull request #303 from alexwlchan/update-talks-page

    Update talks page

commit 88c93f9f81af996c585209bdb275fe45a00ac987
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Sep 23 19:43:14 2019 +0000

    Do a bit more work on editing the talks page

commit 996707762a4aebb7dadcddd89961f6af5729f12f
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Sep 23 11:37:45 2019 +0100

    Add an RSS link to the header

commit 110f5d94d578727efb2ab0c13dd5040af90fe38b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Sep 23 11:37:29 2019 +0100

    Redo my talks page to be more compact, highlight new talks

commit 19637a6e4be0c1ef2f85538ec64a8b2fb0e4717b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Sep 23 11:02:03 2019 +0100

    Categorise another post

commit f4967ccaa09aaac5543869dbeeba944bc60fa1a1
Merge: 325d4aa2 91abcfb8
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Mon Sep 23 09:00:38 2019 +0000

    Merge pull request #302 from alexwlchan/minify-svg-properly

    Minify SVGs when they get copied from `src` to `_site`

commit 91abcfb82e3702a75beda441e7fc79a9aa4cf394
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Sep 23 09:54:42 2019 +0100

    Minify SVGs when they get copied from `src` to `_site`

commit 325d4aa287676c0094d696b09a4a1e778afdd827
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.fastmail.co.uk>
Date:   Mon Sep 23 08:20:20 2019 +0000

    Publish new post triangular-coordinates-in-svg.md

commit fb547ec43330dc75c9aac35c650b5dd602340e68
Merge: 7a49b76f deba43f9
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Mon Sep 23 08:17:36 2019 +0000

    Merge pull request #301 from alexwlchan/svg-coordinates

    Add a post about drawing with triangular coordinates in SVG

commit deba43f9582b7881d66739421b02a8d83bccb7f1
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Sep 23 09:12:29 2019 +0100

    Add some nice preview text for social media

commit 1329dd902eeca8b719d12cbda5736ea99b626148
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Sep 23 08:13:08 2019 +0100

    Markups on the triangular SVG post

commit c745acc3a43aa5614180c9aacda3398e7dfe1076
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Sep 23 08:12:54 2019 +0100

    First draft of the "triangular coordinates" post

commit e7e23fa7361e94ad92522d884289ed830d491ece
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Sep 22 23:08:15 2019 +0100

    Finish the first draft of triangular SVGs

commit 5af3b6a61128cf744b475f501cf4cd01dc333085
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Sep 22 19:22:12 2019 +0100

    A bunch of stuff towards the SVG triangular coordinates post

commit 7a49b76f8eb1f2f9de07c6ce27bdf6d582873aa4
Merge: db357ae0 48aee187
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Mon Sep 23 07:50:18 2019 +0000

    Merge pull request #300 from alexwlchan/fix-linting

    Fix the linting in 'make build' and 'make build-drafts'

commit 48aee18734dc322f770da16338734ea25416587f
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Sep 23 08:45:31 2019 +0100

    Fix the linting in 'make build' and 'make build-drafts'

commit db357ae030a3448f32255996233dbf33351aaa4d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Sep 22 14:25:25 2019 +0100

    Revert "Generate SVG images by template"

    3624594c4dc1755d5479ef34cd00da782d6723fa

commit 2668e24ad016cfbd04c9547c450f2a2c435ce0d3
Merge: d6198ddf a03cc1a2
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Sun Sep 22 09:32:34 2019 +0000

    Merge pull request #299 from alexwlchan/add-svg-generation

    Add a mechanism for generating SVG images by template

commit a03cc1a22e346e8084aed635d674ec4bf692b053
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Sep 22 10:27:20 2019 +0100

    Generate SVG images by template

commit d6198ddfb56e8e15bd9bf223e3db10ed742d4399
Merge: cc50d64b 15b26d56
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Sat Sep 21 21:05:22 2019 +0000

    Merge pull request #294 from alexwlchan/remove-rake

    Get "make serve" to rebuild the site again

commit 15b26d567b84f8f2374c4f24b0e52e39bb6e7ea7
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Sep 21 22:02:06 2019 +0100

    Fix the build-drafts command

commit fa2cfdacee6eaf7d441e3fc25ae273179982fe53
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Sep 21 21:54:34 2019 +0100

    Fix draft publishing in the rake-free world

commit 86c371f1fe1e3c875b50301bfcb70c29f64e00de
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Sep 21 21:31:34 2019 +0100

    Actually publish the new Docker image

commit cc50d64bcbcb3acb4b44bc00bc422feb0902c1af
Merge: 37f99ada 9cd14e4f
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Wed Sep 18 23:11:19 2019 +0000

    Merge pull request #298 from alexwlchan/another-bump

    Quote my YAML strings

commit 9cd14e4fb8233dcc6ac90fcbc87b30b936225a24
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Sep 19 00:07:11 2019 +0100

    Quote my YAML strings

    Another small change to test the new GitHub Actions.

commit 37f99ada86028b0eeb108f7999cdcb17f87e5e80
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Sep 19 00:02:16 2019 +0100

    Tweak the screenshot; trigger a new GitHub Actions build

commit 4a5d7a0c1fe91c1f2f9abeb4e5a1c82b79b236db
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Sep 18 23:47:12 2019 +0100

    converted main.workflow to Actions V2 yml files

commit 641ef3d9a9103cfb824b1ec42f52a8a076a16110
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Sep 14 09:38:20 2019 +0100

    Very tiny tweaks to the main page

commit 3d8b5bb4ac371be6d46f1301febfbb934b9af5f4
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.fastmail.co.uk>
Date:   Fri Sep 13 21:18:04 2019 +0000

    Publish new post slides-for-pycon-uk-2019.md

commit bd16df63fec7668ce6351706eba4cfcd12b32a2d
Merge: 2a9f0906 86bc75bb
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Fri Sep 13 21:15:50 2019 +0000

    Merge pull request #297 from alexwlchan/slides-for-pyconuk-2019

    Add some slides for PyCon UK 2019

commit 86bc75bba7fbe56d24b2eb60a3a8fcbeb34d6cae
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Sep 13 22:10:08 2019 +0100

    Add some slides for PyCon UK 2019

commit 2a9f0906c20a4cadf5d977c545cc8a7d2653b452
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.fastmail.co.uk>
Date:   Thu Sep 12 19:53:53 2019 +0000

    Publish new post streaming-large-s3-objects.md

commit 9d9da213b306e126c370f85efa32eaa269b5253e
Merge: 0cfeb754 5f68c92f
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Thu Sep 12 19:51:36 2019 +0000

    Merge pull request #296 from alexwlchan/read-large-s3-objects

    Add a post about streaming large objects from S3

commit 5f68c92ff089079eb40bceb644a25e0ffbd19311
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Sep 12 20:48:00 2019 +0100

    Add a quick summary

commit 9e2a513749fbfc16c291188d8c2954a4c89ea388
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Sep 12 20:46:56 2019 +0100

    Markups on the post about streaming large objects from S3

commit 3f107b3e9510e2a2712a7d9162a5ae9feb4a482b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Sep 12 10:26:06 2019 +0100

    Plus the diagram of a SequenceInputStream

commit bbe97d0f5fb3a94d15249023c28caaa1600bcf58
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Sep 12 10:25:55 2019 +0100

    Complete the first draft of the "large S3 objects" post

commit 81186cdc0e4aeee4e953a5040c69c5e00bc541c6
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Sep 11 18:14:48 2019 +0100

    Initial draft of the "large objects from S3" post

commit 0cfeb7541163497210109dab7614713626a0d204
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Sep 8 17:43:56 2019 +0100

    Tone it down ever so slightly

commit edd571f6fb211d1dbf8e5bb310a25b05304913f8
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Sep 7 21:34:38 2019 +0100

    Remove the Rakefile; invoke Jekyll directly

commit 7bc4cde100bdef302f729ac840966da2eec78ab1
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Sep 6 07:01:54 2019 +0100

    Tweak the title of this post

commit 2adfa9b771336089a5f231e550c6cfd7bc7c23f2
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.fastmail.co.uk>
Date:   Thu Sep 5 23:16:05 2019 +0000

    Publish new post unpacking-compressed-archives-in-scala.md

commit 2d53bc9aeb57830f1b2909849f843fe74bc14a7c
Merge: 21dc7227 a0290da5
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Thu Sep 5 23:13:50 2019 +0000

    Merge pull request #292 from alexwlchan/compressed-archives

    Post about unpacking compressed archives in Scala

commit 21dc72278c5cf9770b9f451913e9bbde3064e621
Merge: 14973194 5aa74b19
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Thu Sep 5 23:12:59 2019 +0000

    Merge pull request #291 from alexwlchan/jekyll-4-cache

    Add the Jekyll 4 cache to the gitignore

commit a0290da5a722b666c86c1da46add6c4ff60ae129
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Sep 6 00:10:05 2019 +0100

    Post about unpacking compressed archives in Scala

commit 5aa74b19576184df67da59e67d5025171149eab3
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Sep 6 00:09:06 2019 +0100

    Add the Jekyll 4 cache to the gitignore

commit 14973194d059b2a195074816e5924ef76857c215
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Aug 30 10:22:32 2019 +0100

    Add a missing import to the code example in the kmeans post

commit 3937adbee401263004fcc6432ea74844d47b3d9c
Merge: 07e80d71 6a861360
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Mon Aug 26 14:42:35 2019 +0000

    Merge pull request #289 from alexwlchan/fix-formatting

    Fix some code formatting in an old post

commit 6a8613606e66c278bc7f8b381d1198c7d08a8a77
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Aug 26 15:38:40 2019 +0100

    Fix some code formatting in an old post

commit 07e80d71d55f8602b67398e66b485dbb390b94af
Merge: 87e7089f 61e3a7ac
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Sat Aug 24 12:31:31 2019 +0000

    Merge pull request #287 from alexwlchan/update-to-jekyll-4

    Start using Jekyll 4 to build the site

commit 61e3a7ac2368b40f9d48ef92a766c03f84de228b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Aug 24 13:27:04 2019 +0100

    Get the "make serve" command working again

commit 421a1d7d46693f0052d27dd948f1c228e64dca0d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Aug 24 10:57:50 2019 +0100

    Keep moving towards a working Jekyll 4 setup

commit a12538f67467e3e7ca38374b963aba0f40ee7418
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Aug 24 09:48:35 2019 +0100

    enough to get a reliable segfault

commit 87e7089f05fcdf1765d66265207a877822a2373e
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.fastmail.co.uk>
Date:   Mon Aug 19 09:40:53 2019 +0000

    Publish new post finding-tint-colours-with-k-means.md

commit 30f8919315926009aa451cba6971649600a4e9dd
Merge: 3f56892c acdf0b78
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Mon Aug 19 09:38:21 2019 +0000

    Merge pull request #285 from alexwlchan/k-means

    Add my post about k-means clustering

commit acdf0b7845beae64d1b58fef32911ac137edfd50
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Aug 19 10:32:50 2019 +0100

    Add some post metadata

commit 795a65659ab39102a3c98b6fe5c4fdd3f307c407
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Aug 19 09:53:15 2019 +0100

    Sort out alt text on images, clean up for posting

commit 02dfee5d66090309930f3a972e67447bdfde9da7
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Aug 19 08:42:40 2019 +0100

    Markups on the tint colours post

commit 8241ed68c0b95bbebf56e7a0971dc5bada14ce1e
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Aug 18 21:11:23 2019 +0100

    Get the first draft of the post done!

commit c33cccc600b9ca3d6c2edd867434b4b9f3eeae87
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Aug 18 11:45:10 2019 +0100

    Include a mathematical proof that black and white are enough for WCAG

commit 5082c55b02d3ff7b94c925654792481befcfd448
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Aug 17 23:01:18 2019 +0100

    More stuff about tint colours

commit 211ba232a9ac754b19baf90702084beecacd09a6
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Aug 16 20:42:24 2019 +0100

    Write a complete implementation of k-means

commit 3be3d2b339625e860afec0ed88e7877f222f32e9
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Aug 16 18:34:46 2019 +0100

    A bit more stuff on k-means

commit 3ceb2be5b1d32e84196bbf3bd8997e62d026b82e
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Aug 16 09:02:55 2019 +0100

    Green isn't green!

commit 3d1afba065cdacd8376716a3bac91a556c7aeeff
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Aug 16 08:28:33 2019 +0100

    Start writing a post about tint colours and k-means

commit 3f56892cdcdd5d786cdf42bd2a3f57904da1995b
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.fastmail.co.uk>
Date:   Mon Aug 12 16:22:31 2019 +0000

    Publish new post removing-the-drm-from-my-kindle-books.md

commit 93530eacb75d9e979d6cd3fc91605dfec0d4c045
Merge: 00e374b4 39186687
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Mon Aug 12 16:20:09 2019 +0000

    Merge pull request #283 from alexwlchan/kindle-drm

    Add a short post with some links to Kindle DRM-removing scripts

commit 391866874109dbe1ddbfb9a92de41307e0ec9200
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Aug 12 17:15:49 2019 +0100

    Markups on the Kindle DRM post

commit df0529e7b123cf45b9ffa89adf3482b13cb422ee
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Aug 12 13:10:36 2019 +0100

    First draft of a post about stripping Kindle DRM

commit 00e374b4e55bf0ba92910177128d3bf78b9f1bce
Merge: 0ca8ec08 4a209c9b
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Thu Aug 1 09:31:32 2019 +0000

    Merge pull request #282 from alexwlchan/move-analytics-down

    Move the analytics to the bottom of the page

commit 4a209c9ba22e5533f13f16a80605ed3a799be765
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Aug 1 10:26:38 2019 +0100

    Move the analytics to the bottom of the page

    You don't need it to render the page, it's not a critical resource,
    and the rest of the page should be fully loaded before sending any
    analytics off to me.

commit 0ca8ec0837cb9623b1bff48108eb1b2be0b324fd
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.fastmail.co.uk>
Date:   Mon Jul 29 20:34:55 2019 +0000

    Publish new post finding-divisors-with-python.md

commit 106e927dacecaeb8ed74cd6c78ca3efa801ea379
Merge: 44c889ab 251294ef
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Mon Jul 29 20:32:40 2019 +0000

    Merge pull request #281 from alexwlchan/finding-divisors-with-python

    Add a quick post about finding divisors with Python

commit 251294ef7606337b5bb4068ba66309a9567ab06c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Jul 29 21:28:00 2019 +0100

    Markups after brief code review

commit 4e8b71758122205676a55c87a94080934b14d772
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Jul 29 21:23:18 2019 +0100

    First draft of a post about finding divisors in Python

commit 44c889abcf6b0325115433f3bb6b7904384305f3
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jul 21 15:45:17 2019 +0100

    Fix the 00:00:00 timestamps in this Unix time diagram

commit bb1e5a491ccb8409951dd97f85f7a52a29968d1d
Merge: 1b8b2318 717a63f2
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Sun Jul 21 14:01:06 2019 +0000

    Merge pull request #278 from alexwlchan/slim-css

    Slim down the CSS a little

commit 717a63f2c781bc3d46fa35e39520dcf3763e3cda
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jul 21 14:55:26 2019 +0100

    Slim down the CSS a little

commit 1b8b23180314bdc51b76a59adbe86e1c325d4747
Merge: fea55a21 81269962
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Thu Jul 18 15:46:01 2019 +0000

    Merge pull request #277 from alexwlchan/smaller-tweets

    Reduce the size of avatars in embedded tweets

commit 812699623e950262899a81f45b2ae6e5e8db141b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Jul 18 16:42:23 2019 +0100

    Because we read the username from the URL, it needs to case-match

commit 16ca8045e9597208f5493368dd25c35d5368f456
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Jul 18 16:36:20 2019 +0100

    Push a new version of the Docker image

commit 290c5641786ec851c098f4c93115ceed8c6756cb
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Jul 18 16:25:09 2019 +0100

    Handle the case where cutting a thumbnail makes the file *bigger*

commit 5a0724b871d75ca0911cb08c339325ee47452227
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Jul 18 16:12:03 2019 +0100

    Sort out the rendering and creation of Twitter avatars

commit dea8aa68bca2235486c036d07a22a7c06c518bd2
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Jul 18 16:03:46 2019 +0100

    Get avatar resizing working

commit 20c538bdf3e98d2106b58df3d6f26b2f459e9765
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Jul 18 15:53:46 2019 +0100

    Put all the avatar images in the /_tweets directory

commit 6a78cc61d697c3f0761508a12fe2adc87ec73e8b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Jul 18 10:45:03 2019 +0000

    Add ImageMagick to the Docker image

commit bedc5165adee330f9f4f2ef374a83c75dafaa0cb
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Jul 18 11:30:21 2019 +0100

    Put the screen name in cached tweet files for human readability

commit fea55a216a6f06a1adbab2c8a2628723031a0d7e
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.fastmail.co.uk>
Date:   Thu Jul 18 07:53:44 2019 +0000

    Publish new post section-28.md

commit 72e1e7b77b0a6dadb732eb63c31bdebb39c04a2e
Merge: 8b6f3f41 7c9dfbae
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Thu Jul 18 07:51:45 2019 +0000

    Merge pull request #276 from alexwlchan/section-28

    Turn a Twitter thread into a blog post about Section 28

commit 7c9dfbae827ca6dc00b56b6e6d855c412fbb1209
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Jul 18 08:48:21 2019 +0100

    Don't forget to check in the tweet files

commit d6d3a57ade0f3e4dca260ae9aced31dbe5389358
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Jul 18 08:42:23 2019 +0100

    Turn a Twitter thread into a blog post about Section 28

commit 8b6f3f4130c01e065b11b788bd02ae23e1883e53
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Jul 8 22:49:59 2019 +0100

    This post should really be "best of"

commit 19ac71af62022efbfd498dc2d82dc4dfdd0f8854
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.fastmail.co.uk>
Date:   Mon Jul 8 21:44:29 2019 +0000

    Publish new post creating-preview-thumbnails-of-pdf-documents.md

commit f480a655f5695e3661deb01187808cf70544f5d4
Merge: 79738ce8 936affcf
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Mon Jul 8 21:42:23 2019 +0000

    Merge pull request #275 from alexwlchan/pdf-previews

    Add a post about creating PDF thumbnails

commit 936affcf19974af429d90774f4c931bc4da36b00
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Jul 8 22:38:51 2019 +0100

    Add a post about creating PDF thumbnails

commit 79738ce8ffe474b6fb92711d634440d32aef4cab
Merge: 98aa274b 455315b8
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Sat Jul 6 06:57:50 2019 +0000

    Merge pull request #274 from alexwlchan/fix-invalid-html

    Fix a few bits of invalid HTML flagged by HTMLProofer

commit 455315b8dcd97397a5d9763816fb45c6a168e0d1
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Jul 6 07:54:06 2019 +0100

    Ditch an unwanted closing </p> tag in this post

commit c3d81b8845e9b1eec94f2ae4608f87ffaf55c49b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Jul 6 07:52:10 2019 +0100

    Use <figure> instead of <center> in the Skeletor page

commit 7949b8365b9776ddcb5c148b0e3c86d86c00f019
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Jul 6 07:50:55 2019 +0100

    Use CSS rather than <center> for this <iframe>

commit 98aa274b3b068a87a8b8030aa643b237e224b131
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.fastmail.co.uk>
Date:   Wed Jul 3 19:33:56 2019 +0000

    Publish new post listing-s3-keys.md

commit 59be425fbfcebae214a294ed24697f89d4f84405
Merge: 805ecc38 9cee3d5a
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Wed Jul 3 19:31:42 2019 +0000

    Merge pull request #273 from alexwlchan/listing-more-s3-objects

    Add a post about listing ALL THE S3 KEYS

commit 9cee3d5a9f83698cda1842abe3af1d3abc7da042
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Jul 3 20:24:55 2019 +0100

    Add a build task that runs 'jekyll build' with drafts

    This means draft posts will be present when Azure runs a linting check,
    so it will catch missing alt text in drafts *and* won't flag links that
    reference a yet-to-be-posted draft.

commit 6089c3b14a701a9dac158ed20491c8862bd742c4
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Jul 3 20:17:11 2019 +0100

    Add a post about listing even more S3 keys!

commit 1e935404bae62dc92640a8f8f97b2e40b358a8d3
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Jul 3 20:03:25 2019 +0100

    Wrap the text in the LICENSE file

commit 805ecc381a40122050ec23427ef2194f32d5e772
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Jul 2 08:36:54 2019 +0100

    Correct capitalisation of "braille" in the sharing text

commit dc93846fb11d07648895369b698455eae74eb806
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.fastmail.co.uk>
Date:   Mon Jul 1 07:51:12 2019 +0000

    Publish new post ten-braille-facts.md

commit bb12a7e1fd877267e74825c7d3fb87efe13d9fda
Merge: f71015b8 606158a6
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Mon Jul 1 07:48:52 2019 +0000

    Merge pull request #272 from alexwlchan/ten-braille-facts

    Add a post about ten braille facts

commit 606158a669caa3efa91686143f6447d90a1007e6
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Jul 1 08:45:16 2019 +0100

    Back out some faulty debugging code

commit 3255b83d063e0d0f0f2b7e7bee26ec12ceb73644
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Jul 1 08:37:36 2019 +0100

    trailing whitespace here is bad

    It means alt text lookups fail because there's an extra space.

commit 1d3db0045f00ea31675dd1ba0b47180d4644a557
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Jul 1 08:23:17 2019 +0100

    Add a big image for SOCIAL

commit 59d050691160db9c283f1ab492cb358a96a5deaf
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Jul 1 08:17:58 2019 +0100

    Final markups on the Braille post

commit 95454d63d2edd64c041faec43516d887220da444
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Jul 1 08:08:34 2019 +0100

    Add a note about capitalisation, fix it

commit edf2dd8b6935c4c9ecb16c97424ba1540031637b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Jul 1 07:58:49 2019 +0100

    Another round of review on the Braille post

commit 0085d526057df1ef6c8e32d4854ac794e68fa34b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Jul 1 00:16:35 2019 +0100

    Add all the pieces for the Braille facts post

commit f71015b8565b0b8f8ce24d2d8ee4e0ca2804a35f
Merge: 0737fde1 539dde6b
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Sat Jun 29 17:22:43 2019 +0000

    Merge pull request #271 from alexwlchan/pride-hearts

    Add the code for the Pride hearts

commit 539dde6becb7ba718aa8e612edf7ce43f559ab89
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Jun 29 18:17:49 2019 +0100

    Put some more stuff in the "assets" directory

commit 6de2d8a68c7ca26d87aa6c48c9fb3c786bcea7ef
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Jun 17 17:58:23 2019 +0100

    Add some more examples of hearts

commit e179cbb41186cb32ee42ead04b454f01d25d019a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Jun 17 13:03:27 2019 +0100

    Get it all working properly

commit 86986fc3f18f3f468a10f3f913eeeb11b1684297
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Jun 17 12:48:27 2019 +0100

    Add some color helpers

commit 0650ddaa26e7bcb268b45259043ac473c05b3a28
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Jun 17 12:26:23 2019 +0100

    Start breaking up the coordinate generators

commit 29469e6fcc0a4f6b7de7024c7608f7484c2239e1
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Jun 17 11:38:06 2019 +0100

    Add some initial code for the pride hearts

commit 0737fde1d6c9b6dee749e92c64b61fcaf04f4ec1
Merge: 7806a502 4d78e860
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Sat Jun 29 11:19:58 2019 +0000

    Merge pull request #267 from alexwlchan/load-plugin-dynamically

    Sort out html-proofer properly

commit 4d78e8605a98be904e38e684bff95803a29b0709
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Jun 29 12:16:43 2019 +0100

    Don't forget the talks page

commit 7a2cb764959c4d2145b1d7f2eab7b97d62e4c4e8
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Jun 29 12:11:54 2019 +0100

    Add alt text for every image on the site

commit 0579c3cbe335f310a5bf27ca3c790c3dd42c8d2b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Jun 29 12:05:16 2019 +0100

    Support alt text on single-image tweets

commit 22c40abb9a7b24447c1b6a5d76254203e38f5a10
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Jun 29 11:50:14 2019 +0100

    Keep cranking up the alt text

commit 48af16828113a601e4949435e45d038f2f3ce649
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Jun 29 11:42:05 2019 +0100

    Add some more alt text

commit 96f76ffb1bed86e6959f417f8d187417ede7bac5
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Jun 29 11:30:52 2019 +0100

    Keep adding alt text

commit 604e91728b32ac54112eccd01db5ef1c590c55ae
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Jun 29 11:01:37 2019 +0100

    Keep cranking up the alt text

commit 91b57820b62a0a6171f82df8f58d2112e227ae41
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Jun 29 10:45:30 2019 +0100

    Keep adding alt text

commit bf3afadc1e3fcefd9548e5aab52e0132576d1d85
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Jun 29 10:14:31 2019 +0100

    Add some more alt text

commit 49cf1fcba2112f8a8a3332b1720a413c65c48d2d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Jun 29 10:07:32 2019 +0100

    Add some more alt text

commit 99a6c88d3fe10bc01ed6137b81cc6748538fd1d2
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Jun 29 09:42:54 2019 +0100

    Add more alt text

commit 581d9241bc8edc1be40263762e53e221478bf172
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Jun 29 09:33:25 2019 +0100

    Add some more alt text

commit bcb5d37e3e939e976f3bf9633da98a90984fb92f
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Jun 26 21:33:23 2019 +0100

    Add some more alt text

commit 0e4834854fafa7b23bb4fc2621ddea4a4f012cc0
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Jun 26 21:24:15 2019 +0100

    It turns out you can't put an `<ol>` in a `<p>`!

    See https://stackoverflow.com/q/5681481/1558022

commit d2e1632d3f1dddb7265787229e9d694b064b8e8c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Jun 29 09:31:32 2019 +0100

    We can tidy up some of this publish_drafts code

commit c47f88453a36533110734a65d8d6c71afebba381
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jun 28 20:13:26 2019 +0100

    Add some more alt text

commit f9e462013a038adf0a4dd963b2aa67249a711585
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jun 28 20:09:11 2019 +0100

    Bump the Docker image version

commit f3ef261718795c4d017d4454a8f8124c33094505
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jun 28 20:07:47 2019 +0100

    Add a dedicated linting command

commit 43348eaa60b5228c892cd50e09f534ce0fe9fec6
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jun 28 20:04:09 2019 +0100

    Get live reloading with serve

commit 4dd8872881fb7f28224dd5ebbee44c1e8552b9b9
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jun 28 19:55:43 2019 +0100

    Try to get "serve" working with Rake

commit e753bc8e3d48db5d53dfe9f002977f369f1712f1
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jun 28 19:38:07 2019 +0100

    Get publish-drafts working dynamically

commit 761346b65b27162fcd983aa2a8c7e1e24ecf54b6
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jun 28 17:41:46 2019 +0100

    Start using Rake as a task runner

commit 7806a50231e0de5336c091e6c665141d138ab323
Merge: 4251b926 a545347d
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Wed Jun 26 16:44:25 2019 +0000

    Merge pull request #266 from alexwlchan/more-html-proofer-fixes

    Fix more bugs spotted by HTMLProofer

commit a545347d1718f63cafe22a5b1ecbc2869aa48593
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Jun 26 17:40:48 2019 +0100

    Disable HTMLProofer again so the PR can be merged

commit 660efaa585b44afeb4f4ef2d2a9dedb328daf497
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Jun 26 17:38:46 2019 +0100

    Add more alt text to images

commit 272a0787940ed3793bc3faf6d28305f83a8c0a33
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Jun 26 17:33:26 2019 +0100

    Add more alt text + remove broken links

commit 671a83b5a478d5e8a1e169c9ad7f3b9a9d9299d2
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Jun 26 17:31:28 2019 +0100

    Add more alt text

commit 34a3438564ab1f0e324c04075831011a5bad3f74
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jun 23 16:42:04 2019 +0100

    Add a few more instances of alt text

commit 4ec20f039715367b8177e024e951c9b94ed5d345
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jun 23 16:33:30 2019 +0100

    Turn on HTMLProofer

commit 4251b9260f23e82a8799b9546762a9f5bd6e2c1e
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Jun 26 13:24:01 2019 +0100

    Move the ResophNotes CSS stuff back into /posts, add alt text

commit c84d93f026512a8de8c2c95e6d044d77fe1b0743
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Jun 25 09:16:44 2019 +0100

    Fix social preview images

commit 7d0cf3dea3b88b5284dd90a7649aafa87cf243b7
Merge: 7ed4524e e75c3d8b
Author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
Date:   Sun Jun 23 09:00:58 2019 +0000

    Merge pull request #265 from alexwlchan/ditch-pagination

    Ditch the old paginated blog

commit e75c3d8b7aee01a2426b4d211127f7958c4ec203
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jun 23 09:54:07 2019 +0100

    Remove /blog/:page/:n pages from the site

commit e13cdc558582b5f7672a1af15c33a674fb13f9fe
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jun 23 08:36:27 2019 +0100

    Tweak the 410 wording

commit 7ed4524e92acfd3e964ff5d97b4c7a6ab12e189b
Merge: 154e9eec 90ce0b4f
Author: github-actions[bot] <github-actions[bot]@users.noreply.github.com>
Date:   Tue Jun 18 16:00:27 2019 +0000

    Merge pull request #264 from alexwlchan/trans-coming-out-letter

    Add the post about being ✨ trans ✨

commit 90ce0b4f9f1c1f1c2cfeef418264ec1836115325
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Jun 18 12:49:08 2019 +0000

    Publish new post regenerating.md

commit 252206a67ef771877a0000a6f315d115b134a30e
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Jun 18 13:48:33 2019 +0100

    Final markups!

commit 1cadcd2713fa3b44939320b18590b88619f408ae
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Jun 18 09:37:46 2019 +0100

    Add a few more markups on the gender post

commit 9c037a520ccbf01abea8f60d188987772960ae80
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Jun 17 20:48:03 2019 +0100

    Add some more markups

commit c21a4b83ea09047025409e02c4ca612029e71d9d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Jun 17 08:44:21 2019 +0100

    hey look, it a lexie

commit 706d0db611a9252d9013a723eef86aa0df2105be
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Jun 17 08:08:57 2019 +0100

    flesh out some more words

commit 225c27f7a7248f37352c98d17d8ae8b51783acbf
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Jun 17 07:56:35 2019 +0100

    Write lots of words

commit a6491a575e103e49fe53cd9ff2418357a0e3c022
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Jun 17 07:03:43 2019 +0100

    Initial draft of coming out post

commit 154e9eec3512d5b7ea03f380c40b0f90fd1e7535
Merge: 2367d5ea e3474619
Author: github-actions[bot] <github-actions[bot]@users.noreply.github.com>
Date:   Tue Jun 18 10:15:37 2019 +0000

    Merge pull request #263 from alexwlchan/publish-only-tracked-drafts

    Publish only tracked drafts

commit e347461908e3c14ac35fdb97683b58718dfbf063
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Jun 18 11:11:04 2019 +0100

    Bump the Docker image version

commit 6b09893eba5716993e0f70d7bb006c3adfdbd741
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Jun 18 09:41:38 2019 +0000

    Actually, don't clean up the _drafts directory at all

commit 829b9c7cd6e7c7fb57c295cc1a9891f7b3762bc6
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Jun 18 08:52:05 2019 +0000

    Only delete the _drafts directory if it's empty

commit 41998b9a0aab8c2029d1c0aae77d9b6bde0b7093
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Jun 18 08:49:24 2019 +0000

    Only publish a draft that's tracked in Git

commit 2367d5eaca5fc912c4e8b2e1a6a6a66115cf6264
Merge: a500ab8a 045e0a11
Author: github-actions[bot] <github-actions[bot]@users.noreply.github.com>
Date:   Sat Jun 15 22:02:11 2019 +0000

    Merge pull request #262 from alexwlchan/plugin-docs

    Don't talk about no-longer-existing tests in the README

commit 045e0a110044371978c489c150afd6a56cc8084f
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Jun 15 22:58:12 2019 +0100

    Tidy up the Ruby plugins a bit

commit 19a9db7bb7ad038b0e15907d200769d386434182
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Jun 15 22:58:00 2019 +0100

    Remove redundant references to Travis in the README

commit a500ab8ae44f798d5a580445796ac825679c4470
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.fastmail.co.uk>
Date:   Sat Jun 15 21:49:44 2019 +0000

    Publish new post a-jekyll-filter-for-obfuscating-email-addresses.md

commit 476c5d26200c529f57d3bc6aec6417f9288ea703
Merge: 890addeb 8d022754
Author: github-actions[bot] <github-actions[bot]@users.noreply.github.com>
Date:   Sat Jun 15 21:47:46 2019 +0000

    Merge pull request #261 from alexwlchan/readme

    Quick post about the Jekyll filter that obfuscates email addresses

commit 8d022754e14d797ea3d19dc9e5da469e28f1b397
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Jun 15 22:44:19 2019 +0100

    Quick post about the Jekyll filter that obfuscates email addresses

commit 890addeb856c18216a3d182e29eda81f4e910580
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Jun 15 19:04:59 2019 +0100

    Fix a typo on the talks page

commit 3c3753e3a2a4954c2fff03394f7cb65223b36317
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Jun 13 21:44:07 2019 +0100

    That Chinese post should have a ❤️

commit f5e660640dd66e8b4711b450fb9413d9c67002dd
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.fastmail.co.uk>
Date:   Wed Jun 12 07:45:45 2019 +0000

    Publish new post reading-a-chinese-dictionary.md

commit d3ce2934512abccb7260ff5666525478cd8d9743
Merge: e9cab15c ea475f7c
Author: github-actions[bot] <github-actions[bot]@users.noreply.github.com>
Date:   Wed Jun 12 07:43:43 2019 +0000

    Merge pull request #259 from alexwlchan/chinese-radicals

    Add a post about reading Chinese dictionaries

commit ea475f7ce98aedd92264b523d270f576e41519fb
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Jun 12 08:40:21 2019 +0100

    A few final markups/corrections

commit 575f276e6a5829fc0c77cefc699a722da47a8737
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Jun 11 21:57:34 2019 +0000

    fix bugs in the chinese character post

commit 00a53d5c915df9ed16d0ada8d2569d8258120b4f
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Jun 11 22:37:47 2019 +0100

    Restore the missing emoji!

commit 2921b8f222bb544d788460b8e126b394eaee4934
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Jun 11 21:33:54 2019 +0000

    fix some images and text

commit 16c3ef24680d5ccd8c86776298d0e100c78b0d37
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Jun 11 21:29:26 2019 +0000

    Add the initial post draft

commit 416db34ad4d1f786b42bc1f489047e6bbdbfa9aa
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Jun 11 20:27:01 2019 +0000

    Add a post skeleton

commit adc48569c4d5edefc2bea1dda9d2f6afdb81912e
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Jun 11 20:25:53 2019 +0000

    Add images for the Chinese dictionary post

commit e9cab15c0db93120eb767ac40fd43039902615e4
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jun 9 22:03:58 2019 +0100

    Tweak this post so it doesn't overflow on narrow screens

commit b3b7dc38dcbf7f19110f957861e6ebeadedc7556
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.fastmail.co.uk>
Date:   Sun Jun 9 10:36:43 2019 +0000

    Publish new post acorn-on-the-command-line.md

commit 43b766efd5066a6a6065dd7cf69484dc94c8908d
Merge: 7a9c78f6 8e17d615
Author: github-actions[bot] <github-actions[bot]@users.noreply.github.com>
Date:   Sun Jun 9 10:34:43 2019 +0000

    Merge pull request #258 from alexwlchan/batch-acorn-images

    Add a post about using Acorn on the command-line

commit 8e17d61578412fbb0e289326105392b9e055af5b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jun 9 11:31:19 2019 +0100

    Add a post about using Acorn on the command-line

commit 160d447b221dab12d4763b00890d34f2f9b9b196
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jun 9 09:10:30 2019 +0100

    Add a new "Working with macOS" category

commit 301b7b1d85731c93e7453fbb3c31df38bcd710b7
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jun 9 09:10:18 2019 +0100

    Create an empty category on new posts

commit 7a9c78f628160d699998a438cd1c8d42cea43838
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Jun 5 08:36:03 2019 +0100

    Make appearance a bit more consistent

commit b71382a887572d7bfe194a139ccd8f6f871d36cb
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Jun 5 07:49:49 2019 +0100

    Clarify "women" who don't get periods

commit 935f10a1a16331b44e187b1aeff9ab146e2b1dfa
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Jun 4 23:52:17 2019 +0100

    Tweak the blockquote CSS

commit a0d02b1267a9ff29bfdc028fcafdfc316df88ac7
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.fastmail.co.uk>
Date:   Tue Jun 4 22:51:19 2019 +0000

    Publish new post cycle-tracking-isn-t-just-for-women.md

commit cacc07b2c6a8afb63e46eff2003138b052b7fb42
Merge: 0819bac6 c8d52927
Author: github-actions[bot] <github-actions[bot]@users.noreply.github.com>
Date:   Tue Jun 4 22:49:26 2019 +0000

    Merge pull request #257 from alexwlchan/im-going-to-regret-this

    Add a post about cycle tracking

commit c8d52927d0222b28d92004e36a5831e9ba37b127
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Jun 4 23:46:11 2019 +0100

    Add a post about cycle tracking

commit 0819bac6a50d46c6590f35ecd1de02df43070cd5
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.fastmail.co.uk>
Date:   Tue Jun 4 19:43:15 2019 +0000

    Publish new post getting-cover-images-from-mobi-ebooks.md

commit b6acc3759979b56198bc264d4a0ad0064f6123a3
Merge: 229f36fb 5b6ddd79
Author: github-actions[bot] <github-actions[bot]@users.noreply.github.com>
Date:   Tue Jun 4 19:41:16 2019 +0000

    Merge pull request #256 from alexwlchan/link-to-mobi-parser

    Add a link to my Mobi cover image parser

commit 5b6ddd795165f9dedbcafbfa9ea32ce41d6098bf
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Jun 4 20:35:37 2019 +0100

    Add a link to my Mobi cover image parser

commit 229f36fb40e5a1362351cf808a15e03d63555683
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Jun 1 20:42:33 2019 +0100

    Drop the env?

commit 57e06f53416a214c7f0e05cbf0b44dc06cd84caf
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Jun 1 20:35:14 2019 +0100

    No brackets perhaps?

commit 1dcf188e4842e74499b890bf0f625f68d10d5fae
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Jun 1 20:31:53 2019 +0100

    Another go at the SSH key

commit d6d2d98f16ecf4ffdd6ea6e9afd776ce4a2933fc
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Jun 1 20:28:05 2019 +0100

    Try tweaking the env var name

commit a0bc91e83aaa1b0b76634ea6ac35ca96a4df52f7
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Jun 1 20:23:10 2019 +0100

    Try tweaking the SSH key path

commit 14ca1adf79616d26020d8f134c4ca6ffca3f0834
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Jun 1 20:13:29 2019 +0100

    Add the missing ~/.gitconfig file in Azure

commit 78f369b35e931f1628f76894f512c058fe67536a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Jun 1 20:05:19 2019 +0100

    Have a go at using Azure Secure Files for the SSH key

commit d31680c131443d04716f374c21c7c72b3da7cabc
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Jun 1 19:46:38 2019 +0100

    Just link to the front page of Azure

commit a2ea128da0047e5a493aa58365f705ba5ca6efa0
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Jun 1 19:44:13 2019 +0100

    Fix the build badge in the README

commit b31c7d597bdad208e2754ee33e33eaf0c580c3c7
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Jun 1 18:38:23 2019 +0000

    Push to the correct branch

commit f809242f563ac31c0777b893a3d49bd3d2540d26
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Jun 1 18:34:25 2019 +0000

    Make live the main branch

commit 818502c76d178e2a8231d0a2f340c2226e77174c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue May 28 09:19:21 2019 +0100

    Add a quick update to the post

commit 9337ed67277fd2f841ae1ff6037737587690256e
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun May 26 10:06:33 2019 +0100

    Don't break the Jekyll template :facepalm:

commit d90cdbbb3470eb1a4ceac6181706c849ec272544
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun May 26 09:59:53 2019 +0100

    Use my profile image for social banners

commit f02b48ed2d69be092ae17936570cbe87b8e8762f
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri May 24 13:51:21 2019 +0100

    Commonise some of the Sass styles

commit 9910a8413fd9cfebaf255d61a2859fc08f8883d3
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.fastmail.co.uk>
Date:   Fri May 24 07:29:44 2019 +0000

    Publish new post first-thoughts-on-trans-inclusion.md

commit 00dd7361fc32a37d208ca7cd83c1b8b6880cc544
Merge: df7ceb90 f5a1e978
Author: github-actions[bot] <github-actions[bot]@users.noreply.github.com>
Date:   Fri May 24 07:27:41 2019 +0000

    Merge pull request #254 from alexwlchan/gender-policies

    Add a post about gender inclusion policies

commit f5a1e9780e634dbe29ac6fdb6ce6a70d1a8edf2c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri May 24 08:24:05 2019 +0100

    tweak the title

commit 8262b6cf08cc749a484afd09cefbe2bbde402afa
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri May 24 08:23:30 2019 +0100

    Tidy up the front matter

commit d07b2ae2092b9a1f66413dea460b45ce9e009674
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri May 24 08:22:35 2019 +0100

    Final markups on the post

commit baab11f1442b8af28db81f98bfc628746fc5014f
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu May 23 19:51:14 2019 +0100

    Another round of editing about gender inclusion policies

commit 8963a8b113666bb39a6463269d1af9574bb65edf
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu May 23 09:29:50 2019 +0100

    Actually check in the required tweet metadata

commit c8f1ee7f5a20597f90de69aea210901583a35b54
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu May 23 09:29:40 2019 +0100

    Tweak some link appearances

commit 207dd8f2e5aa385221016c7a5581d9de5a8de727
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu May 23 12:48:58 2019 +0100

    Let's call this draft 1

commit 08605db2021ab9c46541bdee2cb579c85c54e0cf
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu May 23 09:18:42 2019 +0100

    Fix the Twitter link

commit 45db28ac3646abdc53138c38a9863bcaa5b40997
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu May 23 08:31:19 2019 +0100

    Sketch out the outline

commit ba3eb2d3c802b2fca3168e596617d5a437e91795
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu May 23 08:19:40 2019 +0100

    Write more sentences

commit f7411cab4215ac851f5b97c5e757b385c6094e25
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed May 22 12:44:17 2019 +0100

    Keep fleshing it out

commit 5eadfaa86ac8b1184867fd41bc40419d5c855a47
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue May 21 08:00:58 2019 +0100

    Keep filling out the inclusion policy

commit 44144de18bce4e66dc242e5fae10c5978d19f0cd
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon May 20 22:25:59 2019 +0100

    First stab at an introduction

commit 059a8ef9e12fc9c7b7eb518c6c894a8130a29887
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon May 20 21:38:08 2019 +0100

    Get the initial post outline in place

commit df7ceb903637090d4e4f4e7cbcb63590e03250b7
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu May 16 21:42:47 2019 +0100

    Correct the ko-fi brand colour

commit e9908fc9215b63807502f9f575a8f13fb9fbad99
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed May 15 07:47:43 2019 +0100

    Save the source for the Unix time diagrams in the repo

commit 786e4d45e917fb12c9b658093a8e6a447f050c78
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.fastmail.co.uk>
Date:   Wed May 15 06:39:01 2019 +0000

    Publish new post falsehoods-programmers-believe-about-unix-time.md

commit 55b51da695c874c04fae8993c7618163f92d8dfa
Merge: f91759ba 92ad73d1
Author: github-actions[bot] <github-actions[bot]@users.noreply.github.com>
Date:   Wed May 15 06:36:59 2019 +0000

    Merge pull request #253 from alexwlchan/unix-time

    Add "falsehoods programmers believe about Unix time"

commit 92ad73d127db3c498b87849da03e7ba8e47ac118
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed May 15 07:32:49 2019 +0100

    Add "falsehoods programmers believe about Unix time"

commit f91759baa544d3e95da93b8ae9367de36034dad8
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue May 14 01:16:02 2019 +0100

    Display category info on individual posts

commit d862e33c8e29613e0451bbd4a037eedd4a356e37
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue May 14 01:09:23 2019 +0100

    Don't display hearts on the homepage

commit a38ed817b6702d5ad792aaf1e9da6161e5d91d73
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue May 14 01:08:28 2019 +0100

    Freshen up the "about the site" page

commit ab7be173ca9f0bedb260c1cd7fb697d1f69e189f
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.fastmail.co.uk>
Date:   Mon May 13 10:17:14 2019 +0000

    Publish new post creating-a-locking-service-in-a-scala-type-class.md

commit 6516b973ae22bcd8da4c46a179fc466ffd0d6498
Merge: e349fe72 56a44559
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon May 13 11:14:50 2019 +0100

    Merge pull request #252 from alexwlchan/locking-service

    Write about our locking service

commit 56a44559e399571b470c1b2bfa3b71a770e476ab
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun May 12 23:05:41 2019 +0100

    one more introductory paragraoh

commit 1d7736fb78eaa69663f46cee3824f8215a4ce0e7
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun May 12 22:59:09 2019 +0100

    A few more markups

commit e2a7281c24e05ae8f407d1acfee848e45654d3b9
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun May 12 22:50:31 2019 +0100

    Review markups on the post

commit 52b81a541309d11e6070438829a68e6515dacc4b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun May 12 19:51:21 2019 +0100

    Make this a starred post

commit 1b3b08c053e616b12fb963cf2bd08ff770e73894
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun May 12 09:33:20 2019 +0100

    Add a link to the mini-project

commit bd912f5436ca96d454c8075f9fe0a0a5e04b619f
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun May 12 09:29:36 2019 +0100

    Add a quick README

commit 6f2e67a2a65c6f01e3c04e9e6b34390697488dc8
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun May 12 09:25:13 2019 +0100

    Add a bit more example code

commit dff098ff678c461e40cda0866ca57e84d44efdd8
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun May 12 09:15:59 2019 +0100

    Add an implementation that compiles!

commit 31ca6ae3e101a4f550f93c308ae347e91dd70120
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun May 12 09:00:01 2019 +0100

    Finish an initial draft

commit 149443e5d47eefb07f5d1ac81118d4c506284085
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri May 10 10:13:21 2019 +0100

    /s/eventually/automatically

commit be36b0651fc2198bd759da5eaba113864c7dad2d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu May 9 19:07:38 2019 +0100

    Mention the DynamoDB LockDao

commit 964ae7b0fff9957d51ffd74535d36e39d00c7bf8
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu May 9 18:56:01 2019 +0100

    Write about creating a LockDao for testing

commit ccce8d836ee6d88721bfe63d7eeb4f5928edcd67
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu May 9 18:25:09 2019 +0100

    Write about the LockDao

commit 956f6b276a01f60eda9d7e4db2857d149e7c0560
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu May 9 17:25:45 2019 +0100

    Start fleshing out the locking post

commit cafd0adf639dfbf2915bc15e6e27feba51c4cf78
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu May 9 16:17:39 2019 +0100

    Add the skeleton of the locking service code

commit e349fe72f1dbe6744d12eabf8f541fe89372417d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun May 12 21:01:17 2019 +0100

    Consistent indentation in the global archive

commit 72e6f83b3aa7d67daca6cdcd0c8ba7172b1f9a5e
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun May 12 20:50:08 2019 +0100

    Add the category pages

commit f10570f11e1cd3ea6b8f00183ea850b884417cde
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun May 12 20:00:17 2019 +0100

    Remove a bunch of analytics code from the main repo

commit 4e15104a0effa9c6efe96b3a8674cffb154cc9a2
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat May 4 06:37:27 2019 +0000

    Add this week's analytics config [skip ci]

commit 2c00493c1f567e60c78bbd7ec06928179d679c20
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.fastmail.co.uk>
Date:   Wed May 1 20:59:08 2019 +0000

    Publish new post finding-unused-variables-in-a-terraform-module.md

commit 68dfb99e1b5c14d895f0a17d158d14d057103e96
Merge: 7e270e1c fb3d2ee9
Author: github-actions[bot] <github-actions[bot]@users.noreply.github.com>
Date:   Wed May 1 20:57:01 2019 +0000

    Merge pull request #251 from alexwlchan/finding-unused-tfvars

    Write a post for finding unused tfvars

commit fb3d2ee97ced00bf111a7229ecee64316535fac1
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed May 1 21:52:58 2019 +0100

    Make a few markups on that post

commit 4cc6be9e75ee179c97f9fc08d02a1a951fe132c5
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed May 1 21:46:16 2019 +0100

    Add a script for finding unused variables

commit 7e270e1c10502bd9c6a6df788a5855d22f0c19bf
Merge: b5253878 5586347c
Author: github-actions[bot] <github-actions[bot]@users.noreply.github.com>
Date:   Tue Apr 30 05:43:06 2019 +0000

    Merge pull request #250 from alexwlchan/ko-fi

    Add a ko-fi link to the footer

commit 5586347cb8103a281b5d13e2a81799222667a679
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Apr 29 22:03:35 2019 +0100

    Add a ko-fi link to the footer

commit b525387866007b71af64a66ccaabbc81fc95ace5
Merge: 9a65acb8 03767c0c
Author: github-actions[bot] <github-actions[bot]@users.noreply.github.com>
Date:   Mon Apr 29 20:56:59 2019 +0000

    Merge pull request #249 from alexwlchan/tweak-rsync

    Don't delete files I've manually added to /files/

commit 03767c0c5c3b6296d558653a64cfd0ae1dc68890
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Apr 29 21:53:01 2019 +0100

    Don't delete files I've manually added to /files/

commit 9a65acb81f1705e5bbe7d8478d6bf70d64dc51a6
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.fastmail.co.uk>
Date:   Sun Apr 28 09:13:06 2019 +0000

    Publish new post reversing-a-tco-url-to-the-original-tweet.md

commit 44485f53bb88eaa28ae51366f9ed5fc71fc81671
Merge: 1c7e0f05 97153462
Author: github-actions[bot] <github-actions[bot]@users.noreply.github.com>
Date:   Sun Apr 28 09:10:56 2019 +0000

    Merge pull request #248 from alexwlchan/tco-urls

    Add a post about reversing t.co URLs

commit 971534629f72b5fbee4af69eeb5e916386c1f44c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Apr 28 10:07:22 2019 +0100

    Add a one-line summary

commit daeff93c8495148d8cea20568c2537025c496b21
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Apr 28 10:04:48 2019 +0100

    Markups on the t.co post

commit deb2a43278310d82823f87d8420f73bc28ee5f36
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Apr 28 09:51:03 2019 +0100

    Initial draft of "reversing a t.co URL to the original tweet"

commit 1c7e0f0592441f80447b3db8ae048acd1ae4ee69
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Apr 27 07:38:56 2019 +0000

    Some more analytics data [skip ci]

commit 4d9872170087e22314de4f211c9816a049599f90
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Apr 27 08:37:07 2019 +0100

    Add a script for quickly adding aliases to referrer.toml

commit bf02b38c0ab201c9276445d622aa7cc76fe8603d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Apr 23 10:33:11 2019 +0100

    Don't repeat the front matter

commit 742aee8541c48b252c2429703ae94800b64c30a9
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.fastmail.co.uk>
Date:   Tue Apr 23 09:27:32 2019 +0000

    Publish new post some-tips-for-conferences.md

commit edfccc7229edb90c8695ca74ebee918fd0330fc2
Merge: 75d09bfe ee3abe1d
Author: github-actions[bot] <github-actions[bot]@users.noreply.github.com>
Date:   Tue Apr 23 09:24:51 2019 +0000

    Merge pull request #247 from alexwlchan/tips-for-conferences

    Add a post with some tips for conferences

commit ee3abe1d9b870dd48d3ac9da679ba64bb0189681
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Apr 23 10:20:56 2019 +0100

    Add a post with some tips for conferences

commit 75d09bfeb29e05365fc22923bfc345652332c96c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Apr 23 06:17:11 2019 +0000

    Remove all the certs code from the main repo

commit 263c21dbb012428884ea99802a22b52795504dd5
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Apr 17 07:14:46 2019 +0000

    Move the infra code to a private repo

commit 123cf27f4b4bf80c86495279f9e14655baa90cfd
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Apr 14 18:51:52 2019 +0100

    Add some infra for books [skip ci]

commit c55c3e575f7ca4a75ba30e5fa8108cdd7c3bae3b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Apr 14 17:13:24 2019 +0000

    Add infra for docstore/talks

commit cf02c8c9e15eeee15a598ad6577f32a27f120c38
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.fastmail.co.uk>
Date:   Thu Apr 11 07:00:43 2019 +0000

    Publish new post getting-a-transcript-of-a-talk-from-youtube.md

commit 144f5fdd36001b4e100e3a977da24cb25abe6ad9
Merge: 0e7e95bb 75079bbe
Author: github-actions[bot] <github-actions[bot]@users.noreply.github.com>
Date:   Thu Apr 11 06:58:27 2019 +0000

    Merge pull request #246 from alexwlchan/transcripts-from-youtube

    Add a blog post about getting transcripts from YouTube

commit 75079bbe227584ccc3bffa07bbb795a650a4f296
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Apr 11 07:54:24 2019 +0100

    Add a blog post about getting transcripts from YouTube

commit 0e7e95bbde9edee7113f5640eaa28908f480663e
Merge: 87141a75 cb767bd1
Author: github-actions[bot] <github-actions[bot]@users.noreply.github.com>
Date:   Tue Apr 9 08:23:12 2019 +0000

    Merge pull request #245 from alexwlchan/best-of

    Tweak the index page to show a "best of" and exclude some posts

commit cb767bd1db6be6276c0bb5f7ae98a7f6f8864bee
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Apr 9 09:18:07 2019 +0100

    Add a way to exclude posts from the global index

commit 6793a4b79d7ae2031b98b614f282e0d110ec9452
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Apr 9 09:03:18 2019 +0100

    Move the "best_of" key into the index

commit 4a27b715a1864faf1b8c1237fa94ea43f16a6bf6
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Apr 7 22:10:46 2019 +0100

    More simplification of template logic

commit 5a6355f060532cbbac01731aea428b64a31a40a0
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Apr 7 16:15:00 2019 +0100

    Add a page for my favourite posts

commit dd60ea80156f7ff6298f78526df697483febbbed
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Apr 7 16:05:05 2019 +0100

    Separate out the archive_list HTML from the main page

commit e8c577c38483457665c61002daa613b6978a2f2e
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Apr 7 16:00:31 2019 +0100

    Label some existing posts as "best of"

commit a5d15c713867a7bcbe44185b78a0c0ce7d9a55d0
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Apr 7 13:53:25 2019 +0100

    Add a "best of" heart to every post

commit 87141a751539287147ee407883bb0937e6414fb4
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.fastmail.co.uk>
Date:   Wed Apr 3 07:03:29 2019 +0000

    Publish new post how-i-back-up-my-computer.md

commit 6a6f1e46bf3596229a4c91351d7e4fa017e7c818
Merge: 33b93827 c152c29c
Author: github-actions[bot] <github-actions[bot]@users.noreply.github.com>
Date:   Wed Apr 3 06:59:53 2019 +0000

    Merge pull request #244 from alexwlchan/my-backup-regime

    Add a post about my backup system

commit c152c29ce3c8e6ae97d26cffb48b1bc2af8e4f2b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Apr 3 07:53:36 2019 +0100

    Add a quick summary to the post

commit 392508b93aa2d0ee54153bf75e7ba4ec76caba9b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Apr 3 07:50:48 2019 +0100

    Improve the margins on `<h3>` headers

commit cb1a6d415cc9dac3e13a3d066f6abffcfc32fbcc
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Apr 3 07:50:37 2019 +0100

    Ditch the category stuff for now

commit c3ea59f8084dd0e82e179b7ec4722e6995d87ff4
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Apr 3 07:50:30 2019 +0100

    Markups on my backups post

commit e1a4f4b42b8729f769b84aad8d8adaf45596d932
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Apr 2 22:41:19 2019 +0100

    Flesh out the second draft of my backups post

commit de2f951ed7ac8c8915036d992cdf63bb6144fa9b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Mar 31 08:14:41 2019 +0100

    First draft of my backup post

commit a1d5761b007ca17180a8d506fdcb93ac3dcc7e01
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Mar 31 08:14:31 2019 +0100

    Don't include summaries in the "recent posts" page

commit 33b9382719ad8f44bb8e7389500e9355ecfd1755
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Mar 25 22:01:07 2019 +0000

    Add missing image file

commit 5facd9f6ef3c3b24b43dc46425a04971f8a39d30
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.fastmail.co.uk>
Date:   Mon Mar 25 21:15:36 2019 +0000

    Publish new post creating-a-github-action-to-auto-merge-pull-requests.md

commit 4c9b304f303deea270ff28c1dfebe4b72825c1fd
Merge: 513a1e10 873fbacc
Author: github-actions[bot] <github-actions[bot]@users.noreply.github.com>
Date:   Mon Mar 25 21:13:23 2019 +0000

    Merge pull request #243 from alexwlchan/github-actions

    Add my post about GitHub Actions

commit 873fbacccdaca453beaf42b5c667951398d7fd4a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Mar 25 20:46:13 2019 +0000

    Finish the draft of this blog post

commit 073cb602144af278bed56683c3910482754f1b3c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Mar 25 19:46:42 2019 +0000

    Finish the second main draft of this post

commit 9d97b0d2c8ff0bf6a00ee390151e0537134e0fc5
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Mar 25 17:06:14 2019 +0000

    Continue making markups

commit b6e0f9f62f5f0918c00b6caba7975f1201547b0d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Mar 25 16:53:38 2019 +0000

    Start tidying up the intro

commit 7ae8f079c5c6006ea3d78e610feac4c0ddf88550
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Mar 25 08:42:36 2019 +0000

    First complete draft (almost)

commit d87fecd383b33da4796eb6bc79646a2f9da58383
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Mar 25 08:42:12 2019 +0000

    Initial draft of the GitHub Actions post + category changes

commit 513a1e104cb3116d0920845c0809d6730fd4c07a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Mar 23 07:30:54 2019 +0000

    Add some more analytics config [skip ci]

commit fe0fcbcb55f09c5bcf6dad5897ed993a761bb7e0
Merge: 66f4e713 a8634ee8
Author: github-actions[bot] <github-actions[bot]@users.noreply.github.com>
Date:   Thu Mar 21 13:49:47 2019 +0000

    Merge pull request #242 from alexwlchan/add-chris-tweet

    Add a link to Chris's ticket tweet

commit a8634ee8f5db70d2d1b94f67fc3ec94c2e943736
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Thu Mar 21 13:43:37 2019 +0000

    Recut all the images with ImageMagick

commit 1d97495e0bf11e5c7575c60ceb71a2de84592a24
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Thu Mar 21 13:32:00 2019 +0000

    Add a link to Chris's tweet about the bridge

commit 66f4e713d8cd93d0b5ac1a2dfceb376be9fe025f
Merge: 3959273d b06a19aa
Author: github-actions[bot] <github-actions[bot]@users.noreply.github.com>
Date:   Thu Mar 21 08:15:34 2019 +0000

    Merge pull request #240 from alexwlchan/tweet-template

    Refactor the tweet plugin to put the HTML in a Liquid template

commit b06a19aa78203cecba6aba5436fe1fab49165b0d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Mar 21 08:12:00 2019 +0000

    We can simplify this code, actually

commit f99a836c669626e5a5f7aa39a2244cfaf71e6fec
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Mar 21 08:10:04 2019 +0000

    This line is misleading

commit 2a6a41c88ea0d0987ac7e750e75f6daaa92cbf6f
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Mar 21 08:07:45 2019 +0000

    Remove an unused variable

commit d83bbaa4fcc51da7e02f60e2d05d68e22624a49b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Mar 21 08:00:58 2019 +0000

    Add some newlines for clarity

commit 81abf3067da1acda3d0f9fac3f56b79ac2ba2c70
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Mar 21 08:00:22 2019 +0000

    Get the remaining methods working in the template

commit b3a76edadb42e264dd10c9d1c4e3923ddf3eec4e
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Mar 21 07:51:22 2019 +0000

    Strip out a bunch of tweet-related code I don't need

commit ee4dfd53629e60482dca0dd56d23391aa0d0ac0e
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Mar 21 07:31:59 2019 +0000

    WIP: Use HTML templates to render tweets

commit 3959273de6dee30946004675baa4185a17efb892
Merge: e84bcd90 9913bc84
Author: github-actions[bot] <github-actions[bot]@users.noreply.github.com>
Date:   Tue Mar 19 13:20:44 2019 +0000

    Merge pull request #239 from alexwlchan/add-categories

    Start organising the “all posts” page by category

commit 9913bc84eb106d433f9e8617ac9949643191d487
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Tue Mar 19 10:40:09 2019 +0000

    Bump the published Docker image

commit 97fba501c0ae4cf673083ed7f1341ad7ff6a849b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Mar 19 09:09:22 2019 +0000

    Slightly tweak the appearance of year/month archives

commit 025f1abbd0862f667a77beea823b6bfa066ec246
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Mar 19 09:08:51 2019 +0000

    Link to the category from the post metadata

commit f936dcd4fc79ddfc5804d6b89157f64ae4b2db2b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Mar 19 07:53:46 2019 +0000

    Push the "everything else" category to the bottom

commit 1c8a94532695c5d8071101874cc68c128c7387eb
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Mar 19 07:25:37 2019 +0000

    Add categories to more posts

commit d8f64aa832640ee34b494330af2d6831b4b1abf5
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Mar 19 06:59:18 2019 +0000

    Assign more categories to posts

commit 8c2c15b5a4c1f5059fda4ce33a89e3bfbc5322aa
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Mon Mar 18 19:11:46 2019 +0000

    Create an archive page, and assign some initial posts

commit e84bcd901a482006fda0f8b57ad3ee386d83880e
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Mar 17 07:53:03 2019 +0000

    Add a couple more referrer aliases [skip ci]

commit 67f411a4d04cdd15f9df4523ad5c99763f478c5f
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Mar 17 07:49:24 2019 +0000

    Fix the nginx references [skip ci]

commit 91dfa3ea87f04f0bf685ff910dfcf6406397dff7
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Mar 17 07:48:11 2019 +0000

    Apparently people are hot-linking to these images? [skip ci]

commit 2353c159f7043f09629008dded12edfd78493417
Merge: 41cff025 c3156cde
Author: github-actions[bot] <github-actions[bot]@users.noreply.github.com>
Date:   Sun Mar 17 00:33:14 2019 +0000

    Merge pull request #238 from alexwlchan/responsive-images

    Allow a gradual resizing of wide images when resizing the window

commit c3156cde43e8253333e738da933a4c4af34babd6
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Mar 17 00:26:35 2019 +0000

    Allow a gradual resizing of wide images when resizing the window

commit 41cff025ed1072bc4b9d9a54fc6129cf64b6c4c4
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.fastmail.co.uk>
Date:   Fri Mar 15 22:02:51 2019 +0000

    Publish new post forth-bridge.md

commit a8ed1920439b9a952dd43d3ca4473c794b721a6c
Merge: a608a9d0 70391edb
Author: github-actions[bot] <github-actions[bot]@users.noreply.github.com>
Date:   Fri Mar 15 22:00:34 2019 +0000

    Merge pull request #237 from alexwlchan/forth-bridge

    Add a post with my Forth Bridge photos

commit 70391edb67f1ce3fab9718fb0b86dda9e4624616
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Mar 15 21:56:43 2019 +0000

    final couple of markups

commit 2dfdf40e51de3a4c2deca2529edaa69bbbcaab5a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Mar 15 21:44:59 2019 +0000

    Add some social media metadata

commit 950dd5986250630d3a49b32543b379f1528c8619
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Mar 15 21:36:20 2019 +0000

    Markups on the Forth Bridge post

commit a608a9d0232cab4845b919d1dd9cae33f8968182
Merge: 41e1a211 b0f2ed5f
Author: github-actions[bot] <github-actions[bot]@users.noreply.github.com>
Date:   Fri Mar 15 11:22:43 2019 +0000

    Merge pull request #236 from alexwlchan/simpler-docker-image

    Slightly simplify the Docker image and make it easier to debug

commit b0f2ed5f190070d9b1f41ba229c048a9744ccb87
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Fri Mar 15 11:19:06 2019 +0000

    Verbosity is always helpful!

commit 76d5ba66acfdbfd3e0d323e77f93b68febd2a365
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Fri Mar 15 11:11:31 2019 +0000

    Images are prebuilt so optimisations for CI can be ditched

commit 78f3ecc6890dca0dba6e1f2a39b48102420f3b0f
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Mar 15 09:45:37 2019 +0000

    Add all the images and initial draft for my Forth Bridge post

commit 5747a6ae97003010b7b67ac899dca2b91ce05b8d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Mar 14 12:43:42 2019 +0000

    Add alt text to one of the Skeletor images

commit 41e1a211d16d491c58d07c239b20f9b91ca0204a
Merge: 490cd36d 38f7ca51
Author: github-actions[bot] <github-actions[bot]@users.noreply.github.com>
Date:   Thu Mar 14 07:50:07 2019 +0000

    Merge pull request #234 from alexwlchan/add-image-attrs

    Add attribution to a few more images, and ditch the {% wide_image %} tag

commit 38f7ca512b16c81d89e273de69df79e767b37d35
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Mar 14 07:44:06 2019 +0000

    Add alt text to all uses of the {% wide_image %} tag

commit e1d17b9b7541a6b8465c57a79be32dad887f1f8d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Mar 14 07:23:12 2019 +0000

    Add alt_text to a bunch of the {% wide_image %} tags

commit 143dfcb467778d0e7044484b1876b148c306cde5
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Mar 14 07:14:06 2019 +0000

    Make the href of the img explicit

commit 625049a1610d0a22d3177c5359e2eb27d77dde05
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Mar 14 00:18:06 2019 +0000

    Start getting wide images working with srcset

commit 93a1e2c41f2a2bd70dc7fae0b8dd26090790bb54
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Mar 14 00:04:46 2019 +0000

    Locate the matching image file from the _images dir

commit 5d50cd3505cc98a210943f6028ceabd9fece9b75
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Mar 13 20:20:56 2019 +0000

    Fix a typo in the alt text

commit e7e9c616e0ebcfab0a21a06e0f28687740ff79c2
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Mar 13 20:20:50 2019 +0000

    Render arbitrary key-value pairs in the {% image %} tag

commit 9603472c70098d2a3bad31215deeb5f0b2d1cd1c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Mar 13 20:15:57 2019 +0000

    Remove an unnecessary leading / in the Docker volume

commit 490cd36ddeff355c73a3eeff4b02781da10e10d7
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Mar 12 06:49:03 2019 +0000

    Add some more analytics config [skip ci]

commit 307af63bce0c2871e9b3ce40279e509b74c40f55
Merge: 9dcb4ffa 6eff08da
Author: github-actions[bot] <github-actions[bot]@users.noreply.github.com>
Date:   Mon Mar 11 20:33:56 2019 +0000

    Merge pull request #231 from alexwlchan/copyright-footer

    Fix the year in the copyright footer

commit 9dcb4ffa21d3bd6a829c28c3ff5917c0f7cd1a80
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.fastmail.co.uk>
Date:   Mon Mar 11 20:31:17 2019 +0000

    Publish new post finding-the-latest-screenshot-in-macos-mojave.md

commit 6eff08da2c085a6dc1950ce0dedfd47d47948a82
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Mar 11 20:30:31 2019 +0000

    Fix the year in the copyright footer

commit f58ee4dd60dadb71741baca09e930d1102807181
Merge: 18a169a8 60200c28
Author: github-actions[bot] <github-actions[bot]@users.noreply.github.com>
Date:   Mon Mar 11 20:29:08 2019 +0000

    Merge pull request #230 from alexwlchan/finding-the-latest-screenshot

    Add a post about finding the latest screenshot in Mojave

commit 60200c28b9808a6622ca980517c0b3760ac16da3
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Mar 11 20:25:26 2019 +0000

    Add a post about finding the latest screenshot in Mojave

commit 18a169a857aa4dbf264178301d920d4f5f5150c3
Merge: e13df0ae f1d43442
Author: github-actions[bot] <github-actions[bot]@users.noreply.github.com>
Date:   Sun Mar 10 23:57:19 2019 +0000

    Merge pull request #229 from alexwlchan/azure-readme

    The README should point to Azure, not Travis

commit f1d43442a1d044d0ed8d84717aaea52373a82fb4
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Mar 10 23:52:18 2019 +0000

    The README should point to Azure, not Travis

commit e13df0aea045f366898110fbae404a41dbf38cbc
Merge: 59d187c0 06e2d8fb
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Mar 10 23:44:53 2019 +0000

    Merge pull request #227 from alexwlchan/use-external-workflow

    Use the workflow defined externally

commit 06e2d8fb327b41ecde08795a21eec3468110b81b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Mar 10 23:40:15 2019 +0000

    Use the workflow defined externally

commit 59d187c0237ab9195dabc1293ed4cb49b79368ea
Merge: 879f6233 0d4c7bbe
Author: github-actions[bot] <github-actions[bot]@users.noreply.github.com>
Date:   Sun Mar 10 23:32:22 2019 +0000

    Merge pull request #226 from alexwlchan/fix-ref

    Extract the API base URL properly

commit 0d4c7bbeabc1d43b0e55808d92b28ceca50ce315
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Mar 10 23:28:27 2019 +0000

    Extract the API base URL properly

commit 879f6233f982fb347d2cf57557cec8ba26b75133
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Mar 10 23:27:47 2019 +0000

    We don't need the jessfraz workflow now [skip ci]

commit 859a6758a411766b5fe44f64aad0ecfdd4226080
Merge: ab04feb1 7253cd00
Author: github-actions[bot] <github-actions[bot]@users.noreply.github.com>
Date:   Sun Mar 10 23:25:44 2019 +0000

    Merge pull request #225 from alexwlchan/delete-branch

    Clean up the branch when the Action completes

commit 7253cd00fcc53ea8a9035ae3bba1fa14e68665e6
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Mar 10 23:22:14 2019 +0000

    Clean up the branch when the Action completes

commit ab04feb18dd8ae607a318e6208d1094d845b8282
Merge: c47377f8 7fbb29fd
Author: github-actions[bot] <github-actions[bot]@users.noreply.github.com>
Date:   Sun Mar 10 23:20:37 2019 +0000

    Merge pull request #224 from alexwlchan/cleanup-gitignore

    Clean up an unused entry from the .gitignore

commit 7fbb29fd8090aecf9f29de339233627930db4758
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Mar 10 23:17:10 2019 +0000

    Clean up an unused entry from the .gitignore

commit c47377f897e6f6c096b15d95ff0d37ec83b4a574
Merge: 3ee734fa 2985cc73
Author: github-actions[bot] <github-actions[bot]@users.noreply.github.com>
Date:   Sun Mar 10 22:55:29 2019 +0000

    Merge pull request #222 from alexwlchan/auto-merge-branch-redux

    Use GitHub Actions to automatically merge my pull requests

commit 2985cc736c861e93924ffd27359a76a3333585ab
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Mar 10 22:52:11 2019 +0000

    That should be a PUT request, not a GET request

commit da583a4d05f285ba9f14618a895ecc8d6bc0951a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Mar 10 22:43:24 2019 +0000

    Add the remainder of the PR logic

commit 52ab071df8fd6a1b0c619b7fefa713093f39cf5a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Mar 10 22:31:57 2019 +0000

    that should be 'success', not 'succeeded'

commit 022400502b81b26864f5db431b80594c51e6a6bd
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Mar 10 22:25:30 2019 +0000

    Return a neutral status code; query PR data

commit 112a67b91fe8e5c32b5173bfe9e517bcb41d1c08
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Mar 10 22:18:18 2019 +0000

    Skip the auto_merge_branch script if the PR is incomplete

commit 3ee734fae6943a3b9971fb9644c4c716457386b5
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Mar 7 16:42:43 2019 +0000

    add the auto_merge_branch action

commit 51af1191db58eadcee93d73187898d3ef30a28a5
Merge: 460ab18e f16663a3
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Mar 7 16:27:05 2019 +0000

    Merge pull request #220 from alexwlchan/alexwlchan-patch-1

    add check_run event to workflow

commit f16663a37cedcc9ef0c1fd6618487919d4506859
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Mar 7 16:23:30 2019 +0000

    add check_run event to workflow

commit 460ab18edf92dbe6136dba84bed73b11ed5ca0b8
Author: Azure Pipelines on behalf of Alex Chan <azurepipelines_git@alexwlchan.fastmail.co.uk>
Date:   Sun Mar 3 23:48:32 2019 +0000

    Publish new post atomic-cross-filesystem-moves-in-python.md

commit 298d85d58063237da2c630d41772ce31273e4827
Merge: 6504cf04 6c45ce2e
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Mar 3 23:46:28 2019 +0000

    Merge pull request #219 from alexwlchan/atomic-move

    Add a blog post about atomic, cross-filesystem moves

commit 6c45ce2edb9d07a6eb96bb2864a2b55c6c8f4b80
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Mar 3 23:40:45 2019 +0000

    Apply review markups

commit 3d4b640b43678d34f694b9831ae85cb1921dbc74
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Mar 3 23:39:38 2019 +0000

    Initial draft of a post about atomic, cross-filesystem moves

commit 6504cf045699c1571f9578013cda87ce98e15d29
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Mar 3 23:43:30 2019 +0000

    When a PR gets merged, clean up the branch

commit 5b6b9f10c906f1b11269b7916d420f5e1c7f3f33
Merge: 35f4ffde 1ba107e5
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Mar 3 16:46:22 2019 +0000

    Merge pull request #218 from alexwlchan/better-images

    Add a plugin for images with alt text; start adding alt text to old images

commit 1ba107e5402c30a7d6293fa2b80d12792c35c1e5
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Mar 3 16:02:59 2019 +0000

    Don't forget the require_relative here

commit d879f9198c5e8aa48615fa1c41398da2db34a45d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Mar 3 15:08:37 2019 +0000

    Alt text on a few more images

commit d72318d4fecbfb1b76d3462ef62999078d86113f
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Mar 3 14:55:03 2019 +0000

    Start adding alt text to images

commit 0f23b73a2ee850b9faf77df15bd0630c45e6d27a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Mar 3 14:38:03 2019 +0000

    Add a Jekyll tag for rendering images

commit 1a7af6f740c2070af2a8dd38c2772f062113abe1
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Mar 3 14:18:04 2019 +0000

    Rename the slide plugin for better_slide/slide

commit 2a80165071b1b04eb8b6008bacc834cb13928b12
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Mar 3 14:17:02 2019 +0000

    Add a helper method for rendering images

commit 35f4ffde7929790f76d917556bf91dde7543f42f
Merge: 5a68c4f7 06a767b6
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Mar 3 10:03:45 2019 +0000

    Merge pull request #217 from alexwlchan/fix-broken-link

    Fix a broken in the S3 pagination post

commit 06a767b63f4ab034c08e1d66b34f0b5deb6f83b1
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Mar 3 09:54:37 2019 +0000

    Link to a fixed GitHub commit for this code

commit dfe5b741c7c7d8c231ddaf088be6a831290de3c7
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Mar 3 09:53:46 2019 +0000

    This script can go in the "misc" folder

commit 121e24a458c30180d4395c65b3f5704fe4784cea
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Mar 3 09:53:25 2019 +0000

    Put the S3 object code back

commit 5a68c4f7e68afc7fed432f4a1bcd4430c05d5260
Merge: 29eea4ba 9df6a56b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Mar 3 09:48:42 2019 +0000

    Merge pull request #216 from alexwlchan/all-slides-alt

    Add alt text to all the remaining slides

commit 9df6a56b64b6613a24b841da931f8969888a5ea8
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Mar 3 09:44:24 2019 +0000

    We can ditch the old, alt-text-less slide plugin

commit 83e5742c7fd8fe86e2b74f939acf22f7a71b16cf
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Mar 3 09:41:37 2019 +0000

    Add alt tags to my remaining slides

commit 29eea4ba26c2dddf68977c0df8e958c7209cde98
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Mar 3 08:51:12 2019 +0000

    Add a few more referrer aliases

commit f3bfd88317905c4726007f0430ac9f49a106d51a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Mar 2 18:43:39 2019 +0000

    Update README badge to point at Azure [skip ci]

commit 050460694eaff5b56a626b71753ee107bba5ac50
Merge: 64de6e97 e6ab4624
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Mar 2 18:39:04 2019 +0000

    Merge pull request #212 from alexwlchan/anti-social-media

    Add alt text to the slides in anti-social-media

commit e6ab46248d7936ed37421404f339b290c4f7cad7
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Mar 2 09:03:14 2019 +0000

    add some indentation to trigger a build

commit 7411a65bb3a32152b144685bef4de0088e01b72a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Mar 2 08:42:53 2019 +0000

    Fix the rest of the slides in that post

commit 3166ccc14a3249a13380a41bd941d874e5eab87d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Mar 2 08:29:00 2019 +0000

    Add alt text to the slides in anti-social-media

commit 64de6e97d331a4d90a76ac50e1605285a859ff75
Merge: 1ad6d24e 2b9a6ec0
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Mar 2 18:33:58 2019 +0000

    Merge pull request #215 from alexwlchan/publish-docker-images

    Use pre-built Docker images in CI

commit 2b9a6ec061d48e89d2b220b8d71d7b0050dbddf8
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Mar 2 18:31:21 2019 +0000

    image = name + version

commit 1ad6d24e74652a0dd874414599180569dc1a89dd
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Mar 2 18:29:11 2019 +0000

    Remove my old Travis and Mergify config

commit fd851b1e3ff70f4f94e28627e5b363e643916a16
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Mar 2 18:27:09 2019 +0000

    Now actually publish the image

commit 059bb33cd42d3290440b4b2e2b80ec065758353c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Mar 2 18:15:55 2019 +0000

    Initial script for publishing Docker images

commit 24dfe7329a57c7e86b33195f72580808dab02357
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Mar 2 18:07:14 2019 +0000

    this should be an empty file, not a dir maybe?

commit e19b098820d3cd749cad1c90e5d29bc24beed86d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Mar 2 17:56:37 2019 +0000

    is this what I need for gitconfig?

commit 3a9a176ab4dd2bfbde36eba0c137b97a9cc18578
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Mar 2 17:50:26 2019 +0000

    Those do need to be in global gitconfig

commit 14f095f302c650e668f3b90118684773004943b1
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Mar 2 17:49:35 2019 +0000

    we do need to create the ~/.ssh directory

commit c7e8f5be421bf65d88a355e92d68410ff9f73068
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Mar 2 17:44:26 2019 +0000

    get azure pipelines to deploy to github!

commit 2b2857ad6423f221824f626ca2ec2cdd2dcd6044
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Mar 2 17:42:41 2019 +0000

    Add github to the list of known hosts

commit d482b6e7810f0ed59e9e63e99e38c056c336b5a5
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Mar 2 17:33:33 2019 +0000

    even more debugging guesses

commit 7e168cc3abb30af76a495aeb534153c9512e0aa7
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Mar 2 17:29:57 2019 +0000

    is this file correct?

commit bc6cc43d5e60b756db793b782bb1e70fd51551df
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Mar 2 17:26:49 2019 +0000

    maybe we don't need this config?

commit 52b666940bb3630dec97c075d50db9593192e535
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Mar 2 17:23:26 2019 +0000

    don't bother building, just do the git sync

commit a9a39339ecf5f0eed0793b593172542d88e3ee8a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Mar 2 12:35:30 2019 +0000

    verbose git push to debug

commit ed2d701e14ae444cb4aa6463eedcefcca841928b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Mar 2 12:27:26 2019 +0000

    Sort out the Git SSH key config

commit 780f7464baf8a13cdbd9dd9dbca835a2be78c13a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Mar 2 12:22:08 2019 +0000

    construct the SSH key another way

commit 6aa5821d81143c38bda96f52ebe92f49a292f80b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Mar 2 11:38:32 2019 +0000

    don't print the SSH key to stdout

commit 7cd6329336b9dfe11a79dacceebebab33d518e47
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Mar 2 10:59:29 2019 +0000

    try a bash substitution

commit 6fd6c42464baf103e7744221728d21f689c41c84
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Mar 2 10:55:33 2019 +0000

    where are the newlines?

commit ce7ae41169a26d6039f31607049ad6c5c6bf3807
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Mar 2 10:49:15 2019 +0000

    I need to build to deploy, so nvm

commit 2066e340e2cb3775944f9a25645394c3350beb28
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Mar 2 10:46:28 2019 +0000

    skip the build while I debug the config

commit 381e852402ffb43d116a5c261f4c732ee4c8d65d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Mar 2 10:43:58 2019 +0000

    fix the python syntax

commit 07de4ed80dd45b2aa58737c6ae59ac65d92662e1
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Mar 2 10:34:44 2019 +0000

    what's being written to the id_rsa file??

commit 9fc9792c712fe4cef9c2b4e629f72c2ab7b6c4a0
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Mar 2 10:25:10 2019 +0000

    another go at creating the SSH key

commit d35f32279186378ff08b336ebfe536301a0c757a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Mar 2 10:14:40 2019 +0000

    create the key before docker creates a directory

commit 8374d6c628f89e4f917ed23245948de7ac7e6ff6
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Mar 2 10:02:46 2019 +0000

    fix the ssh key path

commit d4168b2c20a2f48097c0065f458b8a3036b59204
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Mar 2 09:56:55 2019 +0000

    create an empty gitconfig

commit bc72a33fd9528cddfacc15275e9fa445e5550f1a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Mar 2 09:50:46 2019 +0000

    drop in the SSH key

commit 5dd30ff5807005f73986c8b94ff23d9c0bae0133
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Mar 2 09:49:25 2019 +0000

    wassup with the gitconfig?

commit 0e91d0ed0a3ea8ed66788ae65ef5cabe3184216d
Merge: cbd925bb d42b80e2
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Mar 2 09:41:43 2019 +0000

    Merge pull request #213 from alexwlchan/better-azure

    Try setting up deployments through Azure Pipelines

commit d42b80e2eb5d12e8e5e2bd8b0f41fd1cfcf4e46c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Mar 2 09:36:49 2019 +0000

    Add displayName to the deploy task

commit 2b978865fd8735bc3316c90a72fd3523fa5dbe97
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Mar 2 09:36:08 2019 +0000

    Add a displayName to the build task

commit 14e1eed84499c93cadfec540d722407bbb6e5ae1
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Mar 2 09:34:29 2019 +0000

    remove the displayName

commit 41a3441d01e10fb2f42fe761b21ee25e7267fb00
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Mar 2 09:32:21 2019 +0000

    remove a bit of unused yaml

commit 3c6aa12aa4aad12311f70183230cbc5646986cf5
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Mar 2 09:31:05 2019 +0000

    single job, conditional step

commit b18dbbe2169a5ff2287df00783770cfcbdb47df8
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Mar 2 09:25:41 2019 +0000

    Maybe this shouldn't be de-dented?

commit 187c0a13731172f830f87cc449875c6357ddbd7f
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Mar 2 09:21:07 2019 +0000

    Try setting up deployments through Azure Pipelines

commit cbd925bb68abbb83c39120b65aa5b3df74858596
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Mar 2 09:08:37 2019 +0000

    Set up CI with Azure Pipelines

commit 84f36f6305e1eb02a85fd637869ce37752f9b3b5
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Mar 2 08:35:01 2019 +0000

    okay maybe check_run after all?

commit 6cb253bd6207065324929f103486d4a47fd54ab6
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Mar 2 08:01:14 2019 +0000

    Revert "rip out github actions"

    5dc6d94a8441613cdadee0de9d023d63cd0fadc5

commit c3ac5982ba3bf7c902e4ffbe7f6c169d0aece4fc
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Mar 1 21:50:36 2019 +0000

    rip out github actions

commit d706115fd32d28ce267e702af1721b8f67969be7
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Mar 1 21:47:52 2019 +0000

    maybe check_suite is what I wanted?

commit 2131babfbfe9bbaa16959df211771de7689e077d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Mar 1 21:38:52 2019 +0000

    on pull request pass, merge the branch

commit 419a37e6f7c53f249f467ad2b2c3468a24efeffc
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Mar 1 21:37:01 2019 +0000

    Add some pieces for merging a branch

commit d6a48d60052d63ddf99862d60dfce460151bd92f
Merge: 04ebc267 743ecd12
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Mar 1 21:34:18 2019 +0000

    Merge pull request #210 from alexwlchan/cleanup-workflow

    Let's delete this old workflow file

commit 743ecd125baa0cf73428ee0c4b7de2d7a13dc9a3
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Mar 1 21:33:28 2019 +0000

    Let's delete this old workflow file

commit 04ebc267906181b789bee7f9da94bf4f907a8b9a
Merge: c8410112 6885e2d9
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Mar 1 21:28:59 2019 +0000

    Merge pull request #209 from alexwlchan/more-html-proofer-fixes

    Add alt text for the slides for my suspicious minds post

commit c8410112c888483df41cd5d203563975f6584a23
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Mar 1 21:28:16 2019 +0000

    Another go at defining the workflow

commit 6885e2d9fd2a464ba483227c1cd36d1c4ea0e999
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Mar 1 20:37:53 2019 +0000

    Add alt text for the slides for my suspicious minds post

commit 20f30147b06aeb2c0445e51364d1acde3112ebb3
Merge: da2aa922 d28e6909
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Mar 1 13:31:45 2019 +0000

    Merge pull request #208 from alexwlchan/more-html-proofer-fixes

    Use the {% slide %} plugin for my Hypothesis intro slides; convert to a blog post

commit d28e69094f12a9d8fb7f83f01b12e91e4bbbe2cd
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Mar 1 13:06:05 2019 +0000

    Use the {% slide %} plugin for my Hypothesis intro slides; convert to blog post

commit da2aa922f2e7027c6460adaa22808eb4210e73e2
Merge: 8a001394 fef0bb85
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Mar 1 10:36:24 2019 +0000

    Merge pull request #206 from alexwlchan/more-html-proofer-fixes

    Some more fixes for HTMLProofer and accessibility

commit 8a001394b76ab654774eb568d075f9ae654a01c4
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Mar 1 10:36:18 2019 +0000

    On pull request merge, delete the branch [skip ci]

commit fef0bb852a1f8c1ff88ed27e97353b99334075c9
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Mar 1 10:25:40 2019 +0000

    Fix a couple of broken links

commit cda866abc5f293a75634da12513eff1ff06a1327
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Mar 1 10:25:04 2019 +0000

    Add alt text to the slides in "assume worst intent"

commit 2f492794fdc868a080bb2d9bebd7a630f8c2baca
Merge: 389d4849 d9adfad4
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Mar 1 07:36:55 2019 +0000

    Merge pull request #204 from alexwlchan/better-slide-tag

    Add a {% slide %} tag that requires alt text

commit d9adfad42a5f4abb4f07fb2b0c811aa0529a87ec
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Mar 1 07:29:38 2019 +0000

    Don't forget to check in the new plugin base!

commit 39c886c280d14789e5f29f55476a40fda86044bf
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Mar 1 07:15:42 2019 +0000

    Add alt text to all the slides from my Monki Gras talk

commit a0d5987ff943c47246c396c874b875a92a54035d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Mar 1 07:15:12 2019 +0000

    Add a new slide plugin that requires alt text

commit 389d4849ef611846d3e0071bdb92d5551ccadff6
Author: Travis CI User <travis@example.org>
Date:   Tue Feb 26 20:27:45 2019 +0000

    Publish new post checking-jekyll-sites-with-htmlproofer.md

commit 772ce719fb18f4c556934a400ba5f2cd187e777a
Merge: fe4a5a29 323e22ab
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Feb 26 20:24:33 2019 +0000

    Merge pull request #203 from alexwlchan/reduce-pages

    Add a post about HTMLProofer; move a few more files around

commit 323e22ab94c389ba409c72c12b24679c8fa3f883
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Feb 26 20:04:33 2019 +0000

    Add a short post about using HTMLProofer

commit 3268f8af84cf44621f7b06e821f7ef4f53202ad9
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Feb 26 19:42:30 2019 +0000

    Move around a bunch of the maths PDFs

commit 1e900855ac0b4c9512551fbebe2426d6f84fb205
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Feb 26 19:39:40 2019 +0000

    Add more quoting to _config.yml [skip ci]

commit fe4a5a294de878451ea8aec15e81c8a3f041b616
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Feb 26 19:34:57 2019 +0000

    Add alt text to a few more images

commit 1fd491860e7797a8e9b30dc99b906a2e5f265700
Merge: 847b0f78 6c344728
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Feb 26 19:18:44 2019 +0000

    Merge pull request #202 from alexwlchan/simplify-files

    Simplify files and the site structure

commit 6c34472874d62d307206fd258ba1e56b7332d882
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Feb 26 18:56:58 2019 +0000

    For now remove all the checks in Travis

commit 595e33aaaaa24ef87362b15ce0c2ba9a83b9fbfd
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Tue Feb 26 17:34:35 2019 +0000

    Remove a few more Makefile pieces

commit de58c68229638d4476f54fb49fc755c6dec7e2a7
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Tue Feb 26 17:31:27 2019 +0000

    Remove the old test machinery

commit 3137276fe5f2e0d68efade709a0467e2fbdb50e8
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Tue Feb 26 17:30:25 2019 +0000

    Add html_proof to the plugins/build

commit b25fa86077ea56e30fbaa730bd1cf2870ab76517
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Tue Feb 26 17:06:36 2019 +0000

    ???

    Okay, let's try that again

commit 0b6bd17c9d3d2d7333b6c2575ae495e70de65307
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Tue Feb 26 16:55:54 2019 +0000

    Why is the server failing?

commit 847b0f786c56e560d22d8afa29f9b0e3f783181a
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Tue Feb 26 16:56:41 2019 +0000

    Revert "Why is the server failing?"

    2d75bed917a15ba9dd6ba9ea2645e580bea8cd4f

commit 57b1102446adf141beaabd0c95bca224650495b0
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Tue Feb 26 16:55:54 2019 +0000

    Why is the server failing?

commit d01f46bf337769a196934cae5bfa4168b3231a19
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Feb 26 07:14:30 2019 +0000

    Front-load container pull/build

commit 35601ed084a9d47ba3b170666b1bd43184d190f8
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Feb 26 06:39:35 2019 +0000

    Just ditch the front-matter checks

commit 611a947cb1f069f4750eec14af9fc1e9da6feb30
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Feb 25 22:47:37 2019 +0000

    expunge more micropost complexity

commit 0155a1afa571605b1de10c8a721587d3a0cea884
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Feb 25 22:44:52 2019 +0000

    Yank all the microblog stuff

commit 93db467db4a553b5785cd542544239c896ff40bb
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Feb 25 22:41:21 2019 +0000

    Consolidate the /videos into /files

commit f6347e5be2f7b87798970d2f67879b119ea0afbf
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Feb 25 22:38:57 2019 +0000

    Consolidate the files directories

commit 3fcc8ba0ae7a7b83c2ca8fe69b4c3623039c6495
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Feb 25 22:31:39 2019 +0000

    Move a bunch of files out of /slides/ and into /files/

commit c4f17407c0249818a47bd25ce5e53eb59981cd06
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Feb 12 21:26:32 2019 +0000

    better summary

commit 6c0a9a22f0e4391675f85c11a7557654d7722408
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Tue Feb 12 17:34:24 2019 +0000

    Add a link to the published video

commit 1d0da911026258d32d074f3c8af15d1948ba65dc
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Feb 9 18:20:12 2019 +0000

    even better summary

commit 0725162ce47ad7e5b3dc8da532153e83837e1689
Author: Travis CI User <travis@example.org>
Date:   Sat Feb 9 18:09:32 2019 +0000

    Publish new post working-with-large-s3-objects.md

commit ff6847f6a46729db419016c3e9a2babe75f4bc00
Merge: 7e7c1272 438ec1b9
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Feb 9 18:01:51 2019 +0000

    Merge pull request #201 from alexwlchan/large-zip-file

    Add a post about working with large objects in S3

commit 438ec1b9891eedb8099501f1d5b1c8c5134d6ebd
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Feb 9 17:54:11 2019 +0000

    Improve the summary

commit 7d68423e3281818811153135483045ccf45991bc
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Feb 9 17:53:25 2019 +0000

    Fix the email in the footer

commit 752b1b955f2dbc168e9d333b8abc6e794e4645c0
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Feb 9 17:53:18 2019 +0000

    Add a post about working with large objects in S3

commit 30f999d400036fed6f3e7680c594b25068662755
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Feb 8 08:30:08 2019 +0000

    Add a post about reading large files from S3

commit 3221736583a7722f08fd48bb7dc2f5d285d08761
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Feb 8 08:30:00 2019 +0000

    Allow numbers in post slugs

commit 7e7c1272be65018649835e06f4b86af400573c55
Author: Travis CI User <travis@example.org>
Date:   Tue Feb 5 09:04:12 2019 +0000

    Publish new post inclusive-events-redux.md

commit 4a05cabaab4425f3a2b7b9b9de2227564c5029b8
Merge: 67a68bee 9913ff31
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Feb 5 08:56:56 2019 +0000

    Merge pull request #200 from alexwlchan/new-inclusive-events

    Quick update to point to the new inclusive events guide

commit 9913ff31f4f82ffa38fd6a354788530dfcc2a0b9
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Feb 5 08:48:13 2019 +0000

    Quick update to point to the new inclusive events guide

commit 67a68bee78368069e6f7977a68373c700289f650
Merge: bc013dbf f62d96cd
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Feb 3 22:19:31 2019 +0000

    Merge pull request #199 from alexwlchan/monki-gras

    Add a placeholder post for Monki Gras resources

commit f62d96cd5451c8b51dea8ebd37e5fa3a85344666
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Sun Feb 3 21:38:06 2019 +0000

    And we need python-dev

commit 018785757f16b32fb01283d7298909dad430b54d
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Sun Feb 3 19:47:39 2019 +0000

    just throw in build-base for now

commit 52d103ce0d3f21ed278c1cd3eb022330351c42f9
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Sun Feb 3 19:34:24 2019 +0000

    Try to get the tests building correctly

commit ebe59754c3415750e9a137a62a55edc7b13b33d2
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Sun Feb 3 19:19:51 2019 +0000

    Add another directory exclusion

commit 224707e7c41189fd2484db246302090e27734011
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Sun Feb 3 19:05:31 2019 +0000

    Fix a daft mistake

commit f7e2a6c6f021f37ab5f882eebb82d02cdf81457f
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Thu Jan 31 21:10:32 2019 +0000

    Okay, now add all the notes and links

commit a21bcc796536d15f575a040b7270d3750ff3cc61
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Thu Jan 31 20:50:43 2019 +0000

    Add a bunch of notes to the Monki Gras talk

commit f404dd0fdcc7bce635555aa4b3510f5dcd5a3f8a
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Thu Jan 31 15:41:14 2019 +0000

    Add quotes so the YAML works

commit 89a0934d478450041884f111e1fb231e28493066
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Thu Jan 31 10:03:41 2019 +0000

    Publish new post monki-gras-the-curb-cut-effect.md

commit 3ce52067e56bde7dd0f612667fbf4a32c9d4ceb5
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Thu Jan 31 09:54:40 2019 +0000

    And libxslt

commit 6160458f83e06fb6c1e5d571534848549d9554d9
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Thu Jan 31 09:11:58 2019 +0000

    just add build-base for now

commit 00465a9bf778fcdaab4ea929d6282cf8c89037f0
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Thu Jan 31 08:11:07 2019 +0000

    Add a placeholder post for Monki Gras resources

commit bc013dbfb1dadb153383970c229c37b4dbffa515
Author: Travis CI User <travis@example.org>
Date:   Tue Jan 29 16:07:28 2019 +0000

    Publish new post debugging-a-stuck-terraform-plan.md

commit a5ab7bde0dcf7cb049b04deac029930717d753de
Merge: 6fcdd6d4 1524ecde
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Jan 29 16:01:48 2019 +0000

    Merge pull request #198 from alexwlchan/stuck-tf-plan

    Add a quick post about debugging a stuck TF plan

commit 1524ecde1165574c23a790f7ef1c56fc06632e13
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Tue Jan 29 14:45:05 2019 +0000

    Add a quick post about debugging a stuck TF plan

commit 6fcdd6d45082dfa700d13d5a52007ebe47f36144
Author: Travis CI User <travis@example.org>
Date:   Mon Jan 28 13:42:06 2019 +0000

    Publish new post notes-from-you-got-this.md

commit 3e59d39030c60e36345834460b4fa4d5b87ea14d
Merge: 4127f33a 281c7235
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Jan 28 13:36:09 2019 +0000

    Merge pull request #197 from alexwlchan/you-got-this

    Add a post about #YouGotThisConf

commit 281c7235a5b74da460685527f46a22eefec8ab43
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Jan 28 13:18:00 2019 +0000

    Fix some contact links

commit c92561df61c05d05e11255659951663271d03e86
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Jan 28 12:26:53 2019 +0000

    Tidy up review comments

commit e7e6c562d93ba21164eee21330b54cdce4b2f1f2
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Jan 28 10:07:33 2019 +0000

    Finish the first draft of the post

commit a56bcecf7c06e257ee1c56789de6d6dba7846ead
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Jan 23 08:33:07 2019 +0000

    First draft of my notes from "You Got This"

commit 5e240dcf9b1d069400af9ac9d6529b723ffe4e4a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Jan 22 22:02:38 2019 +0000

    Add a micropost about sunlight

commit 4127f33a404d2ede3bdee3467e8ac70f9471ed8e
Merge: 1fd6d5ab 07a80713
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Jan 22 21:39:05 2019 +0000

    Merge pull request #196 from alexwlchan/microblog-2

    Add some initial pieces for microblogging

commit 07a807134f7b356c3d8f46a7f173777aae15425f
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Jan 21 08:37:39 2019 +0000

    And put the word "micro-blog" at the top

commit a45129e8c3ad751da3c82ba731ed93795152be31
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Jan 21 08:29:16 2019 +0000

    Fix the email in the RSS feed

commit 90446b26f752d9d2f74faf07b722d25cd3a03ad8
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Jan 21 08:29:09 2019 +0000

    Let's make that the first micropost

commit 8df6f6961b909f4f6ec018202a1fec0417903c35
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Jan 21 00:06:31 2019 +0000

    Render all the microposts as individual pages

commit 796192b0fb10ba7ca819577eaba37e27d2666e93
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jan 20 23:56:25 2019 +0000

    Start breaking the assumption that every post needs a title

commit e8d188acfac1adb5d9777ee1d19045210e2aa36a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jan 20 23:28:04 2019 +0000

    insert some micropost metadata at build time

commit b6fa8b016e9bae8d40a80474643183671a7e6255
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jan 20 23:21:06 2019 +0000

    Start getting microposts onto the site, and into the RSS feed

commit 21c41dc7eea611dde70b937c8234570e3574f3ac
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jan 20 23:02:39 2019 +0000

    Remove the standalone contact page

commit f7499fae750f0d204e976d937a86b23b02310bea
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jan 20 22:58:10 2019 +0000

    Create id headings for headings with redcarpet

commit 140f3efa37a573ee4e8e3b1cce49a86ca3063436
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jan 20 22:54:33 2019 +0000

    Add a Make task for just the rsync/ssh task

commit 1fd6d5abdebef6242179ea36a5f3c71f65cf5240
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jan 20 22:59:53 2019 +0000

    Redirect /contact to the front page

commit 96141f3f6598701a810f76dc1b65748889f7e990
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jan 20 22:50:14 2019 +0000

    Put contact details on the front page

commit f0af48c01b976089726a2afc78ca3450d7786d19
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jan 20 22:33:07 2019 +0000

    temporarily removed

commit 5e7c9705924511307bb4c177578213661ba2700d
Author: Travis CI User <travis@example.org>
Date:   Wed Jan 16 08:54:08 2019 +0000

    Publish new post paul-rothe-and-sons.md

commit 32c36f3b0fcec231994e57d529d32fb123523e6b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Jan 16 08:49:13 2019 +0000

    Create the per-year directory in _posts if it doesn't exist yet

commit 2b4c83a1e53a499a6fcac04c8d52baaecc6501b0
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Jan 16 08:47:34 2019 +0000

    Improve this URL slug [skip ci]

commit f31181fdc4e4da1244107e7aa46139750e58edf3
Merge: fa2fd84e 4c0014db
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Jan 16 08:02:34 2019 +0000

    Merge pull request #195 from alexwlchan/paul-rothe

    Add a quick post about Paul Rothe & Sons

commit 4c0014dbf3436f5bfd18ed89b8898ad32257657d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Jan 15 23:18:13 2019 +0000

    wording tweak

commit ec05d5ff8057b17a33d8a3eda5a053f6611a0daf
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Jan 15 23:16:56 2019 +0000

    Add a quick link to Paul Rothe & Sons

commit fa2fd84eaf2d261f7d75d0d244afc2dbc1fafcc0
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jan 6 22:09:14 2019 +0000

    Require a review from me to merge a PR

commit 838d4e1b46482bbcd33f1a57506b27137262d34d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jan 6 22:00:40 2019 +0000

    Revert "Dead link and small code change proposal"

    This reverts commit aec15de64b20155cf5fa11301486b35f1a1bc970.

    Until I sort out my Mergify config and can review properly!

commit e58002347c19c9f9abcea1c520f92d51b8b854cf
Merge: 5f3fff5b 47b09da9
Author: mergify[bot] <mergify[bot]@users.noreply.github.com>
Date:   Wed Jan 2 12:31:37 2019 +0000

    Merge pull request #194 from Mofef/patch-1

    Dead link and small code change proposal

commit 47b09da914952459d3b6e59bfe7bfddfaf9fb821
Author: Moritz Münst <muenst@magazino.eu>
Date:   Wed Jan 2 13:26:13 2019 +0100

    Dead link and small code change proposal

    Thanks a lot for sharing :)

commit 5f3fff5bf754644c0f001a8477240da134289e01
Author: Travis CI User <travis@example.org>
Date:   Thu Dec 27 17:38:55 2018 +0000

    Publish new post reading-a-utf8-encoded-csv.md

commit 16a2a4784208dec13168b6a01c4ab6dc5eb30fa7
Merge: 90b18bde b9d786f5
Author: mergify[bot] <mergify[bot]@users.noreply.github.com>
Date:   Thu Dec 27 17:34:23 2018 +0000

    Merge pull request #193 from alexwlchan/csv-parsing

    Add a quick post about my CSV parsing work

commit b9d786f5fd39a390bc7bad8d8175d9a976bee916
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Dec 27 17:28:05 2018 +0000

    Make this a minipost

commit 3b8591996cec935362a4b083489440530b9d6194
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Dec 27 17:27:40 2018 +0000

    Add some notes on reading a UTF-8 encoded CSV in Python

commit 90b18bde8072dea122445bd53543dbf3cda1127e
Author: Travis CI User <travis@example.org>
Date:   Sun Dec 23 22:39:38 2018 +0000

    Publish new post iterating-in-fixed-size-chunks.md

commit 4ed637b8195d08d3b939faaec435b23839750e82
Merge: 14b90dea b1452cdd
Author: mergify[bot] <mergify[bot]@users.noreply.github.com>
Date:   Sun Dec 23 22:34:40 2018 +0000

    Merge pull request #192 from alexwlchan/iterate-in-chunks

    Add a quick post about iterating in fixed-size chunks

commit b1452cdd4dd754b71740dce5cd8bde53c5469f39
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Dec 23 22:27:25 2018 +0000

    Add a quick post about iterating in fixed-size chunks

commit 14b90dea6deb24b2f710eede1ba5ac2fc50a2cf4
Author: Travis CI User <travis@example.org>
Date:   Thu Dec 13 08:57:16 2018 +0000

    Publish new post getting-credentials-for-an-assumed-iam-role.md

commit 00773a514de090f984ebfaf801703fb54d141ae6
Merge: 27a80a3c a3f60da0
Author: mergify[bot] <mergify[bot]@users.noreply.github.com>
Date:   Thu Dec 13 08:52:44 2018 +0000

    Merge pull request #191 from alexwlchan/aws-iam-role

    Add a post about my IAM roles script

commit a3f60da02ed029c19f025962931228767c4a84e6
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Dec 13 08:47:15 2018 +0000

    Markups to "assume IAM role" post

commit 3f6cb125cacf086c2d2adc8bc15409d041b5166b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Dec 13 08:36:22 2018 +0000

    Add a draft of a post about temporary IAM credentials

commit 27a80a3c2bc037ed9f6a1dad35033c3f1ca2703f
Author: Travis CI User <travis@example.org>
Date:   Wed Dec 5 21:17:14 2018 +0000

    Publish new post backing-up-tumblr.md

commit e38437aa12117a7b217ade4075d8780598d922ee
Merge: fca62ca3 4719b086
Author: mergify[bot] <mergify[bot]@users.noreply.github.com>
Date:   Wed Dec 5 21:12:27 2018 +0000

    Merge pull request #190 from alexwlchan/backup-tumblr

    Add a quick post about backing up Tumblr

commit 4719b0863e14e5a1d49f33ebb5712b57920e3f63
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Dec 5 21:06:08 2018 +0000

    Add a quick post about backing up Tumblr

commit fca62ca30380e49ee3bab71eb88784cfeb33111b
Merge: 2263f7d3 93b0aa95
Author: mergify[bot] <mergify[bot]@users.noreply.github.com>
Date:   Sun Dec 2 11:49:02 2018 +0000

    Merge pull request #189 from alexwlchan/bump-dependencies

    Bump test dependencies for GitHub security alerts

commit 93b0aa9575179fb87fd79639fb155fd39bb1f0e7
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Dec 2 11:44:10 2018 +0000

    Bump test dependencies for GitHub security alerts

commit 2263f7d37b5844efea82e3b1c1aed2bc13710db6
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Nov 14 08:02:16 2018 +0000

    Remove two unwanted Flickr entries

commit 6cd5fbccec7dd3affd46d2b7d8de3a3ee3487b51
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Nov 25 19:47:58 2018 +0000

    Add some more analytics config

commit 35023a15f094ff2500a573d2ff302d99c2615f4e
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Nov 13 20:57:45 2018 +0000

    Tidy up the LaTeX underlines post

commit cc14f85b37c45b071c20b4d06613c6246c113292
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Tue Nov 13 10:59:55 2018 +0000

    Fix a typo in this post

    h/t https://twitter.com/DRMacIver/status/1062298213749850112

commit a818a87c3879abd365c36d42c50b63c649b1656e
Author: Travis CI User <travis@example.org>
Date:   Tue Nov 13 10:44:41 2018 +0000

    Publish new post book-recommendations.md

commit 39fd77e8f8938ac6339dfbd2d89babee694d68c6
Merge: b1f398ed fa4b9046
Author: mergify[bot] <mergify[bot]@users.noreply.github.com>
Date:   Tue Nov 13 10:39:52 2018 +0000

    Merge pull request #188 from alexwlchan/reading-list

    Add a post about my book recommendations

commit fa4b9046edc8b5e58809094b3bb9fbcb90fb5af7
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Tue Nov 13 10:34:29 2018 +0000

    Add a post about my book recommendations

commit b1f398edb2a8c69239732044307a75373d0c752f
Author: Travis CI User <travis@example.org>
Date:   Thu Nov 8 12:37:19 2018 +0000

    Publish new post aberdulais-waterfall.md

commit 6c97ade043234edbc405aaf38f358f14fb093559
Merge: db656b1c 4a4ee684
Author: mergify[bot] <mergify[bot]@users.noreply.github.com>
Date:   Thu Nov 8 12:32:43 2018 +0000

    Merge pull request #187 from alexwlchan/aberdulais

    Add my post about the Aberdulais trip

commit 4a4ee68412b97d6afc3505dbe12530e03e590c8f
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Nov 8 12:22:08 2018 +0000

    Final markups

commit 0b612158a67234915c07e3bd1649d5394e825cd1
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Nov 8 10:14:55 2018 +0000

    Hopefully final draft of the Aberdulais post

commit 428f877d805b86d1c1a51f68da1852a024e09088
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Nov 7 22:59:25 2018 +0000

    First draft markups

commit db656b1cd00a80fd4a190a5a136c594f9ed10a38
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Nov 7 22:37:14 2018 +0000

    Add a bit more analytics config [skip ci]

commit 80d7d97ea6ef80827ac8c4934306eb1b720c3fe0
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Nov 7 22:35:41 2018 +0000

    Use referrers.toml for the Twitter referrers

commit 0b1f8382a021acbeed5f549be16454bf1ad983a6
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Nov 7 22:27:47 2018 +0000

    Don't forget to set the root device! [skip ci]

commit 33294aa3ebf66bf099eab22358ac62d10908078c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Nov 7 22:26:46 2018 +0000

    Make sure to set sda/sdb in the terraform config [skip ci]

commit 9fc1ccefc3bb03f16bd3d441982fc6ba3a750863
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Nov 7 20:49:33 2018 +0000

    And finish the first draft of this post

commit 57fe041867f4fedcff5b8dc6a739b9b033bc0d49
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Nov 7 19:31:15 2018 +0000

    More of the Aberdulais post and the wide_image plugin

commit fee9592d79a1601832ba77e811d3b966675abdb1
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Nov 7 08:39:13 2018 +0000

    One more paragraph and image, plus script improvements

commit e1223a398ac49d261ad24c981044eea4fc5e6859
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Nov 7 07:47:00 2018 +0000

    Add some more stuff about Aberdulais

commit d063cb6fa23c699058785a20d7af3fe512d2fb95
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Nov 6 22:03:13 2018 +0000

    Ditch the Flickr stuff; the free plan is going away

commit 4b42120b8eeff4d601c771dbf81323d4a9c34682
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Nov 5 08:39:56 2018 +0000

    add some links

commit 5b48e3dcbeb4240e66818703b2d7cc843a524d1c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Oct 28 23:15:59 2018 +0000

    Start writing up the Aberdulais post

commit 73000d7d212356f7f23a0b66eebd41a5ba182d88
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Oct 28 20:28:15 2018 +0000

    Get the first iteration of the Flickr plugin working

commit 316a97e6c85ffe09cde45c17a5460185936247a9
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Nov 6 08:06:32 2018 +0000

    Add infra for the notebook site

commit bbba344101e43e2a1dcc926b0945183bd94c64e5
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Nov 6 08:06:23 2018 +0000

    Ensure the analytics can cope with a flat graph

commit 1b613139085e28aada8450132b7c98dc51a81e78
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Nov 6 07:36:01 2018 +0000

    Remove the nginx/docker-compose config needed to boot [skip ci]

commit d531f43e37bd89b8b81757fb49dd8015f62364bb
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Nov 5 22:00:57 2018 +0000

    Ditch the Elasticsearch/scrapbook containers entirely

commit d86dcdf59b118ac7c82a04ff87194a640a0d3fda
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Nov 5 21:25:08 2018 +0000

    Reduce the size of my Linode

commit 4cdb4aac007cdd135d3a13e0eb26af733f7144a7
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Nov 5 21:06:12 2018 +0000

    Start managing my Linode instance with Terraform

commit c30dcb4f770fe127c910d3916219da7b52d85f18
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Nov 5 07:55:52 2018 +0000

    Start incorporating rejections.toml in the Ruby analytics

    [skip ci]

commit e93829c2bf30f33c2d3586b090a7a139d482bdb9
Merge: 69bfe9cf b14bebc1
Author: mergify[bot] <mergify[bot]@users.noreply.github.com>
Date:   Sun Nov 4 23:39:27 2018 +0000

    Merge pull request #186 from alexwlchan/sitemap

    Add a sitemap + exclude robots from /analytics/

commit b14bebc1757ae9aabd285f34bde9705db590546b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Nov 4 23:34:19 2018 +0000

    Exclude robots from the analytics path

commit c4046be02de148cce0a9feb69b8dfd90f77c1a72
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Nov 4 23:34:04 2018 +0000

    Install a plugin for generating a sitemap

commit 69bfe9cf228c6dedb7e279fe6fca6ef67e167499
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Nov 3 19:30:33 2018 +0000

    Remove the Pinboard container

    [skip ci]

commit fcfffe04f1f70867ce4dadfd128140263685d4f0
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Nov 3 19:19:29 2018 +0000

    Stick in a 302 redirect at /theme/

commit 13df14a049e9ab0c8cebcc0c9c17eb04f46078b9
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Nov 3 16:02:52 2018 +0000

    Include a summary of error pages in analytics [skip ci]

commit 71f93beb56c5f84d05ef39f56803bf6b3434bfa0
Merge: 2dc44211 1b7d63d9
Author: mergify[bot] <mergify[bot]@users.noreply.github.com>
Date:   Sat Nov 3 10:22:05 2018 +0000

    Merge pull request #185 from alexwlchan/ruby-analytics-2

    Rewrite the analytics scripts to use Ruby, present better info and use bar charts

commit 1b7d63d90a879c9d8d420ec4e477bae8f674c17e
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Nov 3 10:17:28 2018 +0000

    Put the README back

commit 5f586a85fc9908082fc4b6c7e03702d58f25a264
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Nov 3 10:17:18 2018 +0000

    Get the runner working again

commit 9b5727c3d1f0c949e8f0fd7c98211728f2646ce2
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Nov 3 10:12:19 2018 +0000

    And now move everything into the analytics directory

commit eab846e325d3ce1b74fca895ce9bbe0069bb5f20
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Nov 3 10:11:46 2018 +0000

    Set up the appropriate Makefile and Dockerfile

commit b0338e517888fc632257508f719adb5c626c89f7
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Nov 3 10:10:45 2018 +0000

    I only care about the top few search results

commit 1e92cad7e58cf78f2fc1ab17f3e8baf0072d03e1
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Nov 3 10:10:36 2018 +0000

    Copy across the existing analytics config

commit 9b82eac88dbf92f0bd5fdf7382847e57a902b6cf
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Nov 3 09:32:52 2018 +0000

    Count unique hosts, total visits, and pages

commit 5cabd04a9a36ef1b09ebc08d7485e9632e4072d8
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Nov 3 01:01:54 2018 +0000

    Tidy up one of the redirects

commit f9802a185abc73803ceffe3089c6781dbae5e88b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Nov 3 01:01:48 2018 +0000

    Roll the headings into the printer function

commit 68dd389c7f72147fa2233c2f52355f5e1ebb561d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Nov 3 01:01:17 2018 +0000

    Draw an ASCII bar chart with the results

commit f792bb65c3636d04d08ac1e520dcead263cc1565
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Nov 3 00:53:30 2018 +0000

    Do enough to tally referrers and search terms

commit 0ec013bff4e6ba51dac618a20123a514a3d9494d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Nov 3 00:03:45 2018 +0000

    Start writing the Ruby analytics engine

commit 2dc44211c3171e2f64109a58be2516645e3e0289
Author: Travis CI User <travis@example.org>
Date:   Fri Nov 2 10:42:05 2018 +0000

    Publish new post finding-unsubscribed-sns-topics.md

commit 767249d2304b46c064992192fae8dc6aa00e3ad1
Merge: 46b06ec7 f0e509cd
Author: mergify[bot] <mergify[bot]@users.noreply.github.com>
Date:   Fri Nov 2 10:37:33 2018 +0000

    Merge pull request #184 from alexwlchan/golang-sns-tracker

    Add a post about finding unsubscribed SNS topics in Go

commit f0e509cd218850829ad0356df28d4d5c35f0f4af
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Fri Nov 2 10:32:57 2018 +0000

    One more go at getting this test right

commit 8da8c7779ec1b31876f77ff17ee3dcc86f00c2b2
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Fri Nov 2 10:19:40 2018 +0000

    Hey, Rouge omits the empty `<span>`. Nice!

commit 2659538785cc830c56effd009dd495e39294f230
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Fri Nov 2 10:04:53 2018 +0000

    That test has changed. Shocking, I know.

commit 7285c21ec8f7cdad9ebd273ffde35fab8ec02eed
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Fri Nov 2 09:57:58 2018 +0000

    Disable selecting the '$' symbol in console blocks

commit 0a7194c3e5e68a73bc0c47cc579855c92773d569
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Fri Nov 2 09:57:48 2018 +0000

    Use rouge for syntax highlighting, not pygments

commit 303368a432f192582378797e798b48b5aae6f8d3
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Fri Nov 2 09:45:50 2018 +0000

    Markups on the Go SNS post

commit 9daeb94b1788e0eb01b78b83c61032c7ea97b338
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Nov 2 08:21:52 2018 +0000

    Finish the first draft of the Go post

commit 49abddeb9dcfb075b58318e262b9cbe799429d35
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Nov 1 23:50:19 2018 +0000

    Start writing about my Go script for finding unsubscribed SNS topics

commit 46b06ec7b64f557768ac5311d63a422439d75de7
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Nov 1 10:04:14 2018 +0000

    Add some more referrer info

commit 47f3c7aab0fac0c58b974accb2ecdcdc09539b97
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Oct 29 20:39:38 2018 +0000

    Ensure the plugin is copied to the right directory

commit 1bec2110946e39e08d618d8073440d96d0c7816d
Merge: 1349790f c68420be
Author: mergify[bot] <mergify[bot]@users.noreply.github.com>
Date:   Mon Oct 29 19:58:38 2018 +0000

    Merge pull request #183 from alexwlchan/jekyll-upgrade

    Upgrade from Jekyll 3.5.2 to 3.8.4

commit c68420be11dbd2077c8d93aebbcbfa210649d561
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Oct 29 19:51:08 2018 +0000

    Okay, so not strict_variables

    Turns out this warns when you check if a variable is defined, and I
    cba to fix all those lookups right now.

commit 1acd5614b41991c507df37405094eb815ee63bed
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Oct 29 19:47:33 2018 +0000

    Add the new Jekyll options for strict Liquid rendering

commit 0aa4b9fa89a63372d6494e9b63095b1a0db76786
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Oct 29 19:47:24 2018 +0000

    Ensure we can actually build the Gemfile.lock

commit b5375ad22fe2ef85f38d371e7820732afdb59c63
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Oct 29 19:47:17 2018 +0000

    Bump the version of Jekyll and everything else

commit 1349790fc93c427babcfa301a9c7e7bcd97e8476
Author: Travis CI User <travis@example.org>
Date:   Mon Oct 29 07:48:12 2018 +0000

    Publish new post unscrupulous-time-travel.md

commit 0baa9b40627983c446dd9aa3f2841e534c553017
Merge: 05a5561f b4158693
Author: mergify[bot] <mergify[bot]@users.noreply.github.com>
Date:   Mon Oct 29 07:43:41 2018 +0000

    Merge pull request #182 from alexwlchan/historical-coins

    Add a post about 400 year old coins

commit b4158693535c7f9a21132095a3f0f912a0ba4bd3
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Oct 29 07:39:04 2018 +0000

    Add the post about 400 year old coins

    And the Flickr plugin now supports displaywidth

commit 8c51d4d31bb56f9e89578f5ce46624973b302467
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Oct 28 23:21:09 2018 +0000

    Support different sizes of image in the Flickr plugin

commit 567799e18f6838dff95391b4a52fca213eb7f466
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Oct 28 20:56:38 2018 +0000

    Add a script for uploading to Flickr

commit 140964b55cfcab7bf3a1ba714004343b574a690d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Oct 28 20:28:15 2018 +0000

    Get the first iteration of the Flickr plugin working

commit 05a5561f21c9bfdb3bb04a44cdcd97a5c5c47190
Author: Travis CI User <travis@example.org>
Date:   Sun Oct 28 14:12:26 2018 +0000

    Publish new post horstmann-electric-7.md

commit eab6c3b65f10247dfd11031a510686f80b58f997
Merge: 57a93741 a0ab276c
Author: mergify[bot] <mergify[bot]@users.noreply.github.com>
Date:   Sun Oct 28 14:08:32 2018 +0000

    Merge pull request #180 from alexwlchan/boiler-instructions

    Add the latest set of boiler instructions

commit a0ab276c2ff4680ba996579f9bf5f2c49e5675fc
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Oct 28 10:58:48 2018 +0000

    Add the latest set of boiler instructions

commit 57a93741d3e3aff00cba25110a6dbcf857108805
Merge: f9d850da 4eeaa621
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Oct 28 14:03:28 2018 +0000

    Merge pull request #181 from alexwlchan/mergify-config-tweak

    Maybe adding the /pr suffix will make the check work?

commit 4eeaa621cef9a54069a2119d02df85b29d279ca0
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Oct 28 14:02:52 2018 +0000

    Maybe adding the /pr suffix will make the check work?

commit f9d850daa1ef7db18c3d781674fe43c3f21e233f
Merge: cdcb810e 4f07e85b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Oct 25 20:46:09 2018 +0100

    Merge pull request #178 from alexwlchan/new-mergify-rules

    Create Mergify config for the V2 engine

commit 4f07e85be953e428621a27be3182af895891ab36
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Oct 25 20:20:58 2018 +0100

    Maybe this is the syntax for deleting a merged branch?

    https://doc.mergify.io/examples.html#deleting-merged-branch

commit cdcb810e06a1a00c133ada931f0d0a4282e52c7b
Merge: d05788c8 d984c25f
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Oct 22 21:06:49 2018 +0100

    Merge pull request #179 from alexwlchan/finatra-404

    Add a post about custom 404 responses in Finatra

commit d984c25f66f929a5f9b040191285f2c61ca2edd7
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Mon Oct 22 21:04:51 2018 +0100

    Publish new post finatra-404.md

commit 242aaa9aa26cef83a2d3c8ec72a435ac868b3800
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Oct 22 20:04:12 2018 +0100

    That should be a dict with three keys, not a list of three dicts

commit c44372927c2cac8c84ea4bd703d570ae9414b9f6
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Oct 22 20:01:15 2018 +0100

    Add a post about custom 404 responses in Finatra

commit 97700b4433bf6f28e656c1f13a18224da34011a9
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Oct 22 20:00:25 2018 +0100

    Tweak the example app to be more friendly

commit 6cffa052fcef94a52d68c13f31c4beff1cfe67b9
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Oct 22 19:10:59 2018 +0100

    Get the rest of the Finatra app checked in

commit 79eafccdcc595007842ff207b99f219b49f73d04
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Oct 22 18:18:46 2018 +0100

    Create the first bit of the Scala app

commit 6935a83cd4d4142d5e039a8cdc73f434d81355de
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Mon Oct 22 13:49:14 2018 +0100

    Create Mergify config for the V2 engine

commit d05788c8cbd7d89cc90a3f7cbc3e0bea02ab1585
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Oct 20 06:14:01 2018 +0000

    Add more analytics config

commit a653c833d093fca5358e31ba8858293b747a5818
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Oct 14 17:28:49 2018 +0000

    Add more analytics config

commit 899de28af72e206945e61edc3713a9f2ceafea4e
Author: Travis CI User <travis@example.org>
Date:   Thu Oct 11 07:32:20 2018 +0000

    Publish new post gender-recognition-act.md

commit c8d09979afdfcd6db848619731d7388482485240
Merge: 3771f3ef 363f24c8
Author: mergify[bot] <mergify[bot]@users.noreply.github.com>
Date:   Thu Oct 11 07:27:41 2018 +0000

    Merge pull request #177 from alexwlchan/gender-recognition-act

    Add a post about the Gender Recognition Act consultation

commit 363f24c8ef4a9a6aba670a4e41b743c7a628ee4f
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Oct 11 08:22:33 2018 +0100

    Add a post about the Gender Recognition Act consultation

commit 3771f3ef65ffeecb5210a6db0d5556b11152af35
Author: Travis CI User <travis@example.org>
Date:   Sun Sep 30 07:12:51 2018 +0000

    Publish new post content-warnings.md

commit 1ad982c72d95fad497bc242bc2501ab41d1f417c
Merge: 94c4a187 4f7c11e2
Author: mergify[bot] <mergify[bot]@users.noreply.github.com>
Date:   Sun Sep 30 07:08:35 2018 +0000

    Merge pull request #176 from alexwlchan/content-warnings

    Add a post about content warnings

commit 4f7c11e23d54701b119ca487f7d8cd1e94585f77
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Sep 30 08:03:41 2018 +0100

    Add a post about content warnings

commit 94c4a187d4a098aa47f69f5672eb6918242e783b
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Mon Sep 24 09:22:34 2018 +0100

    Apparently those hex colours need to be lowercased

commit 1ce4d925925fe2f61bedcfb5c5ef9c400dc513cf
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Mon Sep 24 08:09:35 2018 +0100

    Make the "assume worst intent" slides purple

commit 40cbc6ff511000bfad80c1e31e233a9972b01c44
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Mon Sep 24 08:09:21 2018 +0100

    Add the generated _site directory to .dockerignore

commit 3c1f64c0a28e84a6f21c299224dcb55139db2af9
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Mon Sep 24 08:09:12 2018 +0100

    We need to install setuptools, or we get an ImportError about pkg_resources

commit 0e9f9b9a54ae04e056260fc26b87fe4228923973
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Mon Sep 24 08:03:26 2018 +0100

    Tweak the spacing on that image

commit f6b8aac63514c82538fa915c9fdd105e93a194e7
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Mon Sep 24 07:57:21 2018 +0100

    SCSS files can have uppercase hex chars

commit 849d3ba10fd380e1eb7ed76f69ba26afed0639eb
Author: Travis CI User <travis@example.org>
Date:   Mon Sep 24 06:56:21 2018 +0000

    Publish new post assume-worst-intent.md

commit 93acfec6c402802ab2fb3bbfc9b7cc13e9791071
Merge: dd8069b9 e9a8dab9
Author: mergify[bot] <mergify[bot]@users.noreply.github.com>
Date:   Mon Sep 24 06:52:07 2018 +0000

    Merge pull request #174 from alexwlchan/assume-worst-intent

    Add notes about my online harassment talk

commit e9a8dab97b46bb758a0ec037da6acb7c0825213c
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Mon Sep 24 07:47:35 2018 +0100

    Fix the links to the PDF slides

commit e65bf26eeeac222e852dabb661ace768f577138c
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Sun Sep 23 22:35:09 2018 +0100

    Update the links/notes on my talks page

commit 6f05542dd9354ff0978aea0efcba3c6a29640ca4
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Sun Sep 23 22:24:42 2018 +0100

    And add some header/footer stuff to the post

commit 2d57ad0b20c2e920bd8b0ef4f435bd354bb22baf
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Sun Sep 23 22:10:04 2018 +0100

    Finish editing the transcript

commit 50f7d241f8e695a7757c30d5f667a0a5713a571a
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Sun Sep 23 21:35:44 2018 +0100

    Add lots and lots more transcript stuff

commit ad4acd7cb551cd060524c9227d289ebdedf6d352
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Sun Sep 23 20:54:52 2018 +0100

    Another couple of slides

commit de39960c8c5924b6d694d80484b77c0e97612067
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Sun Sep 23 20:48:07 2018 +0100

    Tidy up some more of the transcript

commit 095e0b206142ca244fc4e7a575abab5b6befdf1c
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Sun Sep 23 20:14:28 2018 +0100

    Start tidying up a bunch of the transcripts

commit 6a26b86792f77298fe4ef9a983069c2e2fe26d34
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Sun Sep 23 18:29:41 2018 +0100

    Integrate the slides with the transcript

commit 8dc2e6c078ff1b568f36aa322657cdb7f6ceedec
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Sun Sep 23 12:33:55 2018 +0100

    Add all the slides I need

commit 827ec9e63431b21c0286f42beab296a41d5730b0
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Sun Sep 23 11:15:39 2018 +0100

    Copy the PDF of the Assume Worst Intent slides

commit c0d7f8e4c6c08512b50258e980bff08a71a2dfbe
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Sun Sep 23 11:15:27 2018 +0100

    Add the original transcript of "assume worst intent"

commit ff884fa165d535a0e7e0784055dfccd6998065b7
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Sun Sep 23 11:08:03 2018 +0100

    Link to Daniele's twitter page

commit dd8069b9d8f7413f088342ece9f87f154692aca5
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Sat Sep 22 21:51:06 2018 +0100

    Python 2 means no FileNotFoundError

commit 7ac060e17c073d1e11c1ea657dd0682617d14c36
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Sat Sep 22 21:41:23 2018 +0100

    Move the description of static_file_generator.rb to the plugin

commit b435eb3c06a155ca3c3970353cb45a18586ba767
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Sep 22 20:05:54 2018 +0000

    New referrers and rejections for analytics [skip ci]

commit 95048d58378717f4f7d5a062244a804dfcd67b94
Author: Travis CI User <travis@example.org>
Date:   Sat Sep 22 17:07:59 2018 +0000

    Publish new post suspicious-minds.md

commit dc2e347e538aacee8013f20a43180ff7813dbd30
Merge: 11c6d313 b321a28b
Author: mergify[bot] <mergify[bot]@users.noreply.github.com>
Date:   Sat Sep 22 17:03:44 2018 +0000

    Merge pull request #171 from alexwlchan/suspicious-minds

    Initial post about suspicious minds

commit b321a28b74d80b3611b71901a828c2e199c72b54
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Sat Sep 22 17:59:09 2018 +0100

    Screw it, I'm deleting this entire test as not-very-useful

commit 1c0175d60fbc6ded5d7da410104efdfd19593324
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Sat Sep 22 17:51:48 2018 +0100

    Make sure we prepend the date to draft posts first

commit 03369bf515d922b0d054124ca709f6522fbec9c9
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Sat Sep 22 17:42:58 2018 +0100

    Apparently the tests still run in Python 2?

commit 4bc83ef286b001f413124e6d393ce871cbfc6a35
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Sat Sep 22 17:39:06 2018 +0100

    Have a go at recognising images on draft posts

commit 360b20e88d874676bd93688077079ab8b7af3949
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Sat Sep 22 17:37:38 2018 +0100

    Fix a typo in the description

commit f69bc12a4c2e1a0990c36a80f58caabe265ddaf8
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Sat Sep 22 09:52:28 2018 +0100

    Try to get a large image summary card

commit 96d8abe15480a46495016261bc690dd25bc21391
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Sat Sep 22 09:48:38 2018 +0100

    Finish the transcript!

commit 569b6025f6ac4fcf4871f7bca5f81de0a69da4b0
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Sat Sep 22 09:43:58 2018 +0100

    Another pair of slides

commit d2abe24db44f82f7d9e6a02a8037fb9dd806cb71
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Sat Sep 22 09:36:24 2018 +0100

    A few more aviation slides

commit f1a1bfcdaa8b71e8e9198189c4fe2cf6055b0a9b
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Sat Sep 22 09:26:46 2018 +0100

    Another slide done

commit 95f6120e4aeeb0cbe3c39a95580cb25ad6a5c18c
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Sat Sep 22 08:29:56 2018 +0100

    Down to 10!

commit 3b5279939e622b754f50f1408b2743a502092bb6
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Sat Sep 22 08:21:15 2018 +0100

    Clean up more of the YouTube transcript (15 to go)

commit 393d9d946b77b6a9de8eaed55d11c3a196c35249
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Sat Sep 22 08:13:31 2018 +0100

    Tidy up even more of the transcript

commit d2d10df8208d02f8e3ccdd7f46261b1c0a4a112f
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Sat Sep 22 07:43:09 2018 +0100

    Be able to pick up new slide files in `make serve-debug`

commit 35744a7591cb38c5c0879de2034b1c3d750bad8e
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Sat Sep 22 07:42:54 2018 +0100

    Transcript is broken up into per-slide chunks

commit 16a2c55dd4bca76d4114c715ceb273eff1c84c42
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Fri Sep 21 22:02:36 2018 +0100

    Halfway mark!

commit faaa97ac4d164865c2bf1ba891a1b1bf3a10c27f
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Fri Sep 21 21:24:35 2018 +0100

    Continuing to crank through the YouTube transcript

commit 02cb40b6371a5f0113a6fc373308eda8b90c3252
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Fri Sep 21 21:18:49 2018 +0100

    A third done from the YouTube transcript

commit d5dcc217a48b45bcd322efe15413c4fcacfe3505
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Fri Sep 21 20:34:42 2018 +0100

    Okay, and now use the YouTube transcript

commit af23cbf009f908f86ffb646f299741e6e64c053c
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Fri Sep 21 20:09:17 2018 +0100

    Share the PNG/JPEG choosing logic between captioned/raw slides

commit 4f04349a88f5a182aa888a2b1a9a6338b09b2fef
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Fri Sep 21 19:41:32 2018 +0100

    A bit more text on reliability

commit 2441cb8cd010f5258fc90bd1edfd8596e0dcc567
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Fri Sep 21 08:56:03 2018 +0100

    Add more slide notes

commit 4d495311e5ce9468f6c087f4c560d6b6af8cda4f
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Thu Sep 20 21:37:58 2018 +0100

    Keynote spits out slides with a ".jpeg" extension, so use that

commit eaedafe1e3586756fa8dc45c93e7ff53357ae284
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Thu Sep 20 21:37:46 2018 +0100

    Get all the "trust in an age of suspicious minds" slides up

commit f90a8c51518af651e9c30c5dd7f5a6f3e589ecb1
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Mon Sep 17 06:34:18 2018 +0100

    Get the first bunch of slides out

commit b1bf53192850b9202b17de97d0428f1c0800258f
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Mon Sep 17 06:17:10 2018 +0100

    Cache the layout of the _slides directory for performance

commit a4feb48293c18075b60981b1820f748ea24127d1
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Sat Sep 15 22:17:18 2018 +0100

    Slide plugin can handle JPEG as well as PNG

commit 65369d1ededd9f7aed35eca3a0f847732a733304
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Sat Sep 15 21:49:52 2018 +0100

    Add a link to the YouTube video

commit ac2d685e23bbd0616c89c4b7d5731fa45973352f
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Sat Sep 15 15:18:02 2018 +0100

    Get the first draft of the suspicious-minds talk up

commit 03499ec6ec41fc0ce315f74d1ab37bc9280b6866
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Sat Sep 15 15:00:27 2018 +0100

    Add my PyCon UK 2018 talks to the /talks/ page

commit 11c6d313471e254d0c90ac0a55fbd26af41a953c
Merge: eed57500 88349040
Author: mergify[bot] <mergify[bot]@users.noreply.github.com>
Date:   Fri Sep 21 08:24:12 2018 +0000

    Merge pull request #173 from alexwlchan/described-slides

    Add a Jekyll plugin that allows for adding captions to slide images

commit 883490409f8acaf4cf9a0aca2f2c15cb7d506def
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Fri Sep 21 09:16:15 2018 +0100

    Expand the usage comment

commit 5ffae378cdedf728260efd82895e244844a9b904
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Fri Sep 21 09:14:20 2018 +0100

    Use the new slide block there as well

commit 4b0f64d4e40cbc06ae62cd75cca5937bb0abdc52
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Fri Sep 21 09:09:00 2018 +0100

    Use the new Liquid block in the privilege/inclusion slides

commit 28aacb4c362bc75f57d3d3b370b88eff38fb9874
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Fri Sep 21 09:06:25 2018 +0100

    Add a Liquid block for writing captioned slides

commit eed57500e5c601ac578a82f79279e58eb5da39c7
Author: Travis CI User <travis@example.org>
Date:   Mon Sep 17 17:21:17 2018 +0000

    Publish new post lessons-in-signage.md

commit 7b509ff2b06f441e8ce6171a10b6e53007715e07
Merge: 94197f5f bdf01f94
Author: mergify[bot] <mergify[bot]@users.noreply.github.com>
Date:   Mon Sep 17 17:16:39 2018 +0000

    Merge pull request #172 from alexwlchan/sign-of-the-times

    Add a post about signage at PyCon UK

commit bdf01f942cec3932af895bef64b3b30dd131e24e
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Mon Sep 17 18:10:04 2018 +0100

    Trim quotes around the tweet URL in {% tweet %} tags

commit f58ed09d2240eafe6af41384013ea46a2ba28cc1
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Mon Sep 17 18:09:52 2018 +0100

    Add a post about signage at PyCon UK

commit 94197f5fe7f91cea2a6679120af0170bf2fef988
Author: Travis CI User <travis@example.org>
Date:   Thu Sep 13 16:53:55 2018 +0000

    Publish new post pyconuk-2018.md

commit df0f055291d8e5197f7f4c890cf1d5aa8604428b
Merge: 66ef916f 777bc0ec
Author: mergify[bot] <mergify[bot]@users.noreply.github.com>
Date:   Thu Sep 13 16:48:44 2018 +0000

    Merge pull request #170 from alexwlchan/pyconuk-2018

    Add a quick blog post about PyCon UK

commit 777bc0ec6dbe2a1eeb91dcebdc37886f3c2d8bac
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Sep 13 17:42:00 2018 +0100

    Add a quick blog post about PyCon UK

commit 66ef916fc2bc1b9291557ac029a9daafb0144343
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Thu Sep 6 16:18:03 2018 +0100

    Fix a mistake in the SQS queues post

commit b679efe8e75ea6ff621b68671c19603a20b907f2
Author: Travis CI User <travis@example.org>
Date:   Wed Sep 5 20:11:59 2018 +0000

    Publish new post error-logging-in-lambdas.md

commit 9d10606f74d84ab9c194ee70704b917d55c6401d
Merge: ef644c28 28b53312
Author: mergify[bot] <mergify[bot]@users.noreply.github.com>
Date:   Wed Sep 5 20:07:42 2018 +0000

    Merge pull request #169 from alexwlchan/lambda-log-on-error

    Add a post about error logging in Lambdas

commit 28b5331235f6a71619caa2d803688867a2a8ffb3
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Sep 5 21:03:11 2018 +0100

    Add a post about error logging in Lambdas

commit ef644c2895b766fbbd305b2ba9e3f66bd2257c62
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Sep 1 07:36:35 2018 +0000

    Redirect the about page to /

commit a1a22d0b64856f3de645b6719702404e0119297d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Sep 1 07:34:38 2018 +0000

    Add a few more paths to my referrer ignore list

commit 6582d0128dc2fd326c920b2143c5d6d2f8cb4bd2
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Sep 1 07:32:30 2018 +0000

    Don't rebuild the Docker image just for script changes

commit 7ce0387d399c231f7ec544bd64b7bc8c59fab3fd
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Sep 1 07:30:24 2018 +0000

    Print a more granular bar chart in the analytics

commit 5c06875493ce4aee370915510f83c616beaf27b6
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Sep 1 07:30:12 2018 +0000

    Add another twitter referrer

commit 8674c57cd5c59e31dd4319a90308cd0d4d933360
Merge: 3dbcab91 81b45231
Author: mergify[bot] <mergify[bot]@users.noreply.github.com>
Date:   Mon Aug 27 08:30:57 2018 +0000

    Merge pull request #168 from alexwlchan/preserve-paths

    Mount at the same path inside/outside the container to preserve paths

commit 81b452315354947b9aa3db4634b73a6204c4d55c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Aug 27 09:26:29 2018 +0100

    Install Git inside the Dockerfile

commit 5d0e50776272724e1e994133e678b90eb2548d34
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Aug 27 09:20:13 2018 +0100

    We don't need to set that env var

commit 38df119f15402a423eb28efba99191cb853f3d59
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Aug 27 09:19:51 2018 +0100

    Fix the path to the repo root

commit 59f58ecfac23d1155ac01fb90d758e024ec055df
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Aug 27 09:12:01 2018 +0100

    Mount at the same path inside/outside the container to preserve paths

commit 3dbcab91a6f1f63baa256dca407a878ace3154d6
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Aug 26 08:15:31 2018 +0100

    Use the summary for the page description tag

commit 7b9930fbdcc5b860c021929f707f527894ec7510
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Aug 26 08:14:22 2018 +0100

    Correct the image link for that Twitter card

commit 1f7440e7940f0e35f827a810e63cf7f184d505a3
Author: Travis CI User <travis@example.org>
Date:   Sun Aug 26 07:10:28 2018 +0000

    Publish new post maps-for-pyconuk.md

commit 7f9aade445248168f551d5b212c626fbaf3697bb
Merge: 888ce218 76fb11f8
Author: mergify[bot] <mergify[bot]@users.noreply.github.com>
Date:   Sun Aug 26 07:06:43 2018 +0000

    Merge pull request #167 from alexwlchan/pyconuk-maps

    Add a post about maps for PyCon UK

commit 76fb11f88d989f1d7c5cce3893ed6ff7473a1c95
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Aug 26 07:58:10 2018 +0100

    Make the venue map the summary image

commit 3e55e7e8e04cdf4526c76d6095f68c463dbf8505
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Aug 26 07:56:55 2018 +0100

    A few markups/review suggestions

commit 6c4d16cbd7bf1cf453c1f1893152753747319ee3
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Aug 26 07:54:15 2018 +0100

    Add the first draft of a post about venue maps for PyCon UK

commit 888ce218e566fe51386889c99e3d075184caa18f
Author: Travis CI User <travis@example.org>
Date:   Sat Aug 25 08:20:24 2018 +0000

    Publish new post parallel-scan-scanamo.md

commit 95d03c8d8124518f8a45b4703932182a10bfc6da
Merge: 398817e2 f3c50bf5
Author: mergify[bot] <mergify[bot]@users.noreply.github.com>
Date:   Sat Aug 25 08:15:25 2018 +0000

    Merge pull request #166 from alexwlchan/sbt-parallel-scan

    Add a post about doing parallel scan in DynamoDB

commit f3c50bf59d22523599b43f2f311a341f1d1b03b3
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Aug 25 09:09:29 2018 +0100

    A few review markups

commit 7374b413f717436fe6e9d87cef44cefc77525366
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Aug 25 08:58:59 2018 +0100

    First draft of DynamoDB parallel scan post

commit 398817e2b70de196f966229f1a2202dc1ad49f85
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Aug 21 21:32:23 2018 +0100

    Rearrange some of the scripts in the repo

commit 97300fb57f498db1f5b6bc29c4337892812a725a
Merge: f635a7ec 210588a5
Author: mergify[bot] <mergify[bot]@users.noreply.github.com>
Date:   Tue Aug 21 16:32:36 2018 +0000

    Merge pull request #165 from alexwlchan/test-in-plugins

    Run the front matter checks as a Jekyll plugin, not a standalone test

commit 210588a57bffb1811bb846f48ff8aa97dae67b8a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Aug 21 17:27:28 2018 +0100

    Add another text filter

commit b0d363d6b9833c01b5493f90c720942e8acf34c0
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Aug 21 17:24:31 2018 +0100

    Remove a couple of unneeded Python packages

commit 0006da2e25d8b0e60ccbd793d0f27280c1ba588d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Aug 21 17:21:38 2018 +0100

    Add another three months of summary checking

commit db76304133117e857eb151e4593dbfad361a001e
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Aug 21 17:18:14 2018 +0100

    Missing newline

commit 42402c13117006739061c8ca8ff3e112f10794ee
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Aug 21 17:18:04 2018 +0100

    Move the last front matter check into a Jekyll plugin

commit dc77847a08b6f160fd749c35c2708fd9008879e4
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Aug 21 15:03:31 2018 +0100

    Move tests for slashes in tags into Jekyll

commit 9d64381fc3664edd56077551a53ee5b4a8cfb078
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Aug 21 15:01:23 2018 +0100

    Move the test that tags don't have trailing commas into Jekyll

commit 1fdaf921fe053897877a711320ddd43740b6e542
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Aug 21 14:52:40 2018 +0100

    Check the summary length in a Jekyll plugin

commit 33aaec62613f06dadda80df4b672db66416a525f
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Aug 21 10:09:09 2018 +0100

    Move the check for a "layout" key to a Jekyll plugin

commit f635a7ec3a433763aa0a0fbeb78923489197e190
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Aug 21 07:45:33 2018 +0100

    More strings pushed inside TOML

commit 68c5bda3c39d443426222786fee6a198828219a6
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Aug 21 07:39:30 2018 +0100

    Push referrer config into TOML

    [skip ci]

commit 5abd88116139943cebfd957ffec522b0f36199e9
Merge: 665d7ed2 6ef92376
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Aug 20 08:26:25 2018 +0100

    Merge pull request #164 from alexwlchan/toml-analytics

    Start using TOML for analytics config

commit 6ef9237681d87e78af76128303c22b248b978138
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Aug 20 08:23:44 2018 +0100

    Collapse into a single Python file

commit bacf46ce5b7f31962aa319b83dbebe61bec5cb48
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Aug 20 08:22:53 2018 +0100

    I never save log files in the current setup

commit a928982e094647122effc249e9f25e1e4656df24
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Aug 20 08:22:09 2018 +0100

    I never actually run these tests

commit 57d9a8d60007cbfc263bbca3dc099f112b017292
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Aug 20 08:21:58 2018 +0100

    Another two bad path suffixes

commit 6462a40b04790df7a412123d5e58d3713c0fa3fd
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Aug 20 07:20:03 2018 +0000

    Add a few more referrer aliases

commit ac8100ea1354129cbd8257846a11b915b44f36ab
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Aug 20 07:19:49 2018 +0000

    Make sure we can find the TOML file in the container

commit 1c881ec2881ff1bfdae3f83c99e11873f86bf3ae
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Aug 20 08:18:16 2018 +0100

    Move more analytics config to TOML

commit 665d7ed25bcb1c14d5d45c79862e74d41d0a24b9
Author: Travis CI User <travis@example.org>
Date:   Mon Aug 20 07:17:19 2018 +0000

    Publish new post no-more-tumblr-redirects.md

commit 17369015060e3db924859960d4f1a539e7e9c1bd
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Aug 20 08:16:35 2018 +0100

    Move some of the analytics config into a TOML file

commit 3764e4daaa7cfcc48a365c438dea56aff1658321
Merge: 7563b868 3829b4bf
Author: mergify[bot] <mergify[bot]@users.noreply.github.com>
Date:   Mon Aug 20 07:13:22 2018 +0000

    Merge pull request #163 from alexwlchan/tumblr-redirect

    Add a post about fixing Tumblr 303 redirects

commit ecba67f7d2e84482d20cf07f1c8950d2be1556b3
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Aug 20 08:12:21 2018 +0100

    Add toml to the list of dependencies

commit 3829b4bf2f19e6df8061283734bffb0823c98abc
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Aug 20 08:08:57 2018 +0100

    Do some filtering on homepage posts so miniposts don't appear

commit 40992478bbe4991158b1c96a95de46dfdbf05a8a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Aug 20 07:55:55 2018 +0100

    Add a post about Tumblr redirects

commit 7563b868b92921bbe318dc522accba84f10d48c6
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Mon Aug 13 11:33:04 2018 +0100

    Also remove the 'aria-hidden' attribute from feeds

commit 5b9d47707401a44daf25ee3e1009a6717b40baab
Author: Travis CI User <travis@example.org>
Date:   Mon Aug 13 08:16:20 2018 +0000

    Publish new post inclusive-conferences.md

commit c4dfb2568fd624985ef5742ced99d9863d518d79
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Mon Aug 13 09:12:49 2018 +0100

    Always get emails for build notifications

commit 23858c81ca053e60648b8290a159589124bb84d0
Merge: c1f0e5e0 ea5c8d95
Author: mergify[bot] <mergify[bot]@users.noreply.github.com>
Date:   Mon Aug 13 07:24:49 2018 +0000

    Merge pull request #162 from alexwlchan/inclusive-conferences

    Add a post about creating inclusive conferences and events

commit ea5c8d956325ce8e2f1050ebe7beef04278381fd
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Aug 13 07:34:34 2018 +0100

    Add a summary line

commit 3c9682972e6b5fdc8ccfad8746a07ce5cb83b191
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Aug 13 07:31:49 2018 +0100

    Fix anchor links in the toc

commit dcc17945813dd782024ccab21afaa6540b83f6bc
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Aug 13 07:30:02 2018 +0100

    Add styles for anchor links

commit 62335d2187d272ee32a8460e645be2d55d78b841
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Aug 13 07:21:35 2018 +0100

    Add a table of contents to the post

commit 5bb9e7b012c719bb6d43b656b38334c372ed5240
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Aug 13 07:20:04 2018 +0100

    Add IDs to headings in the post

commit d0777a61eb8b1e1383c5ac35754c8b4199cffdef
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Aug 13 07:12:08 2018 +0100

    Tiny tweak

commit 010836c63b43e4dd72d526e55a007b4dd2abf2db
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Aug 13 07:09:36 2018 +0100

    Tidy up the formatting

commit 167e837cd32d74948966e7a8b9f37a026c6415ac
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Aug 13 07:06:27 2018 +0100

    Finish the final draft

commit 85cb114b57d0d21a7963f593b78faf2ece3d00f9
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Aug 12 19:29:21 2018 +0100

    More markups for the second draft

commit 8bcfce219e755a2aa4d6db543eb96bbd8d64d6ae
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Aug 12 19:05:06 2018 +0100

    stenographers as well

commit 3d923aa952c8676a9d721bd8b3c1ad6fb813bb4c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Aug 12 19:00:33 2018 +0100

    Don't forget the images!

commit 97ff340693beacd7d927d32134134be12e5b2c4d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Aug 12 18:59:45 2018 +0100

    Thrash out the second draft

commit a7fc54c1e45fc65a38889ba16d1d92ec0b4b01e5
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Aug 12 15:36:15 2018 +0100

    First substantial draft of the post

commit cd805a702367415f28db922fed7904a708d505e1
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Aug 12 10:28:17 2018 +0100

    badge policies

commit 1079adac5b1f30b60df537f167f71fb3e39642ea
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Aug 12 09:15:53 2018 +0100

    tickets + finaid

commit 65691704f0db726b988e81b93fd1a82d42545ddb
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Aug 12 08:28:39 2018 +0100

    It's a bit weak, but there's the first disability section

commit e3f70bc9caaf50a01d31417b9ed3b852d498e371
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Aug 12 07:59:37 2018 +0100

    there goes food and drink

commit ccb4b9977f6024a8ff2f294f46876cf75bf6fcef
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Aug 11 21:49:06 2018 +0100

    all the stuff on looking after speakers

commit 2a69502240a83c6a44ef9c33e22f5ebd0074d947
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Aug 11 21:05:48 2018 +0100

    Finish 'inside the venue'

commit d2b41b145c336b20b529441514cab29a17e208c6
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Aug 11 20:57:34 2018 +0100

    Start fleshing out 'venue spaces'

commit 9ef750922396b379d7e4345d680dab19b3e8c1fd
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Aug 11 20:38:52 2018 +0100

    Write the intro and CoC piece

commit 781d691483bf53f5eafbdbb9c792d7fcc8c9e5f4
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Aug 11 20:06:04 2018 +0100

    first draft of the inclusive conferences notes

commit c1f0e5e0fd3159b4b44f5c83ea9c64bb9f6c9350
Author: Travis CI User <travis@example.org>
Date:   Tue Aug 7 15:48:53 2018 +0000

    Publish new post finding-slow-builds-in-travis.md

commit 0ee439aa714ad42f7a9422ebdbdae832cbe0fb1a
Merge: 70c4e73a 6ae07548
Author: mergify[bot] <mergify[bot]@users.noreply.github.com>
Date:   Tue Aug 7 15:45:11 2018 +0000

    Merge pull request #161 from alexwlchan/travis-build-times

     Add a post about finding slow builds in Travis

commit 6ae0754880caad0d3e5e7815c2b2d2c1337bd0ba
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Tue Aug 7 16:41:01 2018 +0100

    Add a post about finding slow builds in Travis

commit 87a25fbfe2b7db24ee25b1ce4966456c2c1c1256
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Tue Aug 7 14:09:53 2018 +0100

    Disable hanging punctuation in code blocks

commit 70c4e73ab17735d2889813ac55e3211b3132ab68
Author: Travis CI User <travis@example.org>
Date:   Sun Aug 5 22:15:55 2018 +0000

    Publish new post do-not-distract-while-driving.md

commit e834b334938eb774ad9d05ed6912ba6468dccab5
Merge: 384c9c73 78413e8e
Author: mergify[bot] <mergify[bot]@users.noreply.github.com>
Date:   Sun Aug 5 22:11:29 2018 +0000

    Merge pull request #160 from alexwlchan/do-not-distract

    Add a post on distracting driving UIs

commit 78413e8ed7fd6bb528cf4688dbef6a7a3be0389b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Aug 5 23:06:12 2018 +0100

    Add a post on distracting driving UIs

commit 384c9c73de4668f21689e1ee3ac60bf19517ce43
Author: Travis CI User <travis@example.org>
Date:   Thu Aug 2 07:31:35 2018 +0000

    Publish new post selective-sudo-on-travis.md

commit b02086fc205491180dd1aaeef4c226037fd9d2be
Merge: 2de8b262 fdedadb9
Author: mergify[bot] <mergify[bot]@users.noreply.github.com>
Date:   Thu Aug 2 07:27:31 2018 +0000

    Merge pull request #159 from alexwlchan/selective-sudo-on-travis

    Add a post about selective sudo on Travis

commit fdedadb913506ab8926e990cd54b668ddc78803e
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Aug 2 08:22:42 2018 +0100

    Add a post about selective sudo on Travis

commit 2de8b262c9603571ae5d91766d17b8aff4277ff6
Author: Travis CI User <travis@example.org>
Date:   Sat Jul 28 10:04:42 2018 +0000

    Publish new post icloud-calendars.md

commit 921572cf84f56e8d2bdba334f9e98445a8f0ae8d
Merge: 41b58e36 f601c0c2
Author: mergify[bot] <mergify[bot]@users.noreply.github.com>
Date:   Sat Jul 28 10:00:59 2018 +0000

    Merge pull request #158 from alexwlchan/calendars

    Add post about iCloud Calendars

commit f601c0c26df711f189cd1cd9fd3b1f343e45e3d8
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Jul 28 10:56:47 2018 +0100

    Add a post about iCloud/FastMail calendars

commit cb9d1444d8d02f1a110c05bdaeb95601119449db
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Jul 28 10:13:38 2018 +0100

    Add some recent posts to the front page

commit 41b58e36d8646b07713f3eb12dafe8c2407daffd
Merge: d0ce57c9 4e34693f
Author: mergify[bot] <mergify[bot]@users.noreply.github.com>
Date:   Sun Jul 22 08:17:32 2018 +0000

    Merge pull request #157 from alexwlchan/better-front-page

    Better front page

commit 4e34693f2c62a6c2fcf49ea1b0b5d94721d73c96
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jul 22 09:12:19 2018 +0100

    Fix page content tests for new pagination

commit 6ec2a073857c562d50e04078394ac74f72d9d17f
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jul 22 09:11:38 2018 +0100

    Fix one more contact/about link

commit 6c2dd6f18b73a3aeb4fd8fd79a6e22bd4a3886fd
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jul 22 08:33:30 2018 +0100

    Fix a few links to the contact page

commit 939096f9456122846db3046e7ebd9605002f4f86
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jul 22 08:32:41 2018 +0100

    Tell the tests about the blog layout

commit d0ce57c9e5d66f9a79632957f9bf8b5619323225
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Jul 21 20:34:36 2018 +0000

    analytics fixes

commit 4975bd874f065b869d5bf0de248344e2086c100b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Jun 16 08:47:09 2018 +0000

    Analytics fixes

commit e1a4cf7ab77a24f4d2c250d66807610102b9a363
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Jul 21 21:24:05 2018 +0100

    Write a better front page

commit 5688ce25839ed1ee9e218d500aa6c22fe6f9142b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Jul 21 21:12:59 2018 +0100

    Add some nginx config to redirect pages

commit 08a2cbaef037ee5fdc2b679b4bdf0732a38d48fc
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Jul 21 21:08:20 2018 +0100

    Move the blog posts to /blog

commit 403af68f7eff283cd67233da4cdc3275ccb9077d
Author: Travis CI User <travis@example.org>
Date:   Thu Jul 19 07:38:10 2018 +0000

    Publish new post leaking-my-ssh-keys.md

commit b4916998573977b0315cebdf6332a2ddb10cc505
Merge: 1e82f2da 4aacdbb1
Author: mergify[bot] <mergify[bot]@users.noreply.github.com>
Date:   Thu Jul 19 07:26:58 2018 +0000

    Merge pull request #156 from alexwlchan/i-did-a-daft-thing

    Add a post about leaking my SSH keys

commit 4aacdbb1187941647a03c410039e46be4e252eb7
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Jul 19 08:20:25 2018 +0100

    Add a post about leaking my SSH keys

commit 1e82f2da2587289b727a93956fb5b78b74cca838
Merge: 6cf8a0bb e7d86305
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jul 15 15:11:16 2018 +0100

    Merge pull request #155 from alexwlchan/add-mergify-config

    Add some Mergify config

commit e7d86305a070b40b3f59e3f89f50dc3a2d65f404
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jul 15 09:57:44 2018 +0100

    I don't care about reviews

commit 6cf8a0bbc4965083207e829ca05b5c1e2988dac6
Author: Travis CI User <travis@example.org>
Date:   Sun Jul 15 08:48:25 2018 +0000

    Publish new post travel-instructions.md

commit f7053658407f272ce00e63b45a29166cca82dac3
Merge: dba61dfb aa548e01
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jul 15 09:44:38 2018 +0100

    Merge pull request #153 from alexwlchan/travel-instructions

    Add a quick post on travel instructions

commit ff9fdff0b46e4f96d6ebec9e6dbf64751f9e6fa8
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jul 15 09:39:14 2018 +0100

    Add some Mergify config

commit aa548e011550b7353ee9dbaae2542d3b0a224c86
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jul 15 09:31:21 2018 +0100

    Add a quick post on travel instructions

commit dba61dfb49c983cb5d32ae44ded4b52d2d02d80a
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Mon Jul 9 11:47:06 2018 +0100

    Update the lxml pin

commit 95f64654f0d706a5660e5f8340392e2f50cd859d
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Sun Jul 8 18:12:54 2018 +0100

    Fix a broken internal link

commit d9c1e8144e4b7cf35082308733ff76369de19e64
Author: Travis CI User <travis@example.org>
Date:   Sun Jul 1 20:12:48 2018 +0000

    Publish new post imac-accessory.md

commit 97a70cbae6be58755ac07bc5a8840d785a5a4365
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jul 1 21:08:24 2018 +0100

    Add a post summary

commit 5846826a32dce5e4d09f460a70a51eecbf98bfd7
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jul 1 21:03:28 2018 +0100

    Add a quick post about my favourite iMac accessory

commit 88890115da6997cf5c505b07bda6609546c171e8
Merge: 448045a7 045368c4
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Jun 26 12:48:09 2018 +0100

    Merge pull request #152 from alexwlchan/fix-cert-issues

    Have another attempt at cert renewal

commit 045368c4869793e87700a1de6917f1a326300033
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Tue Jun 26 12:45:20 2018 +0100

    Then we don't need to share the certbot directory

commit ade6dde5d73e082f646cb9d13fc16d765c5e2e7b
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Tue Jun 26 12:44:55 2018 +0100

    Exclusively use certs from /etc/letsencrypt dir

commit 6e5ba15a682942369c96b633de3220482e79bc66
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Jun 26 11:43:40 2018 +0000

    Add bijouopera.co.uk and finduntaggedtumblrposts.com to cert rotation

commit d54a68741a4fb18d05e04c606132120f69574939
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Jun 25 14:50:57 2018 +0000

    Fix all the cert issues

commit 63437aeda06e678ec99504798fa9deff26ac7224
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Mon Jun 25 14:08:00 2018 +0100

    Fix the top-level Makefile

commit 27d3853dab307ca2c896256b95b61e5c7888d181
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Mon Jun 25 14:07:29 2018 +0100

    Add the script for renewing credentials

commit 443225cc7a21034c35a3470fa0f5c32ab2eba08c
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Mon Jun 25 13:54:22 2018 +0100

    Build a Docker image for Certbot

commit cd03f88bc53a44bccc2254a32c756459ac6712df
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Mon Jun 25 13:49:55 2018 +0100

    Okay, requirements.txt has to be created manually

commit 48fedd9c3b81f6e2f920d26e7eca34ce5397ff9f
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Mon Jun 25 13:42:52 2018 +0100

    Add a basic requirements.in for a certbot container

commit 448045a7a11726ff79516ac8638ae096a3a42915
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Jun 6 07:39:45 2018 +0100

    Add my Oxford Python slide to my talks page

commit a950c13f31a5eedd8e54af1c7feeac1706a283fd
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Jun 6 07:09:53 2018 +0100

    Fix the style of <update> blocks

commit ab3bcccd9204ecd3a49b606ad49e2d729bc46e74
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jun 3 17:07:23 2018 +0000

    Add nginx/docker config for pinboard

commit 24a5c0635139033640e51a1810bc4d4a11b992a8
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jun 3 15:36:18 2018 +0100

    Add a mention of Let's Encrypt on the about page

commit 37605ae8bcd42dbc25d9d239366f39471f155f75
Merge: 563e7e5b f044aada
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jun 3 15:34:42 2018 +0100

    Merge pull request #151 from alexwlchan/better-certbot

    Improve the process of renewing SSL certificates

commit f044aada5ae835c4dc04a7de7f257f8f0cd4e0a4
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jun 3 14:33:05 2018 +0000

    Add a Make target for renewing my SSL certs

commit 189b8eeec48a42045f342f1ca8da054fcb3c68e5
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jun 3 14:27:47 2018 +0000

    Don't include the Certbot Makefile

commit 2cbd26865cea57eed3faf19065896658a4598073
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jun 3 14:27:23 2018 +0000

    Correct the Bijou Opera SSL cert path

commit 7e94de1ccbd33f22f89cdae905cbf06e8ae58ca8
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Jun 3 14:26:23 2018 +0000

    Remove the old Certbot script

commit 563e7e5b517be7635ba5ca59294cf68220dc6b58
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Jun 2 13:08:11 2018 +0100

    Add last updated metadata to posts

commit 5430e3b54cc2c3e5fd1635bfd65632cbcbfc4947
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Jun 1 09:14:18 2018 +0100

    Swap the image; fix the max-width issue in the barcharts post

commit 345d482063738461b71f4ab486357d1ef18c2691
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Jun 2 07:25:02 2018 +0000

    New analytics data

commit 6d68ca50eca20e6d48dba17ec42d67e58106de8e
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun May 27 19:20:00 2018 +0000

    More updates for analytics changes

commit 0fea01dd0fe99266002f3ccbc6aeebefef4d9140
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat May 26 20:00:08 2018 +0100

    Don't display the whole ASCII bar charts post on the homepage

commit 8b315156dc68ecf4c7d977e93901be59daee574a
Author: Travis CI User <travis@example.org>
Date:   Sat May 26 18:57:07 2018 +0000

    Publish new post ascii-bar-charts.md

commit 77ba54ddba1950281f766e9f004f5350d94eea1f
Merge: 3f88b8e7 a761c272
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat May 26 19:53:18 2018 +0100

    Merge pull request #150 from alexwlchan/ascii-bar-charts

    Add a post about drawing ASCII bar charts

commit a761c272dd2ded8503cf747c6de8f570b7546bb8
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat May 26 19:47:13 2018 +0100

    Add a post about drawing ASCII bar charts

commit 3f88b8e72ca94aa5c4447a2c26063353a7f32f14
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue May 15 08:20:06 2018 +0100

    Reduce the size of meta text

commit 42fca7dd9ebd5d9e7a502cffbf1d8e2432f79bbb
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon May 14 23:34:57 2018 +0100

    Crawl the style sample for tests

commit 7722dfbd7756e01d304d6f89215d9f4b68b74922
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon May 14 23:28:21 2018 +0100

    Roll back to an older twitter gem that gets full text tweets

commit 5b072cd00398b80abf761469e144e6d238f97058
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon May 14 23:14:06 2018 +0100

    Don't make tweets appear grey/italic

commit 2565c67b92724aa87356eee749f3a53fe6fc269b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon May 14 23:13:56 2018 +0100

    Add a couple of tweet examples to the style sample

commit 7e7e22f30a932b7e7d1546a9882b478737f82c82
Author: Travis CI User <travis@example.org>
Date:   Mon May 14 06:15:08 2018 +0000

    Publish new post google-duplex.md

commit 1b93d0546f4951a322f596da9d933148a495325c
Merge: 9befabbb 80e372fb
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon May 14 07:10:42 2018 +0100

    Merge pull request #149 from alexwlchan/duplex

    Add a post about Google Duplex

commit 80e372fb1056f2e66ab507c0b183989e1ddd0c45
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun May 13 23:27:14 2018 +0100

    Add a post about Google Duplex

commit 9befabbbf76f5e0ab762dd4cc499fc0135d27a09
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun May 13 10:16:20 2018 +0100

    Add a hash to post tags

commit 8128ce769191be411d62c27f47e1fdac40a3b5d7
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun May 13 10:14:34 2018 +0100

    Tweak blockquote and pre elements to have a flush left edge on wide screens

commit 1cac96ff145e36915ac95e9fc5500576787c1ff6
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun May 13 10:14:17 2018 +0100

    Start writing a style sample for the site

commit f6be84b5d6727653febbcb82d0c294861fb2c17e
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri May 11 23:28:46 2018 +0100

    Add a Read More to the logged errors post

commit 946cdfabbb6b276af70cf244a81ddb477ba5132e
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue May 8 18:08:55 2018 +0100

    Update my talks page with new links

commit f41d95860e0e945c745176ab7df5ae2beb0fd73a
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Fri May 4 13:38:11 2018 +0100

    Dial down the font size slightly

commit df020e9b8cb87f1859450a3eb3c3569592922352
Author: Travis CI User <travis@example.org>
Date:   Fri May 4 08:28:01 2018 +0000

    Publish new post beware-logged-errors.md

commit 76a11ab4d8a2e664f39dc6df4fe754a029862ac6
Merge: bd768e6b ecdec9d3
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri May 4 09:23:36 2018 +0100

    Merge pull request #148 from alexwlchan/keeping-credentials-secure

    Add a post "beware logged errors"

commit ecdec9d3015df5e8793ff6a0a39b53223bab33f5
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri May 4 09:17:38 2018 +0100

    Add a post "beware logged errors"

commit bd768e6bf6e5794b06c3e4bfc31b0859b239d994
Merge: 69c0500b b6b9760b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Apr 28 08:23:39 2018 +0100

    Merge pull request #147 from alexwlchan/refactor-analytics

    Make the analytics easier to extend

commit b6b9760b73ae6f5d4819b0ae8033ae630c674746
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Apr 28 07:21:20 2018 +0000

    Record a couple more pages as 410'ing

commit cff71a0ad94b3b06e0aa9163e389bb1bd267c6f1
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Apr 28 07:20:35 2018 +0000

    Tidy up a bit of the analytics logic

commit 0c5efa4cff6e3fb21a7d8ed0260a749df8b9d528
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Apr 28 07:20:11 2018 +0000

    Add some more rejection logic, including referrers

commit 7d30dc7ad7b38f1b87bfd8eb505666265e657b30
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Apr 28 07:04:40 2018 +0000

    Move more PHP-related nonsense into rejections.py:w

commit 87911459deb8ac680765b491f87da137355e761c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Apr 28 06:55:58 2018 +0000

    Move file format checking into rejections.py

commit afef78c619cc8068d9e265e0dc122b66a5059fe5
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Apr 28 06:52:09 2018 +0000

    Add more to the list of bad paths

commit 368dc82d9b662ddbc57743ead3a91b498a32003c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Apr 28 06:49:46 2018 +0000

    Start moving the rejections logic into a separate file

commit 69c0500b9f8ad9ca1c475bbbc1ef823feea502e5
Author: Travis CI User <travis@example.org>
Date:   Fri Apr 27 06:43:26 2018 +0000

    Publish new post s3-shortcuts.md

commit d019b6b4e180daf40828a05fa07e6390d70204c5
Merge: 1505e3a2 5f40a32f
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Apr 27 07:38:11 2018 +0100

    Merge pull request #146 from alexwlchan/s3-shortcuts

    Add a blog post about my S3 shortcuts

commit 5f40a32f3b61257bd2efad27ce87ed230d593edc
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Apr 27 07:34:00 2018 +0100

    Add the layout metadata to s3-shortcuts.md

commit 91a0566e07b0a4fbe64429702dbe71c3aa210124
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Apr 27 07:32:49 2018 +0100

    Add a note about treating S3 objects like local files

commit b1a63c29a8f97dd956202e7af0af75b16c887f56
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Apr 27 07:23:08 2018 +0100

    Add a blog post about my S3 shortcuts

commit 1505e3a233408427be103a44b868a207537c06d3
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Apr 20 18:56:06 2018 +0000

    Fix more analytics stuff

commit 2068d7741635d8eff853f008114588a079721680
Author: Travis CI User <travis@example.org>
Date:   Wed Apr 18 12:00:33 2018 +0000

    Publish new post anti-social-media.md

commit 6a185017265ff257c60c803ef64fe60eafc76372
Merge: 9949dba5 0745665d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Apr 18 12:56:16 2018 +0100

    Merge pull request #145 from alexwlchan/antisocial-media

    Add the antisocial media post

commit 0745665d9797710184f00cbb239cc47b16a9e828
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Apr 18 11:07:14 2018 +0100

    Fix the link to the privilege/inclusion post

commit f0dade7d59706fdd2da41b9ccc687a26dd0b4f9f
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Apr 18 10:57:08 2018 +0100

    Add a summary to make Travis happy

commit be1ac0f6975adca479fc6f0292a95efd483e2339
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Apr 18 10:56:37 2018 +0100

    Add a small caveat

commit a15c361e3ca40b517b78cbae34746b4af5680090
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Apr 18 10:54:55 2018 +0100

    Add a copy of the PDF slides

commit 684de544dd2c1561ad6adfe78ae05498e7e7339d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Apr 17 21:28:55 2018 +0100

    a few more slides

commit be8c8d267cdfd1c393e05b911eabfefc9028102a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Apr 17 21:18:51 2018 +0100

    even more words

commit aabe782dcf5eaabcfa7097e4b9f8c4d9b90d5c3a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Apr 17 17:56:38 2018 +0100

    Even more words

commit 9949dba552557de7aedf5a4954cbcdc9fcfe0c98
Author: Travis CI User <travis@example.org>
Date:   Tue Apr 17 16:32:42 2018 +0000

    Publish new post 24-hours.md

commit 5907be219c692cee213481d8afcdebfdecdf3c2c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Apr 17 16:28:40 2018 +0000

    Try to fix the publish-drafts plugin

commit ab529050cc2af4cea50cfb501ad503a904dfd133
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Tue Apr 17 16:55:15 2018 +0100

    Add a summary to "24-hours"

commit 68a9059332f8a744ee1be237a4c6a99609dfc48e
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Tue Mar 13 16:23:57 2018 +0000

    a-plumbers-guide-to-git: less repetition

commit 9c57824caee6ce9d2de0b032b7241b3bfde02f50
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Apr 17 14:57:43 2018 +0100

    Add a post about "24 hours or bust"

commit 08e5389b0bfd38001ad50604dca4b21733ee6f17
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Apr 17 14:32:45 2018 +0100

    Continue adding notes

commit 9876db91c05df52da6553e3eb9a2c0596936ff9d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Apr 17 14:00:39 2018 +0100

    These notes aren't definitive ;-)

commit 20c9661c7ba64502800817230bd5189d4fb5da56
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Apr 17 13:51:34 2018 +0100

    A few more notes on anti-social-media

commit 20fb3b43da7b6a4c24a792bcde05fa1e06ecd612
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Apr 17 13:40:41 2018 +0100

    Put all the slides together

commit 54091af1f3837d99c990a595512bead9b8348872
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Apr 17 13:14:52 2018 +0100

    Fill in some more slides for anti_social_media

commit bbb3e5e4af9993f521560af94b803bd057c5270f
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Apr 16 09:39:01 2018 +0100

    All sorts of nasty messages

commit 9d3f5805e96c11af028730e2367e3b91c7870083
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Apr 16 08:47:14 2018 +0100

    Start writing up the first few slides of the antisocial media talk

commit e4ee5787f1eb5ac9a46d7eab9c9a3085bd22b321
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Apr 16 08:46:52 2018 +0100

    Fix links to tags in posts

commit 4465b6bd38242e193c8d228a0b6732f79bf3cb22
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Apr 14 07:10:37 2018 +0000

    More analytics/404 fixes

commit 6cb5fa20766a7a37405e05b1cc39f006552c24be
Merge: b0865934 e069faa6
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Apr 13 09:31:00 2018 +0100

    Merge pull request #143 from alexwlchan/tag-aliases

    Consolidate the 'talks' and 'slides' tags

commit e069faa6d2e2e3ac2cf765abc96500c0df56e14a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Apr 13 09:23:56 2018 +0100

    Create tag aliases on the /tags/ page

commit c9f439d495df4f567e39457847e2f55190d641ad
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Apr 13 09:22:54 2018 +0100

    Collapse the 'talks' tag into the 'slides' tag

commit b0865934995a0eba8a412c38b0287ee3fd33bbe0
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Apr 10 20:58:18 2018 +0100

    It helps if you include the actual talk data

commit 3429ceab0860bf83ef86ca3fdc53be8090873332
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Apr 10 20:49:09 2018 +0100

    Hey look, I'm doing some more talks

commit e952c0ab19913a1d85b0beb7085a84dc72a9d6d1
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Apr 9 21:56:37 2018 +0100

    Actually fix the publish-drafts task

commit 1e89ce5239016c5caddc3fcb4e82789d4d4713e5
Merge: 11b133d0 33a7ea09
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Apr 9 21:41:42 2018 +0100

    Merge pull request #142 from alexwlchan/repo-root-is-jekyll-root

    Make the root of the repo be the root of the Jekyll build

commit 33a7ea09fd61270d8afc8977e1764aef88237925
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Apr 9 21:35:10 2018 +0100

    Point the 'publish-drafts' task at the repo root (maybe?)

commit 01e50cfe9f514b8de44b487da26e7fc8995e965d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Apr 9 21:34:46 2018 +0100

    Point the 'deploy' and 'nginx-serve' tasks at the repo root

commit 975c139d014c92456d2bbd974ce3b55200ce06d7
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Apr 9 21:33:34 2018 +0100

    Point the 'serve' task at the repo root

commit f66479c2499ae0f30e17fcaa98232657e786c1e1
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Apr 9 21:29:32 2018 +0100

    Fix the theming plugin to run from the repo root

commit 626c781218d5bacbeedbd3a2f6f35a8894243a13
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Apr 9 20:47:19 2018 +0100

    Fix the twitter plugin to run from the repo root

commit 01b96bf0b9227219b66451932f87c8d4c2e89288
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Apr 9 20:43:05 2018 +0100

    Fix the static_file_generator plugin to run from the repo root

commit d76f69952aea2765dc5262e63f94fe8f7a694de2
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Apr 9 20:39:35 2018 +0100

    Move _config.yml into the repo root, at src/dst config

commit e46e9aa07776dd2d8707a2ce32d895a7caef0b7e
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Apr 9 20:39:00 2018 +0100

    Point the 'build' task at the repo root

commit 254b417034f3450686b9029d175005096d123f58
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Apr 9 20:38:17 2018 +0100

    Create a volume for /site in the Dockerfile

commit 11b133d01c92293eedccc258bd52d1a056b9946e
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Apr 8 10:37:33 2018 +0100

    new-standing-desk: remove a ref to my now-deleted Flickr account

commit 9625d47806a80b4524a5727be9b89909a20f8fa4
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Apr 7 07:49:06 2018 +0000

    More analytics/404 fixes

commit d9716eed91f6335469e0ea75220229910ba4aa1e
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Apr 2 07:22:33 2018 +0000

    One more lobste.rs referral alias

commit 51a2a500de650d24af67f9023ffce1d8ae87b603
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Apr 2 07:19:25 2018 +0000

    Start breaking out RSS subscriptions separately

commit 0629a4123b2296662813bcca5064cd04a3033f02
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Apr 2 07:13:07 2018 +0000

    Add support for tidying up lobste.rs links

commit af83de5c95bae347714ed24444cdce78f070e9ab
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Apr 2 07:04:24 2018 +0000

    Add a few extra t.co referrals

commit 9a774c0c7d7b27725826a9c76d545eeb19bc4cfa
Merge: c2dd2af3 527bdf32
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Apr 1 21:04:46 2018 +0100

    Merge pull request #141 from alexwlchan/untagged-infra

    Add proxy/SSL config for finduntaggedtumblrposts.com

commit 527bdf3291ffeb6a6e0216c7f17e06f8d4fe35c0
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Apr 1 19:45:47 2018 +0000

    Tweak the location of the certbot certificates

commit d319744606c13ca0106ee5d140b96fdaa65f4c56
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Apr 1 20:22:54 2018 +0100

    Add the infra for finduntaggedtumblrposts.com

commit c2dd2af32c31443fd8bfafe6b82e53bb05b4f87d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Mar 26 09:13:59 2018 +0100

    Fix a couple of nginx issues

commit a865e9ad654d8a091a27d153a410bef409e8f680
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Mar 25 23:19:59 2018 +0100

    nginx: add a bunch more redirects and 410s

commit b5b9c8c085e836622d5d29485efea8a9494fc6cb
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Mar 25 22:19:04 2018 +0000

    Add a bunch of bots to the analytics exclusions [skip ci]

commit 04dda94484a823db1e9f08ddfa3210f4a81f1627
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Mar 25 23:01:05 2018 +0100

    analytics: tidy up the report of 404 errors

    [skip ci]

commit 78e6b82bb93054ef49819fff229de1f9ffcfd2ef
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Mar 25 21:53:47 2018 +0000

    Use the new LetsEncrypt wilcard certs for awlc.net [skip ci]

commit 46968fbb3345fdd0ef5cf6d8db4f05e6aafa79d1
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Mar 25 13:37:40 2018 +0000

    More exclusions in the analytics report

    [skip ci]

commit eb8f8258962be331524bb718fc223fc620b54e7d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Mar 23 17:16:31 2018 +0000

    Exclude two more scrapers from the analytics

commit 23c75aea95f8e23363a685d05d52da110a67e14d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Mar 20 22:23:04 2018 +0000

    Post a fixed version of the CamPUG exercises

commit 1650e68afa512ec6908ae87357ac8df19eaf3daa
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Mar 17 10:18:24 2018 +0000

    infra: Simplify certbot renewals

    Specifically, take advantage of the nice symlinks they provide!  We
    shouldn't have to modify docker-compose.yml for every renewal.

commit 58c2219f7420bdd4f9e783db9536d79e1c9634ab
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Mar 17 10:15:09 2018 +0000

    Add pinteresting to the proxy conf

commit 86f2c47b7267cafa9275c4e58aab4b737026f7aa
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Mar 17 10:10:40 2018 +0000

    Auto-update docker-compose.yml with new cert config [skip ci]

commit cb53dcb2acb8c0725845f5168d9f046a693b8834
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Mar 17 09:12:22 2018 +0000

    Analytics fixes for 2018 week 10 (#113) [skip ci]

commit b656b9dcbfb23faf20e230989635074a7c7cc9fe
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Mar 13 20:40:40 2018 +0000

    atom.xml: strip HTML in the 'title' attribute of <link>

commit fa8834aefb33d59481f0c18a84a4a430fe20d0a6
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Mar 13 20:22:57 2018 +0000

    a-plumbers-guide-to-git: fix a typo on the intro page

    h/t @chailey_ on Twitter

commit 288199e0ece38a3e9d2a97ff4a16314e122c7c9b
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Tue Mar 13 10:55:50 2018 +0000

    a-plumbers-guide-to-git: less repetition in the summary repetition

commit f4bb2931afeb74d8b4c2a03caa7a60721fbc6067
Author: Travis CI User <travis@example.org>
Date:   Tue Mar 13 10:08:04 2018 +0000

    Publish new post a-plumbers-guide-to-git.md

commit be7200580825e64cd238f71a50b3bd4ab7081d1b
Merge: ad6ebb93 08cc2f96
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Mar 13 10:04:06 2018 +0000

    Merge pull request #140 from alexwlchan/git-workshop

    Add the notes, slides and post for my Git workshop

commit 08cc2f96d81f57490d364715bc87f2d600ad10d9
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Mar 13 09:50:55 2018 +0000

    conclusion.md: make the contact link more direct

commit 57a5d06cfaaa765f6178cd247574831e011d53e1
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Mar 13 09:33:37 2018 +0000

    head.html: strip HTML tags from <title>

commit 0c7d3f38a1d0fe05a1f7a6e54bfe9d5cda66e240
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Mar 13 09:31:48 2018 +0000

    a-plumbers-guide-to-git: linkpost from the front page

commit 37f4bd676b37e0c7ae9b751b39f70adcbec44ed7
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Mar 13 08:31:36 2018 +0000

    alexwlchan.net.nginx.conf: set up the appropriate redirects

commit 10582d7b5a0fc339209bc98b7cf5436988d04f56
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Mar 13 08:26:22 2018 +0000

    a-plumbers-guide-to-git: rename everything!

commit 427df1dd1ff363ea1cb1f03dad1724de64d90d7c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Mar 13 08:21:18 2018 +0000

    plumbers-guide-to-git: another go at fixing timestamps

commit 77f4444478c70ee2621dc4789cd0e42f643575d5
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Mar 13 08:19:15 2018 +0000

    plumbers-guide-to-git: bump the publication dates

commit b2349f5e2e3ea94c1cc8b640a71350a20e83cad1
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Mar 13 00:47:55 2018 +0000

    Move the contact link around

commit 5bbb6d59d05ef61382fe1aa31cd181fb741cebff
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Mar 13 00:43:11 2018 +0000

    Make that contact link more direct

commit 496a3dbb772428318a73fb21a35264d4fdea721c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Mar 13 00:42:41 2018 +0000

    plumbers-guide-to-git: cheeky link!

commit 0ff66e17368a4c1346d70f73ecbcf4acc7419fe3
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Mar 13 00:40:16 2018 +0000

    plumbers-guide-to-git: get it into a finished state for publication

commit e8d297918a8a317e924896c4bf0f760f37124d54
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Mar 13 00:09:41 2018 +0000

    3-context-from-commits: review markups and better diagrams

commit 5dc04ee25cc54b94eed2461767e1cf1e23fc0ab2
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Mar 12 23:51:50 2018 +0000

    2-blobs-and-trees.md: some review markups, better diagrams

commit c7b22f61d7e593a171f73783a98c75f546dcb9ae
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Mar 12 23:31:05 2018 +0000

    1-the-git-object-store: markups and extra diagram

commit a35d81a2a36d72ca1f0ed87ae4eaecdf14440297
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Mar 12 08:26:13 2018 +0000

    4-refs-and-branches.md: flesh out the outline

commit fed9779b2ab76d328b534149e24f951d9184a96c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Mar 11 22:36:40 2018 +0000

    plumbers-guide-to-git: add a reference to part 3

commit 0a8e1c9512538e90b30f38ac3cbf1496c739d375
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Mar 11 22:36:02 2018 +0000

    3-context-from-commits: flesh out the outline

commit 41b4553cee19ec273689fdb3a04e08aa12c4f8e1
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Mar 11 21:57:15 2018 +0000

    2-blobs-and-trees.md: finish expanding the exercises and notes

commit 68b7f1913ca97c13323f13395abeed19f6410acd
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Mar 11 21:47:03 2018 +0000

    2-blobs-and-trees.md: tidy up the exercises section

commit 560fb4ed5ce55924c62e22d4b0b0891caf467909
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Mar 11 21:45:29 2018 +0000

    1-the-git-object-store.md: a missing observation in the notes

commit 334490300d88f9fca4bc69b03aa225042afc993e
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Mar 11 21:45:19 2018 +0000

    2-blobs-and-trees.md: flesh out the theory section

commit f83c7a835be6aca40b294e62384c3f56968d660e
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Mar 11 21:45:10 2018 +0000

    Makefile: incremental builds for a better dev process

commit 7cb0154cf81696a96269eec81fce892b4a1fdb23
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Mar 11 20:43:12 2018 +0000

    plumbers-guide-to-git: link to part 1

commit 9a38b12b948c52771c26b0a67868e78e2af60ae0
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Mar 11 20:37:33 2018 +0000

    1-the-git-object-store.md: finish fleshing out the outline

commit 98e380cdbd622aa4be30b739e4ab9bd9f5bb8703
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Mar 11 19:52:37 2018 +0000

    Revert "home.html: move post separators into a plugin"

    197afd5dbf730c6bc9d8c7f2046ac235a24172f9

commit 145d68eee51b47fb1ff8dca1e948a8150e03bf18
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Mar 11 19:36:06 2018 +0000

    1-the-git-object-store.md: start fleshing out the outline

commit 0886cc5eb6733cd161d443aaec18016c060fbe37
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Mar 11 19:35:37 2018 +0000

    _text.scss: an <h2> that follows a post separator shouldn't have margins

commit 6d3575220c039187f3803cd9fa1b7b443223e5d9
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Mar 11 19:35:23 2018 +0000

    home.html: move post separators into a plugin

commit 38bd2e69dba91e76f7d1f9e629bbaf903a5cb6c7
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Mar 11 19:22:55 2018 +0000

    cleanup_text.rb: add non-breaking spaces to "part X"

commit 1a1cf3d0a48aad22c0ff04049bb7cd021adf15f9
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Mar 11 19:22:44 2018 +0000

    page.html: add support for arbitrary page metadata

commit d13d613a9a4d3c94dd4acd2ad6787f6f9ed746ce
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Mar 11 19:22:32 2018 +0000

    _code.scss: don't downsize code in <pre> twice

commit aeaf2f1f25e8ef258648ec3eeff4730517db3d89
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Mar 11 19:22:22 2018 +0000

    plumbers-guide-to-git: fix the top-level YAML metadata

commit 4cdecad14e61024320272b49c7dd62f30f93ba27
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Mar 11 15:19:10 2018 +0000

    4-refs-and-branches.md: write the initial outline

commit 9f1962fe5116648099bc0c49b4a34134c8f05089
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Mar 11 14:59:43 2018 +0000

    3-context-from-commits.md: initial outline

commit f46d9a1219c21b98355802d01c463536c4d96972
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Mar 11 14:43:28 2018 +0000

    2-blobs-and-trees.md: write an outline

commit f58e7548d544eeddd663e0556d7a695063939b1d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Mar 11 14:27:42 2018 +0000

    git-object-store: write an outline

commit ec739230826192cf2c96b57781c3885e3077d9f0
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Mar 11 13:58:01 2018 +0000

    plumbers-guide: Create the introductory page

commit ad6ebb938d841ea232e8500ef3642ee23f796a91
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Mar 11 13:24:56 2018 +0000

    Fix some broken links and analytics referrers

commit 4463470c1a2daa9de208accd77884866702298c1
Author: Travis CI User <travis@example.org>
Date:   Fri Mar 9 16:56:38 2018 +0000

    Publish new post plumbers-guide-intro.md

commit e4566511aed42ee079077186d9d32dd89e8ce4c9
Merge: 60810630 24df631d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Mar 9 16:52:37 2018 +0000

    Merge pull request #139 from alexwlchan/git-plumbing

    [post] A Plumber’s Guide to Git: Introduction

commit 24df631d63b067d6266caa1658a2096080bc084f
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Fri Mar 9 16:45:44 2018 +0000

    head.html: we only need smartlify, not cleanup_text

commit f6917d738c70ad74038c23f10d10e5c0ff5aca84
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Fri Mar 9 16:38:34 2018 +0000

    plumbers-guide-intro.md: finish the introductory draft

commit 4549020092469219d7fe415fca6dad8176d07e7e
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Fri Mar 9 16:22:50 2018 +0000

    plumbers-guide-intro.md: flesh out the first draft

commit db120073bd98ec80847a5c1d8f5aaccc48f2a513
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Fri Mar 9 16:22:40 2018 +0000

    head.html: use an interpunct in the <title>

commit 40cab7a880c1a1a0a2c2580f9fc1cc6eac3c41e9
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Mar 9 16:04:39 2018 +0000

    plumbers-guide: write the introductory post

commit 80d022337fde48ba2c245fed4d6b47ae6b543549
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Mar 9 16:04:25 2018 +0000

    _settings.scss: tweak the font size of inline <code>

commit 60810630b133362d4c5cb3f423bc96fdada58f04
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Tue Mar 6 18:17:55 2018 +0000

    campug_git.pdf: add slides for my CamPUG Git workshop

commit 070d313eeb860e389f973b19a2eef96cc30a2f6c
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Tue Mar 6 18:17:15 2018 +0000

    atom.xml: fix link post arrows in the RSS feed

commit 0535d4ccbb3517d08e9fa32cacbc6aec8f9c269a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Mar 3 09:17:38 2018 +0000

    _archive.scss: make sure the column accommodates every date

commit 94aecdc9ac51887e5668f5e5d6f75192ecfe6080
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Mar 2 18:44:14 2018 +0000

    atom.xml: the arrow in link posts only needs escaping once!

commit 72acc8a3b7b9679b685e4b6e6ee74a1a4d69926c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Mar 2 18:44:05 2018 +0000

    _post.scss: reduce spacing on link post arrows

commit 315b5e7b766bfda98c4ae55d1c06492e01e66522
Author: Travis CI User <travis@example.org>
Date:   Fri Mar 2 08:04:05 2018 +0000

    Publish new post continuous-releases.md

commit 91df091248e2ad916954696deda4f0f5833211c0
Merge: 5a4e2765 21adab76
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Mar 2 07:55:08 2018 +0000

    Merge pull request #138 from alexwlchan/continuous-releases

    [post] Link to my article about continuous releases

commit 21adab764962a033966d26c1cc84111875f1553d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Mar 1 21:52:34 2018 +0000

    continuous-releases.md: add a summary line

commit d45aff3c3a0f227aed508893e25834ebfb95ee9b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Mar 1 21:49:32 2018 +0000

    continuous-releases.md: tidy up the final line

commit 3f316234c26030ea7b5d477ca1661de5bbd1307e
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Mar 1 21:49:04 2018 +0000

    continuous-releases.md: link to my Hypothesis blog post

commit 5a4e276535e92542a4483d2df3e601440a78d509
Author: Travis CI User <travis@example.org>
Date:   Thu Mar 1 19:05:00 2018 +0000

    Publish new post overnight-bag.md

commit b77615c5360aff863d81c54a0d6557885971aba1
Merge: 5ce4560c 5a51dcfa
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Mar 1 19:00:50 2018 +0000

    Merge pull request #137 from alexwlchan/overnight-bag

    [post] Keep an overnight bag in the office

commit 5a51dcfa3ffa8fbf34b840e45720e430798b51df
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Mar 1 18:54:42 2018 +0000

    overnight-bag: Review markups

commit 562d048506da302d9a778ab5cfd26fe46ef6a7f4
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Mar 1 07:36:54 2018 +0000

    overnight-bag.md: Start writing this post

commit 5ce4560c7a0574bec546ea8586951be2113bca70
Merge: 98cff513 72fdc011
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Feb 27 23:21:47 2018 +0000

    Merge pull request #136 from alexwlchan/talks-page

    Bring the /talks page up-to-date

commit 72fdc011d058413d9cba425fce3671a2bc3cf827
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Feb 27 16:59:23 2018 +0000

    test_front_matter.py: 'talks' is a recognised layout

commit afe6a7a21efa7a577dc814f8d3115debfb24e90f
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Feb 27 16:50:48 2018 +0000

    talks: restore the old QCon London slides

commit a3b0f6d30371d2af2a8577ce60dd9d2264d211a7
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Feb 27 09:27:10 2018 +0000

    talks: finish tidying up the page

commit bd69f2711afb68b6d8ddec2124306cb04fab9658
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Feb 27 09:26:59 2018 +0000

    talks.yml: Add the remaining talks I can remember right now

commit 20276a072f59cac11bcc4459cde65a9eba9a8229
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Feb 26 22:50:54 2018 +0000

    talks: actually render them, add more data

commit 9c235267ab00d3318cea456fe9e1d1eaba3527bc
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Feb 26 22:39:33 2018 +0000

    talks.md: Establish a basic data-based workflow

commit 49d6dbcdc18a3af1d8272785f4c6843f5c92aeee
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Feb 26 22:33:06 2018 +0000

    talks.md: Start designing what an updated page might look like

commit 7ff7410259366df016d7200e71d577b2fd99c5db
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Feb 26 22:32:54 2018 +0000

    archive.html: Use Smartypants in the post archive

commit 98cff513a9e2a0d93baa6f7cb58fc96f3abacf39
Merge: e045d087 1b9f31e0
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Feb 25 22:01:31 2018 +0000

    Merge pull request #135 from alexwlchan/tag-redirects

    Redirect old-style tag pages to the new /tags page

commit 1b9f31e0ef60815fbd580bc3fa9a952273d65395
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Feb 25 15:44:11 2018 +0000

    test_nginx.py: remove the tests of tag renames for now

commit 584775b9fc0cac63268a869aef071a52581a35ce
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Feb 25 14:43:51 2018 +0000

    nginx.conf: for now, renamed old /tag pages are dropped

commit ec5ea77b6fe8fe644ec66493606a5781c1e88c89
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Feb 25 14:42:40 2018 +0000

    nginx.conf: You can remove the commas programatically

commit eed3d14e1ac124f551f99e368a7afddf9a9eb009
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Feb 25 14:42:27 2018 +0000

    nginx.conf: You need / and non-slashed redirects for /tag, apparently?

commit 54263208d8f0230dcd06e98c3f89cc39f369fc9f
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Feb 25 14:24:39 2018 +0000

    test_nginx.py: correct the expected redirects

commit 4261962f41f42d70725bc738cb7d0d95904bdf76
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Feb 25 14:19:42 2018 +0000

    nginx.conf: renamed tags go straight to new-style pages

commit e045d08797236323c17fa7673639cc8ff6e71291
Merge: 22edd724 c1a0d6f6
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Feb 25 14:16:34 2018 +0000

    Merge pull request #134 from alexwlchan/text-cleanups

    Add a plugin for doing text cleanups

commit e1ab75c95c40d000385960320c4eee2af89da352
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Feb 25 14:14:03 2018 +0000

    nginx.conf: be more explicit, we 301 to an HTTPS site

commit c1a0d6f6d917ad2bcd0aed0b9ec8c44cc291878c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Feb 25 14:11:46 2018 +0000

    test_page_content.py: titles don't end on the post title

commit 79e9c036dbb80eedbd91409f47d6519c41ae1471
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Feb 25 14:08:03 2018 +0000

    nginx.conf: Fix another tag with a trailing comma

commit e2c03e0a599d24c48a5bfc0a204a8f98d72b1015
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Feb 25 14:01:22 2018 +0000

    nginx.conf: redirect old-style tag pages to new

commit a3f120c2a5e067f1a8f770f90ec16abe2ff566bc
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Feb 25 13:43:44 2018 +0000

    nginx.conf: a few more consolidated tag redirects

commit 78b3f70b5cfe5a3f87d138e536882d832c4dd7de
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Feb 25 13:35:08 2018 +0000

    test_nginx.py: test that redirects work with and without slashes

commit fc0375715b7ae3af6b09ed8ff6e1bb52fc72eb05
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Feb 25 13:33:10 2018 +0000

    nginx.conf: redirects don't need the trailing slash

commit cf4e7d30a63567a70088056b7e98ddcff006f176
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Feb 25 09:23:39 2018 +0000

    cleanup_text.rb: stylise 'LaTeX' in a nice way

commit 0608bfe996d46794d3cfe5e4524edcbaac8c4062
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Feb 25 09:23:28 2018 +0000

    post_content.html: We don't need to escape titles

commit 7d71ca67370fde2655935d70e00405d28d2c74ad
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Feb 25 09:18:14 2018 +0000

    page.html: Apply text cleanups on pages as well

commit 3cb7a3344f0ac9b8f2d80acb45b8f93739d5dc29
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Feb 25 09:17:30 2018 +0000

    ips-for-documentation: remove now-unneeded &nbsp; markers

commit 9f8bfb346dffc32cd849b6de2c2aee847471d2ee
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Feb 25 09:17:18 2018 +0000

    test_links.py: rename to test_page_content.py

commit fe6f18ebae5669cfee216fee4851e0c17081daa5
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Feb 25 09:17:02 2018 +0000

    test_links.py: add a test for the cleanups plugin

commit 01c49f5f3a193028736ad231a599de88d0724008
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Feb 25 09:16:42 2018 +0000

    cleanup_text.rb: add a plugin for fixing RFC spacing

commit 22edd724f7d657ff5a14e38d29c090c446dc851f
Merge: 9a37516b c0a89fb7
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Feb 25 09:08:26 2018 +0000

    Merge pull request #133 from alexwlchan/css-caching

    Implement primitive cache busting for CSS

commit c0a89fb73c9d41f0236318adaf212294a02f5600
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Feb 25 08:51:01 2018 +0000

    head.html: include the time in the CSS path for cache busting

commit fd563c75fd00e7e892c118bfbbfc7dfbf93ffe99
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Feb 25 08:50:42 2018 +0000

    head.html: Remove an outdated comment

commit fd5f37e9a640a8602ce901a13dd0bee4414a2562
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Feb 25 08:40:45 2018 +0000

    _settings.scss: bump up the font size of the smaller elements

commit 9a37516bd4f5f9097041ed4f201da19b11d1ecb0
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Feb 24 07:28:25 2018 +0000

    Analytics fixes for 2018 week 07 (#113) [skip ci]

commit 01f879c673d375177e4c7469765531d7e1e5dab4
Author: Travis CI User <travis@example.org>
Date:   Sat Feb 24 06:51:46 2018 +0000

    Publish new post working-from-home.md

commit c66d1876f924a7d150779af05ec7a5c9d02b3581
Merge: a7a9964c 64bec631
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Feb 24 06:48:05 2018 +0000

    Merge pull request #128 from alexwlchan/working-from-home

    New post: “A working from home experiment”

commit 64bec6311a1088897ed7a6d316c0f6657053c11a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Feb 23 19:37:17 2018 +0000

    working-from-home: a better summary

commit 3c6d3a843b50422b9d3eaa51391460980c64b988
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Feb 23 19:36:39 2018 +0000

    working-from-home: Add some sort of summary to the post

commit eee8325a1a4b8791f3432d494da6f3aa0a9bc999
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Feb 23 19:34:21 2018 +0000

    working-from-home: review markups and copy edits

commit e7fd0c4bdf01448524883437600d6fe6db954ffd
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Feb 23 18:13:47 2018 +0000

    working-from-home: another round of drafting

commit e54f4b73b51e3bb52504c24b557ed14585f16444
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Feb 23 18:13:37 2018 +0000

    scss: bump up the default font size (again)

commit 64450c7b1dc790f363267b473dbe7cf21368f8c9
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Feb 23 15:17:10 2018 +0000

    working-from-home: this belongs in _drafts for now

commit d4c69ed6d5019a8b340d3af56fe3c60fd67a297c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Feb 23 15:15:01 2018 +0000

    working-from-home: add the first part of this post

commit a7a9964c9e8edd36028237f6177f362da9e53a52
Merge: 7e8ee49e 057c5b79
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Feb 22 09:14:05 2018 +0000

    Merge pull request #127 from alexwlchan/tags

    /tags: redesign the page, make it more discoverable

commit 057c5b7971c02aad2e8e2a7f35beab0e1049d63b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Feb 22 08:58:16 2018 +0000

    test_links.py: Adjust the archive page test

commit 3958b894757a9e87fdd98f4e2437230f38210e80
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Feb 22 08:49:50 2018 +0000

    post_content: link to the new /tags page

commit cc9bd20d66d7009ffddbeade2c733f535e362d30
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Feb 22 08:04:15 2018 +0000

    archive: link to the tag pages

commit 448de6cdf8cea0b76fb65ac7e58b0d82694ddff4
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Feb 22 07:59:22 2018 +0000

    tags: render the tag index as a cloud, not a list

commit eb5bb02416ccfeb70a7fb267e7ebf284ebb8c918
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Feb 21 09:04:51 2018 +0000

    cat_and_tag_generator.rb: we don't need distinct tag/cat pages any more

commit 50f99a62c4b06cfa0a350ce2e2125bc88a1d8f22
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Feb 21 09:02:37 2018 +0000

    tags: Include a list of all posts in a tag on one page

commit a49d7d5cb8d9f7ae34c8e984729174aab9c61170
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Feb 21 08:55:41 2018 +0000

    _posts: Fix the spacing on a tag

commit 7e8ee49eafcfbb03bc72910ebec80a43243c5337
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Feb 3 09:14:33 2018 +0000

    Analytics fixes for 2018 week 04 (#113) [skip ci]

commit 6387bbbf0a4a1bd109ded68a54eb6d470100573c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Jan 27 23:49:52 2018 +0000

    Analytics fixes for 2018 week 03 (#113) [skip ci]

commit 7b66b816c48d7c566d43b060cc1370edb7f15344
Merge: 6a23b590 33bb23c1
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Jan 27 23:44:06 2018 +0000

    Merge pull request #121 from alexwlchan/certbot

    Add a script for renewing certbot certificates

commit 33bb23c1cefc8ea7c5638f9aaa3bdfad919cc248
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Jan 20 09:23:24 2018 +0000

    Analytics fixes for 2018 week 02 (#113)

commit 16ab8a8b1f6770571ce9b1b0e1e9bd500095731b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Jan 20 09:24:53 2018 +0000

    Revert "Analytics fixes for 2018 week 02 (#113)"

    This reverts commit 1936bd40e8a9348607dcbdc6d80b097e972a7e5e.

commit 11f8b126cffd62673b5d1788ee57a1f34f781e62
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Jan 20 09:23:24 2018 +0000

    Analytics fixes for 2018 week 02 (#113)

commit bf05bdc60d3e1c9c4e6020db656004a7fba3e72b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Dec 19 08:20:31 2017 +0000

    Use the official certbot image as a base

commit 7687800ca8e8635100777a7995afc2e532556a0f
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Dec 17 21:07:02 2017 +0000

    Auto-update docker-compose.yml with new cert config [skip ci]

commit d205d94cf1c851bf9ddb371c113111732821a86c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Dec 17 21:06:28 2017 +0000

    One more archive fix

commit 8a4872dc57a6fd7fd022d50fcefbbd89a27e4b63
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Dec 17 21:05:39 2017 +0000

    Navigate the certbot folder hierarchy

commit bf8744454ed95643c3184d037512d4c15fd77cd2
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Dec 17 20:57:42 2017 +0000

    Expose docker-compose inside the container

commit 71143f9cab21a3fcb4eed35bf101772ab2af10fe
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Dec 17 20:57:09 2017 +0000

    Auto-update docker-compose.yml with new cert config [skip ci]

commit 2f16e92c730f4a1184f4a7d4a241064ef0b854da
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Dec 17 20:55:26 2017 +0000

    Fix a couple of script bugs

commit cf22d204bf0dc209212874ac31618e2ff7460430
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Dec 17 20:50:49 2017 +0000

    Commit changes to docker-compose.yml

commit a864964568f2f60a3bf125c146c5db923edc8573
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Dec 17 20:49:26 2017 +0000

    Share the whole repo into the container; restart the proxy container

commit e8f6c9e0232217b3c116ef92cea9a0d644b7042f
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Dec 17 20:47:55 2017 +0000

    And get the end-to-end basically working

commit 59ca6c0306de1d0c972e960511f8b6c6ca23afc6
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Dec 17 20:43:01 2017 +0000

    Add a requirements.in and initial Makefile

commit a8142cd742b11ca049ae6ab32d9f3d55ccfb6618
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Dec 17 20:41:58 2017 +0000

    Add a script for renewing certificates and updating docker-compose

commit d4b6c70e4e63f62c2f320c41b61add848af57467
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Dec 17 20:29:14 2017 +0000

    Don't share all my certbot config with the proxy

commit 6a23b5904f0668509a3ed98d193c34edc1b680ac
Author: Travis CI User <travis@example.org>
Date:   Thu Jan 25 21:56:15 2018 +0000

    Publish new post downloading-sqs-queues.md

commit 8e59ac03cbd5b3a05203c518cb142eb2bdf43007
Merge: 653a0731 87ac4b22
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Jan 25 21:52:07 2018 +0000

    Merge pull request #126 from alexwlchan/sqs-queues

    Add post about getting every message in an SQS queue

commit 87ac4b2254702c19cd2c30386b69fe435fe6c315
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Jan 25 21:42:08 2018 +0000

    Add a summary to the SQS post

commit ec7d983424a3346371ca67e2aa2dd7c7ab7a0f0a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Jan 25 21:41:05 2018 +0000

    Markups on the SQS post

commit 7802ae553a4837153d68e17627b4d7cc2daf0a49
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Thu Jan 25 18:24:11 2018 +0000

    Second draft of my SQS post

commit 653a07316a3fa9a8cc3cd19a612320825261eb2e
Author: Travis CI User <travis@example.org>
Date:   Sat Jan 20 20:25:33 2018 +0000

    Publish new post listing-s3-keys-redux.md

commit 9aaa1ad1a6699f621c402134c37333fd1e467bc3
Merge: 1335c5d4 bb182298
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Jan 20 20:21:35 2018 +0000

    Merge pull request #125 from alexwlchan/s3-keys-redux

    Write an update to my "listing keys from S3" post

commit bb182298e2244e9275cdf2ebf03f371e8128432d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Jan 20 20:12:41 2018 +0000

    Link to the update in the original post

commit 80338223db0f2507dc2dc14684689ed03f9744b7
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Jan 20 20:09:44 2018 +0000

    Write a short update to the listing S3 keys code

commit b96aad5debc6409685d62a5c1238c092968ae670
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Jan 20 19:21:33 2018 +0000

    Move everything into the code repo

commit 1335c5d48812b4b1e82830518d694e039aeb139c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Jan 20 09:23:24 2018 +0000

    Analytics fixes for 2018 week 02 (#113)

commit b51f9678c44722d6e3cc545d5fd6ae30311f8871
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Jan 20 01:23:31 2018 +0000

    This isn't a minipost really

commit 876ec72fa0e947651c5799abc978c49859c36df0
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Jan 20 01:20:53 2018 +0000

    Tweak the post separator

commit ca51db339d213673216c3101f01e40457b95a856
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Jan 20 01:14:36 2018 +0000

    Tweak the appearance of the header

commit ef326576b7f422447b6fdcb92a4cec02c94d2dde
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Jan 20 01:13:45 2018 +0000

    Restore pronouns to the About page

commit eb672efc2b1c20b7cfff195f45e5968512162473
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Jan 18 23:28:09 2018 +0000

    Write a post about IP and DNS addresses for docs

commit d6323059ecf1634dea6db240d8054e030797c5bc
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Jan 18 23:04:15 2018 +0000

    Improve the about page

commit 13a1bbff8cbb2fad377bd88373067594c58bb039
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Jan 6 09:35:19 2018 +0000

    Analytics and nginx fixes for 2018 week 00 (#113)

commit 03ed46f65e93983514881a236b3d347c356b4b5f
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Dec 30 10:58:41 2017 +0000

    nginx config tweaks for 404s

    Related: #113

commit 33251529c47cc47e4fbfd761174c756507f7acf8
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Dec 30 10:54:40 2017 +0000

    More spam/cleanups in the analytics report

    [skip ci]

commit 05dda330d879ba6d77306e6c852f465489aa231b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Dec 26 09:16:18 2017 +0000

    Exclude the unmanaged directory on the web server

commit 924c8fec570c3c944a9cab9865d07c48fe734d06
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Dec 26 08:43:55 2017 +0000

    No /wp-admin/ to be found here [skip ci]

commit ce61f19919c5a453aed9f73cf7c3cff552e10567
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Dec 22 07:54:49 2017 +0000

    Allow an empty user agent in analytics

commit e1a224074ed43306347772927f9d2b2048825a77
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Thu Dec 21 17:22:46 2017 +0000

    Allow dot_list to split over lines

commit c4e6d3e48374ceea301474d5452a35a6c160e250
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Thu Dec 21 17:22:04 2017 +0000

    Revert "Miscellaneous CSS tweaks for bigger text"

    45b6d53e057479cce205b41f920b8300ea734762

commit f9d9f40d824be9f8e363f0adf7c0355b064463b4
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Thu Dec 21 17:21:46 2017 +0000

    That link was never going to work in nginx

commit df1b5c133bb0878e84eca9ba613036fdedb78c23
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Thu Dec 21 10:36:23 2017 +0000

    Fix redirects in the Travis tests

commit dac5b99864fd45626ce95b71a5f0796d30dc2499
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Dec 21 08:28:00 2017 +0000

    More updates based on analytics (#113)

commit a1b272e059ba47b871a927e02b652a725ae79cf3
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Dec 19 22:44:30 2017 +0000

    Another round of redirects and report fixes (#113)

commit ede16a2bede25c85160fb53e3323ebf77db236be
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Dec 19 22:39:24 2017 +0000

    Set up some more 301 redirects

    Related: #113

commit 8c8114cf5cb0b5a39cdda70a8a2be6e5c481103c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Dec 19 22:36:30 2017 +0000

    Cut out more noise in the analytics report

commit fa98ce8aa117c45233d54cf02651f8e3c55db903
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Dec 19 08:21:46 2017 +0000

    Miscellaneous CSS tweaks for bigger text

commit 5ca88766537c01d22461be9d284de5aa8671dfb4
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Dec 18 18:59:03 2017 +0000

    Don't forget the trailing newline!

    Resolves #123

commit 3ae46dfb537634b7a89f93ebdc3a82dbab3a2d6d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Dec 18 08:43:40 2017 +0000

    Update 2017-12-18-building-your-repo.md

commit 539f7aa7ad610e75fe649211067bfab8213caba0
Author: Travis CI User <travis@example.org>
Date:   Mon Dec 18 08:40:30 2017 +0000

    Publish new post building-your-repo.md

commit 06eccfa656cc1038779e1469ec0cf9143c439562
Merge: 4820049a 956f52e1
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Dec 18 08:36:40 2017 +0000

    Merge pull request #122 from alexwlchan/building-repos

    Add my post about making repos easy to build

commit 956f52e17729cfa8758836411735ffaf66bbdcd0
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Dec 18 08:26:04 2017 +0000

    Add a summary and a typo fix

commit 11fca945e288927cee7e01044332136f9db0b097
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Dec 17 20:11:31 2017 +0000

    Remove a trailing comma

commit d45fd65b330477a86595e6449fe9a6524e4f3c77
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Dec 17 20:00:32 2017 +0000

    And make a few more markups

commit cdbffeb14c3a52cf6a2d2a39c7026999a2905722
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Dec 14 20:16:10 2017 +0000

    Improve the front page grab

commit 2ad4f118175575d53da67d739d30caf9f45aecf2
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Dec 14 20:14:12 2017 +0000

    Another draft, substantially fleshing out the howto section

commit a6d69cf84f235dc10a973f5ec282ca741b9588a4
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Thu Dec 14 00:31:08 2017 +0000

    Put my tweet onto the post

commit 3ccd19fc8e44cac043ba0b377687ce5af2c9c04d
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Wed Dec 13 23:06:41 2017 +0000

    Add a first draft of the "building your repo" post

commit 4820049a0052ce2598de96edff9d050ffd30161a
Merge: a07a46b7 a1ad8d92
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Dec 17 10:57:33 2017 +0000

    Merge pull request #120 from alexwlchan/fix-tags

    Fix broken links on tag pages

commit a1ad8d926e788c6435ef19da1a8905b4377edd53
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Dec 17 10:47:26 2017 +0000

    Add redirects for old tag pages in the nginx config

commit 4eb37a34fa72a3790a6ca47d1d1488a55bcd93cd
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Dec 17 10:43:48 2017 +0000

    Replace /tag/pycon with /tag/pyconuk

commit 8f0404251b4763d80f43ccb4ab6beb9d99601c02
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Dec 17 10:43:02 2017 +0000

    Don't use slashes in tag names

commit acb78694d18df49dcd773a1acd6ecd1e9d6bc356
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Dec 17 10:36:47 2017 +0000

    Add a test that tags don't have a trailing comma

commit a6e82445c94266d5d6274acde8cbc62e8becf27a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Dec 17 10:34:08 2017 +0000

    Allow running tests outside Docker

commit 1150596c0a4f676f3e83fe6f2796805550fbb5fc
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Dec 17 10:32:56 2017 +0000

    Add a page that lists all tags at /tag/

commit a07a46b78d2e16969ba2a48bb7f672c09138423a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Dec 16 13:39:23 2017 +0000

    Combine all search traffic in analytics [skip ci]

commit 7742fe580e8cf100f9ba06d547e068f251e0135a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Dec 16 13:24:22 2017 +0000

    Bugfixes for referrer reporting, 16 Dec 2017 [skip ci]

commit 23ea8456c68c0722833f6b1a3f4c467836f775ce
Merge: 39862e8b e1110e83
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Dec 14 00:17:45 2017 +0000

    Merge pull request #118 from alexwlchan/drafts-with-dates

    Publish drafts with a time as well as a date, and other front matter fixes

commit e1110e8319a7150309d1e1479beaa76c02575a3f
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Wed Dec 13 23:28:51 2017 +0000

    Rewrite some front matter for consistent ordering

commit a29ae00648f7b2aed8de017bb566020291282e66
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Wed Dec 13 23:26:22 2017 +0000

    Change post filenames to match their slugs

commit c147e041ae01d4efc0956d51ff50bd644a437f86
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Wed Dec 13 23:25:08 2017 +0000

    Remove redundant slugs from the post title

commit f8a3fae6e8ff6834d9ac39916fe563b8f3fa1036
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Wed Dec 13 23:22:35 2017 +0000

    Ruby gives us the correct format by default

commit 3c87ae99e966d3fa92ad2769dd9875d45a397f69
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Wed Dec 13 23:22:23 2017 +0000

    Backfill old post dates based on commit timestamps

commit faabf50c2e480723cc191809d60a92dc6b73e69a
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Wed Dec 13 23:17:43 2017 +0000

    Write an unambiguous date into the top of files

commit 39862e8b279ca547dd045befd76650f5081c67db
Author: Travis CI User <travis@example.org>
Date:   Mon Dec 11 12:19:24 2017 +0000

    Publish new post armed-police.md

commit 97cf12d3f3a1dee9fa50e41d4f92fb776ec62557
Merge: 46a69659 4f15e203
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Dec 11 12:15:52 2017 +0000

    Merge pull request #116 from alexwlchan/armed-police

    Write a post about armed police

commit 4f15e2037063beba7e703fb3888677a1975c8f2a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Dec 11 12:10:53 2017 +0000

    Add a summary to the post

commit 7649e1611e26fae7c4535f971c14248cc128d84b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Dec 11 12:04:53 2017 +0000

    Content warning is a post field

commit 5dba0886adc9e6bd85f7f15f88e23956fe7fc525
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Dec 11 12:01:50 2017 +0000

    Markups on the armed police post

commit 244aa726fb1f2dc7ff4b5f3226b9811b68406bfc
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Dec 11 11:58:46 2017 +0000

    First draft of my armed police post

commit 64de2ab1b0e6e87ddf459a7ee68c7df918bd21b8
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Dec 11 11:58:34 2017 +0000

    Don't show the footer on printed pages

commit 171026999e4b6f6dc00d576bcd536cf6b2fe0e12
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Dec 11 11:58:26 2017 +0000

    Don't check in my Twitter credentials

commit 2f26e3b59ba9a765e9e881b00570975aa30c7c5d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Dec 11 11:58:15 2017 +0000

    Support saving tweets with no media entities

commit 46a696593ad2fef33221f2e5443d2d24401d2866
Merge: 317b0fc7 ba309c24
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Dec 9 23:30:53 2017 +0000

    Merge pull request #115 from alexwlchan/fix-some-404s

    Fix the first batch of 404s spotted by analytics

commit ba309c24a3f76501cd27ec505d817485dce29ea6
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Dec 9 23:26:54 2017 +0000

    Fix one last link

commit cdd29b7631ce85fe5ecc48a6277356ccca1b01aa
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Dec 9 22:42:03 2017 +0000

    Fix the atom self declaration and one more test

commit 62b39b184ec6e0eb73a14a9f8e9d76011d27e711
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Dec 9 22:37:03 2017 +0000

    Fix the tests to point at the right atom feed

commit 57b4606ecf17ba6c71ecfc8dc7e494600e409e46
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Dec 9 22:30:49 2017 +0000

    Delete trailing whitespace

commit 6aea4423e4c8a5662d831436141b9a96b2a9eb70
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Dec 9 22:28:38 2017 +0000

    Don't reprint that it's a 404 in the 404 list

commit d290c3fa1efd579cffbdf70c9b3076585b932ae9
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Dec 9 22:28:15 2017 +0000

    The final few 404 errors

commit 65e701e58ffdf7aeb0f21ba1db08332d63066d35
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Dec 9 22:27:20 2017 +0000

    Add some more podcast-related stuff as 410'd

commit 1af587a8a36556eb6b5768adbb9c935694ae08f8
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Dec 9 22:17:12 2017 +0000

    Redirect a couple of images to the correct location

commit 39d15c58556063e1b8fb27ccd1fe65f433c08f9c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Dec 9 22:06:05 2017 +0000

    Add a robots.txt file to the site

commit 2de35cc7a8ee70e0b8a40dae9290882800553cfc
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Dec 9 22:05:14 2017 +0000

    Put a file in place for /atom.xml

commit 2223b6696ba96b7999939bcf197b9b94ea116e30
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Dec 9 22:01:19 2017 +0000

    Exclude 410 errors from server error reports

commit 317b0fc7b2a4aaadb05497ff7fd5366d86dcc343
Merge: f0807ae4 af9bbe21
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Dec 9 21:56:58 2017 +0000

    Merge pull request #114 from alexwlchan/fix-404s

    Define custom nginx config for the site container

commit af9bbe215a8b4a152246c0974dd77706c0be4c8f
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Dec 9 21:52:56 2017 +0000

    Get the nginx tests passing in CI/Docker

commit 2974b8552b72e8778b91554e37b335a2ad4a87e7
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Dec 9 21:47:49 2017 +0000

    Let's get the hostname right

commit ea458cd78fa43eab2e3494b3fa324d62e7a0e3b6
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Dec 9 21:42:56 2017 +0000

    Publish the nginx container into the test container

commit 477c085136b38b6f4dff651c9ed3bfb40a47a79a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Dec 9 21:37:14 2017 +0000

    Delete some more unused nginx config lines

commit 01789230828badd7e0e17aaa9baea4fee3ffc204
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Dec 9 21:35:34 2017 +0000

    Consolidate more of the nginx config

commit da60e140f5a71f86e5a02c0d9e8167964c425b77
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Dec 9 21:32:45 2017 +0000

    Get the nginx tests working locally

commit 6891fd0536baf91a273300cd365406974d06f47b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Dec 9 21:08:50 2017 +0000

    Push those 410s down into the main container

commit 4e467fd841cfce0a994373ebd1f4351d931d4160
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Dec 9 21:06:56 2017 +0000

    Add a couple of status code tests to nginx

commit e513a33ac9c6c5e3b5c700ae633e0f853cd23dd6
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Dec 9 21:04:34 2017 +0000

    Run the nginx server in CI

commit fd7233bc1cf9ec454f301b1abbab51e1f44c4089
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Dec 9 21:02:38 2017 +0000

    Add a shortcut for testing the nginx config

commit a387f958fe5476173b6dcfdbd6303776ffc30875
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Dec 9 20:59:03 2017 +0000

    Make sure nginx knows where to find the files

commit d65b9e9e48ec9423ac75428c84741e0e2291cee8
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Dec 9 20:58:56 2017 +0000

    We don't need to share certbot config

commit 4c624b9b2c3e353c175da86e8095893fdb83b8be
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Dec 9 20:57:23 2017 +0000

    Point the server at a different hostname

commit 1ea4dc442852f1b039db97a14f41aeae08d97b12
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Dec 9 20:56:25 2017 +0000

    Put an nginx config file inside the site container

commit f0807ae4f0b75157b714c6e7fd9470b9f340f860
Merge: c7da0e75 1d4912bd
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Dec 9 20:52:02 2017 +0000

    Merge pull request #112 from alexwlchan/analytics-cleanup

    Big cleanup of the analytics parser

commit 1d4912bd9d3a2e5c76750383b618c73075087f5d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Dec 9 20:48:44 2017 +0000

    Add a brief README for the analytics

commit 3fe20738744a82e16c62cb07cbb50c380c6fe07a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Dec 9 20:44:17 2017 +0000

    Ignore Wordpress/PHP spam

commit 9e39c6381ba38e384cac73425e4a34a63eafb8e6
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Dec 9 20:41:19 2017 +0000

    More permissive about statuses

commit 69ecf2e0ade120521be560d8700a97051eca73db
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Dec 9 20:40:10 2017 +0000

    Don't count 304 Not Modified as an error

commit 3eadae39f3652f468bfd8f6145397e1b1c30ca67
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Dec 9 20:39:28 2017 +0000

    Also print 404s and other server errors

commit 49eb6575262d219af23e9019590b25ec962668b5
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Dec 9 20:36:59 2017 +0000

    Delete some dead code

commit a400adcfcc02221bc6b454ac9a22984838137f81
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Dec 9 20:36:05 2017 +0000

    Don't read the original referrer

commit 0f6247e3cddbd3e37378dc9c5855aa4598a63d2d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Dec 9 20:33:19 2017 +0000

    Handle empty referrers correctly

commit 84f3ac12816b0568324a72ca31dc3a75326630ce
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Dec 9 20:29:43 2017 +0000

    Fixes in referrers

commit be96b8c259007101c11be93c8fbdc1edfa59b0c1
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Dec 9 20:27:04 2017 +0000

    Add a few tests for the analytics code

commit 95dbf13fe1880a756a25488a46ed408852045804
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Dec 9 20:12:18 2017 +0000

    Be more permissive about requests

commit 839853aaabca4a5d0d0fa98d3286f6bc3bffeb49
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Dec 9 20:10:39 2017 +0000

    less crappy error handling

commit 2e2052d0b40f8e356169653b5a2bda2a7516f2b1
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Dec 9 20:08:05 2017 +0000

    Break up the generators a little

commit fd39fc067547a4f5d9023aca2aecddc08904cc4a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Dec 9 19:51:16 2017 +0000

    Tidy up the CLI options

commit 2b4f4ed86cfa2f1dd08a387e73cbb4651e323d78
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Dec 9 19:38:10 2017 +0000

    Don't stream stdout directly

commit 342fc1c65262982cfb525ed83a3ab9c98ae7ef5b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Dec 9 19:36:09 2017 +0000

    Actually limit the records retrieved

commit 2457ca9f296d288b759709914b53847f169f58df
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Dec 9 19:31:36 2017 +0000

    Add a make task for actually getting the logs

commit 6e7bc7e380d4d9c20e5d6b6bf8975666358fbddd
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Dec 9 19:21:06 2017 +0000

    Have the report script read directly from the container

commit 6f3e432d9b82268199d9ac3c8c667b8825cfdc68
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Dec 9 19:17:14 2017 +0000

    Add a Docker image

commit 9f79fc8ee030d65a2f8d19867e86f948e20a07f5
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Dec 9 18:57:38 2017 +0000

    Add a Makefile for building a requirements.txt file

commit 8a000fcaf18362146919b6d05009f2b037a1276b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Dec 9 18:55:43 2017 +0000

    Add a requirements.in for analytics

commit a87e9b57b28235ba32fe157ec4b7072f496c607b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Dec 9 18:55:28 2017 +0000

    Tweak the regex to pick up the forwarded host, not the proxy host

commit c7da0e75c4036f6c74308619ccc0b67b1b2a4198
Merge: fb02f523 22ba82ac
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Dec 8 18:17:13 2017 +0000

    Merge pull request #110 from alexwlchan/about-the-site

    Add the "about the site" page

commit 22ba82acc6012e0b1966af1bb84fb342d6b94d9b
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Fri Dec 8 18:09:50 2017 +0000

    Bump requirements.txt to match new lxml version

commit 55d04798dbd0da49b3dea645c111a31b1280216b
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Fri Dec 8 17:51:32 2017 +0000

    unzip doesn't need to be that verbose

commit 540a044cb2e0a5a45a3933a62a16ef15e866b50b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Dec 8 07:54:10 2017 +0000

    Fix the Twitter card on the WITCH post (maybe?)

commit 762dd21b16a67865b520a7a0f747113b9264d971
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Dec 8 07:53:54 2017 +0000

    Add the "about the site" page

commit fb02f523acc153f81643fd216affee84971a7d26
Merge: e82c5992 7d93add0
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Nov 29 21:20:40 2017 +0000

    Merge pull request #109 from alexwlchan/analytics-from-nginx

    Serve analytics from nginx, not Flask

commit 7d93add0b631016a20eb855e2cbb1d0ef84781ea
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Nov 29 21:19:00 2017 +0000

    Return the correct referrer

commit 7e81ff56569822be625be80d1889753f1a6d5b19
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Nov 29 21:07:43 2017 +0000

    Fix the name of the analytics.js file

commit 436a0a9f91c735c624fe5d36f7e51770638c5800
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Nov 29 21:07:30 2017 +0000

    Remove the analytics Makefile

commit 423d3f9deb18125c3f7fabe5a188fa82b0e53666
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Nov 29 21:07:00 2017 +0000

    Delete more unused code

commit 34d1e203a1fac5fb34e4e55445aeb3b686bc7d9f
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Nov 29 21:05:46 2017 +0000

    Continue deleting unused code

commit 4056aa3fee52bab8daa45d2c8d261c52614afc48
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Nov 29 20:47:27 2017 +0000

    Get a list of structured blobs

commit 2e34b3d2b41fc74cbf6bd32a5decd67c41618a05
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Nov 29 20:34:59 2017 +0000

    Put back the argument parsing

commit b4b8e810a805499f8c101450d2a8ba7c14fb351d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Nov 29 20:34:07 2017 +0000

    Get a log file with interesting lines

commit a65a56be93a5ccb36abb9f3b71a6c6b9e7366784
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Nov 29 20:31:45 2017 +0000

    Copy the latest log file to local disk

commit 7cc4305ca277335ea04cb1ae45696a68c479e2d8
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Nov 29 20:23:53 2017 +0000

    Import command-line argument parsing

commit e769b472f64ad7d3a3a734afc2acd159a6cc3cca
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Nov 29 20:20:27 2017 +0000

    Delete all the code for the analytics container

commit b1385b48eb72b3fde4d0a0f6784e2b818c3604fc
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Nov 29 20:05:27 2017 +0000

    Move the analytics pieces into the main site

commit e82c5992dc1b19db83daa5ad638759ccd9723175
Merge: ed09f8a4 7ea09c05
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Nov 28 20:56:57 2017 +0000

    Merge pull request #108 from alexwlchan/do-not-track

    Don’t collect analytics for anybody who has Do Not Track enabled 🙈

commit 7ea09c052110a49b37a84ef9586d53a236f33126
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Nov 28 20:55:57 2017 +0000

    Fix the analytics script to run properly

commit b357346559ef8cdb1c0ff2e97aa77f01b98308d6
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Nov 28 20:50:04 2017 +0000

    Tweak the Makefile deps

commit 87a1bd5a664c9f9f227e1fdf52f451153249995b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Nov 28 20:42:00 2017 +0000

    Don't make an analytics call if Do Not Track is set

commit 1b098c39801840f36bd7065bf93ca81c71c1dbd4
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Nov 28 20:37:14 2017 +0000

    Include the JavaScript in the Dockerfile

commit bbc789d347f1e5ec1730e50a23d98ede2f7dc192
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Nov 28 20:36:54 2017 +0000

    Read the analytics JavaScript from a file, minify at startup

commit ed09f8a4a6d3c036d8549aaa62ca9c9c9d1adc2e
Author: Travis CI User <travis@example.org>
Date:   Mon Nov 27 22:41:36 2017 +0000

    Publish new post pruning-git-branches.md

commit 19928700ebfb82761b7d983420d7cfda1692d1f0
Merge: 6a45bed5 aa872a7a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Nov 27 22:37:57 2017 +0000

    Merge pull request #107 from alexwlchan/git-branches

    Add a post about pruning old Git branches

commit aa872a7ac11b53fd69f4d5f755afc1f39bfeb5ce
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Nov 27 22:24:09 2017 +0000

    Add a post about pruning old Git branches

commit 6a45bed5abd8840427805bc499199010aea6bb42
Merge: 6a413b63 2e6f38fb
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Nov 25 23:37:38 2017 +0000

    Merge pull request #106 from alexwlchan/custom-errors

    Return custom pages for 404 and 410 errors on the main site

commit 2e6f38fb580935ad4b2291f57065af5568545e78
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Nov 25 23:36:29 2017 +0000

    Serve custom 404/410 pages from nginx

commit edf665706041fc76c35dc0a1dda230b9acb9016f
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Nov 25 23:10:41 2017 +0000

    Create custom 404 and 410 pages

commit 6a413b6353fce59cf2196ab2ae9dbfb577198a88
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Nov 24 23:41:17 2017 +0000

    Remove the /tools/specktre site and just have it 410

commit 5363399027bc0800e962cc2bf649124c4146163d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Nov 24 20:00:08 2017 +0000

    Continue to refine analytics reports

commit da1c0745d13efc427145924a4bdf9f76ca79467a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Nov 22 22:20:47 2017 +0000

    Minor tweaks to reports.py for bugfixing

    [skip ci]

commit 6bfb9c8eeedb5cea70ce844d10402e0e21f1c2a6
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Nov 22 22:20:10 2017 +0000

    Don't require a SECRET_KEY in reports.py

commit 1c4e254da62223ee4dd0c47ea4a9f1672c15c21c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Nov 22 19:10:23 2017 +0000

    Add a proper summary for that post

commit 5b1e12c837696d9fc56e8194b5a685d7fd1d1f24
Author: Travis CI User <travis@example.org>
Date:   Wed Nov 22 11:50:19 2017 +0000

    Publish new post fetching-cloudwatch-logs.md

commit d8b221b72d6b0cd7693cbb51c5febd539c5c4c02
Merge: f6cd1fba ef1a4d7e
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Nov 22 11:46:46 2017 +0000

    Merge pull request #105 from alexwlchan/cloudwatch-logs

    Add my post about CloudWatch logs

commit ef1a4d7e71d1510098abdc1aae74e6d50fa0a669
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Nov 22 11:41:20 2017 +0000

    Add my post about CloudWatch logs

commit f6cd1fba74f681e987c839abc6225ada2246eb47
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Tue Nov 21 11:45:05 2017 +0000

    Ignore the .well-known directory on my Linode

commit 3ac5cf46e82c6e110ea5a66bee37eb4075bfe9a1
Merge: 9ba78ac3 5c44ecac
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Nov 20 23:37:57 2017 +0000

    Merge pull request #104 from alexwlchan/footnote-marker

    Ensure the footnote marker renders as text on iOS

commit 5c44ecac8d14de9734870aa0785310a038a086fa
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Nov 20 23:07:42 2017 +0000

    And fix footnote markers in the RSS feed too

commit a0c068ae808a60d06eb57f1f6d1107f8afe4921e
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Nov 20 23:02:06 2017 +0000

    Fix footnote markers in HTML pages

commit 4515d8a9ca6ade75cfdaac0860f12260bcb03dc4
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Nov 20 23:00:58 2017 +0000

    Add a test that the footnote marker is rendered correctly

commit 9ba78ac3f18267b9126148455f41467f5f8a047e
Merge: ea6dae14 b0b36659
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Nov 20 22:47:33 2017 +0000

    Merge pull request #103 from alexwlchan/fix-rss

    Remove the stray '<' from the RSS feeds

commit b0b366597ce7b391f54f8238a3ddd8dc611b1047
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Nov 20 22:43:28 2017 +0000

    Fix an off-by-one error when rendering the RSS HTML

commit 3fd3dc879a4d83f1998d31a1dbb15a66a0a0029d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Nov 20 22:37:44 2017 +0000

    Add a test that looks for a stray '<' in RSS

commit ea6dae14836d904c7ff6976d6bdb020feeb98325
Merge: d3d5dcee 0e884a82
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Nov 20 15:24:37 2017 +0000

    Merge pull request #102 from alexwlchan/dekatron-at-five

    Add a post for the WITCH reboot birthday

commit 0e884a82dbb2f5262f86b688a32fa9dfd7d21823
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Mon Nov 20 15:18:28 2017 +0000

    Add two date stamps to disambiguate posts

commit 2874062f0e0445183eebccc861538927af47d6d7
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Mon Nov 20 15:12:14 2017 +0000

    Add a missing summary

commit cf49dc55d529062c7fdcf25f9d1eaad5925fce24
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Mon Nov 20 15:07:06 2017 +0000

    Publish new post five-years-of-witch.md

commit d0792355381e195ef2cc98c948cd8d68559cebf0
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Mon Nov 20 15:06:57 2017 +0000

    Markups on the Dekatron post

commit e4f5e4bd4bc6dc29c476024b3234b9b57a8aa3e7
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Nov 20 13:21:26 2017 +0000

    Fix the footnote CSS

commit ccb0dca7b36ffd5e1818d131c446d4bc5f167f1d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Nov 20 13:21:22 2017 +0000

    Add draft of the WITCH post

commit d3d5dcee0b6a4f550cb760185431eeb8fc1ed13a
Author: Travis CI User <travis@example.org>
Date:   Mon Nov 20 00:19:56 2017 +0000

    Publish new post dont-tap-the-mic.md

commit 215f6a29729e31fba540fc7a86afcc4e39cc1448
Merge: 38217263 b158d64d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Nov 20 00:16:32 2017 +0000

    Merge pull request #101 from alexwlchan/tap-the-mic

    Add post "Don't tap the mic"

commit b158d64d7485bd87c0cff5d4ced5dba4b14ea002
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Nov 20 00:09:39 2017 +0000

    Add post "Don't tap the mic"

commit 38217263633bd1bc8e1d13b28fafb2e0d40fdf8b
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Thu Nov 16 12:52:46 2017 +0000

    Update the bijouopera.co.uk site for the new directory

commit cf6f303129983ec7aadbcdaa93e4f2767f68543c
Merge: 67617eb7 44248f16
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Nov 14 16:39:34 2017 +0000

    Merge pull request #100 from alexwlchan/fix-analytics

    Don't use prod analytics on the dev server

commit 44248f1603f234bd8a7c73085ad96d430c89c46b
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Tue Nov 14 16:34:07 2017 +0000

    Fix a local NameError

commit 215d4627b7e07db034aa2f859be8365645ce0bcf
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Tue Nov 14 16:29:01 2017 +0000

    And check it's the right status code as well!

commit ddccfd0833dbc5b656747a30eebcb26c7e0c1f70
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Tue Nov 14 16:28:01 2017 +0000

    Remove all analytics records

commit 097f8c88c1293fc9f7d820432c14c6b5455a4ec2
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Tue Nov 14 15:31:19 2017 +0000

    Don't test for those analytics, either

commit 14e9bd54bf797b5ece1cb30392c780e4d2a98c8f
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Nov 10 12:34:07 2017 +0000

    Don't use prod analytics on the dev server

commit 67617eb70977ccba2388298afafcab9aae4bcf6e
Merge: 5e8ee8d6 2de6b169
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Nov 10 08:12:44 2017 +0000

    Merge pull request #99 from alexwlchan/feedvalidator

    How fast is fast enough?

commit 2de6b1690d1a5a47212fa7508b324e2a3362326b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Nov 10 08:01:25 2017 +0000

    The nodejs gem was only required for octopress-minify-html, which is gone

commit a09d61d951b06895e803a872fbcedd3b611fc0f5
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Nov 10 07:53:10 2017 +0000

    Does this make installing feedvalidator faster?

commit 5e8ee8d6d8bb847a07493635231b3469370f9d7a
Merge: b3b89ac1 881c1079
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Nov 9 21:50:57 2017 +0000

    Merge pull request #98 from alexwlchan/faster-travis

    Take advantage of dead time in the Travis tests

commit 881c10797b345c26ea9f874aefd6f63d41b8d35d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Nov 9 21:38:51 2017 +0000

    Make sure Python is available for pygments

commit ac0431268fae54af1c1a99bf04e8618b0df71e3e
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Nov 9 21:13:21 2017 +0000

    Skip installing specktre in CI

commit d6570bc2c31b797a0235c95e5c3085fdd99be47c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Nov 9 21:06:48 2017 +0000

    Don't build it first

commit 5c6b36840c20bb91df09056f076cb29e1595985c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Nov 9 20:59:40 2017 +0000

    Use the correct make task

commit aa24d2fd5ca8910514c126db5d48850ab0edcf8d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Nov 9 20:55:37 2017 +0000

    Take advantage of dead time in the Travis tests

commit b3b89ac1a7ba15894487f2e18ecf1b21fcbd043f
Merge: e0c0cf68 df3fdff4
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Nov 9 20:24:32 2017 +0000

    Merge pull request #97 from alexwlchan/fix-minify

    Remove the octopress-html-minify plugin

commit df3fdff448993a8623f24ca47a7507cbe120f019
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Nov 9 20:13:01 2017 +0000

    Fix plugins and test to match new minification

commit e8611a768c920dad23488cabc0be7bd260e6f74c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Nov 9 19:55:53 2017 +0000

    Switch to a Liquid-based minifier

commit e0c0cf682a5cbd2e5eec05e4b9d7667eea310e73
Author: Travis CI User <travis@example.org>
Date:   Thu Nov 9 18:18:05 2017 +0000

    Publish new post a-plumbers-guide-to-git.md

commit d5896e073e29088ce0ac9dd556ef90668fabd71c
Merge: fe96a930 d54b0bf5
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Nov 9 18:10:10 2017 +0000

    Merge pull request #94 from alexwlchan/git-plumbing

    Add my resources/exercises for my Git workshop

commit d54b0bf53ffcf627b5125caef0804be862f52219
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Thu Nov 9 17:55:22 2017 +0000

    Add my resources/exercises for my Git workshop

commit fe96a930f8753c644e2ca913ec772883e7f30475
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Thu Nov 9 13:55:32 2017 +0000

    Add some casts

    [skip ci]

commit 7a1fe12e6c82e07e1babc96a3ee07e6f8a73eb9c
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Thu Nov 9 13:53:40 2017 +0000

    Use docopt for parsing instead

commit 692a94e4c63a4b9863e2b41895fdce6d9cdf47c6
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Thu Nov 9 13:30:17 2017 +0000

    Continue to tweak the referrer reporting

commit 7b30a0773e6c312032d3328f56e57426abdadbc1
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Thu Nov 9 11:59:17 2017 +0000

    Include referrer data in the reports

commit 31f27f231ffa747485acb11d20f747dfe5e915bb
Merge: f31fffd6 685a0e18
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Nov 9 11:05:27 2017 +0000

    Merge pull request #93 from alexwlchan/travis-changes

    Improve the Travis setup (marginally)

commit 685a0e188a1b6a13429eb3904b86cf9b37889345
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Thu Nov 9 10:55:50 2017 +0000

    Add the missing 's'

commit 8ad011ed9e17de2bc4deaa6c7798874c0df75ef1
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Thu Nov 9 10:48:40 2017 +0000

    Tweak the make tasks

commit 801fa57b6e0261c55ae00b8f9dd6cd83f7158cd4
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Nov 9 09:47:15 2017 +0000

    Move container building to the install stage

commit 7d6cbfa288ae5e324fc14cf1e1db27e96d6daf2a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Nov 9 09:38:10 2017 +0000

    Go back to a single Travis job

commit 7e570a779c1005a85ea2345f6b4c2e0a2c4b7c64
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Nov 9 09:43:48 2017 +0000

    Travis caching isn't working, delete it

commit f31fffd640dd4423bd1666bc72ca5b0f217b7056
Merge: c90a2f00 7b7b6137
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Nov 9 09:29:08 2017 +0000

    Merge pull request #91 from alexwlchan/analytics

    Add infra pieces and an analytics service

commit 7b7b613798faf068871f6198646ea033b02a9f24
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Nov 9 09:17:03 2017 +0000

    Add a README to the infra directory

commit daaf6c36712be2ef87cc49829efcaa354401e642
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Nov 9 08:06:02 2017 +0000

    Add a README for the analytics code

commit 298eaf6f923acdd627adfed2dbb8653edc6938e7
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Nov 9 07:55:50 2017 +0000

    Call the analytics JS on every page

commit 85f0f53cceee1689759bf3e150ea856e98d91557
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Nov 8 23:21:33 2017 +0000

    Store the database in the right place

commit 1c1180ea4d04b2d67f0691e1e2ece5d2e655a014
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Nov 8 23:19:07 2017 +0000

    Point /analytics at the analytics container

commit bde30abd87267888016c70d95dcf50b9a9bad7a6
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Nov 8 23:16:28 2017 +0000

    Fix the analytics settings

commit 7531accdb5b32d7732cc5536257b720ffd0380ec
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Nov 8 23:15:23 2017 +0000

    Add the analytics image to docker-compose

commit 4c229819dad8a74a513decf64427340cac848688
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Nov 8 23:13:55 2017 +0000

    Add the correct nginx config

commit d0de4eab5218406dac28bfb6570ced6cb2cb4016
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Nov 8 23:08:55 2017 +0000

    Remove a bad line from docker-compose

commit 2020aa2f16bd3db4e609da5162bb650fb40bca60
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Nov 8 23:06:33 2017 +0000

    And copy across the old nginx config

commit 5a76fdd37bb04aa3ecad57ae3dd53f88b05c0618
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Nov 8 23:04:55 2017 +0000

    Copy across the docker-compose file for the alexwlchan.net stack

commit 386797e6a5b22deab904776ce5eb1ef83593fe44
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Nov 8 23:01:47 2017 +0000

    Switch to gevent for the analytics engine

commit 36ba375c53dfe518ddba04ed51144f6419185bf6
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Nov 8 22:53:05 2017 +0000

    Add a Docker image for the analytics package

commit 1a66fd2837de9097a3677a2e5117b72aa116d15f
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Nov 8 22:50:21 2017 +0000

    Get linting to pass on reports.py

commit a1d8a4bca7c66bf4cfde9460e4b566bb810b3447
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Nov 8 22:49:26 2017 +0000

    Get the reporting script to run successfully

commit 7bdfd32a1a94f213fd8e8668a3de45b0db6eeda7
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Nov 8 22:46:18 2017 +0000

    Fix the print() calls in reports.py

commit 98d6cc77338a6d33aa3294a3285a27e41116d907
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Nov 8 22:42:22 2017 +0000

    Check in the original version of coleifer's reports script

commit a0bc4a8a6fe7295f3e109a865814145bd11e37a4
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Nov 8 22:39:23 2017 +0000

    Add the analytics Makefile to the main Makefile

commit 21d2328ded0295b2bda22c63f3816cb3be16a887
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Nov 8 22:39:12 2017 +0000

    Get the analytics script passing flake8

commit 9c79832d89b000556766bb0fb11b571f6bfd0f6a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Nov 8 22:37:22 2017 +0000

    Add a requirements file for the analytics

commit e025c7f7cb25694ef05a191599c263499625276d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Nov 8 22:35:45 2017 +0000

    Check in the original version of coleifer's analytics script

commit 10d7b784baa279034e6840e98cc2c21f19bc3eb9
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Nov 8 22:33:15 2017 +0000

    Fix quoting in YAML headers

commit c90a2f009e2e4346307db1a89e5cde252b305365
Author: Travis CI User <travis@example.org>
Date:   Wed Nov 8 22:27:28 2017 +0000

    Publish new post asking-about-gender.md

commit 4167a8a13003a4c6e766d98c047661fe9c8ecba2
Merge: 695a4282 b53eb036
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Nov 8 22:16:41 2017 +0000

    Merge pull request #90 from alexwlchan/asking-about-gender

    I'm annoyed about bad surveys this evening

commit b53eb0364758777bc8b988301cb27834be892de3
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Nov 8 22:09:27 2017 +0000

    I'm annoyed about bad surveys this evening

commit 695a4282adae03902ac840ee990a85d29cea52dd
Merge: ba52138d 848c7a65
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Nov 7 06:35:45 2017 +0000

    Merge pull request #89 from alexwlchan/ds_store

    Exclude .DS_Store from the 'make deploy' task

commit ba52138d65da07fd480bcb66e032ead38e8e604f
Merge: 921f52b4 48d23d26
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Nov 6 21:42:59 2017 +0000

    Merge pull request #88 from alexwlchan/youtube

    Fix YouTube links in the RSS feed

commit 48d23d268465825d3ec0e129eccc13e49d4321d9
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Nov 6 21:05:26 2017 +0000

    Trim what we get in the RSS feed

commit 848c7a651b9517332820539e19bfbdd8d38c98b8
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Nov 6 20:59:42 2017 +0000

    Exclude .DS_Store from the 'make deploy' task

commit a8565146936684dac81ada6e296db97d824cb6c1
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Nov 6 20:54:46 2017 +0000

    Convert YouTube <iframe> tags in RSS to <a> tags

commit 0503b99fcb4fed6fbd463f68f1e4a474d59eaeb8
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Mon Nov 6 16:51:30 2017 +0000

    Set up the Atom feed filter

commit 81ce91d518e9c634fda08938f262aec6a828ef25
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Mon Nov 6 16:44:17 2017 +0000

    Set up the Jekyll tag for YouTube embeds

commit 921f52b48e199c9081c11c0fc06264e13065c040
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Nov 5 21:27:00 2017 +0000

    Add a link to the conference video

commit e83f4cfb5c66ab2673b3328e65fe9b94088a631e
Merge: 8163af06 38ea7eb4
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Nov 3 16:12:58 2017 +0000

    Merge pull request #84 from alexwlchan/fix-tweet

    Fix the appearance of a tweet in https://alexwlchan.net/2017/04/lessons-from-alterconf/

commit 38ea7eb45e745d00e4760f11eb1dd7bbff799f6d
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Fri Nov 3 16:08:30 2017 +0000

    Fix a spacing error

commit fd3f953c31f8758c9384bc2476f43bbbdbc49738
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Nov 3 16:01:31 2017 +0000

    Remove some commented-out post

commit 917cfd5971157fc77ee80b937d1d0b0e8078b668
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Nov 3 16:01:19 2017 +0000

    Fix whitespace in the tweet plugin

commit 8163af063d6636bf248e7acf6cffe991c2a6d94b
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Fri Nov 3 14:16:29 2017 +0000

    Typo: /s/perserve/persevere

    h/t Clare Macrae: https://twitter.com/ClareMacraeUK/status/926425302208827393

commit 067afa372009dffb80a3c34b97a36b78f7bc224e
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Fri Nov 3 11:52:01 2017 +0000

    Tweak summary

commit a4ebc51341a52b95d3463c4a4ece5eff0adb7f68
Merge: 822e27de 6ce9296e
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Fri Nov 3 11:51:43 2017 +0000

    Merge branch 'master' of github.com:alexwlchan/alexwlchan.net

commit 6ce9296e3a8fe1d4f13ed87ff3ed4b71e67a7f6d
Author: Travis CI User <travis@example.org>
Date:   Fri Nov 3 11:46:53 2017 +0000

    Publish new post pyconuk-2017-privilege-inclusion.md

commit 822e27defd858442c9cdeed618a6bb7dfb086833
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Fri Nov 3 11:40:52 2017 +0000

    Publish new post pyconuk-2017-privilege-inclusion.md

commit 3debd79df90b59c879e30c11eebd97f2fe7530b0
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Fri Nov 3 11:38:12 2017 +0000

    That image doesn't need to be so big

commit 905bc5d802b4ea5c11990799c9c4ca691005596b
Merge: e3b810ed d6cf3dc4
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Nov 3 11:35:15 2017 +0000

    Merge pull request #83 from alexwlchan/privilege

    Add notes from my PyCon presentation on privilege/inclusion

commit d6cf3dc4f00facc324b8468d827150f0cb74102e
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Fri Nov 3 11:30:35 2017 +0000

    Ignore draft posts in tests

commit 373c046f11833c8210e0573cde132f9ea50ac153
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Nov 3 11:12:51 2017 +0000

    Add all the theming

commit 5a4809a39c3397faac0aa74be04cacd8e66c9edd
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Nov 3 11:11:32 2017 +0000

    Markups and attribution

commit dc826fc827eae77b3795eed74e18adbb15ccdd29
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Nov 3 08:00:25 2017 +0000

    Finish most of the privilege/inclusion slides

commit 8998f3c13b22380cb3984e5ac57bf218d188d173
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Thu Nov 2 16:26:38 2017 +0000

    First draft of privilege/inclusion stuff

commit e3b810ed9f3a0c693cead36004d5b25123fc746a
Merge: c565d326 e2bcc872
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Nov 1 23:03:30 2017 +0000

    Merge pull request #82 from alexwlchan/missing-image

    Restore a missing image

commit e2bcc872adc1ef62267c6240f7b125946bd7a1b8
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Nov 1 22:35:57 2017 +0000

    Add the image from the old site build

commit da56b37b7ad8e2cca557ea1c0ba5ac16adf509b1
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Nov 1 22:35:37 2017 +0000

    Revert "Remove media from a dead tweet (I can't recache it, alas)"

    This reverts commit 977022e1235fd10c318345547c6bc426f6a28527.

commit c565d3263190cfdbe3a7f39f423a928fe4d644f6
Merge: 0c4c5859 6e00966c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Nov 1 14:00:37 2017 +0000

    Merge pull request #81 from alexwlchan/lightning

    Add an update to the lightning talk wording

commit 6e00966ca6c9777044916cc6d102a4faf78c74b9
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Nov 1 13:50:23 2017 +0000

    Add a missing space

commit 0990e5bb49b075731dd342a286e71c962b465300
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Nov 1 12:51:39 2017 +0000

    Beef up the testing of embedded tweets

commit 74401c6bd56d154059fc2b7bc08d8da4a3bdb66a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Nov 1 11:19:56 2017 +0000

    Only record each broken link once

commit 638ef34cfaed3553c1ea0181ce0f2066388d3895
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Nov 1 11:15:33 2017 +0000

    Remove media from a dead tweet (I can't recache it, alas)

commit 466f7942639cd8a5bcec10dc576aee66023a5d48
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Nov 1 11:03:42 2017 +0000

    Clarify when we changed the wording

commit dbbbd9941b4068baafb3fd965bd01165aa1fbb4a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Nov 1 11:02:51 2017 +0000

    Push the local/display path logic into functions

commit 91bc0596ed079e94897c3829bfabe1c6a1f9234e
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Nov 1 10:58:19 2017 +0000

    Inline an unneeded variable

commit ecd18fd0119a21dcf5a881e65628c38b8db6aba7
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Tue Oct 31 23:24:41 2017 +0000

    Tweak the wording about the tweaked wording

commit df440da3c73a551e5f5bf666bd4a52d10c7f9015
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Tue Oct 31 23:22:08 2017 +0000

    Add a background-color to updates

commit ab9a097e1fd79b736528c4c2c8e27d477fd855bf
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Tue Oct 31 23:15:41 2017 +0000

    Add a last modified time

commit 5375277f0312c1b75af0b92de0c8286650c4e5bc
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Tue Oct 31 23:15:31 2017 +0000

    Don't deploy into a subdirectory

commit 1abc1295a1df76f96847b40526b6a146cf353ab4
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Tue Oct 31 23:08:44 2017 +0000

    Sort out local deployments

commit 03c7ed009c1b352fdaa34c35867c1138c0c8e4dd
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Tue Oct 31 23:04:58 2017 +0000

    Render hashtags in tweets correctly

commit 663b71aa63c77b12d8005306e88658dd7679f450
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Tue Oct 31 23:02:31 2017 +0000

    Embed the tweet image correctly

commit e0870a63da7f8780ac76a7fdbe15cc774ee6a8ef
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Tue Oct 31 23:02:14 2017 +0000

    Download the media first, not the cache

commit db6fa8003083615964dca901ca5cbf7ca0aa8b67
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Tue Oct 31 21:32:00 2017 +0000

    Tweak the Twitter plugin to download media images

commit 2d038f2e949dcb4562ad660780d406292b3d9e10
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Tue Oct 31 21:26:15 2017 +0000

    Add a note about the tweaked lightning talk wording

commit 0c4c5859594f884555a84b5a3507bd9ec977f1d0
Merge: 3426994b c92e855c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Oct 31 15:09:52 2017 +0000

    Merge pull request #80 from alexwlchan/travis-pr-builds

    Try conditional build stages

commit c92e855cc36d6fb9ef941765e9f19ef62617b1db
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Oct 31 15:06:22 2017 +0000

    Try conditional build stages

commit 3426994bf1ef24a11785a07172499b31f8c6dc9a
Merge: 819f0aba 7607ff15
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Oct 30 15:11:46 2017 +0000

    Merge 08a51dd57ad0256f2ccd176e477119ce6c16aa10 into c9f06a0673fde027b61ce1bffc83ebc7615d514f

commit 7607ff155f5cc62d5348218f8446102c9cbfb7c8
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Oct 30 15:11:27 2017 +0000

    Remove a reference for a broken link

commit 89e7f9a9815c526127dc0c0654caa313276f5681
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Oct 30 13:22:06 2017 +0000

    Test that descriptions aren't too long

commit ec73ba6c342ab91544b69f87ee28474ffb72b0cf
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Oct 30 11:57:51 2017 +0000

    Add test that every new post has a summary

commit 636964f00db6d308b5cdc592e23ac024cc1d6b5c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Oct 30 11:39:45 2017 +0000

    Add mechanism for testing the front matter

commit 819f0aba99738ef2f98dc7b5ac89e00a4314a715
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Oct 29 23:59:41 2017 +0000

    Switch to Travis build stages

commit cb9ce1bfa55d957c7995b3439a284f09fce430d8
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Oct 29 23:56:08 2017 +0000

    And another go at the SSH key

commit f4a8ba5492e73b8f0467f3d594983aa322fbcc85
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Oct 29 23:49:55 2017 +0000

    Get the RSA key in the right place

commit 735397baccc8a23f0c47794794e9da48764a5d28
Merge: 8cf8c379 4f4e08d8
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Oct 29 23:45:04 2017 +0000

    Merge pull request #77 from alexwlchan/rsync-docker

    Run rsync inside Docker

commit 4f4e08d8f78e09b60e18e50ba54fe639162f94b2
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Oct 29 23:40:45 2017 +0000

    Run rsync inside Docker

commit 8cf8c3799d032a287d7c344b39842250336d030d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Oct 29 23:27:21 2017 +0000

    Don't run 'git stash' in the deploy step

commit 8d7b2d1a9034ddbf88aa788914df5100cc68d176
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Oct 29 23:23:31 2017 +0000

    Tweak the README link

commit 55aa37c6af820b989961f295332fe5e4d82f4e24
Merge: d48fc332 2ddf6c9f
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Oct 29 23:22:41 2017 +0000

    Merge pull request #76 from alexwlchan/deploy-stages

    Move the deployment into a separate build stage

commit 2ddf6c9f18101cf08d6c0c6965bc769549064d0c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Oct 29 23:18:57 2017 +0000

    Move the deployment into a separate build stage

commit d48fc3326cf8dacb4d0c5241245127b749d41f35
Merge: b10d273d f85ac0ff
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Oct 29 22:58:21 2017 +0000

    Merge pull request #75 from alexwlchan/pyconuk-2017

    Initial content from PyCon UK 2017

commit f85ac0ff90cc4a361f572e2c20e38e5e8050af97
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Sat Oct 28 11:23:53 2017 +0100

    Add a summary to the lightning talk post

commit 68eb8474c18b44a4929917feb989d043fa8eb8ad
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Sat Oct 28 10:20:29 2017 +0000

    Publish new post lightning-talks.md

commit 055b4329fca961548631764a310db2ecff97fdc5
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Sat Oct 28 11:20:22 2017 +0100

    Add draft post about lightning talks

commit b51f917810f419e1b7f5ca499b63581d634c6fb1
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Sat Oct 28 10:49:31 2017 +0100

    Add some links

commit dd063dfa08d4927636ed2eeed1bd4dae8de5db70
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Fri Oct 27 08:25:34 2017 +0000

    Publish new post pyconuk-2017-resources.md

commit 5d6c7fafa2962eef46ed6e1f737742ae4646b109
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Fri Oct 27 09:16:55 2017 +0100

    Tweak the summary level of the LaTeX underlines

commit 1e2f88af7fc15a1fad7bba6598dfa47fc4f77cda
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Fri Oct 27 09:16:43 2017 +0100

    Add initial signpost for PyCon UK 2017 resources

commit b10d273d884a0816fa16a191564f42138d9c025b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Oct 25 18:07:32 2017 +0100

    Add a large image to the Twitter preview

commit c9979b2a6e71596b74d34da6d290ebf2aaf9a985
Author: Travis CI User <travis@example.org>
Date:   Wed Oct 25 13:14:54 2017 +0000

    Publish new post tweets-in-keynote.md

commit 1c609f0a9cf51ec34981cccd92aa803dd7d88cf3
Merge: 2831aa6b f599bf60
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Oct 25 14:12:13 2017 +0100

    Merge pull request #74 from alexwlchan/tweets-in-keynote

    Add a post about showing tweets in Keynote

commit f599bf604a058c20a8a875b8a4f5e03d61ea6383
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Oct 25 13:54:17 2017 +0100

    Add a post about showing tweets in Keynote

commit 2831aa6b467bf90242dfd2b09e8f06a07a6cdc0c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Oct 20 20:34:40 2017 +0100

    Add a LICENSE

commit 66b829bb8b95b25afb83eb2f75dda53bfb138540
Author: Travis CI User <travis@example.org>
Date:   Fri Oct 20 17:11:59 2017 +0000

    Publish new post requests-hooks.md

commit 6eb6ad8cdbb4e039f4212bb9b22e0c5224a544e9
Merge: 180d10e3 d038010e
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Oct 20 18:08:08 2017 +0100

    Merge pull request #73 from alexwlchan/requests-hooks

    Add a post about event hooks in python-requests

commit d038010e403e9eb3619a1d4068006a81d089acf3
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Oct 20 17:59:12 2017 +0100

    Add a one-line summary

commit d86489d67ceef2e27c80cf671a3c097189e32eae
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Oct 20 17:57:21 2017 +0100

    Small markups on the requests hook post

commit 1464c348bbb7ee3c2095943ac45eca4a257c3e2a
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Fri Oct 20 17:34:33 2017 +0100

    Write a draft post about hooks in python-requests

commit 180d10e3086363a2008d13e93f592ed81c9ea1a8
Merge: 1f0c0277 5c6d17de
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Oct 20 16:46:32 2017 +0100

    Merge pull request #72 from alexwlchan/control-centre-images

    Ensure Control Centre images display correctly on mobile

commit 5c6d17de3fbdfb8b88b12bc7acb0c0333c98d5c9
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Fri Oct 20 16:43:04 2017 +0100

    Ensure Control Centre images display correctly on mobile

commit 1f0c0277194a92fdb3972f8be6cdfcae91e23fcf
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Oct 19 22:26:16 2017 +0100

    [skip ci] Be neater about Docker images

commit fda41ecaaab420b03f69ef2af5faca29dca129c6
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Thu Oct 19 17:48:58 2017 +0100

    Install Pillow from the Alpine package (#6)

commit e9f79b998eeee5db20a52bef60643febd4ff43f2
Merge: edfb139a 09173cca
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Oct 19 17:42:00 2017 +0100

    Merge pull request #69 from alexwlchan/accessible-css

    Tweak CSS for accessibility

commit edfb139a034eccefaa92cf8f797fc7e99885a70f
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Oct 18 08:11:58 2017 +0100

    Expunge a few remaining references to .tox

commit cbb7cf76833a1eb0bf0324beaa2ccacf0c9c6149
Merge: c6cf4f20 feaf4fe0
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Oct 18 08:08:56 2017 +0100

    Merge pull request #68 from alexwlchan/unused-image-tests

    Add tests that every image in `src` is linked from somewhere

commit feaf4fe01d89ed1268c4990154d8d0c0a3a7f10c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Oct 18 08:05:38 2017 +0100

    Put the slash in the right place

commit da235d2267ac92687e4ec709cfb180f26bed7cf2
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Oct 18 07:59:12 2017 +0100

    And delete two more now-unused images

commit 19c783bdf290112cfa2dece93674476c758ecd0f
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Oct 18 07:59:01 2017 +0100

    Try to pick up more pages which are otherwise unlinked

commit 867d5cf9fd6d21d36934684e81341f3abfc96604
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Oct 18 07:58:27 2017 +0100

    Make src the root of the fixture

commit 8a38284597645bfb6f9d8c8859ba29eeb636d0c6
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Oct 18 07:58:14 2017 +0100

    Throw in another sorted()

commit b89802f5287316c5b0d25966486c543876ceb791
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Oct 18 07:52:43 2017 +0100

    Two images I didn't use in my Crossness post

commit 3b8e87b455a670cc8847fda04bbe0d55a4eb3f7b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Oct 18 07:51:55 2017 +0100

    Delete three images from an unwritten post

commit b8d596096173f5d80fc15c5bbcd8cf29cfb34986
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Oct 18 07:51:35 2017 +0100

    Throw in sorted() for easier error reading

commit 285343a18028830d6d7d9413a5a533c5f6961e0a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Oct 18 07:49:50 2017 +0100

    Add a test that every image is linked somewhere

commit c6cf4f20d477e7000fa560a55bf6cc0a7b73ec93
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Oct 18 07:38:45 2017 +0100

    Actually install feedvalidator correctly

commit 2d698a687ac79fe9866d374613e9a47fb546629b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Oct 18 07:38:13 2017 +0100

    Fix the NameError

commit dabc8d823798e0181c4055559800eaf74d837fbb
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Oct 18 07:34:16 2017 +0100

    Always run the feedvalidator tests

commit 334cf24c9e6df2815a3807138c264630e474cb29
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Oct 18 07:33:41 2017 +0100

    Move the responses to a cacheable fixture

commit f3e301c0688abc9e6fccbd015a79bb8c0ee7c097
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Oct 18 07:32:12 2017 +0100

    Rename files for better consistency

commit b08758dc3911ebec31e09d15bf87e7d53d121398
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Oct 18 07:31:01 2017 +0100

    Share the whole repo with the test container

commit 83fc36bd7bc86e68a90f0174708d54b6360ad6e2
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Oct 17 23:15:08 2017 +0100

    Add a summary to that LaTeX post

commit 2975a51458bdb714d9316dca0f36065d3548c85d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Oct 17 23:05:54 2017 +0100

    Point to the right image

commit ac68c012502513efb4f6b707548a5cb412604af9
Merge: e3de62d6 03904b70
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Oct 17 22:07:03 2017 +0100

    Merge pull request #65 from alexwlchan/toxless

    Simplify the testing process by dropping tox

commit 03904b70916f5c5db35d47666caef6e488e7ab13
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Oct 17 22:00:49 2017 +0100

    Add a note about my pip-tools frustration

commit bf7beff6a38129cdae5892cb9d39ea7f538e24cf
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Oct 17 21:59:27 2017 +0100

    Remove the unused tox.ini

commit f3a60ab48c04d56fce210da59b3134440488f87b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Oct 17 21:59:18 2017 +0100

    Tweak the tests to pass in Python 2.7

commit 82034beb0013617bb35188ef2e19881917755775
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Oct 17 21:57:32 2017 +0100

    Remove the dependency on tox.ini

commit b1b92cc4b7c395c2c9eeab2ed5e05f6459fb7205
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Oct 17 21:56:20 2017 +0100

    Switch tests to run without tox

commit e3de62d6331ae59bcdd606abbd2b8da07b433910
Author: Travis CI User <travis@example.org>
Date:   Tue Oct 17 20:54:13 2017 +0000

    Publish new post control-centre.md

commit c57dcefc56467f9f6fc36e0e06e5b93207f59156
Merge: 31a81c98 19849c58
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Oct 17 21:50:59 2017 +0100

    Merge pull request #64 from alexwlchan/control-centre

    Write a post about Control Centre frustrations

commit ef888ccebd332610814b9e58b338b5d1e7494b3f
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Oct 17 21:50:42 2017 +0100

    Do away with the distinct requirements.txt files

commit 19849c5831d0237a15f795a4c9fbd8fb862068db
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Oct 17 21:44:52 2017 +0100

    A few grammar markups

commit 8d27c872095e61d536d83183aaab0e3085abd6bb
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Oct 17 21:34:53 2017 +0100

    Finish the control centre draft post

commit f56e6e99f99dd23f359bd73125986e5ca95324ac
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Oct 17 21:15:05 2017 +0100

    Start writing my post about Control Centre

commit 31a81c982ac8d6939c1da95624002fc2633366ad
Merge: b469de54 5d0fc0ed
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Oct 11 23:33:42 2017 +0100

    Merge pull request #62 from alexwlchan/ci-serve

    Don't include <style> tags in the RSS feed, ensure PR builds pick up issues in draft posts

commit 5d0fc0edeb74b8822e33b003f6e2a94ee6c2c9b9
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Oct 11 23:29:34 2017 +0100

    Chuck out <style> tags in RSS too

commit 023850e37e5e68127a77c18d0fb6136c72d4bf84
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Oct 11 23:26:34 2017 +0100

    Reduce repetition in the serve-debug task

commit 07bd2e0243cb58cd2762955c71a8788f3a2af331
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Oct 11 23:26:01 2017 +0100

    Running 'make serve' picks up drafts

commit 552ae92bb32fe3bc7cfc88c1e9fcaee1accf848c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Oct 11 23:23:29 2017 +0100

    Add a 'make stop' target

commit b469de54796909b6c0dd1171b58794bbdb3255c7
Author: Travis CI User <travis@example.org>
Date:   Wed Oct 11 22:09:25 2017 +0000

    Publish new post latex-underlines.md

commit 012d65b10a8c2ef6c1c9a69ff4e428a927e06a05
Merge: 03984b62 5c9e1b42
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Oct 11 23:07:23 2017 +0100

    Merge pull request #60 from alexwlchan/latex-underlines

    Add post about underlining in LaTeX

commit 5c9e1b42d07bdf5b65cbd0658dbfdf21a9d1e8f4
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Oct 11 23:02:42 2017 +0100

    Improve the quality of the rendered images

commit 438ada03030dc3fb983c6712081d616412d6d98a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Oct 11 22:59:42 2017 +0100

    Those % are important!

commit e7bc1449a526d062de548f9aa7ba5a767554e06c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Oct 11 22:48:36 2017 +0100

    Add a link to the example code

commit e2a298ba94c25d423e4a63487e971a57df493b8e
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Oct 11 22:44:00 2017 +0100

    Add post about underlines in LaTeX

commit f9cfcde35cddc139ac2fd386ef09a8306b2e1be5
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Oct 11 22:28:08 2017 +0100

    Debug mode runs with drafts enabled

commit 2a0ca77c9f044833c1ef2d79807dec4f9d76f0ce
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Oct 11 22:28:00 2017 +0100

    Tweak the available examples

commit 03984b626eb57c821101223cbb014bcae81f096d
Merge: 64deacf9 46b93ab3
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Oct 11 20:36:25 2017 +0100

    Merge pull request #59 from alexwlchan/license

    Add license information to the repo

commit 46b93ab32a0d906a0f201c16985316a8c04587de
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Oct 11 20:32:36 2017 +0100

    Add a link to GitHub in the footer

commit c1f716eb4e891ed836be71aeca323afa4c5a37aa
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Oct 11 20:29:18 2017 +0100

    Explain the license choice in the README

commit bd3f7efdd6767705fbfac74c7f0abfa331271e69
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Oct 11 20:29:08 2017 +0100

    Add license information to the website footer

commit 3e4ade286f4a680d546586fb8c248aa27a6263e2
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Oct 11 19:10:26 2017 +0100

    Add the last example and the build script

commit a9ab7edf97f4ea79d3c0b29261d3de93218c3dd0
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Oct 11 18:40:24 2017 +0100

    Add the LaTeX examples

commit 64deacf98ed5355e9c716bf0a010f0d6f9a6a856
Author: Travis CI User <travis@example.org>
Date:   Mon Oct 9 08:11:03 2017 +0000

    Publish new post pip-tools.md

commit bc856ff031b2a36ccd7264f7b587677b17a09427
Merge: 38afca02 1b36b269
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Oct 9 10:08:33 2017 +0200

    Merge pull request #58 from alexwlchan/pip-tools

    Write about my use of pip-tools, and actually use it for the site!

commit 1b36b26965c8b7fab24c8f1ceef51bf2216f913e
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Oct 9 10:03:49 2017 +0200

    Crossing the streams

commit a70ce6e9e4c2f2c92908df8065087973b8b8b720
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Oct 9 09:59:53 2017 +0200

    Add the missing link to Docker Hub

commit faa11d8eda261ee03b4f229e388d938d76e0a809
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Oct 9 09:58:42 2017 +0200

    Use the Make task in the site itself!

commit 987ec32235600088c4bdb80f1842d26bb3fde769
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Oct 9 09:57:15 2017 +0200

    Add initial post about pip-tools

commit 09173cca9d6e54922d4d90c709441b0b39254688
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Oct 8 22:01:13 2017 +0200

    Add underlines to permalinks

commit bbce6265afbf3c392eac48d6d3dfd5604ed9ad77
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Oct 8 21:56:27 2017 +0200

    Tweak header appearance when printed

commit 38afca020d804d37ab443b2f3e747dae49faf496
Merge: 2e5049b3 b757c97f
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Oct 8 21:19:48 2017 +0200

    Merge pull request #57 from alexwlchan/minipost

    Move minipost: into the theme block

commit 2e5049b34b12cbf6a3d4c985df3e3ee1f79d77d8
Author: Travis CI User <travis@example.org>
Date:   Sun Oct 8 19:08:16 2017 +0000

    Publish new post pronunciation-peeves.md

commit 63aa970302f5682c1549d851122db5ae051ca26d
Merge: 04b28b20 89a916a5
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Oct 8 21:05:49 2017 +0200

    Merge pull request #55 from alexwlchan/pronunciation

    Add draft post about pronunciation

commit 04b28b20668a6cd98641b5cbedfc914e09fe9bc7
Merge: 93a93162 e3787abe
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Oct 8 21:05:43 2017 +0200

    Merge pull request #54 from alexwlchan/travis-python

    Remove an unused line from the Travis config

commit b757c97f2cc63eaeac60c773948744a0e6271f82
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Oct 8 21:04:30 2017 +0200

    Move minipost: into the theme block

commit e3787abe630f979afadad1615174b2f1d3650e74
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Oct 8 21:00:00 2017 +0200

    Remove an unused line from the Travis config

commit 89a916a511dbad890868fffec292a224a4948f88
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Oct 8 20:59:28 2017 +0200

    Add draft post about pronunciation

commit 93a93162969fa0fb95d9599ab2c514d839936544
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Oct 8 09:06:02 2017 +0200

    More micro-trimming on the Docker image

commit 8d66cbbbde97e6f980fd3d122981ae11e6c2c30b
Merge: e8b60322 e9842895
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Oct 7 21:32:55 2017 +0200

    Merge pull request #53 from alexwlchan/certbot

    Add a Make task for renewing my certbot certificates

commit e9842895987b5b38a800165d51ffe5f63dd5787c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Oct 7 21:30:44 2017 +0200

    Add a Make task for renewing my certbot certificates

commit e8b60322b463683aa4205e6f69e2b85685813a8a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Oct 7 19:40:41 2017 +0200

    Unpublish the example post

commit 41c72504c6d4b64dea10f1a1a7286301e52695d9
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Oct 7 19:40:25 2017 +0200

    Two more Git tweaks

commit b630095fca79c7f6e1ac6941d58ba7a195ea72f6
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Oct 7 19:38:28 2017 +0200

    Tweak the Git commit message

commit a123e75f1c66706a8df1a9e8e3584835c4e1fa6c
Author: Travis CI User <travis@example.org>
Date:   Sat Oct 7 17:37:03 2017 +0000

    [auto] Publish draft entry /repo/src/_drafts/hello-world.md

commit 9a44ab83996ff8f52db7cac8fe3be801d959b943
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Oct 7 19:34:28 2017 +0200

    And another path fix

commit b5763127170829b1b81716406eab309c70b2a3f0
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Oct 7 19:30:11 2017 +0200

    And another path fix

commit 39a9da0077afb0c74beb33d6c1ad0752dde0c4d3
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Oct 7 19:22:35 2017 +0200

    Don't restart Docker before caching

commit 0d66e6bd6c883982571938e62fd48548dc2cb4c9
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Oct 7 19:19:03 2017 +0200

    Fix the file path

commit 2fd0b30819cdd3414623bf3da1a33290f923eac0
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Oct 7 18:58:55 2017 +0200

    Make Git available inside the container

commit 814880059d0e23adf0245e8e2c1921e06153534b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Oct 7 18:58:14 2017 +0200

    You need that argument

commit edff47ec042a4710dce926d1df6af463b66cff8a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Oct 7 18:47:34 2017 +0200

    Point publish-drafts at the right directory

commit caff517a720d7600cc6de5a4cebdc70a86ad78ba
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Oct 7 18:46:19 2017 +0200

    Revert "Don't care about source_dir now"

    2abf3a9a2a9ae570638b36a5999d944e2e3472d8

commit a49b9a764c2c81373adee3a437d9c07bf88535fe
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Oct 7 18:29:12 2017 +0200

    Trigger deployment from run.sh so we get a failed build

commit 944f2bb3c65f45c03776a4149a942d0724703004
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Oct 7 18:26:55 2017 +0200

    Don't cleanup before deploy

commit 02ccbbf58685d5e706272e927f845343a480c564
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Oct 7 18:15:39 2017 +0200

    Don't care about source_dir now

commit d49725705ebf7c363915baebafa49a5fee18369e
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Oct 7 18:12:04 2017 +0200

    Install the command for the right version of Jekyll

commit 75cc8358d07dd14f8365329440da8376cb820d92
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Oct 7 18:11:07 2017 +0200

    I only want to cache images, not containers

commit 6253a44a00c6c89b826c8e59f963d85b463d52fa
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Oct 7 18:07:15 2017 +0200

    Make sure Docker is running for the deploy step

commit ff5e82c8e8c7a4961fd97ebc2e99c38b2fad5381
Merge: 88e1fd20 13fec217
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Oct 7 17:55:43 2017 +0200

    Merge pull request #51 from alexwlchan/publish-drafts-redux

    Automatically publish all drafts that are pushed to Travis, redux

commit 13fec217f89b0c8af24803212c33807ff380f07d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Oct 7 17:38:29 2017 +0200

    Delete the _drafts directory when we're done

commit 6bce35927ac31d807b62441cd8ad508ce3ddc057
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Oct 7 17:37:48 2017 +0200

    Add a draft post for testing

commit 92f8abbcff68800a31a609ce9cbfe9cf40a47f43
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Oct 7 17:37:21 2017 +0200

    Set up the Travis deploy step

commit 1ef3f62914ce795cd26899b81986a4a85348410d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Oct 7 17:34:16 2017 +0200

    Add a new RSA key for Travis

commit 7fe9892d2911ff4dc2ae83ab2d798099a14fb1eb
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Oct 7 17:33:17 2017 +0200

    Pillow is installed as a specktre dependency

commit f3ea31e2f385363e18f0e2a8ca358aab8468fd69
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Oct 7 17:33:00 2017 +0200

    Trim the size of the Docker image

commit c0108d59d5fe636a0f786871250e14ffbbb4f8e9
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Oct 7 17:32:26 2017 +0200

    Add a Make task for publishing drafts

commit 706c380239067a7ae7f50a315e4e050b4dfe0626
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Oct 7 17:31:18 2017 +0200

    Make _plugins available to Docker

commit 5855e5f75665bec502323647e3f1d664db3d52d8
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Oct 7 17:29:54 2017 +0200

    Add the shell-executer dependency

commit 822967df247849335985653b09d74a12c5b747a4
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Oct 7 17:29:06 2017 +0200

    Install the plugin inside the Docker image

commit ccd4f0cf6183a8f57622eb8110273a8691de5bd2
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Oct 7 17:28:08 2017 +0200

    Add the publish_drafts plugin

commit 88e1fd2072e1da8188d696c17ab5506b8fe0d5c4
Merge: e9606f31 6e199b26
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Oct 5 21:10:48 2017 +0200

    Merge pull request #48 from alexwlchan/feed-link-posts

    Link to post targets in the Atom feed, not the post on my site

commit e9606f31b7d2ae6f5128812b5d09484900cb3dfa
Merge: 4e48c4be adde8fb3
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Oct 5 21:10:36 2017 +0200

    Merge pull request #49 from alexwlchan/more-make-fixes

    Note another two Make dependencies, remove an old command

commit adde8fb39270c4f3464d2c2ab7061c54fe742b1f
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Oct 5 20:02:22 2017 +0100

    Note another two Make dependencies, remove an old command

commit 6e199b26fb4037a7b19399d5367f03b6f9595407
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Oct 5 20:01:56 2017 +0100

    Link to post targets in the Atom feed, not the post on my site

commit 4e48c4be0d0011cafb4de636b9d3b224b9e69966
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Oct 5 18:46:03 2017 +0100

    Remove an unused Dockerfile

commit 3e66f9c5087f530f2ac69d8b63ffaa8124cee74f
Merge: d6c28d4c 5ef8e2d3
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Oct 4 23:37:46 2017 +0200

    Merge pull request #46 from alexwlchan/better-make

    Make better use of make's dependency resolution

commit 5ef8e2d32cb5543d915119b2761e8c0e48d61437
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Oct 4 22:29:02 2017 +0100

    Use a pinned Ruby image everywhere

commit 7439fc4b6874476f3a5537d4acceca5161d2504c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Oct 4 21:55:28 2017 +0100

    Switch to a pinned version of Ruby

commit d553fa0d2bf8d0c070db7139357ea9349aba9a52
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Oct 4 21:54:41 2017 +0100

    Take proper advantage of Make's dependency resolution

commit d6c28d4ce15abaf9b9fe7d71b37963a6f2cba06e
Merge: 5002a96f 8cc56055
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Oct 4 07:39:34 2017 +0200

    Merge pull request #45 from alexwlchan/gemfile-update

    Add a Make task to update the Gemfile.lock

commit 5002a96fa2dff8b67386c2bd0ddb008907bb60bf
Merge: db80c840 2b143c3a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Oct 3 23:58:32 2017 +0200

    Merge pull request #43 from alexwlchan/overengineering

    Add my overengineering link post

commit 8cc560551155629e8da7076f4b5955ffec1ed4c7
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Oct 3 22:57:37 2017 +0100

    Add a Make task for rebuilding the Gemfile.lock

commit e63cee79ba1f526339ee35fc942dbab6ee8f70d3
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Oct 3 22:57:02 2017 +0100

    Fix entrypoint to bundler

commit f40615a848c8e27f482143cab5b940d092458705
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Oct 3 22:53:33 2017 +0100

    Install Ruby/bundler in a separate Docker image

commit ff0b4d6604556ecaeb98750382220947d8cb8410
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Oct 3 22:50:24 2017 +0100

    Remove a comment in the Gemfile

commit 2b143c3ab88226c3703c3fdbc4bcc115849ce0e5
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Oct 3 22:24:36 2017 +0100

    Add my overengineering link post

commit db80c840e0a03ee4f88f35e9d97c04ac0ab25f35
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Sep 25 18:56:07 2017 +0100

    Add a Travis link to the README

commit e7bd74287b3aae8e83dd68fca1b20337b0cff291
Merge: c7e2074a 19aaa983
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Sep 25 18:50:25 2017 +0100

    Merge pull request #41 from alexwlchan/travis-docker-caching

    Add scripts for caching in Travis

commit 19aaa983657e3e3e9d7d923280970bdcdcafac1a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Sep 25 18:47:13 2017 +0100

    Add a bit of attribution

commit c7e2074a7b71435b784a7fadc4013610ec48239e
Merge: dffca990 6ae35557
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Sep 25 18:46:00 2017 +0100

    Merge pull request #40 from asettle/patch-1

    Just helping ...

commit dc4e886628a1ff5314f9994c2bca8c8a37e825d7
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Sep 25 16:41:56 2017 +0100

    Indentation sucks

commit 78d204eae6616991477b348e4816685fe306a0b5
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Sep 25 16:40:32 2017 +0100

    Add scripts for caching in Travis

commit 6ae355571e0af66f347ffc52a01782678d144d19
Author: Alexandra Settle <alexandra.settle@rackspace.com>
Date:   Mon Sep 25 14:59:54 2017 +0100

    Just helping ...

    Fixing a typo. Of the word typo.

commit dffca990892d817243b39e3e88187a587d97c5a2
Merge: 3989eb49 c2cdcf80
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Sep 23 23:06:21 2017 +0100

    Merge pull request #37 from alexwlchan/link-checking

    Add a test for broken internal links

commit c2cdcf80a7823c4ddf7b5dbe3cb7ff2d81474f3e
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Sep 23 23:00:06 2017 +0100

    Apparently the link checking ignores HTML comments

commit 9990a67dffcebcb55a3c4ce945fcd86ce22dcff7
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Sep 23 22:53:03 2017 +0100

    Temporarily remove the other broken links

commit 48de6aafe843f74e1c1ff75c117d3fab0a9fe9bd
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Sep 23 22:44:06 2017 +0100

    Correct a few more broken links

commit 8c106d381a114a26cfcae03a9090428d9b690fa1
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Sep 23 18:15:30 2017 +0100

    Use a tty to get coloured output (hopefully)

commit ee2d1f25bded4ecc0c92494b56cb682f4f85eac2
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Sep 23 18:14:02 2017 +0100

    Fix a couple of the broken links

commit 0619adb7cbc7cf99b11179348e47ed64dffe65a7
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Sep 23 17:17:57 2017 +0100

    Actually, caching the .tox directory *is* sensible

commit 3422674e6081c99b322561c6e6e3f9c73b1c716d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Sep 23 17:08:59 2017 +0100

    Split the dependency files so atomvalidation doesn't get lxml

commit d2bfd8ab0fcd366072456f500fc1823602909171
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Sep 23 17:03:02 2017 +0100

    Include the correct fixture

commit bba528f4da90b151099b1ca554d0974b7cc3ed31
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Sep 23 16:55:38 2017 +0100

    Get the lxml dependencies right

commit d60b2be0670c3441f11c99a463363de8d20cc1c8
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Sep 23 16:48:38 2017 +0100

    Use the pytest fixture for the URL

commit 53a84a165b7308974e78969ce2e41dc91a450a95
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Sep 23 16:48:12 2017 +0100

    Add missing libxml2-dev dependency

commit dc3de7412d0ba80df5fa9d93ae5328846ce1e43a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Sep 23 16:31:13 2017 +0100

    Add a test for broken internal links

commit 3989eb492418b071c6684da829e496f63da5a16b
Merge: c22ffffe fab8c93f
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Sep 23 11:23:47 2017 +0100

    Merge pull request #36 from alexwlchan/tests-in-docker

    Run tests inside Docker as well

commit fab8c93f5a052dbbf98e0192d3c376827e11f7f8
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Sep 23 11:19:13 2017 +0100

    Search for the correct container

commit c22ffffe95ca35016e0a7567982d7f4f64deced6
Merge: bff35708 219a6cb0
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Sep 23 11:13:36 2017 +0100

    Merge pull request #34 from alexwlchan/docs

    Add some proper docs in the README

commit b47dc524a8c3f3a4cd86c4b66d5c3864eb68e2b1
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Sep 23 11:10:24 2017 +0100

    We don't need the Travis Python image, either

commit 550babda8ea4f0edf20bbd3f5ede7211ff3556db
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Sep 23 11:10:06 2017 +0100

    Remove the tox code from the Travis config

commit 6fc1cc12d848406a6a847ffa9061bc62ada8c152
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Sep 23 11:07:02 2017 +0100

    Pass through the hostname directly

commit ab6d55be6bc45b9aa582f8c07d3ca5cbe1754563
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Sep 23 10:17:20 2017 +0100

    Get the tests running inside Docker

commit 0ec16fbda9318e3c31102dcc35e6d0b499444b05
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Sep 23 10:17:01 2017 +0100

    Cleaner output from 'make serve'

commit 9494b1138e0eb3fd9bc2b04591628538005c2106
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Sep 23 10:04:32 2017 +0100

    Add a Dockerfile for running the tests

commit 36ec64d0801ec7a3a28ef8024cb9d1d411887ef6
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Sep 23 10:01:15 2017 +0100

    Make the server container name a variable

commit 219a6cb0c2bf5341f769238087d2f9620a72c3e8
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Sep 23 09:56:38 2017 +0100

    Contributing note

commit 6a795e6166b6133b94a2c42b33c73c56d5ba2997
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Sep 23 09:53:27 2017 +0100

    Note builds inside Docker

commit 2e091c46b30e6d265506009de6018541d88c3f6c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Sep 23 09:36:59 2017 +0100

    Document theming, archives, and tweet embeds

commit 068d4fdb165749f418621f478789bf9853f4bd0c
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Fri Sep 22 17:49:19 2017 +0100

    Add a note about static file copying

commit e7bacdb8c37f00d5c7db3037b8049ad80874bfd9
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Fri Sep 22 17:46:18 2017 +0100

    Formatting

commit 5b73fd1f8db5e6e23efa24d3d15c42723bd563f3
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Fri Sep 22 17:45:23 2017 +0100

    Explain my stylesheets

commit b44edf558e5e5a710665e4c284001525be8a980d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Sep 22 08:21:47 2017 +0100

    Write about Travis and Atom feeds

commit 49164bd4f1b1488e31b372c560b98e9c6461736e
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Sep 22 08:15:27 2017 +0100

    Document and tidy up atom_feeds.rb

commit bff35708d6339ed66ea50416e180148dbf1261d2
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Sep 22 07:39:13 2017 +0100

    Tidy up the README instructions

commit 9dbda589086357af104dcd5d9f8090b08ddb7158
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Sep 21 21:46:05 2017 +0100

    Add a proper serve-debug command

    [skip ci]

commit a571b5e6f3821fcd1cae7d89847b5222d5d70fb7
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Sep 21 21:43:21 2017 +0100

    And check in the screenshot!

commit 6dfdfed2959049bb21298578f7b347d85998b6e2
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Sep 21 21:43:01 2017 +0100

    Start to flesh out the README

commit 0f51fa1cfb78b5f3cf799fe25c45181a007c0f6c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Sep 21 21:37:49 2017 +0100

    /s/env/env

commit c53e93f13955626a340830d8b22c665b695696c7
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Sep 21 21:34:03 2017 +0100

    Add a few more directories to the .dockerignore

commit 63e200e92fdb9e5ff96680394e1295b7b5105c8e
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Sep 21 21:32:06 2017 +0100

    Push the Travis RSA key down into the .travis directory

commit 34b10bdacf38482c56501a53a9898415518b2caa
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Sep 21 21:31:49 2017 +0100

    Remove the TODO file from the repo

commit b7d873fcfa46fe74c2062e1a3960b0f41601ce5a
Merge: d3e1d476 330604f7
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Sep 21 21:25:51 2017 +0100

    Merge pull request #33 from alexwlchan/footnotes

    Re-enable support for footnotes

commit 330604f770e4905b51bda941235b511a24e9574c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Sep 21 21:20:05 2017 +0100

    Enable footnotes in Redcarpet

commit cb021c6ab1e25a5e7b626a799040bcdb61a35703
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Sep 21 21:19:56 2017 +0100

    Fix the test for Redcarpet-style footnotes

commit 120d801f02d83e3a73e6048cb8856e7590253719
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Sep 21 21:16:04 2017 +0100

    Add a test that footnotes are rendered correctly

commit d3e1d4767ce138a1d9dfa2eba450d0a6f6c14928
Merge: 93929324 df627722
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Sep 21 21:13:35 2017 +0100

    Merge pull request #32 from alexwlchan/atom-validation

    Fix issues spotted by W3C feed validator

commit df627722643b8768f0e6cfd602f58c9f33ea4dcb
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Sep 21 21:00:20 2017 +0100

    Properly minify the XML in the Atom feed

commit fdf1c3c2549fefcebe32f029128cf6abc2797331
Author: Alex Chan <alex@alexwlchan.net>
Date:   Thu Sep 21 20:45:23 2017 +0100

    Tidy up a bit of code

commit 2b3a308de8a32d7e4b39486bed477fbe8963abfb
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Sep 20 13:23:26 2017 +0100

    These paths are hard!

commit f9fa7d105336936451ee3d18c141bc743e96ba67
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Sep 20 13:11:28 2017 +0100

    Add tests that XML in feeds is minified

commit 529988fbea2c5fe0e03d47ac8e8d809c45b0f708
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Sep 20 10:46:52 2017 +0100

    Adjust those post dates to space them out

commit ceea10d3f78d14d9418dc0b47fe282cd3c945455
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Sep 20 10:44:32 2017 +0100

    Fix the location of the RSS feed

commit 83285814c1ce96ca9f97d674b5983f733b52060a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Sep 20 10:44:24 2017 +0100

    Remove bad attributes from HTML in the RSS

commit 9f01f5c660ca0e482b08c747ccbe2025840ecb66
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Sep 20 09:18:16 2017 +0100

    Actually validate the Atom feed in the test

commit 93328b8b5bb387714d022b88222146bd04c319c6
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Sep 20 08:53:00 2017 +0100

    Install tox on Travis

commit f85f2ba3737d8f083b3180a975cc27017a0a9ba0
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Sep 20 08:48:43 2017 +0100

    Actually run tox in Travis

commit 811f8e614829fdb509e560b412dbd70fd61994e3
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Sep 20 08:48:14 2017 +0100

    Cache the tox directory

commit 277865ef39a8b36fc2572e23fe85b258e1322b33
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Sep 20 08:44:05 2017 +0100

    Add a tox framework for validating Atom feeds

commit 939293245269fd72226befabe49621e8b03cdde7
Merge: 0d8a8f63 198c6733
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Sep 18 22:53:41 2017 +0100

    Merge pull request #30 from alexwlchan/comma-tags

    Don’t add a trailing comma to tags

commit 198c6733658832d6fee3e7a3cf0cb14f8383e85f
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Sep 18 22:31:33 2017 +0100

    Add a test for trailing commas

commit 175cb826257a7d14ab88a20de09c420597470992
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Sep 18 22:30:55 2017 +0100

    Don't add a trailing comma to tag names

commit 0d8a8f63e87112c67a831dd2dcbdbc061f25aeba
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Sep 18 22:21:33 2017 +0100

    Ensure we deploy from the right directory

commit 3968a5121c550f12a555e47950e2170dad5a7759
Merge: f98311ce de0101ae
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Sep 18 22:16:44 2017 +0100

    Merge pull request #29 from alexwlchan/into-the-src

    Move all the Jekyll source files into an src directory

commit de0101aeccbf143daaef478ead72ca9c331a3590
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Sep 18 22:12:59 2017 +0100

    Install from the right requirements.txt

commit 403c3dc5b5e35cd52916dcf15f702271cc4f93a4
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Sep 18 22:10:36 2017 +0100

    Tweak the contents of the .dockerignore

commit 184a59ee687a8c9486b074daf126ed87170c7b84
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Sep 18 22:08:29 2017 +0100

    We don't need to exclude those files any more

commit cbbe0e68b2d32f73fb76c81d2a76549ca60c56b1
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Sep 18 22:08:08 2017 +0100

    Change Makefile paths to point to the src directory

commit 34214b9b1d7b159299ecdd2d328b6640c6e5e304
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Sep 18 22:06:40 2017 +0100

    Move tests into a proper directory

commit f33016abeabb736984b1e635030c5e7589830a6d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Sep 18 22:06:19 2017 +0100

    Move all the Jekyll files into an src directory

commit f98311ced05b06e5fa032838730f3b4337fc2c43
Merge: da4680a0 95d1ca29
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Sep 18 22:03:03 2017 +0100

    Merge pull request #28 from alexwlchan/specktre-in-main

    Move Specktre into the main site container

commit 95d1ca2902c0caf9fe57f3103daeebdd7dc456e3
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Sep 18 21:56:04 2017 +0100

    Give the file a more accurate name

commit d40229b32032c29bd70ed0d075d63b97d7ec307f
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Sep 18 21:55:07 2017 +0100

    Remove the _specktre directory

commit 5a3893aebaeb9dcbcb8da9164c168299b3d70798
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Sep 18 21:54:29 2017 +0100

    Create the Specktre headers in the main build process

commit c5f1283096aae7ffe4e94a8cd11bd1ea38992ed8
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Sep 18 21:41:18 2017 +0100

    FFS, it's my package, get the version right!

commit 62c712a51a7d912bddfc8fa2b2825ec9f6a7dd1e
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Sep 18 21:40:58 2017 +0100

    Exclude the Specktre install script from Jekyll rebuilds

commit 1415f79fe44ff4d8f023f347fd739bfca051d677
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Sep 18 21:38:34 2017 +0100

    Install Specktre as part of the main build image

commit da4680a0f600f82c4b424809b791650f5f455f76
Merge: e99147d5 2291d2ba
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Sep 18 21:24:07 2017 +0100

    Merge pull request #27 from alexwlchan/git-commands

    Blog post about useful Git commands for CI

commit e99147d551b6810bc6f79666cddba211df916fc0
Merge: 5276f87c 22cb3b79
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Sep 18 21:23:58 2017 +0100

    Merge pull request #26 from alexwlchan/markdown-fixes

    Markdown fixes: make sure SmartyPants and syntax highlighting both work

commit 22cb3b796cc4f0aa84d7e60d5e874c175d118c54
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Sep 18 21:19:58 2017 +0100

    Get better tracing from the Travis run

commit 2291d2bab080ed693a38ac2929bf76a2c4773170
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Sep 18 18:46:54 2017 +0100

    [post] Some useful Git commands for CI

commit 39b42134d45ba40ca7fe32ca1b88449e25d68d74
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Sep 18 18:46:32 2017 +0100

    Add styles for miniposts

commit 707191c340d12b44703ca906d35bdfc3baeafd88
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Sep 18 18:46:20 2017 +0100

    Fix Markdown code block

commit d80cc6cff6ef5053f213f8ac86e5ae87b28dd7fb
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Sep 18 18:46:08 2017 +0100

    Tweak help text in slides plugin

commit 39cf19b0342d1be2050af2f7f6ec8fa5da6dfb97
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Sep 18 06:27:08 2017 +0100

    Add a minipost theme flag

commit a12cd0c97311ed2a0d6c8b5daa9aee24bc10ae26
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Sep 18 06:26:39 2017 +0100

    Don't rebuild for changes to _tests

commit a95e896a1926e37f8e35faa5d2114466299f61c7
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Sep 18 06:26:17 2017 +0100

    Changes to ensure Pygments is working

commit f67bff1d8b28a8336909d5d0ef936f0684a7ca36
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Sep 18 06:25:58 2017 +0100

    Enable Smartypants in Redcarpet

commit bf6169f4181558d2973b76dd8d19338ac90b1c16
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Sep 18 06:25:37 2017 +0100

    Switch to using Redcarpet for Markdown

commit b4de38f4de0eb5524500f269b9edd0ade59a09a1
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Sep 18 06:25:10 2017 +0100

    Add tests that Smartypants and syntax highlighting are working

commit 5276f87cbd265b19a8ebb213299d9daaa815d591
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Sep 17 21:42:19 2017 +0100

    Use $(git rev-parse --show-toplevel) in the Makefile!

commit f114385af79bf468eb1c9acfbe07763369ea0e74
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Sep 16 14:50:17 2017 +0100

    Add more to the .dockerignore

commit bfed9822166a31d63b6c84848ca78f686eb6b47a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Sep 16 14:17:10 2017 +0100

    Reduce size of the docopt slides

commit ac9068b4fa611826667895ff97763b7cca88cd65
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Mon Sep 11 13:32:55 2017 +0100

    Tweak the docopt post summary

commit 0eee07b1579720873cb647bf971fbd68e16d22c4
Merge: 33c772c0 1a25a262
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Sep 11 13:26:31 2017 +0100

    Merge pull request #24 from alexwlchan/fix-rsync

    Fix static file generation with rsync

commit 1a25a26212886d7fb0a2acdcd4d4c9472d63211c
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Mon Sep 11 13:18:58 2017 +0100

    Fix static file generation with rsync

commit 33c772c0cc1f70568f7b48d0916e92a5ab0be9d4
Merge: f36b5f81 21cbbba2
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Sep 11 13:03:12 2017 +0100

    Merge pull request #22 from alexwlchan/docopt-slides

    Add notes and slides from my docopt talk

commit 21cbbba288cf4d1fc074a6f5c5b885d0b5bc2d3c
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Mon Sep 11 12:02:22 2017 +0100

    Add backend pieces for docopt talk

commit c0858f2aab40e123bfff2ed33437da68ef687b04
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Mon Sep 11 12:01:54 2017 +0100

    Reduce repetition in the socialgraph code

commit 743fd24fe3170e10ee9516b889332954ccca83f4
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Mon Sep 11 12:01:36 2017 +0100

    Make sure Specktre assets go to the right directory

commit f36b5f81fbf06ce181cb76daf759c261b7c94e2d
Merge: c400de59 33e686d9
Author: Alex Chan <alex@alexwlchan.net>
Date:   Mon Sep 11 07:29:19 2017 +0100

    Merge pull request #21 from alexwlchan/archive-redesign

    Redesign the archive pages

commit 33e686d93a95b58a0c6146468566655b22780794
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Mon Sep 11 07:24:11 2017 +0100

    Add a couple of tests for the formatting pieces

commit ce790a49d1db55e07cd8b87debc6639add47fddf
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Mon Sep 11 07:22:06 2017 +0100

    Add .jekyll-metadata to .gitignore

commit 37665b0ac1f7b9450d616e7797de96eff0842556
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Mon Sep 11 07:21:44 2017 +0100

    Clean up running containers with 'make serve'

commit e1059704f35646e10bb888f9249bf9caf6cb16bb
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Mon Sep 11 07:21:30 2017 +0100

    Adjust the width of the date column

commit 06869a47588d02d84e78686c6211ae35469986ac
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Mon Sep 11 07:20:07 2017 +0100

    Add year headings in the global archive

commit 5a1eed83bf1749a33705793188c71884d9a0494c
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Mon Sep 11 07:12:20 2017 +0100

    First pass at redesigning the archive

commit c400de59a40919915e2de809378459ee031c29da
Merge: fec68a57 2e9b86b0
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Sep 10 23:29:44 2017 +0100

    Merge pull request #19 from alexwlchan/no-jekyll-feed

    Back to doing manual generation of Atom feeds

commit fec68a57e7f971c83226c8ac129116851883279d
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Sun Sep 10 23:09:25 2017 +0100

    Put _slides in the right place

commit 2e9b86b03b81324c3eef4a0aeaafad5397f48627
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Sep 10 22:56:04 2017 +0100

    Include --detach or the build hangs

commit a159c0f757c856b82041c8803cd74c35fe3d230f
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Sep 10 22:14:35 2017 +0100

    Back to doing manual generation of Atom feeds

commit ecaf9527d3b40cb7952ae988137eece04eff9948
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Sep 10 21:48:59 2017 +0100

    Wait, that doesn't work

commit 6bb01a536a70368d15eae44dfca1586bb398f38f
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Sep 10 21:47:31 2017 +0100

    A few small Liquid optimisations

commit 5f985a6aee25e7806e0ff686e1832aa81d5c7272
Merge: d26d7871 d2e5e63d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Sep 10 21:28:39 2017 +0100

    Merge pull request #18 from alexwlchan/more-speedups

    A few more ideas to make the build go faster

commit d2e5e63d0b58b90c63ec3a4d4fc912b0ad5ff55f
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Sep 10 21:24:26 2017 +0100

    rsync another large-ish (getting larger) directory

commit 1b8ccfc8274323f3006aff6f6441ecb2223aa9c3
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Sep 10 21:21:18 2017 +0100

    Okay, I actually need g++ for the unf gem

commit b90b7e9b5512ddffdf0d5b67195351df4250f63e
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Sep 10 21:16:15 2017 +0100

    Remove a handful of unused Alpine packages

commit 986bc8cc9b2fc129edc587437f21cfb664481b19
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Sep 10 21:11:38 2017 +0100

    Remove some gems I don't use (we have Linux inside Docker, not Windows)

commit 59850defca60ce0dbadc1acbdffbe879a2e49927
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Sep 10 20:58:59 2017 +0100

    Skip installing rdoc for Ruby gems

commit 97f34ea795f05525a6efb8c5bf0eb96cb8d0e74e
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Sep 10 20:51:42 2017 +0100

    Cache Python packages used in the build

commit d26d78711f8f538e22cfb84695e575a7cac6f205
Merge: 8d4925f8 a47f1ede
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Sep 10 20:50:36 2017 +0100

    Merge pull request #17 from alexwlchan/remove-travis-caching

    Remove Travis caching entirely

commit a47f1ede651f0002a9d9257e34b984115dd36d4f
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Sep 10 20:43:37 2017 +0100

    Remove Travis caching entirely

    In practice, Docker builds are fast enough that caching actually
    slows us down.  Also, I can't get the caching to work correctly.

commit 8d4925f8eb865ca453ff3f08921efee55b127b81
Merge: 0550f072 de742a98
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Sep 10 19:26:29 2017 +0100

    Merge pull request #14 from alexwlchan/rsync-large-files

    Switch to copying large files with rsync

commit de742a9868c79d966a88a5c745f17d88b30a9f60
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Sep 10 09:41:37 2017 +0100

    Read the setting directly

commit f3aa412ddf984161e34c3c4eb7fc08ea887858e0
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sun Sep 10 09:39:56 2017 +0100

    Switch to copying large files with rsync

    Using a trick from http://rentzsch.tumblr.com/post/58936832594/speed-up-jekyll-using-one-weird-trick

    Shaves ~8s off the build on my local machine

commit 0550f072334dae26a584bc51aea3f27e24480a4c
Merge: 3de9972c eba26223
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Sep 9 23:41:30 2017 +0100

    Merge pull request #12 from alexwlchan/feed-validation

    Switch to using jekyll-feed for feed generation

commit eba26223b660af37e847c1661e5083ef07c8e6c3
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Sep 9 23:27:09 2017 +0100

    Okay, get rid of the explicit RSS tests again

commit 2e1587cf8972d72b1c1cca175a0efe95cb6e12da
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Sep 9 23:26:28 2017 +0100

    Fixes discovered during RSS validating

commit 5698461fc66e037c3ea24fea9c487c4a3deff27c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Sep 9 23:25:43 2017 +0100

    Just use the jekyll-feed plugin

    I was avoiding this plugin so I didn't clobber anybody's RSS
    reader by keeping the old IDs.

    Oops, oh well, no reason not to use it now!

commit c1bdc4c99d9aee5691189c16dd50eef1be8ef8b6
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Sep 9 22:45:17 2017 +0100

    Scope the pushd/popd correctly

commit fc80caec171b7b37160c0fe7675e4ebb1eb2600d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Sep 9 22:36:12 2017 +0100

    Add a test that the feed passes validation

commit 8d84b6e8c3ab96e664212a8e8425fbf9ebc531e4
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Sep 9 22:35:54 2017 +0100

    Don't download feedvalidator in the repo

commit 64fc9e1c970c45541956bf759892d616ae06042b
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Sep 9 22:30:31 2017 +0100

    Install the feedvalidator library

commit 3de9972caef44b2525e83cae29e345bb21e545a2
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Sep 9 18:44:20 2017 +0100

    Try to fix date formats in the Atom feed

    Related: #9

commit 8c458ee5b90559f2c6f563dbc6ec95a6ec993f21
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Sep 9 08:33:29 2017 +0100

    Exclude private keys from the build

commit a69d2a781160c81889b9c42ba6359c4ece404d40
Merge: e8706c33 e66573cb
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Sep 9 08:27:24 2017 +0100

    Merge pull request #8 from alexwlchan/travis-ci

    Start running tests and deployments in Travis

commit e66573cb4b23ef543a2278123fdf9cddea7dde76
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Sep 9 08:22:32 2017 +0100

    Naming things is hard

commit a2b3e66272903e4c5639d8912db4e4ccd0535901
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Sep 9 08:20:23 2017 +0100

    coffee++

commit 69e7e9ac3cddf772ed5a914d5b51953fbdaff272
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Sep 9 08:19:17 2017 +0100

    Only deploy on push to master

commit de7dad6b12abb65bba6570599883185f1d0e9977
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Sep 9 08:18:38 2017 +0100

    Deploy needs a publish

commit a8574dc3e87b152126c3fc365bc4f348b4108e5a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Sep 9 08:13:31 2017 +0100

    Add an export

commit acf1a16db4f6d0b56a9dc5afba636c10c0881b0e
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Sep 9 08:08:41 2017 +0100

    Ensure we rsync to the right folder

commit a30c68d0eaeb29fad8d6a07ca6c78b5cc371f650
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Sep 9 07:52:56 2017 +0100

    Make the image freezer more verbose

commit e3383a4e2c2feacc29f81b447ec00f0bb9057103
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Sep 9 07:52:41 2017 +0100

    Ensure the key perms are correct

commit 7b9fa0562f2d40c5b9d6dc9cde8e0bf3a6c173bf
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Sep 9 07:46:10 2017 +0100

    Add the Travis key to the repo

commit 1934f3d11948c6178c4a1514e246c890d40bd406
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Sep 9 07:11:36 2017 +0100

    More caching tweaks

commit 26b642860804b273d368eaaea2ae336ec0c05e4e
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Sep 9 07:06:03 2017 +0100

    More fixes for the cache freeze/unfreeze

commit 7d11fe2bab2f958ac3dc5bfc8ea5683278947cdb
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Sep 9 07:01:39 2017 +0100

    Make the cache freeze/unfreeze more verbose

commit 50efbef73ca6f0b51ffdf0508a99d9ae927591e6
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Sep 9 06:56:06 2017 +0100

    Fix image freezing

commit ba73bf5a525581b2071bc0bfec43ec27908172df
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Sep 9 06:49:48 2017 +0100

    Don't ask 'Are you sure you want to continue connecting?'

commit a58da569e67a4d6b8bad9faa35b3f115dedf63e4
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Sep 9 06:47:59 2017 +0100

    Do some rudimentary caching of Docker images between Travis runs

commit ed9bed1eae01ff1d7c35f0378cfd73e23638fb61
Author: Alex Chan <alex@alexwlchan.net>
Date:   Sat Sep 9 06:40:37 2017 +0100

    Write an rsync command for deploying files

commit 5c105f0306a42239b93900b351edd4b935f1b61d
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Sep 8 22:34:14 2017 +0100

    Don't delete the container, just stop it

commit 720df5398baccca4e68ee1c495c3b811f8e0b409
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Sep 8 22:26:13 2017 +0100

    Actually run the correct script

commit c338e3af813f3ca197099a6c46ce1b60729fbbe7
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Sep 8 22:19:40 2017 +0100

    Specify a Python version

commit 3b9202047eea3a4311157f037b1c4b621a26eefd
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Sep 8 22:18:05 2017 +0100

    Add a publish step

commit 30510636d404a00decdfa225398ad8fbb5d98a22
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Sep 8 22:17:30 2017 +0100

    Add some debugging to the Travis script

commit 17507a9035fc017cee0509a2b8c0b3026908067c
Author: Alex Chan <alex@alexwlchan.net>
Date:   Fri Sep 8 22:14:44 2017 +0100

    Add some initial Travis config

commit e8706c33f30cb5db46d8a2f257bbaf7a4fde0bc9
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Fri Sep 8 21:08:18 2017 +0100

    Clean really means clean

commit a829b3243724337dd5ce05430ad13d336f467b8f
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Fri Sep 8 21:08:11 2017 +0100

    Fix a broken Liquid tag

commit c17f6b8f3c195adedd3be3d8baa820568a73a8bd
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Fri Sep 8 20:16:35 2017 +0100

    I almost forgot 2015!

commit 90fd396ae52f227fc88a4431afa56eff4cecbda7
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Fri Sep 8 20:13:56 2017 +0100

    Migrate across the remaining content

commit e896a406f8d0ec355c1d8eb6e51ee2af42f67b16
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Fri Sep 8 20:07:35 2017 +0100

    Add social cards and sharing

commit 8671340e45985331ce15795dcbbb71cc827ef5f3
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Fri Sep 8 19:57:16 2017 +0100

    Tweak the appearance of titles (again)

commit df4d7b90787fd71ab5f7a00cf8b8578896719db8
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Fri Sep 8 19:57:05 2017 +0100

    Add a note about building header files

commit f00a8aa554914b89c5b679ee58308876387a7eaa
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Fri Sep 8 17:45:51 2017 +0100

    Remove some debugging code

commit 9237e1c3f4658a7daa7241357dba52a3d54a2b81
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Fri Sep 8 17:44:57 2017 +0100

    Migrate the rest of the existing posts

commit f42ea53f400630e8b5b2b29e79154a34b72e9217
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Fri Sep 8 17:44:27 2017 +0100

    Lots of code for themeing

commit eaf1d8f293083a8e38091838a56951e502676b02
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Fri Sep 8 15:41:30 2017 +0100

    Migrate everything I wrote in 2013

commit 6dc4d9637e8b7c532b95925eadc9d13ff3fe7c1e
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Fri Sep 8 15:40:53 2017 +0100

    Tweak dates on archive pages

commit aa590f2f11fa36fc45322d0923cefb252c115047
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Fri Sep 8 15:40:43 2017 +0100

    Ensure tweets always show their avatars

commit a9e9510981c162496a7b0fe7a3a74a123b339e19
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Fri Sep 8 15:40:33 2017 +0100

    Ensure posts display in the right order!

commit 6fb4c3a84cc5558a22b28ac6ba71b1ec689bbbb8
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Fri Sep 8 11:42:57 2017 +0100

    Another entry in the .gitignore

commit 21a3666fb44ac4b662e73fcf0489e1c3293f7c46
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Fri Sep 8 11:42:49 2017 +0100

    Migrate across the first post

commit c7ea39bc12a6c194750d8af12ce10209a0fa3544
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Fri Sep 8 11:11:54 2017 +0100

    Remove some unused code

commit 0f2a51444943edbf167a44e29a664c2a0fbbbe3e
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Fri Sep 8 11:11:47 2017 +0100

    Tweak the <title>

commit 5095913f9351dd610ad6676b01c008f3fc90eda6
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Fri Sep 8 11:11:38 2017 +0100

    Get archives completely working

commit aba9f4fd25d61f1eadd117b4f8534394f6f518e4
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Fri Sep 8 10:17:49 2017 +0100

    Add tests for year and month archives

commit bcbfe6af78cf9b793033bafa77f6291c575d3dea
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Fri Sep 8 10:15:19 2017 +0100

    Flip the order of archives -- newest first!

commit 4815384d230c6a756d4bf508c8719e12ad0a2031
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Fri Sep 8 10:13:47 2017 +0100

    Rudimentary year and month archives

commit 6c6433ac23e4167015a723d4d64a89227d2bdb23
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Fri Sep 8 07:21:55 2017 +0100

    Consolidate and simplify index pages

commit c0862fffd9aa8b0be1128591e83e95407361fefa
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Fri Sep 8 07:16:12 2017 +0100

    Fix a layout bug in the minified HTML

commit 9610180927f09a8d66bb5e5586475254bf2701bd
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Fri Sep 8 07:15:56 2017 +0100

    Trim the size of the Docker image

commit a1386a06bae23f08cbe2402dcd4d38bdf26ac1a4
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Thu Sep 7 23:22:29 2017 +0100

    Minify HTML upon publishing

commit 12a13c1961ff98af97b75d855a276fecb055ce9c
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Thu Sep 7 23:13:28 2017 +0100

    Remove the jekyll-feed plugin

commit a83380d8e27a21e92a3468ffe0c7a855c3dd00d2
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Thu Sep 7 23:11:58 2017 +0100

    Switch to using my template for the Atom feed

commit b58f40662f0c5bce73a086d56661193fd8bdf1fb
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Thu Sep 7 13:16:11 2017 +0100

    Add a usage example to the Twitter plugin

commit b1a03a6b36115f4e35cfa727b60e692c8635280b
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Thu Sep 7 13:14:50 2017 +0100

    Add a comment to the Twitter plugin

commit f66ad30a9ac53d268c261ebd61f112b73ea9c373
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Thu Sep 7 13:09:05 2017 +0100

    Implement the initial Twitter embed plugin

commit 2f4c082cd371f358e676c7735190eb0b0893a82d
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Wed Sep 6 09:38:00 2017 +0100

    Pull some personal details out of the template logic

commit cafb0b9dab8823cf606508914dc14183b6442ac2
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Wed Sep 6 09:00:19 2017 +0100

    Expunge the minima theme

commit a3575e040aa1120651946b0e878f2c45a89c01c1
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Wed Sep 6 08:59:35 2017 +0100

    Switch back to Rouge so fenced code blocks work!

commit a4ec09637cf62d8a5d739683c4e58d9b95c94e56
Author: Alex Chan <a.chan@wellcome.ac.uk>
Date:   Wed Sep 6 08:58:44 2017 +0100

    Implement pagination links

commit 0a682408e8cf859d2a91efd3790b13ceaa7f0d4f
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Sep 6 08:02:57 2017 +0100

    More TODO items

commit 0ab378dca11196898b8ee387cc0877ba943fb719
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Sep 6 07:47:26 2017 +0100

    Add a TODO.md

commit 9f17bbc95c667cdc4b04d67129cd6e9f00d1c923
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Sep 6 07:36:41 2017 +0100

    Pagination, take 2

commit 9ca00ac7f058e53516801d51f0dae9340d207cd3
Author: Alex Chan <alex@alexwlchan.net>
Date:   Wed Sep 6 07:03:19 2017 +0100

    Get rudimentary tag pages working

commit 7a2cdcd8e68cd56b74bac8de71bb5c50fb3909e2
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Sep 5 23:41:39 2017 +0100

    Make pages look a little nicer

commit c8a21666cf9aa9c4fa9f44316f35dc58eaffe65f
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Sep 5 23:38:24 2017 +0100

    A sprinkling of SmartyPants

commit 5eeaf29267250e65474c5adb61f42021cf50e071
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Sep 5 23:34:47 2017 +0100

    Comments and analytics: just say no

commit 7018dce0ad69a5dfd542a3ba7e4900d49b37bcf0
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Sep 5 23:34:19 2017 +0100

    Fix the broken 'Read more' link

commit 2632e4d6e705318f089dd40418fcfd16745ebd27
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Sep 5 23:34:08 2017 +0100

    Delete some unused includes

commit d585a92cc0d1d7efea3645f90daa118abb32cdb0
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Sep 5 23:33:37 2017 +0100

    Tweak some footer styles

commit 8b2df4c2733db464bc0627a0d79a1b3821d82bad
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Sep 5 23:30:29 2017 +0100

    Switch to Pygments for syntax highlighting

commit 89cb27c296890ab5100e95d6a2ebb8547e71d128
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Sep 5 21:39:55 2017 +0100

    Get post layouts to work

commit 57c95ab169c726405e14602608dd3f0beaed23d0
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Sep 5 21:16:28 2017 +0100

    Add a very basic testing framework

commit 6002c3a1614435f6a77204808811622380ca9647
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Sep 5 21:10:09 2017 +0100

    Enable basic pagination

commit 685999ea22dd578e1e816a44fad23850d37ec135
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Sep 5 20:55:57 2017 +0100

    Copy across the SCSS files from the old site

commit fbcec8b1acccfa742b9b5439431b99e2232d5a0a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Sep 5 20:41:50 2017 +0100

    Copy across the default Minima theme

commit 46f286b32d70bb0d0451e66464bcf4b214e59304
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Sep 5 20:39:47 2017 +0100

    Add support for the Specktre banners

commit 3876038006514d1d5d8b2a070ae088753d9aaff8
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Sep 5 20:18:03 2017 +0100

    Start to migrate the old site theme

commit 42a17dd011172ed18365c53bf32d96693d6c3f2e
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Sep 5 20:02:45 2017 +0100

    Add some basic Make tasks and a README

commit cac5fcf49b3b8d1530587216fe5de5804cab571a
Author: Alex Chan <alex@alexwlchan.net>
Date:   Tue Sep 5 19:49:40 2017 +0100

    Commit of basic Jekyll framework

{% endraw %}