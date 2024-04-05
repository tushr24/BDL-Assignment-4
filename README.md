# BDL-Assignment-4

# Objective
To use DVC and git for project version control.

# Dataset
An enormous database of environmental data, including oceanic, atmospheric, and geophysical data, is kept up to date by the National Centers for Environmental Information (NCEI). Every month, the NCEI archives data from more than 130 observing platforms totaling over 229 gigabytes.
A large portion of the data gathered by NOAA scientists, observation systems, and research projects is also archived by the NCEI. An extensive collection of environmental data from different time periods, observing systems, scientific fields, and geographical locations is managed by the NCEI.

# Task
* Take the files with the `n_loc` number from the ncei data website.
* Use the monthly average aggregates found in the file contents as the *ground truth* data.
* Compute the monthly averages using the *hourly* data available in the files.
* Compute R2 scores for the columns for each file.

# Setup
The commands are present in `comments.txt`. 
Run them individually to add stages and create the `dvc.yaml` file. 

# Information about the files
* The python file `download.py` downloads the `n_locs` number of files to a folder named `ncei_data`.
* The python file `prepare.py` file creates the **ground truth** (GT) data.
* The python file `process.py` file creates the calculated data.
* The python file `evaluate.py` file computed the R2 scores for the columns for each CSV file.
* The output `R2results.csv` file has the index as the number of the CSV file (if 1, then 1st file in the *ncei_data* folder).
