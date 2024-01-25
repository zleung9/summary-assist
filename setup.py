from setuptools import setup, find_packages

setup(name='news',
      version='1.2.0',
      description="Fetch and summarize news articles",
      license='See license',
      packages=find_packages(),
      python_requires=">=3.8",
      install_requires=[
         'whisper',
         'pydub',
         "numpy",
         "newspaper3k"
     ],
     entry_points={ # create scripts and add to sys.PATH
        'console_scripts': [
            'generate_news = news.generate_news:main',
            'publish_news = news.generate_news:publish'
        ],
    },
)