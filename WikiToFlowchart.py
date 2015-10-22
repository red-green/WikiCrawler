from graph_tool.all import *
import sqlite3

conn = sqlite3.connect('wiki.db')

g = Graph()

vertexes_names = g.new_vertex_property("string")
vertexes = {}

c = conn.cursor()
c.execute('SELECT * FROM connections')
ucon = c.fetchall()

lastlevel = ['Philosophy']
nextlevel = []

pcon = []

while lastlevel != []: # 100 iterations
	for i in ucon:
		if i[1] in lastlevel:
			nextlevel.append(i[0])
			pcon.append(i)
	lastlevel = nextlevel
	nextlevel = []

def proc(t): # converts to acronym if too long
	if len(t) > 15:
		return t[:15]
		#return '.'.join(i[0] for i in t.split()) + '.'
	return t

for start, stop in pcon:
	if start == '' or stop == '':
		continue
	if start not in vertexes:
		vertexes[start] = g.add_vertex()
		vertexes_names[vertexes[start]] = proc(start)
	if stop not in vertexes:
		vertexes[stop] = g.add_vertex()
		vertexes_names[vertexes[stop]] = proc(stop)
	g.add_edge(vertexes[start], vertexes[stop])

graph_tool.stats.remove_parallel_edges(g)
pos = None
pos = graph_tool.draw.radial_tree_layout(g,vertexes['Philosophy'])
#pos = graph_tool.draw.sfdp_layout(g)
graph_draw(g, pos=pos, vertex_size=1, edge_pen_width=10, vertex_text=vertexes_names, vertex_font_size=14, output="output.png", output_size=(8000, 8000))
