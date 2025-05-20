Step 1: Download the multiclass data from some standard organization in 3D dicom or nifty format.

Step 2: 
```
!pip install dicom2nifti

!python -m pip install --upgrade pip
```

Step 3: Run the dicom2nifti file script to convert dicom format to nifty format

Step 4: Install some more dependencies before running preprocessing script - 
```
!pip uninstall -y ants
!pip install antspyx
!pip install nilearn
!pip install antspyx antspynet

```

Step 5: Run the preprocessing file script - it performs skull stripping, registration(to mni152 template) and gaussian smoothing.

Step 6: Run the skull_extraction.py script to extract 2D slices from 3D brain MRI scans.
