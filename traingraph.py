#
#
#
#


import traingraph
import logging

class traingraph:

	def __init__( self, new_edges={} ):
		self.edges_dictionary = {}
		for key_1 in new_edges.keys():
			self.edges_dictionary[ key_1 ] = {}
			for key_2 in new_edges[ key_1 ].keys():
				self.edges_dictionary[ key_1 ][ key_2 ] = new_edges[ key_1 ][ key_2 ]
					

	def shortest_route( self, first_node, second_node ):
		current_shortest_route = []
		##### print( 'shortest(): ENTER' )
		if self.edge_exists( first_node, second_node ):
			##### print( 'shortest(): exists direct ' + first_node + ' -> ' + second_node )
			current_shortest_route = [ first_node, second_node ]

		# use dijkstra's on this until you get to the node we want

		neighbours = self.neighbours_going_out_list( first_node )
		if neighbours == []:
			# there are no edges leaving the first_node
			pass # we don't return None here, at the end of all the conditionals we return current_shortest_route
		else:
			for node in neighbours:
				##### print( 'shortest(): exploring neighbour ' + node + ' in chain ' + first_node + ' -> ' + second_node )
				temp_route = [ node ]
				temp_edges_map = self.graph_with_node_removed( first_node )
				##### print( 'shortest():      looking in tree: ' + str( temp_edges_map.get_copy_of_edges() ) )

				temp_short_route = temp_edges_map.shortest_route( node, second_node )
				if temp_short_route == None:
					##### print( 'shortest(): no route found with the neighbour: ' + node + ' to end_node: ' + second_node )
					next
				else:
					temp_route = [ first_node ]
					temp_route.extend( temp_short_route )

				if self.route_exists( temp_route ):
					if len( current_shortest_route ) == 0: 
						##### print( 'shortest(): found first shortest non-direct route: ' + str( temp_route ) ) 
						current_shortest_route = temp_route
					else:
						if self.distance( temp_route ) < self.distance( current_shortest_route ):
							##### print( 'shortest(): found NEW shortest route: ' + str( temp_route ) ) 
							current_shortest_route = temp_route
						else:
							next
							##### print( 'shorest(): found a route ' + node + ' -> ' + second_node + ' but it was NOT shortest' )
							  
				else:
					# route does not exist, 
					##### print( 'shortest(): no route found with the neighbour: ' + node + ' to end_node: ' + second_node )
					pass

		if len( current_shortest_route ) == 0:
			##### print( 'There is no route from ' + first_node + ' to ' + second_node + ' in the tree: ' + str( self.get_copy_of_edges() )  )
			return None

		##### print( 'shortest(): END - I am returning: ' + str( current_shortest_route ) )
		return current_shortest_route



	def route_exists( self, route=[] ):
		if len( route ) <= 1:
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
			return None

		distance_measured = 0
		start = route[0]
		for end in route[1:]:
			# if you still get NoneType here there the check at teh start fails
			current_step_length = self.get_edge( start, end )
			if current_step_length == None:
				return None

			start = end
			distance_measured = distance_measured + current_step_length
		
		return distance_measured
			


	def put_edge( self, node_1, node_2, value ):
		# check for is int and in string
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
		dict = self.get_copy_of_edges()
		if node in dict:
			del dict[ node ]
		
		for other_node in self.edges_dictionary.keys():
			if self.edge_exists( other_node, node ):
				del dict[ other_node ][ node ]
		return traingraph( dict )

	def graph( self ):
		return self.edges_dictionary.copy()

	def return_list_of_unique_nodes( self ):
		pass

	#def calculate_number_of_stops_between( self, first_node, second_node ):
	#	pass

	def get_copy_of_edges( self ):
		dict = {}
		for key_1 in self.edges_dictionary.keys():
			dict[ key_1 ] = {}
			for key_2 in self.edges_dictionary[ key_1 ]:
				dict[ key_1 ][ key_2 ] = self.get_edge( key_1 , key_2 )
		return dict

		
	def calculate_all_routes( self, first_node, second_node ):
		list_of_routes = []
		#current_route  = []
		print( 'all_routes(): ENTER' )
		if self.edge_exists( first_node, second_node ):
			print( 'all_routes(): exists direct ' + first_node + ' -> ' + second_node )
			list_of_routes.append( [ first_node, second_node ] )

		# use dijkstra's on this until you get them all 

		neighbours = self.neighbours_going_out_list( first_node )
		if neighbours == []:
			# there are no edges leaving the first_node, so we are done here
			return None
		else:
			for node in neighbours:
				print( 'all_routes(): exploring neighbour ' + node + ' in chain ' + first_node + ' -> ' + node + ' -> ... -> '  + second_node )
				temp_route = [ node ]
				temp_edges_map = self.graph_with_node_removed( first_node )
				print( 'all_routes():      looking in tree: ' + str( temp_edges_map.get_copy_of_edges() ) )

				routes_from_neighbour = temp_edges_map.calculate_all_routes( node, second_node )
				if routes_from_neighbour == None:
					print( 'all_routes(): no routes from neighbour : ' + node + ' to end_node: ' + second_node )
					next
				else:
					for neighbour_route in routes_from_neighbour:	
						if not neighbour_route == None:
							temp_route = [ first_node ]
							temp_route.extend( neighbour_route )
							list_of_routes.append( temp_route )
							print( 'all_routes(): found and added: ' + str( temp_route ) )

		if len( list_of_routes ) == 0:
			print( 'all_routes(): END - There is no route from ' + first_node + ' to ' + second_node + ' in the tree: ' + str( self.get_copy_of_edges() )  )
			return None

		print( 'all_routes(): END - I am returning: ' + str( list_of_routes ) )
		return list_of_routes 


	def neighbours_going_out_list( self, node ):
		if node in self.edges_dictionary:
			return_list = []
			for neigh in self.edges_dictionary[ node ]:
				return_list.append( neigh )

			return return_list
		return []

	def neighbours_coming_in_list( self, node ):
		return_list = []
		for tempnode in self.graph().keys():
			if self.edge_exists( tempnode, node ):
				return_list.append( tempnode )

		if len( return_list ) == 0:
			return None
		
		return return_list

