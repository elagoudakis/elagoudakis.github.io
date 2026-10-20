---
title: The (historic?) 2024 fire season
description: "Sentinel-5P carbon monoxide around the Arctic Circle for July 2021 to 2024, as the boreal fire season gets under way."
date: 2024-08-13 11:46:00 +0200
categories: [Sentinel-5P]
tags: [CO, arctic, canada, carbonmonoxide, S5P, airpollution, modis, fire]
kind: snapshot
acquired: "2021-07-01/2024-07-31"
location: { name: "Arctic Circle", lat: 62.0, lon: -115.0 }
credit: "Contains modified Copernicus Sentinel data (2021-2024); fire pixels: NASA FIRMS (MODIS)"
linkedin: https://www.linkedin.com/posts/lagoudakis_the-historic-2024-fire-season-the-activity-7224835150705025025-40OF
image:
  path: /assets/img/air-pollution-canada/canada_fires_s3_20240511.jpg
  alt: Smoke from wildfires spreading over western Canada, seen by Sentinel-3 on 11 May 2024
  caption: Wildfire smoke over western Canada, Sentinel-3, 11 May 2024
---


🔥 The 2024 fire season in the Northern Hemisphere is under way and may be as destructive as, or even more than, the 2023 season. 
The animation below utilizes data from the Copernicus Sentinel-5P (S5P) satellite, and illustrates the average carbon monoxide (CO) concentration around the Arctic Circle for July from 2021 to 2024. 
The primary sources of emissions are located in the boreal forests of Canada—Alberta, northeastern British Columbia, southern Northwest Territories—and Russia, particularly Yakutia.

{% include timeseries.html
   frames="/assets/img/air-pollution-canada/co_s5p_july_2021.webp, /assets/img/air-pollution-canada/co_s5p_july_2022.webp, /assets/img/air-pollution-canada/co_s5p_july_2023.webp, /assets/img/air-pollution-canada/co_s5p_july_2024.webp"
   labels="2021, 2022, 2023, 2024"
   alt="July average carbon monoxide around the Arctic Circle from Sentinel-5P"
   caption="Average CO concentration from Sentinel-5P for July 2021-2024. Credits: Copernicus Sentinel-5P"
   start=3 badge=false %}

🛰️ The fires behind these emissions show up clearly in the active fire data. The map below counts the MODIS fire pixels detected in July 2024 on a hexagonal grid: the densest cells sit over the same Canadian provinces and Yakutia that dominate the CO map.

![MODIS fire pixel count per hexagon around the Arctic Circle, July 2024](/assets/img/air-pollution-canada/modis_fire_pixels_hex_july2024.webp)
_Number of MODIS fire pixels in July 2024, aggregated on a hexagonal grid. Credits: NASA FIRMS (MODIS)_

📖 CO is an important atmospheric trace gas for understanding tropospheric chemistry. Main sources of CO are combustion of fossil fuels, biomass burning, and atmospheric oxidation of methane and other hydrocarbons. 
TROPOMI on the S5P satellite observes the CO global abundance exploiting clear-sky and cloudy-sky Earth radiance measurements in the 2.3 μm spectral range of the shortwave infrared (SWIR) part of the solar spectrum.

**Credits:** Copernicus Sentinel-5P