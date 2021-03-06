import unittest

import os, sys
sys.path.append(os.path.abspath(sys.path[0]) + '/../')
import analyseren
from lib import graph
from lib import config



class TestAnalyseren( unittest.TestCase ):
	def setUp( self ):
		self.large_dict  = {'A': {'C': 4, 'B': 9}, 'C': {'H': 45, 'D': 5}, 'B': {'C': 3, 'D': 6}, 'E': {'A': 33, 'B': 3, 'F': 3}, 'D': {'A': 5, 'C': 3}, 'G': {'H': 14}, 'F': {'A': 12, 'E': 2, 'D': 7, 'G': 2}, 'I': {'H': 2, 'J': 2}, 'H': {'I': 2, 'C': 45, 'J': 2}, 'K': {'J': 15, 'L' : 4 }, 'J': {'I': 2, 'H': 2, 'K': 15}}
		self.large_graph = graph.graph( self.large_dict )
		self.example_dict = { 'A' : { 'B' : 5, 'D' : 5, 'E' : 7 }, 'B' : { 'C' : 4 }, 'C' : { 'D' : 8 , 'E' : 2 }, 'D' : { 'C' : 8, 'E' : 6 }, 'E':{'B':3} }
		self.example_graph = graph.graph( self.example_dict )
		#         AB5, BC4, CD8, DC8, DE6, AD5, CE2, EB3, AE7


		# self.empty_dict = {}
		# self.empty_list = []

	def _test_strings_of_paths_are_equal( self, list_1, list_2 , msg ):
		list_of_first_items  = list_1.split( ', ' )
		list_of_second_items = list_2.split( ', ' )
		self.assertCountEqual( list_1, list_2, msg )

	def test_execute_command_shortest_path( self ):
		expected_output = '14'
		test_output	= analyseren.execute_command( 'AEBC l' , self.example_graph )
		self.assertEqual( expected_output, test_output, 'execute_command() shortest path ' )

		expected_output = config.NO_ROUTE_TO_USER_STRING
		test_output	= analyseren.execute_command( 'ZABC l' , self.example_graph )
		self.assertEqual( expected_output, test_output, 'execute_command() shortest path no route' )

		expected_output = '18'
		test_output	= analyseren.execute_command( 'ADEBC l' , self.example_graph )
		self.assertEqual( expected_output, test_output, 'execute_command() shortest path' )

		expected_output = '21'
		test_output	= analyseren.execute_command( 'CDEBC l' , self.example_graph )
		self.assertEqual( expected_output, test_output, 'execute_command() shortest path start == end' )


	def test_execute_command_max_stops( self ):
		expected_output = '11'
		test_output	= analyseren.execute_command( 'EC 5ms' , self.large_graph )
		self._test_strings_of_paths_are_equal( expected_output, test_output, 'execute_command() max stops checks' )

		expected_output = config.NO_ROUTE_TO_USER_STRING
		test_output	= analyseren.execute_command( 'EC 2ms' , self.large_graph )
		self.assertEqual( expected_output, test_output, 'execute_command() max stops checks stops exist, but more than max ' )

		expected_output = '2'
		test_output	= analyseren.execute_command( 'EC 3ms' , self.large_graph )
		self._test_strings_of_paths_are_equal( expected_output, test_output, 'execute_command() max stops checks stops exist, but some more than max ' )



	def test_execute_command_n_stops( self ):
		expected_output = '5'
		test_output	= analyseren.execute_command( 'EC 5s' , self.large_graph )
		self.assertEqual( expected_output, test_output, 'execute_command() only X stops checks' )

		expected_output = '1'
		test_output	= analyseren.execute_command( 'AB 2s' , self.large_graph )
		self.assertEqual( expected_output, test_output, 'execute_command() only X stops checks' )

		expected_output = config.NO_ROUTE_TO_USER_STRING
		test_output	= analyseren.execute_command( 'EL 6s' , self.large_graph )
		self.assertEqual( expected_output, test_output, 'execute_command() only X stops checks, none' )



	def test_execute_max_distance( self ):
		expected_output = '11'
		test_output	= analyseren.execute_command( 'EC 50d' , self.large_graph )
		self.assertEqual( expected_output, test_output, 'execute_command() max distance test we got ' + test_output )

		expected_output = '6'
		test_output	= analyseren.execute_command( 'EC 20d' , self.large_graph )
		self.assertEqual( expected_output, test_output, 'execute_command() max distance test longer routes exist but are not shown' )

		expected_output = config.NO_ROUTE_TO_USER_STRING
		test_output	= analyseren.execute_command( 'EC 5d' , self.large_graph )
		self.assertEqual( expected_output, test_output, 'execute_command() max distance test no routes found ' )


	def test_execute_length_of_path( self ):
		expected_output = '33'
		test_output	= analyseren.execute_command( 'EFABDC l' , self.large_graph )
		self.assertEqual( expected_output, test_output, 'execute_command() path len 1/2' )
		
		expected_output = '19'
		test_output	= analyseren.execute_command( 'EFAC l' , self.large_graph )
		self.assertEqual( expected_output, test_output, 'execute_command() path len 2/2' )

		expected_output = config.NO_ROUTE_TO_USER_STRING
		test_output	= analyseren.execute_command( 'IAE l' , self.large_graph )
		self.assertEqual( expected_output, test_output, 'execute_command() path len path no exist' )

		expected_output = '5'
		test_output	= analyseren.execute_command( 'EFE l' , self.large_graph )
		self._test_strings_of_paths_are_equal( expected_output, test_output, 'execute_command() path len start == end' )





	## ## ## ## ## ## ## ##
	## input errors
	## ## ## ## ## ## ## ##
	def test_execute_command_input_errors( self ):

		expected_output = 'Unknown Command: ZEEDMORE'
		test_output	= analyseren.execute_command( 'ZEEDMORE' , self.example_graph )
		self.assertEqual( expected_output, test_output, 'execute_command() input error' )

		expected_output = 'Unknown Command: ZEE'
		test_output	= analyseren.execute_command( 'ZEE' , self.example_graph )
		self.assertEqual( expected_output, test_output, 'execute_command() input error' )

		expected_output = 'Unknown Command: 333'
		test_output	= analyseren.execute_command( '333' , self.example_graph )
		self.assertEqual( expected_output, test_output, 'execute_command() input error' )

		expected_output = 'Unknown Command: AE 333' # so close
		test_output	= analyseren.execute_command( 'AE 333' , self.example_graph )
		self.assertEqual( expected_output, test_output, 'execute_command() input error' )


