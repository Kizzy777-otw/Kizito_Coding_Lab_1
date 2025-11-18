#!/usr/bin/env python3
"""
Grade Generator Calculator

This script calculates a student's final grade by interactively collecting
assignment details, performing validations, and exports the data to CSV.
"""

import csv
from datetime import datetime


class GradeCalculator:
    """grade calculations and data management"""
    
    def __init__(self):
        self.assignments = []
        self.total_formative = 0
        self.total_summative = 0
        self.fa_weight_total = 0
        self.sa_weight_total = 0
        
    def validate_grade(self, grade):
        """Check if grade is between 0 and 100"""
        try:
            grade_float = float(grade)
            if 0 <= grade_float <= 100:
                return True, grade_float
            else:
                return False, 
        except ValueError:
            return False, "grade is only a number"
    
    def validate_category(self, category):
        """check if category is summative or formative"""
        category_upper = category.upper()
        if category_upper in ['FA', 'SA']:
            return True, category_upper
        else:
            return False, "category must be 'FA' (formative) or 'SA' (summative)"
    
    def validate_weight(self, weight):
        """weight must be a positive number"""
        try:
            weight_float = float(weight)
            if weight_float > 0:
                return True, weight_float
            else:
                return False, "the weight must be a positive number"
        except ValueError:
            return False, "weight must be a number"
    
    def get_assignment_input(self):
        """Collect and assignment details from user"""
        print("\n" + "*"*50)
        print("ENTER YOUR ASSIGNMENT DETAILS")
        print("*"*50)
        
        # Assignment Name
        assignment_name = input("Assignment Name: ").strip()
        while not assignment_name:
            print("Oops!! please enter assignment ")
            assignment_name = input("Enter assignment Name: ").strip()
        
        # Category
        category = input("Category (FA for Formative, SA for Summative): ").strip()
        is_valid_category, category_result = self.validate_category(category)
        while not is_valid_category:
            print(f"Oops!! Error: {category_result}")
            category = input("Make sure category is FA for Formative and SA for Summative: ").strip()
            is_valid_category, category_result = self.validate_category(category)
        
        # Grade
        grade = input("Grade Obtained (0-100): ").strip()
        is_valid_grade, grade_result = self.validate_grade(grade)
        while not is_valid_grade:
            print(f"Oops!! Error: {grade_result}")
            grade = input("PLEASE ENTER THE GRADE YOU OBTAINED (0-100): ").strip()
            is_valid_grade, grade_result = self.validate_grade(grade)
        
        # Weight
        weight = input("ENTER WEIGHT (e.g: 30): ").strip()
        is_valid_weight, weight_result = self.validate_weight(weight)
        while not is_valid_weight:
            print(f"Error: {weight_result}")
            weight = input("PLEASE ENTER WEIGHT (e.g: 30): ").strip()
            is_valid_weight, weight_result = self.validate_weight(weight)
        
        return {
            'name': assignment_name,
            'category': category_result,
            'grade': grade_result,
            'weight': weight_result
        }
    
    def add_assignment(self, assignment):
        """Add updating totals ans adding assignment to list"""
        self.assignments.append(assignment)
        
        # Calculate weighted grade
        weighted_grade = (assignment['grade'] / 100) * assignment['weight']
        
        # Update totals
        if assignment['category'] == 'FA':
            self.total_formative += weighted_grade
            self.fa_weight_total += assignment['weight']
        else:  # SA
            self.total_summative += weighted_grade
            self.sa_weight_total += assignment['weight']
    
    def calculate_final_grade(self):
        """ final grade and GPA"""
        total_grade = self.total_formative + self.total_summative
        gpa = (total_grade / 100) * 5.0 if total_grade > 0 else 0
        
        return total_grade, gpa
    
    def check_pass_fail(self):
        """Checking if student has passed based on criteria"""
        fa_required = self.fa_weight_total * 0.5  # 50% of FA weight
        sa_required = self.sa_weight_total * 0.5  # 50% of SA weight
        
        fa_pass = self.total_formative >= fa_required if self.fa_weight_total > 0 else True
        sa_pass = self.total_summative >= sa_required if self.sa_weight_total > 0 else True
        
        return fa_pass and sa_pass, fa_required, sa_required
    
    def print_summary(self):
        """Print summary of grades and status"""
        total_grade, gpa = self.calculate_final_grade()
        pass_status, fa_required, sa_required = self.check_pass_fail()
        
        print("\n" + "^"*60)
        print("GRADE SUMMARY")
        print("*"*60)
        
        # Assignment details
        print("\nASSIGNMENT DETAILS:")
        print("*" * 40)
        for i, assignment in enumerate(self.assignments, 1):
            weighted_grade = (assignment['grade'] / 100) * assignment['weight']
            print(f"{i}. {assignment['name']} ({assignment['category']})")
            print(f"   Grade: {assignment['grade']}% | Weight: {assignment['weight']}%")
            print(f"   Weighted: {weighted_grade:.2f}%")
        
        # Category totals
        print("\nCATEGORY TOTALS:")
        print("*" * 40)
        print(f"Formative (FA): {self.total_formative:.2f}% / {self.fa_weight_total}%")
        print(f"Summative (SA): {self.total_summative:.2f}% / {self.sa_weight_total}%")
        
        # Final results
        print("\nFINAL RESULTS:")
        print("_" * 40)
        print(f"Total Grade: {total_grade:.2f}%")
        print(f"GPA: {gpa:.2f} / 5.0")
        
        # Pass/Fail status
        status = "PASS" if pass_status else "FAIL"
        status_color = "\033[92m" if pass_status else "\033[91m"  # Green for pass, red for fail
        print(f"\nStatus: {status_color}{status}\033[0m")
        
        if not pass_status:
            print("\nREQUIRED FOR PASSING:")
            if self.total_formative < fa_required:
                print(f"YOU HAVE FAILED YOUR FORMATIVE: You need {fa_required:.2f}%, You have {self.total_formative:.2f}%")
            if self.total_summative < sa_required:
                print(f"YOU HAVE FAILED YOUR SUMMATIVE: You need {sa_required:.2f}%, You have {self.total_summative:.2f}%")
    
    def export_to_csv(self):
        """Exporting data to CSV file"""
        filename = "grades.csv"
        
        try:
            with open(filename, 'w', newline='') as csvfile:
                fieldnames = ['Assignment', 'Category', 'Grade', 'Weight']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                writer.writeheader()
                for assignment in self.assignments:
                    writer.writerow({
                        'Assignment': assignment['name'],
                        'Category': assignment['category'],
                        'Grade': assignment['grade'],
                        'Weight': assignment['weight']
                    })
            
            print(f"\n The data has been succesfully exported to {filename}")
            return True
            
        except Exception as e:
            print(f"\nOOPS!! Error exporting to CSV: {e}")
            return False


def main():
    """Main function to run the grade calculator"""
    print("YOU HAVE MADE IT TO THE GRADE GENERATOR CALCULATOR!")
    print("ALU Year 1 Trimester 2, BSE")
    print("_" * 50)
    
    calculator = GradeCalculator()
    
    # Main input loop
    while True:
        assignment = calculator.get_assignment_input()
        calculator.add_assignment(assignment)
        
        # Ask if user wants to add another assignment
        while True:
            continue_input = input("\n Do you want to add another assignment? (y/n): ").strip().lower()
            if continue_input in ['y', 'n', 'yes', 'no']:
                break
            print("Oops!! Please enter 'y' or 'n'")
        
        if continue_input in ['n', 'no']:
            break
    
    # Check if any assignments were entered
    if not calculator.assignments:
        print("\nNo assignments entered... Exiting program...")
        return
    
    # Display summary and export to CSV
    calculator.print_summary()
    calculator.export_to_csv()
    
    print("\n" + "="*50)
    print("YOU MADE IT PROGRAM HAS BEEN COMPLETED SUCCESSFULLY!!")
    print("^"*50)


if __name__ == "__main__":
    main()