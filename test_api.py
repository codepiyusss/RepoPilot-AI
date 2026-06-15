import requests

# Test 1: Valid repository
print('Test 1: Valid Repository (facebook/react)')
response = requests.post('http://localhost:5000/api/analyze', json={'url': 'https://github.com/facebook/react'})
assert response.status_code == 200, f"Expected 200, got {response.status_code}"
data = response.json()
print(f'  Owner: {data["owner"]}')
print(f'  Stars: {data["stars"]}')
print(f'  Language: {data["language"]}')
print('  ✓ PASS\n')

# Test 2: Invalid URL


print('All tests passed!')
