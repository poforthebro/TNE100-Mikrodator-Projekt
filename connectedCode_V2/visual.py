import cv2


class display:
    def __init__(self, scale_X, scale_y):
        self.scale_x = scale_X
        self.scale_y = scale_y


    def display_frame(self, high_res_frame, faces, quality, delta):
        if faces is not None: # Check that there is a face available
            best_face = faces[0]
            best_face_coord = [int(coord) for coord in best_face[:4]]
            
            small_x = best_face_coord[0] + ( best_face_coord[2] // 2 ) # Center of face
            small_y = best_face_coord[1] + ( best_face_coord[3] // 2 ) # Center of face

            # Put the delta text in left top corner
            cv2.putText(high_res_frame, f"Delta X: {delta[0]}, Delta Y: {delta[1]}", (10, 30), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2) # Use font hershey with color green
        



            score = int(quality)
            cv2.putText(high_res_frame, f"Score: {score}", (int(best_face_coord[0] * self.scale_x), int( (best_face_coord[1] - 10) * self.scale_y) ), 
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            draw_circle_face(high_res_frame, best_face_coord, self.scale_x, self.scale_y)

            # Square around all faces
            for face in faces: # Loop through alla faces
                draw_rectangle(high_res_frame, face, self.scale_x, self.scale_y)


        cv2.imshow('FATTIG ansikts spårning', high_res_frame)




# draw a rectangle around a face
def draw_rectangle(frame, face, scale_x, scale_y):
    box = list(map(int, face[:4]))

    small_x, small_y, small_w, small_h = box[0], box[1], box[2], box[3]

    big_x = int(small_x * scale_x)
    big_y = int(small_y * scale_y)
    big_w = int(small_w * scale_x)
    big_h = int(small_h * scale_y)

    cv2.rectangle(frame, (big_x, big_y), (big_w + big_x, big_h + big_y), (0, 255, 0), 2)
    
    landmarks = list(map(int, face[4:14]))

    # Uncomment both lines to draw circles in eyes, nose and mouth
    #for i in range(5):

    # Uncomment line to draw circles in eyes, nose and mouth
    # cv2.circle(frame, (landmarks[2*i], landmarks[2*i+1]), 2, (0, 0, 255), -1)


# Draw Circle in middle of best face
def draw_circle_face(frame, coordinates, scale_x, scale_y):
    small_x = coordinates[0] + ( coordinates[2] // 2 )
    small_y = coordinates[1] + ( coordinates[3] // 2 )

    big_x = int(small_x * scale_x)
    big_y = int(small_y * scale_y)

    centerOfCircle = (big_x, big_y) 
    image = cv2.circle(frame, centerOfCircle, radius = 10, color = (0, 0, 255), thickness = -1)
