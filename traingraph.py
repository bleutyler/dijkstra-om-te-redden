#
#
#
#

class traingraph:

	def __init__( self, new_edges={} ):
		self.edges_dictionary = new_edges

	def calculate_shortest_route( self, first_node, second_node ):
		if self.exists( first_node, second_node ):
			return self.get( first_node, second_node )
		else:
			# use dijkstra's on this until you get to the node we want
			if first_node == second_node:
				# neighbours = the list of nodes next to first_node
				# for each node in that list
				# subLoop = calculate_shortest_route( neighbour, second_node )
				# return the shortest routes from [first_node][neighbour] + subLoop
				pass

			else:
				# neighbours of first_node
				# new_edges = self.return_sub_graph_with_node_removed()
				# return new_edges.calculate_shortest_route( neighbour, second_node )
				# if no_neighbours:
				# return 'None'
				pass

		return None

	def put( self, node_1, node_2, value ):
		if node_1 in self.edges_dictionary:
			pass
		else:
			self.edges_dictionary[ node_1 ] = {}
		self.edges_dictionary[ node_1 ][ node_2 ] = value
	
	def exists( self, node_1, node_2 ):
		if node_1 in self.edges_dictionary:
			if node_2 in self.edges_dicionary[ node_1 ]:
				return True

		return False
		

	def get( self, node_1, node_2 ):
		if self.exists( node_1, node_2 ):
			return self.edges_dictionary[ node_1 ][ node_2 ]
		else:
			return None

	def return_sub_graph_with_node_removed( self, node_to_delete ):
		# iterate through unique edges
		pass

	def return_list_of_unique_nodes( self ):
		pass

	#def calculate_number_of_stops_between( self, first_node, second_node ):
	#	pass

	def calculate_all_routes( self, first_node, second_node ):
		pass

	def neighbours_list( self, node ):
		if node in self.edges_dictionary:
			return_list = []
			for neigh in self.edges_dictionary[ node ]:
				return_list.append( neigh )

			return return_list
		return []
