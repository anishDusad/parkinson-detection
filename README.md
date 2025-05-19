Step 1: Download the multiclass data from some standard organization

Step 2: Run the dicom2nifti file script to convert dicom format to nifty format

Step 3: Install some more dependencies before running preprocessing script - 
```
!pip uninstall -y ants
!pip install antspyx
!pip install nilearn
!pip install antspyx antspynet

```

Step 4: Run the preprocessing file script - it performs skull stripping, registration(to mni152 template), gaussian smoothing 
