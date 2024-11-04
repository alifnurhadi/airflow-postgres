# Contributing to ETL Pipeline Project

Thank you for your interest in contributing to our ETL pipeline project! This guide will help you get started with contributions.

## Prerequisites

Before you begin, ensure you have the following installed:
- Docker and Docker Compose
- Python 3.9 or higher
- Git

## Setting Up Your Development Environment

1. Fork the repository
2. Clone your fork:
```bash
git clone https://github.com/alifnurhadi/airflow-postgres.git
cd project-name
```

3. Set up your local environment:
```bash
# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

# Install development dependencies
pip install -r requirements.txt
```

4. Start the development environment:
```bash
docker compose up --build
```

## Development Workflow

1. Create a new branch for your feature:
```bash
git checkout -b feature/your-feature-name
```

2. Follow the project structure:
just follow the current structure

3. Code Style Guidelines
- Follow PEP 8 standards
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Include type hints where applicable


## Submitting Changes

1. Commit your changes:
```bash
git add .
git commit -m "feat: add your feature description"
```

2. Push to your fork:
```bash
git push origin feature/your-feature-name
```

3. Open a Pull Request (PR)
- Use a clear PR title
- Include a description of changes
- Reference any related issues
- Ensure CI checks pass

## Getting Help

- Open an issue for bugs or feature requests
- Review existing issues and PRs before creating new ones

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Help others learn and grow
- Follow project conventions and guidelines

Thank you for contributing to our project! 🚀
