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

### Phase 2: Core Features
- [ ] GitHub API integration
- [ ] Repository analysis engine
- [ ] README generation
- [ ] Architecture visualization

### Phase 3: Advanced Features
- [ ] AI-powered insights
- [ ] Interview question generation
- [ ] Health score calculation
- [ ] Syntax analysis

## Usage

1. Navigate to the homepage
2. Enter a GitHub repository URL
3. Click "Analyze Repository"
4. View the generated reports and insights

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

**Current Version**: 1.0.0 (Foundation Release)
**Status**: In Development

For questions or support, please open an issue on GitHub.
