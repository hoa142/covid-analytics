"""Get covid cases numbers from API."""

from datetime import datetime
from typing import Dict, List, NamedTuple

import requests
from pandas import DataFrame

COVID_URL = "https://api.covid19api.com/summary"
CountryCases = NamedTuple(
    "CountryCases",
    [
        ("ID", str),
        ("Country", str),
        ("CountryCode", str),
        ("Slug", str),
        ("NewConfirmed", int),
        ("TotalConfirmed", int),
        ("NewDeaths", int),
        ("TotalDeaths", int),
        ("NewRecovered", int),
        ("TotalRecovered", int),
        ("Date", datetime),
        ("Premium", Dict),
    ],
)


def get_covid_api_response() -> Dict:
    """
    Get response from covid API.

    :return: Dict
    """
    return requests.get(COVID_URL).json()


def get_response_date(api_response: Dict) -> str:
    """
    Get response date from covid API.

    :param api_response: response from covid API
    :return: response date
    """
    response_date_time = api_response["Date"]
    return (
        datetime.strptime(response_date_time, "%Y-%m-%dT%H:%M:%S.%fz")
        .date()
        .strftime("%Y-%m-%d")
    )


def get_covid_numbers(api_response: Dict) -> List[CountryCases]:
    """
    Get covid cases of all countries.

    :param api_response: response from covid API
    :return: List of countries with their covid numbers.
    """
    countries_cases = []

    # Get global covid cases
    global_cases = CountryCases(
        ID=api_response["ID"],
        Country="Global",
        CountryCode="GLOBAL",
        Slug="global",
        **api_response["Global"],
        Premium={}
    )
    countries_cases.append(global_cases)

    # Get covid cases of all countries
    for country in api_response["Countries"]:
        country_cases = CountryCases(**country)
        countries_cases.append(country_cases)

    return countries_cases


def get_covid_df(covid_numbers: List[CountryCases]) -> DataFrame:
    """
    Get covid cases of all countries.

    :param covid_numbers: List of countries with their covid numbers.
    :return: Pandas dataframe
    """
    countries_cases_df = DataFrame(
        covid_numbers,
        columns=[
            "id",
            "country",
            "country_code",
            "slug",
            "new_confirmed",
            "total_confirmed",
            "new_deaths",
            "total_deaths",
            "new_recovered",
            "total_recovered",
            "time",
            "premium",
        ],
    )

    countries_cases_df.drop("premium", axis=1, inplace=True)
    countries_cases_df["time"] = countries_cases_df["time"].apply(
        lambda t: datetime.strptime(t, "%Y-%m-%dT%H:%M:%S.%fz").strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    )
    countries_cases_df["date"] = countries_cases_df["time"].apply(
        lambda t: datetime.strptime(t, "%Y-%m-%d %H:%M:%S").date().strftime("%Y-%m-%d")
    )

    return countries_cases_df
