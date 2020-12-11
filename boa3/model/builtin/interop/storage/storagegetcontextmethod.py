from typing import Dict

from boa3.model.builtin.interop.storage.storagecontexttype import StorageContextType
from boa3.model.builtin.interop.interopmethod import InteropMethod
from boa3.model.variable import Variable


class StorageGetContextMethod(InteropMethod):

    def __init__(self, storage_context_type: StorageContextType):
        identifier = 'get_context'
        syscall = 'System.Storage.GetContext'
        args: Dict[str, Variable] = {}
        super().__init__(identifier, syscall, args, return_type=storage_context_type)

    @property
    def requires_storage(self) -> bool:
        return True

    @property
    def storage_context_hash(self) -> bytes:
        # TODO: refactor when default arguments are implemented
        return self._method_hash(self._storage_context)