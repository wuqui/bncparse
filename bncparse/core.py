# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/index.ipynb.

# %% auto 0
__all__ = ['get_xml']

# %% ../nbs/index.ipynb 4
from pathlib import Path
from collections import defaultdict

from lxml import etree
import pandas as pd

# %% ../nbs/index.ipynb 12
def get_xml(f_path):
    with open(f_path, 'r') as f:
        f = f.read()
    xml = etree.fromstring(f)
    return xml
