# Tech Stack and Feasibility: GTA-Style Worldwide Map App (as of November 2026)

Research method note: Research ran on 2026-11-23. It used about 20 web searches and fetches. Direct page fetches of maplibre.org and developers.google.com were blocked by the session network, so findings for those come from search-result snippets of official pages. They were not read in full. The search tool also summarized results, so treat its quotes as close paraphrases, not guaranteed verbatim text. Items marked **[background knowledge, unverified this session]** come from the researcher's prior knowledge (cutoff mid-2026). They were not confirmed against a live source here and should be checked.

## Rendering libraries: which allow total style control, licences, and 2026 status

### Takeaway
For a fully custom game-map look at hobby cost, the strongest choice is MapLibre GL JS. It is open source (BSD-3) and on a fast-moving v6 line in 2026. You control every style element: colours, road casings, glyphs, sprites, extrusions, sky/fog, and custom WebGL layers. Mapbox GL JS v3 is more polished in 3D (the Standard style, lighting, night presets), but it is proprietary and tied to Mapbox billing. Google and Apple allow only limited restyling.

### Cited Findings
**MapLibre GL JS**
- MapLibre GL JS v6.0.0 reportedly shipped on 22 July 2026. Its headline breaking changes are that WebGL2 is now mandatory and the package is ESM only. This comes from a third-party blog, so confirm it against the official changelog. — [geo.malagis.com](https://geo.malagis.com/maplibre-gl-js-v6-mandatory-webgl-and-esm-only.html)
- The MapLibre August 2026 newsletter, as summarized by search, reports six GL JS releases that month: 6.2.0, 6.3.0, 6.4.0, 6.4.1, 6.5.0 and 6.6.0. — [MapLibre Newsletter August 2026](https://maplibre.org/news/2026-09-02-maplibre-newsletter-august-2026/)
- An unpkg README exists for maplibre-gl@6.16.0, so the v6 line had reached at least 6.16 by late 2026. The release date was not found. — [unpkg maplibre-gl@6.16.0](https://unpkg.com/maplibre-gl@6.16.0/README.md)
- v5 was released in December 2025, and v5.23.0 was noted in April 2026. v6 arrived about 8 months after v5. — [MapLibre newsletters index](https://maplibre.org/categories/newsletter); [MapLibre Newsletter April 2026](https://maplibre.org/news/2026-05-02-maplibre-newsletter-april-2026/)
- The OpenStreetMap website itself bumped maplibre-gl from 5.13.0 to 5.14.0 in December 2025, which is evidence of adoption. — [OSM rails-dev list](https://lists.openstreetmap.org/pipermail/rails-dev/2025-December/045808.html)
- GL JS is BSD-3-Clause licensed. The MapLibre org also maintains MapLibre Native, the Martin tile server and the Maputnik visual style editor. — [MapLibre GitHub org](https://github.com/maplibre); [GL JS README](https://raw.githubusercontent.com/maplibre/maplibre-gl-js/main/README.md)
- A MapLibre style is a JSON document that controls what data is drawn, in what order, and how. — [MapLibre GitHub org](https://github.com/maplibre)

**Mapbox GL JS v3 / Standard style**
- GL JS v3 and the mobile Maps SDK v11 make Mapbox Standard the default style. Standard has four light presets: Day, Dusk, Dawn and Night. — [Mapbox migrate-to-v3 guide](https://docs.mapbox.com/mapbox-gl-js/guides/migrate-to-v3/)
- When Standard is imported into a custom style, its settings go in a `config` property. A custom colour theme is set with `theme: custom` plus a base64 lookup-table (LUT) image. Custom layers added on top of Standard need extra configuration to work with its lighting, for example `fill-emissive-strength`. v3 added AmbientLight and DirectionalLight APIs, marked experimental. — [Mapbox migrate-to-v3 guide](https://docs.mapbox.com/mapbox-gl-js/guides/migrate-to-v3/); [Mapbox Standard docs](https://docs.mapbox.com/map-styles/standard/)
- Detailed road rendering in Standard covers 71 major cities in 29 countries as of September 2026. It requires GL JS v3.30 or Maps SDK v11.30. This comes from a Japanese-language Mapbox blog post. — [Mapbox blog (JA): new road detail](https://www.mapbox.com/ja/blog/new-road-detail-in-mapbox-standard)
- Mapbox says MapLibre shares the same API surface and style format and can consume Mapbox tile APIs. Tiles fetched through a third-party library are billed per tile request, not per map load. — [Mapbox: Use Mapbox APIs in MapLibre](https://docs.mapbox.com/help/dive-deeper/mapbox-in-maplibre/)
- The licence situation is a community concern. Since v2 (2020), Mapbox GL JS has been under a proprietary licence that requires use with Mapbox services, which triggered the MapLibre fork. Users have worried about further restrictions. — [MapLibre discussion #71](https://github.com/maplibre/maplibre-gl-js/discussions/71); [MapTiler: MapLibre fork announcement](https://www.maptiler.com/news/2021/01/mapbox-gl-open-source-fork/)

**Google Maps JS API (cloud-based map styling)**
- Cloud-based styling raised the limit on customizations to "over 250 for most browsers". The older JSON styling was capped by URL character limits. — [Google blog: new maps customization features](https://mapsplatform.google.com/intl/en/resources/blog/introducing-new-maps-customization-features/)
- Data-driven styling (for boundaries and uploaded datasets in GeoJSON, CSV or KML) requires a vector map with a map ID. It is not supported on raster JS maps or Static Maps. — [DDS boundaries get started](https://developers.google.com/maps/documentation/javascript/dds-boundaries/start); [DDS datasets overview](https://developers.google.com/maps/documentation/javascript/dds-datasets/overview)
- The release notes list known issues with text stroke styling and with 3D building strokes. — [Cloud-based maps styling release notes](https://developers.google.com/maps/documentation/javascript/cbms-release-notes)

**Apple MapKit JS**
- `colorScheme` switches between light and dark only for the Standard and MutedStandard map types. — [MapKit JS colorScheme](https://developer.apple.com/documentation/mapkitjs/mapconstructoroptions/colorscheme.md)
- `pointOfInterestFilter` can include or exclude categories, or include or exclude all of them. Older forum reports (MapKit JS 5.61.1) say the filter had no effect and did not cover road annotations. — [pointOfInterestFilter doc](https://developer.apple.com/documentation/mapkitjs/pointofinterestfilter.md); [Apple forum thread 679674](https://developer.apple.com/forums/thread/679674)
- Satellite and hybrid map types reportedly force dark mode. — [Apple forum thread 738104](https://developer.apple.com/forums/thread/738104)

### Inferences
- Ranking by style control: MapLibre GL JS is roughly equal to Mapbox GL JS (custom style) and well above Google cloud styling, which is above Apple MapKit JS (essentially fixed). Mapbox Standard's LUT theming plus Night preset is the fastest route to a moody game-like 3D look. A hand-built MapLibre style gives more total control.
- **[background knowledge, unverified this session]** MapLibre supports `fill-extrusion` for 3D buildings, `sky` and fog, raster-dem terrain and hillshade, a globe projection (since v5), and `CustomLayerInterface`. A custom layer can draw raw WebGL or Three.js into the map's GL context, which lets you add custom shaders. Full-screen post-processing (bloom, CRT, outline shaders) is not built in. You would need to render the map canvas into your own WebGL pipeline, for example by reading the map canvas as a texture, or use a CSS `filter` on the canvas as a cheap hack.
- **[background knowledge, unverified this session]** Other options:
  - **deck.gl** (MIT, vis.gl / OpenJS) layers on top of MapLibre or Google. It is good for animated route trips (TripsLayer) and custom effects, but it is not a basemap renderer.
  - **Leaflet** (BSD-2; a 2.0 line was in alpha/beta in 2025–26) is raster-first and needs plugins for vector tiles. It is a poor fit for a rotating heading-up minimap.
  - **OpenLayers** (BSD-2) supports vector tiles and rotation, and can apply Mapbox style JSON via ol-mapbox-style. It is powerful but more verbose.
  - **CesiumJS** (Apache-2.0) is a full 3D globe. It is good for Google Photorealistic 3D Tiles or OSM Buildings, but heavy for stylized 2D cartography.
  - **Game engines:** Cesium for Unity/Unreal is Apache-2.0. Mapbox's Unity SDK was deprecated years ago. Three.js plus a custom vector-tile renderer gives total artistic control (toon or cel shading), but you must build labels, collision and tiling yourself, which is a large effort.
  - All of these should be version-checked.

### Gaps
- The exact latest MapLibre GL JS version and date for November 2026 could not be confirmed, because maplibre.org fetches were blocked. Check [npm maplibre-gl](https://www.npmjs.com/package/maplibre-gl) and GitHub releases.
- The current Mapbox GL JS v3.x release number for November 2026 was not confirmed.
- Current 2026 versions and status for deck.gl, Leaflet 2.0, OpenLayers, CesiumJS, and the Cesium/ArcGIS Unity/Unreal SDKs were not researched this session.

## How far can Google/Apple be restyled, and do their terms allow a "filter" over their tiles?

### Takeaway
Google allows recolouring and hiding features (over 250 rules via cloud styling) and annotations. Its guidelines say you must not "significantly alter" how Google Maps looks, and some Google content may not be combined with non-Google maps. Apple MapKit JS offers essentially only light/dark and POI filtering. Neither is a realistic base for a GTA-style re-skin. A CSS or shader filter over their tiles is at best a grey area and likely against the terms.

### Cited Findings
- Google's geo guidelines say cloud-based styling lets users recolour components and toggle visibility. They also state: "you must not significantly alter how Google Maps … would look online". The page covers Google products generally and points commercial uses to Maps Platform. — [Google geoguidelines](https://www.google.ca/permissions/geoguidelines)
- On the Map Tiles API, you must not obscure Google's data attribution, and you must make clear which parts of the map are Google's. You may add your own 3D objects only if they are not derived from Photorealistic 3D Tiles. — [Map Tiles API policies](https://developers.google.com/maps/documentation/tile/policies)
- The Service Terms say Directions API content must not be used "in conjunction with a non-Google map". — [Google Maps Platform Service Terms](https://cloud.google.com/maps-platform/terms/maps-service-terms/)
- Google Map Tiles API usage is governed by the customer's agreement with Google, which may differ from the public defaults. — [Map Tiles API policies](https://developers.google.com/maps/documentation/tile/policies)

### Inferences
- If the developer uses Google Routes or Places, those results generally may not be shown on a MapLibre/OSM map. This pushes the project toward an all-OSM or all-open stack for routing and search as well as tiles.
- **[background knowledge, unverified this session]** The Google Maps Platform Terms generally prohibit modifying or creating derivative works of Google Maps content and restrict caching and prefetching. Applying a heavy CSS `filter` or a shader to Google tiles to change their look is therefore likely non-compliant. Apple's MapKit JS agreement similarly bars altering Apple map content.

### Gaps
- I could not fetch the full Google Maps Platform Terms text (developers.google.com was blocked) or Apple's MapKit JS terms to quote the exact derivative-work and caching clauses.

## Basemap vector tile sources (schemas, hosted providers, self-hosting, planet size)

### Takeaway
For a hobby project, the cheapest robust option is either OpenFreeMap (free, no key, OpenMapTiles schema) or a self-hosted Protomaps planet PMTiles file (about 120 GB for z0–15) on object storage. Both are OSM-based with global coverage, and both pair natively with MapLibre.

### Cited Findings
- A Protomaps planet PMTiles file is roughly 120 GB for zoom levels 0–15. An earlier figure from 2023 was about 100 GB. Each extra zoom level roughly doubles the size, and `pmtiles extract --maxzoom` can cut it down. — [Protomaps downloads docs](https://docs.protomaps.com/basemaps/downloads); [SOTMUS 2023 talk](https://bdon.github.io/presentations/SOTMUS2023)
- Daily planet builds are published at maps.protomaps.com/builds and mirrored on Source Cooperative as `tiles/v3.pmtiles`. A planet rebuild takes about 2 hours on a high-end machine. — [Source Cooperative: protomaps/openstreetmap](https://source.coop/protomaps/openstreetmap); [Protomaps build docs](https://docs.protomaps.com/basemaps/build)
- Protomaps maintains open styles and tooling in the protomaps/styles repo. — [protomaps/styles](https://github.com/protomaps/styles)
- A July 2026 Geocode Earth blog post covers Protomaps as "a map you can actually own", which shows continued 2026 activity. — [Geocode Earth blog, 14 July 2026](https://geocode.earth/blog/2026/protomaps-a-map-you-can-actually-own/)
- OpenFreeMap:
  - It has no limits on map views or requests, and no registration, API keys or cookies.
  - Its style URL (for example `tiles.openfreemap.org/styles/liberty`) works directly with MapLibre.
  - It is provided as-is and may change. It offers no search or routing.
  - Self-hosting it needs about 300 GB of SSD.
  - [OpenFreeMap GitHub](https://www.github.com/hyperknot/openfreemap); [openfreemap.org](https://openfreemap.org); [Simon Willison on OpenFreeMap (Sept 2024)](https://simonwillison.net/2024/Sep/28/openfreemap)
- Planetiler (which generates OpenMapTiles-schema tiles) needs roughly 300 GB of free disk for a planet build, with modest RAM if run slowly. — [OSM wiki: Sequentially generate planet mbtiles](https://wiki.openstreetmap.org/wiki/Sequentially-generate-planet-mbtiles)

### Inferences
- **[background knowledge, unverified this session]** Tile schemas:
  - OpenMapTiles is used by MapTiler and OpenFreeMap.
  - The Protomaps Basemap schema is its own schema.
  - Shortbread is used by VersaTiles, which is free and CC0/open and can be self-hosted as a single `.versatiles` file.
  - Mapbox Streets v8 is proprietary.
  - Overture Maps offers GeoParquet themes (buildings, transportation, places, base, divisions) rather than ready-made tiles. Overture publishes PMTiles extracts for exploration.
- **[background knowledge, unverified this session]** Hosted providers:
  - Freemium with free hobby tiers: MapTiler, Stadia Maps, Mapbox, Geoapify, Thunderforest.
  - Paid or usage-based cloud services: Esri, AWS Location Service (which uses Esri, HERE or Open Data styles), Azure Maps.
  - Pricing is covered by another researcher.
- Only PMTiles (Protomaps or custom-built) and VersaTiles are designed as a single static file served from object storage with HTTP Range requests and no tile server.

### Gaps
- I did not verify the current Protomaps planet size in November 2026 from the builds directory, or the current VersaTiles planet size.
- Overture's 2026 release cadence and tile offerings were not researched in detail.

## Style authoring workflow and specific game-map effects

### Takeaway
Use Maputnik, which is free and open source, or MapTiler Customize, or Mapbox Studio if you are on Mapbox, to edit a MapLibre or Mapbox style JSON. Start from an existing open style such as Protomaps or OpenFreeMap Liberty. Most game effects are style properties plus a little custom code. The minimap mask, player arrow and animated route are simple. Real post-processing shaders and fog-of-war are the harder parts.

### Cited Findings
- Maputnik is a MapLibre-maintained visual style editor. — [MapLibre GitHub org](https://github.com/maplibre)
- Protomaps publishes its basemap styles as open source in a repo with two core parts (style generation and themes). — [protomaps/styles](https://github.com/protomaps/styles)
- Mapbox Standard supports custom colour themes via a LUT image, plus Day/Dusk/Dawn/Night light presets. This is a quick path to a neon night look. — [Mapbox migrate-to-v3 guide](https://docs.mapbox.com/mapbox-gl-js/guides/migrate-to-v3/)
- An existing navigation app built on MapLibre GL JS, OSRM and Nominatim rotates the map to the user's heading. It is a reference for heading-up behaviour. — [itch.io post](https://itch.io/post/13953957)
- An existing GTA V map project uses Leaflet (GPL). It is a reference for game-style UI but not a real-world basemap. — [dukeofsussex/gta-v-map](https://github.com/dukeofsussex/gta-v-map)

### Inferences
**[background knowledge, unverified this session]**
- **Flat high-contrast palette and thick cased roads:** use pairs of line layers. Draw a wider dark "casing" layer under a narrower fill layer, with `line-width` interpolated by zoom. Set paint colours and hide clutter layers. This is easy.
- **Fonts and glyphs:** build SDF glyph PBFs from TTF/OTF using `maplibre/font-maker` or `openmaptiles/fonts` (node-fontnik). Host them at a `{fontstack}/{range}.pbf` URL. Licensing matters: GTA's actual font ("Pricedown") is a commercial typeface, and Rockstar's iconography is copyrighted. Use look-alike open fonts and original icons.
- **Sprites:** generate a sprite sheet (`sprite.png`, `sprite.json`, plus @2x versions) from SVGs with `spreet` or `@maplibre/maplibre-gl-style-spec`-adjacent tools. You can also add images at runtime with `map.addImage()` for blips.
- **Water and land:** for stylized water, use flat fill colours plus `fill-pattern` textures. Animated water needs a custom layer.
- **Dark/neon night mode:** use a second style or runtime `setPaintProperty`. Glow can be faked with blurred duplicate line layers (`line-blur`).
- **Extruded buildings:** use a `fill-extrusion` layer on building height attributes, which exist in the OpenMapTiles and Protomaps schemas.
- **Terrain and hillshade:** use a raster-dem source plus `hillshade` and `terrain`. Free DEM tiles include AWS Terrain Tiles (Terrarium) and Mapterhorn.
- **Circular minimap:** run a second small map instance in a `div` with `border-radius: 50%; overflow: hidden`, or a CSS `clip-path`. Call `map.setBearing(heading)` on each compass event and `easeTo` the GPS position, keeping the player arrow fixed at the centre. Main-map interactions are disabled on the minimap.
- **Pulsing or chevron player arrow:** use an HTML Marker with a CSS animation, or a canvas-animated `StyleImageInterface` (the official "animated pulsing dot" example pattern).
- **Animated route line:** use `line-dasharray` animation, or `line-gradient` with `line-progress` (needs `lineMetrics: true`), or deck.gl TripsLayer.
- **Fog of war:** store visited H3 cells or geohashes (for example with h3-js). Render a world-covering polygon with holes, or a fill layer of undiscovered cells. A canvas or WebGL custom layer gives soft edges. This is the hardest effect to make look good and perform at global scale.

### Gaps
- I did not find a published open-source "GTA-style real-world map" style or minimap demo built on MapLibre or Mapbox. The search turned up none, which may simply mean none were found.

## Mobile options and device sensor caveats

### Takeaway
Two paths exist. A PWA or Capacitor wrapper reuses the MapLibre GL JS code with the least effort, but web cannot do background location and iOS needs a tap-gated compass permission. A native rewrite (MapLibre React Native with Expo dev builds, Flutter MapLibre, or MapLibre Native) gives real background GPS and better performance but needs separate code.

### Cited Findings
- MapLibre React Native has an Expo config plugin. It cannot run in Expo Go and needs a development build. — [MapLibre RN Expo setup](https://maplibre.org/maplibre-react-native/docs/setup/expo)
- Version history and current state:
  - v10.0.0 was released in January 2025, followed by 10.2.x and v11 alphas.
  - The npm metadata for v11.3.3 lists peer dependencies of expo >=54 and react-native >=0.80.
  - [newreleases: maplibre-react-native v10.0.0](https://newreleases.io/project/github/maplibre/maplibre-react-native/release/v10.0.0); [jsdelivr: @maplibre/maplibre-react-native@11.3.3 package.json](https://cdn.jsdelivr.net/npm/@maplibre/maplibre-react-native@11.3.3/package.json)
- A community Flutter MapLibre package exists. — [flutter-maplibre-gl](https://github.com/XanderD99/flutter-maplibre-gl)
- Since iOS 13, Safari requires an explicit permission request tied to a user gesture before exposing orientation data. iOS supplies a non-standard `webkitCompassHeading` (0–360°). Other platforms use `deviceorientationabsolute` with `alpha`. — [dev.to: browser compass](https://dev.to/toolswebs1/building-a-compass-in-the-browser-how-the-deviceorientation-api-actually-works-3f37); [Apple forum 128376](https://developer.apple.com/forums/thread/128376)
- A WebKit bug causes `requestPermission()` to be denied after a Web Worker postMessage round-trip, even within a gesture. — [WebKit bug 271099](https://bugs.webkit.org/show_bug.cgi?id=271099)
- Chromium has shipped a DeviceOrientation permission request API. — [blink-dev Intent to Ship](https://groups.google.com/a/chromium.org/d/msgid/blink-dev/df21cbad-a913-4d3b-8eca-f60ec051cfb1n%40chromium.org)

### Inferences
- **[background knowledge, unverified this session]** Web Geolocation `watchPosition` stops when the tab or PWA is backgrounded or the screen locks, on both iOS and Android. There is no background geolocation for web. Capacitor plugins (for example `@capacitor-community/background-geolocation`) or native SDKs are needed for that. Heading from the GPS `coords.heading` is only valid while moving, so a minimap should blend compass heading when stationary with course when moving.
- The Mapbox Maps SDKs (v11) for iOS and Android are proprietary and need a token. MapLibre Native is BSD and free.

### Gaps
- The current MapLibre Native iOS and Android version numbers (November 2026) and Flutter package maintenance status were not verified.

## Routing engines and hosting feasibility

### Takeaway
Self-hosting planet-scale routing is not hobby-friendly. OSRM car routing needs well over 64–130 GB of RAM and Valhalla planet builds need large disk and RAM. Use a hosted API's free tier, such as openrouteservice, GraphHopper, Stadia (Valhalla) or Mapbox, or self-host Valhalla or OSRM for a single country or region.

### Cited Findings
- OSRM hardware figures:
  - In 2017, planet car routing needed just under 64 GB of RAM to serve. Preprocessing needed about 175 GB of RAM plus about 280 GB of disk. The foot profile needed about 248 GB. [osrm-talk 2017](https://lists.openstreetmap.org/pipermail/osrm-talk/2017-July/001465.html)
  - In 2021, an operator reported 130 GB of RAM for car and 165 GB for foot or bike. [osrm-talk 2021](https://lists.openstreetmap.org/pipermail/osrm-talk/2021-May/001997.html)
  - Zero-downtime updates need about twice the RAM.
  - These figures are dated, and OSM has grown since.
- OSRM keeps a Disk and Memory Requirements wiki page (figures as of v5.26, November 2021). It could not be read this session. — [OSRM wiki](https://github.com/Project-OSRM/osrm-backend/wiki/Disk-and-Memory-Requirements)
- Valhalla figures:
  - One community guide uses defaults of 24 GB disk and 6 GB RAM for regional builds.
  - Another suggests 32 GB of RAM and 4 cores as a starting point. Serving needs much less memory than building.
  - Geofabrik regional extracts are recommended over the planet for local use.
  - [community-scripts Valhalla](https://community-scripts.org/scripts/valhalla); [docker-valhalla discussion #90](https://www.github.com/gis-ops/docker-valhalla/discussions/90); [Installing Valhalla with Docker (valh)](https://cran.ms.unimelb.edu.au/web/packages/valh/vignettes/install-valhalla.html)
- openrouteservice needs about 128 GB of RAM for a planet build. — [ORS system requirements](https://giscience.github.io/openrouteservice/run-instance/system-requirements)
- Google Directions content must not be used with a non-Google map. — [Google Maps Platform Service Terms](https://cloud.google.com/maps-platform/terms/maps-service-terms/)

### Inferences
- **[background knowledge, unverified this session]** Licences:
  - OSRM: BSD-2
  - Valhalla: MIT
  - GraphHopper: Apache-2.0
  - openrouteservice: GPL-3
  - All are free and open source. Hosted options with free hobby tiers include openrouteservice (HeiGIT), GraphHopper Directions API, Stadia Maps, Mapbox Directions and Geoapify. Pricing is out of scope.
- Valhalla returns a shape you can draw directly as a GeoJSON line. Map-matched turn-by-turn navigation is extra work.

### Gaps
- There is no authoritative 2026 Valhalla planet build requirement. Treat 64 GB or more of RAM and about 100–200 GB of disk as unverified estimates. Current 2026 OSRM planet numbers were not found.

## Geocoding/search and POI data: what is free at hobby scale

### Takeaway
At hobby scale, use a hosted freemium geocoder (MapTiler, Geoapify, Stadia, Mapbox) or the public Photon or Nominatim with strict fair-use. POI blips can come from vector tiles (the POI layers in OpenMapTiles and Protomaps), Overpass queries, or the open Overture and Foursquare datasets.

### Cited Findings
- Nominatim (OSMF public server) policy:
  - Absolute maximum of 1 request per second, summed across all of your app's users.
  - No heavy use; bulk geocoding is discouraged.
  - Exceeding the limit triggers IP blocks.
  - Self-hosting is recommended for larger loads.
  - [Nominatim Usage Policy](https://operations.osmfoundation.org/policies/nominatim/)
- A forum post cites a 2,500 requests/day soft figure. This is not from the policy page and is unverified. — [OSM help forum](https://help.openstreetmap.org/questions/86982/nominatim-rate-limits)
- Photon (komoot) public API:
  - It may be used if usage is fair. Extensive usage is throttled and availability is not guaranteed.
  - Software is Apache-2.0 and data is OSM (ODbL).
  - An R wrapper's documentation says the public API defaults to 1 request per second.
  - [komoot/photon](https://github.com/komoot/photon); [photon R package](https://rdrr.io/cran/photon/man/photon-package.html)
- Overture Places and Foursquare data:
  - Overture Places is multi-licence. Foursquare-sourced records are Apache-2.0 and require the "Copyright 2024 Foursquare Labs, Inc." notice. Other sources are CDLA-Permissive-2.0.
  - Overture's Places guide shows an October 2026 table.
  - [Overture Places guide](https://docs.overturemaps.org/guides/places); [Overture release notes 2025-09-24](https://docs.overturemaps.org/blog/2025/09/24/release-notes/)
- Foursquare Open Source Places has over 100M POIs under Apache-2.0. Its Hugging Face copy is now gated, and Foursquare asks production users of the public S3 bucket to contact them, which may signal access changes. — [OSM community: FSQ release](https://community.openstreetmap.org/t/foursquare-releases-100m-poi-dataset-under-apache-2-0/121883); [HF fsq-os-places](https://huggingface.co/datasets/foursquare/fsq-os-places); [Foursquare docs](https://docs.foursquare.com/data-products/docs/fsq-places-open-source)

### Inferences
- **[background knowledge, unverified this session]**
  - Pelias (MIT) is powerful but heavy to self-host (Elasticsearch, many GB). Geocode Earth is its hosted version.
  - The Overpass API (public instances) is fine for small on-demand POI queries but not for app-wide traffic.
  - Google Places results generally must be shown on a Google map, which conflicts with a MapLibre stack.
  - Mapbox Search and MapTiler Geocoding are freemium.
- Simplest blip strategy: style the POIs that are already in the vector tiles using custom sprite icons per class. This needs no extra API calls.

### Gaps
- I did not verify the 2026 free-tier quotas of MapTiler, Geoapify, Stadia or Mapbox geocoding (out of scope, per the assignment). Pelias and Geocode Earth status for 2026 was also not checked.

## Hosting/architecture for a hobby project

### Takeaway
A realistic minimal architecture is a static SPA built with Vite and MapLibre, hosted on Cloudflare Pages, Netlify, Vercel or GitHub Pages. Tiles come either from OpenFreeMap or from a self-hosted Protomaps PMTiles planet on Cloudflare R2. A hosted routing and geocoding API sits behind a free tier. Supabase or Firebase stores user waypoints and saved places.

### Cited Findings
- PMTiles is designed to be served as a single file from object storage. Protomaps documents planet downloads and extracts. — [Protomaps getting started](https://docs.protomaps.com/guide/getting-started); [Protomaps downloads](https://docs.protomaps.com/basemaps/downloads)
- OpenFreeMap requires no keys and imposes no limits, which makes it the zero-infrastructure tile option. — [OpenFreeMap GitHub](https://www.github.com/hyperknot/openfreemap)

### Inferences
- **[background knowledge, unverified this session]**
  - Protomaps documents a Cloudflare Workers adapter that serves z/x/y tiles from a PMTiles file on R2, with CDN caching.
  - R2 charges no egress fees, which suits about 120 GB of tiles.
  - GitHub Pages has a 1 GB repo and site limit and cannot hold a planet file. Use regional extracts or external storage instead.
  - Supabase (Postgres plus PostGIS plus auth) is a natural fit for storing waypoints as geometries. Firebase Firestore works but lacks native geo queries.

### Gaps
- Current R2, Workers and Supabase free-tier limits were not checked (pricing is out of scope).

## Realistic effort for a solo-developer MVP and the hard parts

### Takeaway
No published write-up gave a time estimate. The following estimate is an inference: about 4–8 weekends (roughly 60–150 hours) for an MVP with a styled world map, minimap, waypoints and hosted routing, for a developer comfortable with JS. Most of the time goes into style design iterations, sprites and glyphs, and mobile sensor quirks. Fog of war, post-processing shaders, background GPS, and self-hosted planet routing are the hard features.

### Cited Findings
- An existing solo-style app combined MapLibre GL JS, OSRM and Nominatim with a heading-rotating map. This shows the core stack is achievable. — [itch.io post](https://itch.io/post/13953957)
- Building your own planet tiles takes about 2 hours on a high-end machine, but downloading the daily Protomaps build avoids that. — [Protomaps build docs](https://docs.protomaps.com/basemaps/build)
- Self-hosting planet routing requires 64–130 GB or more of RAM (OSRM, dated figures). — [osrm-talk 2021](https://lists.openstreetmap.org/pipermail/osrm-talk/2021-May/001997.html)

### Inferences
- Estimated difficulty tiers. These are the researcher's estimates, not sourced.
  - **Easy (hours to days):**
    - Basemap from OpenFreeMap or Protomaps.
    - Recolouring and casing roads in Maputnik.
    - Blips via sprites.
    - Click-to-place waypoints stored in localStorage or Supabase.
    - A route line from a hosted API.
    - Category filters via `setFilter` or `setLayoutProperty('visibility')`.
    - 3D extrusions.
  - **Medium (days):**
    - Circular heading-up minimap synced to GPS and compass, including iOS permission handling and heading smoothing.
    - Custom glyph PBFs and sprite pipeline.
    - Animated route.
    - Night/neon theme.
    - Legend UI.
    - PWA install.
  - **Hard (weeks):**
    - Fog of war at global scale.
    - True post-processing shaders (bloom, outline, cel-shading) integrated with MapLibre's render loop.
    - Turn-by-turn navigation with rerouting.
    - Background location (needs native or Capacitor).
    - Self-hosted planet routing or geocoding.
- Legal and IP caution: avoid Rockstar's fonts, icons and trade dress. Create an original "inspired-by" style.

### Gaps
- I found no developer write-up or conference talk (FOSS4G or State of the Map 2025–26) that specifically builds a game-styled real-world map with time estimates. Hacker News and Reddit comparison threads from 2025–26 were not reached within the tool budget.
