import os
import zipfile


def zip_selected_files(zip_file_path, items_to_zip):
    try:
        with zipfile.ZipFile(zip_file_path, 'w') as zip_file:
            for item in items_to_zip:
                if os.path.isfile(item):
                    # Add individual file to the zip archive
                    zip_file.write(item, os.path.basename(item))
                elif os.path.isdir(item):
                    # Add all files in a directory to the zip archive
                    for foldername, subfolders, filenames in os.walk(item):
                        for filename in filenames:
                            file_path = os.path.join(foldername, filename)
                            arcname = os.path.relpath(file_path, item)
                            zip_file.write(file_path, arcname)
                else:
                    print(f"Ignoring unknown item: {item}")

        print(f"Zip file created successfully: {zip_file_path}")

    except Exception as e:
        print(f"Error creating zip file: {e}")


# Example Usage
zip_file_path = "iot-bm.zip"
items_to_zip = ["api", "config", "core", "database", "model", "modules", "services", "utils", "saved_model"]

zip_selected_files(zip_file_path, items_to_zip)
