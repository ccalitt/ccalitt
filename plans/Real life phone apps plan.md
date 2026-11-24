# Real-life phone apps plan

One installable web app that behaves like a phone home screen. Each app on the GTA VI in-game phone becomes a small real-life app, and every app can put pins ("blips") on the shared map. Names, icons and screens are original; the game's app names appear here only to say which function each one mirrors. The working names are placeholders I made up.

The in-game app list comes from guide sites, several written from previews. Rockstar has not published one.

## Shared foundation (built first)

- **App shell:** a home screen with an app grid, a status bar, and a phone frame on desktop. Installable to the phone's home screen and usable offline for anything that doesn't need live data.
- **Stack:** Vite, TypeScript and React, hosted as a static site on Cloudflare Pages.
- **Storage:** all personal data stays in the browser on the device (IndexedDB). A backup-to-file and restore-from-file feature ships in version 1, because clearing site data would otherwise delete everything.
- **Shared services used by every app:**
  - location and compass
  - a blip registry, so any app can add pins to the map (photos, parked car, ATMs, bikes, class locations)
  - an in-app notification feed that lands in the inbox app
  - theme and wallpaper
- **One small server piece:** a Cloudflare Worker that fetches third-party feeds on the app's behalf, caches them, holds any API keys and rate-limits requests. Browsers block many of these feeds from being read directly.
- **Design system:** an original palette, icon set and type (Inter and Barlow Condensed, both free).

Size below is my rough estimate of relative effort: S (small), M (medium) or L (large).

## The apps

### 1. Atlas (the map)

- **In the game:** the map and radar.
- **Version 1:**
  - full-screen styled map with day and night themes
  - a legend that filters blip categories
  - place search
  - tap to drop a waypoint, with a route line, distance and time
  - a corner minimap that rotates with your heading, with a player arrow
  - a district-name banner when you cross into a new neighbourhood
- **Built from:** MapLibre GL JS drawing OpenStreetMap-based tiles from OpenFreeMap (free, no key, no service guarantee), with a self-hosted Protomaps file as the fallback. Routing comes from the openrouteservice free plan (2,000 routes a day) through the Worker. The search provider is still to choose: the public Nominatim server can't be used for search-as-you-type.
- **Limits:**
  - on iPhone the compass needs a tap to grant permission
  - GPS stops when the app is in the background
  - "© OpenStreetMap contributors" must stay visible
- **Later:** fog of war, 3D buildings, turn-by-turn guidance.
- **Size:** L.

### 2. Ping (inbox)

- **In the game:** WhatUp, for texts and calls.
- **Version 1:**
  - threads per sender: a system "Dispatch" sender, one per course, one per app
  - messages the phone writes itself: next class in 20 minutes with a "Set waypoint" button, parking timer ending, rain on the way, achievement unlocked
  - timetable import from a calendar (.ics) file, plus manual reminders
  - a call button on a contact opens the phone's real dialer
- **Built from:** on-device data and a calendar-file parser.
- **Limits:** version 1 shows messages in the app and notifies only while it is open. Notifications while the app is closed need a server to send them at the right time, and on iPhone they only work once the app is installed to the home screen.
- **Later:** closed-app notifications; real chat with friends, which needs accounts, moderation and the privacy rules for minors.
- **Size:** M.

### 3. Scene (nearby feed)

- **In the game:** Snapmatic, a social feed the characters can browse but not post to.
- **Version 1:**
  - a vertical swipe feed of cards near you: your own photos, open-licensed geotagged photos, and local event cards
  - "Show on map" and "Set waypoint" on every card
  - likes saved on the device
- **Built from:** Wikimedia Commons' location search for photos (each card must show the author and licence), and campus or community calendar feeds for events, added by hand per campus.
- **Limits:** events are the weak point. I know of no free worldwide events source I can vouch for, so quality depends on the feeds curated for each city or campus. Commons has many landmarks and few everyday scenes.
- **Later:** friends' posts. This needs accounts, photo storage and moderation, and is the heaviest item in the whole plan.
- **Size:** M.

### 4. Lens and Roll (camera and gallery)

- **In the game:** Camera and Gallery.
- **Version 1:**
  - Lens: rear and selfie camera, a handful of original filters and frames, and a stamp with place name and time
  - Roll: photo grid, detail view, delete, share through the phone's share sheet, export
  - every photo becomes a blip on Atlas where it was taken
- **Built from:** the browser camera, canvas filters, on-device storage and the browser's share feature.
- **Limits:** photos live only in this browser on this device. Browser camera quality is below the phone's own camera app (no night mode or HDR), so Roll also accepts photos imported from the phone's gallery.
- **Later:** cloud backup with accounts; video.
- **Size:** M.

### 5. Hail (rides)

- **In the game:** RydeMe, ride-hailing and fast travel.
- **Version 1:**
  - pick a destination from a waypoint, a contact or search
  - see distance and estimated drive time from the app's own routing
  - buttons that open a ride app with the trip prefilled
  - a transit button that opens Google Maps transit directions
- **Built from:** Uber's universal links, which Uber documents for mobile web. A drop-off needs coordinates plus an address or nickname. Other providers (Lyft, Ola, Rapido, Bolt and so on) are added per country; I have not confirmed their link formats yet.
- **Limits:** no in-app booking, live fares or driver tracking. Those need partner access from each ride company.
- **Later:** campus shuttle timetable; a carpool board for students (accounts).
- **Size:** S.

### 6. Wheels (vehicles)

- **In the game:** Scooter Bros, which delivers your car to you.
- **Version 1:**
  - nearby shared bikes and scooters as blips, with a route to the nearest and a button to open the operator's app
  - a "Parked here" pin: one tap saves the spot, with an optional photo and note, a parking timer that pings the inbox, and a route back
- **Built from:** GBFS, the open data standard that bike and scooter operators publish. MobilityData's catalog lists between about 900 and 1,500 systems depending on the source. Feeds go through the Worker with caching.
- **Limits:** coverage depends on the city, and the catalog has no quality check, so some feeds will be dead. Where a city has no feed, only the parked pin works.
- **Size:** M.

### 7. Stash (money)

- **In the game:** BuckMe, with a checking account, an ATM finder and a shared savings account.
- **Version 1:**
  - manual income and expense log with categories
  - a monthly budget showing what is left
  - an ATM finder as blips on Atlas, with a route
  - a savings goal with a progress bar
  - export to a spreadsheet file
- **Built from:** on-device data, with ATM locations from OpenStreetMap. Whether the map tiles already carry ATMs or a separate OpenStreetMap query is needed is still to confirm.
- **Limits:** no connection to real bank accounts and no real money moves. Linking to banks needs a paid aggregator and compliance work. The numbers are only as good as what you type in.
- **Later:** a shared goal and bill-splitting with friends (accounts); a "pay" button that opens your own payment app where a link standard exists, such as UPI in India.
- **Size:** M.

### 8. Spotter (car identifier)

- **In the game:** WAiNK, which scans parked cars for locks, alarms and trackers so you can steal them.
- **Version 1:**
  - point the camera at a car and get make, model, approximate years and body type, with a confidence note
  - save it to a "garage" collection with photo and location
  - collection stats, such as brands spotted
- **Built from:** one photo sent to a vision AI model through the Worker, which holds the key and caps scans per device. On the default model, Claude Opus 5.5, my estimate is about 1 cent per scan. That assumes roughly 2,000 tokens for the image and 150 for the answer, at $4 and $20 per million tokens. Claude Haiku 5.5 ($0.10 and $0.50) would cost a small fraction of a cent with lower accuracy; that choice is yours.
- **Limits:**
  - this is the only app with a per-use cost, and it needs a paid API key and a daily cap
  - photos can include number plates and people, so images are downscaled, sent only for identification and not stored on the server
  - rare or modified cars will be misidentified
  - it will not check locks, alarms or trackers
- **Later:** an on-device model to remove the cost.
- **Size:** M.

### 9. Stride (fitness)

- **In the game:** Fitness, tracking workouts, food and sleep.
- **Version 1:**
  - start and stop a walk, run or ride, with live distance, time and pace
  - the path drawn on Atlas
  - history and weekly totals
  - a manual log for gym sessions, sleep and water
- **Built from:** browser GPS, plus the browser's screen wake lock to keep recording.
- **Limits:** a browser can't read steps, heart rate or sleep from the phone's health system, and it stops tracking when the screen is off or the app is in the background. Recording only works with the app open on screen.
- **Later:** a native build that reads Apple Health and Android's Health Connect; walks feeding fog-of-war discovery.
- **Size:** M.

### 10. Sky (weather)

- **In the game:** Weather.
- **Version 1:**
  - now, the next 24 hours and 7 days, for your location and saved places
  - a rain alert sent to the inbox
  - Atlas switches between day and night themes at sunrise and sunset
- **Built from:** Open-Meteo, which needs no key. Its homepage says non-commercial use is free up to 10,000 calls a day, and attribution is required.
- **Limits:** the free tier is non-commercial only, so a version that earns money needs a paid plan or another source. Some users report rate-limit errors below the stated cap, so forecasts are cached per location.
- **Size:** S.

### 11. Wire (news)

- **In the game:** News.
- **Version 1:**
  - a headline list from chosen local sources, with source, time and image
  - tapping a headline opens the publisher's page
  - a campus news feed for students
- **Built from:** publishers' RSS feeds, fetched and cached by the Worker.
- **Limits:** headlines and links only; full articles stay on the publisher's site. Sources have to be picked per city.
- **Later:** stories that name a place pinned onto Atlas.
- **Size:** S.

### 12. People (contacts)

- **In the game:** Contacts.
- **Version 1:**
  - people and places with a name, picture, phone number, saved location and notes
  - a call button that opens the real dialer, and a "Route to" button
  - import from the phone's contacts where the browser allows it
- **Built from:** on-device data. The browser contact picker works on Android Chrome; I believe it does not on iPhone, which needs checking.
- **Limits:** contacts stay on the device and nothing is uploaded.
- **Size:** S.

### 13. Settings

- **In the game:** Settings, for wallpaper and ringtones.
- **Version 1:**
  - theme, wallpaper and units
  - home location and minimap options
  - permission status for location, compass, camera and notifications, with a fix button for each
  - backup and restore of all data to a file, and clear data
  - a credits page with map and weather attribution and a "not affiliated with any game" notice
- **Size:** S.

### 14. Real estate (deferred)

- **In the game:** Vice City Real Estate, for buying garages.
- **Plan:** not in version 1. A possible later version is a student housing board with listings pinned on Atlas. It needs accounts, moderation and fraud handling, and listing portals generally don't allow their data to be reused.

### 15. Dating app (not planned)

- **In the game:** visible only on another character's phone and not usable.
- **Plan:** not built.

## Build order

1. Foundation and Settings.
2. Atlas.
3. Sky, Lens and Roll. This is the "looks cool" demo.
4. Hail, Wheels, Stash, Wire, People.
5. Ping with timetable import, Scene, Stride.
6. Spotter, the first piece with a running cost.
7. Later, if wanted: accounts and friend features, closed-app notifications, a native build.

## Cost

- **Steps 1–5:** about $10 a year for a domain, with free hosting and free data sources at hobby scale.
- **Step 6:** about 1 cent per car scan on the default model, capped per device and per day.
- **Step 7:** a database (free tier, then about $25 a month), $99 a year for Apple and $25 once for Google Play.

The domain, hosting, database and store figures come from the earlier research and were not checked on vendor pricing pages. The Spotter figure is my estimate from the model prices above.

## Still to verify at build time

- ride-app link formats other than Uber
- Wikimedia Commons location search limits and licence display rules
- iPhone support for closed-app notifications and the contact picker
- whether the map tiles carry ATM locations
- bike and scooter feed coverage for your city

## Needed from you

- **Repo:** an empty one to build in, or a go-ahead to use the existing branch.
- **City and country:** this decides the ride apps, bike feeds, news sources and payment links.
- **Campus and timetable:** which campus, and whether the university exports the timetable as a calendar file.
- **Spotter:** whether a paid AI key with a daily cap is acceptable, and which model.

## Sources

- [Uber: Introduction to deep links](https://developer.uber.com/docs/deep-linking)
- [Uber: deep link FAQ](https://developer.uber.com/docs/riders/ride-requests/tutorials/deep-links/faq)
- [Open-Meteo](https://open-meteo.com/) and [its terms](https://open-meteo.com/en/terms)
- [GBFS FAQ](https://gbfs.org/documentation/faq/)
- [GTABoom: GTA 6 Phone Apps](https://www.gtaboom.com/gta-6-phone-apps-fb38)
- [Beebom: All GTA 6 Phone Apps](https://beebom.com/all-gta-6-phone-apps/)
- [Game8: How to Use Your Phone and All Phone Apps](https://game8.co/games/GTA-6/archives/638295)
- Earlier research in this repo: `reports/GTA style world map app.md`
