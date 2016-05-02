% Created by Chao Luo
function write_DRM_hdf5(filename,DRMu,DRMAcc,DRMNodes,DRMElements,Is_b,nb,ne,time)
h5create(filename,'/Time',[length(time)]);
h5create(filename,'/Elements',length(DRMElements),'Datatype','int32');
h5create(filename,'/DRM Nodes',length(DRMNodes),'Datatype','int32');
h5create(filename,'/Number of Exterior Nodes',length(ne),'Datatype','int32');
h5create(filename,'/Number of Boundary Nodes',length(nb),'Datatype','int32');
h5create(filename,'/Is Boundary Node',length(Is_b),'Datatype','int32');
h5create(filename,'/Displacements',size(DRMu'),'ChunkSize',[50 3]);
h5create(filename,'/Accelerations',size(DRMAcc'),'ChunkSize',[50 3]);

h5write(filename,'/Time',time');
h5write(filename,'/Elements',DRMElements');
h5write(filename,'/DRM Nodes',DRMNodes');
h5write(filename,'/Number of Exterior Nodes',ne);
h5write(filename,'/Number of Boundary Nodes',nb);
h5write(filename,'/Is Boundary Node',(Is_b+0)');
h5write(filename,'/Displacements',DRMu');
h5write(filename,'/Accelerations',DRMAcc');