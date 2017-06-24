# http://github.com/timestocome


# import balance sheet, income statement and cash flow from 
# finance.yahoo.com and parse data into csv files

# sample urls
# https://finance.yahoo.com/quote/AMD/financials?p=AMD
# https://finance.yahoo.com/quote/AMD/balance-sheet?p=AMD
# https://finance.yahoo.com/quote/AMD/cash-flow?p=AMD



###############################################################################
# download files
###############################################################################
import requests
import os

dir = 'financials/'
try: os.stat(dir)
except: os.mkdir(dir)


def download(stock):

    stock = stock.upper()
    url_income = 'https://finance.yahoo.com/quote/' + stock + '/financials?p=' + stock 
    url_balance = 'https://finance.yahoo.com/quote/' + stock + '/balance-sheet?p=' + stock
    url_cash = 'https://finance.yahoo.com/quote/' + stock + '/cash-flow?p=' + stock 

    r = requests.get(url_income, allow_redirects=True)
    income_name = dir + stock + '.income.txt'
    open(income_name, 'wb').write(r.content)

    r = requests.get(url_balance, allow_redirects=True)
    balance_name = dir + stock + '.balance.txt'
    open(balance_name, 'wb').write(r.content)

    r = requests.get(url_cash, allow_redirects=True)
    cash_name = dir + stock + '.cash.txt'
    open(cash_name, 'wb').write(r.content)



#download('COP')


###############################################################################
# parse files
################################################################################
import os
import re
import csv

def parse_income():

    file_names = [fn for fn in os.listdir(dir) if fn.endswith('income.txt')]

    for f in file_names:
        file_name = 'financials/' + f
        
        # ditch everything outside the data area
        print("***************************************************************")
        print(file_name)
    
        with open(file_name, 'rb') as f_in:
            bytes_in = f_in.read()
            s = bytes_in.decode('utf-8')
            data = re.findall(r'Income Statement(.+?)</tbody></table></div></section>', s)

            #print(data)
            
            # split into table cells
            split_data = revenue = re.findall(r'<td(.+?)</td', str(data))

            # for each table cell
            # need data between span /span but not all lines have an /span
            data_only = []
            for i in range(len(split_data)):
                d =  re.findall(r'<span data-reactid="[0-9]+">(.+?)</span>', str(split_data[i]))
                if len(d) > 0:
                    d[0] = re.sub(r',', '', str(d[0]))
                    data_only.append(d[0])
                else: data_only.append('0')

            #print(data_only)

            # split into rows of data
            rows_of_data = []
            row = []
            for i in range(len(data_only)):
                if i == 0:
                    row = ["Dates", data_only[1], data_only[2], data_only[3]]
                    rows_of_data.append(row)

                if i > 3:
                    try:        # if it's a number it's data
                        int(data_only[i])
                        row.append(data_only[i])
                    except:     # else it's a row description
                        rows_of_data.append(row) 
                        row = [data_only[i]]
                    
            # clean up
            rows_of_data = rows_of_data[1:]     # date row gets added in 2x, remove it
            
            clean_data = []             
            for i in rows_of_data:
                if len(i) > 1:                  # remove rows with text but no data
                    clean_data.append(i)
            #print(clean_data)

            clean_file_name = file_name + '.csv'
            with open(clean_file_name, 'w') as f:
                writer = csv.writer(f)
                writer.writerows(clean_data)


def parse_balance():

    file_names = [fn for fn in os.listdir(dir) if fn.endswith('balance.txt')]

     # ditch everything outside the data area
    for f in file_names:
        file_name = 'financials/' + f
        print("***************************************************************")
        print(file_name)
    
        
        with open(file_name, 'rb') as f_in:
            bytes_in = f_in.read()
            s = bytes_in.decode('utf-8')
            data = re.findall(r'Balance Sheet(.+?)</tbody></table></div></section>', s)

            #print(data)
            
            # split into table cells
            split_data = revenue = re.findall(r'<td(.+?)</td', str(data))

            # for each table cell
            # need data between span /span but not all lines have an /span
            data_only = []
            for i in range(len(split_data)):
                d =  re.findall(r'<span data-reactid="[0-9]+">(.+?)</span>', str(split_data[i]))
                if len(d) > 0:
                    d[0] = re.sub(r',', '', str(d[0]))
                    data_only.append(d[0])
                else: data_only.append('0')

            #print(data_only)

            # split into rows of data
            rows_of_data = []
            row = []
            for i in range(len(data_only)):
                if i == 0:
                    row = ["Dates", data_only[1], data_only[2], data_only[3]]
                    rows_of_data.append(row)

                if i > 3:
                    try:        # if it's a number it's data
                        int(data_only[i])
                        row.append(data_only[i])
                    except:     # else it's a row description
                        rows_of_data.append(row) 
                        row = [data_only[i]]
                    
            # clean up
            rows_of_data = rows_of_data[1:]     # date row gets added in 2x, remove it
            
            clean_data = []             
            for i in rows_of_data:
                if len(i) > 1:                  # remove rows with text but no data
                    clean_data.append(i)
            #print(clean_data)

            clean_file_name = file_name + '.csv'
            with open(clean_file_name, 'w') as f:
                writer = csv.writer(f)
                writer.writerows(clean_data)
        

def parse_cash():

    file_names = [fn for fn in os.listdir(dir) if fn.endswith('cash.txt')]

     # ditch everything outside the data area
    for f in file_names:
        file_name = 'financials/' + f
        print("***************************************************************")
        print(file_name)
    
        
        with open(file_name, 'rb') as f_in:
            bytes_in = f_in.read()
            s = bytes_in.decode('utf-8')
            data = re.findall(r'Balance Sheet(.+?)</tbody></table></div></section>', s)

            #print(data)
            
            # split into table cells
            split_data = revenue = re.findall(r'<td(.+?)</td', str(data))

            # for each table cell
            # need data between span /span but not all lines have an /span
            data_only = []
            for i in range(len(split_data)):
                d =  re.findall(r'<span data-reactid="[0-9]+">(.+?)</span>', str(split_data[i]))
                if len(d) > 0:
                    d[0] = re.sub(r',', '', str(d[0]))
                    data_only.append(d[0])
                else: data_only.append('0')

            #print(data_only)

            # split into rows of data
            rows_of_data = []
            row = []
            for i in range(len(data_only)):
                if i == 0:
                    row = ["Dates", data_only[1], data_only[2], data_only[3]]
                    rows_of_data.append(row)

                if i > 3:
                    try:        # if it's a number it's data
                        int(data_only[i])
                        row.append(data_only[i])
                    except:     # else it's a row description
                        rows_of_data.append(row) 
                        row = [data_only[i]]
                    
            # clean up
            rows_of_data = rows_of_data[1:]     # date row gets added in 2x, remove it
            
            clean_data = []             
            for i in rows_of_data:
                if len(i) > 1:                  # remove rows with text but no data
                    clean_data.append(i)
            #print(clean_data)

            clean_file_name = file_name + '.csv'
            with open(clean_file_name, 'w') as f:
                writer = csv.writer(f)
                writer.writerows(clean_data)
        

parse_income()
parse_cash()
parse_balance()


