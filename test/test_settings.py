from tagging_tracker.settings import *

# Remove authentication from tests
REST_FRAMEWORK = {
    **REST_FRAMEWORK,
    "DEFAULT_AUTHENTICATION_CLASSES": []
}
