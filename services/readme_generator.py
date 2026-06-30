
import os
from datetime import datetime


class ReadmeGenerator:
    def __init__(self, repo_data):

        self.repo_data = repo_data
        self.sections = {}

    def extract_repo_features(self):

        features = {
            'name': self.repo_data.get('name', 'Unknown'),
            'description': self.repo_data.get('description', ''),
            'owner': self.repo_data.get('owner', 'Unknown'),
            'url': self.repo_data.get('url', '#'),
            'language': self.repo_data.get('language', 'Unknown'),
            'topics': self.repo_data.get('topics', []),
            'stars': self.repo_data.get('stars', 0),
            'forks': self.repo_data.get('forks', 0),
            'license': self.repo_data.get('license', 'No license'),
            'homepage': self.repo_data.get('homepage', 'N/A'),
            'visibility': self.repo_data.get('visibility', 'Public'),
        }
        return features

    def build_project_summary(self):

        features = self.extract_repo_features()
        
        summary = f"# {features['name']}\n\n"
        
        # Add badges
        badges = []
        if features['visibility'] == 'Public':
            badges.append('![License](https://img.shields.io/badge/License-MIT-green.svg)')
        if features['language'] and features['language'] != 'Unknown':
            badges.append(f'![Language]'
                         f'(https://img.shields.io/badge/Language-{features["language"]}-blue.svg)')
        if features['stars'] > 0:
            badges.append(f'![Stars]'
                         f'(https://img.shields.io/badge/Stars-{features["stars"]}-yellow.svg)')
        
        if badges:
            summary += ' '.join(badges) + '\n\n'
        
        # Add description
        if features['description']:
            summary += f"{features['description']}\n\n"
        else:
            summary += "A comprehensive GitHub repository with useful features.\n\n"
        
        return summary

    def create_installation_section(self):

        features = self.extract_repo_features()
        language = features['language']
        owner = features['owner']
        name = features['name']
        
        installation = "## Installation\n\n"
        
        # Provide language-specific installation instructions
        if language == 'Python':
            installation += "### Prerequisites\n"
            installation += "- Python 3.7 or higher\n"
            installation += "- pip (Python package manager)\n\n"
            installation += "### Steps\n\n"
            installation += "1. Clone the repository:\n"
            installation += "```bash\n"
            installation += f"git clone https://github.com/{owner}/{name}.git\n"
            installation += f"cd {name}\n"
            installation += "```\n\n"
            installation += "2. Install dependencies:\n"
            installation += "```bash\n"
            installation += "pip install -r requirements.txt\n"
            installation += "```\n\n"
            installation += "3. Run the application:\n"
            installation += "```bash\n"
            installation += "python app.py\n"
            installation += "```\n"
            
        elif language == 'JavaScript':
            installation += "### Prerequisites\n"
            installation += "- Node.js (v14 or higher)\n"
            installation += "- npm or yarn\n\n"
            installation += "### Steps\n\n"
            installation += "1. Clone the repository:\n"
            installation += "```bash\n"
            installation += f"git clone https://github.com/{owner}/{name}.git\n"
            installation += f"cd {name}\n"
            installation += "```\n\n"
            installation += "2. Install dependencies:\n"
            installation += "```bash\n"
            installation += "npm install\n"
            installation += "# or\n"
            installation += "yarn install\n"
            installation += "```\n\n"
            installation += "3. Run the project:\n"
            installation += "```bash\n"
            installation += "npm start\n"
            installation += "```\n"
        elif language == 'Java':
            installation += "### Prerequisites\n"
            installation += "- Java Development Kit (JDK) 8 or higher\n"
            installation += "- Maven or Gradle\n\n"
            installation += "### Steps\n\n"
            installation += "1. Clone the repository:\n"
            installation += "```bash\n"
            installation += f"git clone https://github.com/{owner}/{name}.git\n"
            installation += f"cd {name}\n"
            installation += "```\n\n"
            installation += "2. Build the project:\n"
            installation += "```bash\n"
            installation += "mvn clean build\n"
            installation += "# or\n"
            installation += "gradle build\n"
            installation += "```\n\n"
            installation += "3. Run the application:\n"
            installation += "```bash\n"
            installation += "java -jar target/application.jar\n"
            installation += "```\n"
        else:
            installation += "### Prerequisites\n"
            installation += "- Appropriate runtime/tools for the project language\n\n"
            installation += "### Steps\n\n"
            installation += "1. Clone the repository:\n"
            installation += "```bash\n"
            installation += f"git clone https://github.com/{owner}/{name}.git\n"
            installation += f"cd {name}\n"
            installation += "```\n\n"
            installation += "2. Follow the project-specific setup instructions in the documentation.\n"
        
        return installation

    def create_usage_section(self):

        features = self.extract_repo_features()
        repo_name = features['name']
        
        usage = "## Usage\n\n"
        usage += "### Quick Start\n\n"
        
        if features['language'] == 'Python':
            py_name = repo_name.lower().replace('-', '_')
            usage += "```python\n"
            usage += f"from {py_name} import main\n\n"
            usage += "# Example usage\n"
            usage += "result = main()\n"
            usage += "print(result)\n"
            usage += "```\n"
        elif features['language'] == 'JavaScript':
            js_name = repo_name.replace('-', '')
            usage += "```javascript\n"
            usage += f"const {js_name} = require('./{repo_name}');\n\n"
            usage += "// Example usage\n"
            usage += f"const result = {js_name}.process();\n"
            usage += "console.log(result);\n"
            usage += "```\n"
        else:
            usage += "Please refer to the project documentation for usage examples and API reference.\n\n"
            usage += "For more detailed usage information, check the `docs` folder or the project's official documentation.\n"
        
        usage += "\n### Configuration\n\n"
        usage += "Create a configuration file (if required) and set up your environment variables.\n\n"
        
        return usage

    def create_features_section(self):

        features = self.extract_repo_features()
        
        features_section = "## Features\n\n"
        
        # Generate generic features based on repo info
        feature_list = []
        
        if features['language']:
            feature_list.append(f"Built with {features['language']}")
        
        if features['topics']:
            feature_list.append(f"Covers topics: {', '.join(features['topics'][:3])}")
        
        if features['stars'] > 100:
            feature_list.append("Popular and well-maintained")
        
        feature_list.extend([
            "Easy to install and setup",
            "Comprehensive documentation",
            "Active development and community support",
        ])
        
        for feature in feature_list:
            features_section += f"- {feature}\n"
        
        features_section += "\n"
        return features_section

    def create_tech_stack_section(self):

        features = self.extract_repo_features()
        
        tech_stack = "## Technology Stack\n\n"
        
        if features['language'] and features['language'] != 'Unknown':
            tech_stack += f"- **Primary Language**: {features['language']}\n"
        
        if features['topics']:
            tech_stack += f"- **Topics/Tags**: {', '.join(features['topics'][:5])}\n"
        
        tech_stack += "- **Package Manager**: npm/pip/maven (depending on language)\n"
        tech_stack += "- **Version Control**: Git\n"
        
        return tech_stack + "\n"

    def create_project_structure_section(self):

        name = self.repo_data.get('name', 'project')
        structure = "## Project Structure\n\n"
        structure += "```\n"
        structure += f"{name}/\n"
        structure += "├── README.md              # This file\n"
        structure += "├── LICENSE                # Project license\n"
        structure += "├── .gitignore             # Git ignore rules\n"
        structure += "├── requirements.txt       # Python dependencies (if applicable)\n"
        structure += "├── package.json           # Node.js configuration (if applicable)\n"
        structure += "├── src/                   # Source code directory\n"
        structure += "│   ├── main.py            # Main application file\n"
        structure += "│   └── utils.py           # Utility functions\n"
        structure += "├── tests/                 # Test directory\n"
        structure += "│   └── test_main.py       # Unit tests\n"
        structure += "├── docs/                  # Documentation\n"
        structure += "│   └── CONTRIBUTING.md    # Contribution guidelines\n"
        structure += "└── config/                # Configuration files\n"
        structure += "    └── settings.py        # Application settings\n"
        structure += "```\n\n"
        structure += "For more details, explore the repository structure.\n\n"
        return structure

    def create_contributing_section(self):
        features = self.extract_repo_features()
        
        contributing = "## Contributing\n\n"
        contributing += f"""We welcome contributions to {features['name']}! Here's how you can help:

### How to Contribute

1. **Fork the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/""" + features['name'] + """.git
   cd """ + features['name'] + """
   ```

2. **Create a new branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Write clean, well-documented code
   - Follow the existing code style
   - Add tests for new functionality

4. **Commit your changes**
   ```bash
   git commit -m "Add your meaningful commit message"
   ```

5. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Create a Pull Request**
   - Describe your changes clearly
   - Reference any related issues
   - Wait for review and feedback

### Reporting Issues

Found a bug? Have a suggestion? Please:
- Check existing issues first
- Provide clear description and steps to reproduce
- Include your environment details

### Code Style

Please follow these guidelines:
- Use consistent indentation (4 spaces)
- Write descriptive variable names
- Add docstrings to functions and classes
- Keep functions focused and modular

### Testing

- Write tests for new features
- Ensure all tests pass before submitting PR
- Aim for good code coverage

"""
        return contributing

    def create_license_section(self):
        """
        Generate license section
        
        Returns:
            str: Markdown formatted license section
        """
        features = self.extract_repo_features()
        license_name = features['license']
        
        license_section = "## License\n\n"
        
        if license_name and license_name != 'No license':
            license_section += f"""This project is licensed under the {license_name} License.
See the [LICENSE](LICENSE) file for details.

"""
        else:
            license_section += """This project is currently using no specific open-source license.
For licensing inquiries, please contact the project maintainers.

"""
        
        return license_section

    def create_contact_section(self):
        features = self.extract_repo_features()
        
        contact = "## Support & Contact\n\n"
        contact += f"""- **Repository**: [GitHub]({features['url']})
"""
        
        if features['homepage'] and features['homepage'] != 'N/A':
            contact += f"- **Website**: [{features['homepage']}]({features['homepage']})\n"
        
        contact += """- **Issues**: Use the [Issues tab](https://github.com/""" + features['owner'] + "/" + features['name'] + """/issues) for bug reports and feature requests

"""
        return contact

    def format_markdown(self, sections_list=None):

        if sections_list is None:
            sections_list = [
                'summary',
                'features',
                'tech_stack',
                'installation',
                'usage',
                'structure',
                'contributing',
                'license',
                'contact'
            ]
        
        readme = ""
        
        section_methods = {
            'summary': self.build_project_summary,
            'features': self.create_features_section,
            'tech_stack': self.create_tech_stack_section,
            'installation': self.create_installation_section,
            'usage': self.create_usage_section,
            'structure': self.create_project_structure_section,
            'contributing': self.create_contributing_section,
            'license': self.create_license_section,
            'contact': self.create_contact_section,
        }
        
        for section in sections_list:
            if section in section_methods:
                try:
                    readme += section_methods[section]()
                except Exception as e:
                    print(f"Error generating {section}: {str(e)}")
        
        # Add footer
        readme += f"\n---\n\n*This README was auto-generated by RepoPilot AI on {datetime.now().strftime('%B %d, %Y')}*\n"
        
        return readme

    def generate(self):
        try:
            readme_content = self.format_markdown()
            return {
                'success': True,
                'readme': readme_content,
                'message': 'README generated successfully'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': 'Failed to generate README'
            }


def generate_readme(repo_data):

    generator = ReadmeGenerator(repo_data)
    return generator.generate()


def extract_features(repo_data):
    
    generator = ReadmeGenerator(repo_data)
    return generator.extract_repo_features()


def build_project_summary(repo_data):
    generator = ReadmeGenerator(repo_data)
    return generator.build_project_summary()


def create_installation_section(repo_data):
    generator = ReadmeGenerator(repo_data)
    return generator.create_installation_section()

def integrate_ai_provider(provider_name):

    # Placeholder for future AI provider integration
    providers = {
        'ollama': None,
        'deepseek': None,
        'llama': None,
        'gemini': None,
    }
    
    if provider_name in providers:
        return providers[provider_name]
    else:
        raise ValueError(f"Unknown AI provider: {provider_name}")


def enhance_readme_with_ai(readme_content, repo_data, ai_provider='gemini'):
    return readme_content
