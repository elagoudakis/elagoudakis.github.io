---
title: A Hot Middle East Morning
description: "Sentinel-3 land surface temperature over the Middle East on 12 June 2024, and why LST is not the same as air temperature."
date: 2024-07-21 19:12:00 +0200
categories: [Sentinel-3]
tags: [lst, temperature, europe, mediterranean]
kind: story
acquired: "2024-06-12"
location: { name: "Middle East", lat: 31.5, lon: 37.0 }
credit: "Contains modified Copernicus Sentinel data (2024); base map: Esri"
linkedin: https://www.linkedin.com/pulse/hot-middle-east-morning-emmanouil-manos-lagoudakis-2oekf/
image:
  path: /assets/img/a-hot-middle-east-morning/Middle_East_S3B_LST_20240612_v1_banner.jpg
  alt: relationship between LST and landscape features
---

### LST of the Middle East

This land surface temperature (LST) image was acquired on **June 12, 2024**, at 10:50 AM local time by the SLSTR instrument onboard the Copernicus Sentinel-3 satellite.

![Sentinel-3 land surface temperature over the Middle East on 12 June 2024](/assets/img/a-hot-middle-east-morning/me_lst_20240612.webp)
_LST of the Middle East, 12 June 2024, 10:50 am local time. Credits: Copernicus Sentinel-3_

In many areas, the LST exceeds 60 degrees Celsius. As expected, water bodies, mountainous regions, and coastal areas have lower temperatures.

### Differences with AT

Unlike air temperature (AT), which is measured at a specific height (usually 2 meters), LST represents the thermal radiation emitted from Earth's surface. 
In simpler terms, it's how hot the ground would feel to your touch.  

LST can fluctuate more dramatically than AT. For example, on a sunny day, land surfaces like asphalt can absorb significant solar radiation, causing the LST to be much higher than the AT. Conversely, at night, land surfaces lose heat faster than air, sometimes resulting in a lower LST.

The table below shows the differences between LST and AT at selected locations visible on the map.

| Location | LST (°C) | AT (°C) | Difference (°C) |
| --- | ---: | ---: | ---: |
| Amman, Jordan | 45 | 32 | +13 |
| Cairo, Egypt | 46 | 31 | +15 |
| Damascus, Syria | 46 | 33 | +13 |
| Antakya, Türkiye | 37 | 37 | 0 |
| Tabuk, Saudi Arabia | 54 | 33 | +21 |
| Nicosia, Cyprus | 49 | 36 | +13 |
{: .data-table}

_Land surface temperature (LST) and air temperature (AT), 12 June 2024, 11:00 local time_

### Things to Consider When Interpreting LST Maps:

* __Spatial resolution:__ The instrument takes one reading per unit area. For example, the SLSTR instrument of Sentinel-3 has a resolution (unit area) of 1 square kilometre. All the variations of temperature within this square kilometre are represented with one reading.
* __Temporal resolution:__ Sentinel-3 takes one reading per day. The mapped LST quantifies the temperature at the time of acquisition of the data.
* __Conversion from radiance to LST:__ A series of algorithms that include calibration, conversion to brightness temperature, emissivity correction, atmospheric correction.. This process can introduce errors.
* __Cloud filtering:__ Clouds can affect readings, so data filtering is crucial. Clouds are also not uniform. Thin clouds might escape filtering and affect the quality of the LST measurement.

###  **The Bottom Line:**

LST quantifies the energy emitted by the ground at the time of image acquisition. It can also indicate perceived heat and potential discomfort, but it's not the same as AT and should be used with a clear disclaimer. Combining LST and AT data can help us understand how we experience heat and heatwaves in a warming world.

**Credits:** Copernicus Sentinel-3 for the LST data and Esri for the satellite base map
