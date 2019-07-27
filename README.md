# KomaPy

Python library for creating customizable BPPTKG Monitoring API chart


## Requirements

* Python 3.5+
* numpy
* matplotlib
* pandas

KomaPy also depends on library developed at internal BPPTKG project:

* bmaclient


## Installation

Download the latest version from GitLab repository and unpack the archive:

    tar -xvf komapy-v0.1.0.tar.gz

Make Python virtual environment and activate the virtual environment:

    virtualenv -p python3 venv
    source venv/bin/activate

Install dependency packages:

    cd /path/to/komapy/
    pip install -r requirements.txt

Install `bmaclient` package. You can download the package from GitLab
repository:

    tar -xvf bmaclient-v0.0.2.tar.gz
    cd bmaclient-v0.0.2/
    pip install -r requirements.txt
    python setup.py install

Install the package:

    python setup.py install


## Documentation

See full documentation and tutorials at `docs/` directory.


## Contributing

See `CONTRIBUTING.md` to learn how to contribute to this project.


## Support

This project is maintained by Indra Rudianto. If you have any question about
this project, you can contact him at <indrarudianto.official@gmail.com>.


## License

By contributing to the project, you agree that your contributions will be
licensed under its MIT license.
See [LICENSE](https://gitlab.com/bpptkg/komapy/blob/master/LICENSE) for details.
