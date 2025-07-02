---
applyTo: '**'
---

# Custom MCP Tool Set & Development Guidelines

Coding standards, domain knowledge, and preferences that AI should follow.

## Available MCP Tools
C:\Users\Greepo\Tools.toolsets.jsonc locate the tool set file here and always use it when needed.

### File System Operations
Prefer these over terminal commands:
- `read_file`, `read_multiple_files`, `write_file`, `edit_file`
- `create_directory`, `list_directory`, `directory_tree`
- `move_file`, `search_files`, `get_file_info`

### GitHub Integration
- `create_pull_request`, `create_issue`, `get_pull_request`
- `push_files`, `search_code`, `merge_pull_request`
- `get_file_contents`, `create_or_update_file`

### Browser Automation
- `initialize_browser`, `go_to_url`, `click_element`
- `take_screenshot`, `puppeteer_navigate`, `web_search_exa`

### Memory & Knowledge Management
- `add_memory`, `search_memory`, `write_note`, `search_notes`
- `create_entities`, `create_relations`, `read_graph`

### Development Environment
- `execute_cell`, `launch_colab`, `installPythonPackage`
- `configurePythonEnvironment`, `configureNotebook`

## Code Quality Requirements

### Direct File Editing
- Always use `edit_file` instead of terminal commands
- Fix issues by direct code modification, not additional test scripts
- Use `search_files` to locate issues across codebase

### Cloud GPU Environment Assumptions
- Code is designed for cloud GPU environments (Colab, Kaggle, etc.)
- User has NO local NVIDIA graphics cards
- Don't suggest local GPU testing or CUDA installations
- Assume remote execution for ML/AI workloads

### Notebook Handling
- NEVER edit notebook JSON directly
- Always provide notebook cells in markdown code blocks
- Use `execute_cell` for testing notebook code
- Format as: ```python for notebook cells

### Context Management
Maintain `PROJECT_CONTEXT.md` file containing:
- Current project overview and objectives
- Active issues and their status
- List of files being modified
- Dependencies and environment setup
- Known limitations and workarounds

### Changelog Requirements
Maintain `CHANGELOG.md` with entries for:
- Major code changes and fixes
- New features or functionality
- Bug fixes and their solutions
- Configuration changes
- Performance improvements

Format: `## [Date] - Description`

## Development Practices

### Avoid Terminal Commands
- Use MCP file-system tools instead of shell commands
- Direct file manipulation over command-line tools
- Prefer `installPythonPackage` over pip commands

### Code Organization
- Keep functions focused and single-purpose
- Use descriptive variable names
- Add docstrings for complex functions
- Organize imports at file top

### Error Handling
- Include try-catch blocks for file operations
- Provide meaningful error messages
- Log errors to help debugging

### Testing Strategy
- Test in cloud environments, not locally
- Use notebook cells for quick testing
- Validate with small datasets first

Always update PROJECT_CONTEXT.md and CHANGELOG.md when making significant changes.