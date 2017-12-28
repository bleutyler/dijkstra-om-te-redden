import unittest
import traingraph

class TestTrainGraph( unittest.TestCase ):
	def setUp( self ):
		self.simple_dict = { 'A' : { 'B' : 2 , 'C' : 11 }, 'B' : { 'A': 3 , 'C' : 2 } }
		self.medium_dict = {'A': {'C': 4,'B': 9}, 'C': {'D': 5}, 'B': {'C': 3, 'D': 6}, 'E': {'A': 33, 'B': 3, 'F': 3}, 'D': {'A': 5, 'C': 3}, 'F': {'E': 2, 'D': 7}}
		self.large_dict  = {'A': {'C': 4, 'B': 9}, 'C': {'H': 45, 'D': 5}, 'B': {'C': 3, 'D': 6}, 'E': {'A': 33, 'B': 3, 'F': 3}, 'D': {'A': 5, 'C': 3}, 'G': {'H': 14}, 'F': {'A': 12, 'E': 2, 'D': 7, 'G': 2}, 'I': {'H': 2, 'J': 2}, 'H': {'I': 2, 'C': 45, 'J': 2}, 'K': {'J': 15}, 'J': {'I': 2, 'H': 2, 'K': 15}}
		self.empty_dict = {}


	def test_constructors( self ):
		tg_empty = traingraph.traingraph()
		self.assertEqual( tg_empty.graph(), self.empty_dict, 'Constructor with no params gives empty graph' )
		tg = traingraph.traingraph( self.simple_dict )
		self.assertEqual( tg.graph(), self.simple_dict, 'Constructor with dictionary gives dictionary as the graph' )

		# Input Errors
		tg_with_list  	= traingraph.traingraph( [] )
		self.assertEqual( tg_with_list.graph(), self.empty_dict, 'Constructor with list gives empty graph' )
		tg_with_string 	= traingraph.traingraph( 'string here' )
		self.assertEqual( tg_with_string.graph(), self.empty_dict, 'Constructor with string  gives empty graph' )

	def test_getters_and_setters( self ):
		tg_simple = traingraph.traingraph( self.simple_dict )
		simple_with_new_element = self.simple_dict.copy()
