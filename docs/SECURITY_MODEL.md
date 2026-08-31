# Security Model

RemotePC Pro is an authenticated owner-only administration utility, not a Windows security boundary.

## Authentication

Telegram commands are limited to configured Chat IDs. Dashboard login requires an allowed Chat ID and a short-lived OTP delivered through Telegram. The dashboard also applies CSRF checks, rate limiting, secure session settings, and response security headers.

## Network exposure

The default dashboard address is `127.0.0.1`. Direct public-internet exposure is not recommended. Use a private network/VPN or a correctly configured TLS reverse proxy if remote browser access is required.

## Public capability surface

The public edition is deliberately limited to telemetry plus Windows lock, restart, and shutdown. It does not include arbitrary command execution, remote file browsing/transfer, screenshot/webcam/audio capture, keyboard/mouse injection, credential collection, or hidden persistence.

## Local privilege

Actions execute with the privileges of the Windows account running RemotePC Pro. Windows administrators can stop or modify the application. This project does not attempt to bypass Windows security controls.
