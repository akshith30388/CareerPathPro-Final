"""Legacy settings shim.

This keeps compatibility for imports that reference `career_platform.settings`.
Use the split settings modules in `career_platform/settings/` for real configs.
"""

import os

environment = os.environ.get('ENVIRONMENT', 'local')
if environment == 'production':
    from .settings.production import *  # noqa: F401,F403
else:
    from .settings.local import *  # noqa: F401,F403
