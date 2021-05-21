from boa3.builtin import NeoMetadata, metadata, public
from boa3.builtin.contract import Nep17TransferEvent, abort
from boa3.builtin.interop.blockchain import get_contract
from boa3.builtin.interop.contract import call_contract
from boa3.builtin.interop.runtime import calling_script_hash, check_witness
from boa3.builtin.interop.storage import delete, get, put
from boa3.builtin.type import UInt160
from boa3.builtin.interop.runtime import calling_script_hash, check_witness, executing_script_hash, get_time, get_time, invocation_counter
from boa3.builtin.interop.crypto import sha256
from boa3.builtin.interop.binary import serialize, deserialize
from boa3.builtin.interop.runtime import get_time
from boa3.builtin.interop.crypto import sha256
from boa3.builtin.interop.json import json_serialize, json_deserialize
from typing import Any, Dict, cast

# ---------------------------------
# CONTRACT HEADER
# ---------------------------------

CONTRACT_NAME = 'despair'
CONTRACT_VERSION = 'v0.0.1'
AUTHOR = 'The Four Blessings of the Apocalypse (COZ)'
EMAIL = 'contact@coz.io'
DESCRIPTION = 'The core contract for despair.'
DESCRIPTION_EXTENDED = ''


@metadata
def manifest_metadata() -> NeoMetadata:
    meta = NeoMetadata()
    meta.author = 'The Four Blessings of the Apocalypse (COZ)'
    meta.email = 'contact@coz.io'
    meta.description = 'The core contract for despair.'
    meta.version = "v0.0.1"
    return meta

# ---------------------------------
# CONTRACT GLOBALS
# ---------------------------------


ADMIN = UInt160(b'\x8cfQ\x01Rb2\x0f\xc6Ez\xebzP\xe9\xa5\xa1\xa4\xa1\xdd')
TOKEN_DECIMALS = 0
TOKEN_PREFIX = b't'
TOKEN_SYMBOL = 'DESP'
TOTAL_SUPPLY = b's'

# ---------------------------------
# EVENTS
# ---------------------------------

#on_transfer = Nep17TransferEvent

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
    return get(TOTAL_SUPPLY).to_int()

@public
def land_get(owner: UInt160) -> dict:
    land: dict = deserialize(get(owner))
    return land

@public
def create_land(owner: UInt160) -> bool:

    total_supply = get(TOTAL_SUPPLY)

    new_land = land_init(total_supply, owner)
    land_save(new_land)

    put(TOTAL_SUPPLY, total_supply.to_int() + 1)
    return True


def get_seed(total_supply: bytes) -> bytes:
    return sha256(get_time + total_supply.to_int())


def get_rand(seed: int) -> int:
    # this distribution needs to be a Poisson
    return seed % 99


def land_init(index: bytes, owner: UInt160) -> dict:
    seed = get_seed(index)
    land = {
        "seed": seed,
        "owner": owner,
        "index": index.to_int(),
        "wood": get_rand(seed[0]),
        "wheat": get_rand(seed[1]),
        "gold": get_rand(seed[2]),
        "stone": get_rand(seed[3]),
        "water": get_rand(seed[4]),
    }
    return land




def land_save(land: dict) -> bool:
    owner = cast(UInt160, land["owner"])
    put(owner, serialize(land))
    return True
