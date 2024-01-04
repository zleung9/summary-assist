from setuptools import setup, find_packages

setup(name='article',
      version='0.0.0',
      description="Transcribe and summrize audio using ChatGPT",
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
            'transcribe = transcribe.transcribe:main',
        ],
    },
)