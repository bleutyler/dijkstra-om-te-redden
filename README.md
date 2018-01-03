Take in a weighted graph as input, and analyse shortest routes

USAGE:

analyseren.py route_mappings.in route_requests.in


INPUT:

The first Input file is of the form:

	AB5, BC4, CD8, DC8, DE6, AD5, CE2, EB3, AE7

In this example, from node A to node B it is a distance of 5.  This is a directed graph, so a route from B to A need not exist or be equal to A to B.

Assumptions: 

	Node names can only be 1 letter, case sensitive.  Giving a maximum of 52 possible nodes (A-Za-z)

	Distances are measured in positive integers only

	Input that fails these is ignored.

Second (REQUESTS) file format:

The second input file is the calculations asked to be done on the input.  Each line in the file is a requested calculation and can be of one of the following 
formats:

1.  A list of nodes, outlining a specific route, ending with 'l'.  example: "AED l"
	
	A request for the length of this route, A to E to D.  If no such route exists, 'NO SUCH ROUTE'.  1st and last node can be the same

2.  A pair of nodes, asking for specifics about the possible routes between them.  After the pairing is listed, 
    then a set of characters to ask for something specific betweeen them:

	a.  ' s' asking for the length of the shortest route between the pair.  example: "AC s" wants the shortest route from A to C

	b.  ' <number>s' - Asking for the number of routes with exactly N stops between them.  Example: "AC 4s" wants the number of routes between
		A and C with exactly 4 stops.

	c.  ' <number>d' - Asking for the number of routes with a maximum distance of N.  Example: "CC 30d" wants the number of routes from C to C less than
		or equal to 30.

	d.  ' <number>ms' - similar to case b), but the number is the maximum number of stops.

OUTPUT:

stdout	

each item in the operations file is answered on one line

TEST:

On the command line: 

python -m unittest -v  test/Test*


VERSION HISTORY:

0.2 	- Added testing with unittest
0.2.1 	- expanded tests, strengthened method
0.3	- all tests completed for traingraph object methods - for the sake of brevity, testing is much less formal after this.  
					TestTrainGraph is thoroughly tested, all other testing is adhoc
0.3.1	- added analyseren.py, the main executable
0.4	- traingraph renamed to more generic graph object - lib.graph
0.4.2	- added analyseren.py, the main executable
0.4.3	- analyseren will process graph files and command input files
0.4.4	- analyseren will process shortest route 
0.4.5	- TestAnalyseren.py created, tests shortest route, lib.config created
0.4.6	- all cases added to analyseren
0.4.7	- TestAnalyseren.py updated to match all cases in analyseren.py
0.4.8	- redid methods to better match requirements
0.4.9	- lib.graph.__str__() completed

DESIGN:

2 main parts, first iterate through the first file, generating a 2d array of distances between a pair of node according to the first input file.  
This is the lib.graph() object.  
Then iterate through the second file, giving us the answers we want.

The graph is stored as a 2d list, but it is encapsulated in a object.  THen we have methods on the object to answer question 2b) 2c) and 2d)


TRANSLATIONS

Dutch							English
=====							====
analyseren				 		analyze

dijkstra-om-te-redden 			Dijkstra-to-the-rescue
								https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm
							

TO DO:
had to redo input re-reading requiremnets.  SMALL adjustments to be made to analyseren
clean up repo _pycache_ needs to go
