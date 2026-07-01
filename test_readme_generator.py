
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

# Test README generation
print("=" * 60)
print("Testing README Generator")
print("=" * 60)
print()

result = generate_readme(sample_repo_data)

if result['success']:
    print("✓ README Generated Successfully!")
    print()
    print("README Content Preview (first 500 chars):")
    print("-" * 60)
    print(result['readme'][:500] + "...")
    print("-" * 60)
    print()
    print("Full README length:", len(result['readme']), "characters")
    print()
    print("✓ Test passed!")
else:
    print("✗ README Generation failed!")
    print("Error:", result.get('error', 'Unknown error'))
    sys.exit(1)
