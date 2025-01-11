from setuptools import setup, find_packages


setup(
    name ='exp-oven',
    version = '0.1',
    author = 'Yan XIA',
    author_email = '',
    packages = find_packages(),
    package_dir = { 'oven': 'oven' },
    description = 'Experiments monitor and notification utilities.',
    classifiers = [
            'Programming Language :: Python :: 3',
            'License :: OSI Approved :: MIT License',
            'Operating System :: OS Independent',
        ],
    python_requires = '>=3.8',
    install_requires = [
        'omegaconf',
        "requests",
    ],
    entry_points = {
        'console_scripts': [
            'oven = oven.__init__:cli_full',  # Full version of CLI.
            'bake = oven.__init__:cli_cmd',  # Shortcuts for baking a command.
            'ding = oven.__init__:cli_log',  # Shortcuts for logging.
        ],
    },
)