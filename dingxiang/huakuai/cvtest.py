import cv2
# 显示或保存图片
def cv_show(name, img, save=False):
    if save:
        cv2.imwrite(name, img)
    cv2.imshow(name, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# 获取滑块的大小
def fix_img(filename):
    #  1.为了更高的准确率，使用二值图像
    img = cv2.imread(filename)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    # 2.将轮廓提取出来
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    cnt = contours[0]
    # 3.用绿色(0, 255, 0)来画出最小的矩形框架
    x, y, w, h = cv2.boundingRect(cnt)
    rect_x = x + w
    rect_y = y + h
    # print(x, y, rect_x, rect_y)  # x，y是矩阵左上点的坐标，w，h是矩阵的宽和高
    img = cv2.rectangle(img, (x, y), (rect_x, rect_y), (0, 255, 0), 1)
    # 高度和宽度
    mixintu = img[y:rect_y, x:rect_x]
    return mixintu


def mian():
    # 1.对滑块进行图片处理
    tp_img = fix_img('images/front.webp')  # 裁掉透明部分，找出滑块的大小
    tp_edge = cv2.Canny(tp_img, 100, 200)
    tp_pic = cv2.cvtColor(tp_edge, cv2.COLOR_GRAY2BGR)

    # 2.对背景进行图片处理
    bg_img = cv2.imread('background.jpg')
    bg_edge = cv2.Canny(bg_img, 400, 200)
    bg_pic = cv2.cvtColor(bg_edge, cv2.COLOR_GRAY2BGR)

    # 3.模板匹配matchTemplate
    res = cv2.matchTemplate(bg_pic, tp_pic, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    print(min_val, max_val, min_loc, max_loc)  # 最小值，最大值，最小值的位置，最大值的位置

    # 绘制方框 
    X = max_loc[0]
    th, tw = tp_pic.shape[:2]
    t1 = max_loc  # 左上角点的位置
    br = (t1[0] + tw, t1[1] + th)  # 右下角点的坐标
    cv2.rectangle(bg_img, t1, br, (0, 0, 225), 2)  # 绘制矩形
    cv_show('out.png', bg_img, True)


if __name__ == '__main__':
    mian()


