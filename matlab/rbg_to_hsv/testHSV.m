%test hsv
RGB=imread('peppers.png');
HSV = rgb2hsv(RGB);
imshow(RGB)
figure
imshow(HSV)
figure
HSV(10:10:end,:,:)=0;
HSV(:,10:10:end,:)=0;
imshow(HSV)