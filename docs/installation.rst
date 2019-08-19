============
Installation
============

KomaPy package is available on PyPI. You can install it by typing this command:

.. code-block:: bash

    pip install -U komapy

You can also install KomaPy from our GitLab repository. Download the latest
version from GitLab repository and unpack the archive:

.. code-block:: bash

    tar -xvf komapy-v<major>.<minor>.<patch>.tar.gz

Where ``major``, ``minor``, and ``patch`` are KomaPy semantic versioning number.
Then, make Python virtual environment and activate the virtual environment:

.. code-block:: bash

    virtualenv -p python3 venv
    source venv/bin/activate

Install dependency packages:

.. code-block:: bash

    cd /path/to/komapy/
    pip install -r requirements.txt

Install the package:

.. code-block:: bash

    pip install -e .
