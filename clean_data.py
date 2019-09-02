import pandas as pd

castles = pd.read_csv(r"input_data/castles.csv")
cities = pd.read_csv(r"input_data/cities.csv")
flixbus = pd.read_csv(r"input_data/flixbus.csv")
gardens = pd.read_csv(r"input_data/gardens.csv")
museums = pd.read_csv(r"input_data/museums.csv")
zoos = pd.read_csv(r"input_data/zoos.csv")

# CLEANING CITIES
# Split coordinates column into two separate
cities["coordinates"] = cities["coordinates"].str.replace("[", "")
cities["coordinates"] = cities["coordinates"].str.replace("]", "")
cities["coordinates"] = cities["coordinates"].str.replace("'", "")

cities["coordinates"] = cities["coordinates"].apply(lambda x: x.split(","))

cities["latitude"] = cities["coordinates"].apply(lambda x: x[0])
cities["longitude"] = cities["coordinates"].apply(lambda x: x[1])

cities.drop(columns="coordinates", inplace=True)

# Extract city name from URL, make it proper case, replace "-" with whitespace
cities["city"] = cities["city"].apply(lambda x: x.split("/")[-2])

cities["city"] = cities["city"].str.title()

cities["city"] = cities["city"].str.replace("-", " ")

# Create new subfolder clean_data first
cities.to_csv('clean_data/cities_clean.csv', index=False)

# CLEANING FLIXBUS
# Replace "-" with whitespace for consistency with cities
flixbus["city"] = flixbus["city"].str.replace("-", " ")

# cities in flixbus dataset that don't have their coordinates in cities dataset
temp = flixbus.merge(cities, on="city", how="left")
print(temp.isna().sum())

missing_data = temp["city"][temp["latitude"].isna()]
missing_data.to_csv('clean_data/missing_data.csv', index=False, header="city")

# A lot of nan values, missing data copied manually from https://www.gps-coordinates.net/
missing_data_filled_in = pd.read_csv(r"clean_data/missing_data_filled_in.csv", sep=";")

# Append filled in data to cities, merge with flixbus
cities = cities.append(missing_data_filled_in, ignore_index=True)

flixbus = flixbus.merge(cities, how="left", on="city")

flixbus.to_csv('clean_data/flixbus_clean.csv', index=False)

# CLEANING MUSEUMS
# Replace "-" with whitespace for consistency with cities
museums["city"] = museums["city"].str.replace("-", " ")

museums = museums.merge(cities, how="left", on="city")

print(museums.isna().sum())  # 17 missing values, ignored as they are not so crucial here

museums.to_csv('clean_data/museums_clean.csv', index=False)

# Delete rows with missing coordinates
museums = museums[museums["latitude"].notna()]

# CLEANING GARDENS
gardens = gardens.merge(cities, how="left", on="city")

print(gardens.isna().sum())  # 12 missing values, ignored as they are not so crucial here

# Delete rows with missing coordinates
gardens = gardens[gardens["latitude"].notna()]

gardens.to_csv('clean_data/gardens_clean.csv', index=False)

# CLEANING ZOOS
zoos = zoos.merge(cities, how="left", on="city")

print(zoos.isna().sum())  # 2 missing values, ignored as they are not so crucial here

# Delete rows with missing coordinates
zoos = zoos[zoos["latitude"].notna()]

zoos.to_csv('clean_data/zoos_clean.csv', index=False)
