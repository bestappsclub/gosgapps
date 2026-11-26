"""Builds the GoSG Explore and GoSG Holiday guide pages. Run: python3 tools/guides.py

Facts come from the apps' own data (Explore: SpotSG/Models/Venues.swift; Holiday: Cuti Shared/Holidays.swift
and SchoolHolidays.swift, sourced from MOM and MOE). Prices and opening hours are never stated here; the pages
link to the official sites instead, so nothing goes stale.
"""
import html
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = "https://gosgapps.com/"
UPDATED = ("2026-11-26", "26 Nov 2026")
APPLE = ('<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M16.37 12.6c-.02-2.2 1.8-3.26 1.88-3.31-1.03-1.5-2.62-1.7-3.18-1.73-1.35-.14-2.65.8-3.33.8-.69 0-1.75-.78-2.88-.76-1.48.02-2.85.86-3.61 2.19-1.54 2.67-.39 6.62 1.11 8.79.73 1.06 1.6 2.25 2.75 2.2 1.1-.04 1.52-.71 2.85-.71 1.33 0 1.7.71 2.87.69 1.19-.02 1.94-1.08 2.66-2.14.84-1.23 1.18-2.42 1.2-2.48-.03-.01-2.3-.88-2.32-3.54zM14.2 6.1c.6-.73 1.01-1.75.9-2.76-.87.04-1.92.58-2.54 1.31-.56.65-1.05 1.69-.92 2.68.97.08 1.96-.49 2.56-1.23z"/></svg>')
GA = ('<script async src="https://www.googletagmanager.com/gtag/js?id=G-153BDPCC9N"></script>\n'
      "<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments)}gtag('js',new Date());"
      "gtag('config','G-153BDPCC9N',{allow_google_signals:false,allow_ad_personalization_signals:false});</script>")

APPS = {
    "explore": dict(name="GoSG Explore", id="6837199347", icon="../img/icon.jpg", css="../site.css",
                    og="explore/img/og-card.jpg", home="../index.html",
                    pitch="Collect a stamp at each place you visit and snap animals and plants to find out what they are.",
                    nav='<a href="../index.html#features">Features</a><a href="index.html">Guides</a><a href="../index.html#faq">FAQ</a>'),
    "holiday": dict(name="GoSG Holiday", id=None, icon="img/icon.jpg", css="../explore/site.css",
                    og="holiday/img/icon.jpg", home="index.html",
                    pitch="Every Singapore public and school holiday, with a countdown, long weekends and add-to-calendar.",
                    nav='<a href="index.html">Holidays</a><a href="long-weekends-2027.html">Long weekends</a><a href="school-holidays-2027.html">School holidays</a>'),
}


def badge(app, ct):
    a = APPS[app]
    if not a["id"]:
        return ('<div class="tryit"><b>All the dates, with a countdown.</b><span>See every holiday on one page, '
                'free. The iPhone app is coming soon.</span><a class="badge" href="index.html"><span><small>Open</small>'
                '<b>GoSG Holiday</b></span></a></div>')
    return (f'<div class="tryit"><b>Take it with you on the day.</b><span>{a["pitch"]} Free on the App Store.</span>'
            f'<a class="badge" href="https://apps.apple.com/sg/app/id{a["id"]}?ct={ct}&amp;pt=127920570" '
            f'aria-label="Download {a["name"]} on the App Store">{APPLE}<span><small>Download on the</small>'
            f'<b>App Store</b></span></a></div>')


def page(app, slug, eyebrow, title, lead, sections, more, faq=None, extra_css=""):
    a = APPS[app]
    url = f"{SITE}{app}/{'guides/' if app == 'explore' else ''}{slug}"
    url = url.replace("index.html", "")
    toc = "".join(f'<li><a href="#{sid}">{html.escape(h)}</a></li>' for sid, h, _ in sections)
    body = "".join(f'<h2 id="{sid}">{html.escape(h)}</h2>{b}' for sid, h, b in sections)
    cards = "".join(f'<a class="card" href="{href}"><small>{s}</small><b>{t}</b><span>{d}</span></a>'
                    for href, s, t, d in more)
    ld = [{"@context": "https://schema.org", "@type": "Article", "headline": title, "description": lead,
           "dateModified": UPDATED[0], "inLanguage": "en-SG",
           "author": {"@type": "Organization", "name": "GoSG", "url": SITE},
           "publisher": {"@type": "Organization", "name": "GoSG", "url": SITE, "logo": SITE + "img/gosg.jpg"},
           "mainEntityOfPage": url, "image": SITE + a["og"]}]
    if faq:
        ld.append({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": ans}} for q, ans in faq]})
        body += "<h2 id=\"faq\">Quick answers</h2>" + "".join(
            f"<h3>{html.escape(q)}</h3><p>{html.escape(ans)}</p>" for q, ans in faq)
    banner = f'<meta name="apple-itunes-app" content="app-id={a["id"]}">\n' if a["id"] else ""
    lds = "".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>\n' for x in ld)
    t = html.escape(title)
    logo_href = "../index.html" if app == "explore" else "index.html"
    crumbs = ('<a href="../index.html">GoSG Explore</a> / <a href="index.html">Guides</a>' if app == "explore"
              else '<a href="../index.html">GoSG</a> / <a href="index.html">Holidays</a>')
    return f"""<!doctype html>
<html lang="en-SG">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{t} | {a["name"]}</title>
<meta name="description" content="{html.escape(lead)}">
<link rel="canonical" href="{url}">
{banner}<meta name="robots" content="index,follow,max-image-preview:large">
<meta property="og:type" content="article">
<meta property="og:site_name" content="GoSG">
<meta property="og:locale" content="en_SG">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{t}">
<meta property="og:description" content="{html.escape(lead)}">
<meta property="og:image" content="{SITE}{a["og"]}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{a["icon"]}">
<link rel="stylesheet" href="{a["css"]}">
<style>.post table{{width:100%;border-collapse:collapse;margin:14px 0 6px;font-size:15px}}.post th,.post td{{text-align:left;padding:9px 8px;border-bottom:1px solid rgba(127,127,127,.25);vertical-align:top}}.post th{{font-size:13px;opacity:.75}}{extra_css}</style>
{lds}{GA}
</head>
<body>
<header class="bar"><div class="wrap">
  <a class="logo" href="{logo_href}"><img src="{a["icon"]}" alt=""> {a["name"]}</a>
  <nav>{a["nav"]}</nav>
</div></header>

<article class="wrap narrow post">
  <p class="crumb">{crumbs}</p>
  <p class="eyebrow">{eyebrow}</p>
  <h1 class="ph1">{t}</h1>
  <p class="lead dark">{html.escape(lead)}</p>
  <p class="meta">GoSG team · Updated {UPDATED[1]}</p>
  <nav class="toc"><b>On this page</b><ol>{toc}</ol></nav>
  {body}
  {badge(app, f"gosg{app}-{slug.replace('.html', '')}")}
  <h2>Keep reading</h2><div class="cards">{cards}</div>
</article>

<footer><div class="wrap cols">
  <div><b>GoSG</b><p>Free apps for getting around Singapore, days out and holidays.</p></div>
  <div><b>Apps</b><a href="{SITE}bus/">GoSG Bus</a><a href="{SITE}explore/">GoSG Explore</a><a href="{SITE}holiday/">GoSG Holiday</a></div>
  <div><b>Guides</b><a href="{SITE}explore/guides/">Days out in Singapore</a><a href="{SITE}holiday/long-weekends-2027.html">Long weekends 2027</a><a href="{SITE}bus/guides/">Bus guides</a></div>
  <div><b>Contact</b><a href="mailto:bestappsclub@gmail.com">bestappsclub@gmail.com</a></div>
</div><div class="wrap fine">© 2026 Best Apps Club · Check opening hours and prices on each place's official site before you go.</div></footer>
</body>
</html>
"""


def link(url, text):
    return f'<a href="{url}" rel="noopener">{text}</a>'


BUS = f'{link(SITE + "bus/", "GoSG Bus")}'

# ---------------------------------------------------------------- Explore guides
EX = []

EX.append(("zoo-vs-night-safari.html", "Mandai", "Singapore Zoo or Night Safari? How to choose",
    "Both are in Mandai, but they're different days out. What you'll see at each, who each suits, and how to fit in Bird Paradise, River Wonders and Rainforest Wild.",
    [("difference", "The short answer", "<p><b>Singapore Zoo</b> is a daytime visit: open, shady paths and big animals you can see clearly, like orangutans, white tigers, Asian elephants, proboscis monkeys and pygmy hippos. <b>Night Safari</b> starts in the evening: you see animals that are active after dark, like the Malayan tiger, fishing cat, slow loris, pangolin and spotted hyena, partly from a tram and partly on walking trails.</p><p>With young children, the Zoo is usually easier: daylight, splash areas, and you can leave whenever you like. Night Safari suits older kids and adults who don't mind a late night.</p>"),
     ("table", "Side by side", "<table><tr><th></th><th>Singapore Zoo</th><th>Night Safari</th></tr><tr><td>When</td><td>Daytime</td><td>Evening and night</td></tr><tr><td>Getting around</td><td>Walking paths</td><td>Tram plus walking trails</td></tr><tr><td>Animals to look for</td><td>Orangutan, white tiger, elephant, proboscis monkey, pygmy hippo, white rhino</td><td>Malayan tiger, fishing cat, slow loris, pangolin, spotted hyena, Indian rhino</td></tr><tr><td>Best for</td><td>Young kids, first visits</td><td>Older kids, adults, something different</td></tr></table>"),
     ("mandai", "The other three Mandai parks", f"<p>Mandai has five parks next to each other. <b>Bird Paradise</b> has walk-through aviaries with macaws, penguins, flamingos and hornbills. <b>River Wonders</b> has the giant pandas and red pandas, manatees and giant river otters. <b>Rainforest Wild</b> has treetop walks with gibbons, langurs and binturongs. Many families pair the Zoo with River Wonders on the same day, or Bird Paradise with Night Safari.</p><p>Tickets, park hours and bundles change, so check {link('https://www.mandai.com', 'mandai.com')} before you go.</p>"),
     ("app", "Make it a game for the kids", "<p>In GoSG Explore, each Mandai park has its own stamp, and collecting all five earns the Mandai badge. Point the camera at an animal and the app tells you what it is, with a few facts kids can read out. At the end of the day, replay your route on the map with your photos.</p>"),
     ("getting-there", "Getting there by bus", f"<p>Mandai is served by public buses from several MRT stations. Open {BUS} at your stop to see which bus to Mandai comes first, and set a leave-now alert so you don't wait in the sun.</p>")],
    [("pulau-ubin-day-trip.html", "Day trip", "A day on Pulau Ubin with kids", "Bumboat, bikes, Chek Jawa and what to bring."),
     ("free-places-singapore-families.html", "Free", "Free places to explore in Singapore with kids", "Gardens, reserves and beaches that cost nothing.")],
    [("Which is better for young kids, Singapore Zoo or Night Safari?", "Singapore Zoo is usually easier for young children: it's in daylight, you walk at your own pace and can leave any time. Night Safari runs late into the evening."),
     ("Can you do Singapore Zoo and Night Safari on the same day?", "Yes, they are next to each other in Mandai. Many people do the Zoo in the afternoon and Night Safari after dinner. Check mandai.com for park hours and combined tickets.")]))

EX.append(("rainy-day-singapore-kids.html", "Rainy days", "Rainy day in Singapore? Indoor places to take the kids",
    "Indoor days out for when the afternoon storm arrives: aquariums, science, the Rain Vortex and the cool domes at Gardens by the Bay.",
    [("list", "Indoor places that are worth the trip", "<p><b>Singapore Oceanarium</b> (Sentosa): manta rays, sharks, jellyfish and sea turtles, all under cover.</p><p><b>Science Centre Singapore</b>: hands-on exhibits, the Omni-Theatre and KidsSTOP for younger children.</p><p><b>Jewel Changi Airport</b>: the Rain Vortex indoor waterfall, the Shiseido Forest Valley and Canopy Park. Watching the waterfall is free.</p><p><b>Gardens by the Bay</b>: the Flower Dome and Cloud Forest are cool, dry glasshouses, with a waterfall, a baobab tree and pitcher plants.</p><p><b>National Gallery Singapore</b>: big rooms, a rooftop garden and children's spaces. <b>ArtScience Museum</b> at Marina Bay Sands has hands-on exhibitions too.</p>"),
     ("tips", "Tips for wet weather", "<p>Singapore's rain often comes as a heavy storm in the afternoon and clears within an hour or two. Plan indoor places for the afternoon and keep outdoor plans for the morning. If there is lightning, NParks may close exposed trails and some outdoor areas until it passes.</p>"),
     ("app", "Still collect your stamps", "<p>Every place above has a stamp in GoSG Explore, so a rainy day still fills the family passport. In the Oceanarium or the Cloud Forest, point the camera at a fish or a plant and the app names it.</p>"),
     ("bus", "Getting there without getting soaked", f"<p>Check {BUS} before you step out: live arrivals mean less waiting at an open stop, and the MRT map shows which station exit is closest.</p>")],
    [("zoo-vs-night-safari.html", "Mandai", "Singapore Zoo or Night Safari?", "How to choose, and how to fit in the other Mandai parks."),
     ("free-places-singapore-families.html", "Free", "Free places to explore in Singapore with kids", "Gardens, reserves and beaches that cost nothing.")],
    [("Where can kids go in Singapore when it rains?", "Good indoor options are the Singapore Oceanarium on Sentosa, Science Centre Singapore, Jewel Changi Airport, the Flower Dome and Cloud Forest at Gardens by the Bay, and National Gallery Singapore.")]))

EX.append(("pulau-ubin-day-trip.html", "Day trip", "A day on Pulau Ubin with kids: how to go and what to see",
    "Take the bumboat from Changi, rent bikes, walk the Chek Jawa boardwalk and look out for wild boar and hornbills. A simple plan for families.",
    [("getting-there", "Getting there", f"<p>Bumboats to Pulau Ubin leave from <b>Changi Point Ferry Terminal</b>, next to Changi Village. Boats go when they're full, and the ride is about 10 to 15 minutes. Bring cash for the fare, and check the current fare at the jetty.</p><p>Several bus services end at Changi Village Bus Terminal. Open {BUS} to see which one comes first from your stop.</p>"),
     ("plan", "A simple plan for the day", "<p><b>Morning:</b> rent bicycles in the village near the jetty (kids' bikes and bikes with child seats are usually available) and ride the main roads, which are quiet and mostly flat.</p><p><b>Late morning:</b> head to <b>Chek Jawa Wetlands</b> on the east side. The boardwalk goes over mangroves and the sea, where you may see mudskippers, fiddler crabs, herons and seagrass. At low tide, more sea life is visible.</p><p><b>Lunch:</b> the village has simple seafood and drinks stalls.</p>"),
     ("see", "What to look for", "<p>Wild boar (keep your distance and never feed them), oriental pied hornbills, long-tailed macaques, mangroves, jackfruit trees and old kampong houses. Pulau Ubin is one of the last places in Singapore with a kampong village.</p>"),
     ("bring", "What to bring", "<p>Water, sunscreen, insect repellent, a hat, cash, and a bag to carry your rubbish back. Shade is patchy on the roads, so morning is cooler.</p>"),
     ("app", "Two stamps in one trip", "<p>GoSG Explore has separate stamps for Pulau Ubin and Chek Jawa, so one trip fills two pages of the passport. Snap a hornbill or a crab and the app tells you what it is. Back home, your photos replay along the route you cycled.</p>")],
    [("free-places-singapore-families.html", "Free", "Free places to explore in Singapore with kids", "Gardens, reserves and beaches that cost nothing."),
     ("rainy-day-singapore-kids.html", "Rainy days", "Rainy day? Indoor places for kids", "Aquariums, science and cool domes.")],
    [("How do you get to Pulau Ubin?", "Take a bumboat from Changi Point Ferry Terminal near Changi Village. The ride is about 10 to 15 minutes and boats leave when they're full. Bring cash for the fare."),
     ("Is Pulau Ubin good for kids?", "Yes. The roads are quiet for cycling, you can rent kids' bikes in the village, and the Chek Jawa boardwalk is an easy walk with lots of wildlife to spot.")]))

FREE_ROWS = [
    ("Singapore Botanic Gardens", "Orchids, swans, huge rain trees. The National Orchid Garden inside charges entry; the rest is free."),
    ("Gardens by the Bay (outdoor gardens)", "The Supertree Grove and outdoor gardens are free. The domes charge entry."),
    ("MacRitchie Reservoir", "Forest trails and boardwalks with monkeys, monitor lizards and squirrels."),
    ("Bukit Timah Nature Reserve", "Singapore's highest hill, in old rainforest. Look for colugos."),
    ("Southern Ridges and Henderson Waves", "A long walk on bridges through the treetops, with hornbills and butterflies."),
    ("Sungei Buloh Wetland Reserve", "Mudskippers, crabs, monitor lizards and sometimes a saltwater crocodile."),
    ("Jurong Lake Gardens", "Otters, herons and a big nature playground in the west."),
    ("Fort Canning Park", "The tree tunnel, the spice garden and history in the city centre."),
    ("East Coast Park and Coney Island Park", "Beaches, cycling and quiet casuarina woods."),
    ("Labrador Nature Reserve", "A rocky shore and old fort ruins by the sea."),
    ("Haw Par Villa", "Thousands of statues from Chinese myths. The park is free; the museum inside charges entry."),
    ("Jewel Changi Airport (Rain Vortex)", "Watching the indoor waterfall is free."),
    ("Chinatown, Little India, Kampong Gelam, Katong and Tiong Bahru", "Temples, murals, shophouses and hawker food."),
]
EX.append(("free-places-singapore-families.html", "Free", "Free places to explore in Singapore with kids",
    "Thirteen free days out from GoSG Explore's 37 places: gardens, nature reserves, beaches and neighbourhoods, with what to look for at each.",
    [("list", "Free places, and what to look for", "<table><tr><th>Place</th><th>Why go</th></tr>" + "".join(
        f"<tr><td><b>{html.escape(n)}</b></td><td>{html.escape(w)}</td></tr>" for n, w in FREE_ROWS) + "</table><p>Entry rules change sometimes, so check the official site for anything you plan around.</p>"),
     ("app", "Turn free days out into a collection", "<p>All of these places have a stamp in GoSG Explore. Kids love filling the passport, and the camera turns any walk into a hunt: point it at a bird, a lizard or a flower and find out what it is.</p>"),
     ("bus", "Getting there", f"<p>Most of these are an easy bus ride away. {BUS} shows live arrivals at your stop and the MRT map shows station exits.</p>")],
    [("zoo-vs-night-safari.html", "Mandai", "Singapore Zoo or Night Safari?", "How to choose between them."),
     ("pulau-ubin-day-trip.html", "Day trip", "A day on Pulau Ubin with kids", "Bumboat, bikes and Chek Jawa.")],
    [("What can you do for free in Singapore with kids?", "Free options include the Botanic Gardens, the outdoor gardens at Gardens by the Bay, MacRitchie Reservoir, Bukit Timah Nature Reserve, the Southern Ridges, Sungei Buloh Wetland Reserve, Jurong Lake Gardens, East Coast Park and the Rain Vortex at Jewel.")]))

# ---------------------------------------------------------------- Holiday pages
LW = [  # (holiday, dates, days off, note)
    ("New Year's Day", "Fri 1 Jan – Sun 3 Jan", "3 days", ""),
    ("Chinese New Year", "Sat 6 Feb – Mon 8 Feb", "3 days", "Day 2 falls on Sunday, so Monday 8 Feb is a holiday. Schools are also off on Tue 9 Feb."),
    ("Good Friday", "Fri 26 Mar – Sun 28 Mar", "3 days", ""),
    ("Hari Raya Haji", "Sat 15 May – Mon 17 May", "3 days", "Vesak Day is the same week, so this is a good week to take leave."),
    ("National Day", "Sat 7 Aug – Mon 9 Aug", "3 days", "Schools are also off on Tue 10 Aug."),
]
BRIDGE = [
    ("Hari Raya Puasa", "Wed 10 Mar", "Take Thu 11 and Fri 12 Mar: 5 days off for 2 days of leave. School March holidays start Sat 13 Mar."),
    ("Hari Raya Haji + Vesak Day", "Mon 17 May and Thu 20 May", "Take Tue 18, Wed 19 and Fri 21 May: 9 days off (Sat 15 – Sun 23 May) for 3 days of leave."),
    ("Deepavali", "Thu 28 Oct", "Take Fri 29 Oct: 4 days off for 1 day of leave."),
]
SAT = [("Labour Day", "Sat 1 May", "Schools are off on Mon 3 May."), ("Christmas Day", "Sat 25 Dec", "")]

lw_table = "<table><tr><th>Holiday</th><th>Long weekend</th><th>Off</th></tr>" + "".join(
    f"<tr><td><b>{h}</b>{'<br><small>' + n + '</small>' if n else ''}</td><td>{d}</td><td>{o}</td></tr>" for h, d, o, n in LW) + "</table>"
br_table = "<table><tr><th>Holiday</th><th>Date</th><th>Leave plan</th></tr>" + "".join(
    f"<tr><td><b>{h}</b></td><td>{d}</td><td>{p}</td></tr>" for h, d, p in BRIDGE) + "</table>"
sat_list = "".join(f"<p><b>{h}</b>, {d}. {n}</p>" for h, d, n in SAT)
MOM = link("https://www.mom.gov.sg/employment-practices/public-holidays", "MOM")
MOE = link("https://www.moe.gov.sg/news/press-releases/20260714-school-terms-and-holidays-for-2027", "MOE")

HOL = []
HOL.append(("long-weekends-2027.html", "2027", "Singapore long weekends in 2027 (and how to stretch them)",
    "Singapore has 5 long weekends in 2027: New Year, Chinese New Year, Good Friday, Hari Raya Haji and National Day. Plus the best days to take leave for longer breaks.",
    [("long-weekends", "The 5 long weekends in 2027", lw_table + f"<p>When a public holiday falls on a Sunday, the Monday after is a public holiday ({MOM}).</p>"),
     ("leave", "Best days to take leave", br_table),
     ("saturday", "Holidays on a Saturday", sat_list + "<p>When a holiday falls on a Saturday there is no automatic Monday off. Employers give a day off in lieu or a day's pay instead, depending on your contract.</p>"),
     ("all", "All 11 public holidays in 2027", "<p>New Year's Day (Fri 1 Jan), Chinese New Year (Sat 6 and Sun 7 Feb), Hari Raya Puasa (Wed 10 Mar), Good Friday (Fri 26 Mar), Labour Day (Sat 1 May), Hari Raya Haji (Mon 17 May), Vesak Day (Thu 20 May), National Day (Mon 9 Aug), Deepavali (Thu 28 Oct) and Christmas Day (Sat 25 Dec).</p>"),
     ("plan", "Plan a long weekend in Singapore", f"<p>Staying home? {link(SITE + 'explore/guides/', 'GoSG Explore')} has 37 places to collect stamps at, from Mandai to Pulau Ubin, and {BUS} gets you there.</p>")],
    [("school-holidays-2027.html", "School", "Singapore school holidays 2027", "MOE term breaks and extra school days off."),
     ("index.html", "All dates", "Singapore public and school holidays", "2026 and 2027 on one page, with a countdown.")],
    [("How many long weekends does Singapore have in 2027?", "Five: New Year's Day (1–3 Jan), Chinese New Year (6–8 Feb), Good Friday (26–28 Mar), Hari Raya Haji (15–17 May) and National Day (7–9 Aug)."),
     ("When should I take leave in 2027 in Singapore?", "The best value is the week of Hari Raya Haji and Vesak Day: take Tue 18, Wed 19 and Fri 21 May for 9 days off. For Hari Raya Puasa, take Thu 11 and Fri 12 Mar for 5 days off.")]))

SCH = [("March holidays", "Sat 13 Mar – Sun 21 Mar"), ("June holidays", "Sat 29 May – Sun 27 Jun"),
       ("September holidays", "Sat 4 Sep – Sun 12 Sep"), ("Year-end holidays", "Sat 20 Nov – Fri 31 Dec")]
EXTRA = [("Tue 9 Feb", "Off-in-lieu for Chinese New Year"), ("Mon 3 May", "Off-in-lieu for Labour Day"),
         ("Mon 5 Jul", "Youth Day school holiday"), ("Tue 10 Aug", "Day after National Day"),
         ("Fri 3 Sep", "Teachers' Day"), ("Fri 8 Oct", "Children's Day (primary schools only)")]
HOL.append(("school-holidays-2027.html", "2027", "Singapore school holidays 2027: MOE term breaks",
    "MOE school holidays for 2027: March 13–21, June 29 May–27 Jun, September 4–12 and year-end from 20 Nov, plus the extra school days off.",
    [("breaks", "Term breaks", "<table><tr><th>Break</th><th>Dates</th></tr>" + "".join(f"<tr><td><b>{a}</b></td><td>{b}</td></tr>" for a, b in SCH) + f"</table><p>These are for primary and secondary schools, as announced by {MOE} on 14 Jul 2026.</p>"),
     ("extra", "Extra school days off", "<table><tr><th>Date</th><th>Why</th></tr>" + "".join(f"<tr><td>{a}</td><td>{b}</td></tr>" for a, b in EXTRA) + "</table>"),
     ("ideas", "Ideas for the holidays", f"<p>Need things to do? Our {link(SITE + 'explore/guides/', 'days-out guides')} cover free places, rainy-day options, Mandai and Pulau Ubin. GoSG Explore turns each outing into a stamp collection for the kids.</p>")],
    [("long-weekends-2027.html", "2027", "Singapore long weekends in 2027", "5 long weekends and the best days to take leave."),
     ("../explore/guides/free-places-singapore-families.html", "Free", "Free places to explore with kids", "13 free days out in Singapore.")],
    [("When are the 2027 June school holidays in Singapore?", "Saturday 29 May to Sunday 27 June 2027."),
     ("When do schools close for the year in 2027?", "The year-end school holidays start on Saturday 20 November 2027 and run to 31 December.")]))

GUIDE_INDEX = [(s, e, t, l) for s, e, t, l, *_ in EX]


def explore_index():
    cards = "".join(f'<a class="card" href="{s}"><small>{e}</small><b>{html.escape(t)}</b><span>{html.escape(l)}</span></a>'
                    for s, e, t, l in GUIDE_INDEX)
    return page("explore", "index.html", "Guides", "Days out in Singapore: family guides",
                "Practical guides for days out in Singapore with kids: Mandai, Pulau Ubin, free places and rainy days.",
                [("guides", "All guides", f'<div class="cards">{cards}</div>')],
                [("../../holiday/long-weekends-2027.html", "2027", "Singapore long weekends in 2027", "Plan your days out around them."),
                 ("../index.html", "App", "GoSG Explore", "Stamps at 37 places and a camera that names what you see.")])


def main():
    out = ROOT / "explore" / "guides"
    out.mkdir(exist_ok=True)
    for slug, eb, t, l, secs, more, faq in EX:
        (out / slug).write_text(page("explore", slug, eb, t, l, secs, more, faq))
    (out / "index.html").write_text(explore_index())
    for slug, eb, t, l, secs, more, faq in HOL:
        (ROOT / "holiday" / slug).write_text(page("holiday", slug, eb, t, l, secs, more, faq))
    print("built", len(EX) + 1 + len(HOL), "pages")


if __name__ == "__main__":
    main()
