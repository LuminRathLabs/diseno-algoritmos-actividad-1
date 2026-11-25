def validate(a, b):
    if not isinstance(a, str) or not isinstance(b, str): raise TypeError("Las entradas deben ser cadenas")
from .recursive import lcs_recursive
from .hirschberg import lcs_hirschberg
from .tabular import lcs_tabular
