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
print('Test 2: Invalid URL Format')
response = requests.post('http://localhost:5000/api/analyze', json={'url': 'not-a-valid-url'})
assert response.status_code == 400, f"Expected 400, got {response.status_code}"
data = response.json()
print(f'  Error: {data["error"]}')
print('  ✓ PASS\n')

# Test 3: Repository not found
print('Test 3: Repository Not Found')
response = requests.post('http://localhost:5000/api/analyze', json={'url': 'https://github.com/nonexistent/repository12345'})
assert response.status_code == 404, f"Expected 404, got {response.status_code}"
data = response.json()
print(f'  Error: {data["error"]}')
print('  ✓ PASS\n')

# Test 4: No URL provided
print('Test 4: No URL Provided')
response = requests.post('http://localhost:5000/api/analyze', json={})
assert response.status_code == 400, f"Expected 400, got {response.status_code}"
data = response.json()
print(f'  Error: {data["error"]}')
print('  ✓ PASS\n')

# Test 5: URL without https
print('Test 5: URL Without Protocol')
response = requests.post('http://localhost:5000/api/analyze', json={'url': 'github.com/facebook/react'})
assert response.status_code == 200, f"Expected 200, got {response.status_code}"
data = response.json()
print(f'  Owner: {data["owner"]}')
print(f'  ✓ PASS\n')

print('All tests passed! ✓')
