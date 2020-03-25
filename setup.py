from setuptools import setup

setup(
    name='nextEpisodeCalendar',
    version='0.1',
    author='NikosSiak',
    description='Add air dates for your favorite series to your google calendar',
    packages=['nextEpisodeCalendar'],
    entry_points={
        'console_scripts': [
            'calendar = nextEpisodeCalendar.nextEpisode:main'
        ]
    },
    install_requires=[
        'google-api-python-client == 1.8.0',
        'google-auth-httplib2 == 0.0.3',
        'google-auth-oauthlib == 0.4.1',
        'beautifulsoup4 == 4.8.2',
    ]
)
