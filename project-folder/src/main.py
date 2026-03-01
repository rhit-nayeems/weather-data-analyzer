"""
Main entrypoint for the weather analysis project.

This app now starts a GUI workflow instead of console prompts.
"""

from gui import launch_gui


def main():
    """Start the weather analysis GUI."""
    launch_gui()


if __name__ == "__main__":
    main()
