# Security Rules

- Never commit provider API keys or access tokens.
- Never embed ComfyUI credentials in frontend JavaScript.
- Validate uploaded images by MIME type and size at the backend.
- Keep generated files outside the Git repository.
- Use HTTPS for remote backends.
- Configure CORS to the deployed frontend origin in production instead of `*`.
