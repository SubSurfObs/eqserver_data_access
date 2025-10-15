# eqserver_data_access


## Future access

From mid 2025, public stations in the University of Melbourne Seismic network are available through AusPass. Legacy data are beign converted from an EqServer archive, and will be incremenatally added to AusPass. 

In the meantime, this repository contains some information on how to access data through HTTP query. 

## EqServer HTTP query

Our public legacy server (2012–2025) running at:

https://meiproc.earthsci.unimelb.edu.au/eqserver/

Download waveform data directly via the legacy server using an HTTP query:

```
https://meiproc.earthsci.unimelb.edu.au/eqserver/eqwaveextractor?year=2025&month=1&day=1&hour=0&minute=0&duration=120&servernum=0&conttrig=0&sitechoice=list&sitelist=STATIONNAME&siteradius=&closesite=&radius=&latitude=&longitude=&fileformat=miniseed&getwave=Get+Waveform
```

If this doesn't work, it is probablyt because the server needs a reboot. 


#### Parameters

- `year`, `month`, `day`, `hour`, `minute`: Start time of the request
- `duration`: Duration in minuts
- `sitelist`: Replace `STATIONNAME` with the desired station code (e.g., `MELU`)
- `fileformat`: Can be either:
  - `miniseed`: Downloads only the MiniSEED waveform file
  - `mszip`: Downloads a `.zip` archive containing both MiniSEED and StationXML metadata

#### Example  

To see a seismogram from the Mw 5.9, 2021 Woods Point Earthquake, download 2 minutes of data from station `CLIF` starting at **UTC 2021-09-21 23:15:00**:

```
http://meiproc.earthsci.unimelb.edu.au/eqserver/eqwaveextractor?year=2021&month=9&day=21&hour=23&minute=15&duration=2&servernum=0&conttrig=0&sitechoice=list&sitelist=CLIF&siteradius=&closesite=&radius=&latitude=&longitude=&fileformat=mszip&getwave=Get+Waveform
```


> **Note:**  
> Replace `miniseed` with `mszip` to receive a zipped archive that includes both the waveform data (MiniSEED) and corresponding StationXML metadata.
> A free waveform viewer can be downloader here: https://www.src.com.au/downloads/waves/

```
http://agoslog.earthsci.unimelb.edu.au/eqserver/eqwaveextractor?year=2021&month=9&day=21&hour=23&minute=15&duration=2&servernum=0&conttrig=0&sitechoice=list&sitelist=CLIF&siteradius=&closesite=&radius=&latitude=&longitude=&fileformat=mszip&getwave=Get+Waveform
```

```
http://agoslog.earthsci.unimelb.edu.au/eqserver/eqwaveextractor?year=2021&month=9&day=21&hour=23&minute=15&duration=2&servernum=0&conttrig=0&sitechoice=list&sitelist=CLIF&siteradius=&closesite=&radius=&latitude=&longitude=&fileformat=mszip&getwave=Get+Waveform
```

