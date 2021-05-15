from boa3.builtin import NeoMetadata, metadata, public

# ---------------------------------
# CONTRACT HEADER
# ---------------------------------

CONTRACT_NAME = 'despair'
CONTRACT_VERSION = 'v0.0.1'
AUTHOR = 'The Four Blessings of the Apocalypse (COZ)'
EMAIL = 'contact@coz.io'
DESCRIPTION = 'This smart contract represents the core on-chain infrastructure for the game, despair.'
DESCRIPTION_EXTENDED = ''


@metadata
def manifest_metadata() -> NeoMetadata:
    meta = NeoMetadata()
    meta.author = 'The Four Blessings of the Apocalypse (COZ)'
    meta.email = 'contact@coz.io'
    meta.description = 'This smart contract represents the core on-chain infrastructure for the game, despair.'
    meta.version = "v0.0.1"
    return meta

# ---------------------------------
# CONTRACT GLOBALS
# ---------------------------------


# ---------------------------------
# EVENTS
# ---------------------------------

# NEP17 events
# NEP11 events

# ---------------------------------
# Methods
# ---------------------------------


@public
def init() -> bool:
    # initialize despair
    return True

@public
def hello() -> str:
    return "Welcome to despair."