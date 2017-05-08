function [] = distPerUtterance(dimension)
%compareEachUtterance Compare information across different utterances
%   Given the datasets, plot the DTW distance for the given dimension
%   for the different models considered. 
close all;

histMatrix1 = zeros([9 2]); % POE, HTS
histMatrix2 = zeros([9 3]); % POE, ExpGV, ConGV 

for ii=1:9 
    [original,~] = load_htkdata(strcat('../original/cmp/utt',int2str(ii),'.cmp'));
    original = original(dimension,:);
    
    [hts, ~] = load_traj(strcat('../traj-dur/utt',int2str(ii),'.mcep'),60);
    hts = hts(dimension,:);
    [htsDist,~,~] = dtw(original,hts);
    
    fileID = fopen(strcat('../allTraj/traj/utt',int2str(ii),'/dim',int2str(dimension),'/trajNoGV.txt'));
    poe = fscanf(fileID, '%f');
    fclose(fileID);
    [poeDist,~,~] = dtw(original, poe);

    fileID = fopen(strcat('../allTraj/traj/utt',int2str(ii),'/dim',int2str(dimension),'/trajExpertGV.txt'));
    expertGV = fscanf(fileID, '%f');
    fclose(fileID);
    [expertGVDist, ~,~] = dtw(original, expertGV);
    
    fileID = fopen(strcat('../allTraj/traj/utt',int2str(ii),'/dim',int2str(dimension),'/trajConstraintGV.txt'));
    constraintGV = fscanf(fileID, '%f');
    fclose(fileID);
    [constraintGVDist,~,~] = dtw(original, constraintGV);
    
    histMatrix1(ii,:) = [htsDist, poeDist];
    histMatrix2(ii,:) = [poeDist, expertGVDist, constraintGVDist];
 
end

% Plot the results
bar(histMatrix1);
xlabel('Utterance');
ylabel('Distance');
%ylim([0 1e-3]);
legend('HTS', 'PoE');

figure;
bar(histMatrix2);
xlabel('Utterance');
ylabel('Distance');
%ylim([0 1e-3]);
legend('PoE', 'Expert GV', 'Constraint GV');
end

