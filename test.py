"""
Unit tests for the Concert Itinerary Builder.

This file contains unit tests for the ItineraryBuilder class in main.py.
Participants will implement tests based on the system specifications.
"""

import unittest
from main import ItineraryBuilder
from concerts_data import get_all_concerts

class ItineraryBuilderTest(unittest.TestCase):
    """Test cases for the ItineraryBuilder class."""
    
    def setUp(self):
        """Set up for the tests."""
        self.builder = ItineraryBuilder()
        
        self.all_concerts = get_all_concerts()

    def _get_conserts_chronologically_by_artist(self, concerts, artist):
        fetched_conserts = []
        for concert in concerts:
            if concert.artist == artist:
                fetched_conserts.append(concert)
        return sorted(fetched_conserts, key= lambda concert: concert.date)
    
    # ----- Manual Test Cases -----
    # Participants will implement their manual test cases here. 
    
    def test_manual_1(self):
        """Some artists may have no concerts on the list. In that case, that should be indicated in the itinerary."""
        intinerary = self.builder.build_itinerary(self.all_concerts)
        all_artists = [_.artist for _ in self.all_concerts]
        intinerary_artists = [concert.artist for concert in intinerary]

        self.assertTrue(set(intinerary_artists).issubset(set(all_artists)), "Intinerary contains artists not in the concert list.")
    
    def test_manual_2(self):
        """The itinerary should return a list of concerts sorted in chronological order (by date from earliest to latest)."""
        intinerary = self.builder.build_itinerary(self.all_concerts)
        last_date = ""
        for concert in intinerary:
            self.assertGreater(concert.date, last_date, "Intinerary is not sorted chronologically.")
            last_date = concert.date

    def test_manual_3(self):
        """An artist has at most one concert in the itinerary. If an artist has more than one concert in the list, the itinerary should only include the one with the earliest start date."""
        itinerary = self.builder.build_itinerary(self.all_concerts)
        itinerary_artists = [concert.artist for concert in itinerary]

        self.assertEqual(len(itinerary_artists), len(set(itinerary_artists)), "The same artist appears twice in the same itinerary.")

        for artist in itinerary_artists:
            itinerary_concert = self._get_conserts_chronologically_by_artist(itinerary, artist)
            all_concerts = self._get_conserts_chronologically_by_artist(self.all_concerts, artist)
            self.assertEqual(itinerary_concert[0].date, all_concerts[0].date, "The concert of an artist is not the one with their earliest start date.")

    # ----- AI-Assisted Test Cases -----
    # Participants will implement their AI-assisted test cases here.
    # Please name your test in a way which indicates that these are AI-assisted test cases.

    def test_ai_assisted_no_two_concerts_same_day(self):
        """No two concerts may take place on the same day. If two different artists (or the same artist) have a concert on the same day, the itinerary only includes the concert closest to the last one."""
        itinerary = self.builder.build_itinerary(self.all_concerts)
        itinerary_dates = {}

        for concert in itinerary:
            if concert.date in itinerary_dates:
                last_concert = itinerary_dates[concert.date]
                distance_last = ((last_concert.latitude - concert.latitude)**2 + (last_concert.longitude - concert.longitude)**2)**0.5
                distance_current = ((last_concert.latitude - concert.latitude)**2 + (last_concert.longitude - concert.longitude)**2)**0.5
                self.assertLessEqual(distance_current, distance_last, "Concert on the same day is not the closest to the last one.")
            else:
                itinerary_dates[concert.date] = concert

    def test_ai_assisted_concert_details(self):
        """The itinerary should return a list of concerts that state the artist, date, and location of each concert."""
        itinerary = self.builder.build_itinerary(self.all_concerts)

        for concert in itinerary:
            self.assertIsNotNone(concert.artist, "Concert artist is missing.")
            self.assertIsNotNone(concert.date, "Concert date is missing.")
            self.assertIsNotNone(concert.location, "Concert location is missing.")

    def test_ai_assisted_single_concert_priority(self):
        """
        If a single-concert artist is not included in the itinerary,
        it must be because another single-concert artist's concert occurred on the same date
        and was closer to the previous concert.
        """
        itinerary = self.builder.build_itinerary(self.all_concerts)
        itinerary_artists = [concert.artist for concert in itinerary]
        itinerary_by_date = {concert.date: concert for concert in itinerary}
        
        # Identify single-concert artists and their concert
        artist_counts = {}
        for concert in self.all_concerts:
            artist_counts[concert.artist] = artist_counts.get(concert.artist, 0) + 1

        single_concerts = [concert for concert in self.all_concerts if artist_counts[concert.artist] == 1]

        for concert in single_concerts:
            if concert.artist in itinerary_artists:
                continue  # good

            # Check if the concert date is taken by another single-concert artist
            if concert.date in itinerary_by_date:
                occupying_concert = itinerary_by_date[concert.date]
                # Both must be single-concert artists if one got excluded
                self.assertTrue(
                    artist_counts[occupying_concert.artist] == 1,
                    f"Artist {concert.artist} was excluded in favor of a multi-concert artist on {concert.date}."
                )
            else:
                self.fail(f"Artist {concert.artist} with one concert was excluded for no reason.")

if __name__ == "__main__":
    unittest.main()
