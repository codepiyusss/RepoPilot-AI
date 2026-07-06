
import requests

GITHUB_API_BASE = "https://api.github.com"


def fetch_default_branch(owner, repo):
    try:
        url = f"{GITHUB_API_BASE}/repos/{owner}/{repo}"
        response = requests.get(url, timeout=10)

        if response.status_code != 200:
            return {'error': f'GitHub API error: {response.status_code}', 'status': response.status_code}

        return {'branch': response.json().get('default_branch', 'main'), 'status': 200}

    except requests.exceptions.Timeout:
        return {'error': 'Request timeout. Please check your connection', 'status': 408}
    except requests.exceptions.RequestException as e:
        return {'error': f'Network error: {str(e)}', 'status': 500}


def fetch_repository_tree(owner, repo, branch):
    try:
        url = f"{GITHUB_API_BASE}/repos/{owner}/{repo}/git/trees/{branch}?recursive=1"
        response = requests.get(url, timeout=15)

        if response.status_code == 404:
            return {'error': 'Repository tree not found', 'status': 404}
        elif response.status_code == 403:
            return {'error': 'API rate limit exceeded. Please try again later', 'status': 403}
        elif response.status_code != 200:
            return {'error': f'GitHub API error: {response.status_code}', 'status': response.status_code}

        tree_data = response.json()

        # GitHub truncates very large trees. We still analyze what we have.
        paths = [item['path'] for item in tree_data.get('tree', []) if 'path' in item]

        return {'paths': paths, 'truncated': tree_data.get('truncated', False), 'status': 200}

    except requests.exceptions.Timeout:
        return {'error': 'Request timeout. Please check your connection', 'status': 408}
    except requests.exceptions.RequestException as e:
        return {'error': f'Network error: {str(e)}', 'status': 500}


class ArchitectureAnalyzer:

    FOLDER_KEYWORDS = {
        'frontend': ['frontend', 'client', 'web', 'ui', 'public'],
        'backend': ['backend', 'server'],
        'api': ['api', 'routes', 'endpoints', 'controllers'],
        'services': ['services', 'service'],
        'database': ['models', 'model', 'database', 'db', 'migrations', 'schema'],
        'templates': ['templates', 'views'],
        'static': ['static', 'assets'],
        'utils': ['utils', 'helpers', 'lib', 'common'],
        'tests': ['tests', 'test', '__tests__', 'spec'],
        'config': ['config', 'configs', 'settings'],
        'docs': ['docs', 'documentation'],
        'cli': ['cli', 'bin', 'scripts', 'commands'],
        'src': ['src', 'app', 'core'],
    }

    KNOWN_FOLDER_DESCRIPTIONS = {
        'templates': 'Contains HTML templates rendered by the backend.',
        'static': 'Contains CSS, JavaScript, images, and other static assets.',
        'services': 'Contains reusable backend logic, kept separate from routes.',
        'routes': 'Defines the application\'s API endpoints / URL routes.',
        'controllers': 'Handles incoming requests and coordinates responses.',
        'models': 'Defines the data structures and database schema.',
        'database': 'Handles database connections and queries.',
        'migrations': 'Tracks incremental changes to the database schema.',
        'utils': 'Holds small helper functions shared across the codebase.',
        'helpers': 'Holds small helper functions shared across the codebase.',
        'lib': 'Holds shared library code used by other parts of the project.',
        'tests': 'Contains automated tests for the project.',
        'test': 'Contains automated tests for the project.',
        'config': 'Stores configuration files and environment-specific settings.',
        'docs': 'Contains project documentation.',
        'src': 'Main source code directory for the application.',
        'app': 'Core application code.',
        'client': 'Frontend client application code.',
        'frontend': 'Frontend application code (UI).',
        'backend': 'Backend / server-side application code.',
        'components': 'Reusable UI components (frontend).',
        'public': 'Publicly served static files.',
        'assets': 'Images, fonts, and other static assets.',
        'cli': 'Command-line interface entry points and commands.',
        'bin': 'Executable scripts / CLI entry points.',
        'scripts': 'Standalone automation or utility scripts.',
        'api': 'Defines the REST API layer of the application.',
        '.github': 'GitHub configuration, including CI/CD workflows.',
    }

    ENTRY_POINT_FILES = [
        'app.py', 'main.py', 'manage.py', 'wsgi.py', 'asgi.py', 'run.py',
        'index.js', 'server.js', 'app.js', 'main.js', 'index.ts', 'main.go',
        'Main.java', 'Program.cs', 'index.php', 'artisan',
    ]

    CONFIG_FILES = [
        'requirements.txt', 'package.json', 'pyproject.toml', 'Pipfile',
        'Gemfile', 'pom.xml', 'build.gradle', 'go.mod', 'Cargo.toml',
        'composer.json', '.env.example', 'docker-compose.yml', 'Dockerfile',
        'vercel.json', 'tsconfig.json', 'webpack.config.js',
    ]

    def __init__(self, owner, repo, paths):
        self.owner = owner
        self.repo = repo
        self.paths = paths or []
        self.top_level_folders = self._extract_top_level_folders()
        self.root_files = self._extract_root_files()
        self.detected_layers = self._detect_layers()


    def _extract_top_level_folders(self):
        folders = set()
        for path in self.paths:
            if '/' in path:
                folders.add(path.split('/')[0])
        return sorted(folders)

    def _extract_root_files(self):
        return sorted([p for p in self.paths if '/' not in p])

    def _detect_layers(self):
        detected = {}
        for folder in self.top_level_folders:
            folder_lower = folder.lower()
            for layer, keywords in self.FOLDER_KEYWORDS.items():
                if folder_lower in keywords:
                    detected.setdefault(layer, []).append(folder)
                    break
        return detected

    def detect_framework(self):
        files = set(self.root_files)
        folders = set(f.lower() for f in self.top_level_folders)

        if 'manage.py' in files or 'settings.py' in self.paths:
            return 'Django'
        if 'requirements.txt' in files or 'app.py' in files or 'wsgi.py' in files:
            if 'templates' in folders and 'static' in folders:
                return 'Flask'
            return 'Python (Flask/Generic)'
        if 'artisan' in files:
            return 'Laravel'
        if 'Gemfile' in files and any(p.startswith('config/routes.rb') for p in self.paths):
            return 'Ruby on Rails'
        if 'next.config.js' in files or 'next.config.ts' in files:
            return 'Next.js'
        if 'angular.json' in files:
            return 'Angular'
        if 'package.json' in files:
            if any(p.endswith('App.jsx') or p.endswith('App.tsx') or p.endswith('App.js') for p in self.paths):
                return 'React'
            if any('vue' in p.lower() for p in self.paths):
                return 'Vue.js'
            return 'Node.js'
        if 'pom.xml' in files or 'build.gradle' in files:
            return 'Java (Spring/Maven/Gradle)'
        if 'go.mod' in files:
            return 'Go'
        if 'Cargo.toml' in files:
            return 'Rust'
        return 'Generic / Unrecognized Framework'

    def detect_entry_points(self):
        return [f for f in self.root_files if f in self.ENTRY_POINT_FILES]

    def detect_config_files(self):
        return [f for f in self.root_files if f in self.CONFIG_FILES]

    def has_database_layer(self):
        return 'database' in self.detected_layers

    def has_tests(self):
        return 'tests' in self.detected_layers

    def has_docs(self):
        return 'docs' in self.detected_layers or 'README.md' in self.root_files

    def has_frontend_backend_separation(self):
        return 'frontend' in self.detected_layers and 'backend' in self.detected_layers


    def build_architecture_summary(self):
        framework = self.detect_framework()
        entry_points = self.detect_entry_points()
        layers = self.detected_layers

        sentences = []
        sentences.append(
            f"This repository appears to be built with {framework}."
        )

        if entry_points:
            sentences.append(
                f"The application starts from {', '.join(entry_points)}."
            )

        if self.has_frontend_backend_separation():
            sentences.append(
                "The project separates frontend and backend code into distinct folders, "
                "which makes it easier to maintain each layer independently."
            )
        elif 'templates' in layers and 'static' in layers:
            sentences.append(
                "The backend renders HTML templates directly and serves static assets, "
                "following a traditional server-rendered web application structure."
            )
        elif 'api' in layers:
            sentences.append(
                "The project exposes functionality through an API layer, "
                "suggesting it is designed to serve other clients or services."
            )
        elif 'cli' in layers:
            sentences.append(
                "The project is organized around a command-line interface, "
                "with core logic kept separate from CLI entry points."
            )

        if 'services' in layers:
            sentences.append(
                "Reusable business logic is kept in a dedicated services layer, "
                "separating it from the main application routes."
            )

        if self.has_database_layer():
            sentences.append(
                "Data-related code (models, schema, or migrations) is organized "
                "into its own layer, separating it from application logic."
            )

        if self.has_tests():
            sentences.append("The project includes a dedicated folder for automated tests.")
        else:
            sentences.append(
                "No dedicated tests folder was detected, which may indicate limited "
                "automated test coverage."
            )

        return ' '.join(sentences)

    def build_layer_diagram(self):
        layers = self.detected_layers
        chain = []

        if 'frontend' in layers:
            chain.append(('Frontend', 'frontend'))
        elif 'templates' in layers or 'static' in layers:
            chain.append(('UI Templates', 'templates'))
        elif 'cli' in layers:
            chain.append(('CLI', 'cli'))

        framework = self.detect_framework()
        backend_label = framework if framework != 'Generic / Unrecognized Framework' else 'Backend'
        chain.append((backend_label, 'backend'))

        if 'api' in layers:
            chain.append(('API Layer', 'api'))

        if 'services' in layers:
            chain.append(('Services', 'services'))

        if self.has_database_layer():
            chain.append(('Database', 'database'))
        else:
            chain.append(('Data / Storage', 'storage'))

        if 'utils' in layers:
            chain.append(('Utilities', 'utils'))

        # Deduplicate while preserving order
        seen = set()
        unique_chain = []
        for label, key in chain:
            if key not in seen:
                seen.add(key)
                unique_chain.append(label)

        lines = ['flowchart TD']
        node_ids = [f'N{i}' for i in range(len(unique_chain))]

        for node_id, label in zip(node_ids, unique_chain):
            safe_label = label.replace('"', "'")
            lines.append(f'    {node_id}["{safe_label}"]')

        for i in range(len(node_ids) - 1):
            lines.append(f'    {node_ids[i]} --> {node_ids[i + 1]}')

        return '\n'.join(lines)

    def build_project_structure_explanation(self):
        explanations = []

        for folder in self.top_level_folders:
            folder_lower = folder.lower()
            description = self.KNOWN_FOLDER_DESCRIPTIONS.get(folder_lower)
            if description:
                explanations.append({'folder': f'{folder}/', 'description': description})

        # Fall back to a generic note if nothing recognizable was found.
        if not explanations and self.top_level_folders:
            for folder in self.top_level_folders[:6]:
                explanations.append({
                    'folder': f'{folder}/',
                    'description': 'Project folder (purpose not automatically recognized).'
                })

        return explanations

    def calculate_organization_score(self):
        score = 30  # baseline

        # Folder organization: any recognizable structure at all
        if self.detected_layers:
            score += 15

        # Separation of concerns: multiple distinct layers detected
        distinct_layers = len(self.detected_layers)
        if distinct_layers >= 4:
            score += 20
        elif distinct_layers >= 2:
            score += 12
        elif distinct_layers == 1:
            score += 5

        # Configuration present
        if self.detect_config_files():
            score += 10

        # Tests present
        if self.has_tests():
            score += 10

        # Documentation present
        if self.has_docs():
            score += 5

        # Naming consistency: folders should be lowercase, no spaces
        if self.top_level_folders:
            consistent = sum(
                1 for f in self.top_level_folders
                if f == f.lower() and ' ' not in f
            )
            consistency_ratio = consistent / len(self.top_level_folders)
            score += round(consistency_ratio * 10)

        return max(0, min(100, score))

    def build_recommendations(self):
        recommendations = []

        if not self.has_tests():
            recommendations.append('Add a tests folder to improve code reliability with automated tests.')

        if 'services' not in self.detected_layers and self.detect_framework() not in ('React', 'Vue.js', 'Next.js', 'Angular'):
            recommendations.append('Separate business logic into a dedicated services folder for better modularity.')

        if not self.detect_config_files():
            recommendations.append('Add a configuration or dependency file (e.g. requirements.txt, package.json) to document setup.')

        if not self.has_docs():
            recommendations.append('Add documentation (a docs folder or an expanded README) to help new contributors.')

        if len(self.detected_layers) < 2:
            recommendations.append('Improve separation of concerns by organizing code into clearer layers (e.g. routes, services, models).')

        if not recommendations:
            recommendations.append('The repository is well organized. Consider keeping documentation up to date as it grows.')

        return recommendations

    def analyze(self):
        try:
            return {
                'success': True,
                'framework': self.detect_framework(),
                'entry_points': self.detect_entry_points(),
                'summary': self.build_architecture_summary(),
                'diagram': self.build_layer_diagram(),
                'structure': self.build_project_structure_explanation(),
                'score': self.calculate_organization_score(),
                'recommendations': self.build_recommendations(),
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': 'Failed to analyze repository architecture'
            }


def analyze_repository_architecture(owner, repo):
    branch_result = fetch_default_branch(owner, repo)
    if 'error' in branch_result:
        return {'success': False, 'error': branch_result['error'], 'status': branch_result.get('status', 500)}

    tree_result = fetch_repository_tree(owner, repo, branch_result['branch'])
    if 'error' in tree_result:
        return {'success': False, 'error': tree_result['error'], 'status': tree_result.get('status', 500)}

    analyzer = ArchitectureAnalyzer(owner, repo, tree_result['paths'])
    result = analyzer.analyze()

    if not result['success']:
        result['status'] = 500
        return result

    result['truncated'] = tree_result.get('truncated', False)
    return result
