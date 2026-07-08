
import requests
import json

BASE_URL = "https://repo-pilot-ai-tau.vercel.app/"
# Test data
repo_data = {
    'name': 'test-repo',
    'owner': 'test-user',
    'description': 'A test repository with awesome features',
    'url': 'https://github.com/test-user/test-repo',
    'language': 'Python',
    'topics': ['test', 'api'],
    'stars': 100,
    'forks': 10,
    'license': 'MIT',
    'homepage': 'https://test-repo.com',
    'visibility': 'Public'
}
