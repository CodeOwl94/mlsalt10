function [] = varPerDimension( utterance )
%varPerDimension Compare information across different dimensions
%   Given the datasets, plot the global variances for the given utterance
%   for the different models considered. 
close all;

histMatrix1 = zeros([7 3]); % Original, POE, HTS
histMatrix2 = zeros([7 3]); % Original, ExpGV, ConGV
histMatrix3 = zeros([7 3]); % POE, ExpGV, ConGV 
dimensionList = [1 2 3 4 5 6 7];
for jj=1:7
    ii = dimensionList(jj);
    [original,~] = load_htkdata(strcat('../original/cmp/utt',int2str(utterance),'.cmp'));
    original = original(ii,:);
    
    [hts, ~] = load_traj(strcat('../traj-dur/utt',int2str(utterance),'.mcep'),60);
    hts = hts(ii,:);
    
    fileID = fopen(strcat('../allTraj/traj/utt',int2str(utterance),'/dim',int2str(ii),'/trajNoGV.txt'));
    poe = fscanf(fileID, '%f');
    fclose(fileID);

    fileID = fopen(strcat('../allTraj/traj/utt',int2str(utterance),'/dim',int2str(ii),'/trajExpertGV.txt'));
    expertGV = fscanf(fileID, '%f');
    fclose(fileID);
    
    fileID = fopen(strcat('../allTraj/traj/utt',int2str(utterance),'/dim',int2str(ii),'/trajConstraintGV.txt'));
    constraintGV = fscanf(fileID, '%f');
    fclose(fileID);
    
    histMatrix1(ii,:) = [var(original), var(hts), var(poe)];
    histMatrix2(ii,:) = [var(original), var(expertGV), var(constraintGV)];
    histMatrix3(ii,:) = [var(poe), var(expertGV), var(constraintGV)];
    
end

% Plot the results
bar(histMatrix1);
xlabel('Dimension');
ylabel('Variance');
xticklabels({'1','2','3','4','5','6','7'})
ylim([0 5]);
legend('Original', 'HTS', 'PoE');

figure;
bar(histMatrix2);
xlabel('Dimension');
xticklabels({'1','2','3','4','5','6','7'})
ylabel('Variance');
ylim([0 5]);
legend('Original', 'Expert GV', 'Constraint GV');

figure;
bar(histMatrix3);
xlabel('Dimension');
xticklabels({'1','2','3','4','5','6','7'})
ylabel('Variance');
ylim([0 5]);
legend('PoE', 'Expert GV', 'Constraint GV');

end