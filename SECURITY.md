# Security Policy

EduToolsHub is a Django educational productivity application with authenticated user workflows and integrations with external information services.

## Reporting a Vulnerability

Please report security vulnerabilities privately to the repository owner through GitHub or the contact information published on https://allkvd.dev/. Do not publish exploitable details in a public issue.

Include the affected component, reproduction steps, impact, and relevant evidence.

## Security Practices

- Django authentication and CSRF protections are used for state-changing workflows.
- User-owned records must be accessed within the authenticated user's scope.
- Form/model validation is used for application inputs.
- External-service failures are handled without exposing internal stack traces to users.
- Production secrets belong in environment configuration and are not committed to the repository.
- Local development uses SQLite; production database choice is deployment-specific and is not represented as a required PostgreSQL migration in the current application.

## Secret Handling

Never commit `.env` files, API keys, database passwords, signing keys, or other production credentials.
