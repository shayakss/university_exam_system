"""
AI Insights Controller
Provides AI-powered predictions for at-risk students
Note: This is a simplified version using basic heuristics.
For production, integrate scikit-learn for ML models.
"""
from database.db_manager import db
from datetime import datetime, date
from typing import List, Dict, Optional, Tuple

class AIInsightsController:
    """Controller for AI-powered student insights"""
    
    def calculate_risk_score(self, student_id: int) -> Tuple[float, Dict]:
        """Calculate risk score for a student (0-100, higher = more at risk)"""
        try:
            risk_score = 0.0
            factors = {}
            
            # Factor 1: CGPA (40% weight)
            cgpa_query = """
                SELECT cgpa FROM results
                WHERE student_id = ?
                ORDER BY generated_at DESC LIMIT 1
            """
            cgpa_result = db.execute_query(cgpa_query, (student_id,))
            cgpa = cgpa_result[0]['cgpa'] if cgpa_result and cgpa_result[0]['cgpa'] else 0.0
            
            if cgpa < 2.0:
                cgpa_risk = 40.0
            elif cgpa < 2.5:
                cgpa_risk = 30.0
            elif cgpa < 3.0:
                cgpa_risk = 15.0
            else:
                cgpa_risk = 0.0
            
            risk_score += cgpa_risk
            factors['cgpa'] = {'value': cgpa, 'risk': cgpa_risk, 'weight': 40}
            
            # Factor 2: Attendance (30% weight)
            att_query = """
                SELECT 
                    COUNT(*) as total,
                    SUM(CASE WHEN status IN ('Present', 'Late') THEN 1 ELSE 0 END) as present
                FROM student_attendance
                WHERE student_id = ?
            """
            att_result = db.execute_query(att_query, (student_id,))
            attendance_pct = 0.0
            if att_result and att_result[0]['total'] > 0:
                attendance_pct = (att_result[0]['present'] / att_result[0]['total']) * 100
            
            if attendance_pct < 60:
                att_risk = 30.0
            elif attendance_pct < 75:
                att_risk = 20.0
            elif attendance_pct < 85:
                att_risk = 10.0
            else:
                att_risk = 0.0
            
            risk_score += att_risk
            factors['attendance'] = {'value': attendance_pct, 'risk': att_risk, 'weight': 30}
            
            # Factor 3: Failing grades (20% weight)
            fail_query = """
                SELECT COUNT(*) as f_count
                FROM marks
                WHERE student_id = ? AND grade = 'F'
            """
            fail_result = db.execute_query(fail_query, (student_id,))
            f_count = fail_result[0]['f_count'] if fail_result else 0
            
            if f_count >= 3:
                fail_risk = 20.0
            elif f_count >= 2:
                fail_risk = 15.0
            elif f_count >= 1:
                fail_risk = 10.0
            else:
                fail_risk = 0.0
            
            risk_score += fail_risk
            factors['failing_grades'] = {'value': f_count, 'risk': fail_risk, 'weight': 20}
            
            # Factor 4: Assignment submission rate (10% weight)
            assign_query = """
                SELECT 
                    COUNT(*) as total,
                    SUM(CASE WHEN status IN ('Submitted', 'Graded') THEN 1 ELSE 0 END) as submitted
                FROM assignment_submissions
                WHERE student_id = ?
            """
            assign_result = db.execute_query(assign_query, (student_id,))
            submission_rate = 0.0
            if assign_result and assign_result[0]['total'] > 0:
                submission_rate = (assign_result[0]['submitted'] / assign_result[0]['total']) * 100
            
            if submission_rate < 50:
                assign_risk = 10.0
            elif submission_rate < 75:
                assign_risk = 5.0
            else:
                assign_risk = 0.0
            
            risk_score += assign_risk
            factors['assignment_submission'] = {'value': submission_rate, 'risk': assign_risk, 'weight': 10}
            
            return risk_score, factors
            
        except Exception as e:
            print(f"Error calculating risk score: {e}")
            return 0.0, {}
    
    def get_at_risk_students(self, department_id: int = None, 
                            risk_threshold: float = 40.0) -> List[Dict]:
        """Get list of at-risk students"""
        try:
            # Get all active students
            query = """
                SELECT s.student_id, s.roll_number, s.name, s.semester,
                       d.department_name
                FROM students s
                JOIN departments d ON s.department_id = d.department_id
                WHERE s.is_active = 1
            """
            params = []
            
            if department_id:
                query += " AND s.department_id = ?"
                params.append(department_id)
            
            students = db.execute_query(query, tuple(params))
            
            at_risk = []
            for student in students:
                risk_score, factors = self.calculate_risk_score(student['student_id'])
                
                if risk_score >= risk_threshold:
                    at_risk.append({
                        'student_id': student['student_id'],
                        'roll_number': student['roll_number'],
                        'name': student['name'],
                        'semester': student['semester'],
                        'department': student['department_name'],
                        'risk_score': round(risk_score, 2),
                        'risk_level': self._get_risk_level(risk_score),
                        'factors': factors
                    })
            
            # Sort by risk score descending
            at_risk.sort(key=lambda x: x['risk_score'], reverse=True)
            
            return at_risk
            
        except Exception as e:
            print(f"Error getting at-risk students: {e}")
            return []
    
    def _get_risk_level(self, risk_score: float) -> str:
        """Convert risk score to risk level"""
        if risk_score >= 70:
            return 'Critical'
        elif risk_score >= 50:
            return 'High'
        elif risk_score >= 30:
            return 'Medium'
        else:
            return 'Low'
    
    def get_intervention_recommendations(self, student_id: int) -> List[str]:
        """Get recommended interventions for a student"""
        try:
            risk_score, factors = self.calculate_risk_score(student_id)
            recommendations = []
            
            # CGPA-based recommendations
            if factors.get('cgpa', {}).get('risk', 0) > 15:
                recommendations.append("Schedule academic counseling session")
                recommendations.append("Assign peer tutor for weak subjects")
                recommendations.append("Recommend extra study hours")
            
            # Attendance-based recommendations
            if factors.get('attendance', {}).get('risk', 0) > 10:
                recommendations.append("Send attendance warning notice")
                recommendations.append("Contact parent/guardian")
                recommendations.append("Investigate reasons for absence")
            
            # Failing grades recommendations
            if factors.get('failing_grades', {}).get('risk', 0) > 10:
                recommendations.append("Provide remedial classes")
                recommendations.append("Offer re-examination opportunity")
                recommendations.append("Review course difficulty level")
            
            # Assignment submission recommendations
            if factors.get('assignment_submission', {}).get('risk', 0) > 5:
                recommendations.append("Send assignment reminder emails")
                recommendations.append("Extend assignment deadlines if needed")
                recommendations.append("Provide assignment help sessions")
            
            if not recommendations:
                recommendations.append("Student is performing well - continue monitoring")
            
            return recommendations
            
        except Exception as e:
            print(f"Error getting recommendations: {e}")
            return []
    
    def get_performance_prediction(self, student_id: int) -> Dict:
        """Predict student's likely performance in next semester"""
        try:
            risk_score, factors = self.calculate_risk_score(student_id)
            
            # Simple prediction based on current performance
            current_cgpa = factors.get('cgpa', {}).get('value', 0.0)
            attendance = factors.get('attendance', {}).get('value', 0.0)
            
            # Predict next semester CGPA (simplified)
            if risk_score < 30:
                predicted_cgpa = min(4.0, current_cgpa + 0.1)
                prediction = "Likely to improve"
            elif risk_score < 50:
                predicted_cgpa = current_cgpa
                prediction = "Likely to maintain current level"
            else:
                predicted_cgpa = max(0.0, current_cgpa - 0.2)
                prediction = "At risk of decline"
            
            return {
                'current_cgpa': current_cgpa,
                'predicted_cgpa': round(predicted_cgpa, 2),
                'prediction': prediction,
                'confidence': 'Medium',  # Simplified - real ML would calculate this
                'risk_score': round(risk_score, 2)
            }
            
        except Exception as e:
            print(f"Error predicting performance: {e}")
            return {}
    
    def get_insights_summary(self, department_id: int = None) -> Dict:
        """Get overall insights summary"""
        try:
            at_risk = self.get_at_risk_students(department_id, risk_threshold=30.0)
            
            critical = len([s for s in at_risk if s['risk_level'] == 'Critical'])
            high = len([s for s in at_risk if s['risk_level'] == 'High'])
            medium = len([s for s in at_risk if s['risk_level'] == 'Medium'])
            
            return {
                'total_at_risk': len(at_risk),
                'critical_risk': critical,
                'high_risk': high,
                'medium_risk': medium,
                'students_analyzed': len(at_risk),
                'top_risk_factors': self._get_top_risk_factors(at_risk)
            }
            
        except Exception as e:
            print(f"Error getting insights summary: {e}")
            return {}
    
    def _get_top_risk_factors(self, at_risk_students: List[Dict]) -> List[str]:
        """Identify most common risk factors"""
        factor_counts = {
            'Low CGPA': 0,
            'Poor Attendance': 0,
            'Failing Grades': 0,
            'Low Assignment Submission': 0
        }
        
        for student in at_risk_students:
            factors = student.get('factors', {})
            if factors.get('cgpa', {}).get('risk', 0) > 15:
                factor_counts['Low CGPA'] += 1
            if factors.get('attendance', {}).get('risk', 0) > 10:
                factor_counts['Poor Attendance'] += 1
            if factors.get('failing_grades', {}).get('risk', 0) > 10:
                factor_counts['Failing Grades'] += 1
            if factors.get('assignment_submission', {}).get('risk', 0) > 5:
                factor_counts['Low Assignment Submission'] += 1
        
        # Sort by count
        sorted_factors = sorted(factor_counts.items(), key=lambda x: x[1], reverse=True)
        return [f"{factor} ({count} students)" for factor, count in sorted_factors if count > 0]

# Global instance
ai_insights_controller = AIInsightsController()
