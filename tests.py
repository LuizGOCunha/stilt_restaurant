import csv
# I could simply use csv, but it wasn't working for some reason, so i decided to do it myself
# I don't know if this is more or less impressive
def return_complex_countercsv_list(clear_file=False):
    '''This function just splits the csv file by line, then by comma, returning a 2D list'''
    with open('counter.csv', 'r') as csv_file:
        csv_string = csv_file.read()
        csv_rows_list = csv_string.split('\n')
        csv_complex_rows_list = []
        for row in csv_rows_list:
            list_row = row.split(',')
            csv_complex_rows_list.append(list_row)
        if clear_file:
            # Dont panic, this is just so we can clear the file
            with open('counter.csv', 'w') as _:
                pass

    return csv_complex_rows_list


def write_data_to_countercsv(line_list):
    '''Receives a list with the name and number of food order to be inserted into the csv file'''
    line = line_list[0] + ',' + line_list[1] + '\n'
    with open('counter.csv', 'a') as csv_file:
        csv_file.write(line)
        

def remove_line_from_countercsv(id):
    '''Receives an id to be remove, then pulls all data from csv, store it in a variable, 
    then puts it back in excluding the line with the mentioned id. 
    REMEMBER!!: The id must be a string, otherwise the function won't work'''
    csv_list = return_complex_countercsv_list(clear_file=True)
    for line_list in csv_list:
        try:
            if line_list[1] == id:
                print('hey')
                continue
            else: 
                write_data_to_countercsv(line_list)
        except IndexError:
            continue


print(return_complex_countercsv_list())





