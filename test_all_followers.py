""" CSC108: Fall 2020 -- Assignment 3: Twitterverse 

This code is provided solely for the personal and private use of students 
taking the CSC108 course at the University of Toronto. Copying for purposes 
other than this use is expressly prohibited. All forms of distribution of 
this code, whether as given or with any changes, are expressly prohibited.

All of the files in this directory and all subdirectories are:
Copyright (c) 2020 Mario Badr, Jennifer Campbell, Tom Fairgrieve, Diane Horton, 
Michael Liut, Jacqueline Smith, and Anya Tafliovich.
"""

import unittest
import twitterverse_functions


class TestAllFollowers(unittest.TestCase):
    """Test cases for function twitterverse_functions.all_followers
    """

    def test_single_follower(self) -> None:
        """Test all_followers with a user followed by one other user.
        """

        twitter_data = \
            {'tomCruise': {'name': 'Tom Cruise', 
                           'location': 'Los Angeles, CA', 
                           'web': 'http://www.tomcruise.com', 
                           'bio': 'Official TomCruise.com crew tweets. '+ \
                           'We love you guys!\nVisit us at Facebook!', 
                           'following': ['katieH']}, 
             'katieH': {'name': 'Katie Holmes', 'location': '', 
                        'web': 'www.tomkat.com', 'bio': '', 'following': []}}
        actual = twitterverse_functions.all_followers(twitter_data, 'katieH')
        expected = ['tomCruise']
        msg = "Expected {}, but got {}".format(expected, actual)
        self.assertEqual(actual, expected, msg)

    # Add your own test cases here


if __name__ == '__main__':
    unittest.main(exit=False)
