# Software Engineering Guidelines for Action-Items Project

## Core Principles

### YAGNI (You Aren't Gonna Need It)
- Build only what is needed for the current phase
- Do not implement features for future phases until explicitly requested
- Avoid over-engineering solutions with unnecessary abstractions
- Start with simple, working implementations before adding complexity
- Example: Don't build a database layer if file-based storage works for now

### DRY (Don't Repeat Yourself)
- Extract repeated logic into reusable functions
- Use configuration files for values used in multiple places
- Create utility modules for common operations (email parsing, API calls, etc.)
- Avoid copy-pasting code blocks—refactor into shared functions

### KISS (Keep It Simple, Stupid)
- Prefer straightforward implementations over clever ones
- Use standard library functions when available
- Avoid premature optimization
- Clear, readable code is better than "smart" code

## Python-Specific Guidelines

### Code Organization
- One class/major function per file when appropriate
- Group related functionality into modules
- Use `__init__.py` to expose public APIs
- Keep `main.py` minimal—it should orchestrate, not implement

### Type Hints
- Use type hints for all function signatures
- Helps catch bugs early and improves IDE support
- Example: `def fetch_emails(days: int) -> list[Email]:`

### Error Handling
- Use specific exceptions, not bare `except:`
- Fail fast with clear error messages
- Log errors with context for debugging
- Don't silently swallow exceptions

### Dependencies
- Keep dependencies minimal and well-justified
- Pin versions in `pyproject.toml` for reproducibility
- Prefer well-maintained, popular libraries
- Document why each dependency is needed

### Testing
- Write tests for complex business logic
- Focus on integration tests for API interactions
- Use pytest for test framework
- Mock external services (Gmail API, LLM APIs) in tests

## Project-Specific Guidelines

### API Keys & Secrets
- Never commit API keys or credentials
- Use environment variables or `.env` files (gitignored)
- Provide `.env.example` with dummy values
- Document required credentials in README

### Email Handling
- Always respect user privacy
- Don't log full email contents
- Implement rate limiting for API calls
- Handle pagination properly for large inboxes

### LLM Usage
- Cache LLM responses when possible to reduce costs
- Implement retry logic with exponential backoff
- Provide clear prompts with examples
- Handle token limits gracefully

### Output Files
- Use consistent markdown formatting
- Include timestamps in generated files
- Make output human-readable and actionable
- Don't overwrite previous outputs—use timestamped filenames

## Code Review Checklist

Before committing code, ensure:
- [ ] No hardcoded credentials or sensitive data
- [ ] Functions have type hints
- [ ] Error cases are handled appropriately
- [ ] No unnecessary dependencies added
- [ ] Code follows DRY principle
- [ ] Implementation matches current phase requirements (YAGNI)
- [ ] Variable and function names are descriptive
- [ ] Comments explain "why", not "what"

## Anti-Patterns to Avoid

- **Premature abstraction**: Don't create base classes until you have 3+ similar implementations
- **God objects**: Keep classes focused on single responsibilities
- **Magic numbers**: Use named constants for any non-obvious values
- **Deep nesting**: Refactor nested if/for blocks into separate functions
- **Monolithic functions**: Break down functions longer than 50 lines

## When in Doubt

1. Choose the simpler solution
2. Make it work, then make it better
3. Optimize only when there's a proven performance issue
4. Ask for clarification rather than assume requirements
