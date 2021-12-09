import pkg_resources

for ep in pkg_resources.iter_entry_points(group='pygems.demoplugin'):
    plugin = ep.load()
    plugin()
