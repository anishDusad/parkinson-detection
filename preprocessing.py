import os
import nibabel as nib
import numpy as np
from scipy.ndimage import gaussian_filter
import ants
from antspynet.utilities import brain_extraction

# Define paths and directories
input_dir = "/content/drive/MyDrive/BTP/UP1"     
output_dir = "/content/drive/MyDrive/BTP/PP1"  

# Create the output folder if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Load the MNI template once for consistency
mni_template_path = ants.get_ants_data('mni')
mni_template = ants.image_read(mni_template_path)
mni_nib = nib.load(mni_template_path)  # Load via nibabel to extract the affine

# Process each subject folder and file
for subject_id in os.listdir(input_dir):
    subject_path = os.path.join(input_dir, subject_id)
    if os.path.isdir(subject_path):
        # Create subject-specific output folder
        subject_output_dir = os.path.join(output_dir, subject_id)
        if not os.path.exists(subject_output_dir):
            os.makedirs(subject_output_dir)

        for file in os.listdir(subject_path):
            if file.endswith(".nii") or file.endswith(".nii.gz"):
                input_file = os.path.join(subject_path, file)

                print(f"Processing subject {subject_id}, file: {file}")

                # Load the image using ANTs
                raw_img = ants.image_read(input_file, reorient=True)

                # Skull Stripping using deep-learning brain extraction
                # Choose modality as appropriate: for example, 't1' for structural or 'bold' for functional images
                prob_brain_mask = brain_extraction(raw_img, modality='t1', verbose=True)
                # Create a binary mask from the probabilistic mask
                brain_mask = ants.get_mask(prob_brain_mask, low_thresh=0.5)
                # Apply the binary mask to obtain the skull stripped image
                skull_stripped_img = ants.mask_image(raw_img, brain_mask)

                # ---------------------------
                # Normalization (Registration) to the MNI Template
                # ---------------------------
                norm = ants.registration(fixed=mni_template, moving=skull_stripped_img, type_of_transform='SyN')
                warped_image = norm['warpedmovout']

                # ---------------------------
                # Smoothing the normalized image
                # ---------------------------
                # Convert the warped image to a numpy array, ensuring float32
                try:
                    norm_data = warped_image.numpy()
                except AttributeError:
                    norm_data = ants.get_data(warped_image)
                norm_data = np.array(norm_data).astype(np.float32)

                # Apply Gaussian smoothing (approximate FWHM = 6 mm, sigma ≈ 6 / 2.355)
                smoothed_data = gaussian_filter(norm_data, sigma=6/2.355)

                # Create the final preprocessed NIfTI image using the affine from the MNI template
                preprocessed_img = nib.Nifti1Image(smoothed_data, mni_nib.affine)
                preprocessed_file = os.path.join(subject_output_dir, "preprocessed.nii.gz")
                nib.save(preprocessed_img, preprocessed_file)

                print(f"Preprocessing complete for subject: {subject_id}, file: {file}")

print("🎉 All subjects processed successfully!")
