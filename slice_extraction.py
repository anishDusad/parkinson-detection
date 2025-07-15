import os
import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

def process_nifti_files(main_directory, output_directory, slice_index=None):
    # Create output directories for all planes
    planes = ['axial', 'coronal', 'sagittal']
    for plane in planes:
        plane_dir = os.path.join(output_directory, plane)
        os.makedirs(plane_dir, exist_ok=True)

    # Collect all NIfTI files
    nifti_files = []
    for root, _, files in os.walk(main_directory):
        for file in files:
            if file.endswith('.nii') or file.endswith('.nii.gz'):
                nifti_path = os.path.join(root, file)
                subject_id = os.path.basename(root)
                nifti_files.append((nifti_path, subject_id))

    failed_subjects = []

    # Process each file
    for nifti_path, subject_id in tqdm(nifti_files, desc="Processing Subjects"):
        try:
            process_single_nifti(nifti_path, subject_id, output_directory, slice_index)
            print(f"Processed: {subject_id}")
        except Exception as e:
            print(f"Failed: {subject_id} | Reason: {e}")
            failed_subjects.append((subject_id, str(e)))

    # Print summary
    print("\n Processing Summary:")
    print(f"Successfully processed: {len(nifti_files) - len(failed_subjects)} / {len(nifti_files)}")
    if failed_subjects:
        print(f"Failed subjects ({len(failed_subjects)}):")
        for sid, reason in failed_subjects:
            print(f"   - {sid}: {reason}")

def process_single_nifti(nifti_path, subject_id, output_directory, slice_index=None):
    img = nib.load(nifti_path)
    data = img.get_fdata()

    # Define plane configurations (name, axis)
    planes = [
        ('axial', 2),
        ('coronal', 1),
        ('sagittal', 0)
    ]

    # Process each plane
    for plane_name, axis in planes:
        # Calculate slice range for current axis
        if slice_index is None:
            center_slice = data.shape[axis] // 2
        else:
            center_slice = slice_index

        start_idx = max(0, center_slice - 7)
        end_idx = min(data.shape[axis], center_slice + 8)

        # Extract and save slices
        for slice_idx in range(start_idx, end_idx):
            if axis == 0:
                slice_data = data[slice_idx, :, :]
            elif axis == 1:
                slice_data = data[:, slice_idx, :]
            else:  # axis == 2
                slice_data = data[:, :, slice_idx]

            save_slice(slice_data, subject_id, nifti_path,
                      output_directory, plane_name, axis, slice_idx)

def save_slice(slice_data, subject_id, nifti_path, output_dir,
              plane_name, axis, slice_idx):
    # Create output paths
    plane_dir = os.path.join(output_dir, plane_name)
    subject_dir = os.path.join(plane_dir, subject_id)
    os.makedirs(subject_dir, exist_ok=True)

    # Generate filename
    base_name = os.path.splitext(os.path.basename(nifti_path))[0]
    filename = f"{base_name}_{plane_name}_slice{slice_idx}.png"
    save_path = os.path.join(subject_dir, filename)

    # Create and save plot
    plt.figure(figsize=(4, 4))
    plt.imshow(np.rot90(slice_data), cmap='gray')
    plt.axis('off')
    plt.title(f"{subject_id}\n{plane_name} slice {slice_idx}")
    plt.savefig(save_path, bbox_inches='tight', pad_inches=0)
    plt.close()

# Define paths
input_directory = '/content/drive/MyDrive/BTP/Preprocessing' 
output_directory = '/content/drive/MyDrive/BTP/skull_strip'  

# Run processing
process_nifti_files(
    main_directory=input_directory,
    output_directory=output_directory,
    slice_index=None  # Uses middle slice for each axis if None
)
