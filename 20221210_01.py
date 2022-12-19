#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np
import csv


#### setting input file, first with the given test data, then the actual data

# test data
#input_file = "https://raw.githubusercontent.com/pirosbogar/advent_of_code_2022/main/inputs/10/input_test.txt"

# actual data
input_file = "https://raw.githubusercontent.com/pirosbogar/advent_of_code_2022/main/inputs/10/input.txt"


# read input file
df = pd.read_csv(
                input_file, 
                 #sep=',',
                 skip_blank_lines=False, header = None, names = ['rows'])


# split the input file into two rows: the instruction, and the amount added to x (if any)
df[['instruction', 'amount']] = df['rows'].str.split(' ',expand=True)

# dropping the original input values
df = df[['instruction', 'amount']]

# changing the amount column data type to numeric
df['amount'] = pd.to_numeric(df['amount'])


print(df.head())
print(df.dtypes)


# creating an empty dataframe for the results
result = pd.DataFrame(columns = ['cycle', 'x_during', 'x_after'])

# for loop adding 1 to the cycle value if noop, and adding 2 to the cycle value and increasing x_after by N amount (addx N)
x_after = 1
cycle = 0

for a, b in zip(df.instruction, df.amount):
    if a == 'noop':
        cycle += 1
    elif a == 'addx':
        cycle += 2
        x_after += b
    result = result.append({'cycle' : cycle, 'x_after' : x_after},
                        ignore_index = True)


# cycle number of last cycle
result['cycle'].iloc[-1]


# setting x_during to the x_after value of the previous row
for i in range(1, len(result)):
    result.loc[i, 'x_during'] = result.loc[i-1, 'x_after']


# setting x_during = 1 at the beginning of the cycle
result['x_during'].iloc[0] = 1.0


result.head()


# creating empty df for a continuous cycle range
cycle_range = pd.DataFrame(columns = ['cycle'])


# while loop creating a continuous range of integers until it reaches the end of the cycles from the previous results
cycle = 0
while cycle < result['cycle'].iloc[-1]:
    cycle += 1
    cycle_range = cycle_range.append({'cycle' : cycle},
                            ignore_index = True)


cycle_range.head(-1)


# left joining the results from the instructions to the continuous list of cycle numbers
results_joined = cycle_range.merge(result, on='cycle', how='left')


# setting x = 1 at the beginning of the cycle
results_joined['x_after'].iloc[0] = 1.0
results_joined['x_during'].iloc[0] = 1.0


results_joined.head()


# forward filling the empty values (fill with previous value if empty)
results_joined = results_joined.fillna(method='ffill')


for i in range(1, len(results_joined)):
    results_joined.loc[i, 'x_during'] = results_joined.loc[i-1, 'x_after']


# selecting only the rows needed for part 1 of the task: cycle 20, 60, 100, etc.
results_p1 = results_joined.iloc[19::40, :]


results_p1.head(6)


# calculating the signal strengths
results_p1['signal_str'] = results_p1['cycle'] * results_p1['x_during']


results_p1


with pd.option_context('display.max_rows', None,
                       'display.max_columns', None,
                       'display.precision', 3,
                       ):
    print(results_joined)


# #### What is the sum of these six signal strengths?

results_p1['signal_str'].sum()


# ## Part 2: Drawing the image


# creating an empty string for the resulting image
crt_image = ''

# for loop drawing the image: line breaks after cycles divisible by 40, hasthag if x_during overlapping with sprite, dot otherwise
for a, b in zip(results_joined.cycle.astype(int), results_joined.x_during.astype(int)):
    if a % 40 in range(b, b + 3, 1) and a not in range(40,240,40):
        crt_image += '#'
    elif a % 40 in range(b, b + 3, 1) and a in range(40,240,40):
        crt_image += '#\n'
    elif a % 40 not in range(b, b + 3, 1) and a not in range(40,240,40):
        crt_image += '.'
    elif a % 40 not in range(b, b + 3, 1) and a in range(40,240,40):
        crt_image += '.\n'
    


# #### What eight capital letters appear on your CRT?

print(crt_image)




