## `config/`

The `config/` directory contains all configuration settings required to run ApplyWise across different environments (development, staging, production).

### In ApplyWise, this includes:

- Environment variables for API keys (e.g., job boards, LLM services)
- Database connection settings for storing applications and user data
- Feature flags for enabling/disabling AI analysis or reminders
- Logging configuration and runtime settings
- Service endpoints used by the backend and frontend

### Directory Structure:
<!-- BEGIN TREE -->
```text
├── README.md
└── settings.py
```
<!-- END TREE -->


### Purpose:

Ensures ApplyWise can be deployed flexibly while keeping sensitive or environment-specific values separate from the codebase.