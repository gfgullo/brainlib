from setuptools import setup

setup(
    name='brainlib',
    version='0.0.4',
    description='Utility per il gioco Enigma',
    author='Spina Nico',
    author_email='spinanico93@gmail.com',
    url='https://github.com/SpinaNico/brainlib',
    packages=['brainlib',
              "brainlib.matches",
              "brainlib.users",
              "brainlib.message"],
    install_requires=[
        "flask",
        "firebase-admin",
        "google-cloud-firestore",
        " google-cloud-error-reporting"
    ]
     )
