FROM python:3
ADD l7informatics_challenge.py /
RUN pip install numpy
RUN pip install matplotlib
CMD ["python", "C:/Users/Ben/Desktop/Life/Resumes/Summer-2020/L7informatics/l7informatics_challenge.py"]