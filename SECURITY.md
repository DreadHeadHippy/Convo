# Security Policy

## Supported Versions

We actively support the following versions of Convo:

| Version | Supported          |
| ------- | ------------------ |
| main    | :white_check_mark: |
| Latest release | :white_check_mark: |

## Reporting a Vulnerability

If you discover a security vulnerability in Convo, please report it responsibly:

### For Critical Security Issues

1. **Do NOT create a public issue**
2. Email the maintainer directly (create a private vulnerability report on GitHub)
3. Include:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

### For General Security Concerns

- Create an issue using the [security template]
- Mark it with the `security` label
- Provide as much detail as possible

## Security Considerations

### Convo Code Execution

- Convo programs run with the same permissions as the Python interpreter
- Be cautious when running untrusted Convo code
- Consider sandboxing when executing user-provided programs

### Discord Bot Security

When using Convo for Discord bots:

- **Never commit bot tokens** to version control
- Use environment variables or `.env` files for sensitive data
- Follow Discord's security best practices
- Validate all user inputs
- Implement rate limiting for bot commands

### File Operations

- Convo's file operations respect system permissions
- Be aware of path traversal risks with user-provided file paths
- Validate file paths and names before operations

## Best Practices

1. **Keep dependencies updated** - Regularly update Python and required packages
2. **Use virtual environments** - Isolate Convo installations
3. **Validate inputs** - Always validate user-provided data
4. **Principle of least privilege** - Run with minimal necessary permissions
5. **Review code** - Carefully review Convo programs before execution

## Response Timeline

- **Critical vulnerabilities**: Response within 24 hours
- **High severity**: Response within 3 days
- **Medium/Low severity**: Response within 1 week

We appreciate responsible disclosure and will work with security researchers to address issues promptly.
