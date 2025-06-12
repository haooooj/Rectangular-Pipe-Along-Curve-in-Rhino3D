# Rectangular Pipe Along Curve in Rhino3D

This script creates rectangular pipe geometry by sweeping a rotated rectangular profile along one or more user-selected curves. You can control the orientation of the profile using either a **fixed rotation angle** or a **reference vector**, allowing precise control of profile alignment.

## What Does the Script Do?

The **Rectangular Pipe** tool allows you to:

* Select one or more rail curves (open or closed).
* Specify rectangle dimensions:

  * **Width** (along X of profile plane)
  * **Height** (along Y of profile plane)
* Choose how to define profile orientation:

  * **Angle mode**: enter a fixed rotation in degrees (clockwise in profile plane).
  * **Vector mode**: pick two points to define a world-space direction; the script projects this vector into the rail’s local frame to determine alignment.
* Construct a rectangle profile at the start of each rail.
* Perform a **closed sweep** operation along each rail.
* Bake the resulting brep pipes into the document.

## Why Use It?

Unlike Rhino’s native `Pipe` or `Sweep1` command, this tool:

* Uses a **rectangular** profile (not circular or arbitrary).
* Allows **precise control** of orientation, either absolute (angle) or relative (vector).
* Works on multiple curves in one operation.
* Bypasses manual construction geometry or alignment guides.

Ideal for:

* Frame or beam extrusion
* Panel edge modelling
* Rectangular ductwork or channel forms
* Any controlled-profile extrusion along curved paths

## How to Use the Script

### Load the Script in Rhino

**Method 1**:

1. Type `_RunPythonScript` in the command line.
2. Browse to the saved location of the script and run it.

### Method 2 Creating a Button or Alias for Easy Access (Optional)

#### Creating a Toolbar Button

1. **Right-click** on an empty area of the toolbar and select **New Button**.
2. In the **Button Editor**:

   * **Left Button Command**:

     ```plaintext
     ! _-RunPythonScript "FullPathToYourScript\rectangular_pipe.py"
     ```
   * Replace `FullPathToYourScript` with the actual file path where the script is saved.
   * **Tooltip**: e.g., `Sweep rectangular pipe along curve with angle or vector orientation`.
   * **Icon (Optional)**: Assign a relevant visual icon if desired.

#### Creating an Alias

1. Go to **Tools > Options > Aliases**.

2. **Create a New Alias**:

   * **Alias**: e.g., `rectpipe`
   * **Command Macro**:

     ```plaintext
     _-RunPythonScript "FullPathToYourScript\rectangular_pipe.py"
     ```

3. **Use the Alias**: Type the alias (e.g., `rectpipe`) into the command line and press **Enter** to run the script.

### Using the Command

1. **Select** one or more rail curves.
2. Input **rectangle width** (X direction) and **height** (Y direction).
3. Choose **rotation method**:

   * `Angle`: Enter degrees (clockwise rotation in the profile plane).
   * `Vector`: Pick two points in model space to define a directional reference.
4. The script will:

   * Compute a rectangular profile oriented at the rail start point.
   * Sweep it along the rail as a closed profile.
   * Add the resulting brep geometry to the document.

You will see a summary of how many pipes were created successfully.

## Technical Notes

* Profile placement is at the **start point** of each rail.
* Profile frame is computed using `PerpendicularFrameAt` (local normal and tangent).
* Angle mode rotates the profile about the rail's local Z axis.
* Vector mode projects the world vector into the profile plane and computes angle relative to X-axis.
* Sweep tolerance uses `ModelAngleToleranceRadians`.
* All sweeps are **closed**; open profiles are not generated.
