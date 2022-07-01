import logging
import os

import pyarrow as pa
from pyarrow.lib import tobytes
from pyarrow.lib import Table

# create and configure main logger
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)

# create console handler with a higher log level
LOG_HANDLER = logging.StreamHandler()
LOG_HANDLER.setLevel(logging.DEBUG)

# create formatter and add it to the handler
FORMATTER = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
LOG_HANDLER.setFormatter(FORMATTER)

# add the handler to the logger
logging.getLogger('').addHandler(LOG_HANDLER)


class SubstraitUtils(object):
    """
    Common utility for substrait integration tests.
    """
    def __init__(self, name="SubstraitUtils"):
        """

        """
        self.logger = LOGGER
        self.logger.info(name)

    @staticmethod
    def arrow_sort_tb_values(table: type[Table],
                             sortby: list[str]) -> type[Table]:
        """
        Sort the pyarrow table by the given list of columns.

        Args:
            table: Original pyarrow Table
            sortby: Columns to sort the results by

        Returns:
            Pyarrow Table sorted by given columns

        """
        table_sorted_indexes = pa.compute.bottom_k_unstable(table,
                                                            sort_keys=sortby,
                                                            k=len(table))
        table_sorted = table.take(table_sorted_indexes)
        return table_sorted

    @staticmethod
    def format_sql_query(sql_query: str, datasets: list) -> str:
        """
        Replace the 'Table' Parameters from the SQL query with the relative
        file paths of the parquet data.

        Args:
            sql_query: SQL Query
            datasets: List of file names

        Returns:
            SQL Query with file paths
        """
        sql_commands_list = (
            [line.strip() for line in sql_query.strip().split("\n")]
        )
        sql_query = " ".join(sql_commands_list)
        relative_folder_path = "substrait/data/tpch_parquet/"
        relative_file_paths = [f"{relative_folder_path}{x}" for x in datasets]

        return sql_query.format(*relative_file_paths)

    @staticmethod
    def format_substrait_query(substrait_query: str, datasets: list) -> bytes:
        """
        Replace the 'local_files' path in the substrait query plan with
        the full path of the parquet data.

        Args:
            substrait_query: Substrait Query
            datasets: List of file names

        Returns:
            Substrait query plan in byte format
        """
        # Get full path for all datasets used in the query
        realpath_directory = os.path.realpath(
            os.path.join(os.getcwd(), os.path.dirname(__file__)))
        data_dir = os.path.join(realpath_directory, 'data/tpch_parquet')
        parquet_file_paths = (
            [os.path.join(data_dir, dataset) for dataset in datasets]
        )

        # Replace the filename placeholder in the substrait query plan with
        # the proper parquet data file paths.
        for count, file_path in enumerate(parquet_file_paths):
            substrait_query = substrait_query.replace(
                f"FILENAME_PLACEHOLDER_{count}", file_path)

        return tobytes(substrait_query)


