"""One-off generator for library/materials_library.blend -- run with:
    blender --background --python library\\build_materials_library.py

Builds a small starter materials library: named Material ID-blocks with
real Soundboard Lab physical-property fields set, saved as their own
.blend file. This is the actual mechanism docs/CLAUDE.md's "Material
library" decision describes for reuse across projects -- a user's own
materials_library.blend, pulled into any project via Blender's native
File > Append (or Link), optionally cataloged in the Asset Browser.

Not part of the installed extension itself; a standalone convenience
asset. Re-run this script (it overwrites the file) if the starter
materials' field set or defaults change.
"""
import sys
from pathlib import Path

LIBRARY_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(LIBRARY_DIR.parent / "addon"))

import bpy
import soundboard_lab as addon

addon.register()

# Clear the default scene's starter objects/materials -- this file
# exists purely to hold Material ID-blocks for Append/Link, not a
# scene to open and work in directly.
for obj in list(bpy.data.objects):
    bpy.data.objects.remove(obj, do_unlink=True)

spruce = bpy.data.materials.new("Spruce (Soundboard Lab Placeholder)")
spruce.soundboard_lab.kind = 'ORTHOTROPIC'
# Already SPRUCE_PLACEHOLDER's own defaults (see SoundboardLabMaterialSettings) --
# set explicitly anyway so this file stays correct even if the add-on's
# own defaults are ever changed later.
spruce.soundboard_lab.density = 460.0
spruce.soundboard_lab.e_longitudinal = 13800.0
spruce.soundboard_lab.e_radial = 811.76
spruce.soundboard_lab.e_tangential = 593.4
spruce.soundboard_lab.g_lr = 828.0
spruce.soundboard_lab.g_lt = 621.0
spruce.soundboard_lab.g_rt = 41.4
spruce.soundboard_lab.nu_lr = 0.38
spruce.soundboard_lab.nu_lt = 0.40
spruce.soundboard_lab.nu_rt = 0.45
spruce.use_fake_user = True  # survives with 0 users (nothing in this file references it)

bridge_plate = bpy.data.materials.new("Generic Isotropic (Bridge Plate Placeholder)")
bridge_plate.soundboard_lab.kind = 'ISOTROPIC'
bridge_plate.soundboard_lab.density = 1600.0
bridge_plate.soundboard_lab.iso_e = 10000.0
bridge_plate.soundboard_lab.iso_nu = 0.3
bridge_plate.use_fake_user = True

# Carbon-cap blends: isotropic stand-ins for a 4 mm spruce web with a
# carbon cap, modeled as a plain 4 mm body. Same values as
# SPRUCE_CARBON_CAP_ISO_* in src/soundboard_lab/materials.py (see the
# comment there for the derivation and caveats).
CARBON_CAP_BLENDS = [
    ("Spruce+Carbon Cap Iso Low (4mm web)", 650.0, 37500.0,
     "4 mm spruce web + 0.5 mm carbon cap, bending-equivalent isotropic. Carbon E_L = 90 GPa. Estimate, not measured."),
    ("Spruce+Carbon Cap Iso Mid (4mm web)", 650.0, 41300.0,
     "4 mm spruce web + 0.5 mm carbon cap, bending-equivalent isotropic. Carbon E_L = 120 GPa. Estimate, not measured."),
    ("Spruce+Carbon Cap Iso High (4mm web)", 650.0, 44300.0,
     "4 mm spruce web + 0.5 mm carbon cap, bending-equivalent isotropic. Carbon E_L = 150 GPa. Estimate, not measured."),
    ("Spruce+Carbon Light Overlay Iso (13 GPa experiment)", 575.0, 13000.0,
     "Experimental light-overlay stand-in used for diagonal-web waffle runs. Density was not scaled down with E; "
     "a realistic value is closer to 480 kg/m^3."),
]
carbon_blends = []
for name, density, iso_e, description in CARBON_CAP_BLENDS:
    m = bpy.data.materials.new(name)
    m.soundboard_lab.kind = 'ISOTROPIC'
    m.soundboard_lab.density = density
    m.soundboard_lab.iso_e = iso_e
    m.soundboard_lab.iso_nu = 0.3
    m.use_fake_user = True
    carbon_blends.append(m)

# Mark everything as an asset (shows up in the Asset Browser for
# drag-and-drop) and file it under the catalogs defined in
# blender_assets.cats.txt next to this file.
CATALOG_PLACEHOLDERS = "5b0a0f4e-6a49-4c58-9e32-1f3c8a7d2b01"
CATALOG_CARBON_CAP = "8c2d5e71-3f94-4b6a-a1d0-7e9b4c6f3a02"
for m in (spruce, bridge_plate):
    m.asset_mark()
    m.asset_data.catalog_id = CATALOG_PLACEHOLDERS
    m.asset_data.tags.new("placeholder")
for m, (_, _, _, description) in zip(carbon_blends, CARBON_CAP_BLENDS):
    m.asset_mark()
    m.asset_data.catalog_id = CATALOG_CARBON_CAP
    m.asset_data.description = description
    m.asset_data.tags.new("isotropic")
    m.asset_data.tags.new("carbon cap")

assert len(bpy.data.objects) == 0
assert {"Spruce (Soundboard Lab Placeholder)", "Generic Isotropic (Bridge Plate Placeholder)"}.issubset(
    {m.name for m in bpy.data.materials}
)
assert all(m.asset_data is not None for m in bpy.data.materials if m.use_fake_user)

out_path = str(LIBRARY_DIR / "materials_library.blend")
bpy.ops.wm.save_as_mainfile(filepath=out_path)
print(f"Wrote {out_path}")
