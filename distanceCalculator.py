# Calculates the shoulder position
def calcShoulderHeights(results, image_height):
    right = round(results.pose_landmarks.landmark[12].y, 2) * image_height
    left = round(results.pose_landmarks.landmark[11].y, 2) * image_height

    return (right + left)/2

# Calculates the hip position
def calcHipsHeights(results, image_height):
    right = round(results.pose_landmarks.landmark[24].y, 2) * image_height
    left = round(results.pose_landmarks.landmark[23].y, 2) * image_height

    return (right + left)/2

# Calculates the knee position
def calcKneeHeights(results, image_height):
    right = round(results.pose_landmarks.landmark[26].y, 2) * image_height
    left = round(results.pose_landmarks.landmark[25].y, 2) * image_height

    return (right + left)/2

# Calculates the toe position
def calcFootHeights(results, image_height):
    right = round(results.pose_landmarks.landmark[31].y, 2) * image_height
    left = round(results.pose_landmarks.landmark[32].y, 2) * image_height

    return (right + left)/2
