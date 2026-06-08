# EduToolsHub

Educational productivity platform that combines study management tools, resource discovery, and workflow automation into a single web application.

**Live:** https://edutoolshub.onrender.com/

**Demo:** https://youtu.be/Fe0io0Mu53A

## Problem

Students often rely on multiple websites and applications to manage notes, track homework, organize tasks, search for learning resources, and perform simple academic workflows.

EduToolsHub brings these commonly used tools into a unified platform designed to simplify day-to-day learning activities.

## Features

### Study Management

#### Notes

* Create and organize study notes
* View detailed note content
* Delete and manage notes
* User-specific note storage

#### Homework Tracking

* Track assignments and deadlines
* Subject-based organization
* Completion status management
* Due date monitoring

#### Todo Management

* Personal task tracking
* Completion workflows
* Quick task creation
* User-specific organization

---

### Learning Resource Discovery

#### Wikipedia Search

* Article discovery
* Summary generation
* Direct resource access

#### Dictionary Lookup

* Definitions
* Pronunciations
* Example usage
* Synonym discovery
* Audio playback support

#### YouTube Search

* Educational video discovery
* Channel information
* View statistics
* Direct video access

#### Book Search

* Google Books integration
* Book descriptions
* Ratings and categories
* Preview links

---

### Utility Tools

#### Unit Converter

Supports common academic conversions:

* Yard ↔ Foot
* Pound ↔ Kilogram

#### Personal Dashboard

Provides a consolidated view of:

* Pending homework
* Outstanding tasks
* Upcoming work

## Architecture

EduToolsHub follows a server-side rendered architecture using Django.

### Core Components

* Authentication System
* Notes Management
* Homework Management
* Todo Management
* Resource Discovery Services
* Utility Tools
* User Dashboard

### External Integrations

* Wikipedia
* Dictionary API
* Google Books API
* YouTube Search

### Reliability Features

* Request timeout handling
* Retry mechanisms
* Response caching
* Input validation
* Graceful fallback handling

## Tech Stack

### Backend

* Python
* Django

### Frontend

* HTML
* CSS
* Bootstrap 5
* Django Templates

### Forms & Validation

* Django Forms
* django-crispy-forms

### External Services

* Wikipedia
* Google Books API
* Dictionary API
* YouTube Search

## Data Model

### Notes

```text
title
description
user
```

### Homework

```text
subject
title
description
due
is_finished
user
```

### Todo

```text
title
is_finished
user
```

## Key Engineering Highlights

* Integrated 4 external service APIs into a unified platform.
* Implemented timeout boundaries and fallback handling for unreliable external services.
* Built layered input validation across forms, services, and data models.
* Added caching and retry strategies to improve API reliability.
* Developed a user-scoped dashboard experience for personalized workflows.

## Local Development

```bash
git clone https://github.com/kvdhanush06/EduToolsHub.git

cd EduToolsHub

pip install -r requirements.txt

python manage.py migrate

python manage.py runserver
```
