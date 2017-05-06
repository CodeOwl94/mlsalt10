function [] = plotComparison( utterance, dimension)
%plotComparison Compare original trajectories against generated
%trajectories
%   Given an utterance and dimension, plot out the original trajectory, poe
%   no GV trajectory, expert GV trajectory and constrained GV trajectory

% Obtain the original trajectory
originalFile = strcat('../original/cmp/utt', int2str(utterance), '.cmp');
[original,~] = load_htkdata(originalFile);
original = (original(dimension,:))';

% Path where all generated trajectories are stored
generatedPath = strcat('../allTraj/traj/utt', int2str(utterance), '/dim', int2str(dimension), '/traj');

% PoE no GV trajectory
generatedFile = strcat(generatedPath, 'NoGV.txt');
fileID = fopen(generatedFile);
generatedNoGV = fscanf(fileID, '%f');
fclose(fileID);

% PoE Expert GV trajectory
generatedFile = strcat(generatedPath, 'ExpertGV.txt');
fileID = fopen(generatedFile);
generatedExpertGV = fscanf(fileID, '%f');
fclose(fileID);

% PoE Constraint GV trajectory
generatedFile = strcat(generatedPath, 'ConstraintGV.txt');
fileID = fopen(generatedFile);
generatedConstraintGV = fscanf(fileID, '%f');
fclose(fileID);

figure;
plot(original);
hold on;
plot(generatedNoGV);
hold on;
plot(generatedExpertGV);
hold on;
plot(generatedConstraintGV);
legend('Original Trajectories', 'No GV', 'Expert GV', 'Constraint GV');


end

