# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased] 

### Added

- Add `FORWARD_HEADERS` to settings.

### Changed

- Only headers stated in `FORWARD_HEADERS` are forwarded.

## [0.0.1] 2026-03-04

### Added

- Basic unit tests for current basic features.
- Multipart/Form-Data forwarding.
- Forward all HTTP headers to `HOST`
- Request forwarding to `HOST`.
- `HOST` option can be passed via `ProxyBase` kwargs.
- `HOST` option can be loaded from `REST_API_PROXY` (settings.py).
