import unittest

import os, sys
sys.path.append(os.path.abspath(sys.path[0]) + '/../')
from lib import graph



class TestGraph( unittest.TestCase ):
	def setUp( self ):
		self.simple_dict = { 'A' : { 'B' : 2 , 'C' : 11 }, 'B' : { 'A': 3 , 'C' : 2 } }
		self.medium_dict = {'A': {'C': 4,'B': 9}, 'C': {'D': 5}, 'B': {'C': 3, 'D': 6}, 'E': {'A': 33, 'B': 3, 'F': 3}, 'D': {'A': 5, 'C': 3}, 'F': {'E': 2, 'D': 7}}
		self.large_dict  = {'A': {'C': 4, 'B': 9}, 'C': {'H': 45, 'D': 5}, 'B': {'C': 3, 'D': 6}, 'E': {'A': 33, 'B': 3, 'F': 3}, 'D': {'A': 5, 'C': 3}, 'G': {'H': 14}, 'F': {'A': 12, 'E': 2, 'D': 7, 'G': 2}, 'I': {'H': 2, 'J': 2}, 'H': {'I': 2, 'C': 45, 'J': 2}, 'K': {'J': 15, 'L' : 4 }, 'J': {'I': 2, 'H': 2, 'K': 15}}
		self.empty_dict = {}
		self.empty_list = []


	def test_constructors( self ):
		tg_empty = graph.graph()
		self.assertEqual( tg_empty.graph_please(), self.empty_dict, 'Constructor with no params gives empty graph' )
		tg = graph.graph( self.simple_dict )
		self.assertEqual( tg.graph_please(), self.simple_dict, 'Constructor with dictionary gives dictionary as the graph' )

		# Input Errors
		tg_with_list  	= graph.graph( self.empty_list )
		self.assertEqual( tg_with_list.graph_please(), self.empty_dict, 'Constructor with list gives empty graph' )
		tg_with_string 	= graph.graph( 'string here' )
		self.assertEqual( tg_with_string.graph_please(), self.empty_dict, 'Constructor with string  gives empty graph' )
		bizarre_dictionary = { 'A' : 4, 'B' : { 'C' : '4' , 'D' : 4 } }
		only_valid_values_from_bizarre = { 'A' : {}, 'B' : { 'D' : 4 } }
		tg_bizarre = graph.graph( bizarre_dictionary )
		self.assertEqual( tg_bizarre.graph_please(), only_valid_values_from_bizarre, 'Constructor with invalid values in the dictionary ignores bad input' )

	def test_getters_and_setters( self ):
		tg_simple = graph.graph( self.simple_dict )
		simple_with_new_element = self.simple_dict.copy()
		simple_with_new_element['C']      = {}
		simple_with_new_element['C']['D'] = 5
		tg_simple.put_edge( 'C', 'D', 5 )
		self.assertEqual( tg_simple.graph_please(), simple_with_new_element, 'Put edge works properly' )

		self.assertEqual( tg_simple.get_edge( 'A', 'B' ), 2, 'get_edge() works' )

		self.assertTrue( tg_simple.edge_exists( 'A', 'C' ) )
		self.assertFalse( tg_simple.edge_exists( 'not', 'exist' ) )

		self.assertEqual( tg_simple.distance( [ 'A', 'B', 'C' ] ), 4 , 'Distance calculated on a route works' )
		self.assertEqual( tg_simple.distance( [ 'A', 'A', 'A' ] ), 0 , 'Distance on a route taht does not exist is 0' )

		#####
		# input errors
		#####

		tg_input_errors = graph.graph( self.medium_dict )
		tg_input_errors.put_edge( 'A',  'D', 'F' )
		tg_input_errors.put_edge( 'A',  222,  4  )
		tg_input_errors.put_edge( None, 'D',  5  )
		self.assertEqual( tg_simple.graph_please(), simple_with_new_element, '3 inserts of bizarre inputs are ignored. Errors are not thrown ' )
		
		self.assertIsNone( tg_simple.get_edge( 'not', 'exist' ), 'get_edge() works on bad input' )

	def test_route_methods( self ):
		
		short = graph.graph( self.simple_dict) 
		self.assertEqual( short.shortest_route( 'A', 'D' ), self.empty_list, ' shortest_route() works - test 1 of 3' )
		
		med = graph.graph( self.medium_dict ) 
		self.assertEqual( med.shortest_route( 'A', 'F' ), self.empty_list, ' shortest_route() works - test 2 of 3' )
		
		expected_list = ['A', 'C', 'H', 'J', 'K', 'L']
		large = graph.graph( self.large_dict ) 
		self.assertEqual( large.shortest_route( 'A', 'L' ), expected_list, ' shortest_route() works - test 3 of 3' )

		expected_list = [ 'A', 'C', 'D', 'A' ]
		self.assertEqual( large.shortest_route( 'A', 'A' ), expected_list, ' shortest_route() works on a loop, from A to A' )
		
		self.assertFalse( short.route_exists( [ 'A', 'A' ] ) )
		self.assertTrue(  large.route_exists( [ 'F', 'A', 'B', 'D', 'C', 'H' ] ) )
		self.assertFalse( large.route_exists( [ 'C', 'E' ] ) )
		
		
		expected_list = [ ['F', 'E', 'A'], ['F', 'E', 'B', 'C', 'D', 'A'], ['F', 'E', 'B', 'D', 'A'], ['F', 'D', 'A']  ]
		self.assertCountEqual( med.calculate_all_routes( 'F', 'A' ), expected_list, ' calculate_all_routes() on medium sample data ' )

		exptected_list = []
		graph_of_unconnected_nodes = graph.graph( { 'A' : {} , 'B' : {} } )
		self.assertIsNone( graph_of_unconnected_nodes.calculate_all_routes( 'A', 'B'), ' calculate_all_routes() on unconnected graph' )
		self.assertEqual( graph_of_unconnected_nodes.shortest_route( 'A', 'B' ), self.empty_list, ' shorest_route() on unconnected graph' )
		self.assertFalse( graph_of_unconnected_nodes.route_exists( [ 'A', 'B' ] ), ' route_exists() on unconnected graph' )
		
		expected_list = []
		empty_graph = graph.graph()
		self.assertIsNone( empty_graph.calculate_all_routes( 'A', 'B' ), ' calculate_all_routes() on empty graph' )
		self.assertEqual( empty_graph.shortest_route( 'A', 'B' ), self.empty_list, ' shorest_route() on empty graph' )
		self.assertFalse( empty_graph.route_exists( [ 'A', 'B' ] ), ' route_exists() on empty graph' )

		#####
		# input errors
		#####

		self.assertEqual( large.shortest_route( 'A', 'Z' ), self.empty_list, ' shortest_route() works on nodes that do no exist - test 1 of 3' )
		self.assertEqual( large.shortest_route( 'X', 'A' ), self.empty_list, ' shortest_route() works on nodes that do no exist - test 2 of 3' )
		self.assertEqual( large.shortest_route( 'X', 'Z' ), self.empty_list, ' shortest_route() works on nodes that do no exist - test 3 of 3' )

		self.assertEqual( large.shortest_route( 1 , 'A' ), self.empty_list, ' shortest_route() works on integers - test 1 of 3' )
		self.assertEqual( large.shortest_route( 'C' , 1 ), self.empty_list, ' shortest_route() works on integers - test 2 of 3' )
		self.assertEqual( large.shortest_route( 1 , 4 ),   self.empty_list, ' shortest_route() works on integers - test 3 of 3' )

		self.assertFalse( short.route_exists( [ 'A', 'Z' ] ) )
		self.assertFalse( short.route_exists( [ 'Z', 'C' ] ) )
		self.assertFalse( short.route_exists( [ 'Z', 'Z' ] ) )
		self.assertFalse( short.route_exists( self.empty_list ) )
		
		#calculate_all_routes( self, first_node, second_node )

	def test_graph_methods( self ):
		tg = graph.graph( self.simple_dict )
		expected_graph = { 'B' : { 'C' : 2 } }
		self.assertEqual(tg.graph_with_node_removed( 'A' ).graph_please(), expected_graph, 'Node removal works 1 of 2' )

		tg = graph.graph( self.large_dict )
		expected_graph = {'C': {'H': 45, 'D': 5}, 'B': {'C': 3, 'D': 6}, 'E': {'B': 3, 'F': 3}, 'D': {'C': 3}, 'G': {'H': 14}, 'F': {'E': 2, 'D': 7, 'G': 2}, 'I': {'H': 2, 'J': 2}, 'H': {'I': 2, 'C': 45, 'J': 2}, 'K': {'J': 15, 'L' : 4 }, 'J': {'I': 2, 'H': 2, 'K': 15}}
		self.assertEqual(tg.graph_with_node_removed( 'A' ).graph_please(), expected_graph, 'Node removal works 2 of 2' )

		expected_graph = {'A': {'C': 4, 'B': 9}, 'C': {'H': 45, 'D': 5}, 'B': {'C': 3, 'D': 6}, 'E': {'A': 33, 'B': 3, 'F': 3}, 'D': {'A': 5, 'C': 3}, 'G': {'H': 14}, 'F': {'A': 12, 'E': 2, 'D': 7, 'G': 2}, 'I': {'H': 2, 'J': 2}, 'H': {'I': 2, 'C': 45, 'J': 2}, 'K': {'J': 15  }, 'J': {'I': 2, 'H': 2, 'K': 15}}
		self.assertEqual(tg.graph_with_node_removed( 'L' ).graph_please(), expected_graph, 'Node removal works on leaf nodes (no outgoing edges)' )

		#####
		# input errors
		#####

		tg = graph.graph( self.medium_dict )
		self.assertEqual(tg.graph_with_node_removed( 'noelement' ).graph_please(), self.medium_dict, 'Node removal works for nodes that do not exist' )



	def test_list_methods( self ):
		tg = graph.graph( self.large_dict )
		expected_list = [ 'A', 'C' ]
		self.assertCountEqual( tg.neighbours_going_out_list( 'D' ), expected_list, 'neighbours list finds neighbours of D' )
		self.assertCountEqual( tg.neighbours_going_out_list( 'L' ), self.empty_list, 'neighbours list finds neighbours of L - none' )


		#####
		# input errors
		#####
		
		
		self.assertEqual( tg.neighbours_going_out_list( 'Z' ), self.empty_list, 'neighbours_going_out_list() on node that !exist' )
		
	@unittest.skip( "method never used, so stop testing" )
	def test_neighbours_coming_in_list( self ):
		expected_list = [ 'C', 'B', 'F' ]
		self.assertCountEqual( tg.neighbours_coming_in_list( 'D' ), expected_list, 'neighbours list finds those who come to D ' )
		expected_list = [ 'K' ]
		self.assertCountEqual( tg.neighbours_coming_in_list( 'L' ), expected_list, 'neighbours list finds those who come to L ' )
		
		self.assertCountEqual( tg.neighbours_coming_in_list( 'noexist' ), self.empty_list, 'neighbours_coming_in_list() on node that !exist' )

