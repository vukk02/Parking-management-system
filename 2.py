import tkinter as tk
from tkinter import Canvas, ttk
import tkinter.messagebox as messagebox
import cv2
from PIL import Image, ImageTk
import torch
import asyncio
import websockets
import json
import threading
import function.utils_rotate as utils_rotate
import function.helper as helper
import datetime  










    def handle_msg(self, ws, msg):
        uid, mode = msg.split(";")
        print(f"UID: {uid}, Mode: {mode}")

        if mode == "IN":
            if self.is_monthly(uid):
                if self.is_in_parking(uid):
                    print("xe o trong bai")
                else:
                    self.process_monthly_in(uid)
            else:
                self.process_regular_in(uid)

        elif mode == "OUT":
            if self.is_in_parking(uid):
                if self.is_monthly(uid):
                    self.process_monthly_out(uid)
                else:
                    self.process_exit(uid, mode)
            else:
                print("du lieu sai")

    def is_monthly(self, uid):
        return uid in [u["UID"] for u in self.monthly_users]

    def is_in_parking(self, uid):
        return uid in self.parking_users

    def process_exit(self, uid, mode):
        plate = self.read_plate_out
        if plate:
            self.remove_car(uid)
            self.update_revenue(4000)
            self.send_to_esp("OUT")
            print("Da kiem Tra xe Ra.")

    def process_monthly_in(self, uid):
        plate = self.read_plate_in
        if plate and self.verify_monthly(uid, plate):
            self.add_car(uid, plate)
            self.send_to_esp("IN")
            print("Da kiem Tra xe vao")

    def process_monthly_out(self, uid):
        plate = self.read_plate_out
        if plate and self.verify_monthly(uid, plate):
            self.remove_car(uid)
            self.send_to_esp("out")
            print("Da kiem Tra xe ra")

    def process_regular_in(self, uid):
        plate = self.read_plate_in
        if plate and self.is_online_reg(plate):
            self.add_car(uid, plate)
            self.send_to_esp("IN")
            print("Da kiem Tra xe vao")
        elif self.get_free_spots() <= 0:
            print("Parking lot full.")
        else:
            self.add_car(uid, plate)
            self.send_to_esp("IN")
            print("Regular entry processed successfully.")

    def send_to_esp(self, action):
        print(f"Sending to ESP: {action}")










    def read_plate_in():
        global current_vehicle_count, daily_vehicle_count
        ret, frame = cap1.read()
        if ret:
            plates = model(frame, size=640)
            list_plates = plates.pandas().xyxy[0].values.tolist()

            if list_plates:
                x1, y1, x2, y2 = int(list_plates[0][0]), int(list_plates[0][1]), int(list_plates[0][2]), int(list_plates[0][3])
                plate_img = frame[y1:y2, x1:x2]
                plate_img = cv2.resize(plate_img, (200, 100))
                lp_text = ""
                for cc in range(0, 2):
                    for ct in range(0, 2):
                        processed_img = utils_rotate.deskew(plate_img, cc, ct)
                        lp_text = helper.read_plate(model_recognize, processed_img)
                        if lp_text != "unknown":
                            break
                    if lp_text != "unknown":
                        break

                plate_img_pil = Image.fromarray(cv2.cvtColor(plate_img, cv2.COLOR_BGR2RGB))
                plate_imgtk = ImageTk.PhotoImage(plate_img_pil)
                self.uic.lbBienSoXeVao.create_image(150, 60, image=plate_imgtk)
                self.uic.lbBienSoXeVao.image = plate_imgtk  
                self.uic.lXeVao.create_text(150, 35, text=lp_text, font=("Arial", 20), fill="black")

    def read_plate_out():
        global current_vehicle_count, daily_vehicle_count
        ret, frame = cap2.read()
        if ret:
            plates = model(frame, size=640)
            list_plates = plates.pandas().xyxy[0].values.tolist()

            if list_plates:
                x1, y1, x2, y2 = int(list_plates[0][0]), int(list_plates[0][1]), int(list_plates[0][2]), int(list_plates[0][3])
                plate_img = frame[y1:y2, x1:x2]
                plate_img = cv2.resize(plate_img, (200, 100))
                lp_text = ""
                for cc in range(0, 2):
                    for ct in range(0, 2):
                        processed_img = utils_rotate.deskew(plate_img, cc, ct)
                        lp_text = helper.read_plate(model_recognize, processed_img)
                        if lp_text != "unknown":
                            break
                    if lp_text != "unknown":
                        break

                plate_img_pil = Image.fromarray(cv2.cvtColor(plate_img, cv2.COLOR_BGR2RGB))
                plate_imgtk = ImageTk.PhotoImage(plate_img_pil)
                self.uic.lbBienSoXeVao.create_image(150, 60, image=plate_imgtk)
                self.uic.lbBienSoXeVao.image = plate_imgtk  
                self.uic.lXeVao.create_text(150, 35, text=lp_text, font=("Arial", 20), fill="black")