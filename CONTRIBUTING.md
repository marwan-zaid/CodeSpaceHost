# Contributing to Student Registration System

Thank you for your interest in contributing to the Student Registration System! This document provides guidelines for contributing to the project.

## Getting Started

1. Fork the repository on GitHub
2. Clone your forked repository locally
3. Set up the development environment
4. Create a new branch for your feature or bug fix

## Development Setup

### Prerequisites
- Python 3.11 or higher
- PostgreSQL database
- Git version control

### Environment Setup
1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   ```bash
   export DATABASE_URL=postgresql://username:password@localhost/dbname
   export SESSION_SECRET=your-secret-key
   ```

4. Initialize the database:
   ```bash
   python init_data.py
   ```

## Code Style Guidelines

### Python Code
- Follow PEP 8 style guidelines
- Use descriptive variable and function names
- Add docstrings to functions and classes
- Keep functions focused and concise
- Use type hints where appropriate

### HTML/Templates
- Use semantic HTML elements
- Follow Bootstrap 5 conventions
- Maintain consistent indentation (2 spaces)
- Use meaningful class names
- Include proper alt text for images

### CSS/Styling
- Prefer Bootstrap utility classes over custom CSS
- Use CSS variables for theming
- Maintain responsive design principles
- Follow mobile-first approach

## Making Changes

### Branching Strategy
- Create feature branches from `main`
- Use descriptive branch names: `feature/user-profile-edit` or `fix/login-validation`
- Keep branches focused on single features or fixes

### Commit Messages
Use clear, descriptive commit messages:
- Start with a verb in present tense
- Keep the first line under 50 characters
- Add detailed explanation if needed

Examples:
```
Add user profile editing functionality
Fix course enrollment validation bug
Update dashboard layout for mobile devices
```

### Code Changes
1. Write clean, readable code
2. Add appropriate comments
3. Include error handling
4. Update documentation if needed
5. Test your changes thoroughly

## Testing

Before submitting your changes:

1. Test all affected functionality manually
2. Verify responsive design on different screen sizes
3. Check for console errors in browser developer tools
4. Test with different user roles (student/admin)
5. Validate form inputs and error handling

### Test Scenarios
- User registration and login
- Course enrollment and withdrawal
- Admin functions (creating courses, managing students)
- Profile updates and data persistence
- Navigation and UI responsiveness

## Database Changes

If your changes involve database schema modifications:

1. Create appropriate migrations
2. Test with existing data
3. Document any breaking changes
4. Consider backward compatibility

## Security Considerations

When making changes that affect security:

- Validate all user inputs
- Use parameterized queries for database operations
- Implement proper access controls
- Hash passwords securely
- Protect against common vulnerabilities (XSS, CSRF, SQL injection)

## Documentation

Update documentation when you:
- Add new features
- Change existing functionality
- Modify installation or setup procedures
- Update API endpoints
- Change database schema

## Submitting Changes

### Pull Request Process
1. Push your changes to your forked repository
2. Create a pull request against the main repository
3. Provide a clear description of your changes
4. Link any related issues
5. Be responsive to feedback and make requested changes

### Pull Request Description
Include:
- Summary of changes made
- Motivation for the changes
- Testing performed
- Any breaking changes
- Screenshots for UI changes

## Code Review

All contributions go through code review:
- Be open to feedback and suggestions
- Respond promptly to review comments
- Make requested changes thoughtfully
- Ask questions if something is unclear

## Reporting Issues

When reporting bugs or suggesting features:

1. Check existing issues first
2. Use descriptive titles
3. Provide steps to reproduce bugs
4. Include system information when relevant
5. Add screenshots for UI issues

### Bug Report Template
```
**Description:**
Brief description of the issue

**Steps to Reproduce:**
1. Step one
2. Step two
3. Step three

**Expected Behavior:**
What should happen

**Actual Behavior:**
What actually happens

**Environment:**
- Browser: [e.g., Chrome 91.0]
- OS: [e.g., Windows 10]
- Python version: [e.g., 3.11.0]
```

## Questions and Support

If you have questions:
- Check the README.md file
- Search existing issues
- Create a new issue with the "question" label
- Be specific about what you need help with

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers and help them learn
- Focus on constructive feedback
- Maintain a professional tone
- Report inappropriate behavior

Thank you for contributing to the Student Registration System!