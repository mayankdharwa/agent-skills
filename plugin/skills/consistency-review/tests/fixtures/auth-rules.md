# Authentication rules

## Token expiry

Access tokens expire after 30 minutes. Every token must be refreshed before it
expires by calling the refresh endpoint with a valid refresh token.

For the session timeout details, see [retention](retention.md#session-timeout).

## Refresh policy

A refresh token is valid for 30 days. Clients should rotate refresh tokens on
every use.
