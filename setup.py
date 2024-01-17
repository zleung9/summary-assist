from setuptools import setup, find_packages

setup(name='news',
      version='0.0.1',
      description="summarize news articles",
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
        ],
    },
)