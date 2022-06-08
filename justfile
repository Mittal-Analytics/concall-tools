gh:
    open "https://github.com/Mittal-Analytics/concall-tools/pulls?q=is%3Apr+is%3Aopen+sort%3Aupdated-desc"

test-all:
    python -m unittest

test TEST:
    python -m unittest -k {{TEST}}
