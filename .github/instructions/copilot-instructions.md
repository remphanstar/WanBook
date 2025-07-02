<<<<<<< HEAD
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
=======
# GitHub Copilot Instructions for WanBook

## Project Overview
WanBook is a cloud-ready Jupyter notebook implementation for AI video generation using the Wan2GP system. When working on this project, follow these specific guidelines:

## Coding Standards

### General Guidelines
- **Descriptive Variables**: Use clear, descriptive variable names (e.g., `model_download_path` instead of `mdp`)
- **Error Handling**: Always include comprehensive error handling with try/catch blocks
- **Docstrings**: Add detailed docstrings for all complex functions
- **Cloud GPU Focus**: Assume cloud GPU environments - no local NVIDIA card assumptions
- **File Operations**: Prefer direct file editing over terminal commands when possible

### Python Specific
```python
# Good example:
def download_model_with_retry(model_url: str, destination_path: str, max_retries: int = 3) -> bool:
    """
    Download a model with retry logic and error handling.
    
    Args:
        model_url: URL of the model to download
        destination_path: Local path to save the model
        max_retries: Maximum number of retry attempts
    
    Returns:
        bool: True if download successful, False otherwise
    """
    for attempt in range(max_retries):
        try:
            # Download logic here
            return True
        except Exception as download_error:
            if attempt == max_retries - 1:
                print(f"Failed to download model after {max_retries} attempts: {download_error}")
                return False
            time.sleep(2 ** attempt)  # Exponential backoff
```

### Jupyter Notebook Guidelines
- **Never edit notebook JSON directly** - provide code cells in markdown code blocks
- Include clear progress indicators for long-running operations
- Add comprehensive error messages that help users troubleshoot
- Use markdown cells to explain complex operations

## Project Structure Management

### Required Files
Always maintain these files:
- `PROJECT_CONTEXT.md` - Project overview and architecture
- `CHANGELOG.md` - Version history and changes
- `requirements.txt` - Python dependencies
- `README.md` - Main documentation
- `.gitattributes` - Git LFS configuration for large files

### Documentation Updates
When making changes:
1. Update `CHANGELOG.md` with new features/fixes
2. Update `PROJECT_CONTEXT.md` if architecture changes
3. Update `README.md` if usage instructions change

## Cloud Platform Considerations

### Supported Platforms
- RunPod (primary target)
- Vast.ai
- Google Colab
- Paperspace Gradient
- AWS SageMaker

### Optimization Guidelines
- Implement model caching to avoid repeated downloads
- Use GPU memory management and cleanup
- Include automatic environment detection
- Provide fallback options for different cloud providers

## AI/ML Specific Guidelines

### Model Handling
```python
# Good practice for model loading
def load_model_safely(model_path: str, device: str):
    """Load model with proper error handling and memory management."""
    try:
        # Clear GPU cache before loading
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        
        model = ModelClass.from_pretrained(model_path)
        model = model.to(device)
        return model
    except Exception as e:
        print(f"Error loading model from {model_path}: {e}")
        return None
```

### GPU Memory Management
- Always clear CUDA cache before major operations
- Implement proper cleanup in finally blocks
- Monitor memory usage and provide warnings

## Error Handling Patterns

### Network Operations
```python
def download_with_fallback(primary_url: str, fallback_url: str):
    """Download with primary and fallback URL options."""
    for url in [primary_url, fallback_url]:
        try:
            # Download logic
            return True
        except Exception as e:
            print(f"Failed to download from {url}: {e}")
            continue
    return False
```

### File Operations
```python
def safe_file_operation(file_path: str):
    """Perform file operations with proper error handling."""
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None
    except PermissionError:
        print(f"Permission denied: {file_path}")
        return None
    except Exception as e:
        print(f"Unexpected error reading {file_path}: {e}")
        return None
```

## Testing and Validation

### Code Validation
- Test on multiple cloud platforms when possible
- Validate model downloads and loading
- Check GPU memory usage patterns
- Verify error recovery mechanisms

### User Experience
- Provide clear progress indicators
- Include helpful error messages
- Offer troubleshooting suggestions
- Test with various input types and sizes

## Version Control

### Commit Messages
- Use descriptive commit messages
- Reference issues when applicable
- Follow conventional commit format:
  - `feat:` for new features
  - `fix:` for bug fixes
  - `docs:` for documentation changes
  - `refactor:` for code improvements

### Branch Strategy
- Use feature branches for new development
- Keep main branch stable and deployable
- Test thoroughly before merging

## Security Considerations

### API Keys and Tokens
- Never hardcode API keys or tokens
- Use environment variables for sensitive data
- Provide clear instructions for users to set up their own keys

### File Handling
- Validate file paths and names
- Sanitize user inputs
- Implement appropriate access controls

## Performance Optimization

### Model Operations
- Implement lazy loading for large models
- Use appropriate batch sizes for GPU memory
- Optimize inference loops

### File I/O
- Use efficient file formats
- Implement streaming for large files
- Cache frequently accessed data

## User Support

### Documentation
- Include comprehensive setup instructions
- Provide troubleshooting guides
- Add FAQ sections for common issues

### Error Messages
- Make error messages actionable
- Include suggested solutions
- Provide context about what went wrong

---

These instructions should be followed when contributing to or maintaining the WanBook project. They ensure consistency, reliability, and user-friendliness across all cloud GPU platforms.
>>>>>>> 0857ca6e61c1a6379a5ab9e418c5fd47c08202c3
