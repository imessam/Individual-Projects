function P=z_polynomial(w0, zeta, Ts)
s=w0*(-zeta+1i*sqrt(1-zeta*zeta));
z=exp(s*Ts);
rez=real(z); imz=imag(z);
P=[1, -2*rez, rez*rez+imz*imz];