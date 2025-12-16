from flask import jsonify
from .progress_service import ProgressService
import time

class FeedbackController:
    """Feedback controller tích hợp với map progression"""
    
    def __init__(self, progress_service: ProgressService):
        self.progress_service = progress_service

    def check_health(self):
        """Health check"""
        try:
            return jsonify({
                "status": "healthy",
                "service": "feedback",
                "uptime_seconds": int(time.time() - self.progress_service._startup_time),
                "total_feedback": len(self.progress_service.feedback),
                "focus": "map_feedback_system"
            }), 200
        except Exception as e:
            return jsonify({
                "status": "error",
                "error": f"Health check failed: {str(e)}"
            }), 500

    def generate_feedback(self, data):
        """Generate feedback từ map completion - delegate to ProgressService"""
        try:
            user_id = data.get('user_id')
            map_result = data.get('map_result')
            
            if not all([user_id, map_result]):
                return jsonify({
                    "success": False,
                    "error": "Missing required fields: user_id, map_result"
                }), 400

            result = self.progress_service.generate_feedback(user_id, map_result)
            
            if result.get('success'):
                return jsonify(result), 200
            else:
                return jsonify(result), 400
                
        except Exception as e:
            return jsonify({
                "success": False,
                "error": f"Failed to generate feedback: {str(e)}"
            }), 500

    def get_user_feedback(self, user_id):
        """Get all feedback cho user"""
        try:
            result = self.progress_service.get_user_feedback(user_id)
            
            if result.get('success'):
                return jsonify(result), 200
            else:
                return jsonify(result), 404
                
        except Exception as e:
            return jsonify({
                "success": False,
                "error": f"Failed to get user feedback: {str(e)}"
            }), 500

    def get_feedback_by_id(self, feedback_id):
        """Get specific feedback by ID"""
        try:
            result = self.progress_service.get_feedback_by_id(feedback_id)
            
            if result.get('success'):
                return jsonify(result), 200
            else:
                return jsonify(result), 404
                
        except Exception as e:
            return jsonify({
                "success": False,
                "error": f"Failed to get feedback: {str(e)}"
            }), 500