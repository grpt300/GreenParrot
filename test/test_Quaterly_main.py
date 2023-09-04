# Implement Unit Testing For Quaterly_main.py Module

import unittest
import pandas as pd
import Quaterly_Main as qm
from unittest.mock import patch, Mock

@patch('qm.sc.get_quarterly_earnings_data')
class TestQuaterlyMain(unittest.TestCase):

    # Mock the module.stocks_connector.get_quarterly_earnings_data() method
    def mock_get_quarterly_earnings_data(self, symbol):
        df = pd.DataFrame({'reported_Quarterly_EPS': [1.0, 2.0, 3.0],
                           'surprise': [1.0, 2.0, 3.0],
                           'surprisePercentage': [1.0, 2.0, 3.0]})
        return df
    def test_get_quarterly_earnings_data(self):
        qm.sc.get_quarterly_earnings_data = self.mock_get_quarterly_earnings_data
        df = qm.get_quarterly_earnings_data('AAPL')
        self.assertIsInstance(df, pd.DataFrame)
