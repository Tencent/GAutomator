# -*- coding: UTF-8 -*-

def transfer_image_coordinate_to_display(pt, image_size, display_size, display_orientation):
    """
    功能：图像坐标系到屏幕坐标系转换，屏幕坐标系的原点会随着屏幕旋转而变化
    输入：目标点的图像坐标，（图像宽，图像高），（视图宽，视图高）,视图方向（0,1,2,3）
    输出：目标点的屏幕坐标
     """
    percent_x = 1.0 * pt[0] / image_size[0]
    percent_y = 1.0 * pt[1] / image_size[1]
    if display_orientation == 0:
        return (percent_x * display_size[0], percent_y * display_size[1])
    elif display_orientation == 1:
        return (percent_y * display_size[0], display_size[1] - percent_x * display_size[1])
    elif display_orientation == 2:  # untested
        return (display_size[0] - percent_x * display_size[0], display_size[1] - percent_y * display_size[1])
    else:  # (display_orientation==3)
        return (display_size[0] - percent_y * display_size[0], percent_x * display_size[1])

def transfer_display_coordinate_to_image(pt, display_size , display_orientation ,image_size):
        """
        功能：屏幕坐标系到图像坐标系转换，屏幕坐标系的原点会随着屏幕旋转而变化
        输入：目标点的屏幕坐标，（视图宽，视图高），视图方向（0,1,2,3），（图像宽，图像高）
        输出：目标点的图像坐标
         """
        percent_x = 1.0 * pt[0] / display_size[0]
        percent_y = 1.0 * pt[1] / display_size[1]
        if display_orientation == 0:
            return (percent_x * image_size[0], percent_y * image_size[1])
        elif display_orientation == 1:
            return (image_size[0]-percent_y * image_size[0], percent_x*image_size[1])
        elif display_orientation == 2:  # untested
            return (image_size[0] - percent_x * image_size[0], image_size[1] - percent_y * image_size[1])
        else:  # (display_orientation==3)
            return (percent_y * image_size[0],image_size[1] - percent_x * image_size[1] )

def transfer_image_coordinate_list_to_display(pts, image_size, display_size, display_orientation):
    """
    功能：图像坐标系到屏幕坐标系转换，屏幕坐标系的原点会随着屏幕旋转而变化
    输入：目标点集的图像坐标，（图像宽，图像高），（视图宽，视图高）,视图方向（0,1,2,3）
    输出：目标点集的屏幕坐标
     """
    ret_list = []
    for pt in pts:
        ret_list.append(transfer_image_coordinate_to_display(pt, image_size, display_size, display_orientation))
    return ret_list

def transfer_display_coordinate_list_to_image(pts, display_size, display_orientation, image_size):
    """
    功能：屏幕坐标系到图像坐标系转换，屏幕坐标系的原点会随着屏幕旋转而变化
    输入：目标点集的屏幕坐标，（视图宽，视图高），视图方向（0,1,2,3），（图像宽，图像高）
    输出：目标点集的图像坐标
     """
    ret_list = []
    for pt in pts:
        pt=transfer_display_coordinate_to_image(pt, display_size, display_orientation,image_size)
        ret_list.append((int(pt[0]),int(pt[1])))
    return ret_list
