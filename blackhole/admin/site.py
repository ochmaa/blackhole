from jinja2 import Environment, PackageLoader

MEDIA_PATH = 'admin/static_files/'

# jinja template loader
template_env = Environment(loader=PackageLoader('blackhole.admin'))

