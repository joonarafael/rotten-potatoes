echo "Running PEP8..."

source ./venv/bin/activate
find -type f -name '*.py' ! -path '*/venv/*' -exec autopep8 --in-place --aggressive --aggressive '{}' \;

echo "Automated PEP8 formatting complete."