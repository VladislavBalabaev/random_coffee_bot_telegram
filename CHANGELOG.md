<!-- markdownlint-disable MD022 MD024 MD032-->

# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased] - YYYY-MM-DD - Developer
### Added
- Nothing yet

### Changed
- Nothing yet

### Fixed
- Nothing yet

### Removed
- Nothing yet

---

## [0.1.0] - 2025-05-25 - Vlad
### Updated
- Functionality of TgUser repository

## [0.1.0] - 2025-05-24 - Vlad
### Added
- Admin's command to send messages
- Bot's menu

### Updated
- Simplify UserService
- Simplify /messages

## [0.1.0] - 2025-05-22 - Vlad
### Added
- Send notification to user in case of error
- Clear user's state when error occurs
- Bot's keyboard creation
- Admin's command to see messages

### Updated
- No "\n" in console logs
- Directory paths

### Fixed
- Timestamp creation in DB models

## [0.1.0] - 2025-05-21 - Vlad
### Updated
- Separate logging for bot logic, aiogram, API. Bot's console logging includes errors from aiogram

## [0.1.0] - 2025-05-20 - Vlad
### Added
- API for receiving NesUser data
- Dependense of API and Bot containers on DB

### Updated
- Tg messages translated to eng
- Upsert process of NesUser

## [0.1.0] - 2025-05-19 - Vlad
### Updated
- Error handling system

## [0.1.0] - 2025-05-14 - Vlad
### Added
- Tests for NesUser pydantic to sqlalchemy conversion

### Changed
- Divide user repository into tg & nes
- Update nes_user pydantic model

## [0.1.0] - 2025-05-13 - Vlad
### Changed
- User pydantic scheme

## [0.1.0] - 2025-05-12 - Vlad
### Changed
- Filter message on text
- Gracefully stop docker

## [0.1.0] - 2025-05-09 - Vlad
### Added
- Error handling notifications
- Startup & Shutdown notifications
- Processing of pending updates
- Sending documents function
- Example of .env

### Changed
- Timezones in DB models
- DB Repositories work with context of session

## [0.1.0] - 2025-05-08 - Vlad
### Added
- SQLAlchemy repositories functionality
- User context service functionality
- IO stream for telegram bot's messaging

### Changed
- Structure of DB models
- Cancel & ZeroMessage handlers

## [0.1.0] - 2025-05-07 - Vlad
### Added
- Models for DB and pydantic

## [0.1.0] - 2025-05-05 - Vlad
### Added
- JSON file logging
- script for combining all python code into single .txt
- simple DB structure
- service structure
- dependency intergration structure

### Changed
- whole src/ structure
- MongoDB to Postgres & SQLAlchemy
- json logging, file rotation after 10MB, up to 12 log files stored

### Fixed
- library's name

## [0.1.0] - 2025-05-02 - Vlad
### Added
- setup info in developers manual
- `ruff` linting
- `black` formatting
- logging system
- .env reading

### Changed
- `src` structure
- requirements versions

## [0.1.0] - 2025-04-19 - Boris
### Added
- manual of how to contribute

## [0.1.0] - 2025-04-19 - Vlad
### Added
- initial release of NespressoBot
- admin/user/staff handlers
- core telegram bot architecture
- requirements
- docker setup
- notes for developers
