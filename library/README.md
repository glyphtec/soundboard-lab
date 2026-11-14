# Materials Library

`materials_library.blend` is a starter personal materials library for Soundboard Lab, per `docs/SOUNDBOARD-LAB-DOC.md`'s "Material library" decision: physical material records live on native `bpy.types.Material` ID-blocks, so a `materials_library.blend` full of named Materials with their Soundboard Lab physical-property fields set is a real, reusable library across any project -- no custom add-on-side catalog needed.

It currently contains these materials, all marked as **assets** and filed under catalogs (defined in `blender_assets.cats.txt`):

Soundboard Lab/Placeholders (replace with real lab data -- see `src/soundboard_lab/materials.py`'s `SPRUCE_PLACEHOLDER`/`ISOTROPIC_PLACEHOLDER` docstrings):

- **Spruce (Soundboard Lab Placeholder)** -- Orthotropic.
- **Generic Isotropic (Bridge Plate Placeholder)** -- Isotropic.

Soundboard Lab/Carbon Cap Blends (isotropic stand-ins for a 4 mm spruce web with a carbon cap, modeled as a plain 4 mm body; estimates, see the comment above `SPRUCE_CARBON_CAP_ISO_LOW` in `materials.py`):

- **Spruce+Carbon Cap Iso Low / Mid / High (4mm web)** -- E 37,500 / 41,300 / 44,300 MPa, density 650 kg/m^3.
- **Spruce+Carbon Light Overlay Iso (13 GPa experiment)** -- E 13,000 MPa, density 575 kg/m^3 (density was not scaled down with E; closer to 480 is more realistic).

## Using it as an Asset Library (recommended)

1. **Edit > Preferences > File Paths > Asset Libraries > Add**, and point it at this `library` folder (the one containing `materials_library.blend` and `blender_assets.cats.txt`). Name it e.g. "Soundboard Lab".
2. In any project, open an **Asset Browser** editor and pick that library. Materials are grouped by catalog.
3. Drag a material onto the object (or into the viewport) to assign it, or right-click > **Append**/**Link**. Dragging copies the material into your project, so per-project edits don't change the library.

## Using it without the Asset Browser

1. In your soundboard `.blend` file: **File > Append** (or **Link**, if you want live updates from the library file itself), browse into `materials_library.blend > Material`, and pick the material you want.
2. Assign it to an object via the Soundboard Lab N-panel's Material & Grain Orientation sub-panel (material picker) or the Properties editor's Material tab.
3. Edit the physical-property fields freely per-project -- Append copies the data-block into your file, it does not stay tied to the library (use Link instead if you want shared/live-updating materials across many projects).
## Adding a material you've created back into the library

So your own tuned/real-lab-measured materials become available in *future* projects too, not just this session's project:

1. **Save your current project** first -- Append reads from a saved file on disk, not unsaved in-memory state.
2. **Open `library/materials_library.blend` directly** (File > Open) -- you're now editing the library file itself, not your project.
3. **File > Append** > browse into your project's saved `.blend` file > `Material` > select the material(s) you tuned > Append. This copies the Material ID-block (with all its Soundboard Lab physical-property fields already on it) into the library file.
4. **Give it a Fake User**: click the shield icon next to the material's name in its dropdown/browser, or in the Material Properties panel. Without this, the material has 0 real users in the library file (nothing in that file actually assigns it to an object) and Blender will silently drop it the next time the library file is saved and reloaded.
5. Optionally, **mark it as an Asset** (right-click the material > Mark as Asset) so it gets a preview thumbnail and shows up in the Asset Browser for drag-and-drop reuse, not just File > Append.
6. **Save the library file.** It's now available to any project via Append/Link/Asset Browser, same as the two starter materials.

## Regenerating

`build_materials_library.py` is the generator script (not part of the installed extension) -- run it with:

```
blender --background --python library\build_materials_library.py
```

It overwrites `materials_library.blend`. Re-run it if you add new starter materials or the add-on's own placeholder defaults change.
