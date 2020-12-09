from typing import Dict, Any

from boa3.builtin import public


@public
def main() -> Dict[Any, int]:
    d = {
        'a': 1,
        'b': {'a': 2},
    }
    return d['b']
