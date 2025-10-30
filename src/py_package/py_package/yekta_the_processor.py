import numpy as np
import cv2 

def find_road_lines(binary_warped):
    
    histogram = np.sum(binary_warped[binary_warped.shape[0]//2:, :], axis=0)
    out_img = np.dstack((binary_warped, binary_warped, binary_warped))

    midpoint = int(histogram.shape[0] // 2)
    leftx_base = np.argmax(histogram[:midpoint])
    rightx_base = np.argmax(histogram[midpoint:]) + midpoint

    nwindows = 9
    margin = 20
    minpix = 50
    window_height = int(binary_warped.shape[0] // nwindows)

    nonzero = binary_warped.nonzero()
    nonzeroy = np.array(nonzero[0])
    nonzerox = np.array(nonzero[1])

    leftx_current = leftx_base
    rightx_current = rightx_base

    left_lane_inds = []
    right_lane_inds = []

    for window in range(nwindows):
        
        win_y_low = binary_warped.shape[0] - (window + 1) * window_height
        win_y_high = binary_warped.shape[0] - window * window_height

        win_xleft_low = leftx_current - margin
        win_xleft_high = leftx_current + margin
        win_xright_low = rightx_current - margin
        win_xright_high = rightx_current + margin
        
        cv2.rectangle(out_img,(win_xleft_low,win_y_low),(win_xleft_high,win_y_high),(255,0,0), 2) 
        cv2.rectangle(out_img,(win_xright_low,win_y_low),(win_xright_high,win_y_high),(0,255,0), 2)

        good_left_inds = ((nonzeroy >= win_y_low) & (nonzeroy < win_y_high) &
                        (nonzerox >= win_xleft_low) & (nonzerox < win_xleft_high)).nonzero()[0]
        good_right_inds = ((nonzeroy >= win_y_low) & (nonzeroy < win_y_high) &
                        (nonzerox >= win_xright_low) & (nonzerox < win_xright_high)).nonzero()[0]

        left_lane_inds.append(good_left_inds)
        right_lane_inds.append(good_right_inds)

        if len(good_left_inds) > minpix:
            leftx_current = int(np.mean(nonzerox[good_left_inds]))
        if len(good_right_inds) > minpix:
            rightx_current = int(np.mean(nonzerox[good_right_inds]))

    left_lane_inds = np.concatenate(left_lane_inds) if left_lane_inds else np.array([], dtype=np.int32)
    right_lane_inds = np.concatenate(right_lane_inds) if right_lane_inds else np.array([], dtype=np.int32)

    leftx = nonzerox[left_lane_inds]
    lefty = nonzeroy[left_lane_inds]
    rightx = nonzerox[right_lane_inds]
    righty = nonzeroy[right_lane_inds]

    left_fit = np.polyfit(lefty, leftx, 2) if len(leftx) > 0 else [0, 0, 0]
    right_fit = np.polyfit(righty, rightx, 2) if len(rightx) > 0 else [0, 0, 0]

    ploty = np.linspace(0, binary_warped.shape[0]-1, binary_warped.shape[0])
    left_fitx = left_fit[0]*ploty**2 + left_fit[1]*ploty + left_fit[2]
    right_fitx = right_fit[0]*ploty**2 + right_fit[1]*ploty + right_fit[2]
    
    center_fitx = (left_fitx + right_fitx) / 2
    center_points = np.array([np.transpose(np.vstack([center_fitx, ploty]))], dtype=np.int32)

    center_fit = np.polyfit(ploty, center_fitx, 2)
    a, b, c = center_fit

    out_img[lefty, leftx] = [255, 0, 0]
    out_img[righty, rightx] = [0, 0, 255]
    
    cv2.polylines(out_img, center_points, isClosed=False, color=(0, 0, 255), thickness=2)
    
    return out_img, left_fitx, right_fitx, ploty, left_fit, right_fit, a, b, c

#-----------------------------------------------------------------

def binary_threshold(img):
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # cv2.imshow("Gray", gray)
    blurred = cv2.bilateralFilter(gray, 1, 75, 75)
    # cv2.imshow("blurr", blurred)

    sobelx = cv2.Sobel(blurred, cv2.CV_64F, 1, 0)
    abs_sobelx = np.absolute(sobelx)
    percentile = np.percentile(abs_sobelx, 99)
    scaled_sobel = np.uint8(255 * abs_sobelx / percentile) 
    sx_binary = np.zeros_like(scaled_sobel)
    sx_binary[(scaled_sobel >= 150) & (scaled_sobel <= 255)] = 1 
    
    white_binary = np.zeros_like(blurred)
    white_binary[(blurred>200)&(blurred<=255)] = 1
    
    binary = cv2.bitwise_or(sx_binary, white_binary)
    cv2.imshow("Binary Image", binary * 255)

    return binary
    
#-----------------------------------------------------------------

def calculation(frame):
     
    # frame = cv2.imread("/home/yekta/Downloads/photo_2025-10-28_06-46-22.jpg")
    resized_frame = cv2.resize(frame, (300, 200))   

    src = np.float32(
        [[109, 85],  #TL
        [197, 84],   #TR
        [257, 148],  #BR
        [13, 150]]   #BL
                    )
            
    dst = np.float32(
        [[0, 0],         
        [300, 0],       
        [300, 200],     
        [0, 200]]      
                    )
        
    M = cv2.getPerspectiveTransform(src, dst)
    warped = cv2.warpPerspective(resized_frame, M, (300, 200))

    #-----------------------------------------------------------------

    binary_thresh = binary_threshold(warped)  

    #--------------------------------------------------------------

    lane_overlay, left_fitx, right_fitx, ploty, left_fit, right_fit, a, b, c= find_road_lines(binary_thresh)
    center_fitx = (left_fitx + right_fitx) / 2
        
    left_pts = np.array([np.transpose(np.vstack([left_fitx, ploty]))], dtype=np.float32)
    right_pts = np.array([np.transpose(np.vstack([right_fitx, ploty]))], dtype=np.float32)
    center_pts = np.array([np.transpose(np.vstack([center_fitx, ploty]))], dtype=np.float32)

    Minv = cv2.getPerspectiveTransform(dst, src)
    left_unwarped = cv2.perspectiveTransform(left_pts, Minv)
    right_unwarped = cv2.perspectiveTransform(right_pts, Minv)
    center_unwarped = cv2.perspectiveTransform(center_pts, Minv)

    a = (left_fit[0] + right_fit[0]) / 2
    b= (left_fit[0] + right_fit[1]) / 2
    c= (left_fit[1] + right_fit[2]) / 2
    center_equation = a* ploty**2 + b*ploty + c

    second_derivative = 2*a

    distance_in_moment = (a* 200**2 + b*200 + c) - 150
    print("distance_in_moment", distance_in_moment)

    derivation1 = 2*a*200 + b
    radian = np.arctan(derivation1) 
    degree_in_moment= np.degrees(radian)
    print("degree_in_moment", degree_in_moment)

    distance_sum = 0
    derivation_sum = 0

    for y in range(190, 201):
        #find_distance
        center_equation = a* y**2 + b*y + c
        distance = center_equation - 150
        distance_sum += distance
        # find_degree
        derivation = 2*a*y + b
        radian = np.arctan(derivation ) 
        degree= np.degrees(radian)   
        derivation_sum += degree

    #-------- clean code !! ---------------------------------------------

    '''for y in range(125, 201, 25):
        derivation = 2*a*y + b
        radian = np.arctan(derivation ) 
        degree= np.degrees(radian)'''
    
    x1 = a* 125**2 + b*125 + c
    x2 = a* 150**2 + b*150 + c
    x3 = a* 175**2 + b*175 + c
    x4 = a* 200**2 + b*200 + c

    d1 = 2*a*125 + b
    d2 = 2*a*150 + b
    d3 = 2*a*175 + b
    d4 = 2*a*200 + b

    teta1 = np.arctan(d1) 
    degree1= np.degrees(teta1)
    teta2 = np.arctan(d2) 
    degree2= np.degrees(teta2)
    teta3 = np.arctan(d3) 
    degree3= np.degrees(teta3)
    teta4 = np.arctan(d4) 
    degree4= np.degrees(teta4)

    opt1 = (degree1 - degree2) / np.sqrt((x1-x2)**2 + (25)**2)
    opt2 = (degree1 - degree3) / np.sqrt((x1-x3)**2 + (50)**2)
    opt3 = (degree1 - degree4) / np.sqrt((x1-x4)**2 + (75)**2)
    opt4 = (degree2 - degree3) / np.sqrt((x2-x3)**2 + (25)**2)
    opt5 = (degree2 - degree4) / np.sqrt((x2-x4)**2 + (50)**2)
    opt6 = (degree3 - degree4) / np.sqrt((x1-x2)**2 + (25)**2)

    mean_k = (opt1 + opt2 + opt3 + opt4 + opt5 + opt6) / 6
        
    #---------------------------------------------------------------------
            
    mean_distance = distance_sum/10
    cv2.putText(resized_frame, "Distance:"+str(distance_in_moment), (10,20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1 )
    mean_degree = derivation_sum/10
    cv2.putText(resized_frame, "Degree:"+str(degree_in_moment), (10,40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1 )
    cv2.putText(resized_frame, "second_derivative:"+str(second_derivative), (10,60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1 )
    cv2.putText(resized_frame, "mean_k:"+str(mean_k), (10,80), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1 )

    cv2.polylines(resized_frame, [np.int32(left_unwarped)], isClosed=False, color=(255, 0, 0), thickness=2)  
    cv2.polylines(resized_frame, [np.int32(right_unwarped)], isClosed=False, color=(0, 255, 0), thickness=2)  
    cv2.polylines(resized_frame, [np.int32(center_unwarped)], isClosed=False, color=(0, 255, 255), thickness=2)
    cv2.imshow('Warped frames', warped)
    cv2.imshow("Lane Detection", lane_overlay)
    cv2.imshow("Final", resized_frame)
    print("hello")

    # cv2.waitKey(0)

    return distance_in_moment, degree_in_moment, second_derivative, mean_k
