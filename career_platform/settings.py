"""Legacy settings shim.

This keeps compatibility for imports that reference `career_platform.settings`.
Use the split settings modules in `config/settings/` for real configs.
"""

import os

environment = os.environ.get("ENVIRONMENT", "local").lower()
if environment == "production":
    from config.settings.production import *  # noqa: F401,F403
else:
    from config.settings.local import *  # noqa: F401,F403
