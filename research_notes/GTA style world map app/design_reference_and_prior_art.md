# GTA-Style Real-World Map: Design Reference (GTA V / GTA VI Map and HUD) and Prior Art

> Research method note (2026-11-23): Most fetches of third-party sites (gtaboom.com, gtanerd.com, dev.to, gamemapsirl.app) were blocked by this session's network allowlist. Those sources are therefore cited from **search-result summaries only**, not read in full. GitHub pages were fetched directly. Treat any claim sourced only from a search snippet as "single-source, not read in full".

## 1. GTA VI release status (Nov 2026) and what is publicly known about its map, minimap and HUD, compared with GTA V

### Takeaway
GTA VI **did launch on 19 Nov 2026** (PS5 / Xbox Series X|S) to near-universal acclaim (about 99 on Metacritic). Its HUD moves away from GTA V's fixed bottom-left rectangle. The new HUD is configurable: a dynamic or fading minimap, an optional compass, and "Always On". While driving, the minimap is a wider rounded rectangle with a more 3D, GPS-like perspective. The player-set route appears to be **pink**, where GTA V's was purple. Detail comes almost entirely from guide and fan sites, not from Rockstar documentation, and several details conflict between sources.

### Cited Findings
**Release status**
- GTA VI launched 19 Nov 2026 to "rave reviews". Al Jazeera cites an aggregate of 99/100 on Metacritic from 150+ reviews — [Al Jazeera](https://www.aljazeera.com/news/2026/11/19/grand-theft-auto-vi-launches-to-rave-reviews-after-13-year-wait)
- GameSpot scored it 10 ("Setting the bar for open worlds impossibly high") and lists the platforms as PS5 and Xbox Series X — [GameSpot](https://www.gamespot.com/reviews/grand-theft-auto-6-review/)
- Timesaver gives 99 from 132 reviews as of 18 Nov 11:40 UTC. Review embargo was reportedly 18 Nov, which is not confirmed by Rockstar — [Timesaver](https://timesaver.gg/blog/gta-6-reviews-release-date-before-launch-confirmed-2026); [Insider Gaming](https://insider-gaming.com/grand-theft-auto-6-review-embargo/); [TechRadar live blog](https://www.techradar.com/live/news/gta-6-review-embargo-roundup-reaction-ask-me-anything-launch-live)
- No PC version is listed at launch (GameSpot platform list) — [GameSpot](https://www.gamespot.com/reviews/grand-theft-auto-6-review/)

**GTA VI HUD / minimap (guide-site sourced)**
- **Navigation modes:** a fading/dynamic HUD, a permanent minimap, or a compass. Quick waypoints can be set without opening the full map. At setup the game offers "Minimap (Dynamic)", "Minimap & Compass (Dynamic)" or "Minimap Always On", changeable later — [GTABoom (snippet)](https://www.gtaboom.com/gta-6-minimap-c6d7); [Game8](https://game8.co/games/GTA-6/archives/637295); [allthings.how settings](https://allthings.how/gta-6-hud-settings-minimap-street-names/)
- Minimap and Compass each take **On / Dynamic / Off** — [Bloxodes](https://bloxodes.com/articles/gta-6-hud-icons-explained)
- **Layout:** Health / Stamina / Focus meters top-left (icons: heart, lightning bolt, eye). Ammo, weapon and wanted stars top-right. **Minimap bottom-left** — [bo3.gg](https://bo3.gg/games/articles/gta-6-hud-and-icons-explained-meters-police-profiling-icons-and-minimap-options); [GTA Codex](https://gtacodex.com/guides/gta-6-hud-and-wanted-system-explained); [Beebom](https://beebom.com/gta-6-icons-meters-meanings-explained/)
  - Conflict: GTA Codex says three meters, plus Oxygen shown only underwater. Another guide says four status meters — [GTA Codex](https://gtacodex.com/guides/gta-6-hud-and-wanted-system-explained); [Tech Nerdiness](https://www.technerdiness.com/gta/gta-6-hud-icons-explained/)
- **Driving minimap:** a rounded rectangle (not a circle). The route is drawn in **pink** with a live distance readout. This comes from a single source — [allthings.how](https://allthings.how/gta-6-hud-icons-and-meters-explained-extended-look/). Others describe a "wide rectangular minimap" while driving, "drawn like a real GPS" with route and distance — [GTANerd (snippet)](https://gtanerd.com/guides/gta-6-hud-and-minimap/); [gamer.org](https://www.gamer.org/gta-6-hud-icons-minimap-explained/)
- **3D:** one guide says the minimap renders a 3D satellite-style view of Vice City buildings in real time. Another cautions Rockstar has not confirmed a fully rotatable 3D pause map — search summary of [GTABoom](https://www.gtaboom.com/gta-6-minimap-c6d7) / [gta6explained](https://gta6explained.com/blog/gta-6-minimap-navigation-3d-gps-design)
- **Analysis:** GTA VI's minimap is "better suited to forward route guidance and modern driving", while GTA V's flatter radar gives "faster all-around awareness" — [gta6explained](https://gta6explained.com/blog/gta-6-minimap-navigation-3d-gps-design)
- **Police / wanted:** sources conflict. One says hostile police blips were removed from the minimap. Another says the map tints red-pink to show the search perimeter. Red "profiling" icons under the stars are not extra wanted levels — [bo3.gg](https://bo3.gg/games/articles/gta-6-hud-and-icons-explained-meters-police-profiling-icons-and-minimap-options); search summary across HUD guides
- **HUD visibility:** one source says there is no single switch to hide the whole HUD, so rows are toggled one by one. Another says most of the HUD is hidden by default for a cinematic look — [allthings.how](https://allthings.how/gta-6-hud-settings-minimap-street-names/); [GTANerd (snippet)](https://gtanerd.com/guides/gta-6-hud-and-minimap/)
- Rockstar "has not provided complete documentation explaining the GTA 6 icons" — [games.gg](https://games.gg/grand-theft-auto-vi/guides/gta-6-hud-and-ui-icons-explained/)

**GTA VI pause map**
- Options (PS5) or Menu (Xbox) opens the pause screen on the map. The pause map uses **satellite imagery rather than a drawn map**, with a full legend. Zoom is R2/RT in and L2/LT out, and zoom resets each time the map is reopened — search summary of [showgamer](https://showgamer.com/en/guides/7946-kak-uvelichit-i-umenshit-masshtab-karty-v-gta-6-na-ps5-i-xbox-series), [outputlag](https://outputlag.com/guides/gta-6-best-settings-controls/), [gta6data](https://gta6data.com/gta-6-controls-settings-and-in-game-help-guide/)
- Rockstar publishes an **official static, print-ready Leonida map** on the Downloads page of the GTA VI site — search summary (Rockstar GTA VI site); not fetched

**GTA V baseline, for comparison**
- The GTA V radar is **rectangular** (earlier games used a round radar) — [grandtheftwiki Radar](https://www.grandtheftwiki.com/Radar); [GTA Wiki GPS](https://gta.fandom.com/wiki/GPS)
- A design essay says the rectangle shows more map at once. Its "2.5D" tilt shows what is ahead, boosted by zoom that depends on speed and altitude. The essay says the rectangle carried over to GTA VI — [Medium, "The Rectangular Radar"](https://medium.com/@lataxed/the-rectangular-radar-the-design-of-grand-theft-auto-v-b535114f52f4)

### Inferences
- A "GTA VI-inspired" style is now well enough defined to spec: a rounded-rectangle bottom-left minimap, a pink route, a 3D-ish forward-tilted view, dynamic fade, and an optional compass strip. A "GTA V-inspired" style is the safer, better-documented fallback.
- Many "GTA 6 HUD" guides were written from pre-release footage and republished at launch, so treat exact labels with caution.

### Gaps
- No Rockstar-authored description of the GTA VI map or HUD was found. No Digital Foundry, IGN or Eurogamer piece specifically on the map UI could be read; the fetches were blocked.
- No verified information on the phone (in-game smartphone) map app in GTA VI.
- The route colour (pink vs magenta), exact minimap aspect ratio, and whether the pause map has a drawn "atlas" mode in addition to satellite are unverified.
- No post-launch patch notes affecting the map were found.

## 2. Concrete visual characteristics (palette, roads, land/water, buildings, type, blips, route, waypoint, north, behaviour, bars, discovery)

### Takeaway
GTA V's map language is **dark, near-black land, flat mid-grey roads without strong casing, pale or muted water, purple player route and waypoint, yellow mission route, and coloured circular blips with up/down arrows**. Type is set in Chalet (London 1960 / Comprimé Cologne 1960), with Pricedown reserved for the logo and money. GTA VI (per fan reproductions) shifts to **time-of-day colours, steel-blue 3D buildings, cyan water and a pink route**. No official hex values for map tiles exist; only community HUD-colour dumps.

### Cited Findings
**Colours / palette**
- GTA V pause-map look, as reproduced by a fan app: "near-black land, flat grey roads, pale water, and a purple route" — [Overworld Maps README](https://github.com/TheAlgo7/overworld-maps)
- GTA VI look, as reproduced by the same app: "colours shift with the time of day, steel-blue 3D buildings, cyan water, and a pink route"; offered as pause-map and minimap modes — [Overworld Maps README](https://github.com/TheAlgo7/overworld-maps)
- Community dump of GTA V HUD colour constants (unofficial, RGBA): red 194,80,80 (#C25050); blue 93,182,229 (#5DB6E5); yellow 240,200,80 (#F0C850); green 102,152,104 (#669868); white 240,240,240; black 0,0,0 — [Pastebin HUD colours](https://pastebin.com/SACHWjhc). The same named colours (including radar health, armour and damage) are listed at [RAGE MP wiki](https://wiki.rage.mp/wiki/Fonts_and_Colors)
- The **Game Maps IRL** "Los Santos" theme is described by a vendor blog as high-contrast black-and-white noir. This is a commercial interpretation, not the game — search summary, [Game Maps IRL blog](https://gamemapsirl.app/blog/gta-v-map-carplay-guide)

**Typography**
- GTA V: **Pricedown** (Ray Larabie) for the logo and on-screen money. **Chalet Comprime Cologne Sixty** for menu titles. **Chalet London Nineteen Sixty** for subtitles and menu items — [GTA Wiki Fonts](https://gta.fandom.com/wiki/Fonts)
- The whole UI uses Chalet 1960 and Chalet Comprimé 1960. Location and vehicle names use **House Script** (Sign Painter). The logo lettering is custom — [Fonts In Use](https://fontsinuse.com/uses/55702/grand-theft-auto-v)
- In-game font indices: 0 = Chalet London 1960, 1 = House Script, 4–6 = Chalet Comprimé Cologne 1960, 7 = modified Pricedown — [GTAForums fonts list](https://gtaforums.com/topic/794014-fonts-list/)
- GTA VI font: speculative and alternatives-focused coverage only — [fontalternatives.com](https://fontalternatives.com/blog/gta-6-font/)
- Free stand-ins used by fan projects: Barlow / Barlow Condensed / Passion One for GTA V; **Inter + Barlow Condensed for GTA VI**; Pirata One + Anton for San Andreas — [Overworld Maps](https://github.com/TheAlgo7/overworld-maps); [SA Maps](https://github.com/CharbelAt/sa-maps)

**Blips, route, waypoint, north**
- GTA V GPS: **purple** = player-defined route and waypoint; **yellow** = mission route (GTA IV used green for player routes). The route draws on both pause map and radar. It auto-recalculates off-route. It is not voiced in V (it was in IV) — [GTA Wiki GPS](https://gta.fandom.com/wiki/GPS)
- GTA IV/V radar uses **coloured circles** for targets. A small arrow inside the circle shows whether the target is higher or lower than the player — [GTA Wiki File:Radar](https://gta.fandom.com/wiki/File:Radar-GTAVC.png)
- North is marked by a compass-point "N" blip on the radar — [gta.wiki Radar](https://gta.wiki/w/Radar?veaction=edit)
- The complete GTA V blip sprite and colour index (hundreds of sprites with IDs and colour IDs) is documented for modders — [FiveM blips reference](https://docs.fivem.net/docs/game-references/blips/)
- Off-screen blips clamp to the radar edge (a convention reproduced in SA Maps) — [SA Maps](https://github.com/CharbelAt/sa-maps)

**Minimap behaviour**
- GTA V auto-zooms the radar: further out in a vehicle, further again at high speed, and in on foot. FiveM exposes `SetRadarZoom` and a "big map" toggle — [fivem-minimaps guide](https://fivem-minimaps.com/guides/fivem-radar-zoom-settings)
- 2.5D tilt plus speed and altitude-dependent zoom — [Medium essay](https://medium.com/@lataxed/the-rectangular-radar-the-design-of-grand-theft-auto-v-b535114f52f4)
- A player request in another game's forum shows the general design ideas: speed-based zoom, and anchoring the player arrow low in the frame to show more road ahead — [CDPR forum](https://forums.cdprojektred.com/index.php?threads/mini-map-while-driving-needs-to-be-zoomed-out.11045432/)
- GTA VI: rounded rectangle, dynamic fade, optional compass; see section 1.

**Health / armour bars**
- In GTA V, health and armour bars are commonly understood to sit directly under the radar, with a Teardown mod copying "health bar under it, just like in GTA". No authoritative GTA V source was read — [Steam Workshop mod](https://steamcommunity.com/sharedfiles/filedetails/?id=3823006127)
- GTA VI moved meters to the top-left (section 1).

### Inferences
- A practical palette spec: land approx. #0F1113–#1A1D21, roads in flat greys of 2–3 tiers by class, water muted blue-grey (V) or cyan (VI), parks a dark desaturated green, route #A04CD2-ish purple (V) or hot pink (VI). These hex values are **my estimates**, not documented.
- The road treatment is flat fill and minimal casing, with width scaling by road class. This is easy to express in a MapLibre style.

### Gaps
- No official or measured hex values for GTA V or VI map tiles (land, road, water, park) were found.
- GTA V fog-of-war: no source found. GTA V's single-player map is commonly understood to be fully revealed, unlike GTA SA, but this is unverified here. GTA VI fog-of-war or discovery is not documented.
- Exact GTA V route-line width and casing, and the waypoint marker glyph, were not documented in the sources read.

## 3. In-game map functionality

### Takeaway
The core feature set to emulate: full-screen pause map with zoom and pan; a legend that doubles as a category filter; a custom waypoint with GPS route on map and radar; colour-coded mission vs player routes; auto-reroute; blips with height arrows; a speed-adaptive radar; quick waypoints and compass (VI); interiors / "enterable buildings" layer (VI fan maps).

### Cited Findings
- GTA V: waypoint, then route drawn on map and radar; auto-recalculation; purple vs yellow routes — [GTA Wiki GPS](https://gta.fandom.com/wiki/GPS)
- GTA VI: pause map with satellite imagery and a full legend. Zoom with triggers, resets on reopen. Quick waypoints without opening the map — section 1 sources; [GTABoom (snippet)](https://www.gtaboom.com/gta-6-minimap-c6d7)
- Fan-site feature conventions for GTA VI maps: an "Enterable buildings" filter by venue type (counts conflict: 385 vs 414) — [gta6art.com](https://gta6art.com/); [gtamap.io](https://gtamap.io/)
- GTA V radar zoom and "big map" toggle (expanded radar) — [fivem-minimaps guide](https://fivem-minimaps.com/guides/fivem-radar-zoom-settings)
- A HUD-to-navigation mapping idea from SA Maps: next turn in the weapon slot, health bar = trip progress, armour = battery, money = metres remaining, wanted stars when off-route, zone-name banners on entering districts, "mission" briefings — [SA Maps](https://github.com/CharbelAt/sa-maps)

### Inferences
- For a real-world app, "zone name banner on entering a district" (from OSM neighbourhood polygons) and a "legend = filter" sidebar are cheap, high-impact GTA signifiers.

### Gaps
- No verified documentation of GTA VI's in-game phone map, interior map behaviour, or legend categories list.

## 4. Prior art: GTA-styled real-world maps

### Takeaway
This has been done many times, mostly in 2025–2026, almost all on **MapLibre + OpenStreetMap / OpenFreeMap**. The most complete examples are **Overworld Maps** (Android Auto; GTA V, RDR2 and GTA VI styles), **SA Maps** (PWA plus Android Auto; San Andreas radar) and the **Vice City-style OSM** web demo. The commercial **Game Maps IRL** (iOS, CarPlay, Android Auto, subscription) reportedly earns significant revenue. No Snazzy Maps or Mapbox gallery GTA style was found. No takedown of a real-world restyle was found. Take-Two has, however, taken down GTA VI *map-content* fan projects.

### Cited Findings
- **Overworld Maps** (TheAlgo7):
  - What it is: Android plus Android Auto turn-by-turn navigation in GTA V, RDR2 and GTA VI styles, with a GTA VI pause-map and minimap.
  - Stack: Kotlin / Jetpack Compose; MapLibre Native; Ferrostar navigation; Valhalla; OpenFreeMap/OSM tiles; Google Maps web endpoints for routes and traffic; Photon search; Overpass speed cameras; AWS terrain.
  - Themes: one `themes.js` source exported to style files.
  - Licence and popularity: "All rights reserved" (source-visible, not reusable). About 13 stars. Fan-project disclaimer.
  - Links: [GitHub](https://github.com/TheAlgo7/overworld-maps); [site](https://overworld.thealgothrim.com/)
- **SA Maps** (CharbelAt):
  - What it is: a GTA San Andreas radar reskin of navigation; PWA, Android and Android Auto.
  - Stack: MapLibre GL JS, vanilla JS, GitHub Pages; OpenFreeMap tiles, OSRM routing, Photon search; Kokoro-82M TTS voices.
  - Style: olive land, navy water, pale roads; round or full-screen radar; north badge; gang-turf tinting.
  - Popularity and status: 0 stars; "fan-made parody", no game assets — [GitHub](https://github.com/CharbelAt/sa-maps)
- **GTA Vice City-style OpenStreetMap** (subins2000):
  - Stack: MapLibre GL JS, with the style made in Maputnik.
  - Features: retro POI icons. POIs are cached by zooming in, using a "Collect POIs" button. Kochi variant.
  - Popularity and status: about 77 stars. Live demo at lab.subinsb.com — [GitHub](https://github.com/subins2000/gta-vice-city-style-openstreetmap); [demo](https://lab.subinsb.com/gta-vice-city-style-openstreetmap/)
- **Game Maps IRL**:
  - What it is: a commercial iOS app (App Store id6742728012) with CarPlay and Android Auto. Themes include a GTA V-inspired "Los Santos", plus RDR and Minecraft-pixel.
  - Developer: Retry Apps Yazılım Ltd. Şti. Disclaims affiliation with game publishers.
  - Reception: user complaints about paywalls and CarPlay reliability.
  - Revenue: an X post claims about 40K downloads and $50K/month. This is **unverified**.
  - Links: [App Store](https://apps.apple.com/us/app/game-maps-irl/id6742728012); [site](https://gamemapsirl.app/); [Yahoo Tech](https://tech.yahoo.com/apps/articles/game-maps-irl-makes-commute-144303906.html); [X post](https://x.com/adriamatz/status/2078791913189351578); [mwm.ai summary](https://mwm.ai/apps/game-maps-irl/6742728012)
- **Game Maps – IRL Gaming Sim Map**: a separate iOS app with similar game-styled maps — [App Store id6748309177](https://apps.apple.com/app/id6748309177)
- **GrandMap**: a dev.to hobby project. "GTA's minimap turned into a web app", built on Leaflet.js plus ESRI. Not read in full — [dev.to](https://dev.to/swagking/grandmap-the-gta-inspired-map-project-nobody-asked-for-but-i-built-anyway-3p8k)
- **GAME GPS**: a German browser demo with a GTA-inspired UI and radar minimap. Says it contains no original game files — [GitHub](https://github.com/marcellodimartino493-del/game-gps)
- **MiniMap (TiernanDawg/Led)**: an iOS MapLibre + OpenFreeMap navigation app. Its presets are "not yet bespoke GTA" worlds — [GitHub](https://github.com/TiernanDawg/Led)
- **Glavin001/open-world**: a GTA-clone 3D world generated from OSM with Three.js. A game, not a map — [GitHub](https://github.com/Glavin001/open-world)
- **FiveM / GTA V mods (in-game, not real-world)**:
  - GTA VI-style HUDs for FiveM — [F5-Studio GTA-VI-HUD-FIVEM](https://github.com/F5-Studio-FiveM/GTA-VI-HUD-FIVEM); [Geckomacabre GTA-VI-Inspired-HUD](https://github.com/Geckomacabre/GTA-VI-Inspired-HUD-for-FiveM/blob/main/resources/vi_pausemenu/README.md)
  - "GTA VI Styled Minimap" GTA V mod — [gta5mod.net](https://gta5mod.net/gta-5-mods/misc/gta-vi-styled-minimap-legacy-v1-2/); [Beebom coverage](https://beebom.com/you-can-try-the-gta-6-minimap-right-now-with-this-gta-5-mod/)
  - "GTA 5 map style" — [libertycity.net](https://libertycity.net/files/219141-gta-5-map-style.html)
- **Snazzy Maps / Mapbox gallery**: no GTA-named style found through search. Snazzy styles are CC-licensed Google Maps JSON — [Snazzy Maps](https://snazzymaps.com/editor)
- **Takedown risk (context)**:
  - Take-Two served a takedown on a video of a GTA 5 mod recreating the GTA VI map. The mod was then abandoned; it was based on the leak-derived GTA 6 Mapping Project — [PC Gamer](https://www.pcgamer.com/games/grand-theft-auto/playable-gta-6-map-nuked-without-warning-by-take-two-lawyers-my-guess-is-that-the-map-was-probably-a-little-too-accurate); [Techdirt](https://www.techdirt.com/tag/mods/); [Destructoid](https://www.destructoid.com/gta-modder-makes-playable-gta-6-map-and-clashes-with-take-two-after-surprise-takedown/)
  - The GTA 6 Mapping Project's Discord reportedly disappeared. The cause is unconfirmed — [Notebookcheck](https://www.notebookcheck.net/Take-Two-reportedly-targets-GTA-6-Mapping-Project-closing-Discord-that-shared-leaks.1448191.0.html)
  - Take-Two has a history of mod takedowns, e.g. the Liberty City Preservation Project — [PC Gamer](https://pcgamer.com/uk/take-two-has-been-issuing-takedowns-for-gta-mods)

### Inferences
- The niche is crowded at the "it looks like GTA" level. The commercial winner (Game Maps IRL) shows demand. Differentiation would need to come from fidelity to the GTA VI look (few do it), a web-first, no-install experience, or the student utility angle.
- All successful real-world restyles avoid shipping game assets and fonts, and carry "not affiliated" disclaimers. Takedowns so far targeted reproductions of Rockstar's *fictional map content*, not real-world restyles. This is an inference; no legal analysis was done.

### Gaps
- No viral Reddit, HN or TikTok post on a GTA-style real-world map could be verified (searches returned none).
- No download or user numbers were verifiable for any project, apart from GitHub stars.
- No Mapbox Studio GTA style or Snazzy GTA style was confirmed to exist.

## 5. Interactive GTA map sites and their stacks; other game-style real-world map references

### Takeaway
Fan GTA V and GTA VI interactive maps are overwhelmingly **Leaflet with CRS.Simple and a custom raster tile pyramid** (256 px tiles). Data is often from gtadb.org under CC BY 4.0. For other game-style real-world references, the main ones are Lee Martin's **RDR2-style Mapbox Studio map** and the **GOT-inspired Mapbox style**. City Roads (OSM) offers cyberpunk-like themes. Cyberpunk 2077 "realistic map" mods go the other way, making a game map look real.

### Cited Findings
- **Vice6Map**: Leaflet with a multi-resolution 256×256 tile pyramid and gtadb.org data. 3,340 places in 18 categories — [vice6map.com](https://vice6map.com/)
- **Leonida State Map**: Leaflet; data snapshot 17 Nov 2026 — [leonidastatemap.xyz/about](https://leonidastatemap.xyz/about)
- **gta-6.space**: Leaflet with gtadb.org (CC BY 4.0) data. Notes that no complete official map has been released — [gta-6.space](https://gta-6.space/)
- **GTA6MAP (gta6art.com)**: 3,749 places, 385 enterable buildings — [gta6art.com](https://gta6art.com/). Other sites: [gtamap.io](https://gtamap.io/) (414 interiors), [GetLeonida](https://getleonida.com/en/) (route planner, community pins), [GTA 6 Bible](https://gta6bible.com/map/), [Leonida Interactive](https://leonidainteractive.com/), [gtasixmap.com](https://www.gtasixmap.com/)
- **Open source**:
  - navanem/gta6-leonida-atlas: Leaflet, Zustand, Dexie (IndexedDB), optional Three.js 3D — [GitHub](https://github.com/navanem/gta6-leonida-atlas)
  - lofghi87/leonida-atlas: Leaflet CRS.Simple and Supabase — [GitHub](https://github.com/lofghi87/leonida-atlas)
- **GTA V**:
  - [dukeofsussex/gta-v-map](https://github.com/dukeofsussex/gta-v-map) (Leaflet)
  - [Flamm64/GTA-V-World-Map](https://github.com/Flamm64/GTA-V-World-Map) (Google Maps API)
  - [CreepPork/GTAV-Maps](https://github.com/CreepPork/GTAV-Maps): atlas, road, satellite and UV variants of the game map
  - In-game style replacement mods: [menu-map](https://github.com/gennariarmando/menu-map/releases)
- **Game-style real-world references**:
  - RDR2-inspired map built in Mapbox Studio, with a design write-up — [dev.to, Lee Martin](https://dev.to/leemartin/how-i-designed-a-red-dead-redemption-2-inspired-map-in-mapbox-studio-4gkh) (not read in full)
  - GOT-inspired Mapbox map — [Gitee mirror of mapbox/GOT-Inspired-Map](https://gitee.com/mirrors_mapbox/GOT-Inspired-Map)
  - Mapbox post on building a real-world game map — [Mapbox blog, GoCity](https://blog.mapbox.com/gocitys-real-world-game-map-how-we-built-it-ecc3b7f1a5bb)
  - Mapbox map design guide — [Mapbox guide PDF](https://go.mapbox.com/rs/117-NXK-490/images/the-guide-to-map-design.pdf)
  - City Roads (OSM street renders; green-on-black theme) — [lairofsecrets summary](https://lairofsecrets.com/blog/cyberpunk-city-generators/)
- **Reverse direction**: Cyberpunk 2077 "Realistic Map" and "Realistic Minimap" mods (550k+ downloads) make the game map look like satellite imagery — [Nexus](https://www.nexusmods.com/cyberpunk2077/mods/37988); [SvenVH blog](https://www.svenvh.nl/blogs/realistic-map/); [TheGamer](https://www.thegamer.com/cyberpunk-2077-realistic-map-add-on-turns-it-into-google-earth/)
- A hybrid stack is also documented: Leaflet for raster overlays with MapLibre for the vector base — [HackerNoon](https://hackernoon.com/the-mapping-stack-most-developers-get-wrong-and-how-i-got-it-right)

### Inferences
- For *real-world* data, MapLibre GL JS with OpenFreeMap / OSM vector tiles is the de facto stack in prior art. It gives rotation, pitch (for the VI-style tilt) and data-driven styling, which Leaflet raster maps lack.

### Gaps
- No Zelda-, Fallout (Pip-Boy) or Cyberpunk-style *real-world* web map was verified, apart from City Roads themes.
- Fan-map place counts conflict across sites, likely because of different snapshots.
