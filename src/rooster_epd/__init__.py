from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version('rooster-epd')
except PackageNotFoundError:
    # Running from a source checkout that hasn't been installed
    __version__ = '0.0.0'
