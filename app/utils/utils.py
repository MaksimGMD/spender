def is_current_user_owner(current_user_id: int, user_id: int) -> bool:
    """
    Проверяет, является ли текущий пользователь владельцем.

    Args:
        current_user_id (int): Идентификатор текущего пользователя.
        user_id (int): Идентификатор пользователя, для которого выполняется проверка.

    Returns:
        bool: True, если текущий пользователь является владельцем указанного пользователя, в противном случае False.
    """
    return current_user_id == user_id
