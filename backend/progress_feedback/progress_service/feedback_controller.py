from flask import jsonify
from progress_feedback.progress_service.progress_service import ProgressService

class FeedbackController:
    def __init__(self, progress_service: ProgressService):
        """Initialize with the progress service dependency"""
        self.progress_service = progress_service

    def generate_feedback(self, data):
        """Handle generating feedback for an activity result"""
        # Validate required fields
        if 'user_id' not in data or 'result' not in data:
            return jsonify({
                "error": "Missing required fields: user_id and result"
            }), 400
            
        # Generate feedback
        feedback = self.progress_service.generate_feedback(
            data['user_id'],
            data['result']
        )
        
        # Check for error
        if 'error' in feedback:
            return jsonify({"error": feedback['error']}), 500
            
        return jsonify({
            "message": "Feedback generated successfully", 
            "feedback": feedback
        }), 201

    def get_user_feedback(self, user_id):
        """Handle retrieving all feedback for a user"""
        if not user_id:
            return jsonify({"error": "User ID is required"}), 400
            
        # Check if user has feedback
        if user_id in self.progress_service.feedback:
            feedbacks = self.progress_service.feedback[user_id]
            return jsonify({"user_id": user_id, "feedbacks": feedbacks}), 200
        else:
            return jsonify({"user_id": user_id, "feedbacks": []}), 200

    def get_feedback_by_id(self, feedback_id):
        """Handle retrieving specific feedback by ID"""
        if not feedback_id:
            return jsonify({"error": "Feedback ID is required"}), 400
            
        # Search for the feedback across all users
        for user_id, feedbacks in self.progress_service.feedback.items():
            for feedback in feedbacks:
                if feedback.get('id') == feedback_id:
                    return jsonify(feedback), 200
                    
        return jsonify({"error": "Feedback not found"}), 404