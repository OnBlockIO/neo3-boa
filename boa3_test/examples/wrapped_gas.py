from typing import Any, Union

from boa3.builtin import CreateNewEvent, NeoMetadata, metadata, public
from boa3.builtin.contract import Nep17TransferEvent, abort
from boa3.builtin.interop.blockchain import get_contract
from boa3.builtin.interop.contract import GAS, call_contract
from boa3.builtin.interop.runtime import calling_script_hash, check_witness, executing_script_hash
from boa3.builtin.interop.storage import delete, get, put
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
    meta.supported_standards = ['NEP-17']
    meta.author = "Mirella Medeiros, Ricardo Prado and Lucas Uezu. COZ in partnership with Simpli"
    meta.description = "Wrapped GAS Example"
    meta.email = "contact@coz.io"
    return meta


# -------------------------------------------
# TOKEN SETTINGS
# -------------------------------------------


# Script hash of the contract owner
OWNER = UInt160()
SUPPLY_KEY = 'totalSupply'

# Symbol of the Token
TOKEN_SYMBOL = 'zGAS'

# Number of decimal places
TOKEN_DECIMALS = 8

# Total Supply of tokens in the system
TOKEN_TOTAL_SUPPLY = 10_000_000 * 100_000_000  # 10m total supply * 10^8 (decimals)

# Allowance
ALLOWANCE_PREFIX = b'allowance'

# -------------------------------------------
# Events
# -------------------------------------------


on_transfer = Nep17TransferEvent
on_approval = CreateNewEvent(
    [
        ('owner', UInt160),
        ('spender', UInt160),
        ('amount', int)
    ],
    'Approval'
)


# -------------------------------------------
# Methods
# -------------------------------------------


@public
def symbol() -> str:
    """
    Gets the symbols of the token.

    This string must be valid ASCII, must not contain whitespace or control characters, should be limited to uppercase
    Latin alphabet (i.e. the 26 letters used in English) and should be short (3-8 characters is recommended).
    This method must always return the same value every time it is invoked.

    :return: a short string representing symbol of the token managed in this contract.
    """
    return TOKEN_SYMBOL


@public
def decimals() -> int:
    """
    Gets the amount of decimals used by the token.

    E.g. 8, means to divide the token amount by 100,000,000 (10 ^ 8) to get its user representation.
    This method must always return the same value every time it is invoked.

    :return: the number of decimals used by the token.
    """
    return TOKEN_DECIMALS


@public
def totalSupply() -> int:
    """
    Gets the total token supply deployed in the system.

    This number must not be in its user representation. E.g. if the total supply is 10,000,000 tokens, this method
    must return 10,000,000 * 10 ^ decimals.

    :return: the total token supply deployed in the system.
    """
    return get(SUPPLY_KEY).to_int()


@public
def balanceOf(account: UInt160) -> int:
    """
    Get the current balance of an address.

    The parameter account must be a 20-byte address represented by a UInt160.

    :param account: the account address to retrieve the balance for
    :type account: bytes
    """
    assert len(account) == 20
    return get(account).to_int()


@public
def transfer(from_address: UInt160, to_address: UInt160, amount: int, data: Any) -> bool:
    """
    Transfers an amount of zGAS tokens from one account to another.

    If the method succeeds, it must fire the `Transfer` event and must return true, even if the amount is 0,
    or from and to are the same address.

    :param from_address: the address to transfer from
    :type from_address: UInt160
    :param to_address: the address to transfer to
    :type to_address: UInt160
    :param amount: the amount of zGAS tokens to transfer
    :type amount: int
    :param data: whatever data is pertinent to the onPayment method
    :type data: Any

    :return: whether the transfer was successful
    :raise AssertionError: raised if `from_address` or `to_address` length is not 20 or if `amount` is less than zero.
    """
    # the parameters from and to should be 20-byte addresses. If not, this method should throw an exception.
    assert len(from_address) == 20 and len(to_address) == 20
    # the parameter amount must be greater than or equal to 0. If not, this method should throw an exception.
    assert amount >= 0

    # The function MUST return false if the from account balance does not have enough tokens to spend.
    from_balance = get(from_address).to_int()
    if from_balance < amount:
        return False

    # The function should check whether the from address equals the caller contract hash.
    # If so, the transfer should be processed;
    # If not, the function should use the check_witness to verify the transfer.
    if from_address != calling_script_hash:
        if not check_witness(from_address):
            return False

    # skip balance changes if transferring to yourself or transferring 0 cryptocurrency
    if from_address != to_address and amount != 0:
        if from_balance == amount:
            delete(from_address)
        else:
            put(from_address, from_balance - amount)

        to_balance = get(to_address).to_int()
        put(to_address, to_balance + amount)

    # if the method succeeds, it must fire the transfer event
    on_transfer(from_address, to_address, amount)
    # if the to_address is a smart contract, it must call the contracts onPayment
    post_transfer(from_address, to_address, amount, data, True)
    # and then it must return true
    return True


@public
def transfer_from(spender: UInt160, from_address: UInt160, to_address: UInt160, amount: int, data: Any) -> bool:
    """
    A spender transfers an amount of zGAS tokens allowed from one account to another.

    If the method succeeds, it must fire the `Transfer` event and must return true, even if the amount is 0,
    or from and to are the same address.

    :param spender: the address that is trying to transfer zGAS tokens
    :type spender: UInt160
    :param from_address: the address to transfer from
    :type from_address: UInt160
    :param to_address: the address to transfer to
    :type to_address: UInt160
    :param amount: the amount of zGAS tokens to transfer
    :type amount: int
    :param data: whatever data is pertinent to the onPayment method
    :type data: Any

    :return: whether the transfer was successful
    :raise AssertionError: raised if `spender`, `from_address` or `to_address` length is not 20 or if `amount` if less
    than zero.
    """
    # the parameters from and to should be 20-byte addresses. If not, this method should throw an exception.
    assert len(spender) == 20 and len(from_address) == 20 and len(to_address) == 20
    # the parameter amount must be greater than or equal to 0. If not, this method should throw an exception.
    assert amount >= 0

    # The function MUST return false if the from account balance does not have enough tokens to spend.
    from_balance = get(from_address).to_int()
    if from_balance < amount:
        return False

    # The function MUST return false if the from account balance does not allow enough tokens to be spent by the spender.
    allowed = allowance(from_address, spender)
    if allowed < amount:
        return False

    # The function should check whether the spender address equals the caller contract hash.
    # If so, the transfer should be processed;
    # If not, the function should use the check_witness to verify the transfer.
    if spender != calling_script_hash:
        if not check_witness(spender):
            return False

    if allowed == amount:
        delete(ALLOWANCE_PREFIX + from_address + spender)
    else:
        put(ALLOWANCE_PREFIX + from_address + spender, allowed - amount)

    # skip balance changes if transferring to yourself or transferring 0 cryptocurrency
    if from_address != to_address and amount != 0:
        if from_balance == amount:
            delete(from_address)
        else:
            put(from_address, from_balance - amount)

        to_balance = get(to_address).to_int()
        put(to_address, to_balance + amount)

    # if the method succeeds, it must fire the transfer event
    on_transfer(from_address, to_address, amount)
    # if the to_address is a smart contract, it must call the contracts onPayment
    post_transfer(from_address, to_address, amount, data, True)
    # and then it must return true
    return True


@public
def approve(spender: UInt160, amount: int) -> bool:
    """
    Allows spender to spend from your account as many times as they want until it reaches the amount allowed.
    The allowed amount will be overwritten if this method is called once more.

    :param spender: the address that will be allowed to use your zGAS
    :type spender: UInt160
    :param amount: the total amount of zGAS that the spender can spent
    :type amount: int
    :raise AssertionError: raised if `from_address` length is not 20 or if `amount` if less than zero.
    """
    assert len(spender) == 20
    assert amount >= 0

    if balanceOf(calling_script_hash) >= amount:
        put(ALLOWANCE_PREFIX + calling_script_hash + spender, amount)
        on_approval(calling_script_hash, spender, amount)
        return True
    return False


@public
def allowance(owner: UInt160, spender: UInt160) -> int:
    """
    Gets the amount of zGAS from the owner that can be used by the spender.

    :param owner: the address that allowed the spender to spend zGAS
    :type owner: UInt160
    :param spender: the address that can spend zGAS from the owner's account
    :type spender: UInt160
    """
    return get(ALLOWANCE_PREFIX + owner + spender).to_int()


def post_transfer(from_address: Union[UInt160, None], to_address: Union[UInt160, None], amount: int, data: Any, call_onPayment: bool):
    """
    Checks if the one receiving NEP17 tokens is a smart contract and if it's one the onPayment method will be called.

    :param from_address: the address of the sender
    :type from_address: UInt160
    :param to_address: the address of the receiver
    :type to_address: UInt160
    :param amount: the amount of cryptocurrency that is being sent
    :type amount: int
    :param data: any pertinent data that might validate the transaction
    :type data: Any
    :param call_onPayment: whether onPayment should be called or not
    :type call_onPayment: bool
    """
    if call_onPayment:
        if not isinstance(to_address, None):  # TODO: change to 'is not None' when `is` semantic is implemented
            contract = get_contract(to_address)
            if not isinstance(contract, None):  # TODO: change to 'is not None' when `is` semantic is implemented
                call_contract(to_address, 'onNEP17Payment', [from_address, amount, data])


def mint(account: UInt160, amount: int):
    """
    Mints new zGAS tokens.

    :param account: the address of the account that is sending cryptocurrency to this contract
    :type account: UInt160
    :param amount: the amount of gas to be refunded
    :type amount: int
    :raise AssertionError: raised if amount is less than than 0
    """
    assert amount >= 0
    if amount != 0:
        current_total_supply = totalSupply()
        account_balance = balanceOf(account)

        put(SUPPLY_KEY, current_total_supply + amount)
        put(account, account_balance + amount)

        on_transfer(None, account, amount)
        post_transfer(None, account, amount, None, True)


@public
def burn(account: UInt160, amount: int):
    """
    Burns zGAS tokens.

    :param account: the address of the account that is pulling out cryptocurrency of this contract
    :type account: UInt160
    :param amount: the amount of gas to be refunded
    :type amount: int
    :raise AssertionError: raised if `account` length is not 20, amount is less than than 0 or the account doesn't have
    enough zGAS to burn
    """
    assert len(account) == 20
    assert amount >= 0
    if check_witness(account):
        if amount != 0:
            current_total_supply = totalSupply()
            account_balance = balanceOf(account)

            assert account_balance >= amount

            put(SUPPLY_KEY, current_total_supply - amount)

            if account_balance == amount:
                delete(account)
            else:
                put(account, account_balance - amount)

            on_transfer(account, None, amount)
            post_transfer(account, None, amount, None, False)

            call_contract(GAS, 'transfer', [executing_script_hash, account, amount, None])


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

    if get(SUPPLY_KEY).to_int() > 0:
        return False

    put(SUPPLY_KEY, TOKEN_TOTAL_SUPPLY)
    put(OWNER, TOKEN_TOTAL_SUPPLY)

    on_transfer(None, OWNER, TOKEN_TOTAL_SUPPLY)
    return True


@public
def onNEP17Payment(from_address: UInt160, amount: int, data: Any):
    """
    If this smart contract receives GAS, it will mint an amount of wrapped GAS

    :param from_address: the address of the one who is trying to send cryptocurrency to this smart contract
    :type from_address: UInt160
    :param amount: the amount of cryptocurrency that is being sent to the this smart contract
    :type amount: int
    :param data: any pertinent data that might validate the transaction
    :type data: Any
    """
    # Use calling_script_hash to identify if the incoming token is GAS
    if calling_script_hash == GAS:
        mint(from_address, amount)
    else:
        abort()
