#!/bin/bash

# this is a script to organize CSV files by archiving them with timestamps


# generating the timestamp
generate_timestamp() {
    date +"%Y%m%d-%H%M%S"
}

#this is to log actions
log_action() {
    local message="$1"
    local timestamp=$(date +"%Y-%m-%d %H:%M:%S")
    echo "[$timestamp] $message" >> organizer.log
}

# Function to archive CSV files
archive_csv_files() {
    local archive_dir="archive"
    
    # Create archive directory if it doesn't exist
    if [ ! -d "$archive_dir" ]; then
        mkdir "$archive_dir"
        log_action "Archive directory...: $archive_dir"
        echo "Archive directory has been created: $archive_dir"
    else
        echo "The archive directory is already existng: $archive_dir"
    fi
    
    # fetching for all CSV files in current directory
    local csv_files=$(find . -maxdepth 1 -name "*.csv" -type f)
    
    if [ -z "$csv_files" ]; then
        echo "OOPS!!No CSV files found "
        log_action "There was no CSV files found for archiving!"
        return
    fi
    
    # Processing each CSV file
    echo "We are currently processing the CSV files, please hold on...."
    
    for file in $csv_files; do
        # Skips if it's the archive directory itself
        if [ "$file" = "./$archive_dir" ]; then
            continue
        fi
        
        # retrieving filename without path
        local filename=$(basename "$file")
        
        # Generating the timestamp and new filename
        local timestamp=$(generate_timestamp)
        local new_filename="${filename%.*}-${timestamp}.csv"
        
        # Log the archiving action with file content
        log_action "Archiving file: $filename -> $new_filename"
        log_action "File content of $filename:"
        cat "$file" >> organizer.log
        echo "--- THIS IS THE END OF THE FILE: $filename ---" >> organizer.log
        
        # Move and rename the file
        mv "$file" "$archive_dir/$new_filename"
        
        if [ $? -eq 0 ]; then
             echo "Succesfully Archived: $filename -> $archive_dir/$new_filename"
            log_action "Successfully moved $filename to $archive_dir/$new_filename"
        else
              echo "Oops!! we failed to archive: $filename"
              log_action "Oops!! we failed to move $filename to $archive_dir/$new_filename"
        fi
    done
    
      echo "The archiving has been successfully completed!"
    log_action "Archiving process completed successfully!"
}

# Main execution
main() {
        echo "YOU HAVE REACHED THE CSV FILE ORGANIZER"
      echo "African Leadership University - BSE Year 1 Trimester 2"
    echo "**************************************************"
     
   
    
    # Initializing log file
    echo "--- THE ORGANIZER LOG HAS STARTED ---" > organizer.log
      log_action "Organizer script started"
    
    # Displaying all files in current directory
    echo "These are the current directory contents:"
     ls -la
    
    # call archive CSV files
      archive_csv_files
    
    # Displaying the structure after archiving
    echo ""
         echo "Final structure of directories:"
    ls -la
    
    if [ -d "archive" ]; then
        echo ""
        echo "These are the archive directory contents:"
        ls -la archive/
    fi
    
    echo ""
     echo "The log file has been created: organizer.log"
    log_action "Organizer script completed"
    
    echo "************************************************"
    echo "The organizer script has been completed successfully!"
}

# Run main function
main "$@"