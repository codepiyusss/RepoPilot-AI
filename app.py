from flask import Flask, render_template, jsonify, request
import requests
import re
from datetime import datetime
from urllib.parse import urlparse
from services.readme_generator import generate_readme

app = Flask(__name__)

handler = app

# GitHub API Configuration
GITHUB_API_BASE = "https://api.github.com"


# Helper Functions

def validate_github_url(url):

    if not url or not isinstance(url, str):
        return {'valid': False, 'error': 'Invalid URL format'}
    
    url = url.strip()
    
    # Pattern to match GitHub URLs
    pattern = r'^(?:https?://)?(?:www\.)?github\.com/([a-zA-Z0-9_-]+)/([a-zA-Z0-9_.-]+?)(?:\.git)?/?$'
    match = re.match(pattern, url)
    
    if not match:
        return {'valid': False, 'error': 'Invalid GitHub URL format. Use: github.com/owner/repo'}
    
    owner, repo = match.groups()
    return {'valid': True, 'owner': owner, 'repo': repo}


def fetch_repository_data(owner, repo):
    try:
        url = f"{GITHUB_API_BASE}/repos/{owner}/{repo}"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 404:
            return {'error': 'Repository not found', 'status': 404}
        elif response.status_code == 403:
            return {'error': 'API rate limit exceeded. Please try again later', 'status': 403}
        elif response.status_code != 200:
            return {'error': f'GitHub API error: {response.status_code}', 'status': response.status_code}
        
        return {'data': response.json(), 'status': 200}
        
    except requests.exceptions.Timeout:
        return {'error': 'Request timeout. Please check your connection', 'status': 408}
    except requests.exceptions.RequestException as e:
        return {'error': f'Network error: {str(e)}', 'status': 500}


def extract_repo_info(repo_data):
    try:
        created_at = datetime.fromisoformat(repo_data.get('created_at', '').replace('Z', '+00:00'))
        updated_at = datetime.fromisoformat(repo_data.get('updated_at', '').replace('Z', '+00:00'))
        
        return {
            'name': repo_data.get('name', 'Unknown'),
            'owner': repo_data.get('owner', {}).get('login', 'Unknown'),
            'url': repo_data.get('html_url', '#'),
            'description': repo_data.get('description') or 'No description provided',
            'language': repo_data.get('language') or 'Unknown',
            'stars': repo_data.get('stargazers_count', 0),
            'forks': repo_data.get('forks_count', 0),
            'watchers': repo_data.get('watchers_count', 0),
            'open_issues': repo_data.get('open_issues_count', 0),
            'created_at': created_at.strftime('%B %d, %Y'),
            'updated_at': updated_at.strftime('%B %d, %Y'),
            'topics': repo_data.get('topics', []),
            'license': repo_data.get('license', {}).get('name') if repo_data.get('license') else 'No license',
            'homepage': repo_data.get('homepage') or 'N/A',
            'owner_avatar': repo_data.get('owner', {}).get('avatar_url', ''),
            'visibility': 'Public' if not repo_data.get('private') else 'Private'
        }
    except Exception as e:
        return {'error': f'Error processing repository data: {str(e)}'}


# Routes

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/api/analyze', methods=['POST'])
def analyze_repository():
    data = request.get_json()
    
    if not data or 'url' not in data:
        return jsonify({'error': 'No repository URL provided'}), 400
    
    # Validate URL
    validation = validate_github_url(data['url'])
    if not validation['valid']:
        return jsonify({'error': validation['error']}), 400
    
    owner = validation['owner']
    repo = validation['repo']
    
    # Fetch repository data
    fetch_result = fetch_repository_data(owner, repo)
    if 'error' in fetch_result:
        return jsonify({'error': fetch_result['error']}), fetch_result.get('status', 500)
    
    # Extract relevant information
    repo_info = extract_repo_info(fetch_result['data'])
    if 'error' in repo_info:
        return jsonify(repo_info), 500
    
    return jsonify(repo_info), 200


@app.route('/results')
def results():
    return render_template('results.html')


@app.route('/api/generate-readme', methods=['POST'])
def api_generate_readme():
    try:
        data = request.get_json()
        
        if not data or 'repo_data' not in data:
            return jsonify({'error': 'No repository data provided'}), 400
        
        repo_data = data['repo_data']
        
        # Generate README using the service
        result = generate_readme(repo_data)
        
        if result['success']:
            return jsonify({
                'success': True,
                'readme': result['readme'],
                'message': result['message']
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': result.get('error', 'Unknown error'),
                'message': result.get('message', 'Failed to generate README')
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'An error occurred while generating README'
        }), 500


@app.route('/api/download-readme', methods=['POST'])
def api_download_readme():
    try:
        data = request.get_json()
        
        if not data or 'readme_content' not in data:
            return jsonify({'error': 'No README content provided'}), 400
        
        readme_content = data['readme_content']
        
        # Create response with file download
        from flask import Response
        return Response(
            readme_content,
            mimetype='text/markdown',
            headers={'Content-Disposition': 'attachment; filename=README.md'}
        )
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
