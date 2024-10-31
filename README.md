# Pixel Keeping

![pk_explain](https://github.com/user-attachments/assets/c52e30a2-6b7f-4de2-a379-fac63c0005b3)

![pk_window](https://github.com/user-attachments/assets/9688b0f4-a8f8-4a30-999c-96ab7dd5c7f2)

This was developed in the Blender 4.2.0 environment.

## Usage

An add-on that arrange faces in UV space to maintain a specified pixel count.

### Import
1. Download the .py code
2. Launch Blender
3. Open the Preference and Add-ons section, then install .py code
4. Enable Pixel Keeping, switch the mesh object to Edit Mode, and select"Arrange face to UV" in the UV menu

### Operator Panel
- UV Number      :   Add or reduce UV map attribute. Used in conjection with UDIM, like layers in paint software. Supports up to 8 UV maps.
- texture Size   :   Supports texture sizes of 256, 512, 1024, 2048. Adjust according to your desired texture size.
- Pixel Count    :   Faces can keep pixel counts of 4x4, 8x8, 16x16, 32x32.
- Margin         :   Margin with adjucent faces.
   
![pk_menu](https://github.com/user-attachments/assets/be9714f6-1b28-464d-841b-2b5d496346ab)

![image](https://github.com/user-attachments/assets/c36f39da-142b-4774-9e39-af6708907a00)


## Note

- Please refrain from painting in UV space when using this add-on.
- If the face index changes, the arrangement will change, and the texture prograssion will reset.

## License

GPL-3.0

   
