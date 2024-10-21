import pandas as pd

def calculate_distance_matrix(file_path):
    # Read dataset
    df = pd.read_csv(file_path)
    
    # Create a pivot table for direct distances
    dist_matrix = pd.pivot_table(df, index='id_start', columns='id_end', values='distance', aggfunc='min', fill_value=0)
    
    # Ensure symmetry by filling in missing values with the reverse distances
    dist_matrix = dist_matrix.combine_first(dist_matrix.T)
    
    # Set the diagonal to 0 (distance from a point to itself)
    for i in dist_matrix.index:
        dist_matrix.loc[i, i] = 0
    
    return dist_matrix



def unroll_distance_matrix(dist_matrix):
    # Reset index to make ID columns
    unrolled_df = dist_matrix.reset_index().melt(id_vars='id_start', var_name='id_end', value_name='distance')
    
    # Remove rows where id_start equals id_end (no self-distances)
    unrolled_df = unrolled_df[unrolled_df['id_start'] != unrolled_df['id_end']]
    
    return unrolled_df



def find_ids_within_ten_percentage_threshold(unrolled_df, reference_id):
    # Calculate the average distance for each id_start
    avg_distances = unrolled_df.groupby('id_start')['distance'].mean().reset_index()
    
    # Get the reference average distance
    ref_avg_distance = avg_distances[avg_distances['id_start'] == reference_id]['distance'].values[0]
    
    # Calculate 10% threshold
    lower_bound = ref_avg_distance * 0.9
    upper_bound = ref_avg_distance * 1.1
    
    # Find IDs within the threshold range
    ids_within_threshold = avg_distances[(avg_distances['distance'] >= lower_bound) & 
                                         (avg_distances['distance'] <= upper_bound)]['id_start'].tolist()
    
    return sorted(ids_within_threshold)


def calculate_toll_rate(unrolled_df):
    # Define rate coefficients for each vehicle type
    rates = {
        'moto': 0.8,
        'car': 1.2,
        'rv': 1.5,
        'bus': 2.2,
        'truck': 3.6
    }
    
    # Add toll rate columns by multiplying the distance with the respective rate
    for vehicle, rate in rates.items():
        unrolled_df[vehicle] = unrolled_df['distance'] * rate
    
    return unrolled_df


def calculate_time_based_toll_rates(df)->pd.DataFrame():
    """
    Calculate time-based toll rates for different time intervals within a day.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
    # Write your logic here

    return df
