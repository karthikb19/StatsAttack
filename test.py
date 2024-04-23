import pandas as pd
import datetime

def calc_duration(start_time, end_time):
  start_time = datetime.datetime.strptime(start_time, "%I:%M:%S %p")
  end_time = datetime.datetime.strptime(end_time, "%I:%M:%S %p")
  duration = end_time - start_time
  duration = duration.total_seconds() / 3600
  duration = round(duration * 4) / 4
  if (duration < 0):
    duration += 24

  return duration

def reformat_name(og_name):
  name_parts = og_name.split(", ")
  last_name = name_parts[0]
  first_name_with_id = name_parts[1]
  first_name, remaining = first_name_with_id.split(" (")
  id_ = remaining[:-1]
  reformatted_name = f"{id_} {first_name.split()[0]} {last_name}"
  return reformatted_name, f"{first_name.split()[0]} {last_name}", id_

# Load the CSV file
df = pd.read_csv('csv_calendar.csv',
                 index_col=None,
                 usecols=[
                     'Subject', 'Start Date', 'Start Time', 'End Time',
                     'Meeting Organizer', 'Required Attendees',
                     'Optional Attendees', 'Description', 'End Date',
                     'End Time', 'All day event', 'Reminder on/off',
                     'Reminder Date', 'Location', 'Categories'
                 ])

df = df.rename(
    columns={
        "Subject": "Topic",
        "Start Date": "Date of the interaction",
        "Start Time": "Session Duration",
        "Meeting Organizer": "Staff",
        "Optional Attendees": "Additional Staff",
        "Location" : "Primary User Name",
        "Categories" : "Primary User's Computing ID"
    })
start_time_index = df.columns.get_loc("Session Duration")
end_time_index = df.columns.get_loc("End Time")
staff_index = df.columns.get_loc("Staff")
primary_user_name_index = df.columns.get_loc("Primary User Name")
primary_user_id_index = df.columns.get_loc("Primary User's Computing ID")
for i in range(len(df)):
  #reformatting start time
  start_time = df.iloc[i, start_time_index]
  end_time = df.iloc[i, end_time_index]
  duration = calc_duration(start_time, end_time)
  df.iloc[i, start_time_index] = duration

  #reformatting name
  name = (str) (df.iloc[i, staff_index])
  reformatted_name, name, id = reformat_name(name)
  df.iloc[i, staff_index] = reformatted_name
  df.iloc[i, primary_user_name_index] = name
  df.iloc[i, primary_user_id_index] = id
  

df = df.rename(
    columns={
        "End Date": 'School',
        "End Time": "ARL Interaction Type",
        "All day event": "Pre-post-time",
        "Reminder on/off": "RDS+SNE Group",
        "Reminder Date": "Medium"
    })

index = 0
for element in df["Description"]:
  element_lines = element.split('\n')
  #initialize variables to store information
  school = ""
  arl_interaction = ""
  pre_post_time = ""
  rds_sne = ""
  medium = ""
  description = ""

  for line in element_lines:
    label, text = line.split(":", 1)
    label = label.strip()
    text = text.strip()

    if label == "School":
      school = text
    if label == "ARL Interaction Type":
      arl_interaction = text
    if label == "Pre-post-time":
      pre_post_time = text
    if label == "RDS+SNE Group":
      rds_sne = text
    if label == "Medium":
      medium = text
    if label == "Description":
      description = text

  df.iloc[index, df.columns.get_loc("School")] = school
  df.iloc[index, df.columns.get_loc("ARL Interaction Type")] = arl_interaction
  df.iloc[index, df.columns.get_loc("Pre-post-time")] = (str)(pre_post_time)
  df.iloc[index, df.columns.get_loc("RDS+SNE Group")] = rds_sne
  df.iloc[index, df.columns.get_loc("Medium")] = medium
  df.iloc[index, df.columns.get_loc("Description")] = description

  index += 1

df.to_csv('csv_calendar_new.csv', index=False)
