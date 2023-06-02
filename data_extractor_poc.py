from module.InfluxConnector import InfluxConnector
import os

#Method to get data from Quaterly Earnings Table in InfluxDB and save it to a csv file
def get_quaterly_earnings_data():
    influx_connector = InfluxConnector()
    sql_query = f"SELECT * FROM {os.environ.get('Quarterly_Earnings_Table')}"
    print(sql_query)
    df = influx_connector.read_from_influx(sql_query)
    df.to_csv("quaterly_earnings.csv", index=False)

#Execute get_quaterly_earnings_data method through main method with try catch block
if __name__ == "__main__":
    try:
        get_quaterly_earnings_data()
    except Exception as e:
        print(str(e))