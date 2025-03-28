import os
import hashlib
import json
from collections import defaultdict
from tqdm import tqdm

def get_file_hash(file_path, chunk_size=8192):
    """Calculate file hash using SHA-256 algorithm"""
    hasher = hashlib.sha256()
    try:
        with open(file_path, 'rb') as f:
            while chunk := f.read(chunk_size):
                hasher.update(chunk)
        return hasher.hexdigest()
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return None

def find_duplicate_files(directory, ignored_dirs):
    """Search for duplicate files in the specified directory while ignoring user-specified folders"""
    file_hashes = defaultdict(list)
    all_files = []

    for root, _, files in os.walk(directory):
        if any(root.startswith(os.path.normpath(ignored)) for ignored in ignored_dirs):
            continue  # پرش از این دایرکتوری و زیرشاخه‌های آن

        for file in files:
            file_path = os.path.join(root, file)
            all_files.append(file_path)

    total_files = len(all_files)

    with tqdm(total=total_files, desc="Scanning Files", unit="file") as pbar:
        for file_path in all_files:
            file_hash = get_file_hash(file_path)
            if file_hash:
                file_hashes[file_hash].append(file_path)
            pbar.update(1)

    duplicates = {hash_val: paths for hash_val, paths in file_hashes.items() if len(paths) > 1}
    return duplicates

def save_results(duplicates, output_file="duplicates.json"):
    """Save duplicate file results to a JSON file"""
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(duplicates, f, indent=4)
        print(f"Results saved to {output_file}")
    except Exception as e:
        print(f"Error saving results: {e}")

def show_results_console(duplicates):
    """Display duplicate file results in the console"""
    if duplicates:
        for hash_val, files in duplicates.items():
            print("\n".join(files))
            print("-" * 40)
    else:
        print("No duplicate files found.")

def main():
    directory = input("Enter the target directory path: ").strip()
    
    ignored_dirs = set()
    ignore_choice = input("Do you want to ignore specific directories? (yes/no): ").strip().lower()

    if ignore_choice in ("yes", "y"):
        print("Enter directories to ignore (one per line). Type 'done' when finished:")
        while True:
            path = input("Ignore path: ").strip()
            if path.lower() == "done":
                break
            ignored_dirs.add(os.path.normpath(path))

    duplicates = find_duplicate_files(directory, ignored_dirs)
    save_results(duplicates)
    show_results_console(duplicates)
    
    print("Duplicate file scan completed. Results saved to duplicates.json")

if __name__ == "__main__":
    main()
