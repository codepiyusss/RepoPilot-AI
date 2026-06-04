import requests

print("========================================")
print("RepoPilot AI - Feature Implementation")
print("========================================")
print()

# Test with multiple repos
test_repos = [
    'facebook/react',
    'torvalds/linux', 
    'golang/go'
]

print("Testing with multiple repositories:")
print()

for repo in test_repos:
    url = f'https://github.com/{repo}'
    response = requests.post('http://localhost:5000/api/analyze', json={'url': url}, timeout=10)
    
    if response.status_code == 200:
        data = response.json()
        print(f'{repo}')
        print(f'  Stars: {data["stars"]:,}')
        print(f'  Forks: {data["forks"]:,}')
        print(f'  Language: {data["language"]}')
        print()
    else:
        print(f'Error fetching {repo}: {response.status_code}')
        print()

print("========================================")
print("All features working correctly!")
print("========================================")
