// Import the required modules
const fs = require('fs');
const path = require('path');
const glob = require('glob');

// Regex pattern to match the tab block, capture header attribute and contents
const tabPattern = /{{<\s*tab\s+header="([^"]+)"\s*>}}([\s\S]*?){{<\s*\/tab\s*>}}/g;

// Replacement format
//const startReplacement = header => `::: {.panel-tabset}\n## ${header}\n`;
const startReplacement = header => `::: {.panel-tabset}\n## bash\n`;
const endReplacement = '\n:::';

// Find all .md files in the current directory and its subdirectories
glob("**/*.md", function (err, files) {
  if (err) {
    console.error("Error while finding files:", err);
    return;
  }

  files.forEach(function (file) {
    console.log(`Processing: ${file}`);
    // Read the file
    fs.readFile(file, 'utf8', function (err, data) {
      if (err) {
        console.error("Error while reading file:", err);
        return;
      }

      // Replace all occurrences of the tab patterns with the new format
      let newData = data.replace(tabPattern, function(match, header, content) {
        return startReplacement(header) + content.trim() + endReplacement;
      });

      // Write the new data back to the file
      fs.writeFile(file, newData, 'utf8', function (err) {
        if (err) {
          console.error("Error while writing to file:", err);
        } else {
          console.log(`Successfully updated: ${file}`);
        }
      });
    });
  });
});
