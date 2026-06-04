from flask import Flask, render_template, jsonify, request
import requests
import re
from datetime import datetime
from urllib.parse import urlparse

app = Flask(__name__)

# GitHub API Configuration
GITHUB_API_BASE = "https://api.github.com"


# ==================== Helper Functions ====================

def validate_github_url(url):
    """
    Validate GitHub repository URL
    
    Args:
        url (str): The GitHub URL to validate
        
    Returns:
        dict: {'valid': bool, 'owner': str, 'repo': str, 'error': str}
    """
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
    """
    Fetch repository data from GitHub API
    
    Args:
        owner (str): Repository owner username
        repo (str): Repository name
        
    Returns:
        dict: Repository data or error
    """
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
    """
    Extract relevant repository information from GitHub API response
    
    Args:
        repo_data (dict): Raw data from GitHub API
        
    Returns:
        dict: Extracted and formatted repository information
    """
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


# ==================== Routes ====================

@app.route('/')
def home():
    """Homepage route"""
    return render_template('index.html')


@app.route('/about')
def about():
    """About page route"""
    return render_template('about.html')


@app.route('/api/analyze', methods=['POST'])
def analyze_repository():
    """
    API endpoint to analyze a GitHub repository
    
    Expected JSON:
        {
            "url": "https://github.com/owner/repo"
        }
    
    Returns:
        JSON with repository information or error
    """
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
    """Results/Dashboard page"""
    return render_template('results.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
