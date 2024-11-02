# Geosoft-GDB-Conversion
Work looking at converting Geosoft GDBs to useable open format for analysis, machine learning and AI

# Conversion format
- What to store as?
- Zarr / netcdf
    - Use xarray [not looked at tree format]
    - Depending if archiving or wanting to use for analysis
    - Although if you archive as netcdf you can kerchunk it later

- HDF5
    - Nested

# Example data
- Plenty of GDBs to be found
    - e.g. https://geoscience.data.qld.gov.au/ [search for geophysics, choose filetype on the left]
        - https://geoscience.data.qld.gov.au/data/magnetic/mg001116

