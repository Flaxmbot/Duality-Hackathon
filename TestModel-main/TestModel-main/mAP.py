import pandas as pd

df = pd.read_csv('/home/pikazu/Downloads/results.csv')

# Print last epoch mAP50 and mAP50-95
print("==== Last Epoch Metrics ====")
print(df.tail(1)[['metrics/mAP50(B)', 'metrics/mAP50-95(B)']])
