#!/usr/bin/env python3

# The #!/usr/bin/env python3 is called a shebang line. 
# It tells the operating system to use the Python 3 interpreter to run this script. 
# This is important because it ensures that the script will be executed with the correct version of Python,
# regardless of the user's environment or default settings.

"""

Script to generate ArUco markers using OpenCV.
Run this script from: workspace_aruco/src/aruco_detector_pkg/scripts/aruco_generator.py

Author: Imad Jared Cabrera Trejo
Contact: cabreratrejoimadjared@gmail.com
Team: VespoUAV

"""

import sys

import cv2 # OpenCV library for computer vision tasks
import cv2.aruco as aruco # Submodule of OpenCV for ArUco marker detection/generation
import os # Operating system interface for file and directory operations (because we will be saving the generated markers)
from pathlib import Path # Pathlib module for object-oriented filesystem paths (to handle file paths in a more intuitive way)

def save_aruco_markers(markers_ids, aruco_dict, marker_size, path):
    """
    Function to generate and save ArUco markers based on the provided marker IDs.
    
    Parameters:
    - markers_ids: List of marker IDs to generate.
    - aruco_dict: The ArUco dictionary to use for marker generation.
    - marker_size: Size of the markers in pixels.
    """
    for marker_id in markers_ids:
        # Generate the marker image using the ArUco dictionary and the specified size in pixels
        generated_img = aruco.generateImageMarker(aruco_dict, marker_id, marker_size)

        # Now that the image is generated, we save it to the specified path using cv2.imwrite()
        # The filename is constructed using the marker ID (i) and the .png extension
        filename = path / f"aruco_{marker_id}.png"

        # We cast filename to str because cv2.imwrite() accepts only str as input, not a Path object managed by pathlib
        success = cv2.imwrite(str(filename), generated_img)
        if success:
            print(f"Marker {marker_id} generated and saved as {filename}")
        else:
            print(f"Failed to save marker {marker_id}")

def generate_aruco_marker():

    # obtain the ArUco dictionary (DICT_5X5_100 is a predefined dictionary of 100 markers with a 5x5 grid)
    # 5x5 because of TMR's rules, see -> https://femexrobotica.org/tmr2026/index.php/categorias/categorias-fmr/drones-autonomos/
    aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_5X5_100)

    # Start the menu
    # We use ANSI escape codes to format the text in the console.
    # \033[1m makes the text bold, \033[34m sets the text color to blue, and \033[0m resets the formatting to default.
    print("\033[1m\033[34m-----VespoUAV Aruco Marker Generator-----\033[0m")

    # Generate a sample marker to display in the console (for visual reference)
    img = aruco.generateImageMarker(aruco_dict, 0, 25)
    img_matrix = img // 255
    for row in img_matrix:
        print("".join("██" if pixel else "  " for pixel in row))

    print("Family: DICT_5X5_100")

    # Question 1.
    while True:
        try:
            # Get user input for the number of markers to generate
            num_markers = int(input("How many markers do you want to generate? (1-100): "))

            # Validate the input to ensure it's within the acceptable range (1-100)
            if(num_markers >= 1 and num_markers <= 100):
                break
            else:
                print("Please enter a number between 1 and 100.")
        except ValueError:
            # Handle the case where the input is not a valid integer
            print("Invalid input. Please enter a valid integer.")
            continue

    # Question 2.
    while True:
        # Get user input for the size of the markers in pixels
        try:
            print("The size of the markers is in pixels, for example 100 means 100x100 pixels")
            marker_size = int(input("What size do you want the markers to be? (in pixels): "))
            break
        except ValueError:
            # Handle the case where the input is not a valid integer
            print("Invalid input. Please enter a valid integer.")
            continue

    # Question 3.
    while True:
        #Ask the user if they want consecutive markers or not,
        # example consecutive markers: 0,1,2,3,4,5,6,7,8,9,10
        # the other option will trigger a submenu to ask for the specific marker IDs to generate
        # the method .lower is used to convert the input to lowercase so Y and y are treated the same
        # finally the method .strip is used to remove any blank spaces
        consecutive = input("Do you want the markers to be consecutive? (y/n): ").lower().strip()

        # In this case there is no exception handling because we manually handle the exception
        # by checking the input and ensure it never throws an exception.
        # this while is only to ensure the user inputs a valid option, 
        # if not it will keep asking until a valid option is given

        if(consecutive == "y"):
            break
        elif(consecutive == "n"):
            break

        else:
            print("Invalid input. Please enter 'y' or 'n'.")
            continue


    # We initialize our absolute path models/aruco_markers/textures
    # We use Path(__file__).parent.parent to get the parent directory of the current script's directory,
    # we go back two levels (cd .. and cd ..) to reach the root package (aruco_detector_pkg)
    # then we navigate to the models/aruco_markers/textures directory.
    path = Path(__file__).parent.parent / "models" / "aruco_markers" / "textures"
                
    # Now we check if the directory exists, if not we create it using mkdir()
    path.mkdir(parents=True, exist_ok=True)

    # Now we check if the user wants consecutive markers or not
    if (consecutive == "y"):
        save_aruco_markers(range(num_markers), aruco_dict, marker_size, path)
    else:
        # if the user does not want consecutive markers, we ask for specific marker IDs to generate

        # Question 4. (submenu for consecutive markers)
        while True:
            # Step1. Ask the user to input specific marker IDs separated by commas
            try:

                print(f"\033[1m\033[34m----You have chosen to generate {num_markers} specific markers. Please enter the marker IDs you want to generate.----\033[0m")
                print("Note: Marker IDs must be between 0 and 99, and duplicates are not allowed.")
                marker_ids_input = input(f"Please enter the specific marker IDs you want to generate (separated by commas, e.g., 1,2,3): ")
                # Step2. Process / validate the input

                # Split the input string by commas, strip whitespace, and convert to integers (if not empty)
                marker_ids = [int(id.strip()) for id in marker_ids_input.split(",") if id.strip()]

                # Step3. If valid, we break the loop (all IDs are between 0 and 99)
                # we will generate the markers outside of this loop, so we only need to validate the input here

                # First validation, if the markers are in the range of 0 to 99
                markers_inrange = all(id >= 0 and id <= 99 for id in marker_ids)
                # Second validation, duplicate IDs are not allowed
                has_duplicates = len(marker_ids) != len(set(marker_ids)) # set removes duplicates, 
                # so if the lengths are different, there are duplicates

                # Third validation, if the number of markers is exactly the same as the number of markers requested by the user
                is_correct_number = len(marker_ids) == num_markers # here we dont use set because for total validation 
                # the duplicates one will throw false so the validation will not be completed           

                if (markers_inrange and not has_duplicates and is_correct_number):
                    break # all validations passed, we can break the loop and generate the markers
                
                else:
                    # Step4. If not valid, we print an error message and ask again
                    if not markers_inrange:
                        print("Error: All marker IDs must be between 0 and 99.")
                    if has_duplicates:
                        print("Error: Duplicate marker IDs are not allowed.")
                    if not is_correct_number:
                        print(f"Error: You must enter exactly {num_markers} marker IDs.")
                    continue
            
            except ValueError:
                # Handle the case where the input is not a valid integer
                print("Invalid input. Please enter valid integers separated by commas.")
                continue

        # Now that we have valid marker IDs, we can generate the markers
        save_aruco_markers(marker_ids, aruco_dict, marker_size, path)

    print("\033[1m\033[34m-----Marker generation completed. Check the 'models/aruco_markers/textures' directory for the generated markers.-----\033[0m")

    sys.exit(0) # Exit the script with a success status code (0) to indicate that the script has completed successfully

if __name__ == "__main__":
    generate_aruco_marker() # Call the function to generate the ArUco marker when the script is run directly