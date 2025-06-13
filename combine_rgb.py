import micasense.capture as capture

# Paths to the individual band images
BAND_FILES = [
    'data/REDEDGE-MX/IMG_0001_1.tif',
    'data/REDEDGE-MX/IMG_0001_2.tif',
    'data/REDEDGE-MX/IMG_0001_3.tif',
]

# Output RGB filename
OUTPUT_FILE = 'IMG_0001_RGB.jpg'


def main():
    # Create a Capture object from the list of band files
    cap = capture.Capture.from_filelist(BAND_FILES)

    # Align the images (computes radiance if needed)
    cap.create_aligned_capture()

    # Save the aligned stack as an RGB composite
    cap.save_capture_as_rgb(OUTPUT_FILE)
    print(f'Saved RGB image to {OUTPUT_FILE}')


if __name__ == '__main__':
    main()

