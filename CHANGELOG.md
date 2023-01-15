# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased

### Fixed
- Fixed CI to use VERSION file
### Changed
- removed `pychalk` dependency

### Added
- added support for `post` releases that can be used to indicate changes on a released patch version that is in production

### Changed
- Changelogs will always have a newline at the end of a file after being dumped

## 0.2.29 - 2022-05-09
### Added
- added `--no-commit` option
- added `pre-commit` hook

### Fixed
- fixed handling of markdown newlines

## 0.2.23 - 2021-01-14
### Added
- added `auto_generate` option to `links` section in config
- added console command to get the latest version from the Changelog

### Fixed
- Fixed typos
- Fixed #7 where link generation failed if no version was available
- fixed issues with auto generation of links where unrelease template was wrong
- fixed config hierarchy
- If running on gitlab-ci and no host URL is configured the URL is derived from CI_PROJECT_URL
- Fixed #17 where a single newlines was interpreted as a paragraph split, going against the markdown spec

## 0.2.17 - 2020-01-14
### Added
- `release` command will make sure changelog is valid before doing any changes.
- It is now possible to automatically generate links for versions using `kacl-cli link generate` or `kacl-cli release patch --auto-link`

## 0.2.16 - 2020-01-07
### Fixed
- fixed issue #3 that did not detect linked versions with missing links
- fixed issue #2 that caused errors on files with CRLF endings.

## 0.2.15 - 2020-01-06
### Fixed
- Fixed bug where configs where not merged recursively

## 0.2.14 - 2020-01-06
### Fixed
- fixed bug where default config was not copied into the sdist package
- fixed issue where help could not be retrieved for commands if no valid CHANGELOG file was given

## 0.2.13 - 2020-01-05
### Added
- added config file support
- added CLI tests for `verify` command

## 0.2.12 - 2020-01-02
### Fixed
- Validation reported success even if versions did contain information outside of change sections

## 0.2.11 - 2019-12-26
### Fixed
- Fixed issue where description on dockerhub was not updated when deploying

## 0.2.10 - 2019-12-26
### Fixed
- issue where build had been triggered reoccuringly whenever Travis built the master branch

## 0.2.9 - 2019-12-26
### Fixed
- CI behaviour on master branch

## 0.2.8 - 2019-12-26
### Added
- added git support to the `release` command. When using `--tag/--commit` changes will be tracked by git
- added support for simple version increment. User `kacl-cli release [major|minor|patch]`

## 0.2.7 - 2019-12-25

## 0.2.6 - 2019-12-23
### Fixed
- fixed issue where `--version` resulted in error if no CHANGELOG.md file was found within the execution directory

## 0.2.5 - 2019-12-23
### Added
- added checks for `release` function that now checks if there are *available changes*, *already used version* and *valid semver in descending order*
- added default content checks
- cli will now check for valid semantic version when using `release` command
- implemented basic cli with `new`, `get`, `release`, `verify`
- added `--json` option to `verify` command
