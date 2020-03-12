import _csv as csv
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

#Function that accepts two file paths as parameters ('strings') to indicate IMPORT location and EXPORT location

def reformat_data(file_origin, file_destination):

    if file_origin == None:
        return print("File Origin Not indicated At First Parameter")

    elif file_destination == None:
        return print("File Destination Not Indicated At Second Parameter")

    else:
        with open(file_origin, 'r') as file_object:
            reader = csv.reader((file_object))
            next(reader)

            # Create list of lists with sub-lists containing each logged event

            data = []
            for row in reader:
                data.append(row)

            #Relevant columns

            location = [item[0] for item in data]
            weekday = [item[4] for item in data]
            start_times = []
            end_times = []
            traffic = [item[5] for item in data]

            #Convert start_time and end_time timestamp to YYYY-MM-dd HH:mm format

            log_start_time = [item[1] for item in data]
            for start_time_string in log_start_time:
                log_start_time_correct_format = datetime.strptime(start_time_string, '%m/%d/%Y %H:%M')
                start_times.append(log_start_time_correct_format)

            log_end_time = [item[2] for item in data]
            for end_time_string in log_end_time:
                log_end_time_correct_format = datetime.strptime(end_time_string, '%m/%d/%Y %H:%M')
                end_times.append(log_end_time_correct_format)

            #Zip list of all relevant data
            #endtimes redacted
            zipped_lst = list(zip(location, weekday, start_times, traffic))

            #Remove events logged on Saturday or Sunday

            chicago_weekday_data = []

            for i in zipped_lst:

                saturday = i[1] == 'Saturday'
                sunday = i[1] == 'Sunday'
                chicago = i[0] == 'Chicago'
                before_eight_am = i[2].hour < 8
                after_nine_pm = i[2].hour > 21

                if saturday or sunday:
                    pass
                else:
                    if chicago:
                        if before_eight_am:
                            pass
                        elif after_nine_pm:
                            pass
                        else:
                            chicago_weekday_data.append(i)
                    else:
                        pass

            row_labels = []
            col_labels = []
            traffic_value = []

            for i in chicago_weekday_data:

                weekday = i[1]
                hours = i[2].hour

                if weekday not in row_labels:
                    row_labels.append(weekday)
                else:
                    pass

                if hours not in col_labels:
                    col_labels.append(hours)
                else:
                    pass

                traffic_value.append(i[-1])

            traffic_value = list(map(int, traffic_value))

            test = np.array_split(traffic_value, 5)

        test_table = pd.read_csv(file_destination)
        #print(test_table.head())

        sns.heatmap(test, annot = True)

        plt.show()

        #Export Relevant Data to Destination as .csv

        #with open(file_destination, 'w', newline = '') as new_file_object:
            #the_writer = csv.writer(new_file_object)
            #the_writer.writerow(col_labels)
            #for i in test:
                #the_writer.writerow(i)

        #return print("Success! Hourly Data Re-Formatted, New File Exported to " + file_destination)

reformat_data('C:\\Users\pheavlin\OneDrive - payette.com\Desktop\HourlyExportSample.csv', 'C:\\Users\pheavlin\OneDrive - payette.com\Desktop\chicago2.csv')
