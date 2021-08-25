# show the date
date
# format the date as follows in dd-mm-yy format:
date +"%d-%m-%y"
date +"%y-%m-%d"
date +"%Y-%m-%d"

# Simply display the current time:
date "+%T"

# print the date of the day before yesterday, run:
date --date='2 days ago'

# Want to see the day of year of Christmas in the current year? Try:
date --date='25 Dec' +%j

# Display the current full month name and the day of the month:
date '+%B %d

# current timestamp
date '+%s'

# Convert Unix Timestamp to Date
date -d "1970-01-01 956684800 sec GMT"
date -d "1970-01-01 $(date +%s) sec GMT"

# Convert Unix Date to Timestamp
date -d "2000-01-01 GMT" '+%s'
date -d $(date) '+%s'