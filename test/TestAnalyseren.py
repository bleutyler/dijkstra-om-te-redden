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

	def test_execute_command( self ):
		expected_output = 'CE'
		test_output	= analyseren.execute_command( 'CE' , self.example_graph )
		self.assertEqual( expected_output, test_output, 'execute_command() shortest path ' )

		expected_output = config.NO_ROUTE_TO_USER_STRING
		test_output	= analyseren.execute_command( 'ZE' , self.example_graph )
		self.assertEqual( expected_output, test_output, 'execute_command() shortest path no route' )

		expected_output = 'ABC'
		test_output	= analyseren.execute_command( 'AC' , self.example_graph )
		self.assertEqual( expected_output, test_output, 'execute_command() shortest path' )

		expected_output = 'EBC'
		test_output	= analyseren.execute_command( 'EC' , self.example_graph )
		self.assertEqual( expected_output, test_output, 'execute_command() shortest path' )



	@unittest.skip( "method not yet implemented" )
	def test_exe_to_stkpi( self ):
		expected_output = 'ms1'
		test_output	= analyseren.execute_command( 'EC 5ms' , self.example_graph )
		self.assertEqual( expected_output, test_output, 'execute_command() max stops checks' )

		expected_output = config.NO_ROUTE_TO_USER_STRING
		test_output	= analyseren.execute_command( 'EC 2ms' , self.example_graph )
		self.assertEqual( expected_output, test_output, 'execute_command() max stops checks stops exist, but more than max ' )

		expected_output = 'ESA'
		test_output	= analyseren.execute_command( 'EL 5ms' , self.example_graph )
		self.assertEqual( expected_output, test_output, 'execute_command() max stops checks stops exist, but some more than max ' )



		expected_output = 's1'
		test_output	= analyseren.execute_command( 'EC 5s' , self.example_graph )
		self.assertEqual( expected_output, test_output, 'execute_command() only X stops checks' )

		expected_output = 's1'
		test_output	= analyseren.execute_command( 'EC 2s' , self.example_graph )
		self.assertEqual( expected_output, test_output, 'execute_command() only X stops checks' )

		expected_output = config.NO_ROUTE_TO_USER_STRING
		test_output	= analyseren.execute_command( 'EC 3s' , self.example_graph )
		self.assertEqual( expected_output, test_output, 'execute_command() only X stops checks, none' )



		expected_output = 's1'
		test_output	= analyseren.execute_command( 'EC 5s' , self.example_graph )
		self.assertEqual( expected_output, test_output, 'execute_command() only X stops checks' )

		expected_output = 's1'
		test_output	= analyseren.execute_command( 'EC 2s' , self.example_graph )
		self.assertEqual( expected_output, test_output, 'execute_command() only X stops checks' )

		expected_output = config.NO_ROUTE_TO_USER_STRING
		test_output	= analyseren.execute_command( 'EC 3s' , self.example_graph )
		self.assertEqual( expected_output, test_output, 'execute_command() only X stops checks, none' )


		## ## ## ## ## ## ## ##
		## ## ## ## ## ## ## ##
		## input errors
		## ## ## ## ## ## ## ##

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


