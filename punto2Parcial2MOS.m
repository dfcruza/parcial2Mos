clc, clear, close all
syms z x y;% variables simbolicas
z= (1- x).^2 + 100*(y - x.^2).^2; %funcion a minimizar
ezsurf(z); %graficar la funcion
hold on;

v=[x;y];
x_i=0;  %valor inicial en x
y_i=10;  %valor inicial en y
v_i = [x_i;y_i]; %vector de valores iniciales
grad_z=gradient(z); %gradiente
hess_z=hessian(z); %hessiano


convergencia=0.001;  % convergencia

a=0.9;
minimos = []; %vector de minimos
minimos_z = []; %vector de minimos en z

i=1;
grad_z_i = double(subs(grad_z,v,v_i)); %Evaluar el xi en el gradiente
while norm(grad_z_i) > convergencia

    i=i+1;
 
    grad_z_i = double(subs(grad_z,v,v_i));
    
    z_i=double(subs(z,v,v_i)); %Evaluar el xi en f(x) para graficar posteriormente

    inv_hess_z=inv(hessian(z,v)); %Inversa del hessiano 
    inv_hess_z_i = double(subs(inv_hess_z,v,v_i));
    v_i_new=v_i - a* inv_hess_z_i * grad_z_i; %Expresión de Newton Raphson
    v_i=v_i_new;  %Actualizar el xi
    plot3(v_i(1), v_i(2),z_i,"og"); %Graficar el xi
   
end
p = plot3(v_i(1), v_i(2),z_i,'o','LineWidth',4);
p.MarkerFaceColor = [1 0.5 0];
p.MarkerEdgeColor = [1 0.5 0];
disp(v_i);