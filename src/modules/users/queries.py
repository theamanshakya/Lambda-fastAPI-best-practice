USER_QUERIES = {
    "create_user": """
        INSERT INTO users (email, name)
        VALUES (%s, %s)
        RETURNING id, email, name, created_at, updated_at
    """,
    
    "get_user_by_id": """
        SELECT id, email, name, created_at, updated_at
        FROM users
        WHERE id = %s
    """,
    
    "list_users": """
        SELECT id, email, name, created_at, updated_at
        FROM users
        ORDER BY created_at DESC
        LIMIT %s OFFSET %s
    """,
    
    "update_user": """
        UPDATE users
        SET email = %s, name = %s, updated_at = CURRENT_TIMESTAMP
        WHERE id = %s
        RETURNING id, email, name, created_at, updated_at
    """,
    
    "delete_user": """
        DELETE FROM users
        WHERE id = %s
    """
} 