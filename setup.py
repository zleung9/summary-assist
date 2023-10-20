from setuptools import setup, find_packages

setup(name='transcribe',
      version='0.0.0',
      description="Transcribe and summrize audio using ChatGPT",
      license='See license',
      packages=find_packages(),
      # python_requires=">=3.8",
      install_requires=[
         'whisper',
         'pydub',
         "numpy"
     ],
     entry_points={ # create scripts and add to sys.PATH
        'console_scripts': [
            'transcribe = transcribe.audio-to-text:main',
        ],
    },
)