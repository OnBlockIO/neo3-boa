from boa3.builtin import NeoMetadata, metadata, public
from boa3.builtin.interop.contract import update_contract
from boa3.builtin.interop.runtime import check_witness
from boa3.builtin.interop.storage import put, get
from boa3.builtin.type import UInt160


# -------------------------------------------
# METADATA
# -------------------------------------------

@metadata
def manifest_metadata() -> NeoMetadata:
    """
    Defines this smart contract's metadata information
    """
    meta = NeoMetadata()
    meta.author = "Mirella Medeiros, Ricardo Prado and Lucas Uezu. COZ in partnership with Simpli"
    meta.description = "Update Example"
    meta.email = "contact@coz.io"
    # meta.has_storage and meta.is_payable are no longer part of the current NEPs, therefore this contract should update
    # to the new NEPs
    meta.has_storage = True
    meta.is_payable = True
    return meta


# -------------------------------------------
# SETTINGS
# -------------------------------------------

# Owner's address
OWNER = UInt160()
# Storage's key
STORAGE_KEY = b'storage'


# -------------------------------------------
# Methods
# -------------------------------------------

@public
def update(nef_file: bytes, manifest: bytes):
    """
    Updates this smart contract. Only the owner can update this smart contract.

    :param nef_file: the updated contract's nef file
    :type nef_file: bytes
    :param manifest: the updated contract's manifest
    :type manifest: bytes
    :raise AssertionError: raised if this function was not invoked by the owner.
    """
    assert check_witness(OWNER)
    update_contract(nef_file, manifest)


@public
def deploy() -> bool:
    """
    Initializes the storage when the smart contract is deployed.

    :return: whether the deploy was successful. This method must return True only during the smart contract's deploy.
    """
    if not check_witness(OWNER):
        return False
    if get(STORAGE_KEY) != b'':
        return False

    put(STORAGE_KEY, b'deployed')
    return True


@public
def put_storage(value: bytes):
    """
    Puts a value in the storage using the only key available.

    :param value: the value that will be put in the storage
    :type value: bytes
    """
    # putting b'' in the storage is not possible, because it was used as the condition for the deploy
    if value != b'':
        put(STORAGE_KEY, value)


@public
def get_storage() -> bytes:
    """
    Gets the only value stored in the storage. This function is used to show that the storage will change after the
    update.

    :return: the value stored in the storage
    :rtype: bytes
    """
    return get(STORAGE_KEY)
