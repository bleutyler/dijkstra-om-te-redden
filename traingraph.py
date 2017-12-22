#
#
#
#

class traingraph:

	def __init__( self, new_edges={} ):
		self.edges_dictionary = new_edges

	def calculate_shortest_route( self, first_node, second_node ):
		if first_node in self.edges_dictionary and second_node in self.edges_dictionary[ first_node ]:
			return self.edges_dictionary[ first_node ][ second_node ]
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


	def return_sub_graph_with_node_removed( self, node_to_delete ):
		# iterate through unique edges
		pass

	def return_list_of_unique_nodes( self ):
		pass

	def calculate_number_of_stops_between( self, first_node, second_node ):
