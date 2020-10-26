from math import floor, ceil

def get_school_return_projections(total_students, total_teachers, perc_students_returning, perc_teachers_returning, 
                                  num_classrooms, selected_mode_return, config):
    """ 
    Calculates projected number of students and teachers returning to school.
    
    Parameters
    ----------
        total_students : int or float
            Total number of students in the school system.
        total_teachers : int or float
            Total number of teachers in the school system.
        perc_students_returning : int or float
            Percentage of students allowed to return. Range 0-100.
        perc_teachers_returning: int or float
            Percentage of teachers allowed to return. Range 0-100.
        num_classrooms : int or float
            Number of classrooms available.
        selected_mode_return : string
            Mode of return to school (e.g. priority, equitative...).
        config : dict
            General school return parameters.
    
    Returns
    -------
        num_returning_students : int
            Projected numbers of students returning to school.
        num_returning_teachers : int
            Project number of teachers returning to school.
    """

    # Load Fixed Parameters
    max_students_per_class = config["simule"]["class"]["max_students_per_class"]
    hours_per_week = config["simule"]["class"]["hours_per_week"]
    hours_per_lecture = config["simule"]["class"]["hours_per_lecture"]
    
    # Select Mode of Return
    modes = config["simule"]["class"]["lectures_per_student"]
    lectures_per_student = modes[selected_mode_return]
    
    # Determine number of students and faculty allowed to return
    num_students = (total_students*perc_students_returning) // 100
    num_teachers = (total_teachers*perc_teachers_returning) // 100
    
    # Calculate total number of lectures per week
    num_lectures = floor(hours_per_week / hours_per_lecture)
    
    # Determine maximum number of lectures given teacher and classroom constraints
    room_potential = num_classrooms * num_lectures
    teacher_potential = num_teachers * num_lectures
    school_capacity = max_students_per_class*min(room_potential, teacher_potential)
    
    # Adjust for number of lectures per student per week
    school_capacity = school_capacity // lectures_per_student
    
    # Calculate number of actual returning students and teachers
    num_returning_students = min(num_students, school_capacity)
    num_returning_teachers = num_teachers
    
    return num_returning_students, num_returning_teachers

def get_school_return_supplies(num_returning_students, num_returning_teachers, selected_mode_return, config):
    """ 
    Calculates number of school supplies given number of return students and faculty.
    
    Parameters
    ----------
        num_returning_students : int or float
            Number of returning students.
        num_returning_teachers : int or float
            Number of returning teachers.
        selected_mode_return : string
            Mode of return to school (e.g. priority, equitative...).
        config : dict
            General school return parameters.
    
    Returns
    -------
        total_masks : int
            Total number of masks required.
        total_sanitizer : int or float
            Total amount of hand sanitizer required.
        total_thermometers : int
            Total amount of thermometers required.
    """
    
    # Load Fixed Parameters
    
    # Protection Equipment and Cleaning Supplies
    mask_time_limit = config["simule"]["supplies"]["mask_time_limit"]
    sanitizer_per_person_per_hour = config["simule"]["supplies"]["sanitizer_per_person_per_hour"]
    people_per_thermometer = config["simule"]["supplies"]["people_per_thermometer"]
    
    # Class Hours and Composition
    max_students_per_class = config["simule"]["class"]["max_students_per_class"]
    hours_per_lecture = config["simule"]["class"]["hours_per_lecture"]
    lectures_per_student = config["simule"]["class"]["lectures_per_student"][selected_mode_return]
    
    # Determine Masks and Hand Sanitizer for Students
    hours_per_student = lectures_per_student * hours_per_lecture
    
    masks_per_student = max(lectures_per_student, ceil(hours_per_student / mask_time_limit))
    student_masks = num_returning_students * masks_per_student
    student_sanitizer = num_returning_students * hours_per_student * sanitizer_per_person_per_hour
    
    # Determine Masks and Hand Sanitizer for Teachers
    student_hours = num_returning_students * lectures_per_student * hours_per_lecture
    class_hours = student_hours / max_students_per_class
    hours_per_teacher = class_hours / num_returning_teachers
    
    masks_per_teacher = ceil( hours_per_teacher / mask_time_limit)
    teacher_masks = num_returning_teachers * masks_per_teacher
    teacher_sanitizer = num_returning_teachers * hours_per_teacher * sanitizer_per_person_per_hour
    
    # Determine Total Quantities of Masks and Hand Sanitizer
    total_masks = student_masks + teacher_masks
    total_sanitizer = student_sanitizer + teacher_sanitizer
    
    # Determine Number of Thermometers
    total_thermometers = ceil(num_returning_students / people_per_thermometer)
    
    return total_masks, total_sanitizer, total_thermometers