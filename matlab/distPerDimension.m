function [] = distPerDimension(utterance)
%distPerDimension Compare information across different dimensions
%   Given the datasets, plot the DTW distance for the given utterance
%   for the different models considered. 
close all;

histMatrix1 = zeros([7 2]); % POE, HTS
histMatrix2 = zeros([7 3]); % POE, ExpGV, ConGV 
dimensionList = [1 2 3 4 5 6 7];
for jj=1:7
    ii=dimensionList(jj);
    [original,~] = load_htkdata(strcat('../original/cmp/utt',int2str(utterance),'.cmp'));
    original = original(ii,:);
    
    [hts, ~] = load_traj(strcat('../traj-dur/utt',int2str(utterance),'.mcep'),60);
    hts = hts(ii,:);
    [htsDist,~,~] = dtw(original,hts);
    
    fileID = fopen(strcat('../allTraj/traj/utt',int2str(utterance),'/dim',int2str(ii),'/trajNoGV.txt'));
    poe = fscanf(fileID, '%f');
    fclose(fileID);
    [poeDist,~,~] = dtw(original, poe);

    fileID = fopen(strcat('../allTraj/traj/utt',int2str(utterance),'/dim',int2str(ii),'/trajExpertGV.txt'));
    expertGV = fscanf(fileID, '%f');
    fclose(fileID);
    [expertGVDist, ~,~] = dtw(original, expertGV);
    
    fileID = fopen(strcat('../allTraj/traj/utt',int2str(utterance),'/dim',int2str(ii),'/trajConstraintGV.txt'));
    constraintGV = fscanf(fileID, '%f');
    fclose(fileID);
    [constraintGVDist,~,~] = dtw(original, constraintGV);
    
    histMatrix1(ii,:) = [htsDist, poeDist];
    histMatrix2(ii,:) = [poeDist, expertGVDist, constraintGVDist];
 
end

% Plot the results
bar(histMatrix1);
xlabel('Dimension');
xticklabels({'1','2','3','4','5','6','7'})
ylabel('Distance');
%ylim([0 1e-3]);
legend('HTS', 'PoE');

figure;
bar(histMatrix2);
xlabel('Dimension');
xticklabels({'1','2','3','4','5','6','7'})
ylabel('Distance');
%ylim([0 1e-3]);
legend('PoE', 'Expert GV', 'Constraint GV');
end

