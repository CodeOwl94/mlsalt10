function [] = varPerUtterance( dimension )
%compareEachUtterance Compare information across different utterances
%   Given the datasets, plot the global variances for the given dimension
%   for the different models considered. 
close all;

histMatrix1 = zeros([9 3]); % Original, POE, HTS
histMatrix2 = zeros([9 3]); % Original, ExpGV, ConGV
histMatrix3 = zeros([9 3]); % POE, ExpGV, ConGV 

for ii=1:9 
    [original,~] = load_htkdata(strcat('../original/cmp/utt',int2str(ii),'.cmp'));
    original = original(dimension,:);
    
    [hts, ~] = load_traj(strcat('../traj-dur/utt',int2str(ii),'.mcep'),60);
    hts = hts(dimension,:);
    
    fileID = fopen(strcat('../allTraj/traj/utt',int2str(ii),'/dim',int2str(dimension),'/trajNoGV.txt'));
    poe = fscanf(fileID, '%f');
    fclose(fileID);

    fileID = fopen(strcat('../allTraj/traj/utt',int2str(ii),'/dim',int2str(dimension),'/trajExpertGV.txt'));
    expertGV = fscanf(fileID, '%f');
    fclose(fileID);
    
    fileID = fopen(strcat('../allTraj/traj/utt',int2str(ii),'/dim',int2str(dimension),'/trajConstraintGV.txt'));
    constraintGV = fscanf(fileID, '%f');
    fclose(fileID);
    
    histMatrix1(ii,:) = [var(original), var(hts), var(poe)];
    histMatrix2(ii,:) = [var(original), var(expertGV), var(constraintGV)];
    histMatrix3(ii,:) = [var(poe), var(expertGV), var(constraintGV)];
    
end

% Plot the results
bar(histMatrix1);
xlabel('Utterance');
ylabel('Variance');
%ylim([0 1e-3]);
legend('Original', 'HTS', 'PoE');

figure;
bar(histMatrix2);
xlabel('Utterance');
ylabel('Variance');
%ylim([0 1e-3]);
legend('Original', 'Expert GV', 'Constraint GV');

figure;
bar(histMatrix3);
xlabel('Utterance');
ylabel('Variance');
%ylim([0 1e-3]);
legend('PoE', 'Expert GV', 'Constraint GV');

end