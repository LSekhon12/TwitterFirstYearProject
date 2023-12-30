""" Test Cases / Unittests for get_filter_results are all here"""

import unittest
import twitterverse_functions as tf


class TestGetFilterResults(unittest.TestCase):
    """Test cases for function twitterverse_functions.get_filter_results
    """

    def test_following_none_filtered(self) -> None:
        """Test get_filter_results for a single filter of following,
        in which all usernames are kept
        I was only able to do one unittest :((
        """

        twitter_data = \
            {'tomCruise': {'name': 'Tom Cruise', 
                        'location': 'Los Angeles, CA',
                        'web': 'http://www.tomcruise.com',
                        'bio': 'Official TomCruise.com crew tweets. ' +
                        'We love you guys!\nVisit us at Facebook!', 
                        'following': ['katieH']},
            'jimjones': {'name': 'Jim Jones',
                        'location': '',
                        'web': 'http://www.jonesy.com',
                        'bio': '',
                        'following': ['katieH']},
            'katieH': {'name': 'Katie Holmes', 'location': '',
                       'web': 'www.tomkat.com', 'bio': '', 'following': []}}
        usernames = 'tomCruise'
        filt = {'following': 'katieH'}
        actual = tf.get_filter_results(twitter_data, usernames, filt)
        expected = ['tomCruise', 'jimjones']
        msg = "Expected {}, but got {}".format(expected, actual)
        self.assertEqual(actual, expected, msg)


if __name__ == '__main__':
    unittest.main(exit=False)
