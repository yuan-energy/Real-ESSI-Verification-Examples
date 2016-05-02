
cur_dir=pwd;

cd (cur_dir);

div_subdir={'0one';'1half';'2quarter'};
% div_subdir=cellstr(div_subdir);
% i=1;
d_theta=zeros(11,1);
goal_gp_stress=zeros(3,1);
theory_stress=zeros(3,1);

for i_file=1:3

	cd (fullfile(cur_dir,div_subdir{i_file},'fei'));

	file=sprintf('t_1.h5.feioutput');
	gp_stress=h5read(file,...
	'/Model/Elements/Outputs'); 
	gp_stress=reshape(gp_stress,18,length(gp_stress)/18);


	gp_stress=gp_stress';
	gp_stress(:,1:12)=[];

	file=sprintf('t_1.h5.feioutput');
	gp_coor=h5read(file,...
	'/Model/Elements/Gauss_Point_Coordinates');  
	gp_coor=reshape(gp_coor,3,length(gp_coor)/3);
	gp_coor=gp_coor';
    gp_coor=single(gp_coor);
    
	gp_node_num=size(gp_coor,1);
	gp_node_num=linspace(1,gp_node_num,gp_node_num);
	
	% add the old node number to gassian points.. And then sort by x,y,z.
	gp_coor=[gp_node_num' gp_coor];
	gp_coor=sortrows(gp_coor,[2 3 4]);

	% This is the boundary gassian points, which has the minimum value and
	% will be compared with the theoretical solution. 
	goal_gp_num=gp_coor(1,1);
	goal_gp_coor=gp_coor(1,2:4);
	goal_gp_stress(i_file) = gp_stress (goal_gp_num,1);

	force=100;
	force_arm=6-goal_gp_coor(1) ;
	b_moment=force_arm*force;
	axis_y=0.5-goal_gp_coor(2) ;
	I_b=1/12;
	theory_stress(i_file) =b_moment*axis_y/I_b;
	% 
end


% cur_dir='/home/yuan/Dropbox/2plate_shell_veri/beam3Type_moreElem/1to6_cantilever/8brick/0one/fei';
% result_dir=pwd;
% cd (result_dir);
cd (cur_dir);

file_out=fopen('stress_brick27.dat','w');

fprintf(file_out,'goal_gp_stress = \t' );
for i_file=1:3
	fprintf(file_out,' %18.12f \t ',goal_gp_stress(i_file) );
end
fprintf(file_out,'\n' );

fprintf(file_out,'theory_stress = \t' );
for i_file=1:3
	fprintf(file_out,' %18.12f \t ',theory_stress(i_file) );
end
fprintf(file_out,'\n' );


fclose(file_out);

cd (cur_dir);







% 	beam_length=max(gp_coor(:));
% 	beam_height=max(gp_coor(:,3));
% 	beam_width=max(gp_coor(:,3));

% 	for i_node=1:gp_node_num
% 		if (gp_coor(i_node,1)==beam_length & ...
% 			gp_coor(i_node,2)==0 &...
% 			gp_coor(i_node,3)==0 )

% 			bottom_gp_node_num=i_node;
% 		end
% 	end

% 	for i_node=1:gp_node_num
% 		if (gp_coor(i_node,1)==beam_length & ...
% 			gp_coor(i_node,2)==0 &...
% 			gp_coor(i_node,3)==beam_height )

% 			top_gp_node_num=i_node;
% 		end
% 	end
% 	dx=abs(gp_stress(bottom_gp_node_num,1)-gp_stress(top_gp_node_num,1));

% 	d_theta(i_file) =atan(dx)*180/pi;
% end

