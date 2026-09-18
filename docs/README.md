# FFMPEG Python Helper Documentation

This directory contains the API documentation for FFMPEG Python Helper.

## Available Documentation Formats

### 1. Online Documentation
- **README.md**: Comprehensive user guide with examples (in project root)
- **API Reference**: This file contains detailed API documentation

### 2. Generated Documentation
To generate documentation locally:

```bash
# Generate all documentation formats
python scripts/generate_docs.py

# Generate HTML documentation only
python scripts/generate_docs.py html

# Generate Markdown API reference only
python scripts/generate_docs.py markdown

# Show console help
python scripts/generate_docs.py console
```

### 3. Interactive Documentation
You can access documentation directly in Python:

```python
# Module documentation
import ffmpeg_python_helper
help(ffmpeg_python_helper)

# Class documentation
from ffmpeg_python_helper import FFMPEG
help(FFMPEG)

# Method documentation
help(FFMPEG.execute)
help(FFMPEG.gif)
help(FFMPEG.trim)
help(FFMPEG.reformat)
```

## Documentation Structure

### Module Documentation (`ffmpeg_python_helper`)
- Package overview and installation
- Quick start examples
- Version information

### Class Documentation (`FFMPEG`)
- Complete class reference
- Constructor details
- All method signatures with parameters
- Return values and raised exceptions
- Usage examples for each method

### API Reference (`API_REFERENCE.md`)
- Complete Markdown version of all documentation
- Suitable for GitHub/GitLab viewing
- Includes all code examples

## Building HTML Documentation

If you have `pdoc3` installed, you can build HTML documentation:

```bash
# Install pdoc3
pip install pdoc3

# Generate HTML documentation
pdoc --html ffmpeg_python_helper --output-dir docs
```

The HTML documentation will be available at `docs/ffmpeg_python_helper.html`.

## Documentation Standards

All documentation follows these standards:

1. **Google-style docstrings**: Consistent formatting for all classes and methods
2. **Type hints**: Complete type annotations for better IDE support
3. **Examples**: Practical code examples for every method
4. **Error handling**: Clear documentation of raised exceptions
5. **Cross-references**: Links between related methods and classes

## Contributing to Documentation

When adding new features or modifying existing code:

1. Update docstrings in the source code
2. Add examples to the docstrings
3. Update the README.md if necessary
4. Run the documentation generator to update all formats
5. Test that `help()` works correctly with your changes

## Troubleshooting

### Documentation not updating
- Make sure you've saved your changes to source files
- Run the documentation generator script
- Check that docstrings follow the correct format

### Help() not showing documentation
- Ensure docstrings are properly formatted with triple quotes
- Check for syntax errors in docstrings
- Make sure the module is properly imported

### HTML generation issues
- Install pdoc3: `pip install pdoc3`
- Check Python version compatibility
- Ensure the module can be imported