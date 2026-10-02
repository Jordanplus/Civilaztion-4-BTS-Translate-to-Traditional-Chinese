import os
import re
from collections import defaultdict, deque

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WBSAVE_PATH = os.path.join(ROOT, "patch", "PatchFiles", "Beyond the Sword", "PublicMaps", "The Earth Ultra (180x90).CivBeyondSwordWBSave")

def audit():
    print(f"Loading map for Cartographic Audit: {WBSAVE_PATH}")
    with open(WBSAVE_PATH, "r", encoding="utf-8") as f:
        text = f.read()

    plot_blocks = re.findall(r"BeginPlot\s+(.*?)\s+EndPlot", text, re.DOTALL)
    plots = {}
    grid_w = 180
    grid_h = 90

    for p in plot_blocks:
        lines = [l.strip() for l in p.split("\n")]
        coords = [l for l in lines if l.startswith("x=")][0].split(",")
        x = int(coords[0].split("=")[1])
        y = int(coords[1].split("=")[1])
        pt = int([l for l in lines if l.startswith("PlotType=")][0].split("=")[1])
        tt = [l for l in lines if l.startswith("TerrainType=")][0].split("=")[1]
        b = [l.split("=")[1] for l in lines if l.startswith("BonusType=")]
        f_type = [l.split("=")[1].split(",")[0] for l in lines if l.startswith("FeatureType=")]
        rn = any("isNOfRiver" in l for l in lines)
        rw = any("isWOfRiver" in l for l in lines)
        rwe = [int(l.split("=")[1]) for l in lines if l.startswith("RiverWEDirection=")]
        rns = [int(l.split("=")[1]) for l in lines if l.startswith("RiverNSDirection=")]

        plots[(x, y)] = {
            "pt": pt, "tt": tt, "b": b[0] if b else None, "f": f_type[0] if f_type else None,
            "rn": rn, "rw": rw, "rwe": rwe[0] if rwe else 0, "rns": rns[0] if rns else 0
        }

    print(f"Total plots loaded: {len(plots)}")

    # =========================================================================
    # 1. COASTLINE & OCEAN TRANSITION AUDIT
    # =========================================================================
    print("\n" + "="*70)
    print("1. 海岸線與海洋過渡審查 (Coastline & Ocean Transitions)")
    print("="*70)

    ocean_adj_to_land = []
    floating_coasts = []
    isolated_water_holes = []
    isolated_land_dots = []

    for (x, y), p in plots.items():
        is_water = (p["pt"] == 3)
        # Check 8 neighbors
        adj_land_count = 0
        adj_water_count = 0
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0: continue
                nx, ny = (x + dx) % grid_w, y + dy
                if 0 <= ny < grid_h:
                    np = plots[(nx, ny)]
                    if np["pt"] in [0, 1, 2]:
                        adj_land_count += 1
                    else:
                        adj_water_count += 1

        # Check deep ocean directly adjacent to land
        if is_water and p["tt"] == "TERRAIN_OCEAN" and adj_land_count > 0:
            ocean_adj_to_land.append((x, y, adj_land_count))

        # Check floating coast in middle of deep ocean with 0 adjacent land
        if is_water and p["tt"] == "TERRAIN_COAST" and adj_land_count == 0:
            # Check 2-tile radius
            land_2tile = 0
            for dx2 in range(-2, 3):
                for dy2 in range(-2, 3):
                    nx2, ny2 = (x + dx2) % grid_w, y + dy2
                    if 0 <= ny2 < grid_h and plots[(nx2, ny2)]["pt"] in [0, 1, 2]:
                        land_2tile += 1
            if land_2tile == 0:
                floating_coasts.append((x, y))

        # Check isolated water holes (1 water plot surrounded by 8 land)
        if is_water and adj_land_count == 8:
            isolated_water_holes.append((x, y))

        # Check isolated land dots (1 land plot surrounded by 8 water)
        if not is_water and adj_water_count == 8:
            isolated_land_dots.append((x, y))

    print(f"[*] 深海直接貼陸地 (TERRAIN_OCEAN adjacent to Land): {len(ocean_adj_to_land)} 處")
    if ocean_adj_to_land:
        sample = ocean_adj_to_land[:15]
        print(f"    範例地塊: {sample}")

    print(f"[*] 遠洋孤立淺海 (Floating Coast with no land within 2 tiles): {len(floating_coasts)} 處")
    if floating_coasts:
        print(f"    範例地塊: {floating_coasts[:10]}")

    print(f"[*] 陸地單格水窪 (1-tile Water Hole surrounded by 8 land plots): {len(isolated_water_holes)} 處")
    if isolated_water_holes:
        print(f"    座標: {isolated_water_holes}")

    print(f"[*] 海洋單格孤島 (1-tile Land Dot surrounded by 8 water plots): {len(isolated_land_dots)} 處")
    if isolated_land_dots:
        print(f"    座標: {isolated_land_dots}")

    # =========================================================================
    # 2. RIVER TOPOLOGY & INTEGRITY AUDIT
    # =========================================================================
    print("\n" + "="*70)
    print("2. 河流網絡拓撲與走向審查 (River Network Integrity & Flow Directions)")
    print("="*70)

    # In Civ4:
    # A plot at (x, y) has:
    # - isNOfRiver: River on the NORTH edge of plot (x, y). That is the segment between vertex (x, y+1) and (x+1, y+1).
    #   rwe: 1 = East (from (x, y+1) to (x+1, y+1)), 3 = West (from (x+1, y+1) to (x, y+1))
    # - isWOfRiver: River on the WEST edge of plot (x, y). That is the segment between vertex (x, y) and (x, y+1).
    #   rns: 0 = North (from (x, y) to (x, y+1)), 2 = South (from (x, y+1) to (x, y))

    # Let's collect all river edges as pairs of vertices: (v1, v2)
    # Vertex coordinates are (vx, vy) where 0 <= vx <= grid_w, 0 <= vy <= grid_h.
    # An edge between v1 and v2.
    river_edges = []
    edges_by_vertex = defaultdict(list)

    north_river_count = 0
    west_river_count = 0

    for (x, y), p in plots.items():
        if p["rn"]:
            north_river_count += 1
            v_start = (x, y + 1)
            v_end = ((x + 1) % grid_w, y + 1)
            river_edges.append((v_start, v_end, "N", (x, y), p["rwe"]))
            edges_by_vertex[v_start].append(v_end)
            edges_by_vertex[v_end].append(v_start)
        if p["rw"]:
            west_river_count += 1
            v_start = (x, y)
            v_end = (x, y + 1)
            river_edges.append((v_start, v_end, "W", (x, y), p["rns"]))
            edges_by_vertex[v_start].append(v_end)
            edges_by_vertex[v_end].append(v_start)

    print(f"[*] 總河流段數: {len(river_edges)} (北側邊緣: {north_river_count}, 西側邊緣: {west_river_count})")

    # Build connected components of river network
    visited_vertices = set()
    components = []

    all_river_vertices = list(edges_by_vertex.keys())
    for v in all_river_vertices:
        if v not in visited_vertices:
            comp = []
            queue = deque([v])
            visited_vertices.add(v)
            while queue:
                curr = queue.popleft()
                comp.append(curr)
                for neighbor in edges_by_vertex[curr]:
                    if neighbor not in visited_vertices:
                        visited_vertices.add(neighbor)
                        queue.append(neighbor)
            components.append(comp)

    print(f"[*] 獨立水系 (River Basins / Components): {len(components)} 個")

    # Analyze components size
    comp_sizes = [len(c) for c in components]
    size_counts = defaultdict(int)
    for s in comp_sizes:
        size_counts[s] += 1

    print("    水系規模分布 (頂點數: 數量):")
    for s in sorted(size_counts.keys()):
        print(f"      - {s} 個頂點: {size_counts[s]} 條水系")

    # Identify fragmented / orphaned rivers (size <= 3 vertices, meaning 1 or 2 segments)
    short_rivers = [c for c in components if len(c) <= 3]
    print(f"[*] 短小斷頭河 / 孤立斷裂片段 (Short / Orphan Rivers <= 2 segments): {len(short_rivers)} 處")

    # Let's see where these short rivers are located
    short_river_locations = []
    for c in short_rivers:
        # Find adjacent plots
        sample_v = c[0]
        px = sample_v[0] % grid_w
        py = min(grid_h - 1, max(0, sample_v[1]))
        short_river_locations.append((px, py, plots[(px, py)]["tt"], plots[(px, py)]["pt"]))

    if short_river_locations:
        print(f"    斷裂河流範例位置 (X, Y, 地形, PlotType): {short_river_locations[:15]}")

    # Check for rivers that touch ocean / coast (proper estuaries vs dead-ends)
    dead_end_basins = []
    for c in components:
        # Check if any vertex in c touches water
        touches_water = False
        for vx, vy in c:
            # A vertex (vx, vy) touches up to 4 plots: (vx-1, vy-1), (vx-1, vy), (vx, vy-1), (vx, vy)
            for dx in [-1, 0]:
                for dy in [-1, 0]:
                    px = (vx + dx) % grid_w
                    py = vy + dy
                    if 0 <= py < grid_h and plots[(px, py)]["pt"] == 3:
                        touches_water = True
                        break
                if touches_water: break
            if touches_water: break
        if not touches_water and len(c) > 3:
            # Basin with >2 segments that never reaches any water body!
            dead_end_basins.append(c)

    print(f"[*] 未流入任何水體之內陸內流河/死水河 (Basins not reaching any ocean/lake): {len(dead_end_basins)} 處")
    for b in dead_end_basins[:10]:
        v0 = b[0]
        print(f"    內流河位置約: ({v0[0]}, {v0[1]}), 頂點數: {len(b)}")

    # Check for rivers traversing Peaks (PlotType=0) on both sides
    peak_rivers = []
    for v_start, v_end, side, (px, py), flow in river_edges:
        # If side == 'N', the river is between plot (px, py) and plot (px, py+1)
        if side == 'N':
            p1 = plots.get((px, py))
            p2 = plots.get((px, py + 1)) if py + 1 < grid_h else None
        else: # 'W'
            p1 = plots.get((px, py))
            p2 = plots.get(((px - 1) % grid_w, py))
        if p1 and p2:
            if p1["pt"] == 0 and p2["pt"] == 0:
                peak_rivers.append((px, py, side))

    print(f"[*] 兩側均為無法通行的山峰山脊之河流 (Rivers trapped between two Peaks): {len(peak_rivers)} 處")
    if peak_rivers:
        print(f"    位置: {peak_rivers[:10]}")

    # =========================================================================
    # 3. STRATEGIC CHOKEPOINTS & CRITICAL STRAITS AUDIT
    # =========================================================================
    print("\n" + "="*70)
    print("3. 全球關鍵戰略海峽與地峽拓撲審查 (Strategic Straits & Isthmuses)")
    print("="*70)

    chokepoints = {
        "直布羅陀海峽 (Strait of Gibraltar)": [(79, 59), (80, 59), (79, 58), (80, 58)],
        "英吉利海峽 (English Channel)": [(81, 69), (82, 69), (83, 69), (84, 69)],
        "博斯普魯斯海峽 (Bosphorus / Dardanelles - 黑海出口)": [(99, 60), (100, 60), (101, 60), (99, 59), (100, 59)],
        "蘇伊士地峽 (Suez Isthmus - 亞非陸橋)": [(102, 48), (103, 48), (102, 47), (103, 47)],
        "曼德海峽 (Bab-el-Mandeb - 紅海出口)": [(108, 41), (109, 41), (110, 41)],
        "荷姆茲海峽 (Strait of Hormuz - 波斯灣出口)": [(117, 49), (118, 49), (119, 49)],
        "麻六甲海峽 (Strait of Malacca)": [(144, 34), (145, 34), (145, 33), (146, 33)],
        "巴拿馬地峽 (Panama Isthmus - 美洲陸橋)": [(43, 41), (44, 41), (44, 40), (45, 40)],
        "白令海峽 (Bering Strait)": [(178, 77), (179, 77), (0, 77), (1, 77)],
        "對馬海峽 (Korea / Tsushima Strait)": [(159, 61), (159, 62), (160, 61), (160, 62)],
        "丹麥海峽/厄勒海峽 (Danish Straits - 波羅的海出口)": [(90, 72), (91, 72), (92, 72)],
    }

    for name, coords in chokepoints.items():
        desc = []
        for cx, cy in coords:
            p = plots.get((cx, cy))
            if p:
                pt_str = "水體" if p["pt"] == 3 else ("山峰" if p["pt"] == 0 else ("丘陵" if p["pt"] == 1 else "平陸"))
                desc.append(f"({cx},{cy}:{pt_str}:{p['tt'].replace('TERRAIN_', '')})")
        print(f"[*] {name}:")
        print(f"    {' | '.join(desc)}")

if __name__ == "__main__":
    audit()
