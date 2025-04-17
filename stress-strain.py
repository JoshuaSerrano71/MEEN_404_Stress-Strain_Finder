import csv
import math
import os
import sys
import pandas as pd

def calculate_stress_strain(experimental_data_path, dimension_data_path):
    try:
        # Load the experimental data CSV file
        experimental_data = pd.read_csv(experimental_data_path)

        # Load the dimension data CSV file
        dimension_data = pd.read_csv(dimension_data_path)

        # Example: Merge data based on sample number (replace with your actual logic)
        data = pd.merge(experimental_data, dimension_data, on="Sample")

        # Example: Calculate stress and strain (replace with your actual logic)
        data["Stress (MPa)"] = data["Force (kN)"] * 1000  # Example calculation
        data["Strain (mm/mm)"] = data["Displacement (mm)"] / data["Height (mm)"]

        # Return the results as a string
        return data.to_string()
    except Exception as e:
        return f"Error processing data: {e}"

if __name__ == "__main__":
    # Check if the correct number of arguments is provided
    if len(sys.argv) != 3:
        print("Usage: python stress-strain.py <experimental_data_csv> <dimension_data_csv>")
        sys.exit(1)

    # Get the file paths from the command-line arguments
    input_file = sys.argv[1]
    dimension_file = sys.argv[2]

    # Calculate stress and strain
    results = calculate_stress_strain(input_file, dimension_file)

    # Print the results
    print(results)

script_dir = os.path.dirname(os.path.abspath(__file__))  # Directory of the script
output_file = os.path.join(script_dir, 'stress-strain.csv')  # Full path to output file

try:
    # Step 1: Read sample dimensions from specimen_dimension.csv
    dimensions = {}
    if not os.path.exists(dimension_file):
        raise FileNotFoundError(f"Dimension file not found: {dimension_file}")
    with open(dimension_file, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row
        for row in reader:
            sample_number = int(row[0])
            diameter = float(row[1])
            height = float(row[2])
            dimensions[sample_number] = {'diameter': diameter, 'height': height}
            #print(f"Sample {sample_number}: Diameter = {diameter} mm, Height = {height} mm")

    # Step 2: Initialize a dictionary to store data for each sample
    samples = {}

    # Step 3: Read displacement and force data from the input file
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Input file not found: {input_file}")
    with open(input_file, 'r') as file:
        reader = csv.reader(file)
        sample_number = 0
        for row in reader:
            # Check if the row indicates the start of a new sample
            if "Time" in row and "Displacement" in row and "Force" in row:
                sample_number += 1
                samples[sample_number] = {
                    'displacement': [],
                    'force': [],
                    'height': dimensions.get(sample_number, {}).get('height'),
                    'diameter': dimensions.get(sample_number, {}).get('diameter')
                }
                print(f"New sample detected: Sample {sample_number}")
            # Check if the row contains displacement and force data
            elif len(row) >= 4 and row[1].replace('.', '', 1).isdigit():
                # Extract displacement (Column C) and force (Column D) values
                displacement = float(row[2])  # Column C: Displacement (mm)
                force = float(row[3])  # Column D: Force (kN)
                samples[sample_number]['displacement'].append(displacement)
                samples[sample_number]['force'].append(force)
                #print(f"Sample {sample_number}: Displacement = {displacement}, Force = {force}")

    # Step 4: Function to calculate engineering stress (MPa)
    def calculate_stress(force, diameter):
        if diameter is None:
            raise ValueError(f"Diameter is None for force = {force}")
        area = math.pi * ((diameter / 2) ** 2)  # Cross-sectional area in mm²
        stress = (force * 1000) / area  # Convert kN to N and calculate stress in MPa
        return stress

    # Step 5: Function to calculate engineering strain (%)
    def calculate_strain(displacement, height):
        if height is None:
            raise ValueError(f"Height is None for displacement = {displacement}")
        strain = (displacement / height) * 100  # Strain in %
        return strain

    # Step 6: Initialize a list to store stress and strain data for all samples
    stress_strain_data = []

    # Step 7: Calculate stress and strain for each sample
    for sample in samples:
        height = samples[sample]['height']
        diameter = samples[sample]['diameter']
        displacements = samples[sample]['displacement']
        forces = samples[sample]['force']
        stress_strain_data.append([])
        if diameter is None or height is None:
            print(f"Warning: Sample {sample} is missing dimensions. Skipping calculations.")
            continue  # Skip this sample if dimensions are missing
        for i in range(len(displacements)):
            try:
                stress = calculate_stress(forces[i], diameter)
                strain = calculate_strain(displacements[i], height)
                stress_strain_data[-1].append((stress, strain))
                #print(f"Sample {sample}: Stress = {stress} MPa, Strain = {strain} %")
            except ValueError as e:
                print(f"Error in Sample {sample}: {e}")
                stress_strain_data[-1].append((None, None))  # Append None values if calculation fails

    # Step 8: Determine the maximum number of rows across all samples
    max_rows = max(len(data) for data in stress_strain_data)

    # Step 9: Write the stress and strain data to a new CSV file
    try:
        with open(output_file, 'w', newline='') as file:
            writer = csv.writer(file)
            # Write header row
            headers = []
            for sample in samples:
                headers.extend([f'Sample {sample} Stress (MPa)', f'Sample {sample} Strain (%)'])
            writer.writerow(headers)
            # Write data rows
            for i in range(max_rows):
                row = []
                for sample_data in stress_strain_data:
                    if i < len(sample_data):
                        row.extend(sample_data[i])
                    else:
                        row.extend(['', ''])  # Fill with empty values if the sample has fewer rows
                writer.writerow(row)
        print(f"Stress and strain data have been written to {output_file}")
    except PermissionError:
        print(f"Permission denied: Could not write to {output_file}. Ensure the file is not open in another program and you have write permissions.")
    except Exception as e:
        print(f"An error occurred while writing to {output_file}: {e}")

except FileNotFoundError as e:
    print(e)
except Exception as e:
    print(f"An unexpected error occurred: {e}")