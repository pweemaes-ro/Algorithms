"""An attempt to solve the connectivity problem.
- If we only need to find out about a pair (p, q) whether it IS connected,
  but NOT HOW it is connected, things get way easier."""
from collections import defaultdict

connections = ((1, 4), (1, 3))
con_infos: dict[int, set[int]] = defaultdict(set)


def check_connection(connection: tuple[int, int]) -> bool:
	p, q = connection
	if (cons := con_infos.get(p)) and q in cons:
		# q already connected to p
		print(f"{p} and {q} are already connected!")
		# if q connected to p, then also p connected to q
		assert p in con_infos[q]
		# if q connected to p, then q also connected to all other connections
		# of p
		for c in con_infos[p]:
			assert c in con_infos[q]
		# if p connected to q, then p also connected to all other connections
		# of p
		for c in con_infos[q]:
			assert c in con_infos[p]
		return True
	else:
		# Not connected yet
		con_infos[p].add(q)
		con_infos[q].add(p)
		return False
	

for connection in connections:
	print(check_connection(connection))
