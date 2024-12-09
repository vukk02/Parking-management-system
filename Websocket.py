import cv2
from pyzbar import pyzbar
import torch
model = torch.hub.load('yolov5-master', 'custom', path='BienSoAndQR.pt', source='local')
model_recognize = torch.hub.load('yolov5-master', 'custom', path='myNumberV4.pt', source='local')
cap = cv2.VideoCapture(0)

def Recognize_character( imgText):
    detection = model_recognize(imgText)
    results = detection.pandas().xyxy[0].to_dict(orient="records")
    results_array = []
    if len(results) == 0:
        return
    for result in results:
        confidence = result['confidence']
        if confidence > 0.7:
            name = result['name']
            x = int(result['xmax'])
            y = int(result['ymax'])
            result_data = [name, x, y]
            results_array.append(result_data)
    y_min = min(results_array, key=lambda result_info: result_info[2])[2]
    row_1 = []
    row_2 = []
    for array in results_array:
        if array[2] - y_min < 30:
            row_1.append(array)
        else:
            row_2.append(array)
    sorted_result_row_1 = sorted(row_1, key=lambda result_info: result_info[1])
    sorted_result_row_2 = sorted(row_2, key=lambda result_info: result_info[1])
    text = ""
    for result_info in sorted_result_row_1:
        text = text + str(result_info[0])
    for result_info in sorted_result_row_2:
        text = text + str(result_info[0])
    if len(text) > 6 and len(text) < 10:
        return text
    else:
        return "ERROR"

def readBienSoXeRa(imgXeRa):
    detectionXeRa = model(imgXeRa)
    resultsXeRa = detectionXeRa.pandas().xyxy[0].to_dict(orient="records")
    for result_1 in resultsXeRa:
        clas_1 = result_1['class']
        confidence_1 = result_1['confidence']
        if clas_1 == 0 and confidence_1 > 0.7:
            x1 = int(result_1['xmin'])
            y1 = int(result_1['ymin'])
            x2 = int(result_1['xmax'])
            y2 = int(result_1['ymax'])
            roiXeRa = imgXeRa[y1:y2, x1:x2]
            textXeRa = Recognize_character(roiXeRa)
            return textXeRa
    return "NO"

def readQRXeRa(imgXeRa):
    detectionXeRa = model(imgXeRa)
    resultsXeRa = detectionXeRa.pandas().xyxy[0].to_dict(orient="records")
    for result_2 in resultsXeRa:
        clas_2 = result_2['class']
        confidence_2 = result_2['confidence']
        if clas_2 == 1 and confidence_2 > 0.7:
            print("Da kiem tra Auto")
            x1 = int(result_2['xmin'])
            y1 = int(result_2['ymin'])
            x2 = int(result_2['xmax'])
            y2 = int(result_2['ymax'])
            roiQR = imgXeRa[y1:y2, x1:x2]
            barcodes = pyzbar.decode(roiQR)
            print("chieu dai Luc dau")
            print(len(barcodes))
            max_attempts = 20  # Số lần thử giải mã tối đa
            attempts = 0  # Biến đếm số lần đã thử
            while len(barcodes) == 0 and attempts < max_attempts:
                attempts += 1
                print("Co gang")
                print(attempts)
                _, imgXeRa = cap.read()
                detectionAttempts = model(imgXeRa)
                resultsAttempts = detectionAttempts.pandas().xyxy[0].to_dict(orient="records")
                for resultAttempt in resultsAttempts:
                    clasAttempt = resultAttempt['class']
                    confidenceAttempt = resultAttempt['confidence']
                    if clasAttempt == 1 and confidenceAttempt > 0.7:
                        x1Attempt = int(result_2['xmin'])
                        y1Attempt = int(result_2['ymin'])
                        x2Attempt = int(result_2['xmax'])
                        y2Attempt = int(result_2['ymax'])
                        roiQRAttempt = imgXeRa[y1Attempt:y2Attempt, x1Attempt:x2Attempt]
                        barcodes = pyzbar.decode(roiQRAttempt)
            print("chieu dai Luc Sau")
            print(len(barcodes))
            for barcode in barcodes:
                print("Thuc hien barcode")
                barcodeData = barcode.data.decode("utf-8")  # Text
                print(barcodeData)
                return barcodeData
    return "NO"
while True:
    _, img = cap.read()
    textBienSoXeRa = readBienSoXeRa(img)
    textQRXeRa = readQRXeRa(img)
    print("Bien So")
    print(textBienSoXeRa)
    print("QR")
    print(textQRXeRa)
    cv2.imshow("IMG", img)
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break
cap.release()
#img = cv2.imread('TEST2.png')
#textBienSoXeRa = readBienSoXeRa(img)
#textQRXeRa = readQRXeRa(img)
#print("Bien So")
#print(textBienSoXeRa)
#print("QR")
#print(textQRXeRa)
#cv2.imshow("IMG", img)
#cv2.waitKey()




