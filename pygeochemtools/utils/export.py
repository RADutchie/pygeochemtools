"""Export helper functions

.. currentmodule:: pygeochemtools.utils.export
.. moduleauthor:: Rian Dutch <riandutch@gmail.com>
"""

from pathlib import Path

import pandas as pd


def export_dataset(
    df: pd.DataFrame, label: str, path: str = None, out_path: str = None
) -> None:
    """Export element dataset

    Args:
        df (pd.DataFrame): Dataframe to export
        element (str): Name of element in dataset
        path (str): Input file location
        out_path (str): File location to export to, if different from import path.
        Defaults to None
    """
    if out_path is None:
        out_path = Path(path).parent
    else:
        out_path = Path(out_path)

    out_file = out_path / f"{label}.csv"

    df.to_csv(out_file, index=False)
