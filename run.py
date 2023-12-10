# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high
import gspread
from google.oauth2.service_account import Credentials


SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')


def get_sales_data():
    """
    Get sales figures input from the User.
    Run a while loop to collect a valid string of data from the user
    via the termial, which must be a string of 6 numbers separated
    by commas. The loop will repeatedly request data, until it is valid.
    """
    while True:
        print("Please enter the sales data from the last market.")
        print("Data should be 6 numbers, separated by commas.")
        print("Example:10,20,30,40,50,60\n")

        data_str = input("Enter your data here:\n")
        sale_data = data_str.split(",")

        if validate_data(sale_data):
            print("Data is valid!")
            break

    return sale_data


def validate_data(values):
    """
    Inside the try, converts all the string values into integers.
    Raise ValueError if strings cannoy be converted into int
    or if there aren't exactly 6 values.
    """
    try:
        # change the values into integer from str
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(
                f"Exactly 6 values required, you provide only {len(values)}"
            )
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")
        return False

    return True


# def update_sales_worksheet(data):
#     """
#     Update sales worksheet, add new row with the list data provided.
#     """
#     print("Updating sales worksheet......\n")
#     sales_worksheet = SHEET.worksheet("sales")
#     sales_worksheet.append_row(data)
#     print("Sales worksheet updated successfully.\n")


# def update_surplus_worksheet(data):
#     """
#     Update surplus worksheet, add new row with the new surplus.
#     """
#     print("Updating surplus worksheet....\n")
#     surplus_worksheet = SHEET.worksheet("surplus")
#     surplus_worksheet.append_row(data)
#     print("Surplus worksheet updated successfully.\n")


def update_worksheet(data, worksheet):
    """
    Receives a list of integer to be inserted into a worksheet
    Update the relevent worksheet with the date provided
    """
    print(f"Updating {worksheet} worksheet.....\n")
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f"{worksheet} worksheet updated sucessfully.\n")


def calculate_surplus_data(sales_row):
    """
    Compare sales with stock and caculate the surplus for each item type.

    The surplus is defined as sales figure substracted from the stock:
    - Positive surplus indicates wates
    - Negative surplus indicated extra made when stock was sold out.
    """
    print("Calculating surplus data....\n")
    stock = SHEET.worksheet("stock").get_all_values()
    # using slicing to get the lates data
    stock_row = stock[-1]

    surplus_data = []
    for stock, sales in zip(stock_row, sales_row):
        surplus = int(stock) - sales
        surplus_data.append(surplus)
    return surplus_data


def get_last_5_entries_sales():
    """
    Collects columns of data from sales worksheet, collecting
    the last 5 entries for each sandwich and retrun the data
    as a list of lists.
    """
    sales = SHEET.worksheet("sales")

    columns = []
    for ind in range(1, 7):
        column = sales.col_values(ind)
        columns.append(column[-5:])
    return columns


def calculate_stock_data(data):
    """
    Calculate the average stock for each item type, adding 10%
    """
    print("Calculating stock data....\n")
    new_stock_data = []

    for column in data:
        int_column = [int(num) for num in column]
        # the sum() is the total and len() is the lenght of the last 5 entries
        average = sum(int_column) / len(int_column)
        # 1 is the orignal number and 0.1 is the 10%
        stock_num = average * 1.1
        # we append stock_num to the new stcok data list outside the for loop
        new_stock_data.append(round(stock_num))

    return new_stock_data


def main():
    """
    Run all program function
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    # update_sales_worksheet(sales_data)
    update_worksheet(sales_data, "sales")
    new_surplus_data = calculate_surplus_data(sales_data)
    # update_surplus_worksheet(new_surplus_data)
    update_worksheet(new_surplus_data, "surplus")
    sales_columns = get_last_5_entries_sales()
    stock_data = calculate_stock_data(sales_columns)
    update_worksheet(stock_data, "stock")


print("Welcome to Love Sandwiches Data Automation")
main()
