# By Marshall Saltz
"""
The following parameters may be adjusted.
To change the type of test, uncomment any ONE
of the flag lines. Default is straight test.

precision1 - coarse precision
precision2 - fine precision
interval - interval at which to save information,
must be a factor of generation number
init_num - number of initial hands generated.
mutations_num - number of times to mutate initial generation
random_mutations_num - loop number of mutations
carrier_num - number of times to combine winning file
even_odd_num - number of times to combine even and odd files
winner_count - amount of top files
trim_val - for plotting purposes
angles_count - number of angles around center point to test
percent_threshold - largest percent of finger length a segment can be
radius - distance of each finger from center point
"""

# Area test:
#flag = "area"

# Angle test:
flag = "angle"

# Straight test:
#flag = "straight"

precision1 = 0.01
precision2 = 0.005
interval = 50
init_num = 30
mutations_num = 20
random_mutations_num = 5
carrier_num = 5
even_odd_num = 5
winner_count = 20
trim_val = 0.01
angles_count = 8
percent_threshold = 95
radius = 0.039/2
