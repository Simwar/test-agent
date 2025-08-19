from flask import Flask, jsonify, request
from datetime import datetime
import uuid

app = Flask(__name__)

# In-memory data store (in production, you'd use a database)
tasks = []

# Sample data
sample_tasks = [
    {
        'id': str(uuid.uuid4()),
        'title': 'Learn Python',
        'description': 'Complete Python tutorial',
        'completed': False,
        'created_at': datetime.now().isoformat()
    },
    {
        'id': str(uuid.uuid4()),
        'title': 'Build API',
        'description': 'Create a REST API with Flask',
        'completed': True,
        'created_at': datetime.now().isoformat()
    }
]

tasks.extend(sample_tasks)

@app.route('/')
def home():
    """Welcome endpoint"""
    return jsonify({
        'message': 'Welcome to the Simple Task API',
        'version': '1.0.0',
        'endpoints': {
            'GET /tasks': 'Get all tasks',
            'POST /tasks': 'Create a new task',
            'GET /tasks/<id>': 'Get a specific task',
            'PUT /tasks/<id>': 'Update a task',
            'DELETE /tasks/<id>': 'Delete a task',
            'POST /tasks/<id>/duplicate': 'Duplicate a task'
        }
    })

@app.route('/tasks', methods=['GET'])
def get_tasks():
    """Get all tasks"""
    return jsonify({
        'tasks': tasks,
        'count': len(tasks)
    })

@app.route('/tasks/<task_id>', methods=['GET'])
def get_task(task_id):
    """Get a specific task by ID"""
    task = next((t for t in tasks if t['id'] == task_id), None)
    
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    
    return jsonify(task)

@app.route('/tasks', methods=['POST'])
def create_task():
    """Create a new task"""
    data = request.get_json()
    
    if not data or 'title' not in data:
        return jsonify({'error': 'Title is required'}), 400
    
    task = {
        'id': str(uuid.uuid4()),
        'title': data['title'],
        'description': data.get('description', ''),
        'completed': data.get('completed', False),
        'created_at': datetime.now().isoformat()
    }
    
    tasks.append(task)
    return jsonify(task), 201

@app.route('/tasks/<task_id>', methods=['PUT'])
def update_task(task_id):
    """Update an existing task"""
    task = next((t for t in tasks if t['id'] == task_id), None)
    
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    # Update task fields
    task['title'] = data.get('title', task['title'])
    task['description'] = data.get('description', task['description'])
    task['completed'] = data.get('completed', task['completed'])
    task['updated_at'] = datetime.now().isoformat()
    
    return jsonify(task)

@app.route('/tasks/<task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Delete a task"""
    task = next((t for t in tasks if t['id'] == task_id), None)
    
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    
    tasks.remove(task)
    return jsonify({'message': 'Task deleted successfully'})

@app.route('/tasks/<task_id>/duplicate', methods=['POST'])
def duplicate_task(task_id):
    """Duplicate an existing task"""
    original_task = next((t for t in tasks if t['id'] == task_id), None)
    
    if not original_task:
        return jsonify({'error': 'Task not found'}), 404
    
    # Create a duplicate with new ID and timestamp
    duplicated_task = {
        'id': str(uuid.uuid4()),
        'title': original_task['title'],
        'description': original_task['description'],
        'completed': False,  # Reset completion status for the duplicate
        'created_at': datetime.now().isoformat()
    }
    
    # Add any additional fields that might exist (like updated_at)
    if 'updated_at' in original_task:
        # Don't copy updated_at - let the duplicate start fresh
        pass
    
    tasks.append(duplicated_task)
    return jsonify(duplicated_task), 201

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat()
    })

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)