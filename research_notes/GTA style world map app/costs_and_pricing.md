# Costs and Pricing: GTA-style Worldwide Interactive Map App (solo developer, as of Nov 2026)

**Method note (read first):** All figures were gathered on **2026-11-23**. In this research session, direct page fetching (WebFetch) was blocked by the session's network allowlist for every provider domain tried (mapbox.com, docs.mapbox.com, mapsplatform.google.com, developers.google.com, developers.cloudflare.com, maptiler.com, stadiamaps.com, openfreemap.org). So **every figure below comes from web-search result summaries** of the cited pages (official pages where the search surfaced them, otherwise third-party 2026 pricing write-ups). Where sources conflicted, both values are shown. The report writer should treat figures as "best available, not verified against the live pricing page." Before committing money, check each vendor's pricing page directly.

---

## 1. Hosted map platforms: pricing and free tiers (map display, tiles, search, routing)

### Takeaway
For a hobby project, the cheapest hosted options are (a) **OpenFreeMap** (free, no key, no limits), (b) **self-hosted Protomaps PMTiles on Cloudflare** (a few dollars a month), and (c) the generous free tiers of **Mapbox** (50k web map loads/month) and **TomTom** (50k tiles/day). **Google Maps Platform** is the most expensive per unit at scale ($7 per 1,000 Dynamic Map loads after 10k free). Several free tiers (MapTiler, Stadia, GraphHopper, Thunderforest Hobby, Vercel Hobby) are **non-commercial only**. That matters if student-oriented features are ever monetised.

### Cited Findings

**Mapbox**
- Web (GL JS) map loads: **first 50,000 map loads per month free**. A map load is counted each time Mapbox GL JS initializes on a page. — [Mapbox pricing](https://www.mapbox.com/pricing/); [Mapbox GL JS pricing guide](https://docs.mapbox.com/mapbox-gl-js/guides/pricing/)
- Price above 50k: third-party sources report **~$5.00 per 1,000 map loads** for the first paid band, then $4.00 / $3.00 / $2.50 per 1,000 at higher bands. A snippet of the official page showed $4.00 / $3.20 / $2.40 with unclear band labels. **Conflict: unresolved.** — [Woosmap Mapbox pricing 2026](https://www.woosmap.com/blog/mapbox-pricing); [StoreRocket](https://storerocket.io/learn/mapbox-pricing); [Mapbox pricing](https://www.mapbox.com/pricing/)
- Mobile Maps SDK: **free up to 25,000 MAU**, then ~**$4.00 per 1,000 MAU** (third-party). — [superdupr Mapbox pricing Nov 2026](https://superdupr.com/blog/mapbox-pricing); [agentdeals Mapbox](https://agentdeals.dev/vendor/mapbox)
- Navigation SDK (turn-by-turn) table lists only **up to 10 MAU free**. — [Mapbox pricing](https://www.mapbox.com/pricing)
- Directions API: **first 100,000 requests per month free**, then **$2.00 per 1,000 requests** (100,001–500,000) and **$1.60 per 1,000** (500,001–1,000,000). Some sources list $1.20 at higher volumes. — [Mapbox pricing](https://www.mapbox.com/pricing); [apicostcalc Mapbox](https://apicostcalc.com/mapbox.html)
- Temporary Geocoding: **first 100,000 requests per month free**, then **~$0.75 per 1,000** (one source says $0.50). Permanent geocoding (storing results): **no free tier, from $5.00 per 1,000**. — [Mapbox pricing](https://www.mapbox.com/pricing); [Mapscaping geocoding pricing guide](https://mapscaping.com/guide-to-geocoding-api-pricing/)
- Search Box API (autocomplete sessions): introductory/preview rate **500 free sessions, then $3.00 per 1,000** up to 100k sessions. Standard rate: **2,500 free sessions, then $11.50 per 1,000**. A session is described as up to 50 suggest calls plus 1 retrieve. — [Woosmap](https://www.woosmap.com/blog/mapbox-pricing); [apis.io Mapbox plans](https://plans.apis.io/plans/mapbox/mapbox-plans-pricing/)
- Static/Vector Tiles API: **200,000 free tile requests/month** (Raster Tiles API: 750,000), then ~$1 per 1,000 (third-party, conflicting). — [apibenchmarks Mapbox](https://apibenchmarks.com/maps/mapbox); [superdupr](https://superdupr.com/blog/mapbox-pricing)
- Mapbox Studio (style editor) is **free for registered users**. Styles are hosted on Mapbox. — [OSM wiki: Mapbox Studio](https://wiki.openstreetmap.org/wiki/Mapbox_Studio); [Mapbox Studio](https://mapbox.com/mapbox-studio)
- Sources disagree on whether a card is required for the free tier. — [StoreRocket how to use Mapbox free](https://storerocket.io/learn/how-to-use-mapbox-api-free)

**Google Maps Platform**
- **March 1, 2025:** Google replaced the **$200 monthly recurring credit** with **per-SKU free monthly usage caps**: **Essentials 10,000** (Map Tiles API SKUs **100,000**), **Pro 5,000**, **Enterprise 1,000** billable events per SKU per month. Volume discounts were expanded to 5,000,000+ events. — [Google: March 2025 changes](https://developers.google.com/maps/billing-and-pricing/march-2025); [Google pricing categories](https://developers.google.com/maps/billing-and-pricing/pricing-categories)
- Subscription plans were introduced **effective November 3, 2025** as an alternative to pay-as-you-go. — [Google: March 2025 changes / FAQ](https://developers.google.com/maps/billing-and-pricing/faq)
- One third-party guide (checked 16 Oct 2026) lists a **$300 trial credit for new customers** (the standard Google Cloud trial). Unverified against Google. — [StoreRocket Google Maps API pricing](https://storerocket.io/learn/google-maps-api-pricing)
- India-billed accounts get a 70,000 Essentials cap. — [Google pricing categories](https://developers.google.com/maps/billing-and-pricing/pricing-categories)
- **Dynamic Maps (JS map loads):** **10,000 free/month**, then **$7.00 per 1,000** loads, stepping to $5.60 / $4.20 / $2.10 / $0.53 per 1,000 at higher volume tiers. — [Google core services pricing list](https://developers.google.com/maps/billing-and-pricing/pricing)
- **Compute Routes:** Essentials **$5.00 per 1,000** (10k free), Pro **$10.00 per 1,000** (5k free), Enterprise **$15.00 per 1,000** (1k free). — [Mapatlas Google pricing 2026](https://mapatlas.eu/blog/google-maps-api-pricing-2026); [Geoapify: is Google Maps API free](https://www.geoapify.com/is-google-maps-api-free/)
- **Places Text Search Pro:** **$32 per 1,000** after 5,000 free. Enterprise is ~$35 per 1,000. **Autocomplete Requests:** **$2.83 per 1,000** after 10,000 free. **Place Details:** Essentials $5 per 1,000, Pro $17 per 1,000. (Third-party, consistent across guides.) — [Mapricot Google pricing](https://mapricot.com/guides/google-maps-api-pricing/); [Mapatlas](https://mapatlas.eu/blog/google-maps-api-pricing-2026)
- Google's own example: 2,000,000 Geocoding requests/month cost $7,900 before the change and $5,050 after. — [Google: March 2025 changes](https://developers.google.com/maps/billing-and-pricing/march-2025)
- Gap: exact current prices for Map Tiles API (2D/3D Photorealistic) and the Autocomplete per-session SKU were not retrieved.

**Apple MapKit JS / MapKit**
- MapKit JS free quota: **250,000 map views per day and 25,000 service calls per day** (search, geocoding, directions) per Apple Developer Program membership. One forum post notes an inconsistency (Apple's usage page implied 25k per **month**). — [Apple Developer Forums: Is MapKit JS free?](https://developer.apple.com/forums/thread/729746); [Apple Developer Forums: MapKit pricing](https://developer.apple.com/forums/thread/127493)
- The quota is **shared between MapKit JS and Apple Maps Server API** (Dec 2025 thread). Over the cap, calls return **HTTP 429** until the next day. More capacity needs a request form. — [Apple Developer Forums: MapKit JS quota limits](https://origin-devforums.apple.com/forums/thread/818109)
- Native MapKit on iOS has no per-use charge (developer-forum reports). MapKit JS requires a paid Apple Developer Program membership (**$99/year**, see section 5). — [Apple Developer Forums: native MapKit usage](https://developer.apple.com/forums/thread/654501)
- Caveat: Apple's base map styling is limited. Heavy custom (GTA-like) restyling is not really possible with MapKit (inference from the product, not sourced).

**MapTiler Cloud**
- **Free:** non-commercial only, **5,000 map sessions, 1,000 search sessions, 2,000 3D sessions, 100,000 API requests per month**. MapTiler logo is mandatory. Service halts at the limit with no overage. — [frontdeskreview MapTiler 2026](https://frontdeskreview.com/software/maps-api/maptiler/); [freetier.co MapTiler](https://freetier.co/directory/products/maptiler)
- **Flex:** **$30/month** in most recent sources ($25/month in a June 2026 review). Includes ~25,000 sessions and 500,000 API requests. Overage **$2.50 per 1,000 sessions** and **$0.15 per 1,000 API requests**. **Conflict on price: $25 vs $30.** — [europe-alternative MapTiler review](https://europe-alternative.marketercoffee.com/maps-api/maptiler/); [Mapricot vs MapTiler](https://mapricot.com/compare/maptiler/)
- **Unlimited:** **$295/month**, 300,000 sessions, 5,000,000 API requests (June 2026 review, unconfirmed). — [europe-alternative MapTiler review](https://europe-alternative.marketercoffee.com/maps-api/maptiler/)

**Stadia Maps**
- **Free:** **200,000 credits/month, non-commercial only**, no card needed. — [Stadia: what does a free map API cost](https://stadiamaps.com/learn/what-does-a-free-map-api-cost/); [overpass.ch tile API prices](https://overpass.ch/guides/map-tile-api-pricing)
- **Starter $20/month:** 1,000,000 credits, overage $0.03 per 1,000 credits (commercial use starts here). **Standard $80/month:** 7,500,000 credits, overage $0.02 per 1,000. **Professional $250/month:** 25,000,000 credits, overage $0.015 per 1,000. — [Stadia switch page](https://stadiamaps.com/switch-to-stadia/); [maps.guru vs Stadia](https://maps.guru/compare/stadia-maps-alternative)
- **No auto-overage billing by default:** requests return **HTTP 429** until the next cycle unless you opt in to overage. This is a built-in hard cap. — [Stadia switch page](https://stadiamaps.com/switch-to-stadia/)
- Gap: per-request credit costs (credits per tile, geocode or route) were not retrieved.

**Geoapify**
- **Free: 3,000 credits per day**, no card. Map tiles cost **0.25 credits each** (≈12,000 tiles/day). The same credits cover geocoding, routing and places. The quota is daily, so unused credits do not roll over. — [Geoapify pricing](https://www.geoapify.com/pricing/); [Geoapify free maps API](https://www.geoapify.com/free-maps-api/)
- Smallest paid plan: **"API 10" at $59/month for 10,000 credits/day**. — [freetier.wiki Geoapify](https://freetier.wiki/services/geoapify/)

**Thunderforest**
- **Hobby Project: free, 150,000 tile requests/month.** **Solo Developer: $125/month for 1,500,000 tiles/month.** The pricing page may show EUR, so verify the currency. Raster styles only. — [Thunderforest pricing](https://www.thunderforest.com/pricing/)

**Esri ArcGIS Location Platform**
- **2,000,000 free basemap tiles/month**, then **$0.15 per 1,000 tiles**. Alternative session billing: **1,000 free basemap sessions/month**, then **$4.00 per 1,000 sessions** (a session lasts up to 12 hours with unmetered tiles). Also free: 25 GB tile bandwidth and 250 MB storage. Commercial use is reportedly allowed on the free tier (secondary source). — [ArcGIS Location Platform pricing](https://location.arcgis.com/pricing/); [Esri blog: basemap sessions](https://www.esri.com/arcgis-blog/products/platform/announcements/basemap-sessions); [apio ArcGIS](https://apio.sh/apis/arcgis-maps)

**AWS (Amazon) Location Service**
- Free trial: **500,000 map tile requests/month for 3 months** plus 5,000 static map requests. Since **July 15, 2025**, new AWS accounts get **up to $200 in Free Tier credits** to use within 12 months. — [AWS Location pricing](https://aws.amazon.com/location/pricing)
- Tile price: **conflict.** A re:Post answer quotes **$0.40 per 1,000 tiles**, while a calculator example implies **$0.04 per 1,000** (the 2020 launch price). — [AWS re:Post](https://repost.aws/questions/QUQRTgdsi4ToGQekbtTv9A7g/how-to-calculate-the-grab-maps-tile-cost); [TechCrunch 2020](https://techcrunch.com/2020/12/16/aws-launches-amazon-location-a-new-mapping-service-for-developers/amp/)
- Styles, glyphs and sprites are free. Only GetTile is billed. — [AWS Location maps pricing](https://docs.aws.amazon.com/location/latest/developerguide/maps-pricing.html)

**Azure Maps**
- Gen2 pricing: **Base Map Tiles 5,000 free transactions/month**. **1 transaction = 15 tiles**, so ≈75,000 free tiles. Gen1 is deprecated and **retires 9/15/2026**. The per-1,000 price was not shown in search results. — [Understanding Azure Maps transactions](https://learn.microsoft.com/en-US/Azure/azure-maps/understanding-azure-maps-transactions); [Azure Maps pricing](https://azure.microsoft.com/en-us/pricing/details/azure-maps/)

**HERE**
- Freemium allowance: **conflict.** Most 2026 sources say **~30,000 transactions/month** across most APIs (matrix routing only 2,500). Older pages say 250,000. Overage is ~$1 per 1,000 for geocoding and ~$1.50 per 1,000 for routing. — [pricingapis HERE](https://pricingapis.com/maps/here-maps); [apicostcalc HERE (July 2026)](https://apicostcalc.com/here.html); older figure: [Sanborn](https://sanborn.com/blog/google-maps-and-here-which-apis-should-you-choose/)

**TomTom**
- Free daily allowance: **50,000 tile requests/day plus 2,500 non-tile requests/day** (it applies on Pay-As-You-Grow too). Overage is **$0.08 per 1,000 tile requests**. Non-tile is mostly **$0.75 per 1,000** (geocoding, map display non-tile, traffic) and up to **$2.50 per 1,000** for fuzzy/POI search. — [TomTom pricing](https://developer.tomtom.com/pricing); [frontdeskreview TomTom (June 2026)](https://frontdeskreview.com/software/maps-api/tomtom/)

**OpenFreeMap** (free public vector tiles, OpenMapTiles schema, works with MapLibre)
- Free to use, no API key, no registration and no usage limits. It is funded by donations. — [OpenFreeMap](https://openfreemap.org/); [Show HN](https://news.ycombinator.com/item?id=41593463)

**OSM Foundation tile servers**
- The tile.openstreetmap.org policy asks heavy-use apps to run their own servers or use third parties. Violators get 403 "Access blocked". A valid User-Agent and Referer are required. It is unsuitable as a production base for an app. The OSM raster style also isn't restylable. — [OSMF tile usage policy](https://operations.osmfoundation.org/policies/tiles/); [OSM wiki: Blocked tiles](https://wiki.openstreetmap.org/wiki/Blocked_tiles)

### Inferences
- **Style suitability:** A GTA-like look needs a fully custom **vector** style. That means Mapbox (Studio), MapTiler (customize tool), or any MapLibre-compatible vector source (OpenFreeMap, Protomaps, Stadia, MapTiler) edited with the free **Maputnik** editor. Raster-only providers (Thunderforest, OSM tiles) can't be restyled. Google allows "cloud-based map styling" but with much less control (not sourced in detail).
- **Scenario arithmetic (my estimates, assuming ~1 map load, 2 searches and 2 route requests per session; MAU × ~3 sessions/month for scenarios 1–3; for scenario 4, 500k sessions):**
  - **Mapbox:** (1) 100 MAU ≈ 300 loads → **$0**. (2) 1,000 MAU ≈ 3,000 loads → **$0**. (3) 50,000 MAU ≈ 150,000 loads, 300,000 directions and 300,000 geocodes. That is (100k × $5/1k = $500) + (200k × $2/1k = $400) + (200k × $0.75/1k = $150) ≈ **$1,050/month**. At 10k MAU (30k loads, 60k routes, 60k geocodes) → **$0**. (4) 500,000 sessions ≈ 450k paid loads (~$1,800–2,250), 900k paid directions (~$1,640), 900k paid geocodes (~$675) → **≈ $4,000–4,500/month**. Using the Search Box API for autocomplete instead would add more.
  - **Google:** (3) 150k Dynamic Map loads → 140k × $7/1k = $980. 300k Compute Routes Essentials → 290k × $5/1k = $1,450. 300k Autocomplete requests → ~$820. Total **≈ $3,250/month**. (4) 500k sessions → **≈ $8,000–10,000+/month**. Google is roughly 2–3× Mapbox at the same usage.
  - **Self-hosted PMTiles on Cloudflare:** see section 2. It stays **under ~$40/month even at scenario 4**.

### Gaps
- None of the official pricing pages could be fetched directly (network block). Mapbox overage bands, MapTiler Flex price and AWS tile price are in conflict and need live verification.
- Google Map Tiles API (2D/3D) per-1,000 prices, the Places Autocomplete session SKU price, and Azure Maps per-1,000 tile prices were not retrieved.
- Stadia per-request credit weights were not retrieved.

---

## 2. Self-hosting tiles: PMTiles storage and serving costs; what real operators pay

### Takeaway
A full-planet Protomaps basemap is **~120–139 GB** (2026-11-02 build ≈ 139 GB). On Cloudflare R2 that is **≈ $2/month of storage with $0 egress**. Add **Workers Paid at $5/month** and serving the whole planet costs roughly **$7–10/month for hobby traffic** and only tens of dollars even under a viral spike. OpenFreeMap serves hundreds of millions of requests a month on dedicated Hetzner boxes for **~$175–500/month**.

### Cited Findings
- Protomaps planet PMTiles size: **~139 GB** (dry run against the 2026-11-02 build). Earlier figures were ~111 GB (2024) and ~120 GB. The continental US alone is ~19 GB. Build cadence is daily or weekly (sources differ). — [worldmonitor GitHub issue #1044](https://github.com/koala73/worldmonitor/issues/1044); [Pinball Map: Protomaps tile hosting](https://blog.pinballmap.com/2024/11/05/protomaps-tile-hosting/); [HN: Protomaps self-hosting cheap and easy](https://news.ycombinator.com/item?id=50509837)
- Reported real costs: **~$2/month** for a personal map, and **$1.67/month** for a 111 GB planet (2024). One user notes the build can be done free in GitHub Actions. — [HN thread](https://news.ycombinator.com/item?id=50509837); [Pinball Map](https://blog.pinballmap.com/2024/11/05/protomaps-tile-hosting/); [MuckRock self-hosted maps](https://www.muckrock.com/news/archives/2024/feb/13/release-notes-how-to-make-self-hosted-maps-that-work-everywhere-cost-next-to-nothing-and-might-even-work-in-airplane-mode/)
- **Cloudflare R2 (Standard):** storage **$0.015 per GB-month**, Class A (writes/lists) **$4.50 per million**, Class B (reads) **$0.36 per million**, **egress free**. Free tier per month: **10 GB-month storage, 1M Class A, 10M Class B**. Infrequent Access is $0.01/GB-month, $9.00/M Class A and $0.90/M Class B, with retrieval fees and no free tier. — [Cloudflare R2 pricing](https://developers.cloudflare.com/r2/pricing/); [Cloudflare plans](https://www.cloudflare.com/plans.md)
- **Cloudflare Workers:** Free plan **100,000 requests/day**, resetting at midnight UTC (Error 1027 when exceeded). **Paid: $5/month minimum**, includes **10 million requests/month, then $0.30 per additional million**. Static asset requests on Pages/Workers are **free and unlimited**. Pages Functions count against the Workers quota. — [Cloudflare Workers pricing](https://developers.cloudflare.com/workers/platform/pricing/); [Pages Functions pricing](https://developers.cloudflare.com/pages/functions/pricing)
- **Backblaze B2:** **$6.95 per TB-month**, first 10 GB free. Egress is free up to 3× average stored data, then **$0.01 per GB**. Egress through Bandwidth Alliance CDNs (Cloudflare, Fastly, bunny.net) is free. B2 Overdrive costs $15/TB-month with unlimited egress. — [Backblaze B2 pricing](https://www.backblaze.com/cloud-storage/pricing); [Upstash: B2 pricing Oct 2026](https://upstash.com/blog/backblaze-b2-pricing-explained-2026)
- **AWS S3 + CloudFront:** not retrieved this session. A commenter on the OpenFreeMap HN thread cites S3 egress of "~$90/TB" versus Hetzner's "€1/TB". — [HN: Show HN OpenFreeMap](https://news.ycombinator.com/item?id=41635592)
- **Hetzner (2026 price rises):** prices rose twice in 2026 (**1 April +30–37%** on cloud; **15 June** another +30–38% on CX/CAX for new orders). CAX21 (Arm, 4 vCPU, 8 GB): €5.99 → €7.99 → **€10.49** (≈ **$12.49**). CX22 is no longer orderable. Dedicated **AX42 (64 GB RAM): €47.30 → €57.30/month**. — [cloudtally Hetzner prices 2026](https://cloudtally.eu/hetzner-cloud-prices); [capitalandcompute: Hetzner 2026 increases](https://capitalandcompute.net/blog/hetzner-price-increase-2026/); [HN: Hetzner prices increase](https://news.ycombinator.com/item?id=47120145)
- **OpenFreeMap real costs:** in Oct 2024 the server cost was **~$175/month** (GitHub sponsors $105/month), estimated good for ~300 TB/month on Hetzner. Traffic was ~300 requests/s (~777M requests/month). In Aug 2025, after the Wplace spike (**100,000 requests/s**), it ran on **~$500/month in donations**, enough to cover infrastructure. Cloudflare agreed to sponsor bandwidth. The founder estimated the same traffic would cost **>$6 million/month on MapTiler**. No 2026 figures were found. — [First month of OpenFreeMap](https://blog.hyperknot.com/p/first-month-of-openfreemap); [OpenFreeMap survived 100k rps](https://hyperknot.com/blog/openfreemap-survived-100000-requests/); [GIGAZINE](https://gigazine.net/gsc_news/en/20250812-openfreemap-survived-100000-requests-wplace-live/)

### Inferences
- **Planet on R2 + Worker, my arithmetic:** storage (139 − 10 free) GB × $0.015 ≈ **$1.94/month**, plus Workers Paid $5. Assume ~100 tile requests per session (an assumption; vector maps with heavy pan/zoom can be 50–200).
  - (1)–(2), up to ~300k tile requests/month: inside free tiers. About **$7/month** with Workers Paid, or ~$2 if the free Worker's 100k/day cap suffices.
  - (3), 50k MAU × 3 sessions × 100 tiles = 15M tile requests: Workers (15M − 10M) × $0.30/M = $1.50. R2 Class B (15M − 10M) × $0.36/M = $1.80. Total **≈ $10/month**.
  - (4), 500k sessions × 100 = 50M tiles: Workers 40M × $0.30/M = $12. R2 Class B 40M × $0.36/M = $14.40. Total **≈ $33/month**, less if Cloudflare's edge cache absorbs reads.
- A regional extract (one country) shrinks storage to a few GB, putting it inside R2's 10 GB free tier. But the developer requires worldwide coverage.
- Using OpenFreeMap directly costs **$0** in every scenario, but it depends on a donation-funded third party with no SLA.

### Gaps
- AWS S3/CloudFront current egress prices and CloudFront flat-rate plans were not retrieved.
- Current Protomaps build cadence and official file size were not confirmed from protomaps.com.

---

## 3. Routing costs: hosted APIs versus self-hosted OSRM/Valhalla

### Takeaway
For a hobby app, hosted free tiers (Mapbox 100k directions/month, openrouteservice 2,000/day, TomTom 2,500 non-tile/day, Geoapify credits, Apple 25k service calls/day) cover scenarios 1–2 and often 3. **Self-hosting planet routing needs 32–128 GB of RAM**, which means **~$60+/month** for a Hetzner dedicated box. A single-country Valhalla runs on **4–8 GB RAM (~$10–15/month VPS)**.

### Cited Findings
- **Mapbox Directions:** 100,000 free/month, then $2.00 per 1,000 (to 500k) and $1.60 per 1,000 (to 1M). — [Mapbox pricing](https://www.mapbox.com/pricing)
- **Google Compute Routes:** Essentials $5 per 1,000 after 10k free, Pro $10 per 1,000 after 5k free. — [Mapatlas](https://mapatlas.eu/blog/google-maps-api-pricing-2026)
- **openrouteservice (free, by HeiGIT):** Standard plan **Directions 2,000/day and 40/minute**. The collaborative plan (academic, non-profit) allows 10,000/day and 60/minute. The daily window resets 24h after the first request. — [openrouteservice plans](https://openrouteservice.org/plans/); [ORS FAQ](https://giscience.github.io/openrouteservice/frequently-asked-questions)
- **GraphHopper:** Free plan **500 credits/day, non-commercial only**, max 5 locations per route. Paid Basic is 5,000 credits/day, Standard 15,000 and Premium 50,000 (monthly prices not confirmed). — [GraphHopper pricing](https://www.graphhopper.com/pricing/); [GraphHopper plans and rate limits](https://docs.graphhopper.com/openapi/section/plans-and-rate-limits)
- **TomTom routing:** counts as non-tile (within 2,500/day free), then ~$0.75 per 1,000 or more. — [TomTom pricing](https://developer.tomtom.com/pricing)
- **HERE routing:** ~$1.50 per 1,000 after the freemium allowance. — [pricingapis HERE](https://pricingapis.com/maps/here-maps)
- **Stadia:** routing included via credits (Valhalla-based). Credit weights not retrieved. — [Stadia best routing API](https://stadiamaps.com/learn/best-routing-api/)
- **Self-host OSRM planet:** **≥55 GB of free RAM** needed for the full toolchain, ~50 GB disk. Older 2018 reports cite 300+ GB to preprocess. — [OSRM on whole planet wiki](https://github.com/lonvia/Project-OSRM/wiki/OSRM--on-whole-planet-.-Requirements-and-Statistics); [pistack 2026 comparison](https://www.pistack.xyz/posts/2026-04-25-graphhopper-vs-osrm-vs-valhalla-self-hosted-routing-engines-guide-2026/)
- **Self-host Valhalla planet:** the builder needs ≥16 GB RAM and ~400 GB disk during the build. One user's planet build peaked at 40.6 GB RSS on a 64 GB machine. Serving is claimed possible on 32 GB, with ~100 GB of tiles. Production advice is 64–128 GB RAM. **Regional extract: 4–8 GB RAM** is comfortable. — [Valhalla discussion #3879](https://github.com/valhalla/valhalla/discussions/3879); [bigiron ORS vs OSRM vs Valhalla](https://www.bigiron.cc/guides/openrouteservice-vs-osrm-vs-valhalla-self-hosted-routing); [sumguy](https://sumguy.com/osrm-vs-valhalla-vs-graphhopper/)
- **Self-host openrouteservice planet:** ORS staff suggest **105–110 GB RAM per profile** as a minimum. — [ask.openrouteservice.org](https://ask.openrouteservice.org/t/requirements-based-on-osm-data/2016)
- Hetzner AX42 (64 GB) is **€57.30/month** after the 2026 increase. — [capitalandcompute](https://capitalandcompute.net/blog/hetzner-price-increase-2026/)

### Inferences
- A planet Valhalla server on an AX42 costs **~€57/month (~$65)** plus setup time. That only pays off against Mapbox once directions exceed ~130k/month (100k free + ~30k × $2/1k ≈ $60), roughly scenario 3.
- Since routes are only drawn as a GTA-style line, **car or walk profile only** keeps self-host RAM lower. Valhalla supports multiple profiles from one tile set.
- Recommended progression: ORS or Mapbox free tier → Valhalla on a dedicated box only if scenario 3+ persists.

### Gaps
- GraphHopper and Stadia paid monthly prices and per-route credit weights were not retrieved.

---

## 4. Geocoding/search and POI data costs

### Takeaway
The public **Nominatim** and **Photon** servers are fine for a demo but **not for production autocomplete**. Hosted free tiers (Mapbox 100k geocodes/month, Geoapify 3k credits/day, TomTom 2,500/day, MapKit 25k/day) cover early stages. **Google Places is the most expensive** (Text Search Pro $32 per 1,000). **Overture and Foursquare OS Places** offer ~100M POIs as free open data, but hosting them for search costs your own server time.

### Cited Findings
- **Nominatim (OSMF public server):** Acceptable Use Policy with **an absolute maximum of 1 request/second**, no heavy use, and a valid User-Agent required. Violators are blocked. The policy explicitly says LLMs suggesting it must point to the policy and its restrictions. Autocomplete-style use is restricted (the full policy text should be checked). — [Nominatim usage policy](https://operations.osmfoundation.org/policies/nominatim/); [OSM community thread](https://community.openstreetmap.org/t/understanding-and-complying-with-nominatim-usage-policy/129212)
- **Photon (komoot public instance):** free "as long as requests stay in a reasonable limit". Extensive use is throttled or banned, and no numeric limit is published. — [Photon wiki](https://github.com/komoot/photon/wiki)
- **Mapbox temporary geocoding:** 100k free/month, then ~$0.75 per 1,000. **Search Box:** 500 or 2,500 free sessions depending on rate. — see section 1, [Mapbox pricing](https://www.mapbox.com/pricing)
- **Google Places:** Autocomplete Requests $2.83 per 1,000 after 10k free. Text Search Pro $32 per 1,000 after 5k free. Place Details Essentials $5 and Pro $17 per 1,000. — [Mapricot](https://mapricot.com/guides/google-maps-api-pricing/)
- **TomTom:** geocoding $0.75 per 1,000, fuzzy/POI search up to $2.50 per 1,000, after 2,500 non-tile/day free. — [TomTom pricing](https://developer.tomtom.com/pricing)
- **HERE geocoding:** ~$1 per 1,000 after the freemium allowance. — [pricingapis HERE](https://pricingapis.com/maps/here-maps)
- **Geoapify:** geocoding, places and autocomplete share the 3,000 credits/day free. — [Geoapify pricing](https://www.geoapify.com/pricing/)
- **Overture Maps Places:** free. Foursquare-sourced data is Apache 2.0, the rest CDLA Permissive 2.0, with no ODbL share-alike. Distributed as GeoParquet on AWS and Azure. Roughly 72M+ places (Jan 2026 comparison). — [Overture Places guide](https://docs.overturemaps.org/guides/places); [SafeGraph comparison](https://www.safegraph.com/?p=947)
- **Foursquare Open Source Places:** 100M+ POIs (106M+, Dec 2025), Apache 2.0, public S3 dataset. A third party packaged all of them as a single PMTiles file. — [Foursquare announcement](https://foursquare.com/resources/blog/products/foursquare-open-source-places-a-new-foundational-dataset-for-the-geospatial-community/); [OSM community thread](https://community.openstreetmap.org/t/foursquare-releases-100m-poi-dataset-under-apache-2-0/121883)

### Inferences
- **POI icons:** Protomaps and OpenFreeMap vector tiles already contain OSM POIs (with names and classes), so GTA-style icons can be styled in the tile layer at **no extra cost**. Overture/Foursquare are only needed for richer data.
- **Self-hosting search:** Photon or Nominatim for the planet needs a sizeable server. Nominatim planet is commonly cited at 64 GB+ RAM and ~1 TB SSD (not verified this session), so it falls in the same ~€57+/month dedicated-server class. A simpler path is to put Overture/FSQ places into PMTiles or a small SQLite/DuckDB full-text index on R2/Workers. That cost is unverified, so it is listed under gaps.
- For a "couple of searches per session", Mapbox temporary geocoding is $0 through ~16k MAU (at 3 sessions × 2 searches) and ~$150/month at 50k MAU.

### Gaps
- Overture and FSQ places dataset sizes in GB were not found.
- Nominatim and Photon self-host hardware requirements were not verified this session.
- Google Places Autocomplete per-session pricing was not retrieved.

---

## 5. App, hosting and platform costs

### Takeaway
A web-only launch can cost **~$10/year** (a domain) using free tiers on Cloudflare Pages, Netlify or Vercel Hobby (Vercel Hobby is non-commercial). Going mobile adds **$99/year (Apple)** and **$25 one-time (Google Play)**. Expo EAS has a free tier, and Starter costs **$19/month**. A backend for user waypoints fits in **Supabase or Firebase free tiers** until it needs Supabase Pro at **$25/month**.

### Cited Findings
- **Domain:** Cloudflare Registrar sells at cost with no markup. A .com is ~**$10.46/year** (sources range from $9.15 to $14.99). Verisign is raising the .com wholesale price from $10.26 to $10.97. — [Cloudflare Registrar](https://www.cloudflare.com/products/registrar/); [whtop Cloudflare .com](https://www.whtop.com/plans/cloudflare.com/135912); [Porkbun domain cost calculator](https://porkbun.com/about/domain-cost-calculator)
- **Vercel:** Hobby is **free for personal, non-commercial projects**. Over its limits, the feature pauses until 30 days pass (no overage billing). Hobby bandwidth is cited as 100 GB/month (blog, not confirmed). **Pro is $20/month** with ~1 TB bandwidth and $20 usage credit (blog). Pro has a configurable **spend cap**. — [Vercel Hobby docs](https://vercel.com/docs/plans/hobby); [cmaven comparison](https://cmaven.github.io/en/hosting/netlify-vercel-static-hosting-comparison/); [aidoers $800 Vercel bill](https://www.aidoers.io/blog/the-800-vercel-bill-what-vibe-coding-hides-until-it-costs-you)
- **Netlify:** moved to credit-based billing in Sept 2025 (updated again Apr 2026). The free tier is **300 credits/month** and allows commercial use. Personal plan is **$9/month** (blog source). — [dev.to Netlify alternatives 2026](https://dev.to/devtoolpicks/best-netlify-alternatives-for-indie-hackers-in-2026-ceo)
- **Cloudflare Pages/Workers:** static asset requests are free and unlimited. Workers Free allows 100k requests/day. Workers Paid is $5/month for 10M requests, then $0.30 per million. — [Cloudflare Workers pricing](https://developers.cloudflare.com/workers/platform/pricing/)
- **Supabase:** Free plan has a **500 MB database and 50,000 MAU**, and projects **pause after 1 week of inactivity**. **Pro is $25/month** (plus compute add-ons). — [cloudzero Supabase pricing](https://www.cloudzero.com/blog/supabase-pricing/); [toolradar Supabase 2026](https://toolradar.com/blog/supabase-pricing-2026)
- **Firebase:** Spark (free, stops at limits) and Blaze (pay-as-you-go with the same free quotas, then bills overage). Since **Feb 3, 2026**, Cloud Storage requires a linked billing account (Blaze). — [Firebase pricing plans](https://firebase.google.com/docs/projects/billing/firebase-pricing-plans); [activepieces Firebase pricing 2026](https://www.activepieces.com/blog/firebase-pricing-2026-plans-costs-and-free-limits)
- **Apple Developer Program:** **$99 USD/year** (Enterprise $299/year). Required for App Store distribution and for MapKit JS. — [Adalo: Apple Developer Program 2026](https://studio.adalo.com/blog/apple-developer-program-guide); [magora Apple developer fee (Aug 2026)](https://magora-systems.com/apple-developer-fee/)
- **Google Play Console:** **$25 one-time** registration (no prepaid cards). — [magora Google Play account cost (Oct 2026)](https://magora-systems.com/google-play-developer-account-cost/); [splitmetrics](https://splitmetrics.com/blog/google-play-apple-app-store-fees/)
- **Expo EAS:** **Free $0**, **Starter $19/month + usage** (includes $45 of build credit), **Production $199/month + usage**. Free-plan monthly build counts were not retrieved. — [Expo pricing](https://expo.dev/pricing); [Expo billing plans](https://docs.expo.dev/billing/plans/)

### Inferences
- **Web-only year-one fixed cost:** ~$10 (domain) + $0 hosting (Cloudflare Pages) + $0–5/month (Workers) ≈ **$10–70/year**.
- **Adding iOS + Android:** +$99/year +$25 once. EAS Free is likely enough for a solo dev building occasionally. Local builds are free.
- Native mobile Mapbox counts **MAU** rather than map loads (25k MAU free). MapLibre Native with self-hosted tiles has no per-user fee.

### Gaps
- Exact Vercel Hobby and Pro bandwidth limits and Netlify credit-to-bandwidth conversion were not confirmed from official pages.
- EAS free build quota was not retrieved.

---

## 6. Development tooling costs (AI assistants, style editors, fonts/icons, design)

### Takeaway
Expect **$10–20/month** for one AI coding assistant at entry level, or $100–200/month for heavy-use tiers. Map style editors (Mapbox Studio, Maputnik) are **free**. Icons and fonts can be **free** (open-licensed), or tens of dollars for a commercial game-style typeface.

### Cited Findings
- **Claude Pro:** $20/month (~$17/month annual). **Claude Max:** $100/month (5×) and $200/month (20×). Claude Code is included in the subscriptions. — [daily.dev AI coding tools cost](https://daily.dev/blog/ai-coding-tools-cost-cursor-vs-copilot-vs-claude-code-pricing/); [automationatlas AI coding plans](https://automationatlas.io/guides/ai-coding-plans-compared/)
- **Cursor:** Pro $20/month, Pro+ $60/month, Ultra $200/month. — [nxcode AI coding pricing 2026](https://nxcode.io/resources/news/ai-coding-tools-pricing-comparison-2026)
- **GitHub Copilot:** Pro $10/month, Pro+ $39/month, Max $100/month. Individual plans moved to usage-based AI Credits on **June 1, 2026** (1 credit = $0.01). — [dev.to Copilot Max](https://dev.to/jovan_chan_9500711396d4e6/github-copilot-max-100month-is-the-new-heavy-use-tier-worth-it-vs-cursor-pro-and-claude-code-4onf); [tech-insider metered AI coding](https://tech-insider.org/au/ai-coding-tools-pricing-metered-2026/)
- **Mapbox Studio:** free for registered users. — [OSM wiki](https://wiki.openstreetmap.org/wiki/Mapbox_Studio)
- **Maputnik:** free, MIT-licensed visual editor for MapLibre styles (web or local CLI). — [Maputnik GitHub](https://github.com/maplibre/maputnik); [OpenMapTiles: Maputnik](https://openmaptiles.org/docs/style/maputnik/)

### Inferences
- The developer will plausibly pay for one assistant ($20/month typical) during the build months, which is likely the largest early cash cost.
- Free icons: game-icons.net (CC BY 3.0, attribution required; license not verified this session), Maki/Temaki (open-licensed POI icons). Free fonts: Google Fonts (OFL), for example condensed display faces that evoke a game HUD. Fonts must be converted to PBF glyphs for MapLibre/Mapbox, and Mapbox Studio does this on upload. **GTA's actual fonts (e.g. "Pricedown") and Rockstar map icons are proprietary or trademarked. Copying them for a public app carries IP risk.** "In the spirit of" is safer.
- Design tools: Figma has a free tier (not verified this session).

### Gaps
- Licensing for game-icons.net, Pricedown and Figma pricing were not verified this session.

---

## 7. Billing horror stories and spend protections

### Takeaway
Real surprise bills range from **~$1,000 to $14,000+**, mostly on **Google Maps/Cloud** (viral traffic, leaked keys, AI-generated scraping scripts), plus Mapbox (crawlers hitting old tokens) and Vercel (bandwidth/serverless spikes, $700–$96K reported). **Google budgets only alert. They do not cap spend.** Only per-API **daily quotas** hard-stop usage. Hard-capped providers (Stadia returns 429, MapTiler Free halts, Apple MapKit returns 429, Vercel Hobby pauses) or self-hosted tiles remove this risk.

### Cited Findings
- HN, "Side project went viral, now Google is charging me $1k": a weather side project went viral on Reddit and ran up **~$1,000** of Reverse Geocoding charges after Google raised prices. The bill was reduced after phone calls. — [HN 23722296](https://news.ycombinator.com/item?id=23722296)
- A script written with an AI assistant to collect Google Maps data produced **$1,310.05 in 48 hours**. Google refunded 75% ($982.53). — [dev.to $1,310 bill](https://dev.to/ed_ak_ad19f57ac94922e3ee2/i-asked-claude-ai-to-collect-google-maps-data-for-me-ended-up-with-a-1310-bill-in-48-hours-googl-4dlk)
- "We screwed up with the Google Maps API and now have a significant bill" (HN). — [HN 26439591](https://news.ycombinator.com/item?id=26439591)
- A student saw **~$10,000** after a week. Another reported **$14,000** after leaked credentials, where a **$5 billing alert did not cap spending**. — [Latenode community](https://community.latenode.com/t/urgent-massive-unexpected-google-maps-api-bill-what-are-my-options/19719); [Blind: $14k bill](https://www.teamblind.com/post/students-google-cloud-credentials-stolen-14k-bill-ytopuuph)
- A newer risk: Google Maps API keys can be abused for Gemini calls. Guide on restricting keys. — [env.dev Google Maps key Gemini abuse](https://env.dev/guides/google-maps-api-key-gemini-billing)
- **Mapbox:** a 10-year-old project got a large bill from **crawlers using old tokens**. Mapbox did send a warning when the spike began. — [utf9k: a nice big Mapbox bill](https://utf9k.net/blog/mapbox-bill)
- **Vercel:** a $700+ traffic-spike bill, an $800 "vibe coding" bill, and a reported $96K serverless bill (undated). Vercel offers a configurable **spend cap** on Pro. — [bex.co Vercel bill shock (Jul 2026)](https://bex.co/blog/2026/07/31/vercel-bandwidth-bill-shock); [stork.ai $800 Vercel bill](https://www.stork.ai/blog/ai-codings-hidden-tax-my-800-vercel-mistake); [aidoers](https://www.aidoers.io/blog/the-800-vercel-bill-what-vibe-coding-hides-until-it-costs-you)
- **Google protections:** quotas can be set **per day, per minute and per user per minute**. When reached, "your service stops responding to requests". Google Cloud says quotas "aren't designed to act as a project-wide spending cap". **Budgets and budget alerts only notify.** — [Manage Google Maps Platform costs](https://developers.google.com/maps/billing-and-pricing/manage-costs); [Google Cloud: capping API usage](https://docs.cloud.google.com/apis/docs/capping-api-usage)
- **Hard caps by design:** Stadia returns HTTP 429 with no auto-overage. MapTiler Free halts at the limit. MapKit JS returns 429 over quota. Vercel Hobby pauses features for 30 days. Cloudflare Workers Free returns Error 1027 past 100k/day. — [Stadia](https://stadiamaps.com/switch-to-stadia/); [frontdeskreview MapTiler](https://frontdeskreview.com/software/maps-api/maptiler/); [Apple forums](https://origin-devforums.apple.com/forums/thread/818109); [Vercel Hobby](https://vercel.com/docs/plans/hobby); [Cloudflare Workers pricing](https://developers.cloudflare.com/workers/platform/pricing/)

### Inferences
- Protection checklist for this project: use URL/referrer-restricted public tokens (Mapbox and Google both support this). Set daily quota caps on every billable Google SKU. Rotate or delete old tokens. Route geocoding and directions through your own Worker with rate limiting and caching. Prefer self-hosted tiles so a viral map-load spike costs tens of dollars, not thousands.
- R2 has no hard spend cap either, but at $0.36 per million reads a 100M-request spike costs ~$36.

### Gaps
- Mapbox's own spend-cap or billing-limit features were not confirmed from official docs.
- Whether Google budgets can automatically disable billing via Pub/Sub was not confirmed in these results. It is a known documented pattern, but not sourced here.

---

## 8. Comparison: hiring this out (freelance/agency quotes)

### Takeaway
Vendor sources put agency map-app MVPs at **$25,000+** (up to $250k for complex apps). Freelance GIS/Mapbox developers bill **~$45–75/hour**, so a 150–250-hour MVP would be ~**$7k–19k**. These are vendor marketing figures, not verified market data.

### Cited Findings
- Map app development: **$25,000 for a simple MVP to $250,000+** for complex platforms (development firm's own estimate). — [CISIN: how to build a map app](https://www.cisin.com/coffee-break/how-to-build-a-map-app-.html)
- Simple web maps "may cost as little as $25,000" (agency). — [Swivl web maps cost guide](https://swivl.tech/cost-guide-customer/web-maps)
- GIS developer freelance rates are **$45–75/hour**. A worked example: an interactive property-tax web map estimated at 220 hours × $52 = **$11,440**. — [Flexiple: cost to hire GIS developer](https://flexiple.com/cost-to-hire/gis-developer)
- Upwork/Fiverr list Mapbox map gigs (prices not shown in snippets). Custom styles add both licensing and configuration time. — [Upwork Mapbox gig](https://www.upwork.com/services/product/development-it-custom-interactive-mapboxgl-map-1589746430137929728); [Affective: map features and budget](https://weareaffective.com/learning-centre/how-do-map-features-impact-your-app-development-budget)

### Inferences
- The comparison shows the solo-dev path costs ~1–2 orders of magnitude less in cash. The main "cost" is the developer's own time plus ~$20/month of AI tooling.

### Gaps
- No independent survey of actual freelance quotes for a styled-map MVP was found. The figures are vendor or self-reported.
