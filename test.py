def smallest_valid_window(arr, min_val):
    n = len(arr)
    best_window = None
    min_sum = float('inf')
    best_left, best_right = -1, -1
    
    left = 0 
    window_sum = 0
    queue = deque()
    
    for right in range(n):
        window_sum += arr[right]
        queue.append(arr[right])
        
        while queue and window_sum >= min_val:
            if window_sum < min_sum or (window_sum == min_sum and len(queue) < (best_right - best_left + 1)):
                best_window = list(queue)
                min_sum = window_sum
                best_left, best_right = left, right
            
            window_sum -= queue.popleft()
            left += 1
    
    return (best_left, best_right) if best_window is not None else (-1, -1)


def truncate_name(name, max_length):
    """Truncates name by removing words from the middle until it fits max_length, replacing them with '...'."""
    if len(name) <= max_length:
        return name
    
    words = name.split()
    
    words = [word for word in words if word.lower() not in UNNEEDED_WORDS]
    
    ellipse = "..." 
    
    max_length -= len(ellipse)+2
                
    curr_len = len(" ".join(words))
    if curr_len <= max_length:
        return " ".join(words)
    
    ellipse = "..." 
    lengths = [len(word)+1 for word in words]
    
    left, right = smallest_valid_window(lengths, curr_len-max_length)
    if left == -1:
        return ellipse
    
    words = words[:left] + [ellipse] + words[right+1:]
    return " ".join(words)