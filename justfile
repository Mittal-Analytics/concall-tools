alias pu:= gh

gh:
    open "https://github.com/Mittal-Analytics/concall-tools/pulls?q=is%3Apr+is%3Aopen+sort%3Aupdated-desc"

test-all:
    python -m unittest

test TEST:
    python -Wa -m unittest -k {{TEST}}

release:
    bumpver update --minor
    python -m build
    twine upload dist/*
