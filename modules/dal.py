#!/usr/bin/env python

"""Service data access layer (dal)."""
# Import libraries
import os
import json
import logging
from copy import copy
from pathlib import Path


# Setup logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


# Module classes
class Project:
    """
    This class acts as an interface for the local file store. Its primary 
    function is to load and return the mappings associated with the project.

    Attributes
    ----------
    mappings : dict{str:dict}
        A dictionary of all mappings that are available to the project.
        These will be available as a dictionary with the filenames as the keys
        and the contents of the json documents as the bodies.
    """
    
    # Instance attributes
    @property
    def mappings(self) -> dict:
        """Return copy of read-only _mappings attribute."""
        return copy(self._mappings)

    def __init__(self):
        # Set project root
        self.root = Path(__file__).parent.parent

        # Load all associated mappings
        self._mappings = {}
        mappings_path = self.root / 'mappings'
        for root, _, files in os.walk(mappings_path):
            for file in files:
                # Skip all non-json documents
                if '.json' not in file:
                    logger.warning(
                        'Service has received a non-valid json document: %s.',
                        file,
                    )
                    continue
                # Load mappings and save into internal _mappings attribute
                name, mappings = self._load_mapping(root, file)
                self._mappings[name] = mappings

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
        mappings = []
        try:
            with open(path) as rules:
                mappings.extend(json.load(rules))
        except Exception as error:  # pylint: disable = broad-except
            logger.error(
                'Service could not load %s due to %s',
                str(path),
                str(error),
            )
        return name, mappings

    def _parse_roots_ext(self, path, file):
        """Parse given file for name and qualified extension."""
        paths = str(path).replace(str(self.root), '').split('/')
        name, *exts = file.split('.')
        ext = '.'.join(exts) or ''

        paths.append(name)

        if len(paths) >= 2:
            paths = paths[1:]
            paths.remove('mappings')
            return paths, ext

        return None, None