#!/bin/bash

# Function to process files recursively
process_files() {
  for file in "$1"/*; do
    if [ -d "$file" ]; then
      process_files "$file"   # Recursively call function for subdirectories
    elif [ "${file##*.}" == "md" ]; then
      process_file "$file"    # Process individual Markdown file
    fi
  done
}

# Function to process individual Markdown file
process_file() {
  local file="$1"

  # Check if the file contains front matter
  if sed -n '/^---$/,/^---$/p' "$file" | grep -q "^---$"; then
    # Look for "weight" and "linkTitle" in the front matter and remove those lines if found
    sed -i'.bak' -e '/^weight:/d' -e '/^linkTitle:/d' "$file"
    echo "Processed $file"

    # remove backup file
    rm "${file}.bak"
  fi
}

echo "Checking and removing 'weight' and 'linkTitle' fields in .md files ..."

process_files "$(pwd)"

echo "Processing complete!"
