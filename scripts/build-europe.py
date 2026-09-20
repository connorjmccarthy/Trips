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
  day('2026-12-12', 'Alesund, and the last of the daylight', 'Hurtigruten',
      'Day two. The ship calls at Floro and Maloy before dawn, then sits in Alesund most of the day, which is the longest call of the whole voyage and the one to get off for. Molde and Kristiansund after dark.', [
    item('h12a', '09:45', 'boat', 'Alesund, the long winter call', location='Alesund, Norway', endTime='20:00',
         cost=0, currency='NOK',
         notes='Ten hours alongside, which is more than anywhere else on the voyage. Alesund burned down in 1904 and was rebuilt entirely in art nouveau, so it looks like nowhere else in Norway. The walk up the 418 steps of Aksla for the view over the islands is the thing to do, and you are still far enough south that there is real daylight to do it in. Everything is a short walk from the quay.')]),
  day('2026-12-13', 'Trondheim', 'Hurtigruten',
      'Day three. A long morning in Trondheim, then north all afternoon. About six hours of light today and it is the last you will see properly for a fortnight.', [
    item('h13a', '08:30', 'boat', 'Trondheim: Nidaros Cathedral', location='Trondheim, Norway', endTime='12:00',
         cost=0, currency='NOK',
         notes='Three and a half hours, enough for the one thing worth doing. Nidaros is the northernmost medieval cathedral in the world, built over the grave of St Olav, and it was a pilgrimage destination for five hundred years, which given where you are walking in January is a nice piece of symmetry. About 20 minutes on foot from the quay. The Bakklandet quarter of old wooden houses is on the way back.')]),
  day('2026-12-14', 'Across the Arctic Circle', 'Hurtigruten',
      'Day four, and the day the trip changes. You cross the Arctic Circle in the morning; the ship makes a thing of it. From tonight the sun does not rise again until you are back south of it on the 20th.', [
    item('h14a', '07:30', 'boat', 'Crossing the Arctic Circle', location='66 degrees 33 minutes north',
         notes='There is a marker on a small island and usually a ceremony on deck involving a ladle of ice water down the neck. Take it in good humour; it is over in a minute and you get a certificate.'),
    item('h14b', '12:30', 'boat', 'Bodo', location='Bodo, Norway', endTime='15:00',
         notes='Two and a half hours in the afternoon twilight. Then the ship turns into the Lofoten islands and calls at Stamsund and Svolvaer in the dark, which is the stretch you will see properly on the way back south.')]),
  day('2026-12-15', 'Tromso, and the first real chance of lights', 'Hurtigruten',
      'Day five. THE FIRST DAY OF PROPER POLAR NIGHT: no sunrise at all, just four or five hours of blue twilight around the middle of the day. Tromso in the afternoon is the highlight of the northbound leg.', [
    item('h15a', '14:15', 'boat', 'Tromso, four hours ashore', location='Tromso, Norway', endTime='18:30',
         cost=0, currency='NOK',
         notes='THE BEST STOP ON THE WAY NORTH and a proper little city, 350 km inside the Arctic Circle. The Arctic Cathedral with its white glass front is ten minutes over the bridge; there is often an evening concert. Otherwise the Polaria aquarium, or just a beer in one of the pubs on Storgata, which is a very good thing to do in the dark at three in the afternoon. THIS IS ALSO THE BEST AURORA LATITUDE ON THE WHOLE VOYAGE, so if the sky is clear tonight, do not go to bed early.'),
    item('h15b', '21:00', 'activity', 'Up on deck if the sky is clear', status='idea',
         notes='The ship dims the outside lights when the aurora shows and usually wakes people over the tannoy. Dress as if you are standing still outside in the Arctic, because you are: thermals, hat, gloves, and more than you think. A phone on night mode will photograph it better than your eyes see it.')]),
  day('2026-12-16', 'The top of Europe: Hammerfest and the North Cape', 'Hurtigruten',
      'Day six, and the furthest north you will ever be unless you go out of your way. Hammerfest before breakfast, then the long call at Honningsvag, which is the jumping-off point for the North Cape itself.', [
    item('h16a', '11:00', 'boat', 'Honningsvag, for the North Cape', location='Honningsvag, Norway', endTime='14:30',
         cost=1100, currency='NOK', status='idea',
         notes='The one excursion on this voyage most people say they would pay for again: a coach out to Nordkapp, the cliff at the top of Europe, and the globe monument on the edge of it. In December it is dark, usually blowing, and genuinely wild, which is rather better than the summer coach-park version. Roughly 1,100 kroner and it goes through the ship. BOOK IT ON BOARD ON DAY ONE, because it is the excursion that sells out. If you skip it, Honningsvag itself is a small fishing town and three hours is plenty.')]),
  day('2026-12-17', 'Kirkenes, and the ship turns round', 'Hurtigruten',
      'Day seven. The far end: Kirkenes is 400 km east of Helsinki and fifteen minutes from the Russian border. In at nine, out at half twelve, and from there everything is the way home.', [
    item('h17a', '09:00', 'boat', 'Kirkenes: the turning point', location='Kirkenes, Norway', endTime='12:30',
         notes='Three and a half hours. The excursions here are the memorable ones: a snowmobile or husky run, or the King Crab safari where they pull a crab the size of a dustbin lid out of a hole in the ice and then cook it for you. Both book through the ship. If you would rather not, the town is small and the Andersgrotta wartime bomb shelter is ten minutes away; Kirkenes was bombed more than 300 times in the war and is one of the most bombed places in Europe, which is a piece of history almost nobody knows.'),
    item('h17b', '12:30', 'boat', 'Southbound from here',
         notes='Everything you passed in the dark on the way up, you now see in the twilight on the way down. That is the whole design of the round voyage and it is why it is worth doing both ways.')]),
  day('2026-12-18', 'Back along Finnmark', 'Hurtigruten',
      'Day eight. Honningsvag before six, Hammerfest late morning, then the long run to Tromso which you reach near midnight. A quiet day: read, eat, watch the coast go past in the blue.', [
    item('h18a', '11:00', 'boat', 'Hammerfest', location='Hammerfest, Norway', endTime='12:45',
         notes='Claims to be the northernmost town in the world, which is disputed but nobody local will thank you for saying so. Just under two hours, enough to walk up to the Meridian Column or join the Royal and Ancient Polar Bear Society, which is a genuine thing and costs about 250 kroner for a lifetime membership and a certificate.')]),
  day('2026-12-19', 'Lofoten in daylight', 'Hurtigruten',
      'Day nine, and the best scenery of the voyage. The Lofoten wall of peaks that you passed in the dark on the 14th, you now sail along in the middle of the day. If there is one day to be on deck with a hot drink rather than in the lounge, it is this one.', [
    item('h19a', '12:00', 'boat', 'Along the Lofoten wall', location='Lofoten Islands, Norway',
         notes='A line of sharp black peaks rising straight out of the sea with fishing villages tucked underneath, and in December the low blue light on the snow does something to it that summer photographs never show. Svolvaer and Stamsund are the calls. Wrap up and go outside; this is the one people remember.')]),
  day('2026-12-20', 'Back over the Circle', 'Hurtigruten',
      'Day ten. Bodo in the morning, then south across the Arctic Circle again around the middle of the day, and the sun comes back. Not much of it, but it rises, which after six days it is oddly moving.', [
    item('h20a', '10:00', 'boat', 'Bodo, and the Circle southbound', location='Bodo, Norway',
         notes='After Bodo the ship recrosses 66 degrees 33 minutes and you are out of the polar night. Sandnessjoen and Bronnoysund in the afternoon, with the Seven Sisters mountains on the port side if the cloud lifts.')]),
  day('2026-12-21', 'Trondheim again, southbound', 'Hurtigruten',
      'Day eleven, and the last full day aboard. Trondheim in the afternoon this time. PACK TONIGHT, not in the morning.', [
    item('h21a', '13:00', 'boat', 'Trondheim, afternoon call', location='Trondheim, Norway',
         notes='A couple of hours. If you did the cathedral on the way up, the Bakklandet lanes and a coffee are the better use of it now.'),
    item('h21b', '20:00', 'note', 'Settle the bar bill and pack',
         notes='Ask reception tonight what time you can get off tomorrow and whether they will hold your bag. Docking is 14:45 and your hotel will not have a room ready before then anyway.')]),
  day('2026-12-22', 'Back in Bergen', 'Bergen',
      'Off the ship at 14:45 and STAYING IN BERGEN TONIGHT. You could chase an evening flight to London but it is two days before Christmas, the airports are at their worst, and if it goes wrong you are stranded on the 23rd. One calm night is worth the hotel.', [
    item('c1', '14:45', 'boat', 'Hurtigruten docks in Bergen', location='Hurtigruten terminal, Nostegaten 30, Bergen', status='booked',
         notes='Eleven nights done.'),
    item('c2', '15:30', 'stay', 'One night in Bergen', location='See Stays',
         notes='Same hotel as the 10th if they have it, and you will know the way. Eleven nights on a ship and then straight onto a plane two days before Christmas was never a good idea: this way you sleep, and if a flight goes wrong tomorrow you have a day of slack instead of none.'),
    item('c2b', '18:00', 'food', 'Last dinner in Norway', location='Bergen centre',
         cost=450, currency='NOK', status='idea',
         notes='The one proper Norwegian meal of the trip. You have eaten on the ship for eleven nights and you are about to be in England for three weeks.')]),
  day('2026-12-23', 'Bergen to London', 'London',
      'Unhurried. Christmas Eve is tomorrow and you will be at hers by the evening.', [
    item('c3', '12:00', 'flight', 'Norwegian, Bergen to Gatwick', location='Bergen Flesland to London Gatwick',
         cost=150, currency='AUD', status='idea',
         notes='A middle-of-the-day flight, not the last one out. Book it with the outbound. Allow 45 minutes on the Bybanen from the centre to Flesland and get to the airport early: the 23rd of December is one of the busiest flying days of the year.')]),
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
    item('g1', '09:00', 'activity', 'Walk Sarria to Portomarín', location='Sarria to Portomarin, Camino Frances', endTime='15:30', cost=0, currency='EUR',
         notes='22 km, five to six hours at a steady pace with stops. The 100 km marker is just outside Sarria and everybody photographs it. TWO STAMPS A DAY from here on, from bars, churches or hostels, because the last 100 km has the stricter rule. Portomarín is reached over a long bridge and up a staircase, which is a cruel finish, and the village was moved stone by stone when they dammed the river.')]),
  day('2027-01-04', 'Portomarín to Palas de Rei, 25 km', 'Palas de Rei',
      'The longest day of the six. Start early.', [
    item('g2', '08:45', 'activity', 'Walk Portomarín to Palas de Rei', location='Portomarin to Palas de Rei, Camino Frances', endTime='15:30', cost=0, currency='EUR',
         notes='25 km with a long steady climb out of Portomarín in the first two hours. Get it done in the morning. There are bars at Gonzar and Ventas de Narón for coffee and a stamp.')]),
  day('2027-01-05', 'Palas de Rei to Arz\u00faa, 29 km', 'Arz\u00faa',
      'THE LONG DAY, and the price of two nights in Santiago instead of one. Twenty-nine kilometres is a lot in January, so leave in the dark and take the whole day over it.', [
    item('g3', '08:15', 'activity', 'Walk Palas de Rei to Arz\u00faa', location='Palas de Rei to Arzua via Melide, Camino Frances', endTime='16:00', cost=0, currency='EUR',
         notes='29 km, seven to eight hours with proper stops, which is why the bag goes in the van today whatever you decide about the other days. Light is about 08:45 to 18:15, so a head torch for the first half hour and you still have an hour spare at the end. This is the standard stage that five-day walkers do; it is long, not hard, and the ground is gentle.'),
    item('g3b', '12:00', 'food', 'Octopus in Melide, halfway', location='Pulper\u00eda Ez\u00e9quiel, Melide',
         endTime='13:00', cost=15, currency='EUR',
         notes='Melide is almost exactly the midpoint and it is the octopus town. Pulpo a feira, octopus with paprika, olive oil and coarse salt on a wooden plate, with the rough house wine in a white bowl. You would have slept here on the six-day version; now you eat here instead, which is the better half of the deal. Do not rush it, you have the daylight.')]),
  day('2027-01-06', 'Arz\u00faa to O Pedrouzo, 20 km', 'O Pedrouzo',
      'Back to a normal day, and a Spanish public holiday.', [
    item('g5', '09:00', 'activity', 'Walk Arz\u00faa to O Pedrouzo', location='Arzua to O Pedrouzo, Camino Frances', endTime='14:30', cost=0, currency='EUR',
         notes='20 km through eucalyptus woods, gentle after yesterday. TODAY IS D\u00cdA DE REYES, Epiphany, which is a bigger day in Spain than Christmas: shops shut, some bars shut, parades the evening before. The walking is unaffected but buy what you need on the 5th. Arz\u00faa is the cheese town, a soft cow\u2019s cheese called tetilla, so take some with you.')]),
  day('2027-01-07', 'O Pedrouzo to Santiago, 20 km. You arrive', 'Santiago de Compostela',
      'The last day. Leave in the dark and you are at the cathedral by lunchtime.', [
    item('g6', '08:00', 'activity', 'Walk O Pedrouzo into Santiago', location='O Pedrouzo to Santiago de Compostela, Camino Frances', endTime='13:30', cost=0, currency='EUR',
         notes='20 km. Past the airport, over Monte do Gozo where pilgrims first see the spires, then down into the old city and under the archway into Pra\u00e7a do Obradoiro with the cathedral in front of you. 116 km on foot. Take your time on the last hour; there is no train to catch and you have two nights here.'),
    item('g7', '14:30', 'activity', 'Collect your Compostela at the Pilgrim\u2019s Office',
         location='Oficina del Peregrino, R\u00faa das Carretas 33', cost=0, currency='EUR',
         notes='Bring the credencial with its two stamps a day. They check it, ask why you walked, and write your name on the certificate in Latin. Free, and in January the queue is short. Ask them which Pilgrim\u2019s Mass the botafumeiro is swung at, the giant incense burner on ropes; it is not every mass and it is the thing to see. Masses are usually noon and 19:30.'),
    item('g8', '19:30', 'food', 'Dinner on R\u00faa do Franco', location='R\u00faa do Franco, behind the cathedral',
         cost=35, currency='EUR',
         notes='The street of restaurants. Scallops, pimientos de Padr\u00f3n, and Estrella Galicia, which is the local beer and very good. The meal at the end of the walk, so have the good one.')]),
  day('2027-01-08', 'A day in Santiago, with nothing to walk', 'Santiago de Compostela',
      'THE DAY YOU ASKED FOR. Six days of getting up in the dark and now a morning with nowhere to be. Either see Santiago properly or go to the end of the world; both are good and you cannot do both well.', [
    item('g9', '09:00', 'activity', 'Option one: Santiago properly', location='The old town', status='idea',
         notes='The cathedral itself, which you only glanced at yesterday, plus the museum and the rooftop tour over the old city, which is the one worth booking. The Pilgrim\u2019s Mass at noon with the botafumeiro if it is swinging today. Then the Mercado de Abastos, the produce market, which is the second most visited thing in the city and where you buy lunch and have it cooked for you at a stall. An old stone city that is a pleasure to be lost in, and everything is within fifteen minutes on foot. About 15 euro for the rooftop tour and the museum; the budget carries the Finisterre option below instead, because it is the dearer of the two and you can only spend the day once.'),
    item('g10', '09:00', 'activity', 'Option two: the bus to Finisterre, the end of the world',
         location='Santiago bus station, Monbus to Fisterra', status='idea', cost=30, currency='EUR',
         notes='Cape Finisterre is where the Romans thought the land stopped, and it is where many pilgrims carry on to after Santiago. The lighthouse, the 0 km marker, the Atlantic and nothing beyond it. Monbus runs it: the direct service is about 1h15 each way, the scenic coastal one nearly 3 hours, so take the direct one at least in one direction or you spend the day on a bus. CHECK THE WINTER TIMETABLE AT MONBUS.ES, because January services are thinner than summer. About 30 euro return. In January the cape is wild and often empty, which is rather the point.'),
    item('g11', '19:00', 'food', 'Last dinner in Spain', location='R\u00faa do Franco or the market quarter',
         cost=30, currency='EUR',
         notes='Tomorrow you fly. Galician white wine is albari\u00f1o and it is excellent, so have that rather than the beer tonight.')]),
  day('2027-01-09', 'Santiago to London', 'London',
      'Fly back today. Stansted, then across London.', [
    item('h1', '11:30', 'flight', 'Ryanair, Santiago to Stansted', location='Santiago de Compostela airport to London Stansted', cost=150, currency='AUD', status='idea',
         notes='Saturday is one of the three days it flies. CONFIRM THE RETURN DAY when you book: the outbound runs Mon, Wed and Sat and the return usually matches, but check before you commit to the 9th. Stansted to central London is the Stansted Express, about 50 minutes.'),
    item('h2', '18:00', 'stay', 'Last night at your daughter\u2019s', location='See Stays',
         notes='Tomorrow is a 13:40 flight out of Heathrow, so you need to leave hers by about 09:30. A Heathrow hotel would be easier but it is A$180 and the budget has no room for easier.')]),
  day('2027-01-10', 'Fly home', 'London',
      'Thirty-six nights. Home tomorrow.', [
    item('z1', '10:00', 'transfer', 'To Heathrow', location='London Heathrow',
         notes='Be at the airport by 10:40 for a 13:40 departure. A Sunday, so check the night before for engineering works on whichever line you are using.'),
    item('z2', '13:40', 'flight', 'Heathrow to Brisbane', location='London Heathrow', status='booked',
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
  dict(id='e10', group='Book these', text='Seven nights on the Camino, and book Santiago first', due='2026-11-30',
       notes='All seven are named on the Stays page with what they cost: Mar de Plata in Sarria, Portomino in Portomarin, Plaza in Palas de Rei, Casa Frade in Arzua, Arca in O Pedrouzo, and two nights at San Martin Pinario in Santiago. BOOK SAN MARTIN PINARIO FIRST, then Casa Frade, which has only six rooms. RING OR EMAIL EACH ONE rather than booking blind: plenty of Camino lodging shuts between Christmas and mid-January, and a booking site showing availability is not the same as a door that opens. Ask two questions every time: are you open on that date, and do you have a drying room. The second matters more than it sounds in Galician January.'),
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
  dict(id='bg9', category='Food', label='Food and drink in the UK, about 17 days', amount=765, currency='AUD', status='estimate',
       notes='About A$45 a day over the eighteen days you are actually in the UK. It is low because you are staying at your daughter\u2019s: breakfast at home, a pub lunch most days, dinner in more often than out, and a few pints. Eat out every night and this doubles. The other days are covered elsewhere: eleven on the ship with meals included, three ashore in Bergen, eight in Spain.'),
  dict(id='bg10', category='Food', label='Food and drink in Spain, 8 days', amount=300, currency='AUD', status='estimate',
       notes='About A$50 a day, and Galicia is good value. The men\u00fa del d\u00eda is three courses, bread and a glass of wine for 12 to 15 euro at lunchtime, which is how to eat on a walking day. The four named meals, the octopus in Melide and the three in Santiago, are priced on the itinerary already, so this is everything around them: breakfasts, the bar stops for your two stamps a day, and the coffee you will want at 9am in the rain.'),
  dict(id='bg11', category='Food', label='Eating ashore in Norway, 3 days', amount=220, currency='AUD', status='estimate',
       notes='Meals on the ship are included, so this is only Bergen: the 10th and 11th on the way out and the 22nd on the way back. A pint is about A$16 and a modest lunch A$35. The fish market on the 11th and the last dinner on the 22nd are priced on the itinerary, so this is everything around them. Three days out of thirty-six, so stop converting and enjoy it.'),
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
  dict(id='q0', question='The trip costs about A$4,950, but only A$4,000 of that is money you have to spend. Which version do you want?',
       why='This is the only question that matters and everything else follows from it. The number above already assumes the cheap version of everything: every London night at your daughter\u2019s, no hotel in Bergen on the way home, the Camino slept in a mix of bunks and cheap rooms, and about A$45 a day on food. Dublin has already been cut. What is left, in round numbers: A$950 of the total is marked Optional on the Budget page and you can simply not do it: the North Cape coach at A$165, Bletchley Park, the Finisterre bus, a few meals. Ignore all of it and the trip is A$4,000, which is your ceiling to the dollar. The rest of this answer is about the part you cannot ignore. The Camino and Santiago block is A$1,610 (flights A$300, seven nights A$630 in real named places rather than a guess, the train to Sarria, eight days of eating, the bag transfer, the free day at the end). Everything else, the sixteen nights at your daughter\u2019s, the three days in Bergen either side of the ship, the football, insurance and getting about, is A$3,180. Drop the walk and you would eat in London those eight days instead, so it lands near A$3,540. The whole decision is whether the walk is worth about A$1,250 and going A$790 over. ONE REAL LEVER IF YOU WANT IT: the Galician public albergues are about 10 euro a bunk against 45 for a room, and some stay open through January. Four of the five walking nights in a bunk instead of a room takes about A$250 off. At 63, in the rain, that is a genuine trade and not an obvious one.',
       options=['Keep the Camino, private rooms, about A$4,790',
                'Keep the Camino but sleep in albergues, about A$4,540',
                'Drop the Camino and land at about A$3,540'],
       recommendation='Keep it. You are 63, you are going to be on that side of the world once, and A$1,300 for six days walking into Santiago with the certificate at the end is the cheapest big thing on this whole trip. If the A$790 has to come from somewhere, it comes from eating out less in London, where you have a kitchen and a daughter, not from the walk.',
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
       why='Sixteen nights, in three blocks: five in early December, ten over Christmas and New Year, and one at the end. At London hotel rates that is about A$3,500, and it is the single biggest reason any of this fits. Every night that turns into a hotel puts about A$220 back on the total, so six nights in a hotel is the whole Camino.',
       options=['All sixteen, she has offered', 'Most of them, a few nights elsewhere', 'Need to ask her'],
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
  dict(id='sy1b', name='Your daughter\u2019s, 23 Dec to 2 Jan', town='London', status='booked',
       pricePerNightAud=0, nights=10, checkIn='2026-12-23', checkOut='2027-01-02', type='Family',
       notes='The long block: home from Bergen on the 23rd, Christmas Eve, Christmas, the football on the 30th, New Year, then away to Spain on the 2nd. Ten nights, and the reason this trip fits a budget at all.'),
  dict(id='sy1c', name='Your daughter\u2019s, 9 to 10 Jan', town='London', status='booked',
       pricePerNightAud=0, nights=1, checkIn='2027-01-09', checkOut='2027-01-10', type='Family',
       notes='Back from Santiago, one night, then home. SIXTEEN NIGHTS AT HERS IN TOTAL. At London hotel rates that is about A$3,500, which is most of the difference between this trip happening and not. Ask her about all three blocks at once rather than in instalments.'),
  dict(id='sy0', name='Hurtigruten, Bergen to Kirkenes and back', town='Hurtigruten', status='booked',
       pricePerNightAud=0, nights=11, checkIn='2026-12-11', checkOut='2026-12-22',
       type='Cabin on the coastal express',
       notes='Eleven nights, already paid, so it costs nothing more. Here so the Stays page can always answer where you are sleeping tonight, which on the 16th of December in the Arctic is a fair question. Meals are included; the only money on these days is ashore.'),
  dict(id='sy4', name='Bergen, night of 22 Dec', town='Bergen', status='planned', pricePerNightAud=220, nights=1,
       checkIn='2026-12-22', checkOut='2026-12-23', type='Hotel or guesthouse',
       distance='Walkable from the Hurtigruten terminal',
       notes='Off the ship at 14:45 with nowhere to be. Book the same place as the 10th if you can: you will already know the walk from the terminal, which is worth something after eleven nights at sea. A$220, and it buys you a day of slack before flying two days before Christmas.'),
  dict(id='sy3', name='Bergen, night of 10 Dec', town='Bergen', status='planned', pricePerNightAud=220, nights=1,
       checkIn='2026-12-10', checkOut='2026-12-11', distance='Walkable to Bryggen and the Hurtigruten terminal',
       type='Hotel or guesthouse',
       notes='The night before the ship, and it is not negotiable: you do not fly to a cruise on the day it sails. Bergen is expensive but the centre is small, so anything near Bryggen or the fish market walks to everything including the terminal. Look at guesthouses and the Bergen YMCA as well as hotels.'),
  # Real places, in the middle of each town, all on or within a couple of minutes
  # of the Camino. Prices are the off-season private-room rate; the A$55 a night
  # this was costed at before was an albergue bunk rate and too low for a room of
  # your own. WINTER IS THE CATCH: ring or email each one in November, because
  # plenty of Camino lodging shuts between Christmas and mid-January and the ones
  # that stay open fill with the few pilgrims who are walking.
  dict(id='sy6', name='Sarria: Hotel Mar de Plata, or Casa Mat\u00edas', town='Sarria', status='planned',
       pricePerNightAud=85, nights=1, checkIn='2027-01-02', checkOut='2027-01-03',
       type='Hotel, 25 rooms', address='Sarria, Lugo', distance='On the Camino, in the town centre',
       priceNote='Mar de Plata 45-58 euro a room, listed as open year round',
       notes='MAR DE PLATA IS THE PICK: about 45 to 58 euro, twenty-five rooms, and it is listed as open all year, which in January is the thing that matters most. Casa Mat\u00edas (Albergue Mat\u00edas Locanda) is the other good one, 45 to 50 euro for a private room or 12 euro for a bunk if you want to try the albergue once. Hotel Alfonso IX on R\u00faa Peregrino is the smart option at 55 to 90 euro, also year round, by the river. Get your credencial stamped wherever you sleep; that is stamp one of the two you need tomorrow.'),
  dict(id='sy7', name='Portomar\u00edn: Pensi\u00f3n Portomi\u00f1o', town='Portomar\u00edn', status='planned',
       pricePerNightAud=80, nights=1, checkIn='2027-01-03', checkOut='2027-01-04',
       type='Pensi\u00f3n, private rooms with ensuite', distance='In the village, on the Camino',
       priceNote='40 to 75 euro depending on room and season',
       notes='Singles, doubles and twins, all with their own bathroom, and used to pilgrims. Portomar\u00edn is small, so book ahead rather than turning up: in January half the village is shut. Remember the town was moved stone by stone up the hill when they dammed the river, and you arrive over the long bridge and up a staircase, which is a cruel last hundred metres after 22 km.'),
  dict(id='sy8', name='Palas de Rei: Pensi\u00f3n Plaza, or Casa Camino', town='Palas de Rei', status='planned',
       pricePerNightAud=80, nights=1, checkIn='2027-01-04', checkOut='2027-01-05',
       type='Pensi\u00f3n with private rooms', distance='Town centre, on the Camino',
       notes='Pensi\u00f3n Plaza does private rooms with ensuite, laundry and wifi, which after two days of walking in the rain makes the laundry the selling point. Pensi\u00f3n Restaurante Casa Camino is the other, and having the restaurant downstairs is worth something on a night when you do not want to go out again. Palas de Rei is a proper Camino hub with cafes and a supermarket, so this is the night to buy whatever you need for the 29 km tomorrow.'),
  dict(id='sy10', name='Arz\u00faa: Pensi\u00f3n Casa Frade', town='Arz\u00faa', status='planned',
       pricePerNightAud=80, nights=1, checkIn='2027-01-05', checkOut='2027-01-06',
       type='Pensi\u00f3n, 6 rooms, all ensuite', distance='In the centre of Arz\u00faa',
       notes='THE NIGHT AFTER THE 29 KM DAY, so do not economise here. Six rooms, all with their own bathroom, television and wifi, in the middle of town. Hotel Suiza is the step up at about 64 euro if Casa Frade is full. Only six rooms, so book this one first of the five. Buy some tetilla, the local soft cheese, before the shops shut: tomorrow is Epiphany and Spain closes.'),
  dict(id='sy11', name='O Pedrouzo: Pensi\u00f3n Arca, or 9 de Abril', town='O Pedrouzo', status='planned',
       pricePerNightAud=80, nights=1, checkIn='2027-01-06', checkOut='2027-01-07',
       type='Pensi\u00f3n with private rooms', distance='Town centre, 500 m off the Camino',
       notes='Pensi\u00f3n Arca gets called the best bed in O Pedrouzo by people who have tried several. Pensi\u00f3n 9 de Abril is the other, in the centre, rooms with ensuite and a view. Pensi\u00f3n Pedrouzo is the third. Last night before Santiago, and you will want an early start, so ask tonight whether they can do breakfast before eight or leave you something out.'),
  dict(id='sy12', name='Santiago: Hospeder\u00eda San Mart\u00edn Pinario', town='Santiago de Compostela', status='planned',
       pricePerNightAud=115, nights=2, checkIn='2027-01-07', checkOut='2027-01-09',
       type='Converted 16th-century monastery, opposite the cathedral',
       address='Pra\u00e7a da Inmaculada 3, Santiago de Compostela',
       distance='Directly opposite the cathedral', url='https://www.sanmartinpinario.es/',
       priceNote='About 100 to 165 a night; pilgrim rates are often cheaper, so ask',
       notes='BOOK THIS ONE BEFORE ANY OF THE OTHERS. It is a working monastery turned hotel directly across the square from the cathedral, it has been putting up pilgrims for four hundred years, and the dining room is a vaulted hall. Plain rooms, and that is the point. It is the single best thing you can arrange for the end of this walk: you come under the archway into the square having walked 116 km, and your bed is right there. Two nights, the 7th and the 8th. Ask about the pilgrim rate when you book, and show the Compostela. If it is full, Hotel Costa Vella has a garden and Hotel Alta\u00efr is the design one, both in the old town.'),
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

FLIGHTS = [
  dict(id='out', flight='(flight number to add)', from_='Brisbane', to='London Heathrow',
       date='2026-12-04', arrDate='2026-12-05', dep='(to add)', arr='16:10', cabin='Economy',
       duration='about 24 h with one stop',
       notes='BOOKED. Arrives Heathrow 16:10 on Saturday 5 December. Ask whoever booked it for the flight numbers, the airline and the stopover airport, and Connor will put them in; then this page tells you your seat and your connection instead of just the landing time. Check in online 24 hours before and pick an aisle seat: on a 24-hour flight you will want to get up without climbing over anyone.'),
  dict(id='home', flight='(flight number to add)', from_='London Heathrow', to='Brisbane',
       date='2027-01-10', arrDate='2027-01-11', dep='13:40', arr='(to add)', cabin='Economy',
       duration='about 24 h with one stop',
       notes='BOOKED. Leaves Heathrow 13:40 on Sunday 10 January, so be at the airport by 10:40 and leave your daughter\u2019s by about 09:30. A Sunday, so check the night before for engineering works on whichever line you are taking.'),
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
  'g1': 'py12', 'g2': 'py13', 'g3': 'py15', 'g3b': 'py14', 'g5': 'py16', 'g6': 'py17', 'g7': 'py18',
  'g8': 'py17', 'g9': 'py17', 'g11': 'py17', 'z1': 'py1', 'z2': 'py1',
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

SOUVENIRS = [
  dict(id='v1', category='Spirits and bar', name='Norwegian aquavit', ml=500, priceBand='kr kr', status='idea',
       where='Vinmonopolet, the state liquor shop, in Bergen or Tromso. NOT the ship',
       why='Potato spirit flavoured with caraway and aged in sherry casks, and the ones that have crossed the equator in a ship\u2019s hold are a real thing, not a marketing story. Linie is the famous one. Almost impossible to buy in Australia and it is what Norwegians actually drink at Christmas.',
       notes='Alcohol in Norway is sold only at Vinmonopolet, which shuts early and all day Sunday, so buy it on the 11th in Bergen while you have the afternoon. It is expensive there; buying at the airport on the way out is genuinely cheaper.'),
  dict(id='v2', category='Spirits and bar', name='Irish whiskey, if you get to Dublin', ml=700, priceBand='\u20ac\u20ac', status='idea',
       where='Any Dublin off-licence, or the airport',
       why='Redbreast 12 or Green Spot are the two worth the allowance: both are A$100 or more in Australia and about half that in Ireland. Guinness itself is not worth carrying, because you can buy it at home and the whole point of it is that it is poured properly.',
       notes='Only if Dublin goes back in. See Decisions.'),
  dict(id='v3', category='Spirits and bar', name='Albarino, a bottle from Galicia', ml=750, priceBand='\u20ac', status='idea',
       where='Any shop in Santiago',
       why='The white wine of Galicia, crisp and salty, and about 6 euro there against A$35 here. Heavy for what it is, so one bottle, and only if the allowance is not already spoken for.'),
  dict(id='v4', category='The Camino', name='Your Compostela', priceBand='free', status='planned',
       where='The Pilgrim\u2019s Office, Santiago, 8 January',
       why='The certificate with your name on it in Latin. The best souvenir of this entire trip and it costs nothing. THEY SELL A CARDBOARD TUBE FOR A EURO OR TWO: buy it. A rolled certificate in a suitcase for two days does not survive.'),
  dict(id='v5', category='The Camino', name='A scallop shell', priceBand='\u20ac', status='planned',
       where='Anywhere on the Camino; most pilgrims tie one to the pack at the start',
       why='The symbol of the Camino since the middle ages and the thing every pilgrim carries. A euro or two, weighs nothing, and it is the one object that will mean something in ten years.'),
  dict(id='v6', category='Food and snacks', name='Norwegian brown cheese, and other food rules', priceBand='kr', status='idea',
       where='Any Norwegian supermarket',
       why='Brunost is caramelised whey, sweet and strange and genuinely Norwegian. Commercially packaged hard cheese is usually fine into Australia.',
       notes='DECLARE EVERY FOOD ITEM ON THE INCOMING CARD, without exception. Commercially packaged, shelf-stable and sealed is almost always waved through once declared. The soft cheeses are the risk: the tetilla in Arzua and anything from a market stall is unsealed dairy and will be taken off you. Nothing containing meat, ever. Declaring something that turns out to be fine costs thirty seconds; not declaring something that is not fine starts at a A$2,000 fine.'),
  dict(id='v7', category='For other people', name='Work out who actually gets something, before you go', priceBand='\u20ac', status='idea',
       where='Decide at home, buy on the last few days',
       why='Five weeks is a long time to carry things you bought in week one. Write the names down before you leave and buy everything in Santiago and London at the end, when you know what is left in the bag and in the budget.'),
  dict(id='v8', category='Everyday things', name='Nothing bulky, and nothing in week one', priceBand='', status='idea',
       where='n/a',
       why='You are carrying your own bag up a hill in Galicia in January. Anything bought before the 8th of January has to be carried over 116 km or posted home. Buy at the end.'),
]

SOUVENIR_GUIDE = [
  dict(title='What Australia lets you bring in',
       body='Two limits and both work the same cruel way: go over and duty is charged on the WHOLE lot, not just the excess. Alcohol: 2.25 litres per adult, which is three ordinary bottles and nothing more, and buying at the airport does not change it because the limit is on what you bring in rather than where you bought it. General goods: A$900, covering gifts, souvenirs, electronics and the rest. A bottle or two and a few small things will not trouble either. The meter at the top of this page counts anything you mark as on the list or bought, so keep it honest and it will tell you when to stop.'),
  dict(title='Declare the food. All of it.',
       body='Australian biosecurity is the strictest border you will cross and the incoming passenger card is not a formality. Declare all food, plant and wooden items without exception. Sealed, commercially packaged, shelf-stable things are almost always allowed through once declared. Anything with meat in it is prohibited outright. Unsealed dairy, fresh produce and dried plant material will be taken off you. The red lane costs you thirty seconds; the fine starts at A$2,000.'),
  dict(title='Tax back on the way out of Europe',
       body='Spain and Ireland refund the VAT on purchases over about 100 euro in one shop if you are leaving the EU, which you are. Ask for the form in the shop, keep the receipt, and find the refund desk at the airport BEFORE you check the bag, because they may want to see what you bought. The UK stopped doing this for visitors in 2021, so nothing bought in London qualifies. On the amounts you are likely to spend this is probably not worth chasing, but the Galician wine plus a jacket could tip it over.'),
]

trip = dict(
  meta=dict(
    title='Dad’s Trip 2026/27', start=START, end=END, homeCurrency='AUD',
    rates=RATES, updatedAt=UPDATED, version=1,
    mapRegion='', travelMode='transit',
    features=dict(flights=True, budget=True, points=False),
    categories=['Flights', 'Accommodation', 'Transport', 'Food', 'Activities', 'Other'],
    about='Thirty-six nights: London with your daughter, eleven on the Hurtigruten chasing the northern lights, Christmas in London, Arsenal on the 30th, and the last 116 km of the Camino, with two nights in Santiago at the end. About A$4,000 of it you will certainly spend and another A$950 only if you choose to, on top of the flights and the cruise already paid. The A$4,000 is the top of your budget exactly, so the first thing on Decisions is what to do about that. Open Go to see only what is happening now.',
  ),
  days=days,
  flights=dict(confirmed=FLIGHTS, legs=[], lounges=[]),
  people=[], foodGuide=[], staysGuide=[], souvenirGuide=SOUVENIR_GUIDE,
  points={}, stays=stays, food=food, souvenirs=SOUVENIRS, budget=budget, checklist=checklist,
  places=places, questions=questions,
)

trip = carry_over(trip, 'data/europe.json')

with open('data/europe.json', 'w') as f:
    json.dump(trip, f, indent=2, ensure_ascii=False)
    f.write('\n')

print('wrote data/europe.json %d days, %d items, %d stays, %d food, %d todos, %d budget lines, %d questions' % (
    len(trip['days']), sum(len(d['items']) for d in trip['days']), len(trip['stays']),
    len(trip['food']), len(trip['checklist']), len(trip['budget']), len(trip['questions'])))
