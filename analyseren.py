
import re
import sys
import os
import lib.graph
import logging

logging.basicConfig( level=logging.DEBUG, filename='logs/analyseren.log' )

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
	# This has to be last
	shortest_route_parse = re.search( '^(?P<first_node>\w)(?P<second_node>\w)\s$', command )
	if shortest_route_parse:
		logging.info( 'Parsing a shortest route request' )
		node_1 = shortest_route_parse.group( 'first_node' )
		node_2 = shortest_route_parse.group( 'second_node' )
		sr = graph.shortest_route( node_1, node_2 )
		if sr == []:
			return "NO SUCH ROUTE"
		else:
			return list_for_stdout( sr ) 
			
	
	sho

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
		execute_command( command , my_graph )

