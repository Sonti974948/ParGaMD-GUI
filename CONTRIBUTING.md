# Contributing to ParGaMD GUI

Thank you for your interest in contributing to ParGaMD GUI! This document provides guidelines and information for contributors.

## 🤝 How to Contribute

### Reporting Bugs
- Use the GitHub issue tracker
- Include a clear description of the bug
- Provide steps to reproduce the issue
- Include system information (OS, Python version, etc.)
- Attach relevant files or screenshots if applicable

### Suggesting Enhancements
- Use the GitHub issue tracker with the "enhancement" label
- Describe the feature and its benefits
- Provide use cases and examples
- Consider implementation complexity

### Code Contributions
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Make your changes
4. Add tests if applicable
5. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
6. Push to the branch (`git push origin feature/AmazingFeature`)
7. Open a Pull Request

## 🛠️ Development Setup

### Prerequisites
- Python 3.7 or higher
- Git
- A modern web browser

### Local Development
1. Clone your fork:
   ```bash
   git clone https://github.com/yourusername/ParGaMD-GUI.git
   cd ParGaMD-GUI
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the development server:
   ```bash
   python ui_app.py
   ```

4. Open http://localhost:5000 in your browser

## 📝 Code Style Guidelines

### Python
- Follow PEP 8 style guidelines
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions focused and concise
- Use type hints where appropriate

### JavaScript
- Use consistent indentation (2 or 4 spaces)
- Use meaningful variable names
- Add comments for complex logic
- Follow modern ES6+ conventions

### HTML/CSS
- Use semantic HTML elements
- Follow Bootstrap conventions
- Keep CSS organized and commented
- Use responsive design principles

## 🧪 Testing

### Running Tests
```bash
# Run all tests
python -m pytest

# Run with coverage
python -m pytest --cov=.

# Run specific test file
python -m pytest tests/test_ui_app.py
```

### Writing Tests
- Write tests for new features
- Ensure good test coverage
- Use descriptive test names
- Mock external dependencies

## 📋 Pull Request Guidelines

### Before Submitting
- [ ] Code follows style guidelines
- [ ] Tests pass
- [ ] Documentation is updated
- [ ] No new warnings or errors
- [ ] Feature is tested manually

### PR Description
- Describe the changes made
- Link to related issues
- Include screenshots for UI changes
- Mention any breaking changes

## 🏷️ Issue Labels

- `bug`: Something isn't working
- `enhancement`: New feature or request
- `documentation`: Improvements to documentation
- `good first issue`: Good for newcomers
- `help wanted`: Extra attention is needed
- `question`: Further information is requested

## 📞 Getting Help

- Check existing issues and discussions
- Join our community discussions
- Contact maintainers directly
- Review documentation

## 🎯 Areas for Contribution

### High Priority
- Bug fixes and stability improvements
- Documentation improvements
- Performance optimizations
- Security enhancements

### Medium Priority
- New features and enhancements
- UI/UX improvements
- Additional file format support
- Integration with other tools

### Low Priority
- Code refactoring
- Style improvements
- Additional examples
- Community outreach

## 📄 License

By contributing to ParGaMD GUI, you agree that your contributions will be licensed under the MIT License.

## 🙏 Recognition

Contributors will be recognized in:
- The project README
- Release notes
- GitHub contributors page
- Documentation

Thank you for contributing to ParGaMD GUI! 🚀
