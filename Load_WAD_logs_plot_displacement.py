# import pickle
# import pandas as pd
# import matplotlib.pyplot as plt
# import os
#
#
# # Load the Excel file
# file_path = r'C:\Users\or-m\OneDrive - Nova\Desktop\Junk\Intel TPT issues\MMSR Data\408MM2_8MonWW5.xlsx'
# #file_path = r'C:\Users\or-m\OneDrive - Nova\Desktop\Junk\Intel TPT issues\MMSR Data\404MM1_8MonWW5.xlsx'
# #file_path = r'C:\Users\or-m\OneDrive - Nova\Desktop\Junk\Intel TPT issues\MMSR Data\404MM1_WW6.xlsx'
# #file_path = r'C:\Users\or-m\OneDrive - Nova\Desktop\Junk\Intel TPT issues\MMSR Data\406MM1.xlsx'
# #file_path = r'C:\Users\or-m\OneDrive - Nova\Desktop\Junk\Intel TPT issues\MMSR Data\406MM2.xlsx'
# file_path =r'C:\Users\or-m\OneDrive - Nova\Desktop\Junk\Intel TPT issues\240712\WALogs\MM2\mm2VeloCD_bytime.xlsx'
# file_path =r'C:\Users\or-m\OneDrive - Nova\Desktop\Junk\Intel TPT issues\240712\WALogs\MM1\mm1VeloCD.xlsx'
# file_path =r'C:\Users\or-m\OneDrive - Nova\Desktop\Junk\Intel TPT issues\Data From Home Tool\1.xlsx'
# file_path=r'C:\Users\or-m\OneDrive - Nova\Desktop\Junk\Intel TPT issues\240712\WALogs\MM1\mm1VeloCD_firstAz.xlsx'
# file_path =r'C:\Users\or-m\OneDrive - Nova\Desktop\Junk\Intel TPT issues\Data From Home Tool\1.xlsx'
# df = pd.read_excel(file_path)
#
# q='WaferDisplacement'
# # Assume the CSV file has columns 'Value' and 'Label'
# values = df['WaferDisplacement']
# labels = df['RecipeName']
#
# # Generate the indices based on the row number
# indices = df.index
#
# # Filter out values above 2000
# filtered_df = df[df['WaferDisplacement'] <= 2000]
#
# # Compute average values for each label
# avg_values = filtered_df.groupby('RecipeName')['WaferDisplacement'].mean()
#
# # Get the filtered values, labels, and indices
# filtered_values = filtered_df['WaferDisplacement']
# filtered_labels = filtered_df['RecipeName']
# filtered_indices = filtered_df.index
#
# # Plotting
# plt.figure(figsize=(10, 6))
# plt.plot(filtered_indices, filtered_values, marker='o')
#
# # Add labels at the beginning of each batch, showing only selected letters
# previous_label = None
# for i, (index, value, label) in enumerate(zip(filtered_indices, filtered_values, filtered_labels)):
#     if label != previous_label:
#         truncated_label = label[1:16] if len(label) >= 16 else label[0:]
#         plt.text(index, value, truncated_label, fontsize=12, ha='right')
#         previous_label = label
#
#
# # Plot horizontal lines for average values of each label at relevant indices
# for label, avg_value in avg_values.items():
#     relevant_indices = filtered_df[filtered_df['RecipeName'] == label].index
#     plt.plot(relevant_indices, [avg_value] * len(relevant_indices), color='red', linestyle='-', label=f'Average {label}')
#
# file_name = os.path.basename(file_path)
# title = os.path.splitext(file_name)[0]  # Get the file name without extension
#
# plt.xlabel('Running Index')
# plt.ylabel('WaferDisplacement')
# plt.title(title)
# plt.grid(True)
# plt.show()
#
# plt.savefig(title+'.png')  # Save as PNG
# # Save the plot object using pickle
# with open(title, 'wb') as f:
#     pickle.dump(plt.gcf(), f)  # Save the current figure (gcf: get current figure)



#
#
#
# import pandas as pd
# import pickle
# load_path = file_path = r'C:\Users\or-m\OneDrive - Nova\Desktop\Junk\Intel TPT issues\MMSR Data\408MM2_8MonWW5plot.pkl'
# with open(load_path, 'rb') as f:
#     fig = pickle.load(f)  # Load the figure object
#
#
#
# save_path = r'C:\Users\or-m\OneDrive - Nova\Desktop\Junk\Intel TPT issues\MMSR Data\'title+'.pkl'  # Specify your path here
# with open(save_path, 'wb') as f:
#     pickle.dump(plt.gcf(), f)  # Save the current figure (gcf: get current figure)
# plt.clf()  # Clear the current figure to start a new one





#######################
####################
#########################
########################
#########################


import pickle
import pandas as pd
import matplotlib.pyplot as plt
import os


# Load the Excel file
file_path = r'C:\Users\omry-b\OneDrive - Nova\Desktop\4Omry_n_Yaakov\MMSR Data\408MM2_8MonWW5.xlsx'
# file_path =r'C:\Users\omry-b\OneDrive - Nova\Desktop\4Omry_n_Yaakov\WALogs\MM2\mm2VeloCD_bytime.xlsx'
# file_path =r'C:\Users\omry-b\OneDrive - Nova\Desktop\4Omry_n_Yaakov\WALogs\MM1\mm1VeloCD.xlsx'
df = pd.read_excel(file_path)

q='WaferDisplacementDir'
q='WaferDisplacement' # can be used to plot any trait
# Assume the CSV file has columns 'Value' and 'Label'
values = df[q]
labels = df['RecipeName']

# Generate the indices based on the row number
indices = df.index

# Filter out values above 2000
filtered_df = df[df[q] <= 2000]

# Compute average values for each label
avg_values = filtered_df.groupby('RecipeName')[q].mean()

# Get the filtered values, labels, and indices
filtered_values = filtered_df[q]
filtered_labels = filtered_df['RecipeName']
filtered_indices = filtered_df.index

# Plotting
plt.figure(figsize=(10, 6))
plt.plot(filtered_indices, filtered_values, marker='o')

# Add labels at the beginning of each batch, showing only the 8th to 13th letters
previous_label = None
for i, (index, value, label) in enumerate(zip(filtered_indices, filtered_values, filtered_labels)):
    if label != previous_label:
        truncated_label = label[1:16] if len(label) >= 16 else label[0:]
        plt.text(index, value, truncated_label, fontsize=12, ha='right')
        previous_label = label


# Plot horizontal lines for average values of each label at relevant indices
for label, avg_value in avg_values.items():
    relevant_indices = filtered_df[filtered_df['RecipeName'] == label].index
    plt.plot(relevant_indices, [avg_value] * len(relevant_indices), color='red', linestyle='-', label=f'Average {label}')

file_name = os.path.basename(file_path)
title = os.path.splitext(file_name)[0]  # Get the file name without extension

plt.xlabel('Running Index')
plt.ylabel(q)
plt.title(title)
plt.grid(True)
plt.show()

# plt.savefig(title+'.png')  # Save as PNG
# Save the plot object using pickle
# with open(title, 'wb') as f:
#     pickle.dump(plt.gcf(), f)  # Save the current figure (gcf: get current figure)



#
#
#
# import pandas as pd
# import pickle
# load_path = file_path = r'C:\Users\or-m\OneDrive - Nova\Desktop\Junk\Intel TPT issues\MMSR Data\408MM2_8MonWW5plot.pkl'
# with open(load_path, 'rb') as f:
#     fig = pickle.load(f)  # Load the figure object
#
#
#
# save_path = r'C:\Users\or-m\OneDrive - Nova\Desktop\Junk\Intel TPT issues\MMSR Data\'title+'.pkl'  # Specify your path here
# with open(save_path, 'wb') as f:
#     pickle.dump(plt.gcf(), f)  # Save the current figure (gcf: get current figure)
# plt.clf()  # Clear the current figure to start a new one