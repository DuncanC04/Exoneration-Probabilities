
'''
Duncan Craine
Febraury 24 2025
Machine Learning
Project 2
'''

#Packages
import pandas as pd
import numpy as np
from itertools import product
'''
#Datasets from excel
exoneration_df = pd.read_excel("publicspreadsheet.xlsx") 
conviction_df = pd.read_csv("2018 Crime Statistics.csv") 


feature_df = exoneration_df[['Race', 'State', 'Sex', 'Worst Crime Display']]
feature_df["EXONERATED"] = 1

df_selected = conviction_df[['MONRACE', 'HISPORIG', 'DISTRICT', 'MONSEX', 'OFFGUIDE']]
df_selected["EXONERATED"] = 0

#Convert DISTRICT to State
district_to_state = {
    0: "Maine",
    1: "Massachusetts",
    2: "New Hampshire",
    3: "Rhode Island",
    4: "Puerto Rico",
    5: "Connecticut",
    6: "New York",
    7: "New York",
    8: "New York",
    9: "New York",
    10: "Vermont",
    11: "Delaware",
    12: "New Jersey",
    13: "Pennsylvania",
    14: "Pennsylvania",
    15: "Pennsylvania",
    16: "Maryland",
    17: "North Carolina",
    18: "North Carolina",
    19: "North Carolina",
    20: "South Carolina",
    22: "Virginia",
    23: "Virginia",
    24: "West Virginia",
    25: "West Virginia",
    26: "Alabama",
    27: "Alabama",
    28: "Alabama",
    29: "Florida",
    30: "Florida",
    31: "Florida",
    32: "Georgia",
    33: "Georgia",
    34: "Georgia",
    35: "Louisiana",
    36: "Louisiana",
    37: "Mississippi",
    38: "Mississippi",
    39: "Texas",
    40: "Texas",
    41: "Texas",
    42: "Texas",
    43: "Kentucky",
    44: "Kentucky",
    45: "Michigan",
    46: "Michigan",
    47: "Ohio",
    48: "Ohio",
    49: "Tennessee",
    50: "Tennessee",
    51: "Tennessee",
    52: "Illinois",
    53: "Illinois",
    54: "Illinois",
    55: "Indiana",
    56: "Indiana",
    57: "Wisconsin",
    58: "Wisconsin",
    60: "Arkansas",
    61: "Arkansas",
    62: "Iowa",
    63: "Iowa",
    64: "Minnesota",
    65: "Missouri",
    66: "Missouri",
    67: "Nebraska",
    68: "North Dakota",
    69: "South Dakota",
    70: "Arizona",
    71: "California",
    72: "California",
    73: "California",
    74: "California",
    75: "Hawaii",
    76: "Idaho",
    77: "Montana",
    78: "Nevada",
    79: "Oregon",
    80: "Washington",
    81: "Washington",
    82: "Colorado",
    83: "Kansas",
    84: "New Mexico",
    85: "Oklahoma",
    86: "Oklahoma",
    87: "Oklahoma",
    88: "Utah",
    89: "Wyoming",
    90: "District of Columbia",
    91: "Virgin Islands",
    93: "Guam",
    94: "Northern Mariana Islands",
    95: "Alaska",
    96: "Louisiana"
}

monrace_mapping = {
    1: "White",
    2: "Black",
    3: "Native American",
    4: "Asian",
    5: "Multi-Racial",
    7: "Other",
    8: "Don't Know",
    ".": "Don't Know"
}

monsex_mapping = {
    0: "Male",
    1: "Female"
}

#Mapping to match data
df_selected["Sex"] = df_selected["MONSEX"].map(monsex_mapping)
df_selected["State"] = df_selected["DISTRICT"].map(district_to_state)
#Needed ChatGPT here to figure out how to get Hispanic considered in race
df_selected["Race"] = df_selected.apply(lambda row: "Hispanic" if row["HISPORIG"] == 1 #gets the hispanic value, if not then gets race value
                      else monrace_mapping.get(row["MONRACE"], "Other"), axis=1)

feature_df = feature_df[['Race', 'State', 'Sex', 'EXONERATED']]
df_selected = df_selected[['Race', 'State', 'Sex', 'EXONERATED']]
df_combined = pd.concat([feature_df, df_selected], ignore_index=True)

#print(feature_df.head(5))
#print(df_selected.head(5))
print(df_combined.head(5))
df_combined.to_excel("output.xlsx", index=False)  #Save to Excel for quicker runtime

#Calculate the number of years spanned from the dataset
year_span = exoneration_df["Date of Crime Year"].max() - exoneration_df["Date of Crime Year"].min()
print(year_span)

'''
#Above is data cleaning and combining, below is the probability calculations
df_combined = pd.read_excel("output.xlsx") #saves runtime

year_span = 68 #found above


#(P(EXONERATED))
numExonerations = df_combined[df_combined["EXONERATED"] == 1].shape[0]

#P(EXONERATED | Race)
race_prob = (df_combined.groupby("Race")["EXONERATED"].mean()) / year_span

#P(EXONERATED | State)
state_prob = (df_combined.groupby("State")["EXONERATED"].mean()) / year_span

#P(EXONERATED | Sex)
sex_prob = (df_combined.groupby("Sex")["EXONERATED"].mean()) / year_span

#Compute the combined probability for each (Race, State, Sex) combination
probabilities = {}

for race, state, sex in product(race_prob.index, state_prob.index, sex_prob.index):
    combined_prob = race_prob[race] * state_prob[state] * sex_prob[sex]
    probabilities[(race, state, sex)] = combined_prob

#Print results neatly
print(f"{'Race':<15}{'State':<20}{'Sex':<10}{'Combined Probability'}")
print("=" * 60)

for (race, state, sex), prob in probabilities.items():
    print(f"{race:<15}{state:<20}{sex:<10}{prob:.10f}") #Format Output - Too Many to Copy and Paste From Terminal

#Save results to a DataFrame
prob_df = pd.DataFrame(
    [(race, state, sex, prob) for (race, state, sex), prob in probabilities.items()],
    columns=["Race", "State", "Sex", "Combined Probability"]
)

#To excel file, so many probabilities
#prob_df.to_excel("Probabilities.xlsx", index=False)