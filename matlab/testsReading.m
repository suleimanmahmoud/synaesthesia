clc;clear all;close all;
%%Reading and showing the images =)
%figure
%img = imread('7Anoes.jpg');
%imshow(img)
figure
scale=0.2;
img = imresize(imread('7Anoes.jpg'), scale);
imgHSV=rgb2hsv(img);
%medfilt2
%K = hmf(img);
imshow(imgHSV)

%%
figure
img = imread('ImagemHSV48.png');
map=colormap(hsv(12))
imshow(img,'ColorMap',map)