from boa3.builtin import NeoMetadata, metadata, public
from boa3.builtin.contract import Nep17TransferEvent, abort
from boa3.builtin.interop.blockchain import get_contract
from boa3.builtin.interop.contract import call_contract
from boa3.builtin.interop.runtime import calling_script_hash, check_witness
from boa3.builtin.interop.storage import get_context, get, put
from boa3.builtin.type import UInt160
from boa3.builtin.interop.runtime import calling_script_hash, check_witness, executing_script_hash, get_time, get_time, invocation_counter
from boa3.builtin.interop.crypto import sha256
from boa3.builtin.interop.binary import serialize, deserialize, itoa
from boa3.builtin.interop.runtime import get_time
from boa3.builtin.interop.crypto import sha256
from boa3.builtin.interop.json import json_serialize, json_deserialize
from typing import Any, Dict, cast, List
from boa3.builtin.interop.iterator import Iterator
from boa3.builtin.interop.contract import call_contract

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
LAND_OWNERSHIP = b'_lo_'
CLAIM_TIMESTAMP = b'_ct_'

# ---------------------------------
# CONTRACT HASHES
# ---------------------------------

MATERIAL_WOOD = UInt160(b'\xcf\xa0\x9b\x19\xf7#\xd9ig&\x91*0cb\xc3!*\x01\xc4')


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
def land_get(index: str) -> dict:
    land: dict = deserialize(get(index))
    return land

# TODO - we still need to dynamic invoke the `mint` method
@public
def claim_bounty(owner: UInt160, index: str, material: str) -> bool:
    unclaimed = get_unclaimed(index, material)

    # dynamic invoke to `mint` on relevant contract
    res: bool = call_contract(MATERIAL_WOOD, "mint", (owner, unclaimed))
    if res == True:
        put(CLAIM_TIMESTAMP + index.to_bytes() + material.to_bytes(), get_time)

    return True


# TODO - reduce the generation rate
@public
def get_unclaimed(index: str, material: str) -> int:
    land = land_get(index)
    rate = cast(int, land[material])


    last_claim = cast(int, get(CLAIM_TIMESTAMP + index.to_bytes() + material.to_bytes()))
    return (get_time - max(cast(int, land["genesis"]), last_claim)) * rate + 1


@public
def create_land(owner: UInt160) -> bool:

    total_supply = get(TOTAL_SUPPLY).to_int()
    total_supply = total_supply + 1

    new_land = land_init(total_supply, owner)
    land_save(new_land, owner)

    put(TOTAL_SUPPLY, total_supply)
    return True

# TODO NEEDS TO WORK
@public
def tokensOf(owner: UInt160) -> List[str]:
    key = LAND_OWNERSHIP + owner

    current_ownership: List[str] = deserialize(get(key))
    return current_ownership


def get_seed(index: int) -> bytes:
    return sha256(get_time + index)


# TODO - Make the distribution a Poisson 0-100
def get_rand(seed: int) -> int:
    return seed % 99


def land_init(index: int, owner: UInt160) -> dict:
    seed = get_seed(index)
    land = {
        "seed": seed,
        "owner": owner,
        "index": "i_" + itoa(index),
        "wood": get_rand(seed[0]),
        "wheat": get_rand(seed[1]),
        "gold": get_rand(seed[2]),
        "stone": get_rand(seed[3]),
        "water": get_rand(seed[4]),
        "genesis": get_time
    }
    return land


def land_save(land: dict, owner: UInt160) -> bool:

    index: str = land["index"]
    put(index, serialize(land))

    key = LAND_OWNERSHIP + owner

    #current_ownership: List[str] = deserialize(get(key))
    #current_ownership.append(index)

    #put(key, serialize(current_ownership))
    return True
