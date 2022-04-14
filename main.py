from dataclasses import dataclass, field
from enum import Enum


class CallState(Enum):
    EXPLORING = 0
    FINISHED = 1


@dataclass
class Vertex:
    id: str = "-"
    d: int = -1
    f: int = -1
    pred: object = None
    adj: list = field(default_factory=list)
    visited: bool = False

    def reset(self):
        self.d: int = -1
        self.f: int = -1
        self.pred: object = None
        self.visited: bool = False


time = 0


def dfs_rec(vertices):
    def dfs_visit(u):
        global time
        time += 1
        u.d = time
        u.visited = True

        for v in u.adj:
            if not v.visited:
                v.pred = u
                dfs_visit(v)

        time += 1
        u.f = time

    for v in vertices:
        if not v.visited:
            dfs_visit(v)


def dfs_iter(vertices):
    _time = 0
    call_stack = []
    for s in vertices:
        if not s.visited:
            _time += 1
            s.d = _time
            s.visited = True
            call_stack.append((s, 0, CallState.EXPLORING))

            while len(call_stack) > 0:
                u, index, call_state = call_stack.pop()
                if call_state == CallState.FINISHED:
                    _time += 1
                    u.f = _time
                else:

                    if index < len(u.adj):
                        call_stack.append((u, index + 1, CallState.EXPLORING))
                        v = u.adj[index]
                        if not v.visited:
                            v.pred = u
                            v.visited = True
                            _time += 1
                            v.d = _time
                            call_stack.append((v, 0, CallState.EXPLORING))
                    else:
                        call_stack.append((u, index, CallState.FINISHED))


def dfs_iter_no_time(vertices):
    stack = []
    _time = 0
    for s in vertices:
        if not s.visited:
            stack.append(s)

            while len(stack) > 0:
                u = stack.pop()
                print(u.id, end=", ")
                _time += 1
                u.d = _time

                for v in u.adj:
                    if not v.visited:
                        v.visited = True
                        stack.append(v)


if __name__ == "__main__":
    v1 = Vertex("u", -1, -1, None, [], False)
    v2 = Vertex("v", -1, -1, None, [], False)
    v3 = Vertex("w", -1, -1, None, [], False)
    v4 = Vertex("x", -1, -1, None, [], False)
    v5 = Vertex("y", -1, -1, None, [], False)
    v6 = Vertex("z", -1, -1, None, [], False)

    v1.adj += [v2, v4]
    v2.adj += [v5]
    v3.adj += [v5, v6]
    v4.adj += [v2]
    v5.adj += [v4]
    v6.adj += [v6]

    vertices = [v1, v2, v3, v4, v5, v6]

    dfs_rec(vertices)

    print("dfs recursive:")
    for v in vertices:
        print(f'{v.id}: {v.d}, {v.f}')

    [v.reset() for v in vertices]

    dfs_iter(vertices)

    print("dfs iterative")
    for v in vertices:
        print(f'{v.id}: {v.d}, {v.f}')