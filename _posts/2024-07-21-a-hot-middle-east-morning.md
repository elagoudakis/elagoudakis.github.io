---
title: A Hot Middle East Morning
date: 2024-07-21 19:12:00 +0200
categories: [Sentinel-3]
tags: [lst, temperature, europe, mediterranean]
image:
  path: /assets/img/a-hot-middle-east-morning/Middle_East_S3B_LST_20240612_v1_banner.jpg
  alt: relationship between LST and landscape features
comments: true
---

### LST of the Middle East

This land surface temperature (LST) image was acquired on **June 12, 2024**, at 10:50 AM local time by the SLSTR instrument onboard the Copernicus Sentinel-3 satellite.

![Sentinel-3 LST](https://media.licdn.com/dms/image/D4D12AQGdFg1AaUXP_g/article-inline_image-shrink_1500_2232/0/1718258448324?e=1727308800&v=beta&t=trL3rSkPFcQ7rKZeSaBkrznq8HQ2TCR6GNMLlMhfE4E)
_LST of the Middle East, 12 June 2024, 10:50 am local time. Credits: Copernicus Sentinel-3_

In many areas, the LST exceeds 60 degrees Celsius. As expected, water bodies, mountainous regions, and coastal areas have lower temperatures.

### Differences with AT

Unlike air temperature (AT), which is measured at a specific height (usually 2 meters), LST represents the thermal radiation emitted from Earth's surface. 
In simpler terms, it's how hot the ground would feel to your touch.  

LST can fluctuate more dramatically than AT. For example, on a sunny day, land surfaces like asphalt can absorb significant solar radiation, causing the LST to be much higher than the AT. Conversely, at night, land surfaces lose heat faster than air, sometimes resulting in a lower LST.

The table below shows the differences between LST and AT at selected locations visible on the map.

![AT vs LST readings](https://media.licdn.com/dms/image/D4D12AQEokxeg4lbK5w/article-inline_image-shrink_1500_2232/0/1718283545833?e=1727308800&v=beta&t=gaUIazqR4IbtQP8PNVFWnzU480i3Zs5952cNspZ6-2A)


### Things to Consider When Interpreting LST Maps:

* __Spatial resolution:__ The instrument takes one reading per unit area. For example, the SLSTR instrument of Sentinel-3 has a resolution (unit area) of 1 square kilometre. All the variations of temperature within this square kilometre are represented with one reading.
* __Temporal resolution:__ Sentinel-3 takes one reading per day. The mapped LST quantifies the temperature at the time of acquisition of the data.
* __Conversion from radiance to LST:__ A series of algorithms that include calibration, conversion to brightness temperature, emissivity correction, atmospheric correction.. This process can introduce errors.
* __Cloud filtering:__ Clouds can affect readings, so data filtering is crucial. Clouds are also not uniform. Thin clouds might escape filtering and affect the quality of the LST measurement.

###  **The Bottom Line:**

LST quantifies the energy emitted by the ground at the time of image acquisition. It can also indicate perceived heat and potential discomfort, but it's not the same as AT and should be used with a clear disclaimer. Combining LST and AT data can help us understand how we experience heat and heatwaves in a warming world.

This article was also posted on my [__Linkedin__](https://www.linkedin.com/pulse/hot-middle-east-morning-emmanouil-manos-lagoudakis-2oekf/?trackingId=LUxMceQwTOqOoecJXAkrig%3D%3D) account.

**Credits:** Copernicus Sentinel-3 for the LST data and Esri for the satellite base map


{% if page.comments %}

<div id="disqus_thread"></div>
<script>
    /**
    *  RECOMMENDED CONFIGURATION VARIABLES: EDIT AND UNCOMMENT THE SECTION BELOW TO INSERT DYNAMIC VALUES FROM YOUR PLATFORM OR CMS.
    *  LEARN WHY DEFINING THESE VARIABLES IS IMPORTANT: https://disqus.com/admin/universalcode/#configuration-variables    */
    /*
    var disqus_config = function () {
    this.page.url = PAGE_URL;  // Replace PAGE_URL with your page's canonical URL variable
    this.page.identifier = PAGE_IDENTIFIER; // Replace PAGE_IDENTIFIER with your page's unique identifier variable
    };
    */
    (function() { // DON'T EDIT BELOW THIS LINE
    var d = document, s = d.createElement('script');
    s.src = 'https://digital-scape.disqus.com/embed.js';
    s.setAttribute('data-timestamp', +new Date());
    (d.head || d.body).appendChild(s);
    })();
</script>
<noscript>Please enable JavaScript to view the <a href="https://disqus.com/?ref_noscript">comments powered by Disqus.</a></noscript>

{% endif %}