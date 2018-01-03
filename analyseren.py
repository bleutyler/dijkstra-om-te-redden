
import re
import sys
import os
import lib.graph
import logging
import lib.config

logging.basicConfig( level=logging.DEBUG, filename='logs/analyseren.log' )
NO_ROUTE_TO_USER_STRING = 'NO SUCH ROUTE'

def read_in_graph_file_and_operations_file_and_output_results( graph_file, operations_file ):
	pass

def get_graph_from_file( graph_file ):
	logging.debug( 'Loading file: ' + str( graph_file ) )
	if isinstance( graph_file, str) and os.path.exists( graph_file ):
		file_h = open( graph_file )
		graph_data_raw = str( file_h.read() )
		temp_graph = lib.graph.graph()
		for edge_raw in graph_data_raw.split( ', ' ):
			proper_edge_parse = re.search( '(?P<first>\w)(?P<second>\w)(?P<distance>\d+)', edge_raw )
			if not proper_edge_parse == None:
				node_1   = str( proper_edge_parse.group( 'first' ) )
				node_2   = str( proper_edge_parse.group( 'second' ) )
				distance = int( proper_edge_parse.group( 'distance' ) )
				
				temp_graph.put_edge( node_1, node_2, distance )
				logging.debug( 'added ' + node_1 + ', ' + node_2 + ' to value ' + str( distance ) )
			else:
				logging.warn( 'Incorrect Edge input from file (' + graph_file + ') : ' + edge_raw )
		logging.info( 'Gathered graph: ' + str( temp_graph.graph_please() ) )
		return temp_graph
	else:
		print( 'Graph File ' + str( graph_file ) + ' not found.' )
		sys.exit( 1 )

def execute_command( command, graph ):
	logging.debug( 'Parsing command: "' + str( command ) + '"')
	max_stops_parse      = re.search( '^(?P<first_node>\w)(?P<second_node>\w) (?P<number>\d+)ms\s*$', command )
	max_distance_parse   = re.search( '^(?P<first_node>\w)(?P<second_node>\w) (?P<number>\d+)d\s*$', command )
	exact_stops_parse    = re.search( '^(?P<first_node>\w)(?P<second_node>\w) (?P<number>\d+)s\s*$', command )
	route_length_parse   = re.search( '^(?P<nodes>\w+) l\s*$', command )
	shortest_route_parse = re.search( '^(?P<first_node>\w)(?P<second_node>\w)\s*$', command )

	if max_stops_parse:
		# 6. The number of trips starting at C and ending at C with a maximum of 3 stops.
		logging.debug( 'Parsing a maximum route request' )
		node_1 		= max_stops_parse.group( 'first_node' )
		node_2 		= max_stops_parse.group( 'second_node' )
		maximum_stops 	= int( max_stops_parse.group( 'number' ) )
		all_routes = graph.calculate_all_routes( node_1, node_2 )

		if all_routes == None:
			return lib.config.NO_ROUTE_TO_USER_STRING

		return_list = []
		for route in all_routes:
			if len( route ) <= maximum_stops:
				return_list.append( route )
		
		if return_list == []:
			return lib.config.NO_ROUTE_TO_USER_STRING
		else:
			return str( len( return_list ) )
		
	elif exact_stops_parse:
		# 7. The number of trips starting at A and ending at C with exactly 4 stops.  
		logging.debug( 'Parsing an exact X stops route request' )
		node_1 		= exact_stops_parse.group( 'first_node' )
		node_2 		= exact_stops_parse.group( 'second_node' )
		num_stops 	= int( exact_stops_parse.group( 'number' ) )
		all_routes = graph.calculate_all_routes( node_1, node_2 )

		if all_routes == None:
			return lib.config.NO_ROUTE_TO_USER_STRING

		return_list = []
		for route in all_routes:
			if len( route ) == num_stops:
				return_list.append( route ) 
		
		if return_list == []:
			return lib.config.NO_ROUTE_TO_USER_STRING
		else:
			return str( len( return_list ) )

	elif route_length_parse:
		# 5. The distance of the route A-E-D
		logging.debug( 'Parsing a route length request command on :' + command )
		# nodes_list = route_length_parse.group( 'nodes' ).split( '' )
		logging.debug( 'Making a list on :' + str( command[0:-2] ) )
		nodes_list = list( command[0:-2] )
		logging.debug( 'The routes list is: ' + str( nodes_list ) )
		if graph.route_exists( nodes_list ):
			logging.debug( 'The route exists: ' + str( nodes_list ) )
			return str( graph.distance( nodes_list ) )
		else:
			logging.debug( 'The was foudn not to exist! '  )
			return lib.config.NO_ROUTE_TO_USER_STRING

	elif max_distance_parse: 
		# 10. The number of different routes from C to C with a distance of less than 30.
		logging.debug( 'Parsing a max distance route request' )
		node_1 		= max_distance_parse.group( 'first_node' )
		node_2 		= max_distance_parse.group( 'second_node' )
		distance  	= int( max_distance_parse.group( 'number' ) )
		all_routes = graph.calculate_all_routes( node_1, node_2 )

		if all_routes == None:
			return lib.config.NO_ROUTE_TO_USER_STRING
			
		return_routes = []
		for route in all_routes:
			if graph.distance( route ) <= distance:
				return_routes.append( route )
		
		if return_routes == []:
			return lib.config.NO_ROUTE_TO_USER_STRING
		else:
			return str( len( return_routes ) )

	elif shortest_route_parse:
		# 9. The length of the shortest route (in terms of distance to travel) from B to B.
		logging.debug( 'Parsing a shortest route request' )
		node_1 = shortest_route_parse.group( 'first_node' )
		node_2 = shortest_route_parse.group( 'second_node' )
		sr = graph.shortest_route( node_1, node_2 )
		
		if sr == []:
			return lib.config.NO_ROUTE_TO_USER_STRING
		else:
			return str( graph.distance( sr ) )
	else:
		return 'Unknown Command: ' + str( command )
		

def list_for_stdout( list ):
	list_as_a_string = "" 
	for item in list:
		list_as_a_string = list_as_a_string + str( item )
	return list_as_a_string


if __name__ == '__main__':
	if len(sys.argv) < 3:
		print( 'Usage: ' + sys.argv[0] + ' graph_file operations_file' )
		sys.exit( 1 )
		
	my_graph = get_graph_from_file( sys.argv[1] )
	logging.info( 'Loaded graph: ' + str( my_graph.graph_please() ) )

	operations_file = sys.argv[2]
	operations = []
	if isinstance( operations_file, str ) and os.path.exists( operations_file ):
		file_h = open( operations_file, 'r' )
		operations = file_h.readlines()
	else:
		print( 'Operations File ' + str( operations_file ) + ' not found.' )
		sys.exit( 1 )
	
	for command in operations:
		print( execute_command( command , my_graph ))
		

