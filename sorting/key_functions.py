"""Some key function related stuff (like caching dicts)."""
from functools import lru_cache
from typing import Any


@lru_cache
def identity_key(item: Any) -> Any:
	"""The default (identity) key function if none is supplied."""
	
	return item
