import cv2
import numpy as np

isDragging = False
x0, y0, w, h = -1, -1, -1, -1
blue, red = (255, 0, 0), (0, 0, 255)


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y



title = 'mouse event'

img = cv2.imread('./images/before_parking.jpg')
after_img = cv2.imread('./images/after_parking.jpg')

print(img.shape)
cv2.imshow(title, img)
# 주차장 블록 배열

blocks = []
def onMouse(event, x, y, flags, param):
    global isDragging, x0, y0, img
    if event == cv2.EVENT_RBUTTONDOWN:
        # 지름이 30픽셀인 검은색 원을 해당 좌표에 그림, -1은 채우기
        print(event, x, y, )
        point = Point(x, y)
        blocks.append(point)
        cv2.circle(img, (x, y), 5, (255, 0, 0), -1)
        cv2.imshow(title, img)

    if event == cv2.EVENT_LBUTTONDOWN:
        isDragging = True
        x0 = x
        y0 = y

    elif event == cv2.EVENT_MOUSEMOVE:
        if isDragging:
            img_draw = img.copy()
            cv2.rectangle(img_draw, (x0, y0), (x, y), blue, 2)
            cv2.imshow('img', img_draw)
    elif event == cv2.EVENT_LBUTTONUP:
        if isDragging:
            isDragging = False
            w = x - x0
            h = y - y0
            print("x:%d, y:%d, w:%d, h:%d" % (x0, y0, w, h))
            if w > 0 and h > 0:
                img_draw = img.copy()
                #cv2.rectangle(img_draw, (x0, y0), (x, y), red, 2)
                for i in range(y0, y0+h):
                    for j in range(x0, x0+w):
                        img_draw[i][j] = [136, 136, 136]
                print(img_draw[0][0])
                cv2.imshow('img', img_draw)
                cv2.imwrite('images/before_parking.jpg', img_draw)
            else:
                cv2.imshow('img', img)
                print("잘못 드래그함.")

cv2.setMouseCallback(title, onMouse)

while True:
    if cv2.waitKey(0) & 0xFF == 27:
        break
cv2.destroyAllWindows()

points = []
for i in range(len(blocks)):
    tmp = Point(blocks[i].x, blocks[i].y)
    points.append(tmp)
a11 = Point(149, 134)
a12 = Point(294, 244)
a13 = Point(437, 244)
a14 = Point(580, 244)
a15 = Point(728, 244)
a16 = Point(871, 244)
a21 = Point(155, 605)
a22 = Point(302, 605)
a23 = Point(441, 605)
a24 = Point(590, 605)
a25 = Point(728, 605)
a26 = Point(875, 605)

#a11_block = img[a11.y:a11.y + 10][a11.x:a11.y + 10]
# 구역안에 있는 총 픽셀 수
count = 0
# 구역안에서 픽셀 정보가 변한 픽셀의 수
changed_count = 0
# 오차범위
for i in range(points[0].x, points[0].x + 3):
    for j in range(points[0].y, points[0].y + 3):
        count += 1
        # 나원웅이 고민해야될 부분.
        # img[i][j]가 픽셀의 3가지 BGR정보를 담고있는것임. 예를 들어 img[i][j] = [136, 136, 136]
        if img[i][j][0] > 50 and img[i][j][0] < 136:
            print("0, 1, 2번째 : ", img[i][j][0], img[i][j][1], img[i][j][2])
            changed_count += 1
print("총 픽셀 수", count)
print("변화한 픽셀 수 ", changed_count)
if changed_count > (0.2 * count):
    print("a11 주차중!!!!")
else:
    print("a11 비어있음!!")
#a12_block = img[a12.y:a12.y + 10][a12.x:a12.y + 10]
print('주차장 칸 수 :', len(blocks))
