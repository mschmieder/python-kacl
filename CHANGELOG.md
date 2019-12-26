# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
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

[Unreleased]: https://github.com/mschmieder/python-kacl/compare/v1.0.0...HEAD