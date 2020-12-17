from boa3.builtin.type import UInt160


class Transaction:
    def __init__(self):
        self.hash: bytes = bytes()  # TODO: Change bytes to UInt256
        self.version: bytes = bytes()
        self.nonce: int = 0
        self.sender: UInt160 = UInt160()
        self.system_fee: int = 0
        self.network_fee: int = 0
        self.valid_until_block: int = 0
        self.script: bytes = bytes()
