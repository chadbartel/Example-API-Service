#!/usr/bin/env python

"""Project configuration."""
# Import libraries
import os
import logging
from copy import copy
from pathlib import Path
from yaml import load
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader


# Setup logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


# Model objects
class Config:
    """
    This class acts as a wrapper to a YAML configuration file.
    
    Attributes
    ----------
    data : dict{str:any}
        The ingested configuration data.
    items : dict{str:any}
        An iterable of of the configuration file.
    """
    
    # Instance attributes
    @property
    def data(self) -> dict:
        """Return a copy of the internal read-only _data attributes."""
        return copy(self._data)

    @property
    def items(self) -> list:
        """Return a dictionary of the mapped data, per the given rules."""
        return dict(iter(self))
    
    def get(self, key:str):
        """Return value(s) for a given key."""
        if key in self._data:
            yield self._data[key]
        for _, v in self._data.items():
            if isinstance(v, dict):
                for i in self.get(v, key):
                    yield i

    def __init__(self):
        # Set project root
        self.root = Path(__file__).parent.parent

        # Load all associated data
        self._data = {}
        data_path = self.root / 'configurations'
        for root, _, files in os.walk(data_path):
            for file in files:
                # Skip all non-yaml documents
                if '.yaml' not in file:
                    logger.warning(
                        'Service has received a non-valid yaml document: %s.',
                        file,
                    )
                    continue
                # Load data and save into internal _data attribute
                name, data = self._load_mapping(root, file)
                self._data[name] = data

    # Instance methods
    def _load_mapping(self, root: str, file: str):
        """Load given file as mapping."""
        path = os.path.join(root, file)
        roots, ext = self._parse_roots_ext(root, file)
        name = '.'.join(roots)

        logger.debug(
            'Processing mapping %s at %s.',
            '.'.join([name, ext]),
            path,
        )

        # Load mapping
        data = []
        try:
            with open(path) as rules:
                data.append(load(rules, Loader=Loader))
        except Exception as error:
            logger.error(
                'Service could not load %s due to %s',
                str(path),
                str(error),
            )
        return name, data

    def _parse_roots_ext(self, path, file):
        """Parse given file for name and qualified extension."""
        paths = str(path).replace(str(self.root), '').split('/')
        name, *exts = file.split('.')
        ext = '.'.join(exts) or ''

        paths.append(name)

        if len(paths) >= 2:
            paths = paths[1:]
            paths.remove('configurations')
            return paths, ext

        return None, None