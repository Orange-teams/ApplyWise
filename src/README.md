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
│   ├── crawler.py
│   └── linkedin_germany_filtered.json
├── constants
│   └── filters.py
├── core
│   └── exceptions.py
├── crawlers
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
├── models
│   └── job.py
├── services
│   ├── job_service.py
│   ├── storage_service.py
│   └── user_service.py
├── utils
│   ├── http.py
│   └── logger.py
├── workers
│   └── job_description_worker.py
├── workflows
│   └── application_pipeline.py
├── main.py
└── README.md
```
<!-- END TREE -->


### Purpose:

This is the heart of ApplyWise, where all job tracking, analysis, and user interaction logic is implemented.