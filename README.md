# RepoPilot AI

## Overview

RepoPilot AI is a GitHub Repository Analyzer that automatically analyzes repositories and generates comprehensive documentation, insights, and developer reports.

## Features

- **Repository Summary**: Quick overview of any GitHub repository
- **README Generator**: Automatically generate professional README files
- **Architecture Analyzer**: Visualize and understand project architecture
- **Syntax Checker**: Detect syntax issues and code problems
- **Interview Question Generator**: Generate technical interview questions based on codebase
- **Repository Health Score**: Get a comprehensive health assessment of the repository

## Tech Stack

- **Backend**: Python Flask
- **Frontend**: HTML, CSS, Vanilla JavaScript
- **Database**: SQLite (future)
- **Design**: Modern, responsive, dark mode

## Project Structure

```
RepoPilotAI/
├── app.py                 # Flask application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── static/
│   ├── css/
│   │   └── style.css     # Main stylesheet
│   └── js/
│       └── main.js       # Client-side JavaScript
├── templates/
│   ├── base.html         # Base template
│   ├── index.html        # Homepage
│   └── about.html        # About page
├── database/             # Database files (future)
└── uploads/              # Uploaded files (future)
```

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Steps

1. **Clone or navigate to the project directory**
   ```bash
   cd RepoPilotAI
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   ```

3. **Activate virtual environment**
   - **Windows:**
     ```bash
     venv\Scripts\activate
     ```
   - **macOS/Linux:**
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Access the application**
   - Open your browser and navigate to: `http://localhost:5000`

## Development Roadmap

### Phase 1: Foundation (Current)
- [x] Project structure setup
- [x] UI/UX design
- [x] Landing page
- [x] Navigation and footer
- [x] GitHub API integration
- [x] Repository data fetching
- [x] Results dashboard
- [x] Error handling and validation

### Phase 2: Core Features
- [x] GitHub API integration (Completed)
- [x] Repository information fetching (Completed)
- [x] Results dashboard with statistics (Completed)
- [ ] README generation
- [ ] Architecture visualization
- [ ] Code analysis

### Phase 3: Advanced Features
- [ ] AI-powered insights
- [ ] Interview question generation
- [ ] Health score calculation
- [ ] Syntax analysis

## Usage

1. Navigate to the homepage at `http://localhost:5000`
2. Enter a GitHub repository URL (e.g., `https://github.com/facebook/react` or `github.com/facebook/react`)
3. Click "Analyze Repository" button
4. View the generated dashboard with:
   - Repository overview with owner information
   - Statistics (stars, forks, watchers, open issues)
   - Repository details (language, license, dates, homepage)
   - Topics/tags associated with the repository

## API Endpoints

### POST `/api/analyze`
Analyze a GitHub repository and return its information.

**Request:**
```json
{
  "url": "https://github.com/owner/repository"
}
```

**Response (Success - 200):**
```json
{
  "name": "repository",
  "owner": "owner",
  "url": "https://github.com/owner/repository",
  "description": "Repository description",
  "language": "JavaScript",
  "stars": 1000,
  "forks": 100,
  "watchers": 1000,
  "open_issues": 50,
  "created_at": "January 01, 2020",
  "updated_at": "June 04, 2026",
  "topics": ["topic1", "topic2"],
  "license": "MIT License",
  "homepage": "https://example.com",
  "owner_avatar": "https://avatars.githubusercontent.com/...",
  "visibility": "Public"
}
```

**Response (Error - 400/404):**
```json
{
  "error": "Error message describing what went wrong"
}
```

## Browser Support

- Chrome/Chromium (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Design Philosophy

RepoPilot AI follows modern SaaS design principles:
- Dark mode for reduced eye strain
- Clean, professional interface
- Responsive design for all devices
- Smooth animations and transitions
- Developer-focused experience

## License

MIT License - Feel free to use this project for learning and development

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## Author

Created as a comprehensive GitHub Repository Analysis tool for developers and teams.

---

**Current Version**: 1.0.1 (Repository Analysis Release)
**Status**: Feature Complete - Phase 2 Core Features Implemented

## Implemented Features

✅ **Phase 2 Completion:**
- GitHub API integration with public API (no authentication needed)
- Repository URL validation (flexible formats)
- Comprehensive data extraction from GitHub
- Professional results dashboard
- Responsive design for all devices
- Error handling for invalid URLs, missing repos, and network issues
- API rate limit handling

## Testing

Run the verification script to test the implementation:
```bash
python verify_implementation.py
```

Run API tests:
```bash
python test_api.py
```

For questions or support, please open an issue on GitHub.
