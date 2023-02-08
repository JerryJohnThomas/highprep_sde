import streamlit as st
import cv2
from syed import calc

def magic_function(a,b):
	# replace this with syeds function
	return 1

	
st.title("Take Preview Photos from 2 Video Sources")

cap1 = cv2.VideoCapture(0)
cap2 = cv2.VideoCapture(1)

ret1, frame1 = cap1.read()
ret2, frame2 = cap2.read()

st.sidebar.title("Display Preview")

if ret1 and ret2:
	st.image(cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB), use_column_width=True, caption="Source 1")
	st.image(cv2.cvtColor(frame2, cv2.COLOR_BGR2RGB), use_column_width=True, caption="Source 2")

if st.sidebar.button("Capture Photos"):
	st.write("Volume Output: ")
	st.write(calc(frame1, frame2))

cap1.release()
cap2.release()

