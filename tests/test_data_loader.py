from distutils.command.config import config
import unittest
import pandas as pd
from config import Config

from app.loader import (cumulative_to_daily_deaths, download_covid_data)


class TestDataLoader(unittest.TestCase):

    def test_download_one_day_covid_data(self):
        """
        Test that the download function returns a dataframe with one day.
        """
        config = Config()
        date = '20211231'
        config.COVID_URL = f'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni-{date}.csv'

        data = download_covid_data(config)
        self.assertEqual(data.shape, (len(config.REGIONS), data.shape[1]))

    def test_download_invalid_covid_data(self):
        """
        Test that the download function returns None if the data is invalid.
        """
        config = Config()
        config.COVID_URL = 'https://www.google.com'
        df = download_covid_data(config)
        self.assertIsNone(df)

    def test_download_invalid_link(self):
        """
        Test that the download function returns None if the link is invalid.
        """
        config = Config()
        config.COVID_URL = 'https://fsnaigerigbeksgneur.com'
        df = download_covid_data(config)
        self.assertIsNone(df)

    def test_something(self):
        config = Config()
        data = download_covid_data(config)
        t = cumulative_to_daily_deaths(data)
        print(t)
