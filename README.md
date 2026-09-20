# EduToolsHub — Educational Productivity & Workflow Platform

**EduToolsHub** is an educational productivity platform combining study management, learning-resource discovery, utility tools, and workflow automation in a single Django web application.

**Live:** https://edutoolshub.onrender.com/

**Demo:** https://youtu.be/Fe0io0Mu53A

**Repository:** https://github.com/kvdhanush06/EduToolsHub

## Problem

Students often rely on multiple websites and applications to manage notes, homework, tasks, learning resources, and academic workflows. EduToolsHub brings these functions into one application designed for day-to-day study productivity.

## Features

### Study Management

- Create and organize study notes
- Track assignments and deadlines
- Manage personal todos
- User-specific organization and dashboards

### Learning Resource Discovery

- Wikipedia article search and summaries
- Dictionary definitions, pronunciations, examples, and synonyms
- YouTube educational video discovery
- Google Books search, descriptions, ratings, and previews

### Utility Tools

- Academic unit conversions
- Consolidated dashboard for pending homework, tasks, and upcoming work

## Architecture

EduToolsHub follows a server-side rendered architecture using Django.

### Core Components

- Authentication System
- Notes Management
- Homework Management
- Todo Management
- Resource Discovery Services
- Utility Tools
- User Dashboard

### External Integrations

- Wikipedia
- Dictionary API
- Google Books API
- YouTube Search

### Reliability Features

- Request timeout handling
- Retry mechanisms
- Response caching
- Input validation
- Graceful fallback handling

## Tech Stack

- Python
- Django
- SQLite
- HTML/CSS
- Bootstrap 5
- Django Templates
- Django Forms
- django-crispy-forms

## Key Engineering Highlights

- Integrated four external service APIs into a unified platform.
- Implemented timeout boundaries and fallback handling for unreliable external services.
- Built layered validation across forms, services, and data models.
- Added caching and retry strategies for API reliability.
- Developed user-scoped dashboards for personalized workflows.

## Local Development

```bash
git clone https://github.com/kvdhanush06/EduToolsHub.git
cd EduToolsHub
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

---

## Product & Creator

EduToolsHub is a software product published by **Venkata Dhanush Kakarlamudi** under the AllKVD project portfolio.

- **Product:** https://edutoolshub.onrender.com/
- **Creator:** https://allkvd.dev/
- **Portfolio:** https://portfolio.allkvd.dev/
- **GitHub:** https://github.com/kvdhanush06
- **Resume:** https://drive.google.com/file/d/1NCT6ZCa_HfxCdScqI-1Q2yA6y2c7O-qA/view
