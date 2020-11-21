from setuptools import setup

setup(name='quart_app',
      version='1.0.0',
      description='Quart Applicaton',
      url='https://github.com/xamorena/quart_app',
      author='Xavier AMORENA',
      author_email='xavier.amorena@labri.fr',
      license='MIT',
      packages=['quart_app'],
      install_requires=[
          'quart'
      ],
      zip_safe=False,
      scripts=['quart_app=quart_app.application'],
      entry_points={})
