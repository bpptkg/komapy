============
Installation
============

Download the latest version from GitLab repository and unpack the archive, for
example:

    tar -xvf komapy-v0.1.0.tar.gz

Make Python virtual environment and activate the virtual environment:

    virtualenv -p python3 venv
    source venv/bin/activate

Install dependency packages:

    cd /path/to/komapy/
    pip install -r requirements.txt

Install `bmaclient` package. You can download the package from GitLab
repository:

    tar -xvf bmaclient-v0.1.0.tar.gz
    cd bmaclient-v0.1.0/
    pip install -r requirements.txt
    python setup.py install

Install the package:

    python setup.py install
