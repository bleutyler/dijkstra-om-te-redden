
import re
import sys
import os
import lib.graph

def read_in_graph_file_and_operations_file_and_output_results( graph_file, operations_file ):


if __name__ = '__main__':
	graph_file 		= argv[0]
	operations_file = argv[1]
	
	if not os.path.exists( graph_file ):
		print( 'File ' + graph_file + ' not found.' )
		sys.exit( 1 )

	if not os.path.exists( operations_file ):
		print( 'File ' + operations_file + ' not found.' )
		sys.exit( 1 )
	
	read_in_graph_file_and_operations_file_and_output_results( graph_file, operations_file )