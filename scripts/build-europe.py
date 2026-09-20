#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build data/europe.json: Dad's trip, 5 December 2026 to 10 January 2027.

Shared. He is the one who opens it, so everything is written TO him in second
person, not about him. He is 63, travelling alone, walks fine, and says he gets
overwhelmed easily, so the rule for this trip is one decision at a time and
never more than one thing per half-day.

Four things are fixed and everything else hangs off them:

    Sat  5 Dec 16:10   land Heathrow
    Fri 11 Dec 09:30   cruise departs        (FROM WHERE IS NOT YET KNOWN)
    Tue 22 Dec 14:45   cruise returns
    Sun 10 Jan 13:40   Heathrow, fly home

That leaves 6 nights before the cruise and 19 nights after it. Christmas with
your daughter and the football on the 30th sit inside the second block, so the
genuinely free stretch is about 8 nights from New Year.

    python3 scripts/build-europe.py
"""
import datetime
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _carry import carry_over   # noqa: E402

UPDATED = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z')
START, END = '2026-12-05', '2027-01-10'

# Rough only. Change them on the Budget page once you are closer and the real
# rate is known; every foreign amount on this trip converts through these.
RATES = {'GBP': 0.52, 'EUR': 0.57, 'NOK': 6.70}


def item(id, time, type, title, **kw):
    d = dict(id=id, time=time, type=type, title=title, status=kw.pop('status', 'planned'))
    d.update(kw)
    return d


# Items that are known for a given date. Everything else gets an empty day.
ITEMS = {
  '2026-12-05': [
    item('a1', '16:10', 'flight', 'Land at Heathrow', location='London Heathrow', status='booked',
         notes='Arriving 16:10 on a Saturday, which is the good news: your daughter is not at work. Expect 45-90 min through the border, then the Elizabeth line or the Heathrow Express into town. Buy nothing at the airport except water. If she is not collecting you, agree BEFORE you fly exactly where you are meeting, because Heathrow has four terminals and phone signal in the baggage hall is poor.'),
    item('a2', '18:30', 'stay', 'First night in London', location='Your daughter’s, or a hotel near her',
         notes='ONE OF THE OPEN QUESTIONS: are you sleeping at her place or booking somewhere? It changes about 25 nights of this trip and it is the first thing to settle. See Decisions.'),
  ],
  '2026-12-11': [
    item('c0', '06:00', 'transfer', 'Get to the ship', location='Cruise terminal, port not yet confirmed',
         notes='BIGGEST UNKNOWN IN THE PLAN. A 09:30 departure means boarding closes well before that, usually two hours ahead. If the ship leaves from a UK port (Southampton, Dover, Tilbury, Newcastle) this is a train or a coach from London the same morning, and 09:30 is brutally early, so you would almost certainly go down the night before. If it leaves from Bergen, you need a flight out of London on the 10th and a hotel in Norway that night. Find the booking and tell Connor the port; nothing around these dates can be planned until it is known.'),
    item('c1', '09:30', 'boat', 'Cruise departs', status='booked', location='See above',
         notes='11 nights, back on the 22nd. Northern lights.'),
  ],
  '2026-12-22': [
    item('c2', '14:45', 'boat', 'Cruise returns', status='booked',
         notes='Back on dry land at 14:45. Whatever port this is, assume you do not reach London until the evening. Do not plan anything for tonight.'),
  ],
  '2026-12-25': [
    item('x1', '00:00', 'note', 'Christmas Day with your daughter', location='London',
         notes='The fixed point of the whole trip. Nothing else goes near it. Worth knowing: London public transport, the Tube, buses, and the mainline trains, ALL STOP on Christmas Day. Not reduced, stopped. If you are not already where you need to be by Christmas Eve, you are walking or paying a fortune for a taxi.'),
  ],
  '2026-12-30': [
    item('x2', '00:00', 'activity', 'Football', location='Ground not yet confirmed',
         notes='You mentioned a match on the 30th. Tell Connor which one and where, because if it is not in London it decides where you sleep that night. Fixtures move for television, often at short notice, so whoever holds the ticket should check the date again in December.'),
  ],
  '2027-01-10': [
    item('z1', '10:00', 'transfer', 'To Heathrow', location='London Heathrow',
         notes='A 13:40 departure means being at the airport by about 10:40, so leaving central London around 09:30. A Sunday, so check for engineering works on the line the night before.'),
    item('z2', '13:40', 'flight', 'Fly Heathrow to Brisbane', status='booked',
         notes='Home. Roughly 24 hours with one stop.'),
  ],
}

# Days without their own items still need to exist so the plan has a spine.
PHASES = [
  ('2026-12-05', '2026-12-10', 'London, before the cruise', 'London',
   'Six nights with your daughter before the ship. She may be working on the weekdays, which is either time to yourself in London or the window for Ireland. See Decisions.'),
  ('2026-12-11', '2026-12-22', 'Northern lights cruise', 'At sea',
   'Eleven nights. Ports and sea days go in here once the cruise line sends the itinerary. Ask Connor to add them: it is the difference between knowing what tomorrow is and not.'),
  ('2026-12-23', '2027-01-10', 'Christmas, New Year and whatever you decide', 'London',
   'Nineteen nights, anchored by Christmas with your daughter and the football on the 30th. The free stretch is roughly eight nights from New Year, which is exactly one big thing: the Camino, or Ireland, not both.'),
]

days = []
d0 = datetime.date.fromisoformat(START)
d1 = datetime.date.fromisoformat(END)
cur = d0
while cur <= d1:
    iso = cur.isoformat()
    title, base, notes = 'Open', 'London', ''
    for s, e, t, b, n in PHASES:
        if datetime.date.fromisoformat(s) <= cur <= datetime.date.fromisoformat(e):
            title, base, notes = t, b, n
    if iso in ITEMS and iso in ('2026-12-05', '2026-12-11', '2026-12-22', '2026-12-25', '2026-12-30', '2027-01-10'):
        title = {'2026-12-05': 'Land in London', '2026-12-11': 'Board the ship',
                 '2026-12-22': 'Back off the ship', '2026-12-25': 'Christmas Day',
                 '2026-12-30': 'The football', '2027-01-10': 'Fly home'}[iso]
    days.append(dict(id='d' + iso.replace('-', ''), date=iso, title=title, base=base,
                     notes=notes, items=ITEMS.get(iso, [])))
    cur += datetime.timedelta(days=1)

# =============================================================================
# The paperwork. Two of these are hard stops at the airport, not formalities.
# =============================================================================
checklist = [
  dict(id='e1', group='Paperwork', text='Apply for the UK ETA. You cannot board without it', due='2026-10-31',
       notes='Since 25 February 2026 every Australian passport holder needs an Electronic Travel Authorisation to enter the UK, including just changing planes. It costs £20, you apply on the official UK ETA app or at gov.uk, and most decisions come back within minutes, though the Home Office asks you to allow up to three working days. It lasts two years or until the passport expires. THE AIRLINE CHECKS IT AT THE GATE IN BRISBANE. No ETA, no boarding, and no refund. Do this one first and do not use any website that is not gov.uk, because the copycat sites charge four times the price for the same thing.'),
  dict(id='e2', group='Paperwork', text='Check the passport has at least 6 months on it and was issued within the last 10 years', due='2026-09-30',
       notes='Two separate rules and people trip on the second one. For the Schengen countries, which on this trip means Norway and, if you go, Spain, the passport must be valid for at least 3 months after you leave AND have been issued within the last 10 years. An Australian passport renewed early can carry extra months that push its issue date past ten years, and that passport gets refused even though it looks in date. Check the issue date, not just the expiry. Renewal takes about 6 weeks, longer near Christmas.'),
  dict(id='e3', group='Paperwork', text='Watch for ETIAS opening, then apply. Norway needs it, and so would Spain', due='2026-11-15',
       notes='ETIAS is the European travel permit Australians will need for the Schengen countries. Norway is one, so the cruise is affected; Spain is another, so the Camino would be too. It is expected to start in the last months of 2026, with a grace period into 2027 while everyone adjusts, which means your December may fall either side of the line. It will cost about €20. THE APPLICATION SITE IS NOT OPEN YET. Any website taking ETIAS applications today is a scam, and there are a lot of them. Wait, and apply only through the official EU site when it opens. Connor will check the date in November.'),
  dict(id='e4', group='Paperwork', text='Travel insurance for 37 days, aged 63, including the cruise', due='2026-10-31',
       notes='Cruise cover is almost always a separate box you have to tick, and a policy without it will not pay for anything that happens on the ship or for missing the sailing. Declare any medical conditions honestly, because an undeclared one voids the lot. Also: Australia has reciprocal healthcare agreements with the UK, Ireland and Norway, so medically necessary treatment is covered there on your Medicare card. That is genuinely useful but it is NOT insurance: it does not cover getting you home, and it does not cover Spain.'),
  dict(id='e5', group='Before you go', text='Put an eSIM on the iPhone before you leave', due='2026-11-30',
       notes='One eSIM covering the UK and Europe costs about A$20 for the month and saves you from roaming charges and from hunting for wi-fi. Install it at home while you have good internet and someone to help, then switch it on when you land. Keep your Australian number active for texts from the bank.'),
  dict(id='e6', group='Before you go', text='Tell the bank you are travelling, and take two cards', due='2026-11-30',
       notes='Two cards from two different banks, kept in two different places. A card that stops working in Norway on a Sunday is a ruined day if it is the only one you have. Ask your bank what it charges on foreign purchases: 3% is common and adds up over 37 days.'),
  dict(id='e7', group='Before you go', text='Ask the cruise line for the day-by-day itinerary and send it to Connor', due='2026-10-15',
       notes='Which port each day, and what time the ship sails. Once that is in here you will always know what tomorrow is, which is the whole point of having this on your phone.'),
]

# =============================================================================
# The open questions. One per real decision, so nothing is decided twice.
# =============================================================================
questions = [
  dict(id='q1', question='Where does the cruise leave from and come back to?',
       why='Nothing around the 10th, 11th or 22nd of December can be planned until this is known. A UK port means a train from London and a night nearby beforehand. Bergen means a flight out on the 10th and a hotel in Norway.',
       options=['A UK port (Southampton, Dover, Tilbury, Newcastle)', 'Bergen, Norway', 'Somewhere else'],
       recommendation='Find the booking confirmation and read the first line. This is the one that unblocks everything else.', answer='', resolved=False),
  dict(id='q2', question='The Camino or Ireland? There is only room for one',
       why='After the cruise you have 19 nights, but Christmas with your daughter and the football on the 30th are inside them. The free stretch is about eight nights from New Year. Walking the last 100 km of the Camino takes five to six days plus two travel days, which is all eight. Ireland properly done is four or five. They do not both fit in January. THERE IS A WAY TO HAVE BOTH: put Ireland in the first week instead, midweek while your daughter is at work. Dublin is a 1h15 flight from London and they go all day.',
       options=['Ireland in the first week, Camino in January (both, and the best fit)', 'Camino in January, Ireland another time', 'Ireland in January, no Camino', 'Neither, stay in England'],
       recommendation='Ireland from about the 7th to the 10th of December while she is working, then the Camino from New Year. You get both and you are never rushing.', answer='', resolved=False),
  dict(id='q3', question='If you walk the Camino, is the certificate the point?',
       why='This decides where you start and it is not a small difference. The Compostela, the certificate they hand you in Santiago, requires the last 100 km on foot, which means starting at Sarria: 111 km, five or six days of walking, and you must collect two stamps a day. The last 50 km, starting around Palas de Rei, is three days and gets you to the same cathedral with no certificate.',
       options=['Sarria, 111 km, five or six days, and the Compostela at the end', 'Palas de Rei, about 50 km, three days, no certificate', 'Decide closer to the time'],
       recommendation='If you are flying to the other side of the world and walking to Santiago anyway, walk from Sarria. The extra is two days and about 60 km at a gentle pace, and you finish holding the thing that says you did it.', answer='', resolved=False),
  dict(id='q4', question='Where are you sleeping in London?',
       why='About 25 of the 36 nights are London nights. Staying with your daughter and booking a hotel are very different trips and very different money, and you may want a mix: with her over Christmas, somewhere of your own for a few days so nobody is on top of anybody.',
       options=['With your daughter throughout', 'A hotel or apartment throughout', 'A mix: with her for Christmas, your own place otherwise'],
       recommendation='Ask her before you book anything. Five weeks is a long time to have a guest, and she may be relieved to be asked.', answer='', resolved=False),
  dict(id='q5', question='Which football match, and where?',
       why='If it is not in London it decides where you sleep on the 30th and possibly the 29th. Fixtures also get moved for television, sometimes by a day or two and sometimes late.',
       options=['In London', 'Elsewhere in England', 'Not booked yet'],
       recommendation='Whoever holds the ticket should re-check the date in early December, because a move to the 29th or the 31st changes the plan around it.', answer='', resolved=False),
  dict(id='q6', question='Which train journey do you want?',
       why='You said you like the idea of a proper train. Several are already sitting inside this trip at no extra cost: London to Santiago is nothing, but the Camino finishes in Galicia and the Spanish high-speed line back to Madrid is genuinely impressive. In the UK the classic is the West Highland Line from Glasgow to Mallaig, though in January it is dark by four. And the Eurostar out of St Pancras is a train journey that happens to also be transport.',
       options=['Keep it simple: whatever trains the plan already needs', 'Build a day around one scenic line', 'The Eurostar, if any of this touches mainland Europe'],
       recommendation='Decide after the cruise and the Camino are settled. Trains are the easiest thing to add late.', answer='', resolved=False),
  dict(id='q7', question='Do you actually want mainland Europe, or is this a UK, Ireland and Norway trip?',
       why='You said maybe not Europe. Worth knowing that the cruise already takes you into Norway, and the Camino is in Spain, so both are Europe in the sense that matters for paperwork. If the answer is no beyond those, that is a perfectly good trip and it makes the planning much simpler.',
       options=['UK, Ireland and the cruise only', 'Add Spain for the Camino', 'Open to more if it is easy'],
       recommendation='Do not add a fourth country. Five weeks sounds long until you are moving every three days.', answer='', resolved=False),
]

food = [
  dict(id='f1', town='Dublin', dish='Guinness at the Storehouse, and then somewhere better',
       where='Guinness Storehouse, St James’s Gate; then the Long Hall, Kehoe’s or the Palace Bar',
       why='The Storehouse is the tourist one and worth doing once for the view from the Gravity Bar at the top, where the pint is included in the ticket. But the best Guinness in Dublin is in an old pub with a slow pour and a barman who does not rush it. Do the Storehouse in the afternoon, then walk into town and have the real one.', priceBand='€€'),
  dict(id='f2', town='London', dish='A proper pub Sunday roast', where='Any pub with a blackboard and no television',
       why='Beef, Yorkshire pudding, gravy. The thing England does better than anywhere. Book it, because good ones fill up by Thursday.', priceBand='££'),
  dict(id='f3', town='Norway', dish='Whatever is caught that morning', where='The fish market in Bergen, or the ship',
       why='Norway is expensive and the beer especially so, a pint runs A$16 and up, so this is where the budget goes if you let it. Eat on the ship and spend ashore on one good thing a day rather than three ordinary ones.', priceBand='kr kr kr'),
  dict(id='f4', town='Santiago de Compostela', dish='Galician octopus, pimientos de Padrón, and Estrella Galicia',
       where='Rua do Franco, the street of restaurants behind the cathedral',
       why='Pulpo a feira, octopus with paprika and olive oil on a wooden plate, is the dish of the region and Santiago is where to eat it. The local beer is Estrella Galicia and it is very good. This is the meal at the end of the walk.', priceBand='€€'),
]

stays = [
  dict(id='sy1', name='London base (to be decided)', town='London', status='idea', nights=25,
       type='Your daughter’s place, a hotel, or a mix', checkIn='2026-12-05', checkOut='2027-01-10',
       notes='Placeholder until Decisions question 4 is answered. Twenty-five nights is the single biggest cost in this trip, so it is also the biggest saving.'),
]

places = [
  dict(id='py1', name='London Heathrow', kind='airport', town='London', lat=51.4700, lng=-0.4543),
  dict(id='py2', name='Guinness Storehouse', kind='other', town='Dublin', lat=53.3419, lng=-6.2867,
       notes='St James’s Gate. The Gravity Bar at the top has the view and the included pint.'),
  dict(id='py3', name='Santiago de Compostela Cathedral', kind='other', town='Santiago de Compostela', lat=42.8806, lng=-8.5446,
       notes='The end of the Camino. The Pilgrim’s Office, where the Compostela is issued, is a few minutes away on Rúa das Carretas.'),
  dict(id='py4', name='Sarria', kind='town', town='Sarria', lat=42.7810, lng=-7.4140,
       notes='Where the last 100 km starts. 111 km to Santiago, five or six days.'),
  dict(id='py5', name='Bergen', kind='town', town='Bergen', lat=60.3913, lng=5.3221,
       notes='Bryggen, the old wharf, is a UNESCO site and about 15 minutes on foot from the cruise berths.'),
]

trip = dict(
  meta=dict(
    title='Dad’s Trip 2026/27', start=START, end=END, homeCurrency='AUD',
    rates=RATES, updatedAt=UPDATED, version=1,
    mapRegion='', travelMode='transit',
    features=dict(flights=True, budget=True, points=False),
    categories=['Flights', 'Accommodation', 'Transport', 'Food', 'Activities', 'Other'],
    about='Five weeks away: London with your daughter, eleven nights chasing the northern lights, Christmas in London, the football on the 30th, and one more big thing in January. Four times are fixed and the rest is still being decided. Everything open is on the Decisions page, one question at a time.',
  ),
  days=days,
  flights=dict(confirmed=[], legs=[], lounges=[]),
  people=[], foodGuide=[], staysGuide=[], souvenirGuide=[],
  points={}, stays=stays, food=food, souvenirs=[], budget=[], checklist=checklist,
  places=places, questions=questions,
)

trip = carry_over(trip, 'data/europe.json')

with open('data/europe.json', 'w') as f:
    json.dump(trip, f, indent=2, ensure_ascii=False)
    f.write('\n')

print('wrote data/europe.json %d days, %d items, %d todos, %d questions' % (
    len(trip['days']), sum(len(d['items']) for d in trip['days']), len(trip['checklist']), len(trip['questions'])))
