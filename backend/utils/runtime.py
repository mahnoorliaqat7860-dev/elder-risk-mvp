import platform

IS_WINDOWS = platform.system() == "Windows"

# Backend timeout enabled only on Unix
ENABLE_BACKEND_TIMEOUT = not IS_WINDOWS
