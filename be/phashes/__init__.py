from .blockhash.blockhash import blockhash
from .neuralhash.neuralhash import neuralhash

from imagehash import phash

PERCEPTUAL_HASHES = {
    "blockhash": lambda x: blockhash(x, 16),
    "neuralhash": neuralhash,
    "colourhash": lambda x: str(phash(x)),
}
