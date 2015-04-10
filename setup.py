from setuptools import setup
setup(name='distroshare_ubuntu_updater',
      version='1.0',
      description='Updates configuration files and packages',
      author='Hugh Greenberg',
      author_email='hugegreenbug@gmail.com',
      url='https://distroshare.com',
      packages=['distroshare_updater'],
      data_files=[('/usr/sbin', ['distroshare_updater/distroshare-updater'])]
)
