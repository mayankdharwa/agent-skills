# Data retention

## Token expiry

Access tokens expire after 30 minutes, except for service accounts whose access
tokens expire after 24 hours. Every token must be refreshed before it expires.

## Cleanup job

A nightly job purges expired refresh tokens. A refresh token is valid for 7 days
before it is purged.
