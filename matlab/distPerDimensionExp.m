function [] = distPerDimensionExp(utterance)
%distPerDimension Compare information across different dimensions
%   Given the datasets, plot the DTW distance for the given utterance
%   for the different models considered. 
close all;

histMatrix1 = zeros([7 2]); % POE, HTS 
dimensionList = [1 2 3 4 5 6 7];
for jj=1:7
    ii=dimensionList(jj);
    [original,~] = load_htkdata(strcat('../original/cmp/utt',int2str(utterance),'.cmp'));
    original = original(ii,:);

    fileID = fopen(strcat('../allTraj/traj/utt',int2str(utterance),'/dim',int2str(ii),'/trajExpertGV.txt'));
    expertGV = fscanf(fileID, '%f');
    fclose(fileID);
    [expertGVDist, ~,~] = dtw(original, expertGV);
    
    fileID = fopen(strcat('../allTraj/traj/utt',int2str(utterance),'/dim',int2str(ii),'/trajExpertAltGV.txt'));
    constraintGV = fscanf(fileID, '%f');
    fclose(fileID);
    [expertAltGVDist,~,~] = dtw(original, constraintGV);
    
    histMatrix1(ii,:) = [expertGVDist, expertAltGVDist];
 
end

% Plot the results
bar(histMatrix1);
xlabel('Dimension');
xticklabels({'1','2','3','4','5','6','7'})
ylabel('Distance');
%ylim([0 1e-3]);
legend('Expert GV 1', 'Expert GV 2');

end

