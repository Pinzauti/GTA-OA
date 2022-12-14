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
    This class manage the dataset, returning some metrics and filtering the data.
    """
    url: str = None
    source: dict | list[dict] = None
    data_key: str = None
    year_key: str = 'Year'
    population_key: str = 'Population'

    def __post_init__(self) -> None:
        """
        We retrieve the data from the url if provided or from the argument source, if provided.
        We filter it by the key data_key, if present.
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

    def filter_by_year(self, year: str) -> list[dict] | None:
        """
        We filter the data by the year.
        :param year: The year to filter.
        :return: A list of entries filtered by the year.
        """
        try:
            return list(filter(lambda x: x[self.year_key] == year, self.data))
        except KeyError as err:
            stderr.write(f'The key {err} is not present in the dictionary.\n')
        except AttributeError as err:
            stderr.write(f'There was probably something wrong retrieving the data. {err}\n')
        except TypeError as err:
            stderr.write(f'There was probably something wrong retrieving the data. {err}\n')

        return None

    def years_in_dataset(self) -> set[str | int] | None:
        """
        We seek the different years present in the dataset.
        :return: A set of all the years in the dataset.
        """
        try:
            return set(element[self.year_key] for element in self.data)
        except KeyError as err:
            stderr.write(f'The key {err} is not present in the dictionary.')
        except AttributeError as err:
            stderr.write(f'{err}\n')
        except TypeError as err:
            stderr.write(f'{err}\n')

        return None

    def average_population_per_year(self, year: str) -> float | None:
        """
        Returns the average population for a given year.
        :param year: The year to filter.
        :return: The average population for the year.
        """
        filter_by_year: list[dict] = self.filter_by_year(year)
        try:

            if not filter_by_year:
                raise NoResultFromFunctionError('filter_by_year')

            return sum(element[self.population_key] for element in filter_by_year) / len(
                filter_by_year)

        except KeyError as err:
            stderr.write(f'The key {err} is not present in the dictionary.\n')
        except TypeError as err:
            stderr.write(f'{err}\n')
        except NoResultFromFunctionError as err:
            stderr.write(f'{err}\n')

        return None

    def close_to_average_per_year(self, year: str, closeness: int) -> list[dict] | None:
        """
        Returns a list of all the counties that are within a given closeness of the average
        population for a given year.
        :param year: The year to filter.
        :param closeness: The closeness to the average.
        :return: A list of all the counties that are within a given closeness of the average.
        """
        try:

            if not isinstance(closeness, int):
                raise TypeError('The closeness must be an integer.')

            if not self.average_population_per_year(year):
                raise NoResultFromFunctionError('average_population_per_year')
            if not self.filter_by_year(year):
                raise NoResultFromFunctionError('filter_by_year')

            average: float = self.average_population_per_year(year)
            return list(filter(lambda x: abs(x[self.population_key] - average) <= closeness,
                               self.filter_by_year(year)))

        except KeyError as err:
            stderr.write(f'The key {err} is not present in the dictionary.\n')
        except TypeError as err:
            stderr.write(f'{err}\n')
        except NoResultFromFunctionError as err:
            stderr.write(f'{err}\n')

        return None

    def close_to_average(self, closeness: int) -> list[dict]:
        """
        Returns a list of all the counties that are within a given closeness of the average
        population for a given years, for all years.
        :param closeness: The closeness to the average.
        :return: A list of all the counties that are within a given closeness of the average.
        """
        try:

            if not isinstance(closeness, int):
                raise TypeError('The closeness must be an integer.')
            if not self.years_in_dataset():
                raise NoResultFromFunctionError('years_in_dataset')

            for year in self.years_in_dataset():
                for element in self.close_to_average_per_year(year, closeness):
                    yield element

        except TypeError as err:
            stderr.write(f'{err}\n')
        except NoResultFromFunctionError as err:
            stderr.write(f'{err}\n')


counties = Counties(counties_url, data_key='data')

for result in counties.close_to_average(100):
    print(f'{result}\n')
