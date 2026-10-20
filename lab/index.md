---
layout: page
title: Component lab
permalink: /lab/
description: Demo page for DScape's interactive components.
sitemap: false
---

A test page for the interactive pieces that can be dropped into any post. It isn't linked from the menu.

## Before/after compare

Drag the handle, click anywhere on the image, or focus it and use the arrow keys.

{% include compare.html
   before="/assets/img/a-hot-middle-east-morning/me_20240612_truecolor.webp"
   after="/assets/img/a-hot-middle-east-morning/me_20240612_lst.webp"
   before_label="True colour"
   after_label="Land surface temperature"
   alt="Eastern Mediterranean and Middle East on 12 June 2024"
   caption="12 June 2024, 10:50 local time. Credits: Contains modified Copernicus Sentinel data (2024); base map: Esri" %}

Usage in a post:

```liquid
{% raw %}{% include compare.html
   before="/assets/img/slug/before.webp"
   after="/assets/img/slug/after.webp"
   before_label="17 Aug 2024"
   after_label="20 Aug 2024"
   alt="What both images show"
   caption="Optional caption with credits" %}{% endraw %}
```

Both images must show the same area at the same pixel size. Optional: `start=30` sets where the handle begins (percent from the left).

## Time series

Press play, pick a year, or use the arrow keys.

{% include timeseries.html
   frames="/assets/img/air-pollution-canada/co_s5p_july_2021.webp, /assets/img/air-pollution-canada/co_s5p_july_2022.webp, /assets/img/air-pollution-canada/co_s5p_july_2023.webp, /assets/img/air-pollution-canada/co_s5p_july_2024.webp"
   labels="2021, 2022, 2023, 2024"
   alt="July average carbon monoxide around the Arctic Circle from Sentinel-5P"
   caption="Credits: Copernicus Sentinel-5P"
   badge=false %}
