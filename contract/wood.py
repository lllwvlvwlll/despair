from typing import Any, Union

from boa3.builtin import NeoMetadata, metadata, public
from boa3.builtin.contract import Nep17TransferEvent, abort
from boa3.builtin.interop.blockchain import get_contract
from boa3.builtin.interop.contract import call_contract
from boa3.builtin.interop.runtime import calling_script_hash, check_witness
from boa3.builtin.interop.storage import delete, get, put
from boa3.builtin.type import UInt160


# ---------------------------------
# CONTRACT HEADER
# ---------------------------------

CONTRACT_NAME = 'wood'
CONTRACT_VERSION = 'v0.0.1'
AUTHOR = 'The Four Blessings of the Apocalypse (COZ)'
EMAIL = 'contact@coz.io'
DESCRIPTION = 'This smart contract represents one of the core resources for the game, wood.'
DESCRIPTION_EXTENDED = ''


@metadata
def manifest_metadata() -> NeoMetadata:
    meta = NeoMetadata()
    meta.author = 'The Four Blessings of the Apocalypse (COZ)'
    meta.email = 'contact@coz.io'
    meta.description = 'This smart contract represents one of the core resources for the game, wood.'
    meta.version = "v0.0.1"
    return meta

# ---------------------------------
# CONTRACT GLOBALS
# ---------------------------------


ACCOUNT_PREFIX = b'a'
ADMIN = UInt160(b'\x8cfQ\x01Rb2\x0f\xc6Ez\xebzP\xe9\xa5\xa1\xa4\xa1\xdd')
TOKEN_DECIMALS = 0
TOKEN_PREFIX = b't'
TOKEN_SYMBOL = 'DWOOD'
TOTAL_SUPPLY = b's'

# ---------------------------------
# EVENTS
# ---------------------------------

on_transfer = Nep17TransferEvent

# ---------------------------------
# Methods
# ---------------------------------


@public
def symbol() -> str:
    """
    Gets the symbols of the token.

    :return: a short string representing symbol of the token managed in this contract.
    """
    return TOKEN_SYMBOL


@public
def decimals() -> int:
    """
    Gets the amount of decimals used by the token.

    :return: the number of decimals used by the token.
    """
    return TOKEN_DECIMALS


@public
def totalSupply() -> int:
    """
    Gets the total token supply deployed in the system.

    :return: the total token supply in the system.
    """
    return get(TOTAL_SUPPLY).to_int()


@public
def balanceOf(account: UInt160) -> int:
    """
    Get the current balance of an address

    :param account: the account address to retrieve the balance for

    :return: the accounts balance
    """
    assert len(account) == 20
    return get(account).to_int()


@public
def transfer(from_address: UInt160, to_address: UInt160, amount: int, data: Any) -> bool:
    """
    Transfers an amount of DWOOD tokens from one account to another

    If the method succeeds, it must fire the `Transfer` event and must return true, even if the amount is 0,
    or from and to are the same address.

    :param from_address: the address to transfer from
    :param to_address: the address to transfer to
    :param amount: the amount of NEP17 tokens to transfer
    :param data: whatever data is pertinent to the onPayment method

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
    post_transfer(from_address, to_address, amount, data)
    # and then it must return true
    return True


def post_transfer(from_address: Union[UInt160, None], to_address: Union[UInt160, None], amount: int, data: Any):
    """
    Checks if the one receiving DWOOD tokens is a smart contract and if it's one the onPayment method will be called

    :param from_address: the address of the sender
    :param to_address: the address of the receiver
    :param amount: the amount of cryptocurrency that is being sent
    :param data: any pertinent data that might validate the transaction
    """
    if not isinstance(to_address, None):
        contract = get_contract(to_address)
        if not isinstance(contract, None):
            call_contract(to_address, 'onNEP17Payment', [from_address, amount, data])


@public
def mint(account: UInt160, amount: int):
    """
    Mints DWOOD tokens.

    :param account: the address of the account that is sending cryptocurrency to this contract
    :param amount: the amount of gas to be refunded
    :raise AssertionError: raised if amount is less than than 0 or the check_witness using ADMIN goes wrong
    """
    assert amount >= 0 and check_witness(ADMIN)
    if amount != 0:
        current_total_supply = totalSupply()
        account_balance = balanceOf(account)

        put(TOTAL_SUPPLY, current_total_supply + amount)
        put(account, account_balance + amount)

        on_transfer(None, account, amount)
        post_transfer(None, account, amount, None)


@public
def burn(account: UInt160, amount: int):
    """
    Burns DWOOD tokens.

    :param account: the address of the account that is sending cryptocurrency to this contract
    :param amount: the amount of gas to be refunded
    :raise AssertionError: raised if amount is less than than 0 or the check_witness using ADMIN goes wrong
    """
    assert amount >= 0 and check_witness(ADMIN)
    if amount != 0:
        current_total_supply = totalSupply()
        account_balance = balanceOf(account)

        assert account_balance >= amount
        put(TOTAL_SUPPLY, current_total_supply - amount)

        if account_balance == amount:
            delete(account)
        else:
            put(account, account_balance - amount)

        on_transfer(account, None, amount)
        post_transfer(account, None, amount, None)


@public
def onNEP17Payment(from_address: UInt160, amount: int, data: Any):
    """
    This contract is currently not accepting any transfers.

    :param from_address: the address of the one who is trying to send cryptocurrency to this smart contract
    :param amount: the amount of cryptocurrency that is being sent to the this smart contract
    :param data: any pertinent data that might validate the transaction
    """
    abort()
