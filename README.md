# Geosoft-GDB-Conversion
Work looking at converting Geosoft GDBs to useable open format for analysis, machine learning and AI

## 📋 Important: Feasibility Analysis Available

**See [GDB_REVERSE_ENGINEERING_FEASIBILITY_ANALYSIS.md](GDB_REVERSE_ENGINEERING_FEASIBILITY_ANALYSIS.md)** for a comprehensive analysis of GDB reverse engineering feasibility.

**Key Finding**: While reverse engineering exploration is educational, **using the official [geosoft.gxpy](https://github.com/GeosoftInc/gxpy) Python API is strongly recommended** for all practical applications. See `src/example_conversion.py` for a working example.

---

# Geosoft GDB info
- "Geosoft database files are made up of straight binary data"
- https://help.seequent.com/Oasismontaj/2023.2/Content/ss/prepare_om/work_with_databases/c/oasis_databases.htm
	- To quote "proprietary 3-dimensional-file format"
		- Lines, channels, elements

## Data storage
### VV
- Vector Vectors - like (18,2) - 18 records, 0 has the actual measurements, 1 has the fiducial.
### VA
- Vectory Array - like (18,13) - 18 records, e.g. IP data so it can show up as plotted lines in the interface

- Given it is a 'spreadsheet' - you can get (0,) data as well for empty channels (or fields?)
        

# Example data
- Plenty of GDBs to be found
    - e.g. https://geoscience.data.qld.gov.au/ [search for geophysics, choose filetype on the left]
        - https://geoscience.data.qld.gov.au/data/magnetic/mg001116
     
# Binary Headers
- Need to compare the first part of a reasonable sample of files
  	- QLD has 300, perhaps pull those
		
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
    - Geoh5 
        - would need to implicitly make dummy coordinates


# Compression
- Looks like gzip signature found as reported by Loop/Fatiando 
    - but 1 and in the middle?

## binwalk
```bash
 binwalk -e DB_1116.gdb

DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
4996991       0x4C3F7F        Certificate in DER format (x509 v3), header length: 4, sequence length: 18436
11004320      0xA7E9A0        MySQL MISAM index file Version 8
11666672      0xB204F0        MySQL MISAM compressed data file Version 6
```

**Note**: binwalk results show false positives. See feasibility analysis for details.

---

# Recommended Approach: Official geosoft.gxpy API

For practical GDB file access, use the official Python API:

```bash
pip install geosoft
```

Example usage (see `src/example_conversion.py` for complete working code):

```python
import geosoft.gxpy.gdb as gxdb
import geosoft.gxpy.gx as gxp
import numpy as np

with gxp.GXpy() as gxp:
    gdb = gxdb.Geosoft_gdb.open('your_file.gdb')
    
    # List available data
    lines = gdb.list_lines()
    channels = gdb.list_channels()
    
    # Read data
    for line in lines:
        for channel in channels:
            data = gdb.read_channel_vv(line, channel)
            np_array = np.asarray(data)
            # Process your data here
```

**Resources**:
- Official API: https://github.com/GeosoftInc/gxpy
- Documentation: https://geosoftinc.github.io/gxpy/
- Full analysis: [GDB_REVERSE_ENGINEERING_FEASIBILITY_ANALYSIS.md](GDB_REVERSE_ENGINEERING_FEASIBILITY_ANALYSIS.md)

