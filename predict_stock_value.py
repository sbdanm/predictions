import csv, os, random

input_directory = "input_stock_price_data_files"
output_directory = "output_stock_price_data_files"


def generate_output_files(stock_market, *args):

    for l in args:
        for entry in l:
            file_info = entry.split('.')
            ticker = file_info[0]
            file_extension = "." + file_info[1]

            new_file_name = ticker + "_" + predict_price.__name__ + file_extension ### if we want to create files also with 10 consective entris FUNC_NAME.__name__
            new_file_path = os.path.join(os.path.join(output_directory, stock_market), new_file_name)

            if stock_market not in os.listdir(output_directory):
                os.mkdir(os.path.join(output_directory, stock_market))
                print("Directory was successful created")

            try:
                base_file = os.path.join(os.path.join(input_directory, stock_market), entry) ### this line can be moved outside the try/except
                predicted_prices = predict_price(base_file)

                with open(new_file_path, "w", newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerows(predicted_prices)

                    if new_file_name in os.listdir(os.path.join(output_directory, stock_market)):
                        print(f"{new_file_name} was successful created")
                    else:
                        print(f"{new_file_name} was NOT successful created")

            except:
                print(f"{new_file_name} was not possible to be generated, proeeeding to the next set of data or file")


def first_ten_entries(file):

    try:
        with open(file, "r") as f:

            data = csv.reader(f)

            ticker_data = []

            for entry in data:
                ticker, date, price = entry[0], entry[1], entry[2]

                if [ticker, date, price] not in ticker_data:
                    ticker_data.append([ticker, date, price])

            start_point = random.randint(0, len(ticker_data[0]))
            end_point = start_point + 10 # this 10 consecutive numbers can be an improvement,
                                                     # maybe we want a different value at each run

        first_ten_entries = []
        print(f"\nFor {ticker} We are having the following 10 consecutive values:")
        for i in range(start_point, end_point):
            first_ten_entries.append([ticker_data[i][0], ticker_data[i][1], float(ticker_data[i][2])])
            print(f" {i} --> Date: {ticker_data[i][1]}, Price: {ticker_data[i][2]}")

        return first_ten_entries

    except:
        print("Error opening file")


def predict_price(file):

    data = first_ten_entries(file)

    last_data_entry = data[-1]
    ticker, last_date, n_price = last_data_entry[0], last_data_entry[1], last_data_entry[2]
    n = n_price

    prices_in_data = []
    for entry in range(len(data)):
        prices_in_data.append(data[entry][2])
    prices_in_data.sort()

    ### predict the n+1
    ### "first predicted (n+1) data point is same as the 2nd highest value present in the 10 data points"

    n_1 = prices_in_data[-2]

    ### predict the n+2
    ### n+2 data point has half the difference between n and n +1

    n_2 = n + (n_1 - n) / 2

    ### predict the n+3
    ### n+3 data point has 1/4th the difference between n+1 and n+2

    n_3 = n_1 + (n_2 - n_1) / 4

    future_prices = [n_1, n_2, n_3]

    print(f"Predicted Prices:")
    i = 1
    for p in future_prices:
        next_day = int(last_date.split("-")[0]) + i
        next_date = last_date.replace(last_date.split("-")[0], str(next_day))
        print(f"Ticker: {ticker}, Date: {next_date}, Price: {p}")
        data.append([ticker, next_date, float(round(p, 2))])
        i+=1

    return data




stock_market_directories = os.listdir(input_directory)
for directory in stock_market_directories:
    dir_path = os.path.join(input_directory, directory)

    files = []
    for file in os.listdir(dir_path):
        files.append(file)

    generate_output_files(directory,files)
