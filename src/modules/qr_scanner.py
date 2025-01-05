import cv2

def auto_detect():
    img = cv2.imread("/tmp/raw_image.png")
    detector = cv2.QRCodeDetector()
    data, bbox, straight_qrcode = detector.detectAndDecode(img)
    return data
