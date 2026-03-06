# ML CI/CD Pipeline Documentation

## Overview
This repository includes a comprehensive GitHub Actions CI/CD pipeline for machine learning projects.

## Pipeline Jobs

### 1. **Test** (test)
- Runs on multiple Python versions (3.8, 3.9, 3.10, 3.11)
- Executes pytest on all test files
- Generates code coverage reports
- Uploads coverage to Codecov

### 2. **Code Quality** (code-quality)
- Lints code with flake8
- Checks code formatting with black
- Performs pylint analysis
- Ensures code standards compliance

### 3. **Build** (build)
- Depends on test and code-quality jobs
- Builds Python distribution packages
- Uploads artifacts for 30 days

### 4. **Security Scan** (security-scan)
- Runs Bandit for security vulnerability detection
- Checks for known vulnerabilities with safety
- Provides security reports

## Trigger Events
- Push to `main` or `develop` branches
- Pull requests to `main` or `develop` branches

## Setup Instructions

### 1. Push to GitHub
```bash
git init
git add .
git commit -m "Initial commit with CI/CD pipeline"
git branch -M main
git remote add origin https://github.com/yourusername/your-repo.git
git push -u origin main
```

### 2. Configure GitHub Secrets (Optional)
If using Codecov for coverage reports:
- Go to Settings → Secrets and variables → Actions
- Add `CODECOV_TOKEN` if needed

### 3. Enable Actions
- Go to Actions tab in your GitHub repository
- Ensure GitHub Actions is enabled

## Local Testing

### Run Tests Locally
```bash
cd appgithubaction
pytest tests/ -v
```

### Run with Coverage
```bash
cd appgithubaction
pytest tests/ --cov=src --cov-report=html
```

### Check Code Quality
```bash
# Format with black
black src/ tests/

# Lint with flake8
flake8 src/

# Check with pylint
pylint src/
```

### Security Scanning
```bash
bandit -r src/
safety check
```

## Files Created/Modified

- `.github/workflows/ml-ci-cd.yml` - Main CI/CD pipeline configuration
- `pyproject.toml` - Python project configuration and tool settings
- This documentation file

## Requirements
- Python 3.8+
- Dependencies listed in `appgithubaction/requirements.txt`

## Adding More Tools
To extend the pipeline, add new jobs to `.github/workflows/ml-ci-cd.yml`:

Example: Adding Docker build
```yaml
docker-build:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v3
    - name: Build Docker image
      run: docker build -t myapp:latest .
```
