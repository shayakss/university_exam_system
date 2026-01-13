"""
Timetable Controller
Manages class schedules and exam schedules with conflict detection
"""
from database.db_manager import db
from datetime import datetime, date, time
from typing import List, Dict, Optional, Tuple

class TimetableController:
    """Controller for timetable and scheduling management"""
    
    def create_class_schedule(self, course_id: int, teacher_id: int, department_id: int,
                             semester: int, day_of_week: str, start_time: str, end_time: str,
                             room_number: str = None) -> Tuple[bool, str]:
        """Create a new class schedule"""
        try:
            # Check for conflicts
            conflicts = self.check_schedule_conflicts(
                teacher_id, day_of_week, start_time, end_time, room_number
            )
            
            if conflicts:
                conflict_msg = "Schedule conflicts detected:\n"
                for conflict in conflicts:
                    conflict_msg += f"- {conflict['conflict_type']}: {conflict['details']}\n"
                return False, conflict_msg
            
            query = """
                INSERT INTO class_schedule 
                (course_id, teacher_id, department_id, semester, day_of_week, 
                 start_time, end_time, room_number)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """
            success, schedule_id = db.execute_update(
                query, (course_id, teacher_id, department_id, semester, 
                       day_of_week, start_time, end_time, room_number)
            )
            
            if success:
                return True, f"Class schedule created successfully (ID: {schedule_id})"
            return False, "Failed to create class schedule"
            
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def check_schedule_conflicts(self, teacher_id: int, day_of_week: str,
                                start_time: str, end_time: str, 
                                room_number: str = None,
                                exclude_schedule_id: int = None) -> List[Dict]:
        """Check for scheduling conflicts"""
        conflicts = []
        
        try:
            # Check teacher conflict
            query = """
                SELECT cs.*, c.course_name, c.course_code
                FROM class_schedule cs
                JOIN courses c ON cs.course_id = c.course_id
                WHERE cs.teacher_id = ? 
                    AND cs.day_of_week = ?
                    AND cs.is_active = 1
                    AND (
                        (cs.start_time <= ? AND cs.end_time > ?) OR
                        (cs.start_time < ? AND cs.end_time >= ?) OR
                        (cs.start_time >= ? AND cs.end_time <= ?)
                    )
            """
            params = [teacher_id, day_of_week, start_time, start_time, 
                     end_time, end_time, start_time, end_time]
            
            if exclude_schedule_id:
                query += " AND cs.schedule_id != ?"
                params.append(exclude_schedule_id)
            
            teacher_conflicts = db.execute_query(query, tuple(params))
            
            for conflict in teacher_conflicts:
                conflicts.append({
                    'conflict_type': 'Teacher Conflict',
                    'details': f"Teacher already scheduled for {conflict['course_name']} ({conflict['start_time']}-{conflict['end_time']})"
                })
            
            # Check room conflict if room specified
            if room_number:
                query = """
                    SELECT cs.*, c.course_name, u.full_name as teacher_name
                    FROM class_schedule cs
                    JOIN courses c ON cs.course_id = c.course_id
                    JOIN users u ON cs.teacher_id = u.user_id
                    WHERE cs.room_number = ? 
                        AND cs.day_of_week = ?
                        AND cs.is_active = 1
                        AND (
                            (cs.start_time <= ? AND cs.end_time > ?) OR
                            (cs.start_time < ? AND cs.end_time >= ?) OR
                            (cs.start_time >= ? AND cs.end_time <= ?)
                        )
                """
                params = [room_number, day_of_week, start_time, start_time,
                         end_time, end_time, start_time, end_time]
                
                if exclude_schedule_id:
                    query += " AND cs.schedule_id != ?"
                    params.append(exclude_schedule_id)
                
                room_conflicts = db.execute_query(query, tuple(params))
                
                for conflict in room_conflicts:
                    conflicts.append({
                        'conflict_type': 'Room Conflict',
                        'details': f"Room already booked for {conflict['course_name']} by {conflict['teacher_name']} ({conflict['start_time']}-{conflict['end_time']})"
                    })
            
            return conflicts
            
        except Exception as e:
            print(f"Error checking conflicts: {e}")
            return []
    
    def update_class_schedule(self, schedule_id: int, **kwargs) -> Tuple[bool, str]:
        """Update an existing class schedule"""
        try:
            # Get current schedule
            current = db.execute_query(
                "SELECT * FROM class_schedule WHERE schedule_id = ?", (schedule_id,)
            )
            if not current:
                return False, "Schedule not found"
            
            current = current[0]
            
            # Check for conflicts if time/day/room changed
            if any(k in kwargs for k in ['day_of_week', 'start_time', 'end_time', 'room_number']):
                conflicts = self.check_schedule_conflicts(
                    kwargs.get('teacher_id', current['teacher_id']),
                    kwargs.get('day_of_week', current['day_of_week']),
                    kwargs.get('start_time', current['start_time']),
                    kwargs.get('end_time', current['end_time']),
                    kwargs.get('room_number', current['room_number']),
                    exclude_schedule_id=schedule_id
                )
                
                if conflicts:
                    conflict_msg = "Schedule conflicts detected:\n"
                    for conflict in conflicts:
                        conflict_msg += f"- {conflict['conflict_type']}: {conflict['details']}\n"
                    return False, conflict_msg
            
            # Build update query
            update_fields = []
            params = []
            
            for field, value in kwargs.items():
                if field in ['course_id', 'teacher_id', 'department_id', 'semester',
                           'day_of_week', 'start_time', 'end_time', 'room_number', 'is_active']:
                    update_fields.append(f"{field} = ?")
                    params.append(value)
            
            if not update_fields:
                return False, "No fields to update"
            
            params.append(schedule_id)
            query = f"UPDATE class_schedule SET {', '.join(update_fields)} WHERE schedule_id = ?"
            
            success, _ = db.execute_update(query, tuple(params))
            
            if success:
                return True, "Class schedule updated successfully"
            return False, "Failed to update class schedule"
            
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def delete_class_schedule(self, schedule_id: int) -> Tuple[bool, str]:
        """Delete a class schedule"""
        try:
            query = "DELETE FROM class_schedule WHERE schedule_id = ?"
            success, _ = db.execute_update(query, (schedule_id,))
            
            if success:
                return True, "Class schedule deleted successfully"
            return False, "Failed to delete class schedule"
            
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def get_class_schedules(self, department_id: int = None, semester: int = None,
                           teacher_id: int = None, day_of_week: str = None) -> List[Dict]:
        """Get class schedules with filters"""
        try:
            query = """
                SELECT cs.*, c.course_name, c.course_code, c.credits,
                       u.full_name as teacher_name, d.department_name
                FROM class_schedule cs
                JOIN courses c ON cs.course_id = c.course_id
                JOIN users u ON cs.teacher_id = u.user_id
                JOIN departments d ON cs.department_id = d.department_id
                WHERE cs.is_active = 1
            """
            params = []
            
            if department_id:
                query += " AND cs.department_id = ?"
                params.append(department_id)
            if semester:
                query += " AND cs.semester = ?"
                params.append(semester)
            if teacher_id:
                query += " AND cs.teacher_id = ?"
                params.append(teacher_id)
            if day_of_week:
                query += " AND cs.day_of_week = ?"
                params.append(day_of_week)
            
            query += " ORDER BY cs.day_of_week, cs.start_time"
            
            return db.execute_query(query, tuple(params))
        except Exception as e:
            print(f"Error getting class schedules: {e}")
            return []
    
    def create_exam_schedule(self, course_id: int, department_id: int, semester: int,
                            exam_date: date, start_time: str, end_time: str,
                            room_number: str, exam_type: str, total_marks: int) -> Tuple[bool, str]:
        """Create an exam schedule"""
        try:
            query = """
                INSERT INTO exam_schedule
                (course_id, department_id, semester, exam_date, start_time, end_time,
                 room_number, exam_type, total_marks)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            success, exam_id = db.execute_update(
                query, (course_id, department_id, semester, exam_date, start_time,
                       end_time, room_number, exam_type, total_marks)
            )
            
            if success:
                return True, f"Exam schedule created successfully (ID: {exam_id})"
            return False, "Failed to create exam schedule"
            
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def get_exam_schedules(self, department_id: int = None, semester: int = None,
                          start_date: date = None, end_date: date = None) -> List[Dict]:
        """Get exam schedules with filters"""
        try:
            query = """
                SELECT es.*, c.course_name, c.course_code, d.department_name
                FROM exam_schedule es
                JOIN courses c ON es.course_id = c.course_id
                JOIN departments d ON es.department_id = d.department_id
                WHERE 1=1
            """
            params = []
            
            if department_id:
                query += " AND es.department_id = ?"
                params.append(department_id)
            if semester:
                query += " AND es.semester = ?"
                params.append(semester)
            if start_date:
                query += " AND es.exam_date >= ?"
                params.append(start_date)
            if end_date:
                query += " AND es.exam_date <= ?"
                params.append(end_date)
            
            query += " ORDER BY es.exam_date, es.start_time"
            
            return db.execute_query(query, tuple(params))
        except Exception as e:
            print(f"Error getting exam schedules: {e}")
            return []
    
    def get_timetable_for_student(self, student_id: int) -> List[Dict]:
        """Get complete timetable for a student based on their department and semester"""
        try:
            query = """
                SELECT cs.*, c.course_name, c.course_code, u.full_name as teacher_name
                FROM class_schedule cs
                JOIN courses c ON cs.course_id = c.course_id
                JOIN users u ON cs.teacher_id = u.user_id
                JOIN students s ON cs.department_id = s.department_id AND cs.semester = s.semester
                WHERE s.student_id = ? AND cs.is_active = 1
                ORDER BY 
                    CASE cs.day_of_week
                        WHEN 'Monday' THEN 1
                        WHEN 'Tuesday' THEN 2
                        WHEN 'Wednesday' THEN 3
                        WHEN 'Thursday' THEN 4
                        WHEN 'Friday' THEN 5
                        WHEN 'Saturday' THEN 6
                        WHEN 'Sunday' THEN 7
                    END,
                    cs.start_time
            """
            return db.execute_query(query, (student_id,))
        except Exception as e:
            print(f"Error getting student timetable: {e}")
            return []

# Global instance
timetable_controller = TimetableController()
