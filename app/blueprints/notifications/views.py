from flask import Blueprint, render_template, jsonify, request
from flask_login import login_required, current_user
from datetime import datetime

notifications_bp = Blueprint("notifications", __name__, url_prefix="/notifications")


# Mock notification data - this would typically come from a database
def get_user_notifications():
    """Get notifications for the current user"""
    # This is mock data - in a real app, you'd query from a notifications table
    notifications = [
        {
            'id': 1,
            'type': 'recipe_like',
            'title': 'Someone liked your recipe',
            'message': 'John Doe liked your recipe "Spaghetti Carbonara"',
            'icon': 'fa-heart',
            'color': 'text-red-600',
            'bg_color': 'bg-red-100',
            'timestamp': datetime.now(),
            'read': False,
            'link': '/dashboard/recipe/1'
        },
        {
            'id': 2,
            'type': 'comment',
            'title': 'New comment on your recipe',
            'message': 'Jane Smith commented on "Chocolate Cake"',
            'icon': 'fa-comment',
            'color': 'text-blue-600',
            'bg_color': 'bg-blue-100',
            'timestamp': datetime.now(),
            'read': False,
            'link': '/dashboard/recipe/2'
        },
        {
            'id': 3,
            'type': 'follower',
            'title': 'New follower',
            'message': 'Mike Johnson started following you',
            'icon': 'fa-user-plus',
            'color': 'text-green-600',
            'bg_color': 'bg-green-100',
            'timestamp': datetime.now(),
            'read': True,
            'link': '/profile'
        },
        {
            'id': 4,
            'type': 'system',
            'title': 'Welcome to ODiGO',
            'message': 'Thank you for joining ODiGO! Start by adding your first recipe.',
            'icon': 'fa-bell',
            'color': 'text-indigo-600',
            'bg_color': 'bg-indigo-100',
            'timestamp': datetime.now(),
            'read': True,
            'link': '/dashboard/add-recipe'
        }
    ]
    return notifications


@notifications_bp.route("/")
@login_required
def index():
    """Display all notifications"""
    notifications = get_user_notifications()
    unread_count = sum(1 for n in notifications if not n['read'])
    
    return render_template(
        "notifications/index.html",
        notifications=notifications,
        unread_count=unread_count
    )


@notifications_bp.route("/mark-read/<int:notification_id>", methods=["POST"])
@login_required
def mark_read(notification_id):
    """Mark a notification as read"""
    # In a real app, you'd update the database here
    return jsonify({"success": True, "message": "Notification marked as read"})


@notifications_bp.route("/mark-all-read", methods=["POST"])
@login_required
def mark_all_read():
    """Mark all notifications as read"""
    # In a real app, you'd update all user's notifications in the database
    return jsonify({"success": True, "message": "All notifications marked as read"})


@notifications_bp.route("/delete/<int:notification_id>", methods=["POST"])
@login_required
def delete(notification_id):
    """Delete a notification"""
    # In a real app, you'd delete from the database here
    return jsonify({"success": True, "message": "Notification deleted"})
