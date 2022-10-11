from logging import Logger
import os
from dataclasses import dataclass
import pandas as pd
import os
import pyodbc
import datetime as dt
import streamlit as st
import functools


@dataclass
class EndpointInfo:
    host: str
    token: str
    http_path: str
    driver_path: str


class DataProvider:
    """
    Base class for providing access to the data 
    """
    def __init__(self, logger: Logger) -> None:
        self.logger = logger
        endpoint_info = self._get_endpoint_info()
        self.connection = pyodbc.connect(
            self.get_connection_string(endpoint_info), autocommit=True
        )

    @staticmethod
    def _get_endpoint_info() -> EndpointInfo:
        """
        This function collects all the nessesary bits of information to connect to the endpoint
        """
        for var in ["DATABRICKS_HOST", "DATABRICKS_TOKEN", "DATABRICKS_HTTP_PATH"]:
            if var not in os.environ:
                raise Exception(f"Environment variable {var} is not defined")

        _host = os.environ["DATABRICKS_HOST"]
        _token = os.environ["DATABRICKS_TOKEN"]
        _http_path = os.environ["DATABRICKS_HTTP_PATH"]
        _driver_path = os.environ.get(
            "SIMBA_DRIVER_PATH", "/opt/simba/spark/lib/64/libsparkodbc_sb64.so"
        )  # default location on Debian
        return EndpointInfo(_host, _token, _http_path, _driver_path)

    @staticmethod
    def get_mapbox_token() -> str:
        """
        For chosen visualization map type, a free token from Mapbox is needed.
        """
        token = os.environ.get("MAPBOX_TOKEN")
        if not token:
            raise Exception(
                "Mapbox token is not provided, please create one for free at https://studio.mapbox.com/"
            )
        return token

    @staticmethod
    def get_connection_string(endpoint_info: EndpointInfo) -> str:
        """
        This function builds the connection string as per Simba ODBC driver documentation
        """
        connection_string = "".join(
            [
                f"DRIVER={endpoint_info.driver_path}",
                f";Host={endpoint_info.host}",
                ";PORT=443",
                f";HTTPPath={endpoint_info.http_path}",
                ";AuthMech=3",
                ";Schema=default",
                ";SSL=1",
                ";ThriftTransport=2",
                ";SparkServerType=3",
                ";UID=token",
                f";PWD={endpoint_info.token}",
                ";RowsFetchedPerBlock=10000", # Please note that the default value is 10k, we increase it to 100k for faster fetches
            ]
        )
        return connection_string

    def _get_data(self, query: str) -> pd.DataFrame:
        self.logger.debug(f"Running SQL query: {query}")
        start_time = dt.datetime.now()
        data = pd.read_sql(query, self.connection)
        end_time = dt.datetime.now()
        time_delta = end_time - start_time
        self.logger.debug(
            f"Query executed, returning the result. Total query time: {time_delta}"
        )
        return data