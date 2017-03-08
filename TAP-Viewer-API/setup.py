import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))


# better to use:
# conda install --file conda_requirements
# or
# pip install -r requiremrents.txt
# rather than havin setuptools pull this stuff in..

requires = []
# requires = ['pyramid',
#             'pyramid_debugtoolbar',
#             'waitress',
#             ]


setup(name='TAP-Viewer-API',
      version='0.0',
      description='tap-viewer',
      #long_description=README + '\n\n' + CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='',
      author_email='',
      url='',
      keywords='web pyramid pylons',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      # install_requires=requires,
      # tests_require=requires,
      # test_suite="tapviewer",
      entry_points="""\
      [paste.app_factory]
      main = tap_viewer_api:main
      """,
      )
