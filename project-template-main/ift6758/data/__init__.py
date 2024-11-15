"""
You can "pre" import stuff in the __init__.py module, but this is not required.
This allows you to import this function as:

    from ift6758.data import get_player_stats

instead of only:

    from ift6758.data.question_1 import get_player_stats

but both are still valid. You can read more about packages and modules here:
https://docs.python.org/3/reference/import.html#regular-packages
"""
from .data_fetching import NHL_Season_Data_Fetcher