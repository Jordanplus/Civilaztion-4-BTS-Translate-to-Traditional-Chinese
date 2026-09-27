import os, struct, io
import numpy as np
import trimesh
import fast_simplification
from PIL import Image
import time
time.clock = time.perf_counter
from pyffi.formats.nif import NifFormat

GLB_PATH = r'C:\Users\jorda\Downloads\CIV4 3D\玉山級.glb'
STEAM_VANILLA_DIR = "C:/Program Files (x86)/Steam/steamapps/common/Sid Meier's Civilization IV Beyond the Sword/Beyond the Sword/Assets/Art/Units/Missile_Cruiser"
YUSHAN_DIR = r'patch\PatchFiles\Beyond the Sword\Assets\Art\Units\Taiwan_Yushan'
STEAM_YUSHAN_DIR = "C:/Program Files (x86)/Steam/steamapps/common/Sid Meier's Civilization IV Beyond the Sword/Beyond the Sword/Assets/Art/Units/Taiwan_Yushan"

print('1. Loading GLB and optimizing geometry...')
scene = trimesh.load(GLB_PATH)
geom = list(scene.geometry.values())[0]
orig_v = geom.vertices
orig_f = geom.faces
orig_uv = geom.visual.uv

# Decimate to Civ 4 unit standards (~800 vertices)
pts_low, tris_low = fast_simplification.simplify(orig_v, orig_f, target_count=700)
N = len(pts_low)
print(f'Vertices: {N}')

# Barycentric UV mapping
closest, distance, tri_id = geom.nearest.on_surface(pts_low)
tri_verts = orig_v[orig_f[tri_id]]
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

tri_uvs = orig_uv[orig_f[tri_id]]
uv_low = u[:, None] * tri_uvs[:, 0] + v[:, None] * tri_uvs[:, 1] + w[:, None] * tri_uvs[:, 2]

# Civ 4 coordinates
scale_beam, scale_length, scale_height = 115.0, 190.0, 185.0
waterline = -0.155
civ4_verts = np.zeros_like(pts_low)
civ4_verts[:, 0] = -pts_low[:, 2] * scale_beam
civ4_verts[:, 1] = -pts_low[:, 0] * scale_length
civ4_verts[:, 2] = (pts_low[:, 1] - waterline) * scale_height

# 2. Fix inverted faces & create double-sided geometry (eliminates transparent holes)
center = np.mean(civ4_verts, axis=0)
v0 = civ4_verts[tris_low[:, 0]]
v1 = civ4_verts[tris_low[:, 1]]
v2 = civ4_verts[tris_low[:, 2]]
fn = np.cross(v1 - v0, v2 - v0)
face_centers = (v0 + v1 + v2) / 3.0
vec_from_center = face_centers - center
dots = np.sum(fn * vec_from_center, axis=1)

# Orient outward
corrected_tris = tris_low.copy()
inward_idx = np.where(dots < 0)[0]
corrected_tris[inward_idx, 1] = tris_low[inward_idx, 2]
corrected_tris[inward_idx, 2] = tris_low[inward_idx, 1]
print(f'Flipped {len(inward_idx)} inward faces to outward!')

# Add back-faces so inner walls and recessed docks are also 100% visible
back_tris = np.zeros_like(corrected_tris)
back_tris[:, 0] = corrected_tris[:, 0]
back_tris[:, 1] = corrected_tris[:, 2]
back_tris[:, 2] = corrected_tris[:, 1]
all_tris = np.vstack([corrected_tris, back_tris])
M = len(all_tris)
print(f'Total solid faces: {M} ({len(corrected_tris)} front + {len(back_tris)} back)')

# Compute outward vertex normals from front faces
v0_c = civ4_verts[corrected_tris[:, 0]]
v1_c = civ4_verts[corrected_tris[:, 1]]
v2_c = civ4_verts[corrected_tris[:, 2]]
fn_c = np.cross(v1_c - v0_c, v2_c - v0_c)
vert_normals = np.zeros_like(civ4_verts)
for i in range(3):
    np.add.at(vert_normals, corrected_tris[:, i], fn_c)
lens = np.linalg.norm(vert_normals, axis=1, keepdims=True)
lens[lens == 0] = 1.0
vert_normals = vert_normals / lens

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
    
    # Add NiStencilProperty to disable backface culling in DirectX 9
    has_stencil = any(type(p).__name__ == 'NiStencilProperty' for p in shape.properties)
    if not has_stencil:
        stencil = NifFormat.NiStencilProperty()
        stencil.flags = 0x0
        stencil.stencil_enabled = 0
        stencil.draw_mode = 3 # DRAW_BOTH
        shape.add_property(stencil)
    
    # 1. NiTriShapeData
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
        data.normals[i].x = float(vert_normals[i, 0])
        data.normals[i].y = float(vert_normals[i, 1])
        data.normals[i].z = float(vert_normals[i, 2])
        data.uv_sets[0][i].u = float(uv_low[i, 0])
        data.uv_sets[0][i].v = float(uv_low[i, 1])
        
    data.set_triangles([tuple(f) for f in all_tris])
    data.update_center_radius()
    
    # 2. NiSkinData
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
        
    # 3. NiSkinPartition
    sp = si.skin_partition
    sp.num_skin_partition_blocks = 1
    sp.skin_partition_blocks.update_size()
    blk = sp.skin_partition_blocks[0]
    blk.num_vertices = N
    blk.num_triangles = M
    blk.num_bones = 1
    blk.num_strips = 0
    blk.num_weights_per_vertex = 4
    blk.bones.update_size()
    blk.bones[0] = 0
    blk.has_vertex_map = True
    blk.vertex_map.update_size()
    for i in range(N):
        blk.vertex_map[i] = i
        
    blk.has_vertex_weights = True
    blk.vertex_weights.update_size()
    for i in range(N):
        blk.vertex_weights[i][0] = 1.0
        blk.vertex_weights[i][1] = 0.0
        blk.vertex_weights[i][2] = 0.0
        blk.vertex_weights[i][3] = 0.0
        
    blk.has_bone_indices = True
    blk.bone_indices.update_size()
    for i in range(N):
        blk.bone_indices[i][0] = 0
        blk.bone_indices[i][1] = 0
        blk.bone_indices[i][2] = 0
        blk.bone_indices[i][3] = 0
        
    blk.has_faces = True
    blk.triangles.update_size()
    for j, f in enumerate(all_tris):
        blk.triangles[j].v_1 = int(f[0])
        blk.triangles[j].v_2 = int(f[1])
        blk.triangles[j].v_3 = int(f[2])
        
    with open(out_path, 'wb') as f:
        d.write(f)
    print(f'Wrote: {out_path} ({os.path.getsize(out_path)} bytes)')

# Source vanilla templates from Steam installation
steam_nif = os.path.join(STEAM_VANILLA_DIR, 'Missile_Cruiser.nif')
steam_fx_nif = os.path.join(STEAM_VANILLA_DIR, 'Missile_Cruiser_FX.nif')

out_nif = os.path.join(YUSHAN_DIR, 'Missile_Cruiser.nif')
out_fx_nif = os.path.join(YUSHAN_DIR, 'Missile_Cruiser_FX.nif')

print('2. Building solid, 100% opaque NIF files...')
build_nif(steam_nif, out_nif)
build_nif(steam_fx_nif, out_fx_nif)

print('Done!')
