%Main script function.
function [R, S, T]=control(w0, zeta,Ts, Pz,Az,Bz)
setGlobalVar();
[R, S, T]=solveRST(w0, zeta,Ts, Pz,Az,Bz);


%Get the current Date and store it into a global variable.
function setGlobalVar()
global st
st =  strrep(datestr(datetime('now')), ':', '_');
function DateString = getGlobalVar
global st
DateString=st;


%Generate P(z).
function P=z_polynomial(w0, zeta, Ts)
s=w0*(-zeta+1i*sqrt(1-zeta*zeta));
z=exp(s*Ts);
rez=real(z); imz=imag(z);
P=[1, -2*rez, rez*rez+imz*imz];


%finds if A has no integrator.
function no_int=has_no_integrator(A)
r=roots(A);
sr=size(r);
no_int=true;
for k=1:sr(1)
    if r(k)==1
        no_int=false;
    end
end


%Generate the required parameters.
function [Ts, B, A, Hr, Hs, dist, P, Bm, Am]=acquire_data(w0, zeta,Ts, Pz,Az,Bz)

%GET PLANT PTF

%discrete plant
    B=Bz;
    A=Az;

%GET REGULATION P(z) & TRACKING Bm(z)/Am(z)
    P=Pz;
    Am=z_polynomial(w0, zeta, Ts);
    Bm=sum(Am);%Bm(z)=Am(1)
   
Hr=1;
Hs=1;
distf=0;
if distf==0
    dist=[1 -1];
else
    dist=[1, -2*cos(2*pi*distf*Ts), 1];
end


%Generate the Simulink Model and the C Code.
function [Ts,R,S,T]=generateSimulink(Ts, Bp, Ap,Bm, Am,R,S,T)

%global it_counter;
%it_counter=it_counter+1;
c=clock;
name=sprintf('System_%d%02d%02d_%02d%02d_%02d', c(1), c(2), c(3), c(4), c(5), round(c(6)));

sim_time=100;
t_ref=5; 
str_Ts=num2str(Ts);
x=0; y=0;
sys=new_system(name);
set_param(name, 'stoptime',num2str(sim_time));

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

x=x+0; y=y+100;%step position
add_block('simulink/Sources/Step', [name '/Reference'], 'position',[x, y, x+30, y+30],...
    'time',num2str(t_ref*Ts), 'sampletime',str_Ts);
x=x+30;%step width

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

x=x+35;%spacing
add_block('simulink/Discrete/Discrete Filter', [name '/Bm(z)//Am(z)'], 'position',[x, y, x+195, y+30],...
    'numerator',['[' num2str(Bm) ']'], 'denominator',['[' num2str(Am) ']'], 'sampletime',str_Ts);
x=x+195;%tracking width
add_line(name, 'Reference/1', 'Bm(z)//Am(z)/1');

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

x=x+35;%spacing
add_block('simulink/Discrete/Discrete Filter', [name '/T(z)'], 'position',[x, y, x+195, y+30],...
    'numerator',['[' num2str(T) ']'], 'denominator','[1]', 'sampletime',str_Ts);
x=x+195;%T width
add_line(name, 'Bm(z)//Am(z)/1', 'T(z)/1');

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

x=x+25;%spacing
add_block('simulink/Math Operations/Sum', [name '/Sum1'], 'position',[x, y+5, x+20, y+5+20],...
    'inputs','|+-');
x=x+20;%sum width
add_line(name, 'T(z)/1', 'Sum1/1');


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

x=x+35;%spacing
add_block('simulink/Discrete/Discrete Filter', [name '/1//S(z)'], 'position',[x, y, x+195, y+30],...
    'numerator','[1]', 'denominator',['[' num2str(S) ']'], 'sampletime',str_Ts);
x=x+195;%S width
add_line(name, 'Sum1/1', '1//S(z)/1');

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

x=x+45;
%discrete plant
 add_block('simulink/Discrete/Discrete Filter', [name '/Bp(z)//Ap(z)'], 'position',[x, y, x+195, y+30],...
        'numerator',['[' num2str(Bp) ']'], 'denominator',['[' num2str(Ap) ']'], 'sampletime',str_Ts);
    x=x+195;%plant width
    add_line(name, '1//S(z)/1', 'Bp(z)//Ap(z)/1');
x=x+105;%spacing till sum2

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%feedback blocks
x=x-465; 
y=y+110;%from scope left edge to R
add_block('simulink/Discrete/Discrete Filter', [name '/R(z)'], 'position',[x, y, x+195, y+30],...
    'numerator',['[' num2str(R) ']'], 'denominator','[1]', 'sampletime',str_Ts, 'orientation','left');
%all=get(get_param(block_R, 'handle'))
add_line(name, 'Bp(z)//Ap(z)/1', 'R(z)/1');
add_line(name, 'R(z)/1','Sum1/2');
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


oldPath=pwd;
newPath=getGlobalVar;
mkdir (newPath);
copyfile('config.m',newPath);
cd(newPath);
save_system(sys,'rst');
blocks=find_system('rst');
sub=[get_param(blocks{2}, 'handle');
    get_param(blocks{5}, 'handle');
    get_param(blocks{7}, 'handle');
    get_param(blocks{8}, 'handle')];
Simulink.BlockDiagram.createSubSystem(sub);
Simulink.BlockDiagram.loadActiveConfigSet('rst', 'config.m');
rtwbuild('rst/Subsystem');
save_system('rst');
close_system('rst');
cd(oldPath);


%Solve the system and generate the RST parameters/
function [R, S, T]= solveRST(w0, zeta,Ts, Pz,Az,Bz)%solve
[Ts, Bp, Ap, Hr, Hs , dist, P, Bm, Am]=acquire_data(w0, zeta,Ts, Pz,Az,Bz);


%don't cancel
Bps=1; Bpu=Bp;


%SOLUTION
%Ap Hs S + Bp Hr R = P      (no zeros cancelled)
S_has_integrator=has_no_integrator(Ap);
if S_has_integrator
    Hs_full=conv(Hs, [1 -1]);
else
    Hs_full=Hs;
end
A=conv(Ap, Hs_full)';
B=conv(Bpu, Hr)';
nA=size(A); nA=nA(1)-1;%vertical vector size, power of z = size-1
nB=size(B); nB=nB(1)-1;
A=padarray(A, nB-1, 0, 'post');
B=padarray(B, nA-1, 0, 'post');
M=[];
for k=1:nB
    M=[M A];
    A=circshift(A, 1);
end
for k=(nB+1):(nB+nA)
    M=[M B];
    B=circshift(B, 1);
end
%M
n=size(M);  n=n(1);%M is a square matrix
nP=size(P); nP=nP(2);
P_full=padarray(P', n-nP, 0, 'post');
SR=M\P_full;

%Extract R, S, T
R=SR((nB+1):(nB+nA))';
S=SR(1:nB)';
if S_has_integrator
    S=conv(S, [1, -1]);
end
S=conv(S, Bps);
T=P/sum(Bpu);%(no zeros cancelled)


R=conv(R, Hr);
S=conv(S, Hs);
generateSimulink(Ts, Bp, Ap,Bm, Am,R,S,T);
