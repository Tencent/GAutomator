"""
Tencent is pleased to support the open source community by making GAutomator available.
Copyright (C) 2016 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at
http://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" basis, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

"""

__author__ = 'yifengcai'

import sys
import wpyscripts.manager as manager

logger = manager.get_logger()

class Vertex(object):
    # node must implement "==" operator, "__hash__" and "str" operator
    
    def __init__(self, node):
        self.id = node
        self.adjacent = {}  # Vertex object -> (entry, weight)
        
        self.clear()

    def clear(self):
        # Set distance to infinity
        self.distance = sys.maxint
        # Mark unvisited        
        self.visited = False  
        # Predecessor
        self.previous = None

    def add_neighbor(self, neighbor, entry=None, weight=1):
        # neighbor is a Vertex object
        # note!! if there are 2 entries from self to neighbor, only the last one will be recorded
        self.adjacent[neighbor] = (entry, weight)

    def check_neighbor(self, neighbor):
        # neighbor is a Vertex object
        return neighbor in self.adjacent

    def del_neighbor(self, neighbor):
        # neighbor is a Vertex object
        if neighbor in self.adjacent:
            del self.adjacent[neighbor]
        else:
            logger.warn("current vertex %s has no neighbor %s, can not delete it", self, neighbor)

    def get_connections(self):
        return self.adjacent.keys()  

    def get_id(self):
        return self.id

    def get_entry(self, neighbor):
        # neighbor is Vertex
        return self.adjacent[neighbor][0]

    def get_weight(self, neighbor):
        # neighbor is Vertex
        return self.adjacent[neighbor][1]

    def set_distance(self, dist):
        self.distance = dist

    def get_distance(self):
        return self.distance

    def set_previous(self, prev):
        self.previous = prev

    def set_visited(self):
        self.visited = True

    def __str__(self):
        return "Vertex (%s)" % str(self.id)


class Graph(object):
    def __init__(self):
        self.vert_dict = {}     # node -> Vertex object
        self.num_vertices = 0

    def __iter__(self):
        # iterate all Vertex objects
        return iter(self.vert_dict.values())

    def add_vertex(self, node):
        if node not in self.vert_dict:
            self.num_vertices += 1
            new_vertex = Vertex(node)
            self.vert_dict[node] = new_vertex
            return new_vertex
        else:
            logger.warn("node %s already in graph, can not add it", node)
            return self.vert_dict[node]

    def del_vertex(self, node):
        v = self.get_vertex(node)
        if not v:
            logger.warn("node %s not in graph, can not delete it", node)
            return
        
        for i in self:
            if i.check_neighbor(v):
                i.del_neighbor(v)
            
        del self.vert_dict[node]
        self.num_vertices -= 1

    def check_vertex(self, n):
        return n in self.vert_dict
   
    def get_vertex(self, n):
        if n in self.vert_dict:
            return self.vert_dict[n]
        else:
            logger.warn("node %s not in graph, can not get it", n)
            return None

    def add_edge(self, frm, to, entry=None, cost=1):
        # frm, to are nodes
        if frm not in self.vert_dict:
            self.add_vertex(frm)
        if to not in self.vert_dict:
            self.add_vertex(to)

        self.vert_dict[frm].add_neighbor(self.vert_dict[to], entry, cost)
        
    def del_edge(self, frm, to):
        # frm, to are nodes
        if frm not in self.vert_dict:
            return
        
        if to not in self.vert_dict:
            return
        
        self.vert_dict[frm].del_neighbor(self.vert_dict[to])

    def get_vertices(self):
        return self.vert_dict.keys()

    def clear_all_vertices(self):
        for v in iter(self):
            v.clear()
            
    def __str__(self):
        reslist = ["Graph data:"]
        for vertex in self:
            reslist.append("%s, edge %d" % (vertex.get_id(), len(vertex.adjacent)))            
            for conn in vertex.get_connections():
                vid = vertex.get_id()
                wid = conn.get_id()
                entry = vertex.get_entry(conn)
                reslist.append('Edge (%s, %s, entry: %s)'  % (vid, wid, entry))
        
        return "\n".join(reslist)


def dijkstra(aGraph, start, end):
    '''Dijkstra's shortest path
    @note: start, end are Vertices 
    @return: path elements are objects(id)
    '''
    # start and end are Vertex objects
    aGraph.clear_all_vertices()
    
    # Set the distance for the start node to zero 
    start.set_distance(0)

    # Put tuple pair into the priority queue
    unvisited_queue = [(v.get_distance(),v) for v in aGraph]
    heapq.heapify(unvisited_queue)

    while len(unvisited_queue):
        # Pops a vertex with the smallest distance 
        uv = heapq.heappop(unvisited_queue)
        current = uv[1]
        current.set_visited()
        
        if current == end:
            # find end Vertex
            break

        #for next_ in v.adjacent:
        for next_ in current.adjacent:
            # if visited, skip
            if next_.visited:
                continue
            new_dist = current.get_distance() + current.get_weight(next_)
            
            if new_dist < next_.get_distance():
                next_.set_distance(new_dist)
                next_.set_previous(current)
#                 print 'updated : current = %s next_ = %s new_dist = %s' \
#                         %(current.get_id(), next_.get_id(), next_.get_distance())
            else:
#                 print 'not updated : current = %s next_ = %s new_dist = %s' \
#                         %(current.get_id(), next_.get_id(), next_.get_distance())
                pass

        # Rebuild heap
        # 1. Pop every item
        while len(unvisited_queue):
            heapq.heappop(unvisited_queue)
        # 2. Put all vertices not visited into the queue
        unvisited_queue = [(v.get_distance(),v) for v in aGraph if not v.visited]
        heapq.heapify(unvisited_queue)
        
    return _getpath(start, end)

def _getpath(start, end):
    # start, end are Vertices
    # path elements are objects(id)
    path = [end.get_id()]
    
    _shortest(end, path)
    if path[-1] != start.get_id():
        # no reachable path
        return None
    
    return path[::-1]

def _shortest(v, path):
    ''' make shortest path from v.previous'''
    # v is target Vertex object, path is OUTPUT
    
    if v.previous:
        path.append(v.previous.get_id())
        _shortest(v.previous, path)
    return

import heapq


def _test1():
    g = Graph()

    g.add_vertex('a')
    g.add_vertex('b')
    g.add_vertex('c')
    g.add_vertex('d')
    g.add_vertex('e')
    g.add_vertex('f')
    g.add_vertex('x')
    g.add_vertex('y')

    g.add_edge('a', 'b', 'ab')  
    g.add_edge('a', 'c', 'ac')
    g.add_edge('a', 'f', 'af')
    g.add_edge('b', 'c', 'bc')
    g.add_edge('b', 'd', 'bd')
    g.add_edge('c', 'd', 'cd')
    g.add_edge('c', 'f', 'cf')
    g.add_edge('d', 'e', 'de')
    g.add_edge('e', 'f', 'ef')
    g.add_edge('x', 'y', 'xy')

    print(str(g))

            
    path = dijkstra(g, g.get_vertex('a'), g.get_vertex('e')) 
    print('The shortest path : %s' %(path))
    print('Vertex data:')
    for v in g:
        vid = v.get_id()
        print('(%s , is visited %s, distance %d)'  % (vid, v.visited, v.get_distance()))

    
    path = dijkstra(g, g.get_vertex('a'), g.get_vertex('y')) 
    print('The shortest path : %s' %(path))
    print('Vertex data:')
    for v in g:
        vid = v.get_id()
        print('( %s , is visited %s, distance %d)'  % ( vid, v.visited, v.get_distance()))

    
    path = dijkstra(g, g.get_vertex('a'), g.get_vertex('d')) 
    print('The shortest path : %s' %(path))
    print('Vertex data:')
    for v in g:
        vid = v.get_id()
        print('( %s , is visited %s, distance %d)'  % ( vid, v.visited, v.get_distance()))
    print
    
    
    path = dijkstra(g, g.get_vertex('b'), g.get_vertex('a')) 
    print('The shortest path : %s' %(path))
    print('Vertex data:')
    for v in g:
        vid = v.get_id()
        print('( %s , is visited %s, distance %d)'  % ( vid, v.visited, v.get_distance()))

    g.del_edge('c', 'd')
    print(str(g))

    g.del_vertex('c')
    print(str(g))


def _test2():
    g = Graph()

    #g.add_vertex('a')
    #g.add_vertex('b')
    
    print(str(g))

    path = dijkstra(g, g.get_vertex('a'), g.get_vertex('b')) 
    print('The shortest path : %s' %(path))
    print('Vertex data:')
    for v in g:
        vid = v.get_id()
        print('(%s , is visited %s, distance %d)'  % (vid, v.visited, v.get_distance()))


if __name__ == '__main__':
    #_test1()
    _test2()
    
    
