# Python Social Auth - Examples

Python Social Auth is an easy to setup social authentication/registration
mechanism with support for several frameworks and auth providers.

## Description

This is a collection of examples implementations of the
python-social-auth ecosystem functionality.

## Documentation

Project documentation is available at <https://python-social-auth.readthedocs.io/>.

## Backend configuration

The examples demonstrate a broad selection of backends supported by current
social-auth-core. Enable the providers you need and register applications with
those providers before filling in your local credentials. See the
[backend documentation](https://python-social-auth.readthedocs.io/en/latest/backends/)
for provider requirements and callback URLs.

Older configurations need updated backend classes and credential prefixes:

| Provider | Backend name / credential prefix |
| --- | --- |
| Dropbox | `dropbox-oauth2` / `SOCIAL_AUTH_DROPBOX_OAUTH2_` |
| LinkedIn | `linkedin-openidconnect` / `SOCIAL_AUTH_LINKEDIN_OPENIDCONNECT_` |
| Bitbucket | `bitbucket-oauth2` / `SOCIAL_AUTH_BITBUCKET_OAUTH2_` |
| OpenStreetMap | `openstreetmap-oauth2` / `SOCIAL_AUTH_OPENSTREETMAP_OAUTH2_` |
| Yahoo | `yahoo-oauth2` / `SOCIAL_AUTH_YAHOO_OAUTH2_` |
| Microsoft Live → Microsoft Graph | `microsoft-graph` / `SOCIAL_AUTH_MICROSOFT_GRAPH_` |
| Evernote Sandbox → production | `evernote` / `SOCIAL_AUTH_EVERNOTE_` |
| Fedora | `fedora-oidc` / `SOCIAL_AUTH_FEDORA_OIDC_` |

Use Google OAuth2 or OpenID Connect instead of Google OAuth1, OpenID, or Google+,
and Mendeley OAuth2 instead of OAuth1. Register the callback URL for the new
backend name, for example `/complete/linkedin-openidconnect/` in the Flask
example. Changing a provider or protocol does not automatically migrate existing
account associations; review provider identifiers and link accounts while
authenticated instead of assuming old associations are compatible.

To check all example backend configurations without installing the frameworks:

```sh
uv run --no-project --with 'social-auth-core[all]' python scripts/check-backends.py
```

## Contributing

Contributions are welcome!

Only the core and Django modules are currently in development. All others are in maintenance only mode, and maintainers are especially welcome there.

See the [CONTRIBUTING.md](https://github.com/python-social-auth/.github/blob/main/CONTRIBUTING.md) document for details.

## Versioning

This project follows [Semantic Versioning 2.0.0](https://semver.org/spec/v2.0.0.html).

## License

This project follows the BSD license. See the [LICENSE](LICENSE) for details.
