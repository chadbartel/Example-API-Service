#!/usr/bin/env python

"""Service models and factories."""
import re
import logging
from copy import copy
from typing import Generator, List, Any


# Setup logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


# TODO: Model objects
class JSONManifest:
    """
    This object acts as a container for a JSON document. Instances of this 
    class are initialized with a Python dictionary and a list of rules. 
    The list of rules act as an iterator for the resulting combination 
    of the two documents.

    For each rule, if the `source` values match the path for the value in 
    the data, then the manifest will output the `target` along with the values.

    Parameters
    ----------
    data : dict{str:any}
        The data dictionary that the JSONManifest instance will wrap.
    rules : list[dict]
        A list of rules to apply to the ingested data.
        Rules must be a list of dictionaries, each with a `source` and `target`
        key to operate correctly.
    Attributes
    ----------
    data : dict{str:any}
        The ingested data.
    rules : list[dict]
        The ingested rules.
    items : dict{str:any}
        A dictionary where the keys are the target paths and the values are
        the values, after the transformation has occurred.
    """
    pass

# TODO: Factory objects
class JSONFactory:
    """
    This class acts as a factory on top of JSONManifest objects to 
    recombine all mapped values back into a valid JSON document. This 
    recombined JSON document is referred to as a "Projection" or a 
    "Projected JSON".


    Parameters
    ----------
    manifest : JSONManifest
        The JSONManifest object, which is a container for the rules and data
        that should be combined to create the projected JSON.
    
    Attributes
    ----------
    RE_PAT : re.Pattern
        A regex pattern which parses JSONPaths for queries.
    RE_IDX : dict{str:str}
        A dictionary which represents the group names of `RE_PAT`.
    """
    pass
