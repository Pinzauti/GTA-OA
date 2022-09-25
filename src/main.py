"""
Main file of the project. We define the main class and we run the function close_to_average().
"""
import os
from sys import stderr
from dataclasses import dataclass
from requests import get, exceptions
from dotenv import load_dotenv
from exceptions_main import MissingArgumentError, NoResultFromFunctionError

load_dotenv()
counties_url: str = os.environ.get("COUNTIES-URL")


@dataclass
class Counties:
    """
    TODO
    """
    url: str = None
    source: dict | list[dict] = None
    data_key: str = None
    year_key: str = 'Year'
    population_key: str = 'Population'

    def __post_init__(self) -> None:
        """
        TODO
        :return: None.
        """
        try:

            if not(self.url or self.source):
                raise MissingArgumentError('You must provide a url or a source.')

            raw: dict | list[dict] = self.source or get(self.url, timeout=5).json()
            self.data: list[dict] = raw[self.data_key] if self.data_key else raw

        except (exceptions.MissingSchema, exceptions.InvalidSchema, exceptions.InvalidURL) as err:
            stderr.write(f'The URL provided is not a valid URL. {err}\n')
        except (exceptions.ConnectionError, exceptions.TooManyRedirects, exceptions.HTTPError,
                exceptions.Timeout) as err:
            stderr.write(f' There is an error with the URL or the connection. {err}\n')
        except exceptions.InvalidJSONError as err:
            stderr.write(f'The data is not in a valid JSON format. {err}\n')
        except KeyError as err:
            stderr.write(f'The key {err} is not present in the dictionary.\n')
        except MissingArgumentError as err:
            stderr.write(f'{err}\n')

