import logging
import pandas as pd

logging.basicConfig(
    filename='./results.log',
    level=logging.INFO,
    filemode='w',
    format='%(name)s - %(levelname)s - %(message)s'
)


class DataStoryTeller:
    file_path = 'euro-daily-hist_1999_2020.csv'

    def __init__(self):
        self.exchange_rates = pd.DataFrame()
        self.brl_to_euro_to_dollar = pd.DataFrame()

    def read_data(self):
        try:
            self.exchange_rates = pd.read_csv(self.file_path)
            logging.info(f'Sucesso: Existem {self.exchange_rates.shape[0]} linhas no seu dataframe')
        except FileNotFoundError:
            print(f'O arquivo {self.file_path} não existe')
            logging.error('Erro: Não foi possível encontrar este arquivo')

    def data_cleaning(self):
        self.exchange_rates.rename(columns={'[US dollar ]': 'US_dollar',
                                            'Period\\Unit:': 'Time'},
                                   inplace=True)
        self.exchange_rates['Time'] = pd.to_datetime(self.exchange_rates['Time'])
        self.exchange_rates.sort_values('Time', inplace=True)
        self.exchange_rates.reset_index(drop=True, inplace=True)
        self.exchange_rates.rename(columns={'[Brazilian real ]': 'BRL_real'}, inplace=True)

        euro_to_dollar = self.exchange_rates[['Time', 'US_dollar']].copy()
        euro_to_dollar = euro_to_dollar[euro_to_dollar['US_dollar'] != '-']
        euro_to_dollar['US_dollar'] = euro_to_dollar['US_dollar'].astype(float)

        euro_to_dollar_to_real = euro_to_dollar.copy()
        euro_to_dollar_to_real['BRL_real'] = self.exchange_rates['BRL_real']
        euro_to_dollar_to_real = euro_to_dollar_to_real[euro_to_dollar_to_real['BRL_real'] != '-']
        euro_to_dollar_to_real['BRL_real'] = euro_to_dollar_to_real['BRL_real'].astype(float)

        self.brl_to_euro_to_dollar = euro_to_dollar_to_real[['Time', 'BRL_real']].copy()
        self.brl_to_euro_to_dollar.rename(columns={'BRL_real': 'euro_rate'}, inplace=True)
        self.brl_to_euro_to_dollar['dollar_rate'] = euro_to_dollar_to_real['BRL_real'] / euro_to_dollar_to_real['US_dollar']

    def print_head(self):
        print(self.exchange_rates.head())

    def print_tail(self):
        print(self.exchange_rates.tail())

    def print_info(self):
        print(self.exchange_rates.info())


if __name__ == '__main__':
    pass
