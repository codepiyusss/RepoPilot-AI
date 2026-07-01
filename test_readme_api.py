
import requests
import json

BASE_URL = "http://localhost:5000"

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

# Test 2: Missing repo_data
print('Test 2: POST /api/generate-readme - Missing repo_data')
response = requests.post(
    f'{BASE_URL}/api/generate-readme',
    json={}
)
assert response.status_code == 400, f"Expected 400, got {response.status_code}"
data = response.json()
assert 'error' in data, "Expected error message"
print(f'  Error: {data["error"]}')
print('  ✓ PASS\n')

# Test 3: Generate with JavaScript repo
print('Test 3: POST /api/generate-readme - JavaScript Project')
js_repo_data = repo_data.copy()
js_repo_data['language'] = 'JavaScript'
js_repo_data['name'] = 'awesome-js-lib'
response = requests.post(
    f'{BASE_URL}/api/generate-readme',
    json={'repo_data': js_repo_data}
)
assert response.status_code == 200, f"Expected 200, got {response.status_code}"
data = response.json()
assert data.get('success') == True, "Expected success=True"
readme_content = data.get('readme', '')
assert 'npm install' in readme_content or 'npm' in readme_content, "README should mention npm"
print(f'  Generated JavaScript-specific README: {len(readme_content)} characters')
print(f'  Contains npm installation instructions')
print('  ✓ PASS\n')

# Test 4: Generate with Java repo
print('Test 4: POST /api/generate-readme - Java Project')
java_repo_data = repo_data.copy()
java_repo_data['language'] = 'Java'
java_repo_data['name'] = 'java-framework'
response = requests.post(
    f'{BASE_URL}/api/generate-readme',
    json={'repo_data': java_repo_data}
)
assert response.status_code == 200, f"Expected 200, got {response.status_code}"
data = response.json()
assert data.get('success') == True, "Expected success=True"
readme_content = data.get('readme', '')
assert 'mvn' in readme_content or 'Maven' in readme_content or 'gradle' in readme_content, "README should mention Java build tools"
print(f'  Generated Java-specific README: {len(readme_content)} characters')
print(f'  Contains Maven/Gradle build instructions')
print('  ✓ PASS\n')

print('=' * 60)
print('All README Generator API tests passed! ✓')
print('=' * 60)
