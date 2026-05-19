## `src/`

The `src/` directory contains the core implementation of ApplyWise — the main application logic.

### Contents:

- Backend services for managing job applications and user profiles
- API routes for creating, updating, and tracking applications
- AI/analysis modules for evaluating job postings and matching
- Frontend components for dashboards, job lists, and analytics views
- Utility functions for parsing job descriptions and normalizing data

### Directory Structure:
<!-- BEGIN TREE -->
```text
├── agents
├── constants
│   └── filters.py
├── core
│   └── exceptions.py
├── crawlers
│   ├── parsers
│   │   └── linkedin_job_description_parser.py
│   ├── base.py
│   └── linkedin.py
├── db
│   ├── repositories
│   │   ├── job_repo.py
│   │   ├── keyword_repo.py
│   │   └── user_repo.py
│   ├── base.py
│   ├── bootstrap.py
│   ├── init_db.py
│   ├── models.py
│   └── session.py
├── llms
│   ├── services
│   │   └── cv_tailor_service.py
│   ├── base.py
│   └── gemini_provider.py
├── models
│   └── job.py
├── prompts
│   └── prompts.yaml
├── resume
│   ├── compiler
│   │   └── latex_compiler.py
│   ├── storage
│   │   └── resume_storage.py
│   └── templates
│       └── master_resume.tex
├── services
│   ├── job_service.py
│   ├── storage_service.py
│   └── user_service.py
├── utils
│   ├── http.py
│   ├── logger.py
│   └── prompt_loader.py
├── workflows
│   ├── application_pipeline.py
│   └── cv_tailoring_pipeline.py
├── main.py
└── README.md
```
<!-- END TREE -->


### Purpose:

This is the heart of ApplyWise, where all job tracking, analysis, and user interaction logic is implemented.