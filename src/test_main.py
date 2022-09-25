"""
Contains the exceptions used in the project.
"""
import json
import pytest
import responses
from mock import patch
from main import Counties, counties_url

YEAR = '2020'
CLOSENESS = 100


@pytest.fixture(scope='function', name='mock_counties')
def fixture_mock_counties() -> Counties:
    """
    Intercepts the call to the API and returns a mock object.
    :return: Counties.
    """

    with open('resources/test.json', encoding='utf-8') as json_file:
        data: dict[list] = json.load(json_file)

    with responses.RequestsMock() as mock:
        mock.add(responses.GET, counties_url, json=data, status=200)
        yield Counties(counties_url, data_key='data')


class TestFilterByYearCounties:

    def test_correct_result(self, mock_counties: Counties) -> None:
        assert mock_counties.filter_by_year(YEAR) == [{
            "ID County": "05000US01071",
            "County": "Jackson County, AL",
            "ID Year": 2020,
            "Year": "2020",
            "Population": 51765,
            "Slug County": "jackson-county-al"
        },
            {
                "ID County": "05000US01073",
                "County": "Jefferson County, AL",
                "ID Year": 2020,
                "Year": "2020",
                "Population": 658615,
                "Slug County": "jefferson-county-al"
            },
            {
                "ID County": "05000US01075",
                "County": "Lamar County, AL",
                "ID Year": 2020,
                "Year": "2020",
                "Population": 13854,
                "Slug County": "lamar-county-al"
            },
            {
                "ID County": "05000US01075",
                "County": "Lamar County, AL",
                "ID Year": 2020,
                "Year": "2020",
                "Population": 241410,
                "Slug County": "lamar-county-al"
            }]

    def test_wrong_key(self, mock_counties: Counties) -> None:
        mock_counties.year_key = 'test'
        assert mock_counties.filter_by_year(YEAR) is None

    def test_wrong_datatype(self, mock_counties: Counties) -> None:
        mock_counties.data = ['test']
        assert mock_counties.filter_by_year(YEAR) is None

    def test_no_data(self, mock_counties: Counties) -> None:
        del mock_counties.data
        assert mock_counties.filter_by_year(YEAR) is None

    def test_filter_by_wrong_year(self, mock_counties: Counties) -> None:
        assert mock_counties.filter_by_year('2050') == []


class TestYearsInDatasetCounties:

    def test_correct_result(self, mock_counties: Counties) -> None:
        assert mock_counties.years_in_dataset() == {'2020'}

    def test_wrong_key(self, mock_counties: Counties) -> None:
        mock_counties.year_key = 'test'
        assert mock_counties.years_in_dataset() is None

    def test_wrong_datatype(self, mock_counties: Counties) -> None:
        mock_counties.data = ['test']
        assert mock_counties.years_in_dataset() is None

    def test_no_data(self, mock_counties: Counties) -> None:
        del mock_counties.data
        assert mock_counties.years_in_dataset() is None


class TestAveragePopulationPerYearCounties:

    def test_correct_result(self, mock_counties: Counties) -> None:
        assert mock_counties.average_population_per_year(YEAR) == 241411.0

    def test_wrong_key(self, mock_counties: Counties) -> None:
        mock_counties.population_key = 'test'
        assert mock_counties.average_population_per_year(YEAR) is None

    def test_wrong_year(self, mock_counties: Counties) -> None:
        assert mock_counties.average_population_per_year('test') is None

    def test_no_filter_by_year(self, mock_counties: Counties) -> None:
        with patch.object(mock_counties, 'filter_by_year', return_value=None):
            assert mock_counties.average_population_per_year(YEAR) is None

    def test_zero_division(self, mock_counties: Counties) -> None:
        with patch.object(mock_counties, 'filter_by_year', return_value=[]):
            assert mock_counties.average_population_per_year(YEAR) is None


class TestCloseToAveragePerYearCounties:

    def test_correct_result(self, mock_counties: Counties) -> None:
        assert mock_counties.close_to_average_per_year(YEAR, CLOSENESS) == [{
            "ID County": "05000US01075",
            "County": "Lamar County, AL",
            "ID Year": 2020,
            "Year": "2020",
            "Population": 241410,
            "Slug County": "lamar-county-al"
        }]

    def test_wrong_key(self, mock_counties: Counties) -> None:
        mock_counties.population_key = 'test'
        assert mock_counties.close_to_average_per_year(YEAR, CLOSENESS) is None

    def test_wrong_year(self, mock_counties: Counties) -> None:
        assert mock_counties.close_to_average_per_year('test', CLOSENESS) is None

    def test_no_filter_by_year(self, mock_counties: Counties) -> None:
        with patch.object(mock_counties, 'filter_by_year', return_value=None):
            assert mock_counties.close_to_average_per_year(YEAR, CLOSENESS) is None

    def test_no_average_population_per_year(self, mock_counties: Counties) -> None:
        with patch.object(mock_counties, 'average_population_per_year', return_value=None):
            assert mock_counties.close_to_average_per_year(YEAR, CLOSENESS) is None


class TestCloseToAverageCounties:

    def test_correct_result(self, mock_counties: Counties) -> None:
        assert list(mock_counties.close_to_average(CLOSENESS)) == [{
            "ID County": "05000US01075",
            "County": "Lamar County, AL",
            "ID Year": 2020,
            "Year": "2020",
            "Population": 241410,
            "Slug County": "lamar-county-al"
        }]

    def test_wrong_closeness_datatype(self, mock_counties: Counties) -> None:
        assert not list(mock_counties.close_to_average('test'))

    def test_no_years_in_dataset(self, mock_counties: Counties) -> None:
        with patch.object(mock_counties, 'years_in_dataset', return_value=None):
            assert not list(mock_counties.close_to_average(CLOSENESS))

    def test_years_in_dataset_wrong_return_value(self, mock_counties: Counties) -> None:
        with patch.object(mock_counties, 'years_in_dataset', return_value='test'):
            assert not list(mock_counties.close_to_average(CLOSENESS))
