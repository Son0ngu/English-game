from flask import jsonify
from progres-feedback.progress_service.progress_service import ProgressService

class ProgressController:
    def __init__(self, progress_service: ProgressService):
        """Initialize with the progress service dependency"""
        self.progress_service = progress_service

    def record_activity(self, data):
        """Handle recording a new activity result"""
        # Validate required fields
        required_fields = ['user_id', 'lesson_id', 'score', 'max_score', 
                          'difficulty', 'completion_time', 'answers']
        
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({
                "error": f"Missing required fields: {', '.join(missing_fields)}"
            }), 400
            
        # Record the activity result
        result = self.progress_service.record_activity_result(
            data['user_id'],
            data['lesson_id'],
            data['score'],
            data['max_score'],
            data['difficulty'],
            data['completion_time'],
            data['answers']
        )
        
        # Check for error
        if 'error' in result:
            return jsonify({"error": result['error']}), 500
            
        return jsonify({"message": "Activity recorded successfully", "result": result}), 201

    def get_user_progress(self, user_id):
        """Handle retrieving a user's progress"""
        if not user_id:
            return jsonify({"error": "User ID is required"}), 400
            
        progress = self.progress_service.get_user_progress(user_id)
        
        # Check for error
        if 'error' in progress:
            return jsonify({"error": progress['error']}), 404
            
        return jsonify(progress), 200

    def get_average_grade(self, user_id, difficulty):
        """Handle retrieving average grade for a difficulty level"""
        if not user_id or not difficulty:
            return jsonify({"error": "User ID and difficulty are required"}), 400
            
        grade = self.progress_service.get_average_grade(user_id, difficulty)
        return jsonify({"user_id": user_id, "difficulty": difficulty, "grade": grade}), 200

    def get_performance_by_difficulty(self, user_id):
        """Handle retrieving performance breakdown by difficulty"""
        if not user_id:
            return jsonify({"error": "User ID is required"}), 400
            
        performance = self.progress_service.get_performance_by_difficulty(user_id)
        
        # Check for error
        if 'error' in performance:
            return jsonify({"error": performance['error']}), 500
            
        return jsonify({"user_id": user_id, "performance": performance}), 200

    def check_health(self):
        """Handle health check request"""
        health_data = self.progress_service.check_internal()
        return jsonify(health_data), 200