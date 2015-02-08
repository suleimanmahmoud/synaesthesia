cc=hsv(12);
figure; 
hold on;
for i=1:12
    plot([0 1],[0 i],'color',cc(i,:));
end
crgb = hsv2rgb(cc)

%%
figure

%# First, create a 100-by-100 image to texture the cone with:

H = repmat(linspace(0,1,100),100,1);     %# 100-by-100 hues
S = repmat([linspace(0,1,50) ...         %# 100-by-100 saturations
            linspace(1,0,50)].',1,100);  %'
V = repmat([ones(1,50) ...               %# 100-by-100 values
            linspace(1,0,50)].',1,100);  %'
hsvImage = cat(3,H,S,V);                 %# Create an HSV image
C = hsv2rgb(hsvImage);                   %# Convert it to an RGB image

%# Next, create the conical surface coordinates:

theta = linspace(0,2*pi,100);  %# Angular points
X = [zeros(1,100); ...         %# X coordinates
     cos(theta); ...
     zeros(1,100)];
Y = [zeros(1,100); ...         %# Y coordinates
     sin(theta); ...
     zeros(1,100)];
Z = [2.*ones(2,100); ...       %# Z coordinates
     zeros(1,100)];

%# Finally, plot the texture-mapped surface:

surf(X,Y,Z,C,'FaceColor','texturemap','EdgeColor','none');
axis equal
%%
clear all;clc;close all;
k = 1;
nHues=18; %12 ou multiplos de 12
ccm=hsv(nHues);%vetor com 12 hues
tamanhoX=150;
tamanhoY=200;
tamQuadrado=ceil(sqrt(tamanhoX*tamanhoY/nHues)) %tamanho do quadrado é definido para manter a proporção tamX/tamY
nRows=tamanhoX/tamQuadrado
nCols=tamanhoY/tamQuadrado


for row = 0 : nRows-1
    for col = 0 : nCols-1
        for quadX = 1 : tamQuadrado
            for quadY = 1 : tamQuadrado
                hsvImage(row*tamQuadrado+quadX, col*tamQuadrado+quadY, 1) = ccm(k, 1);
                hsvImage(row*tamQuadrado+quadX, col*tamQuadrado+quadY, 2) = ccm(k, 2);
                hsvImage(row*tamQuadrado+quadX, col*tamQuadrado+quadY, 3) = ccm(k, 3);
            end
        end
        k = k + 1;
    end
  
end
% Now convert that to an RGB image
imshow(hsvImage)
imwrite(hsvImage, ['ImagemHSV' num2str(nHues) '.jpg']);
rgbImage = hsv2rgb(hsvImage);
imwrite(rgbImage, ['ImagemRGB' num2str(nHues) '.jpg']);
display('terminou')

%%
%%
clear all;clc;close all;
k = 1;
nHues=96; %12 ou multiplos de 12
ccm=hsv(nHues) %vetor com 12 hues
tamQuadrado=50; %tamanho do quadrado é definido para manter a proporção tamX/tamY
%tam=tamQuadrado*tamQuadrado*nHues
nRows=4
nCols=nHues/nRows

for row = 0 : nRows-1
    for col = 0 : nCols-1
        for quadX = 1 : tamQuadrado
            for quadY = 1 : tamQuadrado
                hsvImage(row*tamQuadrado+quadX, col*tamQuadrado+quadY, 1) = ccm(k, 1);
                hsvImage(row*tamQuadrado+quadX, col*tamQuadrado+quadY, 2) = ccm(k, 2);
                hsvImage(row*tamQuadrado+quadX, col*tamQuadrado+quadY, 3) = ccm(k, 3);
            end
        end
        k = k + 1;
    end
  
end
% Now convert that to an RGB image
imshow(hsvImage)
imwrite(hsvImage, ['ImagemHSV' num2str(nHues) '.png']);
%save(['ImagemHSV' num2str(nHues) '.txt'], 'hsvImage', '-ASCII', '-append');

rgbImage = hsv2rgb(hsvImage);
	
imwrite(rgbImage, ['ImagemRGB' num2str(nHues) '.png']);
display('terminou')