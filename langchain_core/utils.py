"""Minimal utils module to support imports."""

def get_from_dict_or_env(data, key, env_var=None):
    """Get a value from a dict or environment variable."""
    if key in data:
        return data[key]
    if env_var:
        import os
        return os.environ.get(env_var)
    return None

