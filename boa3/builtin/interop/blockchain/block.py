from boa3.builtin.type import UInt160


class Block:
    def __init__(self):
        self.hash: bytes = bytes()  # TODO: change to UInt256
        self.version: int = 0
        self.prev_hash: bytes = bytes()  # TODO: change to UInt256
        self.merkle_root: bytes = bytes()  # TODO: change to UInt256
        self.timestamp: int = 0
        self.index: int = 0
        self.next_consensus: UInt160 = UInt160()
        self.transactions_count: int = 0
