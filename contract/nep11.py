from typing import Any, Union, List, cast, Dict

from boa3.builtin import CreateNewEvent, NeoMetadata, metadata, public
from boa3.builtin import NeoMetadata, metadata, public
from boa3.builtin.interop.storage import delete, get, put
from boa3.builtin.type import UInt160
from boa3.builtin.interop.binary import serialize, deserialize
from boa3.builtin.interop.runtime import get_time
from boa3.builtin.interop.crypto import sha256
from typing import Any, Dict, cast


# ---------------------------------
# CONTRACT HEADER
# ---------------------------------

CONTRACT_NAME = ''
CONTRACT_VERSION = 'v0.0.1'
AUTHOR = 'The Four Blessings of the Apocalypse (COZ)'
EMAIL = 'contact@coz.io'
DESCRIPTION = ''
DESCRIPTION_EXTENDED = ''


@metadata
def manifest_metadata() -> NeoMetadata:
    meta = NeoMetadata()
    meta.author = 'The Four Blessings of the Apocalypse (COZ)'
    meta.email = 'contact@coz.io'
    meta.description = ''
    meta.version = "v0.0.1"
    return meta

# ---------------------------------
# CONTRACT GLOBALS
# ---------------------------------


ACCOUNT_PREFIX = b'a'
ADMIN = UInt160(b'')
TOKEN_PREFIX = b't'
TOTAL_SUPPLY = b's'

# ---------------------------------
# EVENTS
# ---------------------------------

Nep11TransferEvent = CreateNewEvent(
    [
        ('from', Union[UInt160, None]),
        ('to', Union[UInt160, None]),
        ('amount', int),
        ('tokenId', bytes)
    ],
    'Transfer'
)

# ---------------------------------
# Methods
# ---------------------------------


@public
def symbol() -> str:
    return "DESP"


@public
def decimals() -> int:
    return 0


@public
def totalSupply() -> int:
    return get(TOTAL_SUPPLY).to_int()


# TODO
@public
def balanceOf(owner_: UInt160) -> int:
    owner = get(ACCOUNT_PREFIX + owner_)
    assert len(owner) == 20
    ids = cast(List[bytes], deserialize(owner))
    return len(ids)

# TODO
@public
def tokensOf(owner_: UInt160) -> List[bytes]:
    owner = get(ACCOUNT_PREFIX + owner_)
    assert len(owner) == 20
    ids = cast(List[bytes], deserialize(owner))
    return ids

# TODO
@public
def transfer(to: UInt160, token_id: bytes, data: Any):
    assert len(to) == 20

    token = cast(Dict['str'], deserialize(get(TOKEN_PREFIX + token_id)))

    from_address: UInt160 = token['owner']
    if from_address != calling_script_hash and not check_witness(from_address):
        return False

    # if it's not transferring to your own account
    if from_address != to:
        owner = cast(List[int], deserialize(get(ACCOUNT_PREFIX + from_address)))




    post_transfer()
    return True


@public
def burn():
    pass


@public
def mint(owner: UInt160) -> bool:
    return create_land(owner)



@public
def post_transfer():
    pass


# non-divisible
@public
def ownerOf(token_id: bytes) -> UInt160:
    token = get(TOKEN_PREFIX + token_id)
    owner = cast(Dict['str'], deserialize(token))['owner']
    return owner


# optional
@public
def tokens():
    pass


@public
def properties():
    pass




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
