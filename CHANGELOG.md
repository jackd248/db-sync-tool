# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [2.2.6] - 2021-01-18
### Added
- [Task] Extend scripts feature
- [Doc] Support section
- [Doc] Quickstart documentation
- [Task] Improved console output
- [Task] Drupal recipe uses Drush
- [Doc] Release Guide added
- [Doc] Advanced documentation

## [2.2.5] - 2020-12-28
### Added
- [Task] Allow run command to fail
- [Improvement] Adjust console header

## [2.2.4] - 2020-12-28
### Added
- [Task] Refactoring
- [Task] Additional output
- [Task] Refactor authorization
- [Task] Client "Local"

## [2.2.3] - 2020-12-23
### Added
- [Task] Database port is not required
- [Task] User confirmation for database import
### Fixed
- [Bugfix] Nested dict for shell argument initialization
- [Bugfix] Wrong dict key for ssh key

## [2.2.2] - 2020-12-09
### Fixed
- [Bugfix] Requirements in setup extended

## [2.2.1] - 2020-12-06
### Added
- [Task] After_dump feature added
### Fixed
- [Bugfix] Fix legacy shell script call

## [2.2.0] - 2020-12-03
### Added
- [Task] Added python 3.5 support
- [Task] Shell arguments extended
- [Task] Improved test output
- [Task] Extend setup
- [Task] Added Travis CI
- [Task] Manual database credentials
- [Task] Refactoring module structure
- [Task] Simplify extensions to recipes
- [Task] Further error prevention
- [Task] Wildcards for ignore tables
### Fixed
- [Bugfix] Drupal database settings parsing improved

## [2.1.0] - 2020-11-05
### Added
- [Task] Test scenario symfony2.8 added
- [Task] Support Symfony v2.8

## [2.0.1] - 2020-11-05
### Added
- [Task] Validating database credentials

### Fixed
- [Bugfix] SSH key authorization for dump-remote

## [2.0.0] - 2020-11-03
### Added
- [Task] Support legacy script call from command line
- [Task] Improved script handling
- [Task] Support Wordpress
- [Task] Extension Drupal improved
- [Task] Run sync as module
- [Task] Adding supported framework Drupal 8
- [Task][!!!] Refactoring for export as python package
- [Task] Connection output improved

## [1.8.0] - 2020-10-06
### Added
- [Task] Error handling improved
- [Task] Logging output optimized
- [Task] Re-enable check dump feature
- [Task] Added test environment
- [Task] Host linking feature added
- [Task] Added password option for hosts
- [Task] Adding "no-tablespaces" option for mysqldump command
- [CleanUp] Refactoring code

### Fixed
- [Bugfix] Logging error bug