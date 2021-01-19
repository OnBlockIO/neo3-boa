from typing import Any

from boa3.builtin import public

from boa3.builtin.interop.runtime import notify, get_time, check_witness, log, trigger


@public
def main(operation: str, arg: Any) -> Any:

    if operation == 'get_trigger':
        return trigger()

    elif operation == 'check_witness':
        return check_witness(arg)

    elif operation == 'get_time':
        return get_time

    elif operation == 'log':
        log(arg)
        return True

    elif operation == 'notify':
        notify(arg)
        return True

    return 'unknown'
