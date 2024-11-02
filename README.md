# Geosoft-GDB-Conversion
Work looking at converting Geosoft GDBs to useable open format for analysis, machine learning and AI

# Geosoft GDB info
- https://help.seequent.com/Oasismontaj/2023.2/Content/ss/prepare_om/work_with_databases/c/oasis_databases.htm
	- To quote "proprietary 3-dimensional-file format"
		- Lines, channels, elements
		
## Lines
- Name - TYPE number.version:flight

## Channels
- Names have no spaces

## Elements
- byte
- unsigned 2-byte integer 
- short 2 int
- long 4 int
- float 4
- double 8
- string

Channels

## Fiducial
- Incrementing field
		

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

