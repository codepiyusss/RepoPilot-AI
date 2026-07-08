
import sys
sys.path.insert(0, 'e:\\RepoPilotAI')

from services.readme_generator import generate_readme

# Sample repository data
sample_repo_data = {
    'name': 'awesome-project',
    'owner': 'john-doe',
    'description': 'An awesome open-source project for developers',
    'url': 'https://github.com/john-doe/awesome-project',
    'language': 'Python',
    'topics': ['python', 'api', 'web', 'rest'],
    'stars': 1250,
    'forks': 89,
    'license': 'MIT',
    'homepage': 'https://awesome-project.com',
    'visibility': 'Public'
}

