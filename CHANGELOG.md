# Changelog

All notable changes to the ParGaMD GUI project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Quick start script for easy installation
- Enhanced error handling and user feedback
- Improved documentation and examples

### Changed
- Updated dependencies to latest stable versions
- Improved code organization and structure

### Fixed
- Minor bug fixes and performance improvements

## [1.3.0] - 2024-01-21

### Added
- Complete ZIP export functionality with full directory structure
- Support for infinite bounds (`-inf` and `inf`) in progress coordinates
- Enhanced file preview with complete file content
- Dynamic NODELOC configuration in env.sh
- Template management for saving and loading configurations

### Changed
- Updated west.cfg template to render Python-style boundary lists
- Improved UI/UX with better error handling
- Enhanced configuration file templates with complete structures
- Removed SSH functionality to focus on local configuration

### Fixed
- File upload validation and handling
- Configuration preview display issues
- Template rendering for all configuration files
- Boundary generation for progress coordinates

## [1.2.0] - 2024-01-20

### Added
- ZIP download functionality for configuration files
- Enhanced configuration preview system
- Better error handling and user feedback
- Support for file upload validation

### Changed
- Improved UI responsiveness and design
- Enhanced JavaScript functionality
- Better parameter validation

### Fixed
- File upload issues and validation
- Configuration generation errors
- Preview display problems

## [1.1.0] - 2024-01-19

### Added
- Infinite bounds support for progress coordinates
- Enhanced configuration file templates
- Improved parameter management
- Better user interface design

### Changed
- Updated template structure for better maintainability
- Enhanced error handling
- Improved code organization

### Fixed
- Template rendering issues
- Parameter validation problems
- UI responsiveness issues

## [1.0.0] - 2024-01-18

### Added
- Initial release of ParGaMD GUI
- Web-based interface for ParGaMD configuration
- Support for all major configuration files (west.cfg, env.sh, runseg.sh, etc.)
- File upload functionality for PDB and PRMTOP files
- Real-time configuration preview
- Parameter management for WE and MD simulations
- GPU parallelization control
- Progress coordinate configuration

### Features
- Interactive parameter configuration
- Dynamic configuration file generation
- Template-based file generation
- Bootstrap-based responsive UI
- Flask backend with SocketIO support
- File validation and error handling

## [0.1.0] - 2024-01-17

### Added
- Initial development version
- Basic Flask application structure
- Template system for configuration files
- Frontend UI components

---

## Version History Summary

- **v1.3.0**: Complete ZIP export, infinite bounds support, enhanced templates
- **v1.2.0**: ZIP download, enhanced preview, better error handling
- **v1.1.0**: Infinite bounds, enhanced templates, improved UI
- **v1.0.0**: Initial stable release with full functionality
- **v0.1.0**: Initial development version

## Migration Guide

### From v1.2.0 to v1.3.0
- No breaking changes
- New infinite bounds feature is optional and enabled by default
- ZIP export now includes complete directory structure

### From v1.1.0 to v1.2.0
- No breaking changes
- Enhanced ZIP functionality
- Improved error handling

### From v1.0.0 to v1.1.0
- No breaking changes
- New infinite bounds feature added
- Enhanced template system

### From v0.1.0 to v1.0.0
- Major version release
- Complete feature set implemented
- Stable API and functionality
