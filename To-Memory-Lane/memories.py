import os
from flask import Blueprint, request, jsonify, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from models import db, Memory

memories_bp = Blueprint('memories', __name__)

@memories_bp.route('/memories', methods=['GET'])
@login_required
def get_memories():
    memories = Memory.query.filter_by(user_id=current_user.id).order_by(Memory.created_at.desc()).all()
    return jsonify([
        {
            'id': m.id,
            'type': m.type,
            'title': m.title,
            'content': m.content,
            'media': m.media_path,
            'date': m.created_at.isoformat()
        } for m in memories
    ])


@memories_bp.route('/memories', methods=['POST'])
@login_required
def add_memory():
    mem_type = request.form.get('type')
    title = request.form.get('title')
    content = request.form.get('content')

    memory = Memory(
        type=mem_type,
        title=title,
        content=content,
        user_id=current_user.id
    )

    if mem_type in ['image', 'video']:
        file = request.files.get('file')
        filename = secure_filename(file.filename)
        folder = 'images' if mem_type == 'image' else 'videos'
        path = os.path.join(current_app.config['UPLOAD_FOLDER'], folder)
        os.makedirs(path, exist_ok=True)
        file.save(os.path.join(path, filename))
        memory.media_path = f"/static/uploads/{folder}/{filename}"

    db.session.add(memory)
    db.session.commit()
    return jsonify({'message': 'Memory saved'})


@memories_bp.route('/memories/<int:id>', methods=['DELETE'])
@login_required
def delete_memory(id):
    memory = Memory.query.get_or_404(id)
    if memory.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403

    db.session.delete(memory)
    db.session.commit()
    return jsonify({'message': 'Memory deleted'})