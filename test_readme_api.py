
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
print('=' * 60)
print('Testing README Generator API')
print('=' * 60)
print()

# Test 1: Generate README
print('Test 1: POST /api/generate-readme')
response = requests.post(
    f'{BASE_URL}/api/generate-readme',
    json={'repo_data': repo_data}
)
assert response.status_code == 200, f"Expected 200, got {response.status_code}"
data = response.json()
assert data.get('success') == True, "Expected success=True"
readme_content = data.get('readme', '')
assert len(readme_content) > 100, "README should have substantial content"
assert '# test-repo' in readme_content, "README should contain project title"
assert '## Installation' in readme_content, "README should contain Installation section"
assert '## Usage' in readme_content, "README should contain Usage section"
print(f'  Generated README: {len(readme_content)} characters')
print(f'  Contains all expected sections')
print('  ✓ PASS\n')

