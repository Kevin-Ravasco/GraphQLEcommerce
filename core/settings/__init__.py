from .base import * # NOQA

# we import settings accordingly
if DEBUG:
    from .development import * # NOQA
else:
    from .production import * # NOQA