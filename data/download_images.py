#!/usr/bin/env python3
"""
Script to download images from URLs in the dataset and organize them 
according to the image path structure.
"""

import json
import os
import requests
import time
import argparse
from pathlib import Path
from urllib.parse import urlparse
import hashlib

def ensure_directory(file_path):
    """
    Ensure that the directory for the given file path exists.
    
    Args:
        file_path (Path): The file path whose directory should be created
    """
    file_path.parent.mkdir(parents=True, exist_ok=True)

def download_image(url, local_path, timeout=30, retries=3):
    """
    Download an image from URL and save it to local path.
    
    Args:
        url (str): URL to download from
        local_path (Path): Local path to save the image
        timeout (int): Request timeout in seconds
        retries (int): Number of retry attempts
        
    Returns:
        bool: True if download successful, False otherwise
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    for attempt in range(retries):
        try:
            print(f"  Downloading from: {url}")
            response = requests.get(url, headers=headers, timeout=timeout, stream=True)
            response.raise_for_status()
            
            # Ensure directory exists
            ensure_directory(local_path)
            
            # Write image data to file
            with open(local_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            
            print(f"  ✓ Successfully saved to: {local_path}")
            return True
            
        except requests.exceptions.RequestException as e:
            print(f"  ✗ Attempt {attempt + 1} failed: {e}")
            if attempt < retries - 1:
                print(f"  Retrying in 2 seconds...")
                time.sleep(2)
            else:
                print(f"  Failed to download after {retries} attempts")
                
        except Exception as e:
            print(f"  ✗ Unexpected error: {e}")
            break
    
    return False

def get_file_extension_from_url(url):
    """
    Try to determine file extension from URL.
    
    Args:
        url (str): The image URL
        
    Returns:
        str: File extension (with dot), defaults to '.png'
    """
    parsed = urlparse(url)
    path = parsed.path.lower()
    
    # Common image extensions
    for ext in ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp']:
        if path.endswith(ext):
            return ext
    
    # Default to PNG if can't determine
    return '.png'

def download_dataset_images(dataset_file, base_download_dir="downloaded_images", resume=True):
    """
    Download all images from the dataset and organize them according to image paths.
    
    Args:
        dataset_file (str): Path to the JSONL dataset file
        base_download_dir (str): Base directory for downloaded images
        resume (bool): Whether to skip already downloaded files
        
    Returns:
        dict: Statistics about the download process
    """
    base_path = Path(base_download_dir)
    
    stats = {
        'total': 0,
        'successful': 0,
        'failed': 0,
        'skipped': 0
    }
    
    print(f"Starting image download process...")
    print(f"Dataset file: {dataset_file}")
    print(f"Download directory: {base_path.absolute()}")
    print(f"Resume mode: {resume}")
    print("-" * 60)
    
    try:
        with open(dataset_file, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                try:
                    data = json.loads(line.strip())
                    image_path = data.get('image', '')
                    image_url = data.get('image_url', '')
                    
                    if not image_path or not image_url:
                        print(f"Line {line_num}: Missing image path or URL, skipping")
                        continue
                    
                    stats['total'] += 1
                    
                    # Create local file path based on the image path from dataset
                    local_file_path = base_path / image_path
                    
                    # Check if file already exists and resume is enabled
                    if resume and local_file_path.exists():
                        print(f"[{line_num}] Skipping existing file: {local_file_path}")
                        stats['skipped'] += 1
                        continue
                    
                    print(f"[{line_num}] Processing: {image_path}")
                    
                    # Download the image
                    if download_image(image_url, local_file_path):
                        stats['successful'] += 1
                    else:
                        stats['failed'] += 1
                    
                    # Small delay to be respectful to the server
                    time.sleep(0.5)
                    
                except json.JSONDecodeError as e:
                    print(f"Line {line_num}: JSON decode error - {e}")
                    continue
                except Exception as e:
                    print(f"Line {line_num}: Unexpected error - {e}")
                    continue
                    
                # Print progress every 50 items
                if stats['total'] % 50 == 0:
                    print(f"\nProgress: {stats['total']} processed, {stats['successful']} successful, {stats['failed']} failed, {stats['skipped']} skipped\n")
                    
    except FileNotFoundError:
        print(f"Error: Dataset file '{dataset_file}' not found")
        return stats
    except Exception as e:
        print(f"Error reading dataset file: {e}")
        return stats
    
    return stats

def print_download_summary(stats):
    """
    Print a summary of the download process.
    
    Args:
        stats (dict): Download statistics
    """
    print("\n" + "=" * 60)
    print("DOWNLOAD SUMMARY")
    print("=" * 60)
    print(f"Total entries processed: {stats['total']}")
    print(f"Successfully downloaded: {stats['successful']}")
    print(f"Failed downloads: {stats['failed']}")
    print(f"Skipped (already exist): {stats['skipped']}")
    
    if stats['total'] > 0:
        success_rate = (stats['successful'] / stats['total']) * 100
        print(f"Success rate: {success_rate:.1f}%")
    
    print("=" * 60)

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Download images from URLs in the dataset and organize them according to image paths."
    )
    parser.add_argument(
        "--input", 
        required=True,
        help="Path to the input JSONL dataset file containing image URLs and paths"
    )
    parser.add_argument(
        "--output-dir", 
        default="downloaded_images",
        help="Output directory for downloaded images (default: downloaded_images)"
    )
    parser.add_argument(
        "--resume", 
        action="store_true",
        help="Resume download by skipping existing files"
    )
    parser.add_argument(
        "--no-resume", 
        action="store_true",
        help="Don't resume, re-download existing files"
    )
    return parser.parse_args()

def main():
    # Parse command line arguments
    args = parse_args()
    
    # Determine resume mode
    if args.no_resume:
        resume = False
    elif args.resume:
        resume = True
    else:
        # Default to resume mode
        resume = True
    
    # Check if input file exists
    input_file = Path(args.input)
    if not input_file.exists():
        print(f"Error: Input file '{input_file}' not found.")
        return 1
    
    print("Image Download Script")
    print("=" * 40)
    print(f"Input file: {input_file}")
    print(f"Output directory: {args.output_dir}")
    print(f"Resume mode: {resume}")
    print()
    
    # Start download process
    start_time = time.time()
    stats = download_dataset_images(str(input_file), args.output_dir, resume)
    end_time = time.time()
    
    # Print summary
    print_download_summary(stats)
    print(f"Total time: {end_time - start_time:.1f} seconds")
    
    # Check downloaded directory structure
    download_path = Path(args.output_dir)
    if download_path.exists():
        print(f"\nDownloaded images are organized in: {download_path.absolute()}")
        
        # Show directory structure
        subdirs = [d for d in download_path.iterdir() if d.is_dir()]
        if subdirs:
            print("Directory structure:")
            for subdir in sorted(subdirs):
                image_count = len(list(subdir.glob("**/*.png"))) + len(list(subdir.glob("**/*.jpg"))) + len(list(subdir.glob("**/*.jpeg")))
                print(f"  {subdir.name}/: {image_count} images")
    
    return 0

if __name__ == "__main__":
    main()
