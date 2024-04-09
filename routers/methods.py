import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

def create_metrics(metrics: dict):
    # Convert the detections list to a DataFrame
    df = pd.DataFrame(metrics, columns=['timestamp', 'detection_id', 'detector_id', 'value'])
    
    # Ensure 'timestamp' is a datetime type for time series plotting
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    # Calculate basic statistics
    stats = {
        "max_value": df['value'].max(),
        "min_value": df['value'].min(),
        "avg_value": df['value'].mean()
    }
    
    # Setup for saving plots
    f = Path.cwd().joinpath("static")
    if not f.is_dir():
        f.mkdir()
    f1 = f.joinpath("detector_values_over_time.png")
    f2 = f.joinpath("avg_value_per_detector.png")

    # Plotting: Line plot of detector values over time
    plt.figure()
    for detector_id in df['detector_id'].unique():
        plt.plot('timestamp', 'value', data=df[df['detector_id'] == detector_id], label=f'Detector {detector_id}')
    plt.title('Detector Values Over Time')
    plt.xlabel('Time')
    plt.ylabel('Value')
    plt.legend()
    plt.savefig(f1)
    plt.close()

    # Bar plot of average values per detector
    avg_values_per_detector = df.groupby('detector_id')['value'].mean().reset_index()
    plt.figure()
    plt.bar(avg_values_per_detector['detector_id'], avg_values_per_detector['value'])
    plt.title('Average Value per Detector')
    plt.xlabel('Detector ID')
    plt.ylabel('Average Value')
    plt.savefig(f2)
    plt.close()
    
    return stats, str(f1), str(f2)
