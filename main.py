DIRS = {"NORTH": (0, 1), "SOUTH": (0, -1), "EAST": (1, 0), "WEST": (-1, 0)}
WALL_BIT = {"NORTH": 1, "EAST": 2, "SOUTH": 4, "WEST": 8}


def wall_at(obs, config, col, row):
    idx = (row - obs.southBound) * config.width + col
    if 0 <= idx < len(obs.walls) and obs.walls[idx] != -1:
        return obs.walls[idx]
    return 0


def has_road(obs, config, col, row, direction):
    return not (wall_at(obs, config, col, row) & WALL_BIT[direction])


def neighbor(col, row, direction):
    dc, dr = DIRS[direction]
    return col + dc, row + dr


def my_robots(obs):
    return {uid: data for uid, data in obs.robots.items() if data[4] == obs.player}


def my_factory(obs):
    for uid, data in my_robots(obs).items():
        if data[0] == 0:
            return uid, data
    return None, None


def parse_cell(key):
    c, r = key.split(",")
    return int(c), int(r)


def factory_bug_north(uid, col, row, jump_cd, obs, config):
    if has_road(obs, config, col, row, "NORTH"):
        return "NORTH"
    if jump_cd == 0:
        return "JUMP_NORTH"
    if has_road(obs, config, col, row, "EAST"):
        return "EAST"
    if has_road(obs, config, col, row, "WEST"):
        return "WEST"
    return "IDLE"


_scout_state = {}


def snail_step(uid, col, row, target, obs, config):
    state = _scout_state.setdefault(uid, {"target": None, "tabu": []})
    if state["target"] != target:
        state["target"] = target
        state["tabu"] = []

    tc, tr = target
    candidates = []
    for direction in ("NORTH", "SOUTH", "EAST", "WEST"):
        if not has_road(obs, config, col, row, direction):
            continue
        nc, nr = neighbor(col, row, direction)
        if (nc, nr) in state["tabu"]:
            continue
        dist = abs(nc - tc) + abs(nr - tr)
        candidates.append((dist, direction))

    if not candidates:
        state["tabu"] = []
        return "IDLE"

    candidates.sort()
    action = candidates[0][1]
    state["tabu"] = (state["tabu"] + [(col, row)])[-2:]
    return action


def scout_action(uid, col, row, energy, factory_pos, obs, config):
    fc, fr = factory_pos
    if energy >= 75:
        for direction in ("NORTH", "SOUTH", "EAST", "WEST"):
            if neighbor(col, row, direction) == (fc, fr) and has_road(obs, config, col, row, direction):
                return f"TRANSFER_{direction}"
        return snail_step(uid, col, row, (fc, fr), obs, config)

    crystals = [parse_cell(key) for key in obs.crystals]
    if crystals:
        target = min(crystals, key=lambda cell: abs(cell[0] - col) + abs(cell[1] - row))
    else:
        target = (col, row + 5)
    return snail_step(uid, col, row, target, obs, config)


def agent(obs, config):
    actions = {}
    robots = my_robots(obs)
    _, f_data = my_factory(obs)

    scout_count = sum(1 for data in robots.values() if data[0] == 1)

    for uid, data in robots.items():
        rtype, col, row, energy = data[0], data[1], data[2], data[3]
        jump_cd = data[6] if len(data) > 6 else 0
        build_cd = data[7] if len(data) > 7 else 0

        if rtype == 0:
            if scout_count == 0 and build_cd == 0 and energy >= config.scoutCost:
                actions[uid] = "BUILD_SCOUT"
            else:
                actions[uid] = factory_bug_north(uid, col, row, jump_cd, obs, config)
        elif rtype == 1 and f_data is not None:
            factory_pos = (f_data[1], f_data[2])
            actions[uid] = scout_action(uid, col, row, energy, factory_pos, obs, config)

    return actions
