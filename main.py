import csv
import requests


def main():
    # Read NYTimes Covid Database
    download = requests.get(
        "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv"
    )
    decoded_content = download.content.decode("utf-8")
    file = decoded_content.splitlines()
    reader = csv.DictReader(file)

    # Construct 14 day lists of new cases for each states
    new_cases = calculate(reader)

    # Create a list to store selected states
    states = []
    print("Choose one or more states to view average COVID cases.")
    print("Press enter when done.\n")

    while True:
        state = input("State: ")
        if state in new_cases:
            states.append(state)
        if len(state) == 0:
            break

    print(f"\nSeven-Day Averages")

    # Print out 7-day averages for this week vs last week
    comparative_averages(new_cases, states)



# TODO: Create a dictionary to store 14 most recent days of new cases by state
def calculate(reader):
    new_cases={}
    previous_cases={}
    for row in reader:
        if row['state'] not in new_cases:
            new_cases[row['state']]=[]
            new_cases[row['state']].append(row['cases'])
            previous_cases[row['state']]=row['cases']
        elif len(new_cases[row['state']])<14:
            state_name=str(row['state'])
            cases=int(row['cases'])-int(previous_cases[state_name])
            new_cases[row['state']].append(cases)
            previous_cases[state_name]=row['cases']
        else:
            new_cases[row['state']]=new_cases[row['state']][1:14]
            cases=int(row['cases'])-int(previous_cases[row['state']])
            new_cases[row['state']].append(cases)
            previous_cases[row['state']]=row['cases']
    return new_cases


def comparative_averages(new_cases, states):
    for state in states:
        cases=list(new_cases[state])
        first7avg=sum(cases[0:7])/7
        last7avg=sum(cases[7:14])/7
        try:
            change = ((last7avg-first7avg) / first7avg) * 100
            if change > 0:
                print(f"{state} had a 7-day average of {round(last7avg)} and an increase of {round(change)}%")
            elif change < 0:
                print(f"{state} had a 7-day average of {round(last7avg)} and an decrease of {round(change)}%")
            else:
                print(f"{state} had a 7-day average of {round(last7avg)} and no change")
        except ZeroDivisionError:
            print(f"{state} had a 7-day average of {round(last7avg)}")






main()
