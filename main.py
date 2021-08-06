import cv2
import numpy as np

# 드래그 앤 드롭 기능 구현하기 위한 변수
isDragging = False
x0, y0, w, h = -1, -1, -1, -1
blue, red = (255, 0, 0), (0, 0, 255)

# 픽셀 정보 x좌표, y좌표
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y



title = 'before parking'

# 주차 전 이미지
img = cv2.imread('./images/before_parking.jpg')
print(img.dtype)
# 주차 후 이미지
after_img = cv2.imread('./images/after_parking.jpg')

print(img.shape)
cv2.imshow(title, img)
# 주차장 블록 배열

# 마우스로 찍어준 block들 정보 담기 위한 배열
# 배열의 원소의 형식은 위의 Point 객체 타입
blocks = []

def onMouse(event, x, y, flags, param):
    # 아래의 변수들을 전역변수로 참조하겠다는 의미
    global isDragging, x0, y0, img

    # 마우스 오른쪽 버튼으로 점찍는 기능
    if event == cv2.EVENT_RBUTTONDOWN:
        # 지름이 30픽셀인 검은색 원을 해당 좌표에 그림, -1은 채우기
        tmp_img = img.copy()
        print(event, x, y, )
        point = Point(x, y)
        blocks.append(point)
        cv2.circle(tmp_img, (x, y), 5, (255, 0, 0), -1)
        cv2.imshow(title, tmp_img)
    # 만약 드래그 시작한다면 isDragging boolean 값을 True로 설정
    if event == cv2.EVENT_LBUTTONDOWN:
        isDragging = True
        x0 = x
        y0 = y
    # 드래그 중이라면
    elif event == cv2.EVENT_MOUSEMOVE:
        if isDragging:
            img_draw = after_img.copy()
            cv2.rectangle(img_draw, (x0, y0), (x, y), blue, 2)
            cv2.imshow('img', img_draw)
    # 드래그가 끝났다면
    elif event == cv2.EVENT_LBUTTONUP:
        if isDragging:
            isDragging = False
            w = x - x0
            h = y - y0
            print("x:%d, y:%d, w:%d, h:%d" % (x0, y0, w, h))
            if w > 0 and h > 0:
                img_draw = after_img.copy()
                # 드래그 한 영역을 빨간색 박스로 칠하는 함수
                #cv2.rectangle(img_draw, (x0, y0), (x, y), red, 2)

                # 주차장 바닥이 회색이므로 사진 편집하기 위해 픽셀을 회색 [136, 136, 136]으로 바꿔주는 반복문
                for i in range(y0, y0+h):
                    for j in range(x0, x0+w):
                        img_draw[i][j] = [136, 136, 136]
                print(img_draw[0][0])
                cv2.imshow('img', img_draw)
                cv2.imwrite('images/changed_parking.jpg', img_draw)
            # 잘못 드래그 한 경우
            else:
                cv2.imshow('img', img)
                print("잘못 드래그함.")
# 마우스의 동작이 인식되면 Callback 함수로 onMouse 함수가 실행되는 것
# Callback 이란 예를 들어 setMouseCallback 함수가 실행되고 난 후, 이어서 실행되는 함수를 Callback 함수라고 함
cv2.setMouseCallback(title, onMouse)

# 사진이 출력되는 창에서 ESC 버튼을 누르면 종료되게 설정한 내용
while True:
    if cv2.waitKey(0) & 0xFF == 27:
        break
cv2.destroyAllWindows()


print("총 주차장 칸 수 : ", len(blocks))
# 구역안에 있는 총 픽셀 수
count = 0
# 구역안에서 픽셀 정보가 변한 픽셀의 수
changed_count = 0
before_points = []
after_points = []
for length in range(len(blocks)):
    row = blocks[length].y
    col = blocks[length].x
    # 기존 이미지의 블록
    tmp = img[row - 5:row + 5, col - 5:col + 5]
    before_points.append(tmp)
    # 주차 후 이미지의 블록
    tmp = after_img[row - 5:row + 5, col - 5:col + 5]
    after_points.append(tmp)

# 주차 전 이미지와 주차 후 이미지의 정보를 이용해서
# 주차 여부 판단하는 알고리즘 구현
for i in range(len(blocks)):
    # 달라진 픽셀 개수 확인하기 위한 변수
    diff_check = 0
    # 주차 구분 영역 사각형의 가로(r), 세로(c)값
    r = len(after_points[i])
    c = len(after_points[i][0])
    # before_block, after_block 의 shape 는 (10, 10, 3)이 나온다
    # 그 이유는 before_points, after_points 의 shape 는 (점을 찍은 블록의 개수, 10, 10, 3)이기 때문에
    before_block = np.array(before_points[i], dtype=np.int16)
    after_block = np.array(after_points[i], dtype=np.int16)
    block_size = r * c
    for x in range(r):
        for y in range(c):
            # before_pixel, after_pixel 의 shape 는 예를 들어, BGR 순서로 [136, 136, 136]
            before_pixel = before_block[x][y]
            after_pixel = after_block[x][y]

            # 주차 전과 후의 이미지 픽셀들 합의 차이를 저장하는 변수
            diff = np.sum(before_pixel) - np.sum(after_pixel)
            # 차이 변수에 절대값 적용
            abs_diff = abs(diff)
            # 차이가 나는 픽셀의 정보가 10 보다 크면 block 의 상태 변했다고 인식
            # 이 부분이 분별하는 핵심 알고리즘 부분
            if(abs_diff > 10):
                diff_check += 1

    print("달라진 pixel의 수는 : ", diff_check)
    # 반복문에서는 i가 0부터 시작하므로 보기 편하게 하기위해 +1했음
    block_num = i+1
    if diff_check > (block_size * 0.2):
        print("-----------%d번째 block 상태 변함!!!------------" %block_num)
    else:
        print("%d번째 block 상태 안변함" %block_num)

# 주차 후 이미지 출력
cv2.imshow('after parking', after_img)
while True:
    if cv2.waitKey(0) & 0xFF == 27:
        break
cv2.destroyAllWindows()
