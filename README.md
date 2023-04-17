# Example: Geocoding

## Summary

The **demo.py** file in this repository shows how to use the Nominatim API to geocode addresses. Nominatium is the search engine associated with OpenStreetMap.

## Input Data

There are no input files: the addresses to be geocoded are built into **demo.py**. In a production version, they could be read from an input file instead.

## Deliverables

None. This is an example only and there's nothing due.

## Instructions

1. Run demo.py and have a look at the PNG file it produces.

1. Load `demo.gpkg` into QGIS and have a look at it there as well.

## Tips

* Nominatium often returns multiple records for each search since there may be several things near the address. Each result has a detailed JSON object that describes what it is. If you just need the coordinates, it may be sufficient to pick any one of the records since the differences in the coordinates will be small.