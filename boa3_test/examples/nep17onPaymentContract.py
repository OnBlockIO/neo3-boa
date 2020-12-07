from typing import Any

from boa3.builtin import NeoMetadata, metadata, public
from boa3.builtin.contract import abort
from boa3.builtin.interop.runtime import check_witness, executing_script_hash
from boa3.builtin.interop.storage import get, put
from boa3.builtin.interop.crypto import hash160


# -------------------------------------------
# METADATA
# -------------------------------------------


@metadata
def manifest_metadata() -> NeoMetadata:
    """
    Defines this smart contract's metadata information
    """
    meta = NeoMetadata()
    meta.has_storage = True     # TODO: remove both attributions when test engine gets updated
    meta.is_payable = True
    return meta


# -------------------------------------------
# TOKEN SETTINGS
# -------------------------------------------


# Script hash of the contract owner
OWNER = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'

# Script hash of this smart contract
SMART_CONTRACT = executing_script_hash()
SUPPLY_KEY = 'totalSupply'

# Symbol of the accepted Token
TOKEN_SYMBOL = 'NEP17'

# Password that accepts a transfer to this address
TRANSFER_PASSWORD = hash160('password')

# Whether the contract was deployed or not
DEPLOYED = 'deployed'


# -------------------------------------------
# Methods
# -------------------------------------------


@public
def onPayment(from_address: bytes, amount: int, data: Any):
    if not isinstance(data, list) or not (data[0] == TOKEN_SYMBOL) or not (hash160(data[1]) == TRANSFER_PASSWORD):
        abort()


def get_address() -> bytes:
    """
    Gets the script hash corresponding with this smart contract address
    :return: this smart contract address
    :rtype: bytes
    """
    return SMART_CONTRACT


@public
def get_balance() -> int:
    """

    :return:
    :rtype: int
    """
    return get(SMART_CONTRACT).to_int()


@public
def verify() -> bool:
    """
    When this contract address is included in the transaction signature,
    this method will be triggered as a VerificationTrigger to verify that the signature is correct.
    For example, this method needs to be called when withdrawing token from the contract.

    :return: whether the transaction signature is correct
    """
    return check_witness(OWNER)


@public
def deploy() -> bool:
    """
    Initializes the storage when the smart contract is deployed.

    :return: whether the deploy was successful. This method must return True only during the smart contract's deploy.
    """
    if not check_witness(OWNER):
        return False

    if get(DEPLOYED).to_int() == 1:
        return False

    put(DEPLOYED, True)

    return True
