# # # # # # # # # # # # # # # # # # # # # # # #
__author__ = "Tyler Slijboom"
__copyright__ = "Copyright 2017, PI Solutions"
__credits__ = ["BMO Bank"]
__license__ = "GPL"
__version__ = "0.2.1"
__email__ = "bleutylerplusplus@gmail.com"
__status__ = "Development"

# todo:
#			
# nice to have:
#			new traingraph object maybe packed nicer?   piweb.graph because there must be better names / data structures
# # # # # # # # # # # # # # # # # # # # # # # #


#import graph
import logging
import copy

logging.basicConfig( level=logging.INFO, filename='logs/graph.log' )

class graph:

	def __init__( self, new_edges={} ):
		self.edges_dictionary = {}
		if isinstance( new_edges, dict ):
			for key_1 in new_edges.keys():
				self.edges_dictionary[ key_1 ] = {}
				if isinstance( new_edges[ key_1 ], dict ):
					for key_2 in new_edges[ key_1 ].keys():
						value = new_edges[ key_1 ][ key_2 ]
						if isinstance( value, int ):
							self.edges_dictionary[ key_1 ][ key_2 ] = value
						else:
							logging.warning( 'Value [' + key_1 + '][' + key_2 + '] is not an int.  it is type: ' + str( type( value ) ) )
				else:
					logging.warning( 'Value [' + key_1 + '] is not a dict.  it is type: ' + str( type( new_edges[ key_1 ] ) ) )
					
		else:
			logging.warning( 'Item passed in was not a dictionary' )
			
	def shortest_route( self, first_node, second_node ):
		all_routes = self.calculate_all_routes( first_node, second_node )
		current_shortest_route = []
		
		if all_routes == None:
			return []

		for current_route in all_routes:	
			if len( current_shortest_route ) == 0: 
				current_shortest_route = current_route
			else:
				if self.distance( current_route ) < self.distance( current_shortest_route ):
					current_shortest_route = current_route 
				else:
					next
						  
		return current_shortest_route



	def route_exists( self, route=[] ):
		if not isinstance( route, list ) or len( route ) <= 1:
			return False

		start = route[0]
		for end in route[1:]:
			if self.edge_exists( start, end ):
				start = end
			else:
				return False

		return True

	def distance( self, route=[] ):
		if not self.route_exists( route ):
			return 0

		distance_measured = 0
		start = route[0]
		for end in route[1:]:
			# if you still get NoneType here there the check at teh start fails
			current_step_length = self.get_edge( start, end )
			if current_step_length == None:
				return 0

			start = end
			distance_measured = distance_measured + current_step_length
		
		return distance_measured
			


	def put_edge( self, node_1, node_2, value ):		
		# check for is int and in string
		if not isinstance( node_1, str ) or not isinstance( node_2, str ) or not isinstance( value, int ):
			return
		if node_1 in self.edges_dictionary:
			pass
		else:
			self.edges_dictionary[ node_1 ] = {}

		self.edges_dictionary[ node_1 ][ node_2 ] = value
	
	def put( self, node_1, node_2, value ):
		self.put_edge( node_1, node_2, value )

	def edge_exists( self, node_1, node_2 ):
		if node_1 in self.edges_dictionary:
			if node_2 in self.edges_dictionary[ node_1 ]:
				return True

		return False
		

	def get_edge( self, node_1, node_2 ):
		if self.edge_exists( node_1, node_2 ):
			return self.edges_dictionary[ node_1 ][ node_2 ]
		else:
			return None

	def graph_with_node_removed( self, node ):
		dict = self.graph_please()
		if node in dict:
			del dict[ node ]
		
		for other_node in self.edges_dictionary.keys():
			if self.edge_exists( other_node, node ):
				del dict[ other_node ][ node ]
		return graph( dict )

	def __str__( self ):
		return_string = ''
		for first_level in self.edges_dictionary.keys():
			if return_string == '':
				return_string = first_level + ' : ' + str( self.edges_dictionary[ first_level ] )
			else:
				return_string = return_string + ", " + first_level + ' : ' + str( self.edges_dictionary[ first_level ] )
		
		return return_string


	def graph_please( self ):
		return copy.deepcopy( self.edges_dictionary )

	def calculate_all_routes( self, first_node, second_node ):
		list_of_routes = []
		logging.debug( 'all_routes(): ENTER' )

		if not isinstance( first_node, str ) or not isinstance( second_node, str ):
			return None

		if self.edge_exists( first_node, second_node ):
			logging.debug( 'all_routes(): exists direct ' + first_node + ' -> ' + second_node )
			list_of_routes.append( [ first_node, second_node ] )

		# use dijkstra's on this until you get them all 

		neighbours = self.neighbours_going_out_list( first_node )
		if neighbours == []:
			# there are no edges leaving the first_node, so we are done here
			return None
		else:
			logging.debug( 'all_routes(): looking for paths from neighbours of ' + first_node )
			for node in neighbours:
				if node == second_node:
					logging.debug( 'all_routes(): Do not go into sub trees now!' )
					continue
				temp_route = [ node ]
				# This should remove the node iff first_node != second_node
				temp_edges_map = {}
				if first_node == second_node:
					temp_edges_map = graph( self.graph_please() )
				else:
					temp_edges_map = self.graph_with_node_removed( first_node )
				logging.debug( 'all_routes(): looking for path from ' + node + ' to ' + second_node + ' in tree: ' + str( temp_edges_map.graph_please() ) )

				routes_from_neighbour_to_the_end = temp_edges_map.calculate_all_routes( node, second_node )
				if routes_from_neighbour_to_the_end == None:
					logging.debug( 'all_routes(): no routes from neighbour : ' + node + ' to end_node: ' + second_node )
					next
				else:
					for neighbour_route in routes_from_neighbour_to_the_end:	
						if not neighbour_route == None:
							temp_route = [ first_node ]
							temp_route.extend( neighbour_route )
							list_of_routes.append( temp_route )
							logging.debug( 'all_routes(): found and added: ' + str( temp_route ) )

		if len( list_of_routes ) == 0:
			logging.debug( 'all_routes(): END - There is no route from ' + first_node + ' to ' + second_node + ' in the tree: ' + str( self.graph_please() )  )
			return None

		logging.debug( 'all_routes(): END - I am returning: ' + str( list_of_routes ) )
		return list_of_routes


	def neighbours_going_out_list( self, node ):
		if node in self.edges_dictionary:
			return_list = []
			for neigh in self.edges_dictionary[ node ]:
				return_list.append( neigh )

			return return_list
		return []

	def return_routes_within_x_stops( self, node_1, node_2, max_stops ):
		return_list = []
		if max_stops <= 0:
			return []

		if self.edge_exists( node_1, node_2 ):
			logging.debug( 'distance() it was low enough, so add that as a possible route.' )
			if max_stops == 1:
				return_list.append( [ node_1, node_2 ] )

			logging.debug( 'max_stops() check for other routes from ' + node_2 + ' to ' + node_2 + ' with max stops < ' + str(max_stops - 1) )
			sub_lists = self.return_routes_within_x_stops( node_2, node_2, max_stops - 1 )
			if sub_lists != []:
				logging.debug( 'Wow!  found loops to ' + node_2 + ' after already connecting, so add them as a route' ) 
				for route in sub_lists:
					temp_route = [ node_1 ]
					temp_route.extend( route )
					return_list.append( temp_route )

		# find neighbours a distance away
		neighbours = self.neighbours_going_out_list( node_1 )
		if neighbours == []:
			# there are no edges leaving the first_node, so we are done here
			return []
		else:
			for node in neighbours:
				if node == node_2:
					# already handled this above
					continue

				sub_lists = self.return_routes_within_x_stops( node, node_2, max_stops - 1 )

				if sub_lists != []:
					for route in sub_lists:
						temp_route = [ node_1 ]
						temp_route.extend( route )
						return_list.append( temp_route )

		return return_list

	def return_routes_travelling_maximum_distance( self, node_1, node_2, max_distance ):
		return_list = []
		if max_distance <= 0:
			logging.debug( 'want to travel a distance of ' + str( max_distance ) + ' so return empty' )
			return []

		if self.edge_exists( node_1, node_2 ):
			distance          = self.edges_dictionary[node_1][node_2]
			logging.debug( 'distance() travelled a distance of ' + str( distance ) + ' DIRECTLY from ' + node_1 + ' to ' + node_2 )
			if distance < max_distance:
				logging.debug( 'distance() it was low enough, so add that as a possible route.' )
				return_list.append( [ node_1, node_2 ] )
				logging.debug( 'distance() check for other routes from ' + node_2 + ' to ' + node_2 + ' with distance < ' + str(max_distance - distance) )
				sub_lists = self.return_routes_travelling_maximum_distance( node_2, node_2, max_distance - distance )
				if sub_lists != []:
					logging.debug( 'Wow!  found loops to ' + node_2 + ' after already connecting, so add them as a route' ) 
					for route in sub_lists:
						temp_route = [ node_1 ]
						temp_route.extend( route )
						return_list.append( temp_route )
			else:
				pass

		# find neighbours a distance away
		neighbours = self.neighbours_going_out_list( node_1 )
		if neighbours == []:
			# there are no edges leaving the first_node, so we are done here
			return []
		else:
			for node in neighbours:
				if node == node_2:
					# already handled this above
					continue

				distance = self.edges_dictionary[ node_1 ][ node ]
				sub_lists = self.return_routes_travelling_maximum_distance( node, node_2, max_distance - distance )

				if sub_lists != []:
					for route in sub_lists:
						temp_route = [ node_1 ]
						temp_route.extend( route )
						return_list.append( temp_route )

		return return_list

#	def neighbours_coming_in_list( self, node ):
#		return_list = []
#		for tempnode in self.graph_please().keys():
#			if self.edge_exists( tempnode, node ):
#				return_list.append( tempnode )
#
#		if len( return_list ) == 0:
#			return None
#		
#		return return_list

