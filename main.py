"""
Concert Itinerary Builder

This module provides functionality to build an itinerary of upcoming concerts.
"""

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
    """
    A class to build concert itineraries. 
    """
    
    def build_itinerary(self, concerts):
        itinerary = []
        for concert in sorted(concerts, key= lambda concert: concert.date):
            if concert.artist in [_.artist for _ in itinerary]:
                continue
            if concert.date in [_.date for _ in itinerary]:
                continue
            itinerary.append(concert)
        return itinerary
