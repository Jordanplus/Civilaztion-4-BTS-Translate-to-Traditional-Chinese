import os, struct, io, time
import numpy as np
import trimesh
import fast_simplification
from PIL import Image, ImageDraw, ImageFont, ImageFilter

time.clock = time.perf_counter
from pyffi.formats.nif import NifFormat

GLB_PATH = r'C:\Users\jorda\Downloads\CIV4 3D\玉山級.glb'
STEAM_VANILLA_DIR = r"C:\Program Files (x86)\Steam\steamapps\common\Sid Meier's Civilization IV Beyond the Sword\Beyond the Sword\Assets\Art\Units\Missile_Cruiser"
YUSHAN_DIR = r'patch\PatchFiles\Beyond the Sword\Assets\Art\Units\Taiwan_Yushan'
STEAM_YUSHAN_DIR = r"C:\Program Files (x86)\Steam\steamapps\common\Sid Meier's Civilization IV Beyond the Sword\Beyond the Sword\Assets\Art\Units\Taiwan_Yushan"

print('=== 1. Generating High-Definition Authentically Detailed Warship Texture ===')
scene = trimesh.load(GLB_PATH)
geom = list(scene.geometry.values())[0]
raw_tex = geom.visual.material.baseColorTexture.convert('RGB')
arr_raw = np.array(raw_tex, dtype=np.float32)

# Smooth tone mapping: gentle gamma with zero blown-out clipping
gamma = 0.82
boosted = 255.0 * np.power(arr_raw / 255.0, gamma)
boosted = np.clip(boosted * 1.08, 0, 215).astype(np.uint8)
tex = Image.fromarray(boosted)

# Unsharp mask to make plating lines and mechanical vents pop
tex_sharp = tex.filter(ImageFilter.UnsharpMask(radius=2, percent=140, threshold=3))
draw = ImageDraw.Draw(tex_sharp)

# 1. Flight Deck: U=[324, 490], V=[795, 961]
# Non-skid dark grey deck surface
deck_box = [324, 795, 490, 961]
deck_arr = np.array(tex_sharp.crop(deck_box)).astype(float) * 0.76
tex_sharp.paste(Image.fromarray(deck_arr.astype(np.uint8)), (324, 795))

# White perimeter border
draw.rectangle([330, 801, 484, 955], outline=(235, 235, 240), width=2)
# White helicopter landing circle
cx, cy = 407, 878
r = 38
draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(240, 240, 245), width=3)
# 'H' inside landing circle
draw.line([cx - 15, cy - 18, cx - 15, cy + 18], fill=(240, 240, 245), width=3)
draw.line([cx + 15, cy - 18, cx + 15, cy + 18], fill=(240, 240, 245), width=3)
draw.line([cx - 15, cy, cx + 15, cy], fill=(240, 240, 245), width=3)

# Centerline dashed tramline
for y in range(805, 950, 14):
    draw.line([cx, y, cx, y + 8], fill=(240, 240, 245), width=2)

# 2. Crisp ROC Navy '1401' Hull Numbers
try:
    font = ImageFont.truetype('arialbd.ttf', 20)
except:
    font = ImageFont.load_default()

# Port Bow: X=35, Y=135
draw.text((37, 137), '1401', fill=(15, 18, 22), font=font)
draw.text((35, 135), '1401', fill=(245, 245, 250), font=font)

# Starboard Bow: X=615, Y=310
draw.text((617, 312), '1401', fill=(15, 18, 22), font=font)
draw.text((615, 310), '1401', fill=(245, 245, 250), font=font)

# 3. Tinted Command Bridge Windows (Comp 89): X=[20, 150], Y=[815, 825]
for wx in range(25, 145, 12):
    draw.rectangle([wx, 818, wx + 8, 824], fill=(20, 28, 38), outline=(10, 15, 20), width=1)

# Convert to RGBA DDS
tex_rgba = np.array(tex_sharp)
h, w, _ = tex_rgba.shape
final_rgba = np.zeros((h, w, 4), dtype=np.uint8)
final_rgba[:, :, :3] = tex_rgba
final_rgba[:, :, 3] = 255
dds_img = Image.fromarray(final_rgba, 'RGBA')

repo_dds_path = os.path.join(YUSHAN_DIR, 'Missle_Cruiser_256.dds')
steam_dds_path = os.path.join(STEAM_YUSHAN_DIR, 'Missle_Cruiser_256.dds')
dds_img.save(repo_dds_path)
dds_img.save(steam_dds_path)
print(f'Saved enhanced high-definition texture to {repo_dds_path} and Steam!')

print('\n=== 2. Loading GLB & Splitting into Contiguous UV Islands (High Fidelity) ===')
components = geom.split(only_watertight=False)
print(f'Original mesh: {len(geom.vertices)} vertices, {len(geom.faces)} faces across {len(components)} UV islands')

simplified_pieces = []
for idx, comp in enumerate(components):
    cv = comp.vertices
    cf = comp.faces
    cuv = comp.visual.uv
    nf = len(cf)
    
    if nf <= 16:
        # Small thin details (antennas, railings, masts, fittings): Keep 100% intact!
        simplified_pieces.append((cv, cf, cuv))
        continue
        
    # Main hull and superstructure surfaces (higher ratio = double geometric detail!)
    target = max(14, int(nf * 0.22))
    pts_s, tris_s = fast_simplification.simplify(cv, cf, target_count=target)
    
    # Barycentric interpolation within THIS UV island only
    closest, dist, tri_id = comp.nearest.on_surface(pts_s)
    tri_verts = cv[cf[tri_id]]
    v0, v1, v2 = tri_verts[:, 0], tri_verts[:, 1], tri_verts[:, 2]
    e0, e1, e2 = v1 - v0, v2 - v0, closest - v0
    d00 = np.sum(e0 * e0, axis=1)
    d01 = np.sum(e0 * e1, axis=1)
    d11 = np.sum(e1 * e1, axis=1)
    d20 = np.sum(e2 * e0, axis=1)
    d21 = np.sum(e2 * e1, axis=1)
    denom = d00 * d11 - d01 * d01
    denom[np.abs(denom) < 1e-8] = 1e-8
    v = np.clip((d11 * d20 - d01 * d21) / denom, 0, 1)
    w = np.clip((d00 * d21 - d01 * d20) / denom, 0, 1)
    u = np.clip(1.0 - v - w, 0, 1)
    sum_uvw = u + v + w
    sum_uvw[sum_uvw == 0] = 1.0
    u /= sum_uvw
    v /= sum_uvw
    w /= sum_uvw
    
    tri_uvs = cuv[cf[tri_id]]
    uv_s = u[:, None] * tri_uvs[:, 0] + v[:, None] * tri_uvs[:, 1] + w[:, None] * tri_uvs[:, 2]
    simplified_pieces.append((pts_s, tris_s, uv_s))

all_v = []
all_f = []
all_uv = []
v_offset = 0

for pts, tris, uvs in simplified_pieces:
    all_v.append(pts)
    all_f.append(tris + v_offset)
    all_uv.append(uvs)
    v_offset += len(pts)

all_v = np.vstack(all_v)
all_f = np.vstack(all_f)
all_uv = np.vstack(all_uv)

N = len(all_v)
M = len(all_f)
print(f'Combined high-fidelity mesh: {N} vertices, {M} triangles')

print('\n=== 3. Transforming Coordinates & Aligning Outward Normals ===')
scale_beam, scale_length, scale_height = 115.0, 190.0, 185.0
waterline = -0.155

civ4_verts = np.zeros_like(all_v)
civ4_verts[:, 0] = -all_v[:, 2] * scale_beam
civ4_verts[:, 1] = -all_v[:, 0] * scale_length
civ4_verts[:, 2] = (all_v[:, 1] - waterline) * scale_height

# Area-weighted vertex normal computation
v0 = civ4_verts[all_f[:, 0]]
v1 = civ4_verts[all_f[:, 1]]
v2 = civ4_verts[all_f[:, 2]]
fn = np.cross(v1 - v0, v2 - v0)
vert_norms = np.zeros_like(civ4_verts)
for i in range(3):
    np.add.at(vert_norms, all_f[:, i], fn)
l = np.linalg.norm(vert_norms, axis=1, keepdims=True)
l[l == 0] = 1.0
vert_norms /= l

# Fix any face whose normal opposes vertex normals (winding consistency)
fn_len = np.linalg.norm(fn, axis=1, keepdims=True)
fn_len[fn_len == 0] = 1.0
fn_unit = fn / fn_len
dots = np.sum(fn_unit * (vert_norms[all_f[:, 0]] + vert_norms[all_f[:, 1]] + vert_norms[all_f[:, 2]]) / 3.0, axis=1)
neg_idx = np.where(dots < 0)[0]
if len(neg_idx) > 0:
    all_f[neg_idx, 1], all_f[neg_idx, 2] = all_f[neg_idx, 2], all_f[neg_idx, 1].copy()
    print(f'Flipped {len(neg_idx)} inverted triangles to 100% outward winding!')

# Recompute final smooth vertex normals with corrected winding
v0 = civ4_verts[all_f[:, 0]]
v1 = civ4_verts[all_f[:, 1]]
v2 = civ4_verts[all_f[:, 2]]
fn = np.cross(v1 - v0, v2 - v0)
vert_norms = np.zeros_like(civ4_verts)
for i in range(3):
    np.add.at(vert_norms, all_f[:, i], fn)
l = np.linalg.norm(vert_norms, axis=1, keepdims=True)
l[l == 0] = 1.0
vert_norms /= l

fn_len = np.linalg.norm(fn, axis=1, keepdims=True)
fn_len[fn_len == 0] = 1.0
fn_unit = fn / fn_len
final_dots = np.sum(fn_unit * (vert_norms[all_f[:, 0]] + vert_norms[all_f[:, 1]] + vert_norms[all_f[:, 2]]) / 3.0, axis=1)
print(f'Normal Quality: Mean dot = {np.mean(final_dots):.4f}, Min dot = {np.min(final_dots):.4f}, Inverted faces = {np.sum(final_dots < 0)}')

print('\n=== 4. Partitioning Mesh into Safe Hardware Skin Blocks (<=750 verts/block) ===')
blocks = []
current_faces = []
current_verts = set()

for face in all_f:
    new_verts = set(face) - current_verts
    if len(current_verts) + len(new_verts) > 750 and len(current_faces) > 0:
        blocks.append(np.array(current_faces))
        current_faces = [face]
        current_verts = set(face)
    else:
        current_faces.append(face)
        current_verts.update(face)

if current_faces:
    blocks.append(np.array(current_faces))

num_blocks = len(blocks)
print(f'Created {num_blocks} Skin Partition Blocks:')
partition_data = []
for i, blk_faces in enumerate(blocks):
    local_to_global = sorted(list(set(v for tri in blk_faces for v in tri)))
    global_to_local = {g: l for l, g in enumerate(local_to_global)}
    local_tris = [(global_to_local[t[0]], global_to_local[t[1]], global_to_local[t[2]]) for t in blk_faces]
    partition_data.append((local_to_global, local_tris))
    print(f'  Block {i}: {len(local_to_global)} vertices, {len(local_tris)} triangles')

print('\n=== 5. Constructing Gamebryo 20.0 NIF with Matte Naval Steel Shading ===')
def build_nif(template_path, out_path):
    d = NifFormat.Data()
    with open(template_path, 'rb') as f:
        d.read(f)
        
    shape = None
    for b in d.roots[0].tree():
        if type(b).__name__ == 'NiTriShape' and b.name == b'missle_cruiser':
            shape = b
            break
            
    shape.translation.x = 0.0
    shape.translation.y = 0.0
    shape.translation.z = 0.0
    
    # 1. NiMaterialProperty: Matte warship steel (no blinding specular glare, no pitch-black shadows)
    for p in shape.properties:
        if type(p).__name__ == 'NiMaterialProperty':
            p.ambient_color.r = 0.65
            p.ambient_color.g = 0.65
            p.ambient_color.b = 0.65
            p.diffuse_color.r = 0.88
            p.diffuse_color.g = 0.88
            p.diffuse_color.b = 0.88
            p.specular_color.r = 0.22
            p.specular_color.g = 0.22
            p.specular_color.b = 0.22
            p.emissive_color.r = 0.0
            p.emissive_color.g = 0.0
            p.emissive_color.b = 0.0
            p.glossiness = 20.0
            p.alpha = 1.0
            
        elif type(p).__name__ == 'NiTexturingProperty':
            p.has_glow_texture = False
            p.has_decal_0_texture = False
            
    # Hardware double-sided stencil property
    has_stencil = any(type(p).__name__ == 'NiStencilProperty' for p in shape.properties)
    if not has_stencil:
        stencil = NifFormat.NiStencilProperty()
        stencil.flags = 0x0
        stencil.stencil_enabled = 0
        stencil.draw_mode = 3 # DRAW_BOTH
        shape.add_property(stencil)
        
    # 2. NiTriShapeData
    data = shape.data
    data.num_vertices = N
    data.has_vertices = True
    data.vertices.update_size()
    data.has_normals = True
    data.normals.update_size()
    data.num_uv_sets = 1
    data.bs_num_uv_sets = 1
    data.uv_sets.update_size()
    
    for i in range(N):
        data.vertices[i].x = float(civ4_verts[i, 0])
        data.vertices[i].y = float(civ4_verts[i, 1])
        data.vertices[i].z = float(civ4_verts[i, 2])
        data.normals[i].x = float(vert_norms[i, 0])
        data.normals[i].y = float(vert_norms[i, 1])
        data.normals[i].z = float(vert_norms[i, 2])
        data.uv_sets[0][i].u = float(all_uv[i, 0])
        data.uv_sets[0][i].v = float(all_uv[i, 1])
        
    data.set_triangles([tuple(f) for f in all_f])
    data.update_center_radius()
    
    # 3. NiSkinData
    si = shape.skin_instance
    sd = si.data
    sd.skin_transform.scale = 1.0
    sd.skin_transform.translation.x = 0.0
    sd.skin_transform.translation.y = 0.0
    sd.skin_transform.translation.z = 0.0
    
    b0 = sd.bone_list[0]
    b0.skin_transform.scale = 1.0
    b0.skin_transform.translation.x = 0.0
    b0.skin_transform.translation.y = -12.270
    b0.skin_transform.translation.z = 0.0
    b0.bounding_sphere_offset.x = float(data.center.x)
    b0.bounding_sphere_offset.y = float(data.center.y - 12.270)
    b0.bounding_sphere_offset.z = float(data.center.z)
    b0.bounding_sphere_radius = float(data.radius)
    b0.num_vertices = N
    b0.vertex_weights.update_size()
    for i in range(N):
        b0.vertex_weights[i].index = i
        b0.vertex_weights[i].weight = 1.0
        
    for i in range(1, len(sd.bone_list)):
        sd.bone_list[i].num_vertices = 0
        sd.bone_list[i].vertex_weights.update_size()
        
    # 4. NiSkinPartition
    sp = si.skin_partition
    sp.num_skin_partition_blocks = num_blocks
    sp.skin_partition_blocks.update_size()
    
    for b_idx in range(num_blocks):
        local_to_global, local_tris = partition_data[b_idx]
        num_v = len(local_to_global)
        num_t = len(local_tris)
        
        blk = sp.skin_partition_blocks[b_idx]
        blk.num_vertices = num_v
        blk.num_triangles = num_t
        blk.num_bones = 1
        blk.num_strips = 0
        blk.num_weights_per_vertex = 4
        
        blk.bones.update_size()
        blk.bones[0] = 0
        
        blk.has_vertex_map = True
        blk.vertex_map.update_size()
        for i in range(num_v):
            blk.vertex_map[i] = int(local_to_global[i])
            
        blk.has_vertex_weights = True
        blk.vertex_weights.update_size()
        for i in range(num_v):
            blk.vertex_weights[i][0] = 1.0
            blk.vertex_weights[i][1] = 0.0
            blk.vertex_weights[i][2] = 0.0
            blk.vertex_weights[i][3] = 0.0
            
        blk.has_bone_indices = True
        blk.bone_indices.update_size()
        for i in range(num_v):
            blk.bone_indices[i][0] = 0
            blk.bone_indices[i][1] = 0
            blk.bone_indices[i][2] = 0
            blk.bone_indices[i][3] = 0
            
        blk.has_faces = True
        blk.triangles.update_size()
        for j, tri in enumerate(local_tris):
            blk.triangles[j].v_1 = int(tri[0])
            blk.triangles[j].v_2 = int(tri[1])
            blk.triangles[j].v_3 = int(tri[2])
            
    with open(out_path, 'wb') as f:
        d.write(f)
    print(f'Successfully built: {out_path} ({os.path.getsize(out_path)} bytes)')

steam_nif = os.path.join(STEAM_VANILLA_DIR, 'Missile_Cruiser.nif')
steam_fx_nif = os.path.join(STEAM_VANILLA_DIR, 'Missile_Cruiser_FX.nif')

repo_nif = os.path.join(YUSHAN_DIR, 'Missile_Cruiser.nif')
repo_fx_nif = os.path.join(YUSHAN_DIR, 'Missile_Cruiser_FX.nif')

steam_target_nif = os.path.join(STEAM_YUSHAN_DIR, 'Missile_Cruiser.nif')
steam_target_fx_nif = os.path.join(STEAM_YUSHAN_DIR, 'Missile_Cruiser_FX.nif')

print('\nBuilding Repo NIFs...')
build_nif(steam_nif, repo_nif)
build_nif(steam_fx_nif, repo_fx_nif)

print('\nBuilding Steam Installation NIFs...')
build_nif(steam_nif, steam_target_nif)
build_nif(steam_fx_nif, steam_target_fx_nif)

print('\n=== All NIFs & Textures Successfully Built & Deployed! ===')
