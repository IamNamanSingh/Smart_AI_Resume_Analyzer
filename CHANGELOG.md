# Changelog

All notable changes to the Smart Resume AI project will be documented in this file.

---

## [1.0.0] - 2026-06-12

### Added
* **MVC Project Architecture**: Separated layouts rendering (`pages/`), styles and components (`components/`), database setups (`core/` & `database/`), and logic services (`services/`).
* **Interactive Admin Dashboard**: Added four Plotly Express data diagrams mapping upload rates, target roles, match distribution histograms, and platform averages.
* **Unified Database Schema**: Consolidated individual feedback tables and parsed data metrics into a single SQLite storage file (`resume_data.db`) managed via migrations.
* **Automated Unit Tests**: Built 13 test units under `tests/` covering parsing, connection isolation, and dashboard calculations.
* **Guide Documentations**: Created guides mapping screenshots locations (`SCREENSHOT_GUIDE.md`) and recommended video tutorials sequences (`VIDEO_GUIDE.md`).

### Changed
* **Top Navbar Navigation**: Replaced the sidebar with a modern desktop topbar featuring horizontal radio switches and admin popover modules.
* **Styling Variables System**: Configured standard HSL stylesheet classes targetingStreamlit container borders.

### Removed
* Obsolete Spacy-based analyzer module directory (`resume_analytics/`).
* All hardcoded email credentials from verification checks.
* Original author usernames and repository links.
