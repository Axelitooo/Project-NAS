Class LinksGraph

	def __init__(self, RouteurGraph): 
        self.routers = RouteurGraph
        self.graph = [[0 for column in range(RouteurGraph)]  
                    for row in range(RouteurGraph)] 

	""" """
	def dijkstra(self, source_router):
		dist = [self.routers] * [self.routers]
		for 

		dist[source_router] = 0

			

