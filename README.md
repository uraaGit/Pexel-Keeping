# Pixel Keeping

This was developed in the Blender 4.2.0 environment.

## Usage

An add-on that unwrap UVs to keep pixel evently distributed on quad faces.

### Import
1. Download the zip file or .py code
2. Launch Blender
3. Open the Preference and Add-ons section, then install zip file or .py code
4. Enable Pixel Keeping, switch the mesh object to Edit Mode, and select"Arrange face to UV" in the UV menu

### Operator Panel
- UV Number      :   Expand texture with UDIM. Supports up to 8 UV maps.
- texture Size   :   Supports texture sizes of 256, 512, 1024, 2048. Adjust according to your desired texture size.
- Pixel Count    :   Faces can keep pixel counts of 4x4, 8x8, 16x16, 32x32.
- Margin         :   Margin with adjucent faces.
   
![pk_menu](https://github.com/user-attachments/assets/be9714f6-1b28-464d-841b-2b5d496346ab)

## Note

- Please refrain from painting in UV space when using this add-on.
- If the face index changes, the arrangement will change, and the texture prograssion will reset.

   
