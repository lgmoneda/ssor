from setuptools import setup

setup(name='ssor',
      version='0.1',
      description='Semantic Search for Org-Roam',
      py_modules=['ssor'],
      python_requires='>=3.7, <4',
      install_requires=[
          'adjustText==0.7.3',
          'langchain==0.0.101',
          'openai==0.27.0',
          'orgparse==0.3.2',
          'pandas==1.5.2',
          'sentence-transformers==2.2.2',
          'scikit-learn==1.1.3',
      ])
