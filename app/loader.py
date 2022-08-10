from io import StringIO
import requests
import pandas as pd
import numpy as np
import streamlit as st

from config import Config


@st.cache(suppress_st_warning=True, allow_output_mutation=True)
def download_covid_data(config: Config) -> pd.DataFrame:
    """
    Downloads the COVID-19 data from the DPC repository.
    """
    try:
        r = requests.get(config.COVID_URL, allow_redirects=True)
        urlData = r.content.decode('utf-8')
        df = pd.read_csv(StringIO(urlData), sep=',', parse_dates=[0])
    except:
        return None

    # Rename relevant columns translating them in english
    df.rename(columns={
        'data': 'date',
        'denominazione_regione': 'region',
        'deceduti': 'deaths'
    },
              inplace=True)

    # Fix regions name
    autonomous_province_to_regions = {
        'P.A. Trento': 'Trentino-Alto Adige',
        'P.A. Bolzano': 'Trentino-Alto Adige'
    }
    df.replace(to_replace={'region': autonomous_province_to_regions},
               inplace=True)
    df = df.groupby(['date', 'region'])['deaths'].sum().reset_index()

    # Keep only the dates
    df['date'] = df['date'].dt.normalize()
    return df


@st.cache(suppress_st_warning=True, allow_output_mutation=True)
def cumulative_to_daily_deaths(data: pd.DataFrame) -> pd.DataFrame:
    """
    Converts cumulative deaths to daily deaths.
    """
    # Computes the daily deaths from cumulative deaths
    cum_deaths_per_region = pd.pivot_table(data=data,
                                           values='deaths',
                                           index='date',
                                           columns='region',
                                           aggfunc=np.sum)

    regions = cum_deaths_per_region.columns
    fake_row = pd.DataFrame(
        data={r: 0
              for r in regions},
        index=[cum_deaths_per_region.index.min() - pd.DateOffset(days=1)])

    cum_deaths_per_region = pd.concat([fake_row, cum_deaths_per_region])
    inc_deaths_per_region = cum_deaths_per_region.diff(periods=1, axis=0)
    inc_deaths_per_region.dropna(axis=0, how='all', inplace=True)

    return inc_deaths_per_region
