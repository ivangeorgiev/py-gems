"""List console_scripts entry points for all installed packages using pkg_resources"""
import pkg_resources

for ep in pkg_resources.iter_entry_points(group='console_scripts'):
    print(f"name='{ep.name}', module='{ep.module_name}', attr='{ep.attrs}'")
