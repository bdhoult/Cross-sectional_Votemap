import numpy as np
from scipy.spatial import cKDTree
import os
import matplotlib.pyplot as plt



def load_data(filepath):
    # Load data from a .txt file and return as a numpy array
    data = np.loadtxt(filepath)
    return data

# Create a vote map from multiple datasets.
def create_vote_map(data_files, threshold=0.2):
    
    # Initialize a list to store all points and their values
    all_points = []
    all_values = []

    # Load all datasets
    for file in data_files:

        data = load_data(file)
        points = data[:, :3]  # X, Y, Z coordinates
        values = data[:, 3]   # Value (%)
        all_points.append(points)
        all_values.append(values)

    # Combine all points into a single array
    combined_points = np.vstack(all_points)
    combined_values = np.hstack(all_values)

    # Create a KDTree for nearest neighbor search
    tree = cKDTree(combined_points)

    # Initialize a vote map
    vote_map = np.zeros_like(combined_values)

    # Iterate over each dataset and count votes
    for points, values in zip(all_points, all_values):
        # Find indices of nearest points in the combined dataset
        _, indices = tree.query(points, k=1)
        
        # Count votes where the value exceeds the positive threshold
        vote_map[indices] += (values > threshold)

    return combined_points, vote_map

# Convert x,y,z to lat,lon,depth
def xyz_to_lat_lon_depth(points):

    x, y, z = points[:, 0], points[:, 1], points[:, 2]
    
    # Calculate longitude and latitude
    rxy = np.sqrt(x**2 + y**2)
    lon = np.arctan2(y, x) * 180.0 / np.pi
    lat = np.arctan2(z, rxy) * 180.0 / np.pi
    
    # Calculate depth
    rxyz = np.sqrt(x**2 + y**2 + z**2)
    depth = 6371.0 - rxyz # Convert distance from centre of Earth to Depth using Earth's radius in km
    
    return lat, lon, depth

# Filter data to only show points between two given longitudes
def filter_by_longitude(points, vote_map, lon_min=-80, lon_max=-40):

    # Convert XYZ coordinates to latitude, longitude, and depth
    lat, lon, depth = xyz_to_lat_lon_depth(points)
    
    # Create a mask for the specified longitude range
    mask = (lon >= lon_min) & (lon <= lon_max)
    
    # Apply the mask to the points and vote map
    filtered_points = points[mask]
    filtered_vote_map = vote_map[mask]
    filtered_lon = lon[mask]
    filtered_depth = depth[mask]
    
    return filtered_lon, filtered_depth, filtered_vote_map

# Convert longitude for x axis
def lon_to_km(lon, lat):
    # Convert longitude to kilometers at a constant latitude
    R = 6371  # Earth's radius in km
    lon_rad = np.deg2rad(lon)
    lat_rad = np.deg2rad(lat)
    dx = R * np.cos(lat_rad) * lon_rad
    return dx

# Create a 2D votemap at a given latitude and save it in a given folder
def save_vote_map_as_2d_plot(lon, depth, vote_map, save_folder, filename="votemap_.png", num_files=None, lat=-37):
    # Filter to show only depths less than 1000 km
    mask = depth < 1500
    lon = lon[mask]
    depth = depth[mask]
    vote_map = vote_map[mask]

    # Convert longitude to kilometers
    lon_km = lon_to_km(lon, lat)






    # Create a 2D plot
    fig, ax = plt.subplots(figsize=(10, 6))


    # Set colours 
    cmap = plt.get_cmap('viridis')  # Use the 'viridis' colourmap
    norm = plt.Normalize(vmin=1, vmax=num_files)  # Count votes from 1 to however many files were read. (exclude zero)
    colours = cmap(norm(vote_map))  # Apply colourmap
    colours[vote_map == 0] = [0, 0, 0, 0]  # Set transparent for 0 votes

    # Scatter plot with colour representing the number of votes
    scatter = ax.scatter(lon_km, depth, c=colors, s=10)

    # Add a colour bar
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    cbar = plt.colorbar(sm, ax=ax, shrink=0.8)
    cbar.set_label('Number of Votes')

    # Set labels
    ax.set_xlabel('Distance (from 0° Longitude) (km)')
    ax.set_ylabel('Depth (km)')
    ax.set_title(f'Vote Map: Distance vs. Depth (Latitude = {lat}°)')

    # Invert the y-axis to show depth increasing downward
    ax.invert_yaxis()

    # Set equal scaling
    ax.set_aspect('equal')

    # Add dashed horizontal lines at 660 km and 1000 km depth
    ax.axhline(y=660, color='blue', linestyle='--', linewidth=1, label='660 km')
    ax.axhline(y=1000, color='red', linestyle='--', linewidth=1, label='1000 km')







    # Save the plot to the specified folder
    save_path = os.path.join(save_folder, filename)
    plt.savefig(save_path, dpi=300, bbox_inches='tight', transparent=True)
    plt.close()

    print(f"2D vote map saved as {save_path}")

#Get a list of all .txt files in a folder
def get_txt_files_from_folder(folder_path):
    txt_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.txt')]
    return txt_files

# Main script
if __name__ == "__main__":
    # Path to the folder containing the .txt files
    data_folder = r""  

    # Path to the folder where the vote map image will be saved
    save_folder = r""

    # Get all .txt files in the folder
    data_files = get_txt_files_from_folder(data_folder)

    # Check if any files were found
    if not data_files:
        print("No .txt files found in the specified folder.")
    else:
        print(f"Found {len(data_files)} .txt files in the folder.")

        # Create the vote map
        points, vote_map = create_vote_map(data_files, threshold=0.2)

        # Filter points between two longitude lines
        filtered_lon, filtered_depth, filtered_vote_map = filter_by_longitude(points, vote_map, lon_min=-80, lon_max=-40)

        # Save the vote map as a 2D plot
        save_vote_map_as_2d_plot(filtered_lon, filtered_depth, filtered_vote_map, save_folder, filename="votemap_-37.png", num_files=len(data_files), lat=-37)
