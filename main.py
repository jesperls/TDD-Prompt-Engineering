"""
Concert Itinerary Builder

This module provides functionality to build an itinerary of upcoming concerts.
"""
from collections import defaultdict
import math

class Concert:
    """
    Represents a concert event.
    
    Attributes:
        artist (str): The name of the artist performing.
        date (str): The date of the concert in 'YYYY-MM-DD' format.
        location (str): The location where the concert will take place.
        latitude (float): Latitude coordinate of the concert location.
        longitude (float): Longitude coordinate of the concert location.
    """
    
    def __init__(self, artist, date, location, latitude, longitude):
        self.artist = artist
        self.date = date
        self.location = location
        self.latitude = latitude
        self.longitude = longitude

class ItineraryBuilder:
    def build_itinerary(self, concerts):
        concerts_by_artist = defaultdict(list)
        for concert in concerts:
            concerts_by_artist[concert.artist].append(concert)

        earliest_concert_by_artist = {
            artist: min(c_list, key=lambda c: c.date)
            for artist, c_list in concerts_by_artist.items()
        }

        single_concerts = [
            concert for artist, concert in earliest_concert_by_artist.items()
            if len(concerts_by_artist[artist]) == 1
        ]
        multi_concerts = [
            concert for artist, concert in earliest_concert_by_artist.items()
            if len(concerts_by_artist[artist]) > 1
        ]

        single_concerts.sort(key=lambda c: c.date)
        multi_concerts.sort(key=lambda c: c.date)

        itinerary = []
        used_dates = set()
        added_artists = set()

        def distance(c1, c2):
            return math.hypot(c1.latitude - c2.latitude, c1.longitude - c2.longitude)

        def resolve_same_day_conflict(candidates):
            if not itinerary:
                return min(candidates, key=lambda c: c.date)
            last = itinerary[-1]
            return min(candidates, key=lambda c: distance(c, last))

        for concert_list in [single_concerts, multi_concerts]:
            for concert in concert_list:
                if concert.date in used_dates:
                    same_day = [
                        c for c in concert_list
                        if c.date == concert.date and c.artist not in added_artists
                    ]
                    if same_day:
                        chosen = resolve_same_day_conflict(same_day)
                        if chosen.date not in used_dates and chosen.artist not in added_artists:
                            itinerary.append(chosen)
                            used_dates.add(chosen.date)
                            added_artists.add(chosen.artist)
                elif concert.artist not in added_artists:
                    itinerary.append(concert)
                    used_dates.add(concert.date)
                    added_artists.add(concert.artist)

        itinerary.sort(key=lambda c: c.date)
        return itinerary
