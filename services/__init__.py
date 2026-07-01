# Services Package
# This package contains modular services for RepoPilot AI

from .readme_generator import (
    generate_readme,
    extract_features,
    build_project_summary,
    create_installation_section,
    ReadmeGenerator
)

__all__ = [
    'generate_readme',
    'extract_features',
    'build_project_summary',
    'create_installation_section',
    'ReadmeGenerator'
]
