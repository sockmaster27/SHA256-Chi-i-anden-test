# En lille hjælpefil, så det kan tjekkes at det ser nogenlunde rigtigt ud.
import pickle


with open("frequency_table_65536", "rb") as f:
    (frequency_table, end_value) = pickle.load(f)

# Selve frekvenstabellen er meget stor.
print(f"frequency table: {frequency_table}")
print(f"total: {sum(frequency_table)}")
print(f"max: {max(frequency_table)}")
print(f"min: {min(frequency_table)}")
print(f"avg: {sum(frequency_table) / len(frequency_table)}")

# end_value er teknisk set den næste værdi som burde beregnes, men det betyder ikke rigtig noget.
print(f"last value computed: {end_value}")
