from typing import Any, Union, List, cast, Dict

from boa3.builtin import CreateNewEvent, NeoMetadata, metadata, public
from boa3.builtin.interop.binary import deserialize
from boa3.builtin.interop.runtime import calling_script_hash, check_witness
from boa3.builtin.interop.storage import get
from boa3.builtin.type import UInt160


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
def symbol():
    return "NFT"


@public
def decimals():
    return 0


@public
def totalSupply():
    return get(TOTAL_SUPPLY)


@public
def balanceOf(owner_: UInt160):
    owner = get(ACCOUNT_PREFIX + owner_)
    assert len(owner) == 20
    ids = cast(List[bytes], deserialize(owner))
    return len(ids)


@public
def tokensOf(owner_: UInt160) -> List[bytes]:
    owner = get(ACCOUNT_PREFIX + owner_)
    assert len(owner) == 20
    ids = cast(List[bytes], deserialize(owner))
    return ids


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
def mint():
    pass


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
