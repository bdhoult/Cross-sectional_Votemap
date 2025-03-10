The code attached is used to create a vote-map from seismic tomography data gathered from submachine.
Within the Supplementary Material is code for creating 3d or 2d vote-maps. - The code is formatted such that these instructions apply to both. The figures used in the paper all use 2d plots, but the 3d plots are more accurate to physical morphology, especially at greater depths.
The datasets used within this paper are attached in the Supplementary Material.
This Read Me file explains both how to reproduce the vote-maps in this paper and how to alter the code for different regions.

First open a python terminal and run the following code to ensure you have all the necessary libraries installed:

pip install numpy scipy matplotlib scikit-learn

Line 14: set the threshold to whatever value dv/v you wish to use as a minimum to count as a vote - I chose 0.2.
Line 45: if using this code with hot features such as mantle plumes, simply change (values > threshold) to (values < threshold)
Line 66: set your longitude range using the variables lon_min and lon_max
Line 92: set your chosen latitude using the variable lat
Line 94: set your depth range (2d only)
Line 162: set the full path to the folder containing your data files
Line 165: set the full path to the folder you want to save the vote map in
Line 177: set the threshold
Line 180: set the longitude range
Line 183: set the latitude and chosen filename for the votemap
