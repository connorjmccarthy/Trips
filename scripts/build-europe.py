#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build data/europe.json: Dad's trip, 5 December 2026 to 10 January 2027.

Shared with him and nobody else: the registry gives this trip audience "dad",
so the link .../Trips/?for=dad shows this and not Bali, Ubud or Japan. Written
in second person because he is the one who opens it.

He is 63, travelling alone, walks fine, and says he gets overwhelmed easily.
So: one thing per half-day, one question at a time, and every leg that could go
wrong has a day of slack in front of it.

The spine, all confirmed:

    Sat  5 Dec 16:10  land Heathrow
    Fri 11 Dec 20:30  Hurtigruten sails from Bergen (NOT 09:30, see below)
    Tue 22 Dec 14:45  Hurtigruten back in Bergen
    Wed 30 Dec        Arsenal v Fulham, Emirates
    Sun 10 Jan 13:40  Heathrow, fly home

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

# Rough. Change them on the Budget page when you are closer.
RATES = {'GBP': 0.52, 'EUR': 0.57, 'NOK': 6.70}


def item(id, time, type, title, **kw):
    d = dict(id=id, time=time, type=type, title=title, status=kw.pop('status', 'planned'))
    d.update(kw)
    return d


def day(date_, title, base, notes, items):
    return dict(id='d' + date_.replace('-', ''), date=date_, title=title, base=base, notes=notes, items=items)


days = [
  # ---------------------------------------------------------------- London
  day('2026-12-05', 'Land in London', 'London',
      'Saturday, so she is not at work. Do nothing today except get to a bed.', [
    item('a1', '16:10', 'flight', 'Land at Heathrow', location='London Heathrow', status='booked',
         notes='Allow 45 to 90 minutes to get through the border and collect the bag. Then the Elizabeth line into central London, about 30 minutes, or the Heathrow Express if you are past caring. AGREE BEFORE YOU FLY exactly where you are meeting her: Heathrow has four terminals, they are miles apart, and the phone signal in the baggage hall is poor.'),
    item('a2', '18:30', 'stay', 'To your daughter’s', location='See Stays',
         notes='Eat whatever she puts in front of you and go to bed early. You will wake at 3am regardless; that is normal and it passes in two days.')]),
  day('2026-12-06', 'London, no plans', 'London',
      'Sunday with her. A roast if she is up for it.', []),
  day('2026-12-07', 'London, your own time', 'London',
      'She is back at work. Three quiet days before the ship: this is deliberate, not a gap to fill. The Imperial War Museum is the one to do if you do one thing.', [
    item('a3', '10:00', 'activity', 'Imperial War Museum', location='Lambeth Road, London SE1 6HZ',
         cost=0, currency='GBP', status='idea',
         notes='Free. The best war museum in the country and the one that will hold you longest: the First World War galleries, the Second World War and Holocaust galleries, and the atrium full of aircraft. Give it three hours. Nearest tube Lambeth North or Elephant & Castle.')]),
  day('2026-12-08', 'London, your own time', 'London', 'Nothing booked. Churchill War Rooms if you want a second war day.', [
    item('a4', '10:00', 'activity', 'Churchill War Rooms', location='Clive Steps, King Charles St, London SW1A 2AQ',
         cost=32, currency='GBP', status='idea',
         notes='The underground bunker Churchill ran the war from, left as it was in 1945. About £32 and you must book a time slot online, it sells out. Two hours. Right by St James’s Park.')]),
  day('2026-12-09', 'London, and pack for Norway', 'London',
      'Pack tonight, not tomorrow morning. Norway in December is dark, wet and about freezing: thermals, a proper waterproof, a warm hat, gloves, and boots with grip.', []),
  # ---------------------------------------------------------------- Bergen
  day('2026-12-10', 'Fly to Bergen', 'Bergen',
      'A day early on purpose. The ship sails tomorrow evening and you do not fly to a cruise on the day it leaves.', [
    item('b1', '08:40', 'flight', 'Norwegian, Gatwick to Bergen', location='London Gatwick to Bergen Flesland',
         endTime='11:35', cost=150, currency='AUD', status='idea',
         notes='Norwegian is the only airline flying this nonstop, about 1h55, and it runs most days. The 08:40 arriving 11:35 is the good one. GATWICK, NOT HEATHROW: allow 90 minutes from central London on the Gatwick Express from Victoria, and leave her place by about 05:30. Book this as soon as the dates are certain; December fares only go up.'),
    item('b2', '13:00', 'transfer', 'Airport to the city', location='Bergen Flesland to the centre',
         cost=50, currency='NOK', status='idea',
         notes='The Bybanen light rail runs from outside the terminal to the city centre in about 45 minutes and costs a fraction of a taxi. Buy the ticket from the machine on the platform.'),
    item('b3', '15:00', 'stay', 'Check in, Bergen', location='See Stays',
         notes='Dark by about 15:30 this far north in December. Do not fight it. Get warm, eat early, sleep.')]),
  day('2026-12-11', 'A day in Bergen, then the ship', 'Bergen',
      'THE DAY YOU ASKED FOR. The ship does not sail until 20:30, so you have the whole of Bergen with a bag already in a hotel. Daylight is roughly 09:30 to 15:30, so front-load it.', [
    item('b4', '09:30', 'activity', 'Bryggen, the old wharf', location='Bryggen, Bergen',
         cost=0, currency='NOK',
         notes='The row of crooked wooden merchant houses on the harbour, UNESCO listed, and the reason people photograph Bergen. Wander the alleys behind the front row. Free, and 10 minutes from the fish market.'),
    item('b5', '11:00', 'food', 'Fish market, then something hot', location='Torget fish market, Bergen',
         cost=300, currency='NOK',
         notes='The indoor market is open year round. Fish soup or a prawn sandwich. BE READY FOR NORWEGIAN PRICES: a pint is about A$16 and a modest lunch A$35. This is the single most expensive country on the trip and you are only here two days, so eat what you want and stop converting.'),
    item('b6', '12:30', 'activity', 'Fløibanen funicular up Mount Fløyen', location='Fløibanen, Vetrlidsallmenningen 23A',
         cost=180, currency='NOK',
         notes='Eight minutes up, and the view back over the city and the fjord is the one to send home. Go before the light goes. Cafe at the top if it is foul.'),
    item('b7', '15:00', 'transfer', 'Collect the bag, get to the terminal', location='Hurtigruten terminal, Nøstegaten 30',
         notes='About 20 minutes on foot from the centre, or a short taxi with the case. Hurtigruten asks you to be in the terminal no later than 30 minutes before departure, so be there by 19:30 at the very latest. Being there at 18:00 with a book is a better evening than cutting it fine.'),
    item('b8', '21:30', 'boat', 'Hurtigruten sails for Kirkenes', location='Bergen', status='booked',
         notes='CONFIRMED 21:30, so today is genuinely yours. Hurtigruten\u2019s published Bergen time is 20:30 and yours says 21:30, which may be a seasonal difference or the particular ship. Either way BE IN THE TERMINAL BY 19:45 and you cannot be caught out. They ask for 30 minutes before departure as a minimum; two hours early with a coffee is a better evening than a taxi you are shouting at.')]),
  # ---------------------------------------------------------------- cruise
  day('2026-12-12', 'At sea, heading north', 'Hurtigruten', '', []),
  day('2026-12-13', 'At sea, heading north', 'Hurtigruten', '', []),
  day('2026-12-14', 'At sea, heading north', 'Hurtigruten',
      'Somewhere around here you cross the Arctic Circle. They make a thing of it.', []),
  day('2026-12-15', 'Tromsø and the lights country', 'Hurtigruten',
      'The middle of the voyage is the best of the northern lights window. Dress for standing still outside in the cold, which is much colder than walking in it.', []),
  day('2026-12-16', 'North Cape and Kirkenes', 'Hurtigruten', '', []),
  day('2026-12-17', 'Kirkenes, then turn south', 'Hurtigruten',
      'The turning point. From here you see by day the ports you passed in the dark.', []),
  day('2026-12-18', 'Southbound', 'Hurtigruten', '', []),
  day('2026-12-19', 'Southbound', 'Hurtigruten', '', []),
  day('2026-12-20', 'Southbound', 'Hurtigruten', '', []),
  day('2026-12-21', 'Southbound, last full day', 'Hurtigruten', 'Pack tonight.', []),
  day('2026-12-22', 'Back in Bergen', 'Bergen',
      'Off the ship at 14:45 and STAYING IN BERGEN TONIGHT. You could chase an evening flight to London but it is two days before Christmas, the airports are at their worst, and if it goes wrong you are stranded on the 23rd. One calm night is worth the hotel.', [
    item('c1', '14:45', 'boat', 'Hurtigruten docks in Bergen', status='booked',
         notes='Eleven nights done.'),
    item('c2', '16:00', 'transfer', 'Straight to Flesland for the evening flight',
         location='Bergen Flesland', endTime='17:15',
         notes='The Bybanen light rail from the centre takes about 45 minutes. A hotel night in Bergen is A$220 you do not have to spend, which is why this is an evening flight rather than a lie-in.'),
    item('c3', '19:30', 'flight', 'Norwegian, Bergen to Gatwick', location='Bergen Flesland to London Gatwick',
         cost=150, currency='AUD', status='idea',
         notes='CHECK AN EVENING FLIGHT ACTUALLY EXISTS ON 22 DEC BEFORE YOU RELY ON THIS. Norwegian runs this route most days and the last departure is usually late evening, but 22 December is peak Christmas traffic. If there is nothing after about 18:00, add a night in Bergen and fly on the 23rd instead: that is A$220 and it is worth paying rather than cutting it fine with an 11-night cruise behind you.')]),
  day('2026-12-23', 'London, Christmas Eve eve', 'London',
      'Nothing planned. Recover.', []),
  day('2026-12-24', 'Christmas Eve', 'London', 'With her. Nothing planned.', []),
  day('2026-12-25', 'Christmas Day', 'London',
      'The fixed point of the whole trip.', [
    item('x1', '09:00', 'note', 'Christmas with your daughter', location='London',
         notes='ONE THING TO KNOW: London transport STOPS on Christmas Day. Not reduced, stopped. No tube, no buses, no trains. If you are not already where you need to be by Christmas Eve night you are walking or paying a fortune for a taxi, if you can find one.')]),
  day('2026-12-26', 'Boxing Day', 'London', 'Quiet. Pack a small bag for Dublin.', []),
  # ---------------------------------------------------------------- Dublin
  day('2026-12-27', 'London, quiet', 'London',
      'THIS WAS DUBLIN. It came out to make the budget work, and adding it back is Decisions question 2: about A$800 for two nights, the flights and the Guinness Storehouse. If the money appears, this is where it goes.', []),
  day('2026-12-28', 'London, quiet', 'London', '', []),
  day('2026-12-29', 'London, quiet', 'London', 'Early night. Football tomorrow.', []),
  # ---------------------------------------------------------------- football
  day('2026-12-30', 'Arsenal v Fulham', 'London',
      'Emirates Stadium. A London derby, and the ground is one of the best in the country.', [
    item('e1', '17:00', 'activity', 'Arsenal v Fulham, Emirates Stadium',
         location='Emirates Stadium, Hornsey Rd, London N7 7AJ', cost=80, currency='GBP', status='booked',
         notes='CHECK THE KICK-OFF TIME AGAIN IN DECEMBER. Premier League fixtures get moved for television, sometimes by a day, and the broadcast picks for this round are usually confirmed about six weeks out. Holloway Road on the Piccadilly line is the nearest tube and it is mobbed afterwards; Arsenal or Finsbury Park are a slightly longer walk and much easier. Go early, the ground is worth seeing filling up. It is cold: more layers than you think.')]),
  day('2026-12-31', 'New Year’s Eve', 'London', 'Whatever she is doing. The fireworks on the Thames need a ticket months ahead, so watch them on television like most of London does.', []),
  day('2027-01-01', 'New Year’s Day', 'London',
      'Rest. Pack for Spain: you are walking 115 km in six days starting the day after tomorrow.', []),
  # ---------------------------------------------------------------- Camino
  day('2027-01-02', 'Fly to Spain, and get to Sarria', 'Sarria',
      'A long travel day, and the only one on the Camino leg. Everything after this is walking.', [
    item('f1', '10:25', 'flight', 'Ryanair, Stansted to Santiago de Compostela',
         location='London Stansted to Santiago de Compostela', endTime='13:35',
         cost=150, currency='AUD', status='idea',
         notes='Ryanair is the only nonstop and IT ONLY FLIES MONDAY, WEDNESDAY AND SATURDAY, which is what fixes these dates. The later of the two departures on purpose: it means leaving London about 07:30 rather than sleeping at the airport, which saves A$180. About 2h10. Hand luggage only if you possibly can, because you are carrying it for six days.'),
    item('f2', '15:00', 'train', 'Santiago to Sarria', location='Santiago de Compostela to Sarria',
         endTime='17:30', cost=25, currency='EUR',
         notes='About 2.5 hours by train or bus. Yes, you travel to the far end and walk back; that is how the last 100 km works. Book the train on Renfe when the date is close.'),
    item('f3', '18:00', 'stay', 'First night in Sarria', location='See Stays',
         notes='GET YOUR CREDENCIAL TONIGHT if you have not already: the pilgrim passport you collect stamps in. The parish church and most pilgrim hostels in Sarria issue them for a couple of euros. Without it there is no Compostela at the other end.')]),
  day('2027-01-03', 'Sarria to Portomarín, 22 km', 'Portomarín',
      'Day one. Rolling farmland, oak woods and stone hamlets. Light from about 08:45 to 18:15, so leave by 09:00 and you have hours in hand.', [
    item('g1', '09:00', 'activity', 'Walk Sarria to Portomarín', endTime='15:30', cost=0, currency='EUR',
         notes='22 km, five to six hours at a steady pace with stops. The 100 km marker is just outside Sarria and everybody photographs it. TWO STAMPS A DAY from here on, from bars, churches or hostels, because the last 100 km has the stricter rule. Portomarín is reached over a long bridge and up a staircase, which is a cruel finish, and the village was moved stone by stone when they dammed the river.')]),
  day('2027-01-04', 'Portomarín to Palas de Rei, 25 km', 'Palas de Rei',
      'The longest day of the six. Start early.', [
    item('g2', '08:45', 'activity', 'Walk Portomarín to Palas de Rei', endTime='15:30', cost=0, currency='EUR',
         notes='25 km with a long steady climb out of Portomarín in the first two hours. Get it done in the morning. There are bars at Gonzar and Ventas de Narón for coffee and a stamp.')]),
  day('2027-01-05', 'Palas de Rei to Melide, 15 km', 'Melide',
      'A short day on purpose, after the long one.', [
    item('g3', '09:30', 'activity', 'Walk Palas de Rei to Melide', endTime='13:30', cost=0, currency='EUR',
         notes='15 km, three to four hours. Melide is the octopus town: Pulpería Ezéquiel is the famous one and pulpo a feira, octopus with paprika, olive oil and coarse salt on a wooden plate, is what you eat there. Earned it.')]),
  day('2027-01-06', 'Melide to Arzúa, 14 km', 'Arzúa',
      'The shortest day, and a Spanish public holiday.', [
    item('g4', '09:30', 'activity', 'Walk Melide to Arzúa', endTime='13:00', cost=0, currency='EUR',
         notes='14 km through eucalyptus woods. TODAY IS DÍA DE REYES, Epiphany, and it is a bigger day in Spain than Christmas: shops shut, some bars shut, and there are parades the evening before. The walking is unaffected but buy anything you need the day before. Arzúa is the cheese town, a soft cow’s cheese called tetilla.')]),
  day('2027-01-07', 'Arzúa to O Pedrouzo, 20 km', 'O Pedrouzo',
      'Last full day before Santiago.', [
    item('g5', '09:00', 'activity', 'Walk Arzúa to O Pedrouzo', endTime='14:30', cost=0, currency='EUR',
         notes='20 km, gentle. You start meeting people who are also finishing tomorrow.')]),
  day('2027-01-08', 'O Pedrouzo to Santiago, 20 km. You arrive', 'Santiago de Compostela',
      'The last day. Leave in the dark if you want to reach the cathedral by lunchtime.', [
    item('g6', '08:00', 'activity', 'Walk O Pedrouzo into Santiago', endTime='13:30', cost=0, currency='EUR',
         notes='20 km. Past the airport, over Monte do Gozo where pilgrims first see the spires, then down into the old city and under the archway into Praça do Obradoiro with the cathedral in front of you. 115 km on foot. Take your time on the last hour.'),
    item('g7', '14:30', 'activity', 'Collect your Compostela at the Pilgrim’s Office',
         location='Oficina del Peregrino, Rúa das Carretas 33', cost=0, currency='EUR',
         notes='Bring the credencial with its two stamps a day. They check it, ask why you walked, and write your name on the certificate in Latin. Free. There is a queue; in January it will be short. THE PILGRIM MASS at the cathedral is usually at noon and again at 19:30, and the botafumeiro, the giant swinging incense burner, is not swung at every mass, so ask at the office which one to go to.'),
    item('g8', '19:00', 'food', 'Dinner on Rúa do Franco', location='Rúa do Franco, behind the cathedral',
         cost=35, currency='EUR',
         notes='The street of restaurants. Octopus, pimientos de Padrón, scallops, and Estrella Galicia, which is the local beer and very good. This is the meal at the end of the walk, so have the good one.')]),
  day('2027-01-09', 'Santiago to London', 'London',
      'Fly back today. Stansted, then across London.', [
    item('h1', '11:30', 'flight', 'Ryanair, Santiago to Stansted', cost=150, currency='AUD', status='idea',
         notes='Saturday is one of the three days it flies. CONFIRM THE RETURN DAY when you book: the outbound runs Mon, Wed and Sat and the return usually matches, but check before you commit to the 9th. Stansted to central London is the Stansted Express, about 50 minutes.'),
    item('h2', '18:00', 'stay', 'Last night at your daughter\u2019s', location='See Stays',
         notes='Tomorrow is a 13:40 flight out of Heathrow, so you need to leave hers by about 09:30. A Heathrow hotel would be easier but it is A$180 and the budget has no room for easier.')]),
  day('2027-01-10', 'Fly home', 'London',
      'Thirty-six nights. Home tomorrow.', [
    item('z1', '10:00', 'transfer', 'To Heathrow', location='London Heathrow',
         notes='Be at the airport by 10:40 for a 13:40 departure. A Sunday, so check the night before for engineering works on whichever line you are using.'),
    item('z2', '13:40', 'flight', 'Heathrow to Brisbane', status='booked',
         notes='CLAIM YOUR VAT REFUND BEFORE YOU DROP THE BAG if you bought anything substantial in Spain or Ireland. The UK no longer does tax-free shopping for visitors, but the EU does, so Spanish and Irish purchases over about €100 qualify and the refund desk is landside.')]),
]

# =============================================================================
# THE PAPERWORK. Two of these stop him at the gate in Brisbane.
# =============================================================================
checklist = [
  dict(id='e1', group='Paperwork', text='Apply for the UK ETA. You cannot board without it', due='2026-10-31',
       notes='Since 25 February 2026 every Australian passport holder needs an Electronic Travel Authorisation to enter the UK. £20, on the official UK ETA app or at gov.uk, usually approved in minutes though they ask you to allow three working days. Lasts two years. THE AIRLINE CHECKS IT AT THE GATE IN BRISBANE: no ETA, no boarding, no refund. Use gov.uk and nothing else, because the copycat sites charge four times the price for the same thing.'),
  dict(id='e2', group='Paperwork', text='Check the passport: 6 months left AND issued within the last 10 years', due='2026-09-30',
       notes='Two separate rules and the second one catches people. Norway and Spain are both Schengen, which requires the passport to be valid at least 3 months after you leave AND to have been issued within the last 10 years. An Australian passport renewed early carries extra months that can push its issue date past ten years, and that passport gets refused while looking perfectly in date. Check the ISSUE date. Renewal takes about six weeks and longer near Christmas.'),
  dict(id='e3', group='Paperwork', text='Watch for ETIAS opening, then apply. Norway and Spain both need it', due='2026-11-15',
       notes='ETIAS is the European travel permit Australians will need for the Schengen countries. This trip enters Schengen twice, Norway on the 10th of December and Spain on the 2nd of January. Expected to start in the last months of 2026 with a grace period into 2027, so your dates may fall either side. About €20. THE SITE IS NOT OPEN YET AND EVERY WEBSITE CURRENTLY TAKING ETIAS APPLICATIONS IS A SCAM. Wait. Connor is checking the real date in November.'),
  dict(id='e4', group='Paperwork', text='Travel insurance: 37 days, age 63, must include the cruise', due='2026-10-31',
       notes='Cruise cover is nearly always a separate tick box and a policy without it pays for nothing that happens on the ship. Declare every medical condition honestly; an undeclared one voids the whole policy. Also worth knowing: Australia has reciprocal healthcare agreements with the UK, Ireland and Norway, so medically necessary treatment is covered there on your Medicare card. That is real but it is NOT insurance. It does not fly you home and it does not cover Spain.'),
  # ---- the bookings, in the order they should be made ----
  dict(id='e5', group='Book these', text='Gatwick to Bergen on 10 Dec, and Bergen to Gatwick on 23 Dec', due='2026-10-15',
       notes='Norwegian is the only nonstop, about 1h55. The 08:40 out of Gatwick arriving 11:35 is the one. Going on the 10th rather than the 11th is deliberate: you never fly to a cruise on the day it sails. Coming back on the 23rd rather than the evening of the 22nd is the same logic in reverse, two days before Christmas.'),
  dict(id='e6', group='Book these', text='Two nights in Bergen: 10 Dec and 22 Dec', due='2026-10-15',
       notes='Same hotel both times if you can. Bergen is expensive, about A$250 a night, and the centre is small enough that anything near Bryggen or the fish market is walkable to the Hurtigruten terminal.'),
  dict(id='e7', group='Book these', text='Guinness Storehouse tickets for 28 Dec', due='2026-11-30',
       notes='Ireland’s most visited attraction and it sells out, especially in the week between Christmas and New Year. Book a morning slot online, about €30, which includes the pint at the top.'),
  dict(id='e8', group='Book these', text='Dublin flights and two nights, 27 to 29 Dec', due='2026-11-15',
       notes='About 1h25, they go all day from every London airport. Stay near Grafton Street or the south side of the river so everything is walkable.'),
  dict(id='e9', group='Book these', text='Stansted to Santiago on Sat 2 Jan, back Sat 9 Jan', due='2026-11-15',
       notes='Ryanair is the only nonstop and IT ONLY FLIES MONDAY, WEDNESDAY AND SATURDAY, which is what fixes the Camino dates. Confirm the return runs on the Saturday before you commit. Book the Stansted airport hotel for the night of the 1st at the same time.'),
  dict(id='e10', group='Book these', text='Seven nights on the Camino: Sarria, Portomarín, Palas de Rei, Melide, Arzúa, O Pedrouzo, Santiago', due='2026-11-30',
       notes='BOOK THESE AHEAD, do not walk in. Most pilgrim albergues close from Christmas to mid-January, so this is a hotel and guesthouse walk rather than a hostel one. That costs more, about A$120 a night, and at 63 with a private room and a hot shower every night it is the better trip anyway. Somewhere with a drying room is worth paying for in Galician January.'),
  dict(id='e11', group='Book these', text='Decide the London hotel nights and book them', due='2026-11-15',
       notes='You are at your daughter’s for some of it and in a hotel for the rest. Work out which nights with her BEFORE you book anything: five weeks is a long time to have a guest and she may be relieved to be asked. Whatever is left is the biggest single cost in the trip.'),
  # ---- the walk ----
  dict(id='e12', group='The Camino', text='Break the boots in now. Not in December, now', due='2026-10-15',
       notes='Six days and 115 km. Walk 10 km in them, then 15, then 20, on hills, in the rain, with the pack you will carry. Blisters on day two of six is the one thing that can actually ruin this, and it is entirely preventable. If the boots hurt at all in Gympie they will be agony in Galicia.'),
  dict(id='e13', group='The Camino', text='Get a credencial, the pilgrim passport', due='2027-01-02',
       notes='You collect stamps in it and hand it in at Santiago to get the Compostela. Buy it in Sarria for a couple of euros at the parish church or a hostel, or order one from the Australian Friends of the Camino before you leave. ON THE LAST 100 KM THE RULE IS TWO STAMPS A DAY, not one: bars, cafes, churches and hostels all stamp. Miss the stamps and there is no certificate.'),
  dict(id='e14', group='The Camino', text='Pack for Galician rain, not Spanish sun', due='2026-12-01',
       notes='January in Galicia is 5 to 12 degrees and it is the wettest part of Spain. A proper waterproof jacket, a pack cover, two pairs of walking socks so one can dry, and a head torch because it is not light until nearly 09:00. Keep the pack under 8 kg; every kilo is 115 km of carrying it. Luggage transfer between stages costs about €8 a day and is a perfectly respectable thing to use.'),
  # ---- practical ----
  dict(id='e15', group='Before you go', text='Put an eSIM on the iPhone before you leave', due='2026-11-30',
       notes='One eSIM covering the UK and Europe is about A$25 for the month and saves both roaming charges and hunting for wi-fi. Install it at home where the internet is good and someone can help, then switch it on when you land. Keep the Australian number active for bank texts.'),
  dict(id='e16', group='Before you go', text='Two cards from two banks, in two different pockets', due='2026-11-30',
       notes='A card that stops working in Norway on a Sunday is a ruined day if it is the only one you have. Tell both banks the dates. Ask what they charge on foreign purchases, because 3% is common and over 37 days it adds up to real money; a fee-free travel card is worth getting.'),
  dict(id='e17', group='Before you go', text='Ask Hurtigruten for the port-by-port timetable and send it to Connor', due='2026-10-15',
       notes='Which port each day and what time the ship is alongside. Once that is in here you will always know what tomorrow is, which is the whole reason this is on your phone.'),
  dict(id='e18', group='Before you go', text='Ask Hurtigruten about the Northern Lights Promise', due='2026-10-15',
       notes='Hurtigruten has long run a guarantee on the 12-day round voyage in the winter months: if the aurora does not appear, you get another voyage free. Terms change, so ask them directly whether your booking has it and what counts. Worth knowing before you go rather than after.'),
]

# =============================================================================
# WHAT IT WILL COST. He asked, so here is a real number rather than a shrug.
# Flights from Brisbane and the cruise itself are already paid and not in here.
# =============================================================================
budget = [
  # Flights and ticketed activities are priced on the itinerary; beds on Stays.
  # This page is only for what has no home of its own, so nothing counts twice.
  dict(id='bg9', category='Food', label='Food and drink in the UK, about 18 days', amount=810, currency='AUD', status='estimate',
       notes='About A$45 a day over the eighteen days you are actually in the UK. It is low because you are staying at your daughter\u2019s: breakfast at home, a pub lunch most days, dinner in more often than out, and a few pints. Eat out every night and this doubles. The other days are covered elsewhere: eleven on the ship with meals included, two ashore in Bergen, eight in Spain.'),
  dict(id='bg10', category='Food', label='Food and drink in Spain, 8 days', amount=400, currency='AUD', status='estimate',
       notes='About A$50 a day, and Galicia is good value. The men\u00fa del d\u00eda is three courses, bread and a glass of wine for 12 to 15 euro at lunchtime, which is how to eat on a walking day. The named meals in Melide and Santiago are on the itinerary already.'),
  dict(id='bg11', category='Food', label='Eating ashore in Norway, 2 days', amount=250, currency='AUD', status='estimate',
       notes='Meals on the ship are included, so this is only Bergen, where a pint is about A$16 and a modest lunch A$35. Two days, so stop converting and enjoy it.'),
  dict(id='bg14', category='Transport', label='Tubes, buses, airport trains, an Oyster card', amount=350, currency='AUD', status='estimate',
       notes='Five weeks of getting about London, the Gatwick and Stansted Express runs, and the Bybanen in Bergen. The Santiago to Sarria train is on the itinerary.'),
  dict(id='bg15', category='Other', label='Travel insurance, 37 days, age 63, with cruise cover', amount=400, currency='AUD', status='estimate',
       notes='The one line not to trim. Cruise cover is nearly always a separate tick box and a policy without it pays for nothing that happens on the ship.'),
  dict(id='bg16', category='Other', label='UK ETA, ETIAS and an eSIM', amount=100, currency='AUD', status='estimate'),
  dict(id='bg18', category='Other', label='Camino luggage transfer, 6 stages', amount=80, currency='AUD', status='estimate',
       notes='About 8 euro a stage for a van to take the bag on to the next guesthouse. The cheapest comfort on the whole trip.'),
  dict(id='bg17', category='Other', label='Contingency', amount=300, currency='AUD', status='estimate',
       notes='Thin for five weeks, but it is what is left. Something always comes up.'),
]

questions = [
  dict(id='q0', question='The trip costs about A$4,325 and your budget is A$3,000 to A$4,000. Which version do you want?',
       why='This is the only question that matters and everything else follows from it. The number above already assumes the cheap version of everything: every London night at your daughter\u2019s, no hotel in Bergen on the way home, the Camino slept in a mix of bunks and cheap rooms, and about A$45 a day on food. Dublin has already been cut. What is left, in round numbers: the Camino block is A$1,300 (flights A$300, seven nights A$415, the train to Sarria, eight days of eating, the bag transfer). Everything else, the seventeen nights at your daughter\u2019s, the two days in Bergen either side of the ship, the football, insurance and getting about, is A$3,025. Drop the walk and you would eat in London those eight days instead, so it lands near A$3,385. The whole decision is whether the walk is worth about A$950 of real difference and going A$325 over.',
       options=['Keep the Camino and go to about A$4,325',
                'Drop the Camino and land at about A$3,385',
                'Keep the Camino and find the A$325 somewhere else'],
       recommendation='Keep it. You are 63, you are going to be on that side of the world once, and A$1,300 for six days walking into Santiago with the certificate at the end is the cheapest big thing on this whole trip. If the A$325 has to come from somewhere, it comes from eating out less in London, where you have a kitchen and a daughter, not from the walk.',
       answer='', resolved=False),
  dict(id='q0b', question='Is the Arsenal ticket already paid for?',
       why='It is in the budget at A$160. If you have already bought it, that is A$160 off the number above and it is not part of the A$3,000 to A$4,000 you are planning to spend.',
       options=['Already bought', 'Not yet'],
       recommendation='If it is bought, tell Connor and he will take it out of the total.', answer='', resolved=False),
  dict(id='q2', question='Add Dublin back? It costs about A$800',
       why='It was in the plan for 27 to 29 December, between Boxing Day and the football, which is the only gap on the whole trip that fits it. It came out to make the budget work. Putting it back is about A$800: A$240 in flights, A$280 for two nights, the Guinness Storehouse at about A$55, and two days of eating out instead of eating at your daughter\u2019s. The three days are still in the plan as quiet London days, so nothing has to be rearranged to put it back.',
       options=['Leave it out this trip', 'Put it back, find the A$800', 'Put it back and drop the Camino instead'],
       recommendation='Leave it out. Ireland is a short flight from London and your daughter lives there, so it is the easiest thing in the world to come back for. The Camino is not.',
       answer='', resolved=False),
  dict(id='q1', question='What time does the Hurtigruten actually sail?',
       why='Settled: 21:30 on Friday 11 December. It matters because it means the whole of that day is yours in Bergen, which is the day in Bergen you wanted, at no extra cost beyond the hotel night you were having anyway.',
       options=['21:30, confirmed'],
       recommendation='Be in the terminal by 19:45 regardless. Hurtigruten\u2019s published Bergen time is 20:30 and yours says 21:30, so leave no room for that difference to matter.',
       answer='21:30. Bryggen, the fish market and the funicular all fit into the 11th before boarding.', resolved=True),
  dict(id='q3', question='Luggage transfer on the Camino, yes or no?',
       why='About 8 euro a stage for a van to take your bag to the next guesthouse while you walk with a daypack. It is A$80 for the week and it is already in the budget.',
       options=['Use it every day, walk light', 'Carry everything, that is the point', 'Book it and decide each morning'],
       recommendation='Use it. Nobody at the Pilgrim\u2019s Office asks and the Compostela is identical. Six days at 63 in Galician rain carrying 8 kg is a different walk to carrying 3 kg, and A$80 is the cheapest comfort on this trip.',
       answer='', resolved=False),
  dict(id='q4', question='Which nights at your daughter\u2019s, and have you actually asked her?',
       why='Seventeen nights, in three blocks: five in early December, eleven over Christmas and New Year, and one at the end. At London hotel rates that is about A$3,700, and it is the single biggest reason any of this fits. Every night that turns into a hotel puts about A$220 back on the total, so six nights in a hotel is the whole Camino.',
       options=['All seventeen, she has offered', 'Most of them, a few nights elsewhere', 'Need to ask her'],
       recommendation='Ask her outright and take the answer at face value. Five weeks is a long time to have a guest, even your own father, and it is much better to know in October than in December.',
       answer='', resolved=False),
]

stays = [
  # Seventeen nights at his daughter's, in three blocks, with real dates so the
  # count is checkable rather than asserted. It was written as one row of 27,
  # which was ten nights of wishful arithmetic.
  dict(id='sy1a', name='Your daughter\u2019s, 5 to 10 Dec', town='London', status='booked',
       pricePerNightAud=0, nights=5, checkIn='2026-12-05', checkOut='2026-12-10', type='Family',
       notes='The first five nights, before you fly to Bergen.'),
  dict(id='sy1b', name='Your daughter\u2019s, 22 Dec to 2 Jan', town='London', status='booked',
       pricePerNightAud=0, nights=11, checkIn='2026-12-22', checkOut='2027-01-02', type='Family',
       notes='The long block: home off the ship on the 22nd, Christmas, the football on the 30th, New Year, then away to Spain on the 2nd. Eleven nights, and the reason this trip fits a budget at all.'),
  dict(id='sy1c', name='Your daughter\u2019s, 9 to 10 Jan', town='London', status='booked',
       pricePerNightAud=0, nights=1, checkIn='2027-01-09', checkOut='2027-01-10', type='Family',
       notes='Back from Santiago, one night, then home. SEVENTEEN NIGHTS AT HERS IN TOTAL. At London hotel rates that is about A$3,700, which is most of the difference between this trip happening and not. Ask her about all three blocks at once rather than in instalments.'),
  dict(id='sy0', name='Hurtigruten, Bergen to Kirkenes and back', town='Hurtigruten', status='booked',
       pricePerNightAud=0, nights=11, checkIn='2026-12-11', checkOut='2026-12-22',
       type='Cabin on the coastal express',
       notes='Eleven nights, already paid, so it costs nothing more. Here so the Stays page can always answer where you are sleeping tonight, which on the 16th of December in the Arctic is a fair question. Meals are included; the only money on these days is ashore.'),
  dict(id='sy3', name='Bergen, night of 10 Dec', town='Bergen', status='planned', pricePerNightAud=220, nights=1,
       checkIn='2026-12-10', checkOut='2026-12-11', distance='Walkable to Bryggen and the Hurtigruten terminal',
       type='Hotel or guesthouse',
       notes='The only hotel night before the ship, and it is not negotiable: you do not fly to a cruise on the day it sails. Bergen is expensive but the centre is small, so anything near Bryggen or the fish market walks to everything including the terminal. Look at guesthouses and the Bergen YMCA as well as hotels.'),
  dict(id='sy6', name='Sarria, night of 2 Jan', town='Sarria', status='planned', pricePerNightAud=55, nights=1,
       checkIn='2027-01-02', checkOut='2027-01-03', type='Pensi\u00f3n or albergue'),
  dict(id='sy7', name='Portomar\u00edn, night of 3 Jan', town='Portomar\u00edn', status='planned', pricePerNightAud=55, nights=1,
       checkIn='2027-01-03', checkOut='2027-01-04', type='Pensi\u00f3n or albergue'),
  dict(id='sy8', name='Palas de Rei, night of 4 Jan', town='Palas de Rei', status='planned', pricePerNightAud=55, nights=1,
       checkIn='2027-01-04', checkOut='2027-01-05', type='Pensi\u00f3n or albergue'),
  dict(id='sy9', name='Melide, night of 5 Jan', town='Melide', status='planned', pricePerNightAud=55, nights=1,
       checkIn='2027-01-05', checkOut='2027-01-06', type='Pensi\u00f3n or albergue'),
  dict(id='sy10', name='Arz\u00faa, night of 6 Jan', town='Arz\u00faa', status='planned', pricePerNightAud=55, nights=1,
       checkIn='2027-01-06', checkOut='2027-01-07', type='Pensi\u00f3n or albergue'),
  dict(id='sy11', name='O Pedrouzo, night of 7 Jan', town='O Pedrouzo', status='planned', pricePerNightAud=55, nights=1,
       checkIn='2027-01-07', checkOut='2027-01-08', type='Pensi\u00f3n or albergue',
       notes='THE SIX CAMINO NIGHTS AT ABOUT A$55 EACH. In January the Xunta de Galicia public albergues are about 10 euro for a bunk and many stay open, while a pensi\u00f3n with your own room and a hot shower is 35 to 45 euro. A$55 a night assumes a mix. At 63, walking six days in the rain, take the private room on the nights you feel it and the bunk on the nights you do not. A drying room is worth paying for.'),
  dict(id='sy12', name='Santiago de Compostela, night of 8 Jan', town='Santiago de Compostela', status='planned',
       pricePerNightAud=85, nights=1, checkIn='2027-01-08', checkOut='2027-01-09', type='Hotel or pensi\u00f3n',
       notes='The night you arrive. Spend a bit more and stay in the old town within sight of the cathedral. You will have walked 115 km to get there.'),
  dict(id='sy5', name='Dublin, 2 nights (CUT, see Decisions)', town='Dublin', status='idea', pricePerNightAud=140, nights=2,
       type='Hotel', notes='Not in the budget. Adding Dublin back costs about A$800 all in: A$280 for two nights, A$240 in flights, the Storehouse and a couple of days of eating out. Kept here so the number is visible if the money appears.'),
]

food = [
  dict(id='f1', town='Dublin', dish='Guinness at the Storehouse, then the real one in a pub',
       where='Storehouse at St James’s Gate; then the Long Hall, Kehoe’s or the Palace Bar',
       why='The Storehouse is the tour and the rooftop view, with a pint in the ticket. The actual best pint in Dublin is in a Victorian pub with no television, poured in two goes and left to settle. Do both, in that order.', priceBand='€€'),
  dict(id='f2', town='Dublin', dish='Seafood chowder and brown bread, or a proper Irish stew',
       where='Anywhere two streets away from Temple Bar', why='Temple Bar charges double for worse. Walk out of it.', priceBand='€€'),
  dict(id='f3', town='London', dish='A pub Sunday roast', where='Any pub with a blackboard and no television',
       why='Beef, Yorkshire pudding, gravy. Book it; the good ones fill by Thursday.', priceBand='££'),
  dict(id='f4', town='Bergen', dish='Fish soup at the Torget market', where='Torget fish market, indoor hall, open year round',
       why='The thing to eat in Bergen, and it is hot, which matters in December.', priceBand='kr kr'),
  dict(id='f5', town='Melide', dish='Pulpo a feira at Pulpería Ezéquiel', where='Melide, on the Camino, day four',
       why='Octopus with paprika, olive oil and coarse salt on a wooden plate. Melide is where pilgrims stop for it and Ezéquiel is the one they stop at. You will have walked 15 km to get there.', priceBand='€€'),
  dict(id='f6', town='Arzúa', dish='Tetilla cheese', where='Any shop in Arzúa', why='The soft cow’s cheese the town is known for. Buy a piece for the next day’s walk.', priceBand='€'),
  dict(id='f7', town='Santiago de Compostela', dish='Scallops, Padrón peppers, and Estrella Galicia',
       where='Rúa do Franco, the restaurant street behind the cathedral',
       why='The meal at the end of the walk. The scallop shell is the symbol of the Camino, so eating one here is the joke everybody makes and it is still good. Estrella Galicia is the local beer and better than its reputation.', priceBand='€€'),
  dict(id='f8', town='Anywhere in Spain', dish='Menú del día', where='Any bar with a board outside at lunchtime',
       why='Three courses, bread and a glass of wine for about €12 to €15, served between about 13:30 and 15:30. It is how Spain eats lunch and it is the best value on this trip by a mile.', priceBand='€'),
]

places = [
  dict(id='py1', name='London Heathrow', kind='airport', town='London', lat=51.4700, lng=-0.4543),
  dict(id='py2', name='London Gatwick', kind='airport', town='London', lat=51.1537, lng=-0.1821, notes='For Bergen.'),
  dict(id='py3', name='London Stansted', kind='airport', town='London', lat=51.8860, lng=0.2389, notes='For Santiago.'),
  dict(id='py4', name='Imperial War Museum', kind='other', town='London', lat=51.4959, lng=-0.1086),
  dict(id='py5', name='Churchill War Rooms', kind='other', town='London', lat=51.5020, lng=-0.1292),
  dict(id='py6', name='Emirates Stadium', kind='other', town='London', lat=51.5549, lng=-0.1084, notes='Arsenal. Holloway Road, Arsenal or Finsbury Park tube.'),
  dict(id='py7', name='Bryggen, Bergen', kind='other', town='Bergen', lat=60.3975, lng=5.3243),
  dict(id='py8', name='Hurtigruten terminal, Bergen', kind='station', town='Bergen', lat=60.3891, lng=5.3116, notes='Nøstegaten 30. In the terminal 30 min before sailing.'),
  dict(id='py9', name='Fløibanen funicular', kind='other', town='Bergen', lat=60.3963, lng=5.3300),
  dict(id='py10', name='Guinness Storehouse', kind='other', town='Dublin', lat=53.3419, lng=-6.2867),
  dict(id='py11', name='Sarria', kind='town', town='Sarria', lat=42.7810, lng=-7.4140, notes='Where the last 100 km starts.'),
  dict(id='py12', name='Portomarín', kind='town', town='Portomarín', lat=42.8072, lng=-7.6161),
  dict(id='py13', name='Palas de Rei', kind='town', town='Palas de Rei', lat=42.8730, lng=-7.8690),
  dict(id='py14', name='Melide', kind='town', town='Melide', lat=42.9140, lng=-8.0150),
  dict(id='py15', name='Arzúa', kind='town', town='Arzúa', lat=42.9290, lng=-8.1610),
  dict(id='py16', name='O Pedrouzo', kind='town', town='O Pedrouzo', lat=42.9070, lng=-8.3660),
  dict(id='py17', name='Santiago de Compostela Cathedral', kind='other', town='Santiago de Compostela', lat=42.8806, lng=-8.5446),
  dict(id='py18', name='Pilgrim’s Office, Santiago', kind='other', town='Santiago de Compostela', lat=42.8797, lng=-8.5468, notes='Rúa das Carretas 33. Bring the credencial.'),
]

PLACE_OF = {
  'a1': 'py1', 'a3': 'py4', 'a4': 'py5', 'b1': 'py2', 'b4': 'py7', 'b5': 'py7', 'b6': 'py9',
  'b7': 'py8', 'b8': 'py8', 'c1': 'py8', 'd3': 'py10', 'e1': 'py6', 'f1': 'py3', 'f3': 'py11',
  'g1': 'py12', 'g2': 'py13', 'g3': 'py14', 'g4': 'py15', 'g5': 'py16', 'g6': 'py17', 'g7': 'py18',
  'g8': 'py17', 'z1': 'py1', 'z2': 'py1',
}
for d in days:
    for it in d['items']:
        if it['id'] in PLACE_OF:
            it['placeId'] = PLACE_OF[it['id']]

# ---- guards -----------------------------------------------------------------
_dates = [d['date'] for d in days]
assert _dates == sorted(_dates), 'days out of order'
assert _dates[0] == START and _dates[-1] == END, 'days do not span the trip'
assert len(_dates) == len(set(_dates)) == 37, 'expected 37 unique days, got %d' % len(_dates)
_ids = [i['id'] for d in days for i in d['items']]
assert len(_ids) == len(set(_ids)), 'duplicate item id'
for _d in days:                      # times must run forwards within a day
    _t = [i['time'] for i in _d['items']]
    assert _t == sorted(_t), 'times out of order on %s' % _d['date']
# Ryanair only flies Stansted to Santiago on Mon, Wed and Sat, which is what
# fixes the Camino dates. If either end moves to another weekday, the flight
# does not exist.
for _iso in ('2027-01-02', '2027-01-09'):
    assert datetime.date.fromisoformat(_iso).weekday() in (0, 2, 5), \
        '%s is not a Ryanair Stansted-Santiago day' % _iso

# Every night of the trip has to be slept somewhere, and exactly once. This is
# what catches a stay whose night count was asserted rather than counted: the
# first version of this file claimed 27 nights at his daughter's when the real
# answer is 17, and nothing noticed.
_trip_nights = (datetime.date.fromisoformat(END) - datetime.date.fromisoformat(START)).days
_slept = {}
for _s in stays:
    if _s.get('status') not in ('planned', 'booked') or not _s.get('checkIn'):
        continue
    _n = int(_s.get('nights') or 0)
    _span = (datetime.date.fromisoformat(_s['checkOut']) - datetime.date.fromisoformat(_s['checkIn'])).days
    assert _n == _span, '%s says %d nights but %s to %s is %d' % (_s['id'], _n, _s['checkIn'], _s['checkOut'], _span)
    for _k in range(_n):
        _d = (datetime.date.fromisoformat(_s['checkIn']) + datetime.timedelta(days=_k)).isoformat()
        assert _d not in _slept, 'two beds on the night of %s: %s and %s' % (_d, _slept[_d], _s['id'])
        _slept[_d] = _s['id']
assert len(_slept) == _trip_nights, 'the trip is %d nights but the stays cover %d' % (_trip_nights, len(_slept))
_first = datetime.date.fromisoformat(START)
for _k in range(_trip_nights):
    _d = (_first + datetime.timedelta(days=_k)).isoformat()
    assert _d in _slept, 'nowhere to sleep on the night of %s' % _d

# Money must come from exactly one place per category or the total is wrong.
# Flights and ticketed activities are priced on the itinerary, beds on Stays.
# This catches a budget line that quietly duplicates either, which it did once.
_TYPE_CAT = {'flight': 'Flights', 'train': 'Transport', 'bus': 'Transport', 'transfer': 'Transport',
             'boat': 'Transport', 'stay': 'Accommodation', 'food': 'Food', 'activity': 'Activities', 'note': 'Other'}
_priced = {i.get('category') or _TYPE_CAT.get(i['type'], 'Other')
           for d in days for i in d['items'] if i.get('cost')}
if any(x.get('status') in ('planned', 'booked') and x.get('pricePerNightAud') for x in stays):
    _priced.add('Accommodation')
# Food, Transport and Other carry deliberate catch-all lines for the gaps
# between named items. Every other category must be priced in one place only.
_clash = (_priced & {b.get('category') for b in budget}) - {'Food', 'Transport', 'Other'}
assert not _clash, 'priced twice, on the plan and on the budget page: %s' % sorted(_clash)

trip = dict(
  meta=dict(
    title='Dad’s Trip 2026/27', start=START, end=END, homeCurrency='AUD',
    rates=RATES, updatedAt=UPDATED, version=1,
    mapRegion='', travelMode='transit',
    features=dict(flights=True, budget=True, points=False),
    categories=['Flights', 'Accommodation', 'Transport', 'Food', 'Activities', 'Other'],
    about='Thirty-six nights: London with your daughter, eleven on the Hurtigruten chasing the northern lights, Christmas in London, Arsenal on the 30th, and the last 115 km of the Camino into Santiago. Costed at about A$4,325 on top of the flights and the cruise you have already paid, which is still a little over your budget, so the first thing on Decisions is what to do about that. Open Go to see only what is happening now.',
  ),
  days=days,
  flights=dict(confirmed=[], legs=[], lounges=[]),
  people=[], foodGuide=[], staysGuide=[], souvenirGuide=[],
  points={}, stays=stays, food=food, souvenirs=[], budget=budget, checklist=checklist,
  places=places, questions=questions,
)

trip = carry_over(trip, 'data/europe.json')

with open('data/europe.json', 'w') as f:
    json.dump(trip, f, indent=2, ensure_ascii=False)
    f.write('\n')

print('wrote data/europe.json %d days, %d items, %d stays, %d food, %d todos, %d budget lines, %d questions' % (
    len(trip['days']), sum(len(d['items']) for d in trip['days']), len(trip['stays']),
    len(trip['food']), len(trip['checklist']), len(trip['budget']), len(trip['questions'])))
