from user_profile_service.user.user_service import UserProfileService
from admin_service.admin_service import AdminService
import time

class ProgressService:
    def __init__(self, user_service: UserProfileService, admin_service: AdminService):
        self._startup_time = time.time()
        self._last_error = None
        self._stats = {"activities_recorded": 0, "feedback_generated": 0}
        self.user_service = user_service
        self.admin_service = admin_service
        self.activity_results = {}  # Dict[str, ActivityResult[]]
        self.feedback = {}  # Dict[str, Feedback[]]
        self.difficulty_evaluator = DifficultyEvaluator()
        
    def record_activity_result(self, user_id: str, lesson_id: str, score: int, 
                               max_score: int, difficulty: str, completion_time: int,
                               answers: list) -> dict:
        """Record a student's activity result"""
        self._stats["activities_recorded"] += 1
        try:
            # Implementation would create and store activity result
            result_id = f"{user_id}_{lesson_id}_{int(time.time())}"
            
            new_result = {
                "id": result_id,
                "user_id": user_id,
                "lesson_id": lesson_id,
                "score": score,
                "max_score": max_score,
                "percent_correct": score / max_score if max_score > 0 else 0,
                "difficulty": difficulty,
                "completion_time": completion_time,
                "answers": answers,
                "completed_at": int(time.time())
            }
            
            if user_id not in self.activity_results:
                self.activity_results[user_id] = []
            
            self.activity_results[user_id].append(new_result)
            
            # Update user progress
            self.user_service.update_progress(user_id, lesson_id, score)
            
            return new_result
        except Exception as e:
            self._last_error = e
            return {"error": str(e)}
    
    def generate_feedback(self, user_id: str, result) -> dict:
        """Generate feedback for a student's activity"""
        self._stats["feedback_generated"] += 1
        try:
            # Get performance level from difficulty evaluator
            performance_level = self.difficulty_evaluator.evaluate_performance(
                result["percent_correct"], result["difficulty"]
            )
            
            # Create feedback
            feedback_id = f"{result['id']}_feedback"
            new_feedback = {
                "id": feedback_id,
                "user_id": user_id,
                "course_id": result["lesson_id"],
                "strong_points": [],  # Would be generated based on answers
                "weak_points": [],    # Would be generated based on answers
                "suggestions": [],    # Would be generated based on weak points
                "created_at": int(time.time()),
                "performance_level": performance_level
            }
            
            if user_id not in self.feedback:
                self.feedback[user_id] = []
            
            self.feedback[user_id].append(new_feedback)
            
            return new_feedback
        except Exception as e:
            self._last_error = e
            return {"error": str(e)}
    
    def get_user_progress(self, user_id: str) -> dict:
        """Get a user's overall progress"""
        try:
            if user_id in self.activity_results:
                results = self.activity_results[user_id]
                lessons_completed = len({r["lesson_id"] for r in results})
                avg_score = sum(r["percent_correct"] for r in results) / len(results) if results else 0
                
                return {
                    "user_id": user_id,
                    "lessons_completed": lessons_completed,
                    "average_score": avg_score,
                    "total_points": sum(r["score"] for r in results)
                }
            return {"user_id": user_id, "error": "No progress data found"}
        except Exception as e:
            self._last_error = e
            return {"user_id": user_id, "error": str(e)}
    
    def get_average_grade(self, user_id: str, difficulty: str) -> float:
        """Get a user's average grade for a specific difficulty level"""
        try:
            if user_id in self.activity_results:
                results = [r for r in self.activity_results[user_id] if r["difficulty"] == difficulty]
                
                if not results:
                    return 0.0
                
                total_grade = sum(self.difficulty_evaluator.calculate_grade(
                    r["percent_correct"], r["difficulty"]) for r in results)
                
                return total_grade / len(results)
            return 0.0
        except Exception as e:
            self._last_error = e
            return 0.0
    
    def get_performance_by_difficulty(self, user_id: str) -> dict:
        """Get a user's performance broken down by difficulty levels"""
        try:
            if user_id in self.activity_results:
                results = self.activity_results[user_id]
                difficulties = set(r["difficulty"] for r in results)
                
                performance = {}
                for diff in difficulties:
                    diff_results = [r for r in results if r["difficulty"] == diff]
                    avg_score = sum(r["percent_correct"] for r in diff_results) / len(diff_results)
                    
                    performance[diff] = {
                        "count": len(diff_results),
                        "average_score": avg_score,
                        "average_grade": self.get_average_grade(user_id, diff)
                    }
                
                return performance
            return {}
        except Exception as e:
            self._last_error = e
            return {"error": str(e)}
    
    def check_internal(self) -> dict:
        """Internal health check for this service"""
        return {
            "status": "healthy" if not self._last_error else "degraded",
            "uptime": time.time() - self._startup_time,
            "stats": self._stats,
            "activity_results_count": sum(len(results) for results in self.activity_results.values()),
            "feedback_count": sum(len(feedbacks) for feedbacks in self.feedback.values()),
            "last_error": str(self._last_error) if self._last_error else None,
            "details": "Progress service running normally"
        }

class DifficultyEvaluator:
    """Evaluates performance based on difficulty levels"""
    
    def __init__(self):
        # Default thresholds for different difficulty levels
        self.thresholds = {
            "Easy": {"A": 0.9, "B": 0.8, "C": 0.7, "D": 0.6},
            "Normal": {"A": 0.85, "B": 0.75, "C": 0.65, "D": 0.55},
            "Hard": {"A": 0.8, "B": 0.7, "C": 0.6, "D": 0.5}
        }
    
    def evaluate_performance(self, percent_correct: float, difficulty: str) -> str:
        """Evaluate performance level based on percent correct and difficulty"""
        thresholds = self.thresholds.get(difficulty, self.thresholds["Normal"])
        
        if percent_correct >= thresholds["A"]:
            return "Excellent"
        elif percent_correct >= thresholds["B"]:
            return "Good"
        elif percent_correct >= thresholds["C"]:
            return "Average"
        elif percent_correct >= thresholds["D"]:
            return "Need Improvement"
        else:
            return "Poor"
    
    def calculate_grade(self, percent_correct: float, difficulty: str) -> float:
        """Calculate numeric grade based on percent correct and difficulty"""
        # Simple grade calculation - could be more sophisticated
        base_grade = percent_correct * 4.0  # 4.0 scale
        
        # Adjust for difficulty
        if difficulty == "Hard":
            return min(4.0, base_grade * 1.1)  # Bonus for hard difficulty
        elif difficulty == "Easy":
            return base_grade * 0.9  # Penalty for easy difficulty
        
        return base_grade
    
    def get_threshold(self, difficulty: str) -> float:
        """Get the pass/fail threshold for a given difficulty"""
        return self.thresholds.get(difficulty, self.thresholds["Normal"])["D"]