"""List console_scripts entry points for all installed packages"""

from importlib import metadata
for ep in metadata.entry_points()['console_scripts']:
    print(f"name='{ep.name}', value='{ep.value}', module='{ep.module}', attr='{ep.attr}'")
