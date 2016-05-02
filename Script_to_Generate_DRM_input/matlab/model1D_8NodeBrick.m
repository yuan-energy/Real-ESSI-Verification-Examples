clc
clear
% Input the DRM boundary node, exterior node and DRM element information.
load DRMbound_node.txt
load DRMexterior_node.txt
load DRMelements.txt

% Organize the node and element informatin.
DRMNode=int32([ DRMbound_node; DRMexterior_node ]);
DRMElement=int32([DRMelements]);
n_b=int32(length(DRMbound_node));
n_e=int32(length(DRMexterior_node));

% Designate whether the node is boundary node or exterior node.
one_b=linspace(1,1,n_b);
zero_e=linspace(0,0,n_e);
isboundary=int32([ one_b zero_e]);

% Designate the time length and timesteps
dt=0.01;
timesteps=1000;
time=linspace(dt,dt*timesteps,timesteps);

% Input the DRM motion from 1D Real ESSI model
load accel.dat
load displ.dat

% Organize the motion for different nodes at different elevations
DRM_displ=zeros(3*length(DRMNode),length(time));
DRM_acc=zeros(3*length(DRMNode),length(time));

for i=1:n_b
	DRM_displ(i*3-2,:)=displ(2,1:timesteps);
	DRM_acc(i*3-2,:)=accel(2,1:timesteps);
end

for i=(n_b+1) : n_b+n_e
	DRM_displ(i*3-2,:)=displ(1,1:timesteps);
	DRM_acc(i*3-2,:)=accel(1,1:timesteps);
end

% Use a matlab function to output the HDF5 DRM motion.
delete input.hdf5
write_DRM_hdf5('input.hdf5',DRM_displ,DRM_acc,DRMNode,DRMElement,isboundary,n_b,n_e,time);
