# Geosoft-GDB-Conversion
Work looking at converting Geosoft GDBs to useable open format for analysis, machine learning and AI

# Conversion format
- What to store as?
- Zarr / netcdf
    - Use xarray [not looked at tree format]
    - Depending if archiving or wanting to use for analysis
    - Although if you archive as netcdf you can kerchunk it later

- HDF5
    - Nexted
