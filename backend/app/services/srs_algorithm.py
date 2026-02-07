from datetime import datetime, timedelta

def calculate_next_review(current_interval: int, current_ease: float, quality: str):
    """
    quality: 'forgot' (Oublié), 'hard' (Difficile), 'easy' (Facile)
    """
    if quality == 'forgot':
        return 1, current_ease, datetime.now() + timedelta(days=1)
    
    if quality == 'hard':
        new_ease = max(1.3, current_ease - 0.15)
        new_interval = max(1, int(current_interval * 1.2))
    else: # 'easy'
        new_ease = current_ease + 0.15
        new_interval = int(current_interval * current_ease)
        
    return new_interval, new_ease, datetime.now() + timedelta(days=new_interval)
