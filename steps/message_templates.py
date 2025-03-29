# steps/message_templates.py

def format_library_open_error(plugin_path, dlopen_error):
    """
    Returns the expected error message when the plugin file is missing.

    Parameters:
        plugin_path (str): The path to the plugin.
        dlopen_error (str): The error message from dlopen.

    Returns:
        str: The formatted error message.
    """
    return (
        "Library couldn't be opened.\n"
        f"\tLibrary's path is {plugin_path}\n"
        f"\tdlopen: {plugin_path}: {dlopen_error}\n"
        "\tcheck plugins folder or rename library"
    )

def format_library_exec_error(function_name, plugin_name, plugin_path, dlsym_error):
    """
    Returns the expected error message when a required function is missing in the plugin.

    Parameters:
        function_name (str): The name of the missing function.
        plugin_name (str): The name of the plugin.
        dlsym_error (str): The error message from dlsym.

    Returns:
        str: The formatted error message.
    """
    return (
        f"Library couldn't execute {function_name}.\n"
        f"\tLibrary's name is {plugin_name}. Dlsym message: {plugin_path}: {dlsym_error}\n"
        "\tcheck plugins folder or rename library"
    )

