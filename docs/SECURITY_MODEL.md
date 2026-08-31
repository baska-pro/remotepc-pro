# Security Model

RemotePC Pro is an authenticated remote-administration utility, not a security boundary.

## Authentication

Telegram access is limited by an allowlist. The dashboard requires an allowed Chat ID and a short-lived OTP delivered through Telegram. The application also uses CSRF checks and rate limiting.

## Public exposure

Default repository configuration binds the dashboard to localhost. Direct public-internet exposure is not recommended.

## Elevated features

Some code paths can perform powerful administration actions. The public package keeps advanced commands and the web file manager disabled by default. Enabling sensitive features should be an explicit local decision on a machine you are authorized to administer.

## Local privilege

Actions execute with the Windows privileges of the running process. Windows administrators can stop the application, alter its files, or remove local startup configuration.
