echo "Running Pylint..."

source ./venv/bin/activate
find -type f -name '*.py' ! -path '*/venv/*' -exec pylint '{}' \;

echo "Pylint report complete."