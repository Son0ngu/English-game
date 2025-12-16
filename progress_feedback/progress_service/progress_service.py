import time
from typing import Dict, Any, List
from user_profile_service.user.user import StudentProfile

class ProgressService:
    """Progress service focused on map progression"""
    
    def __init__(self, user_service, admin_service):
        self.user_service = user_service
        self.admin_service = admin_service
        self.map_results = {}  # Dict[user_id, List[MapResult]]
        self.feedback = {}     # ✅ THÊM: Dict[user_id, List[Feedback]]
        self.difficulty_evaluator = DifficultyEvaluator()
        self._startup_time = time.time()

    def complete_map(self, user_id: str, map_number: int, score: int, max_score: int, 
                     completion_time: int, difficulty: str = "Normal") -> dict:
        """
        Complete a map and unlock next map
        
        Args:
            user_id: ID của user
            map_number: Số map đã hoàn thành (1-10)
            score: Điểm đạt được
            max_score: Điểm tối đa
            completion_time: Thời gian hoàn thành (seconds)
            difficulty: Độ khó của map
            
        Returns:
            Kết quả complete map
        """
        try:
            # Enhanced validation
            if not isinstance(map_number, int) or map_number < 1 or map_number > 20:
                return {"success": False, "error": "Invalid map_number. Must be 1-20"}
            
            if not isinstance(score, int) or score < 0:
                return {"success": False, "error": "Invalid score. Must be non-negative integer"}
            
            if not isinstance(max_score, int) or max_score <= 0:
                return {"success": False, "error": "Invalid max_score. Must be positive integer"}
            
            if score > max_score:
                return {"success": False, "error": "Score cannot exceed max_score"}
            
            if not isinstance(completion_time, int) or completion_time < 0:
                return {"success": False, "error": "Invalid completion_time. Must be non-negative integer"}
            
            if difficulty not in ["Easy", "Normal", "Hard"]:
                return {"success": False, "error": "Invalid difficulty. Must be Easy, Normal, or Hard"}
            
            # Lấy thông tin user
            user = self.user_service.user_repository.find_by_id(user_id)
            if not user or not isinstance(user, StudentProfile):
                return {"success": False, "error": "Student not found"}
            
            # Kiểm tra có thể access map này không
            if not user.can_access_map(map_number):
                return {
                    "success": False, 
                    "error": f"Map {map_number} is locked. Current max unlocked: {user.max_map_unlocked}"
                }
            
            # Kiểm tra điểm đạt yêu cầu để pass map (ví dụ: >= 60%)
            percent_correct = score / max_score
            pass_threshold = 0.6  # 60% để pass
            
            if percent_correct < pass_threshold:
                # Lưu attempt nhưng không unlock map tiếp theo
                map_result = {
                    "id": f"{user_id}_map_{map_number}_{int(time.time())}",
                    "user_id": user_id,
                    "map_number": map_number,
                    "score": score,
                    "max_score": max_score,
                    "percent_correct": percent_correct,
                    "completion_time": completion_time,
                    "difficulty": difficulty,
                    "passed": False,
                    "completed_at": int(time.time())
                }
                
                # Lưu vào memory
                if user_id not in self.map_results:
                    self.map_results[user_id] = []
                self.map_results[user_id].append(map_result)
                
                return {
                    "success": True,
                    "passed": False,
                    "message": f"Map {map_number} not passed. Need {pass_threshold*100}% to unlock next map",
                    "score_percent": percent_correct * 100,
                    "required_percent": pass_threshold * 100,
                    "map_result": map_result
                }
            
            # Complete map thành công
            map_completed = user.complete_map(map_number)
            
            if not map_completed:
                return {"success": False, "error": f"Map {map_number} already completed or out of order"}
            
            # Cập nhật points và money khi complete map
            map_rewards = self._calculate_map_rewards(map_number, percent_correct, difficulty)
            user.points += map_rewards["points"]
            user.money += map_rewards["money"]
            
            # Lưu user với map progression mới
            self.user_service.user_repository.save(user)
            
            # Lưu map result
            map_result = {
                "id": f"{user_id}_map_{map_number}_{int(time.time())}",
                "user_id": user_id,
                "map_number": map_number,
                "score": score,
                "max_score": max_score,
                "percent_correct": percent_correct,
                "completion_time": completion_time,
                "difficulty": difficulty,
                "passed": True,
                "rewards": map_rewards,
                "completed_at": int(time.time())
            }

            if user_id not in self.map_results:
                self.map_results[user_id] = []
            self.map_results[user_id].append(map_result)

            # ✅ THÊM: Auto-generate feedback
            feedback_result = self.generate_feedback(user_id, map_result)

            return {
                "success": True,
                "passed": True,
                "message": f"Map {map_number} completed successfully!",
                "map_progression": user.get_map_progress(),
                "rewards": map_rewards,
                "feedback": feedback_result.get('feedback') if feedback_result.get('success') else None,
                "next_map_unlocked": user.current_map if user.current_map <= 10 else None,
                "map_result": map_result
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def _calculate_map_rewards(self, map_number: int, percent_correct: float, difficulty: str) -> dict:
        """Calculate rewards for completing map - Enhanced balancing"""
        # ✅ Cải thiện reward calculation
        base_points = 50 + (map_number * 25)  # More balanced progression
        base_money = 30 + (map_number * 15)   # Không quá nhiều money
        
        # Performance bonus (chỉ bonus cho phần trên pass threshold)
        if percent_correct > 0.6:
            performance_bonus = (percent_correct - 0.6) / 0.4  # 0.0 to 1.0
        else:
            performance_bonus = 0
        
        # Difficulty multiplier
        difficulty_multiplier = {"Easy": 0.8, "Normal": 1.0, "Hard": 1.3}.get(difficulty, 1.0)
        
        # Perfect score bonus
        perfect_bonus = 1.5 if percent_correct >= 0.95 else 1.0
        
        final_points = int(base_points * (1 + performance_bonus * 0.5) * difficulty_multiplier * perfect_bonus)
        final_money = int(base_money * (1 + performance_bonus * 0.3) * difficulty_multiplier * perfect_bonus)
        
        return {
            "points": final_points,
            "money": final_money,
            "base_points": base_points,
            "base_money": base_money,
            "performance_bonus": performance_bonus,
            "difficulty_multiplier": difficulty_multiplier,
            "perfect_bonus": perfect_bonus if perfect_bonus > 1.0 else None
        }

    def get_user_map_progress(self, user_id: str) -> dict:
        """Get user's map progression"""
        try:
            user = self.user_service.user_repository.find_by_id(user_id)
            if not user or not isinstance(user, StudentProfile):
                return {"success": False, "error": "Student not found"}
            
            map_progress = user.get_map_progress()
            
            # Lấy history của các map attempts
            user_results = self.map_results.get(user_id, [])
            
            return {
                "success": True,
                "user_id": user_id,
                "map_progression": map_progress,
                "map_history": user_results,
                "can_access_maps": list(range(1, user.max_map_unlocked + 1))
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_map_leaderboard(self, map_number: int) -> dict:
        """Get leaderboard for specific map"""
        try:
            leaderboard = []
            
            for user_id, results in self.map_results.items():
                map_results = [r for r in results if r["map_number"] == map_number and r["passed"]]
                if map_results:
                    best_result = max(map_results, key=lambda x: x["percent_correct"])
                    leaderboard.append({
                        "user_id": user_id,
                        "score": best_result["score"],
                        "max_score": best_result["max_score"],
                        "percent_correct": best_result["percent_correct"],
                        "completion_time": best_result["completion_time"],
                        "completed_at": best_result["completed_at"]
                    })
            
            # Sort by percent_correct descending, then by completion_time ascending
            leaderboard.sort(key=lambda x: (-x["percent_correct"], x["completion_time"]))
            
            return {
                "success": True,
                "map_number": map_number,
                "leaderboard": leaderboard[:10]  # Top 10
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def check_internal(self) -> dict:
        """Service health check"""
        return {
            "status": "healthy",
            "uptime_seconds": int(time.time() - self._startup_time),
            "total_users_tracked": len(self.map_results),
            "total_map_attempts": sum(len(results) for results in self.map_results.values()),
            "focus": "map_progression_system"
        }

    def generate_feedback(self, user_id: str, map_result: dict) -> dict:
        """Generate feedback with detailed analysis"""
        try:
            percent_correct = map_result.get('percent_correct', 0)
            difficulty = map_result.get('difficulty', 'Normal')
            map_number = map_result.get('map_number', 1)
            completion_time = map_result.get('completion_time', 0)
            
            # Evaluate performance
            performance_level = self.difficulty_evaluator.evaluate_performance(percent_correct, difficulty)
            
            # ✅ Enhanced feedback generation
            suggestions = []
            strong_points = []
            weak_points = []
            next_steps = []
            
            # Performance-based feedback
            if percent_correct >= 0.95:
                strong_points = ["Perfect or near-perfect score", "Excellent comprehension", "Strong skill mastery"]
                suggestions = [f"Try Map {map_number + 1} on Hard difficulty", "Challenge yourself with advanced content"]
                next_steps = ["Move to next map", "Try harder difficulty"]
                
            elif percent_correct >= 0.85:
                strong_points = ["Very good performance", "Strong understanding", "Good accuracy"]
                suggestions = ["Review any mistakes", f"Practice similar content", "Try Normal or Hard difficulty"]
                next_steps = ["Continue to next map", "Optional: Retry for perfect score"]
                
            elif percent_correct >= 0.7:
                strong_points = ["Good progress", "Basic understanding achieved"]
                weak_points = ["Some areas need improvement", "Room for better accuracy"]
                suggestions = ["Review incorrect answers", "Practice weak areas", "Take your time"]
                next_steps = ["Continue to next map", "Consider additional practice"]
                
            elif percent_correct >= 0.6:
                strong_points = ["Passed the map", "Basic concepts understood"]
                weak_points = ["Below average performance", "Several areas need work"]
                suggestions = ["Review fundamentals", "Practice more", "Focus on weak areas"]
                next_steps = ["Continue to next map", "Consider reviewing this content"]
                
            else:
                weak_points = ["Below passing threshold", "Needs significant improvement"]
                suggestions = ["Review all content", "Try easier difficulty", "Get additional help", "Practice fundamentals"]
                next_steps = ["Retry this map", "Review content before advancing"]
            
            # Time-based feedback
            if completion_time > 0:
                if completion_time < 60:
                    strong_points.append("Quick completion time")
                elif completion_time > 300:  # 5 minutes
                    suggestions.append("Try to improve speed")
            
            feedback = {
                "id": f"feedback_{user_id}_{map_number}_{int(time.time())}",
                "user_id": user_id,
                "map_number": map_number,
                "performance_level": performance_level,
                "score_analysis": {
                    "percent_correct": percent_correct * 100,
                    "grade": performance_level,
                    "passed": percent_correct >= 0.6
                },
                "strong_points": strong_points,
                "weak_points": weak_points,
                "suggestions": suggestions,
                "next_steps": next_steps,
                "created_at": int(time.time())
            }
            
            # Save feedback
            if user_id not in self.feedback:
                self.feedback[user_id] = []
            self.feedback[user_id].append(feedback)
            
            return {"success": True, "feedback": feedback}
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_user_feedback(self, user_id: str) -> dict:
        """Get all feedback for user"""
        try:
            user_feedback = self.feedback.get(user_id, [])
            return {
                "success": True,
                "user_id": user_id,
                "feedbacks": user_feedback,
                "total_feedback": len(user_feedback)
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_feedback_by_id(self, feedback_id: str) -> dict:
        """Get specific feedback by ID"""
        try:
            for user_id, feedbacks in self.feedback.items():
                for feedback in feedbacks:
                    if feedback.get('id') == feedback_id:
                        return {"success": True, "feedback": feedback}
            
            return {"success": False, "error": "Feedback not found"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_map_statistics(self, map_number: int) -> dict:
        """Get statistics for specific map"""
        try:
            all_attempts = []
            passed_attempts = []
            
            for user_id, results in self.map_results.items():
                map_attempts = [r for r in results if r["map_number"] == map_number]
                all_attempts.extend(map_attempts)
                passed_attempts.extend([r for r in map_attempts if r.get("passed", False)])
            
            if not all_attempts:
                return {
                    "success": True,
                    "map_number": map_number,
                    "total_attempts": 0,
                    "passed_attempts": 0,
                    "pass_rate": 0,
                    "average_score": 0,
                    "average_time": 0
                }
            
            total_attempts = len(all_attempts)
            passed_count = len(passed_attempts)
            pass_rate = (passed_count / total_attempts) * 100 if total_attempts > 0 else 0
            
            avg_score = sum(r["percent_correct"] for r in all_attempts) / total_attempts * 100
            avg_time = sum(r["completion_time"] for r in all_attempts) / total_attempts
            
            return {
                "success": True,
                "map_number": map_number,
                "total_attempts": total_attempts,
                "passed_attempts": passed_count,
                "pass_rate": round(pass_rate, 2),
                "average_score": round(avg_score, 2),
                "average_time": round(avg_time, 2),
                "difficulty_breakdown": self._get_difficulty_breakdown(all_attempts)
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def _get_difficulty_breakdown(self, attempts: list) -> dict:
        """Get breakdown by difficulty"""
        breakdown = {"Easy": 0, "Normal": 0, "Hard": 0}
        for attempt in attempts:
            difficulty = attempt.get("difficulty", "Normal")
            breakdown[difficulty] = breakdown.get(difficulty, 0) + 1
        return breakdown

    def get_user_progress_summary(self, user_id: str) -> dict:
        """Get comprehensive progress summary for user"""
        try:
            # Get basic map progress
            map_progress_result = self.get_user_map_progress(user_id)
            if not map_progress_result.get('success'):
                return map_progress_result
            
            # Get feedback summary
            feedback_result = self.get_user_feedback(user_id)
            feedbacks = feedback_result.get('feedbacks', []) if feedback_result.get('success') else []
            
            # Calculate performance trends
            user_results = self.map_results.get(user_id, [])
            passed_maps = [r for r in user_results if r.get("passed", False)]
            
            performance_trend = []
            if len(passed_maps) >= 2:
                recent_scores = [r["percent_correct"] for r in passed_maps[-5:]]  # Last 5
                trend = "improving" if recent_scores[-1] > recent_scores[0] else "declining"
                performance_trend = {
                    "trend": trend,
                    "recent_average": round(sum(recent_scores) / len(recent_scores) * 100, 2),
                    "best_score": round(max(r["percent_correct"] for r in passed_maps) * 100, 2),
                    "total_time_played": sum(r["completion_time"] for r in passed_maps)
                }
            
            return {
                "success": True,
                "user_id": user_id,
                "map_progression": map_progress_result.get('map_progression'),
                "total_feedback": len(feedbacks),
                "latest_feedback": feedbacks[-1] if feedbacks else None,
                "performance_trend": performance_trend,
                "achievements": self._calculate_achievements(user_id, passed_maps)
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def _calculate_achievements(self, user_id: str, passed_maps: list) -> list:
        """Calculate user achievements"""
        achievements = []
        
        if len(passed_maps) >= 1:
            achievements.append("First Map Completed")
        if len(passed_maps) >= 5:
            achievements.append("Map Explorer")
        if len(passed_maps) >= 10:
            achievements.append("Map Master")
        
        # Perfect scores
        perfect_scores = [r for r in passed_maps if r["percent_correct"] >= 0.95]
        if len(perfect_scores) >= 1:
            achievements.append("Perfectionist")
        if len(perfect_scores) >= 3:
            achievements.append("Triple Perfect")
        
        # Speed achievements
        fast_completions = [r for r in passed_maps if r["completion_time"] < 60]
        if len(fast_completions) >= 1:
            achievements.append("Speed Runner")
        
        return achievements

class DifficultyEvaluator:
    """Evaluator for map difficulty and grading"""
    
    def __init__(self):
        self.thresholds = {
            "Easy": {"A": 0.9, "B": 0.8, "C": 0.7, "D": 0.6},
            "Normal": {"A": 0.85, "B": 0.75, "C": 0.65, "D": 0.6}, 
            "Hard": {"A": 0.8, "B": 0.7, "C": 0.6, "D": 0.6}
        }
    
    def evaluate_performance(self, percent_correct: float, difficulty: str) -> str:
        """Evaluate performance grade"""
        thresholds = self.thresholds.get(difficulty, self.thresholds["Normal"])
        
        if percent_correct >= thresholds["A"]:
            return "Excellent"
        elif percent_correct >= thresholds["B"]:
            return "Good"
        elif percent_correct >= thresholds["C"]:
            return "Average"
        elif percent_correct >= thresholds["D"]:
            return "Passed"
        else:
            return "Failed"