echo "hey there, this is my first pip package"

python -m pip install --user --upgrade setuptools wheel twine

python setup.py sdist bdist_wheel

python -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*

python -m twine upload --repository-url https://upload.pypi.org/legacy/ dist/*