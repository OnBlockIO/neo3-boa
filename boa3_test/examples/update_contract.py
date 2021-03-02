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
    meta.has_storage = True
    meta.is_payable = True
    return meta


# -------------------------------------------
# SETTINGS
# -------------------------------------------

OWNER = UInt160()
PREFIX_STORAGE = b'storage'


# -------------------------------------------
# Methods
# -------------------------------------------

@public
def update(nef_file: bytes, manifest: bytes):
    """
    Updates this smart contract
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
    if get(PREFIX_STORAGE) != b'':
        return False

    put(PREFIX_STORAGE, b'deployed')
    return True


@public
def put_storage(value: bytes):
    put(PREFIX_STORAGE, value)


@public
def get_storage() -> bytes:
    return get(PREFIX_STORAGE)
