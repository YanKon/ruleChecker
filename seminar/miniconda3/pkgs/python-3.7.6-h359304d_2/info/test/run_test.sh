

set -ex



python -V
python3 -V
2to3 -h
pydoc -h
python3-config --help
python -c "import sys; files = [f for f in sys.argv[2:] if b' -partition=none' in open(f, 'rb').read()]; assert len(files) == 0, files" ${PREFIX}/lib/*/*.py
python -c "import sysconfig; print(sysconfig.get_config_var('CC'))"
for f in ${CONDA_PREFIX}/lib/python*/_sysconfig*.py; do echo "Checking $f:"; if [[ `rg @ $f` ]]; then echo "FAILED ON $f"; cat $f; exit 1; fi; done
pushd tests
pushd distutils
python setup.py install -v -v
python -c "import foobar"
popd
pushd distutils.cext
python setup.py install -v -v
python -c "import greet; greet.greet('Python user')" | rg "Hello Python"
popd
pushd prefix-replacement
bash build-and-test.sh
popd
pushd cmake
cmake -GNinja -DPY_VER=3.7.6
popd
popd
exit 0
