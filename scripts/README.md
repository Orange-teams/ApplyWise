## `scripts/`

The `scripts/` directory contains utility scripts that support development and operational workflows in ApplyWise.

### Contents:

- Scripts to import/export job applications
- Data cleaning or migration scripts for user/job data
- Setup scripts for initializing the database
- Automation scripts for testing job scraping or parsing
- Maintenance utilities (reset data, seed demo accounts)

### Directory Structure:
<!-- BEGIN TREE -->
```text
├── db
│   ├── cv_insert.py
│   ├── init_db.py
│   ├── reset_db.py
│   └── seed_db.py
├── update_readme
│   ├── tree_utils.py
│   ├── update_all_readmes.py
│   └── update_readme.py
└── README.md
```
<!-- END TREE -->


### Purpose:

Automates repetitive tasks and simplifies managing job application data and system setup.