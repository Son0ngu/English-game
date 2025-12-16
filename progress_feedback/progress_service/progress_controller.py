from flask import jsonify
from .progress_service import ProgressService
import time

class ProgressController:
    """Progress controller for map progression system"""
    
    def __init__(self, progress_service: ProgressService):
        self.progress_service = progress_service

    def check_health(self):
        """Health check"""
        try:
            health_status = self.progress_service.check_internal()
            status_code = 200 if health_status.get('status') == 'healthy' else 503
            return jsonify(health_status), status_code
        except Exception as e:
            return jsonify({
                "status": "error",
                "error": f"Health check failed: {str(e)}"
            }), 500

    def complete_map(self, data):
        """Complete a map"""
        try:
            user_id = data.get('user_id')
            map_number = data.get('map_number')
            score = data.get('score')
            max_score = data.get('max_score')
            completion_time = data.get('completion_time')
            difficulty = data.get('difficulty', 'Normal')

            if not all([user_id, map_number, score is not None, max_score, completion_time]):
                return jsonify({
                    "success": False,
                    "error": "Missing required fields: user_id, map_number, score, max_score, completion_time"
                }), 400

            result = self.progress_service.complete_map(
                user_id, map_number, score, max_score, completion_time, difficulty
            )
            
            if result.get('success'):
                return jsonify(result), 200
            else:
                return jsonify(result), 400
                
        except Exception as e:
            return jsonify({
                "success": False,
                "error": f"Failed to complete map: {str(e)}"
            }), 500

    def get_user_map_progress(self, user_id):
        """Get user's map progression"""
        try:
            result = self.progress_service.get_user_map_progress(user_id)
            
            if result.get('success'):
                return jsonify(result), 200
            else:
                return jsonify(result), 404
                
        except Exception as e:
            return jsonify({
                "success": False,
                "error": f"Failed to get map progress: {str(e)}"
            }), 500

    def get_map_leaderboard(self, data):
        """Get leaderboard for specific map"""
        try:
            map_number = data.get('map_number')
            
            if not map_number:
                return jsonify({
                    "success": False,
                    "error": "map_number required"
                }), 400

            result = self.progress_service.get_map_leaderboard(map_number)
            
            if result.get('success'):
                return jsonify(result), 200
            else:
                return jsonify(result), 400
                
        except Exception as e:
            return jsonify({
                "success": False,
                "error": f"Failed to get leaderboard: {str(e)}"
            }), 500

    def get_map_statistics(self, data):
        """Get statistics for specific map"""
        try:
            map_number = data.get('map_number')
            
            if not map_number:
                return jsonify({
                    "success": False,
                    "error": "map_number required"
                }), 400

            result = self.progress_service.get_map_statistics(map_number)
            
            if result.get('success'):
                return jsonify(result), 200
            else:
                return jsonify(result), 400
                
        except Exception as e:
            return jsonify({
                "success": False,
                "error": f"Failed to get map statistics: {str(e)}"
            }), 500

    def get_user_progress_summary(self, user_id):
        """Get comprehensive progress summary"""
        try:
            result = self.progress_service.get_user_progress_summary(user_id)
            
            if result.get('success'):
                return jsonify(result), 200
            else:
                return jsonify(result), 404
                
        except Exception as e:
            return jsonify({
                "success": False,
                "error": f"Failed to get progress summary: {str(e)}"
            }), 500