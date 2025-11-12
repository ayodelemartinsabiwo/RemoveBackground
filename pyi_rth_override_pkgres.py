# Override problematic pkg_resources runtime hook
# This hook runs before pyi_rth_pkgres.py and provides stub implementations

import sys

# Create stub modules to prevent import errors
class StubModule:
    def __getattr__(self, name):
        return StubModule()

    def __call__(self, *args, **kwargs):
        return StubModule()

# Install stub modules for problematic imports
stub_modules = [
    'jaraco',
    'jaraco.text',
    'jaraco.functools',
    'jaraco.context',
    'jaraco.classes',
    'more_itertools',
    'pkg_resources.py2_warn',
    'pkg_resources._vendor',
    'pkg_resources.extern',
]

for module_name in stub_modules:
    if module_name not in sys.modules:
        sys.modules[module_name] = StubModule()

# Also stub the entire jaraco package hierarchy
if 'jaraco' not in sys.modules:
    jaraco = StubModule()
    jaraco.text = StubModule()
    jaraco.functools = StubModule()
    jaraco.context = StubModule()
    jaraco.classes = StubModule()
    sys.modules['jaraco'] = jaraco
