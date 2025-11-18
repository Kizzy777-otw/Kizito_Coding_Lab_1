# Lab 1: Grade Generator Calculator

## the overview:
This project is made of two parts:
1. **the python Application** (`grade-generator.py`): Interactive grade calculator
2. **the bash Script** (`organizer.sh`): CSV file organizer and archiver

## Files:
- `grade-generator.py` : this is the main Python application
- `organizer.sh` : this is a bash script for archiving
- `grades.csv` : this is an output file created right after running grade generator
- `organizer.log` :this is a log file created right after running organizer

## Part 1: Grade Generator (Python)

### Features
- validation of grade range (0-100)
- checking category(FA/SA)
- checking weight (positive numbers)
- calculating weighted grades
- total from each category (Formative/Summative)
- calculating final grade and GPA
- determining Pass/Fail status
- generating summary

### how to use?
```bash
python3 grade-generator.py