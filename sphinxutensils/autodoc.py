"""Autodoc
==========
"""
#1. Include `from sphinxutensils import setup` in your sphinx conf.py
#2. Add {autodoc} comments in docstrings
#3. Implement __autodoc__ classmethods

def process_docstring(app, what, name, obj, options, lines):
    """Process Docstring."""
    if what == 'class' and hasattr(obj, '__autodoc__') and '{autodoc}' in '\n'.join(lines):
        insert = obj.__autodoc__()
        for i, line in enumerate(lines):
            lines[i] = line.replace('{autodoc}', insert)

def setup(app):
    """Attach autodoc processing command to Sphinx."""
    app.connect('autodoc-process-docstring', process_docstring)
