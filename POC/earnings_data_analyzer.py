import pandas as pd

# Function to get data from influxdata_2023-06-02T18_44_38Z.csv file and print the column names and return the dataframe
def get_column_names():
    df = pd.read_csv("influxdata_2023-06-02T18_44_38Z.csv")
    print(df.columns)
    return df

# main function to execute the same
if __name__ == "__main__":
    df = get_column_names()
    # filter both estimated_Quarterly_EPS and reported_Quarterly_EPS which are greater than 0 to one df and less than 0 to another df to write a csv
    df_1 = df[(df['estimated_Quarterly_EPS'] > 0) & (df['reported_Quarterly_EPS'] > 0)]
    df_2 = df[(df['estimated_Quarterly_EPS'] < 0) | (df['reported_Quarterly_EPS'] < 0)]
    #df_1.to_csv("influxdata_2023-06-02T18_44_38Z_1.csv", index=False)
    #df_2.to_csv("influxdata_2023-06-02T18_44_38Z_2.csv", index=False)
    # Create a new column in df_1 that will get the difference between reported_Quarterly_EPS and estimated_Quarterly_EPS
    df_1['reported_actuals_diff'] = df_1['reported_Quarterly_EPS'] - df_1['estimated_Quarterly_EPS']
    # filter df_1 to have reported_actuals_diff greater than 0
    df_1 = df_1[df_1['reported_actuals_diff'] > 0]
    #df_1.to_csv("influxdata_2023-06-02T18_44_38Z_3.csv", index=False)
    # Loop throguh grouping based on symbol and for each print the symbol and the count of rows
    all_groups = []
    for symbol, group in df_1.groupby('symbol'):
        print(symbol, len(group))
        # sort group by time column
        group = group.sort_values(by=['time'])
        group['moving_estimate'] = group['estimated_Quarterly_EPS'].diff()
        group['moving_reported'] = group['reported_Quarterly_EPS'].diff()
        # Convert group dataframe to dictionary
        group_dict = group.to_dict('records')
        # put all values into all_groups list
        all_groups.extend(group_dict)
    df_result = pd.DataFrame.from_dict(all_groups)
    df_result.to_csv("influxdata_2023-06-02T18_44_38Z_4.csv", index=False)