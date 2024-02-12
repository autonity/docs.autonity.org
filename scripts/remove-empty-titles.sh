#!/bin/bash

# problem: empty title fields in front matter cause quarto to fail compilation
# solution: remove empty title fields

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

  # grab the line number
  local frontmatter_line=$(sed -n '/^---$/,/^---$/p' "$file" | grep -n "^title:" | cut -d':' -f1)

  if [ -n "$frontmatter_line" ]; then
    local line_number=$(( frontmatter_line + 1 ))

    # get the value of the title field
    local title_value=$(sed -n "${line_number}p" "$file" | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//')

    # if the title field is empty, remove it
    if [ -z "$title_value" ]; then
      sed -i '' "/^title:/d" "$file"
      echo "Removed 'title' field from $file"
    fi
  fi
}

echo "Checking and removing empty 'title' fields in .md files ..."

process_files "$(pwd)"

echo "Processing complete!"
